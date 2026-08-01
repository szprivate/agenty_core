"""Relay ComfyUI's own console output for as long as a job is running.

The progress stream says *where* a run is — which node is executing, how far
through its steps.  ComfyUI's terminal says *what it is doing*: which model is
being loaded onto which device, the dtype it settled on, the warning that a
checkpoint carries no text-encoder weights, how much got unloaded to make room.
When a run sits on "Running node 12" for two minutes, that terminal is the only
thing separating "a 25 GB checkpoint is staging" from "this is wedged" — and it
was visible only to whoever happened to be looking at the ComfyUI window.

ComfyUI already publishes it.  ``PATCH /internal/logs/subscribe`` registers a
client id, and every stdout/stderr flush is then pushed to that client's
websocket as a ``logs`` event (see ComfyUI's
``api_server/services/terminal_service.py``).  This module holds exactly one
such subscription — its own socket, its own client id — for as long as anything
is watching a job, and hands the finished lines to the watcher.

Two things it deliberately does not do:

* **Emit unterminated lines.**  tqdm redraws its bar with a bare carriage
  return several times a second; relaying that would bury the run in its own
  progress bar, and the executor already draws one from the websocket
  ``progress`` events.  Only newline-terminated lines are published — which is
  why a finished sampler still reports its closing ``100%|...`` line, the one
  that carries the timing.
* **Fan out.**  ComfyUI has a single console for the whole process, so a batch
  of eight monitored jobs must not print eight copies of it.  Lines go to the
  oldest attached watcher only; when that one detaches the next takes over.

The tap is keyed by event loop rather than global: a host that runs each turn
on its own loop gets its own tap (and its own console copy) instead of sharing
an ``Event`` across loops, which would not work at all.
"""

from __future__ import annotations

import asyncio
import contextlib
import json
import logging
import os
import re
import threading
import uuid
from collections import deque
from urllib.parse import urlparse

logger = logging.getLogger("agentY.comfyui_console")

# How many lines a watcher may fall behind before the oldest are dropped.  A
# watcher is drained every time its job stream comes round, so this only fills
# when a node dumps a wall of text at once (a traceback, a model summary).
MAX_PENDING = 200

# CSI/OSC escapes.  ComfyUI colours its own log lines, and some nodes emit
# cursor moves; neither survives a trip into a chat panel.
_ANSI_RE = re.compile(r"\x1b\[[0-9;?]*[ -/]*[@-~]|\x1b\][^\x07\x1b]*(?:\x07|\x1b\\)")


def console_enabled(explicit: bool | None = None) -> bool:
    """Whether ComfyUI console lines are relayed at all.

    An explicit argument wins (the caller read a setting); otherwise
    ``AGENTY_COMFY_CONSOLE`` decides, defaulting to on.
    """
    if explicit is not None:
        return bool(explicit)
    env = os.environ.get("AGENTY_COMFY_CONSOLE")
    if env is not None and env.strip():
        return env.strip().lower() not in ("0", "false", "no", "off")
    return True


class _LineAssembler:
    """Reassemble raw ``write()`` chunks into finished terminal lines.

    The entries ComfyUI ships are whatever was handed to ``stdout.write`` —
    arbitrary fragments, not lines.  A single log line can arrive in three
    pieces, and a progress bar arrives as dozens of carriage-return redraws of
    the same line.
    """

    def __init__(self) -> None:
        self._buf = ""

    def feed(self, chunk: str) -> list[str]:
        """Add a chunk; return the lines it completed (possibly none)."""
        self._buf += _ANSI_RE.sub("", chunk)
        lines: list[str] = []
        while True:
            cut = self._buf.find("\n")
            if cut < 0:
                break
            line, self._buf = self._buf[:cut], self._buf[cut + 1:]
            # Everything before the last carriage return was overwritten in
            # place, so only the final segment was ever on screen.
            line = line.rsplit("\r", 1)[-1].rstrip()
            if line.strip():
                lines.append(line)
        # Same collapse for the unfinished tail: without it a sampler that
        # redraws its bar 200 times leaves all 200 redraws in the buffer,
        # waiting for a newline that closes a line nobody wants anyway.
        if "\r" in self._buf:
            self._buf = self._buf.rsplit("\r", 1)[-1]
        return lines


class ConsoleWatcher:
    """One consumer's view of the console: a bounded backlog it drains."""

    def __init__(self) -> None:
        self._lines: deque[str] = deque(maxlen=MAX_PENDING)
        self._dropped = 0
        self._ready = asyncio.Event()
        self._tap: _ConsoleTap | None = None
        self._loop: object | None = None

    def _offer(self, lines: list[str]) -> None:
        for line in lines:
            if len(self._lines) == MAX_PENDING:
                self._dropped += 1     # deque discards the oldest
            self._lines.append(line)
        if self._lines:
            self._ready.set()

    async def get(self) -> list[str]:
        """Wait for console output, then return every line since the last call."""
        await self._ready.wait()
        self._ready.clear()
        out = list(self._lines)
        self._lines.clear()
        if self._dropped:
            out.insert(0, f"… {self._dropped} earlier console line(s) dropped")
            self._dropped = 0
        return out

    def close(self) -> None:
        """Stop watching.  Idempotent; safe from a generator's ``finally``."""
        tap, loop, self._tap = self._tap, self._loop, None
        if tap is None:
            return
        with _registry_lock:
            done = tap.remove(self)
            if done and _taps.get(loop) is tap:
                del _taps[loop]
        if done:
            tap.stop()


class _ConsoleTap:
    """The single subscription: one websocket, one client id, N watchers."""

    def __init__(self) -> None:
        self.client_id = f"agentY-console-{uuid.uuid4().hex[:8]}"
        self._watchers: list[ConsoleWatcher] = []
        self._assembler = _LineAssembler()
        self._task: asyncio.Task | None = None

    # ── watcher bookkeeping (called under the registry lock) ────────────────
    def add(self, watcher: ConsoleWatcher) -> None:
        self._watchers.append(watcher)

    def remove(self, watcher: ConsoleWatcher) -> bool:
        """Drop *watcher*; return True when nobody is left watching."""
        with contextlib.suppress(ValueError):
            self._watchers.remove(watcher)
        return not self._watchers

    def _publish(self, lines: list[str]) -> None:
        # Oldest watcher only — see the module docstring on fan-out.
        if self._watchers:
            self._watchers[0]._offer(lines)

    # ── lifecycle ───────────────────────────────────────────────────────────
    def start(self) -> None:
        if self._task is None or self._task.done():
            self._task = asyncio.ensure_future(self._run())

    def stop(self) -> None:
        """Cancel the reader.  Not awaited: the unsubscribe in its ``finally``
        is best-effort, and ComfyUI drops a subscriber whose socket has gone
        anyway, so a teardown that never gets to run costs nothing."""
        task, self._task = self._task, None
        if task is not None:
            task.cancel()

    def _subscribe(self, enabled: bool) -> None:
        from agenty_core.utils.comfyui_client import get_client

        try:
            get_client().patch(
                "/internal/logs/subscribe",
                {"clientId": self.client_id, "enabled": enabled},
                timeout=5,
            )
        except Exception as exc:  # noqa: BLE001 — an old ComfyUI simply has no route
            logger.debug("console tap could not %ssubscribe: %s",
                         "" if enabled else "un", exc)
            raise

    async def _run(self) -> None:
        import websockets

        from agenty_core.utils.comfyui_client import get_client

        client = get_client()
        parsed = urlparse(client.base_url)
        scheme = "wss" if parsed.scheme == "https" else "ws"
        ws_url = f"{scheme}://{parsed.netloc}/ws?clientId={self.client_id}"

        connect_kwargs: dict = {"max_size": None}
        if client.api_key:
            connect_kwargs["additional_headers"] = [
                ("Authorization", f"Bearer {client.api_key}")
            ]

        try:
            async with websockets.connect(ws_url, **connect_kwargs) as ws:
                # Subscribe only once the socket exists: ComfyUI sends log
                # events to a client id, and drops the subscription the moment
                # it finds no socket registered under it.
                self._subscribe(True)
                try:
                    while True:
                        raw = await ws.recv()
                        if isinstance(raw, (bytes, bytearray)):
                            continue          # binary preview frames
                        try:
                            msg = json.loads(raw)
                        except json.JSONDecodeError:
                            continue
                        if msg.get("type") != "logs":
                            continue
                        entries = (msg.get("data") or {}).get("entries") or []
                        lines: list[str] = []
                        for entry in entries:
                            if isinstance(entry, dict):
                                lines.extend(self._assembler.feed(str(entry.get("m", ""))))
                        if lines:
                            self._publish(lines)
                finally:
                    with contextlib.suppress(Exception):
                        self._subscribe(False)
        except asyncio.CancelledError:
            raise
        except Exception as exc:  # noqa: BLE001 — never let this break a run
            logger.debug("console tap stopped: %s", exc)


# One tap per event loop.  A plain threading lock is enough: nothing inside the
# critical section awaits, and hosts that run turns on separate loops (each in
# its own thread) would otherwise share asyncio primitives across loops.
_taps: dict[object, _ConsoleTap] = {}
_registry_lock = threading.Lock()


def attach(enabled: bool | None = None) -> ConsoleWatcher | None:
    """Start watching ComfyUI's console; ``close()`` the result when done.

    Returns ``None`` when relaying is switched off, so callers can carry one
    optional handle rather than branching twice.  Must be called from a running
    event loop — the tap's reader lives on it.
    """
    if not console_enabled(enabled):
        return None

    loop = asyncio.get_running_loop()
    watcher = ConsoleWatcher()
    with _registry_lock:
        tap = _taps.get(loop)
        if tap is None:
            tap = _taps[loop] = _ConsoleTap()
        tap.add(watcher)
    watcher._tap, watcher._loop = tap, loop
    tap.start()
    return watcher
