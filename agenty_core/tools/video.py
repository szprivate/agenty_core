"""Shot detection and splitting.

``split_video_into_shots`` finds where a video cuts and writes one file per shot,
so a supplied clip can be worked on shot by shot — restyle one, feed each to a
per-shot workflow, or just find out where the cuts are before deciding anything.

Two halves, and they fail differently, which is why they are kept apart below:
**detection** is PySceneDetect reading the frames, and **cutting** is ffmpeg
writing the files. A machine can perfectly well detect and be unable to write
(no ffmpeg), so the cut list is still reported when that happens rather than the
whole call coming back as a failure.
"""

from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path
from shutil import which

from agenty_core._compat import tool

# Where a shot boundary is looked for. `content` compares consecutive frames in
# HSV and fires on the discontinuity a hard cut makes — the right default for
# edited footage. `adaptive` scores each frame against a rolling window instead,
# which is what stops a whip pan or a strobe from reading as a cut; it is the one
# to reach for on handheld or high-motion material.
_DETECTORS = ("content", "adaptive")

# A boundary this close to the last one is a flash, a flicker or a one-frame
# glitch rather than a shot. Stated in seconds and converted to frames for the
# detector, because "shorter than half a second" is something a person can judge
# and "shorter than 15 frames" depends on a frame rate they would have to look up.
_MIN_SHOT_SECONDS = 0.4

# Writing a thousand files because a detector misfired on a strobe is not a
# result, it is a mess someone has to clean up. The cap is on WRITING; detection
# still reports everything it found, so "why so many" stays answerable.
_MAX_SHOTS = 200

_FFMPEG_TIMEOUT = 900   # seconds per shot — a long 4K re-encode is not a hang


def _resolve_video(path: str) -> str | None:
    """Resolve a video path: as given, ``~``-expanded, then ComfyUI's input dir.

    The last one matters because the agent is usually holding a bare loader
    filename off the canvas ("clip.mp4"), not a path.
    """
    raw = (path or "").strip().strip('"')
    if not raw:
        return None
    p = Path(os.path.expanduser(raw))
    if p.is_file():
        return str(p.resolve())
    try:
        from agenty_core.tools.comfyui import get_comfyui_dirs
        dirs = json.loads(get_comfyui_dirs())
        in_dir = dirs.get("input_dir") if isinstance(dirs, dict) else None
        if in_dir and in_dir != "unknown":
            cand = Path(in_dir) / p.name
            if cand.is_file():
                return str(cand.resolve())
    except Exception:  # noqa: BLE001
        pass
    return None


def _ffmpeg_exe() -> str | None:
    """The ffmpeg binary to cut with.

    Prefers the one ``imageio-ffmpeg`` ships, because it is already a dependency
    and it is present whether or not the machine has ffmpeg on PATH — which on
    Windows it usually does not. Falls back to PATH so a system build still works
    if the wheel's binary is ever missing.
    """
    try:
        import imageio_ffmpeg
        exe = imageio_ffmpeg.get_ffmpeg_exe()
        if exe and Path(exe).is_file():
            return exe
    except Exception:  # noqa: BLE001
        pass
    return which("ffmpeg")


def _timecode(seconds: float) -> str:
    """``12.4`` → ``00:00:12.400`` — the shape scenedetect's own timecodes take."""
    s = max(0.0, float(seconds or 0.0))
    h, rem = divmod(s, 3600.0)
    m, sec = divmod(rem, 60.0)
    return f"{int(h):02d}:{int(m):02d}:{sec:06.3f}"


def _shots_dir(source: Path, output_dir: str = "") -> Path:
    """Where the shots go: one folder per source clip.

    Per source, because splitting a second clip into the same place interleaves
    two films' shots under names that both start at 001. Defaults under the
    agent's own videos directory so the shots land where every other piece of
    generated media does.
    """
    if str(output_dir or "").strip():
        d = Path(os.path.expanduser(str(output_dir).strip().strip('"')))
    else:
        base = None
        try:
            from agenty_core.tools.comfyui import get_agent_output_dirs
            base = (json.loads(get_agent_output_dirs()) or {}).get("videos")
        except Exception:  # noqa: BLE001
            base = None
        d = (Path(base) if base else source.parent) / f"{source.stem}_shots"
    d.mkdir(parents=True, exist_ok=True)
    return d


def _detect_shots(path: str, detector: str, threshold: float,
                  min_shot_seconds: float) -> tuple[list, dict]:
    """``(shots, meta)`` — each shot ``(start_s, end_s, start_tc, end_tc)``.

    PySceneDetect returns an EMPTY list when it finds no cuts, and that does not
    mean "nothing here": it means the whole file is one shot. It is turned into a
    single shot spanning the clip, so no caller has to know the difference —
    reading the empty list as failure is how a perfectly good single-take clip
    becomes an error message.
    """
    from scenedetect import AdaptiveDetector, ContentDetector, detect, open_video

    video = open_video(path)
    fps = float(video.frame_rate or 0.0) or 25.0
    duration = float(video.duration.get_seconds()) if video.duration is not None else 0.0
    min_len = max(1, int(round(max(0.0, float(min_shot_seconds)) * fps)))

    if str(detector).strip().lower() == "adaptive":
        det = AdaptiveDetector(adaptive_threshold=float(threshold), min_scene_len=min_len)
    else:
        det = ContentDetector(threshold=float(threshold), min_scene_len=min_len)

    found = detect(path, det, show_progress=False)
    meta = {"fps": round(fps, 3), "duration_s": round(duration, 3),
            "detector": str(detector).strip().lower(), "threshold": float(threshold)}
    if not found:
        return [(0.0, duration, "00:00:00.000", _timecode(duration))], dict(meta, cuts=0)
    shots = [(round(a.get_seconds(), 3), round(b.get_seconds(), 3),
              a.get_timecode(), b.get_timecode()) for a, b in found]
    return shots, dict(meta, cuts=max(0, len(shots) - 1))


def _cut_one(exe: str, source: str, dest: Path, start: float, duration: float,
             fast: bool) -> tuple[bool, str]:
    """Cut ``[start, start + duration)`` out of *source* into *dest*.

    ``-ss`` goes BEFORE ``-i`` (fast seek, still frame-accurate in modern ffmpeg)
    and the length is given as ``-t``, never ``-to``: with a pre-input seek, what
    ``-to`` measures from has changed between ffmpeg versions, and a shot that
    silently runs to the wrong end is worse than one that takes longer to write.

    Re-encoding is the default because a stream copy can only cut on a keyframe,
    so shot 2 opens with the tail of shot 1 — the exact thing this tool exists to
    avoid. ``fast`` takes the copy anyway, for when speed matters more than the
    first few frames.
    """
    cmd = [exe, "-hide_banner", "-loglevel", "error", "-y",
           "-ss", f"{start:.3f}", "-i", source, "-t", f"{duration:.3f}"]
    if fast:
        cmd += ["-c", "copy", "-avoid_negative_ts", "make_zero"]
    else:
        cmd += ["-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
                "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k"]
    cmd.append(str(dest))
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=_FFMPEG_TIMEOUT)
    except subprocess.TimeoutExpired:
        return False, f"ffmpeg timed out after {_FFMPEG_TIMEOUT}s"
    except Exception as exc:  # noqa: BLE001
        return False, str(exc)
    if proc.returncode != 0 or not dest.is_file() or dest.stat().st_size == 0:
        return False, " ".join((proc.stderr or "").split())[-300:] or \
            f"ffmpeg exited {proc.returncode}"
    return True, ""


@tool
def split_video_into_shots(file_path: str = "", detector: str = "content",
                           threshold: float = 27.0,
                           min_shot_seconds: float = _MIN_SHOT_SECONDS,
                           detect_only: bool = False, output_dir: str = "",
                           fast: bool = False, max_shots: int = 0) -> dict:
    """Detect the cuts in a video and split it into one file per shot.

    Finds shot boundaries automatically and writes each shot as its own video
    file, so a clip can be worked on shot by shot — restyle one shot, feed each to
    a per-shot workflow, or just find out where the cuts are. Run it with
    ``detect_only=True`` first when you are unsure of the settings: that reads the
    file and writes nothing.

    Args:
        file_path: The video to split. A path, or a bare filename sitting in
            ComfyUI's input dir.
        detector: ``content`` (default) compares consecutive frames — right for
            edited footage with hard cuts. ``adaptive`` scores against a rolling
            window instead, which stops fast camera motion, whip pans and strobes
            from reading as cuts; use it on handheld or high-motion material.
        threshold: Sensitivity. LOWER finds more cuts. 27.0 suits ``content``; for
            ``adaptive`` the comparable default is 3.0. If a known cut is missed,
            lower it; if one shot comes back split into several, raise it.
        min_shot_seconds: Ignore any shot shorter than this (default 0.4), so a
            flash frame or a one-frame glitch is not reported as a shot.
        detect_only: Report where the cuts are and write nothing.
        output_dir: Where the shots go. Defaults to a ``<name>_shots`` folder
            under the agent's videos directory.
        fast: Stream-copy instead of re-encoding. Much faster, but a copy can only
            cut on a keyframe, so shots may open with a fraction of a second of
            the previous one. Leave this off when the boundaries matter.
        max_shots: Stop writing after this many (default 200). Detection still
            reports everything it found.

    Returns:
        ``{"status", "content": [{"text"}], "shots": [...], "output_dir", "meta"}``
        — each shot carrying its index, start/end in seconds and timecode, its
        duration, and (unless ``detect_only``) the path written.
    """
    resolved = _resolve_video(file_path)
    if resolved is None:
        return {"status": "error", "content": [{"text": f"Video not found: {file_path}"}]}
    det = str(detector or "content").strip().lower()
    if det not in _DETECTORS:
        return {"status": "error", "content": [{"text": (
            f"Unknown detector {detector!r}. Use one of: {', '.join(_DETECTORS)}."
        )}]}
    try:
        cap = int(max_shots or 0) or _MAX_SHOTS
    except (TypeError, ValueError):
        cap = _MAX_SHOTS

    try:
        shots, meta = _detect_shots(resolved, det, threshold, min_shot_seconds)
    except ImportError:
        return {"status": "error", "content": [{"text": (
            "Shot detection needs PySceneDetect, which is not installed in this "
            "environment. It is declared in requirements.txt — install with: "
            "uv pip install scenedetect"
        )}]}
    except Exception as exc:  # noqa: BLE001
        return {"status": "error", "content": [{"text": (
            f"Could not read {resolved} for shot detection: {exc}"
        )}]}

    rows = [{"index": i, "start_s": a, "end_s": b, "duration_s": round(b - a, 3),
             "start": sa, "end": sb} for i, (a, b, sa, sb) in enumerate(shots, 1)]
    single = meta.get("cuts", 0) == 0
    head = (f"{resolved} — {len(rows)} shot(s), {meta['cuts']} cut(s) found "
            f"({meta['detector']} detector, threshold {meta['threshold']}, "
            f"~{meta['duration_s']}s at {meta['fps']} fps)")
    listing = "\n".join(
        f"  shot {r['index']:03d}  {r['start']} -> {r['end']}  ({r['duration_s']}s)"
        for r in rows[:cap])

    if detect_only:
        note = "\nNo cuts found — this is one continuous shot." if single else ""
        return {"status": "success", "shots": rows, "meta": meta, "output_dir": "",
                "content": [{"text": head + "\n" + listing + note}]}

    if single:
        # Splitting a single-take clip would write one file that is a copy of the
        # input under a new name. Saying so is the useful answer; a duplicate the
        # user then has to tell apart from the original is not.
        return {"status": "success", "shots": rows, "meta": meta, "output_dir": "",
                "content": [{"text": head + "\nNo cuts found, so nothing was split — "
                             "the file already is a single shot; use it as it is."}]}

    exe = _ffmpeg_exe()
    if exe is None:
        # Detection worked. Report what it found rather than throwing it away with
        # the failure — the cut list is most of the value and it cost a full read.
        return {"status": "error", "shots": rows, "meta": meta, "content": [{"text": (
            head + "\n" + listing + "\nCuts were found but there is no ffmpeg binary "
            "to split with (imageio-ffmpeg is missing and nothing is on PATH). The "
            "cut list above still stands."
        )}]}

    src = Path(resolved)
    dest_dir = _shots_dir(src, output_dir)
    ext = src.suffix if (fast and src.suffix) else ".mp4"
    print(f"[split_video] {src.name}: {len(rows)} shot(s) -> {dest_dir}")

    written, failed = [], []
    for r in rows[:cap]:
        out = dest_dir / f"{src.stem}_shot_{r['index']:03d}{ext}"
        ok, err = _cut_one(exe, resolved, out, r["start_s"], r["duration_s"], bool(fast))
        if ok:
            r["path"] = str(out)
            written.append(r)
        else:
            r["error"] = err
            failed.append(r)

    truncated = max(0, len(rows) - cap)
    lines = [head, f"Wrote {len(written)} shot file(s) to {dest_dir}"]
    lines += [f"  shot {r['index']:03d}  {r['start']} -> {r['end']}  "
              f"({r['duration_s']}s)  {r['path']}" for r in written]
    if failed:
        lines.append(f"{len(failed)} shot(s) could not be written:")
        lines += [f"  shot {r['index']:03d}: {r.get('error', '?')}" for r in failed[:5]]
    if truncated:
        lines.append(f"{truncated} further shot(s) were detected but not written "
                     f"(cap {cap}) — raise max_shots, or raise the threshold if the "
                     "detector is firing on motion rather than on cuts.")
    if fast:
        lines.append("Stream-copied: each shot may open with a fraction of a second "
                     "of the previous one. Re-run with fast=false for exact cuts.")
    return {
        "status": "success" if written else "error",
        "shots": rows, "meta": meta, "output_dir": str(dest_dir),
        "content": [{"text": "\n".join(lines)}],
    }
