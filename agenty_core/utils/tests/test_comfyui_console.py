"""Tests for the ComfyUI console relay and its use by the job progress stream.

Nothing here touches a real ComfyUI: the tap's reader is replaced with one that
publishes fixed lines, and the progress stream is driven by a scripted fake
websocket.
"""

import asyncio
import sys
import unittest

from agenty_core.utils import comfyui_console as cc


def run(coro):
    return asyncio.run(coro)


# ── line assembly ───────────────────────────────────────────────────────────
class LineAssemblerTest(unittest.TestCase):
    def setUp(self):
        self.asm = cc._LineAssembler()

    def test_completed_line_is_emitted(self):
        self.assertEqual(self.asm.feed("[INFO] got prompt\n"), ["[INFO] got prompt"])

    def test_line_split_across_chunks(self):
        self.assertEqual(self.asm.feed("[INFO] model_"), [])
        self.assertEqual(self.asm.feed("type FLUX\n"), ["[INFO] model_type FLUX"])

    def test_several_lines_in_one_chunk(self):
        self.assertEqual(
            self.asm.feed("one\ntwo\nthree\n"), ["one", "two", "three"]
        )

    def test_ansi_colour_is_stripped(self):
        out = self.asm.feed("\x1b[1m\x1b[33m[WARNING]\x1b[0m no CLIP weights\n")
        self.assertEqual(out, ["[WARNING] no CLIP weights"])

    def test_unterminated_line_is_held_back(self):
        # The redrawing part of a progress bar never ends in a newline, and the
        # executor already draws its own bar from the websocket progress events.
        self.assertEqual(self.asm.feed("\r 50%|#####     | 4/8"), [])

    def test_final_progress_line_survives(self):
        # ...but the closing redraw does end in a newline, and it carries the
        # timing, so it is the one line of the bar worth relaying.
        self.asm.feed("\r 50%|#####     | 4/8 [00:14<00:14]")
        out = self.asm.feed("\r100%|##########| 8/8 [00:29<00:00,  3.63s/it]\n")
        self.assertEqual(out, ["100%|##########| 8/8 [00:29<00:00,  3.63s/it]"])

    def test_redraws_do_not_accumulate_in_the_buffer(self):
        for i in range(500):
            self.assertEqual(self.asm.feed(f"\r{i}%|#### | {i}/500"), [])
        self.assertLess(len(self.asm._buf), 200)

    def test_blank_lines_are_dropped(self):
        self.assertEqual(self.asm.feed("\n   \n\nreal\n"), ["real"])


# ── watcher backlog ─────────────────────────────────────────────────────────
class ConsoleWatcherTest(unittest.TestCase):
    def test_get_returns_everything_since_the_last_call(self):
        async def go():
            w = cc.ConsoleWatcher()
            w._offer(["a", "b"])
            first = await w.get()
            w._offer(["c"])
            return first, await w.get()

        first, second = run(go())
        self.assertEqual(first, ["a", "b"])
        self.assertEqual(second, ["c"])

    def test_get_waits_for_output(self):
        async def go():
            w = cc.ConsoleWatcher()
            asyncio.get_running_loop().call_later(0.02, w._offer, ["late"])
            return await asyncio.wait_for(w.get(), timeout=2)

        self.assertEqual(run(go()), ["late"])

    def test_overflow_is_reported_not_silently_swallowed(self):
        async def go():
            w = cc.ConsoleWatcher()
            w._offer([f"line {i}" for i in range(cc.MAX_PENDING + 5)])
            return await w.get()

        out = run(go())
        self.assertEqual(len(out), cc.MAX_PENDING + 1)   # + the notice
        self.assertIn("5 earlier console line(s) dropped", out[0])
        self.assertEqual(out[-1], f"line {cc.MAX_PENDING + 4}")


# ── attach / fan-out / teardown ─────────────────────────────────────────────
async def _idle_run(self):
    """Stand-in for _ConsoleTap._run that never opens a socket."""
    await asyncio.sleep(3600)


class TapLifecycleTest(unittest.TestCase):
    def setUp(self):
        self._real_run = cc._ConsoleTap._run
        cc._ConsoleTap._run = _idle_run
        cc._taps.clear()

    def tearDown(self):
        cc._ConsoleTap._run = self._real_run
        cc._taps.clear()

    def test_watchers_on_one_loop_share_a_single_subscription(self):
        async def go():
            a, b = cc.attach(True), cc.attach(True)
            self.assertEqual(len(cc._taps), 1)
            self.assertIs(a._tap, b._tap)
            a.close()
            b.close()

        run(go())

    def test_only_the_oldest_watcher_receives_lines(self):
        # ComfyUI has one console; a batch of monitored jobs must not print one
        # copy of it per member.
        async def go():
            a, b = cc.attach(True), cc.attach(True)
            a._tap._publish(["[INFO] got prompt"])
            first = await asyncio.wait_for(a.get(), timeout=1)
            self.assertEqual(first, ["[INFO] got prompt"])
            self.assertEqual(list(b._lines), [])
            a.close()
            b.close()

        run(go())

    def test_the_next_watcher_takes_over_when_the_first_leaves(self):
        async def go():
            a, b = cc.attach(True), cc.attach(True)
            tap = a._tap
            a.close()
            tap._publish(["[INFO] still going"])
            self.assertEqual(await asyncio.wait_for(b.get(), timeout=1),
                             ["[INFO] still going"])
            b.close()

        run(go())

    def test_last_watcher_out_cancels_the_reader(self):
        async def go():
            w = cc.attach(True)
            tap = w._tap
            w.close()
            self.assertEqual(cc._taps, {})
            await asyncio.sleep(0)      # let the cancellation land
            return tap

        tap = run(go())
        self.assertIsNone(tap._task)

    def test_close_is_idempotent(self):
        async def go():
            w = cc.attach(True)
            w.close()
            w.close()

        run(go())

    def test_disabled_attach_returns_nothing(self):
        async def go():
            self.assertIsNone(cc.attach(False))
            self.assertEqual(cc._taps, {})

        run(go())


class ConsoleEnabledTest(unittest.TestCase):
    def test_explicit_wins(self):
        self.assertTrue(cc.console_enabled(True))
        self.assertFalse(cc.console_enabled(False))

    def test_env_is_read_when_nothing_explicit(self):
        import os
        old = os.environ.get("AGENTY_COMFY_CONSOLE")
        try:
            for val, want in (("0", False), ("off", False), ("1", True), ("", True)):
                os.environ["AGENTY_COMFY_CONSOLE"] = val
                self.assertIs(cc.console_enabled(None), want, val)
            del os.environ["AGENTY_COMFY_CONSOLE"]
            self.assertTrue(cc.console_enabled(None))     # default: on
        finally:
            if old is None:
                os.environ.pop("AGENTY_COMFY_CONSOLE", None)
            else:
                os.environ["AGENTY_COMFY_CONSOLE"] = old


# ── the progress stream, driven by a scripted socket ────────────────────────
class _FakeWS:
    """Replays a script of websocket frames, then goes quiet.

    A float in the script is a pause rather than a frame, which is how a test
    puts a gap between two events for the console to speak into.
    """

    def __init__(self, frames):
        self._frames = list(frames)

    async def __aenter__(self):
        return self

    async def __aexit__(self, *exc):
        return False

    async def recv(self):
        while self._frames:
            frame = self._frames.pop(0)
            if isinstance(frame, (int, float)):
                await asyncio.sleep(frame)
                continue
            return frame
        await asyncio.sleep(3600)


class _FakeClient:
    base_url = "http://127.0.0.1:8188"
    api_key = ""

    def __init__(self, history=None):
        self.history = history or {}

    def get(self, path, **kwargs):
        if path.startswith("/history"):
            return self.history
        if path == "/queue":
            return {"queue_running": [], "queue_pending": []}
        return {}

    def patch(self, *args, **kwargs):
        return {}


_DONE_HISTORY = {
    "p1": {
        "status": {"status_str": "success", "completed": True},
        "outputs": {"9": {"images": [{"filename": "out.png", "subfolder": "", "type": "output"}]}},
    }
}


class ProgressStreamTest(unittest.TestCase):
    """The relay is wired into the job stream without disturbing it."""

    def setUp(self):
        import json as _json

        from agenty_core.utils import comfyui_client, comfyui_progress

        self.progress = comfyui_progress
        self._real_run = cc._ConsoleTap._run
        self._real_get_client = comfyui_client.get_client
        cc._taps.clear()

        self.frames = [
            _json.dumps({"type": "executing",
                         "data": {"node": "12", "prompt_id": "p1"}}),
            _json.dumps({"type": "execution_success", "data": {"prompt_id": "p1"}}),
        ]
        # A client whose /history is empty until the job reports success, so the
        # stream does not short-circuit on its pre-check.
        self.client = _FakeClient()

        fake_ws_module = type(sys)("websockets")
        fake_ws_module.connect = lambda url, **kw: _FakeWS(self.frames)
        self._old_ws = sys.modules.get("websockets")
        sys.modules["websockets"] = fake_ws_module
        comfyui_client.get_client = lambda: self.client

    def tearDown(self):
        from agenty_core.utils import comfyui_client

        cc._ConsoleTap._run = self._real_run
        comfyui_client.get_client = self._real_get_client
        if self._old_ws is None:
            sys.modules.pop("websockets", None)
        else:
            sys.modules["websockets"] = self._old_ws
        cc._taps.clear()

    def _collect(self, console):
        async def go():
            out = []
            gen = self.progress.stream_comfyui_job("p1", "c1", console=console)
            try:
                async for event in gen:
                    out.append(event)
                    if isinstance(event, dict):
                        break
            finally:
                await gen.aclose()
            return out

        return run(asyncio.wait_for(go(), timeout=10))

    def test_console_lines_are_relayed_alongside_progress(self):
        async def talkative(tap_self):
            await asyncio.sleep(0.05)
            tap_self._publish(["[INFO] got prompt", "[INFO] model_type FLUX"])
            self.client.history = _DONE_HISTORY
            await asyncio.sleep(3600)

        cc._ConsoleTap._run = talkative
        # Hold the success frame back until the console has spoken, so the two
        # sources genuinely interleave.
        self.frames.insert(1, 0.15)
        out = self._collect(True)

        self.assertIn("🖥 [INFO] got prompt", out)
        self.assertIn("🖥 [INFO] model_type FLUX", out)
        self.assertTrue(any(isinstance(e, str) and "Running node 12" in e for e in out))
        self.assertIsInstance(out[-1], dict)
        self.assertIn("history", out[-1])

    def test_console_off_yields_no_console_lines(self):
        async def talkative(tap_self):
            tap_self._publish(["[INFO] should not appear"])
            await asyncio.sleep(3600)

        cc._ConsoleTap._run = talkative
        self.client.history = _DONE_HISTORY
        out = self._collect(False)

        self.assertFalse([e for e in out if isinstance(e, str) and e.startswith("🖥")])
        self.assertIsInstance(out[-1], dict)
        self.assertEqual(cc._taps, {})       # nothing was ever attached

    def test_a_broken_relay_does_not_take_the_run_down(self):
        async def explodes(tap_self):
            await asyncio.sleep(0.02)
            raise RuntimeError("socket died")

        cc._ConsoleTap._run = explodes
        self.client.history = _DONE_HISTORY
        out = self._collect(True)

        self.assertIsInstance(out[-1], dict)
        self.assertIn("history", out[-1])    # the job still completed normally

    def test_the_tap_is_released_when_the_stream_ends(self):
        cc._ConsoleTap._run = _idle_run
        self.client.history = _DONE_HISTORY
        self._collect(True)
        self.assertEqual(cc._taps, {})


if __name__ == "__main__":
    unittest.main()
