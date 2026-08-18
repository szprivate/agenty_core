"""Tests for shot detection and splitting (``agenty_core.tools.video``).

Built around a real three-shot clip written to a temp dir, because the two things
worth pinning cannot be faked: that the detector finds the cuts where they
actually are, and that each written shot OPENS on its own content. The second is
the whole reason the default re-encodes instead of stream-copying — a copy can
only cut on a keyframe, so shot 2 arrives carrying the tail of shot 1 and every
downstream frame reference is a frame or twelve out.

Runs under pytest or directly (``python test_video_shots.py``).
"""

import os
import tempfile

import numpy as np

from agenty_core.tools import video as V

# Divisible by 16: the h264 writer silently resizes anything else and prints a
# warning per clip, which buries the test output it is mixed into.
FPS, W, H = 12, 160, 128
SHOT_FRAMES = FPS          # one second per shot
# Which colour channel each shot is dominated by, so a written file can be
# checked to open on the right one.
DOMINANT = {1: 0, 2: 1, 3: 2}


def _three_shot_clip(path: str) -> str:
    """A 3s clip: one second each of red, green and blue, hard cuts between.

    Every shot MOVES (a travelling bar, a rolling gradient, noise). A static clip
    would let a detector look right by finding nothing at all.
    """
    import imageio.v2 as iio

    rng = np.random.default_rng(7)
    frames = []
    for i in range(SHOT_FRAMES):
        f = np.zeros((H, W, 3), np.uint8)
        f[:, :, 0] = 200
        f[:, (i * 6) % W:(i * 6) % W + 14] = 255
        frames.append(f)
    for i in range(SHOT_FRAMES):
        f = np.zeros((H, W, 3), np.uint8)
        f[:, :, 1] = np.tile(np.linspace(0, 255, W, dtype=np.uint8), (H, 1))
        f[(i * 5) % H:(i * 5) % H + 10, :, 2] = 180
        frames.append(f)
    for _ in range(SHOT_FRAMES):
        f = rng.integers(0, 90, (H, W, 3), dtype=np.uint8)
        f[:, :, 2] = 220
        frames.append(f)
    iio.mimwrite(path, frames, fps=FPS, codec="libx264", quality=8)
    return path


def _single_shot_clip(path: str) -> str:
    """One continuous take — moving, but never cutting."""
    import imageio.v2 as iio

    frames = []
    for i in range(SHOT_FRAMES * 2):
        f = np.zeros((H, W, 3), np.uint8)
        f[:, :, 0] = 200
        f[:, (i * 4) % W:(i * 4) % W + 12] = 255
        frames.append(f)
    iio.mimwrite(path, frames, fps=FPS, codec="libx264", quality=8)
    return path


def _dominant_channel(path: str) -> int:
    import imageio.v2 as iio

    rd = iio.get_reader(path)
    try:
        first = rd.get_data(0)
    finally:
        rd.close()
    return int(np.argmax(first.reshape(-1, 3).mean(0)))


def _frame_count(path: str) -> int:
    import imageio.v2 as iio

    rd = iio.get_reader(path)
    try:
        return rd.count_frames()
    finally:
        rd.close()


def test_detect_only_finds_the_cuts_and_writes_nothing():
    with tempfile.TemporaryDirectory() as d:
        clip = _three_shot_clip(os.path.join(d, "clip.mp4"))
        out = os.path.join(d, "shots")
        r = V.split_video_into_shots(file_path=clip, detect_only=True, output_dir=out)
        assert r["status"] == "success"
        assert len(r["shots"]) == 3 and r["meta"]["cuts"] == 2
        # The cuts are one second apart, and the boundary must land on the cut
        # rather than near it — a "shot" that starts half a second late is not one.
        starts = [s["start_s"] for s in r["shots"]]
        assert abs(starts[1] - 1.0) < 0.09, starts
        assert abs(starts[2] - 2.0) < 0.09, starts
        assert not os.path.exists(out), "detect_only must not create anything"
        assert all("path" not in s for s in r["shots"])


def test_each_written_shot_opens_on_its_own_content():
    with tempfile.TemporaryDirectory() as d:
        clip = _three_shot_clip(os.path.join(d, "clip.mp4"))
        r = V.split_video_into_shots(file_path=clip, output_dir=os.path.join(d, "shots"))
        assert r["status"] == "success", r["content"][0]["text"]
        assert len(r["shots"]) == 3
        for s in r["shots"]:
            p = s["path"]
            assert os.path.isfile(p) and os.path.getsize(p) > 0
            assert os.path.basename(p) == f"clip_shot_{s['index']:03d}.mp4"
            # The point of re-encoding: no frames of the previous shot come along.
            assert _dominant_channel(p) == DOMINANT[s["index"]], f"shot {s['index']}"
            assert abs(_frame_count(p) - SHOT_FRAMES) <= 1, f"shot {s['index']}"


def test_a_single_take_is_reported_not_duplicated():
    # Writing one file that is a copy of the input under a new name is not a
    # split; it is a second file the user then has to tell apart from the first.
    with tempfile.TemporaryDirectory() as d:
        clip = _single_shot_clip(os.path.join(d, "solo.mp4"))
        out = os.path.join(d, "shots")
        r = V.split_video_into_shots(file_path=clip, output_dir=out)
        assert r["status"] == "success"
        assert r["meta"]["cuts"] == 0 and len(r["shots"]) == 1
        assert "no cuts found" in r["content"][0]["text"].lower()
        assert not os.path.exists(out)


def test_the_cap_limits_writing_but_not_reporting():
    with tempfile.TemporaryDirectory() as d:
        clip = _three_shot_clip(os.path.join(d, "clip.mp4"))
        r = V.split_video_into_shots(file_path=clip, max_shots=2,
                                     output_dir=os.path.join(d, "shots"))
        assert len(r["shots"]) == 3, "detection still reports everything it found"
        assert len([s for s in r["shots"] if "path" in s]) == 2
        assert "not written" in r["content"][0]["text"]


def test_no_ffmpeg_still_hands_back_the_cut_list():
    # Detection cost a full read of the file. Throwing that away because the
    # machine cannot WRITE is losing most of the value over half a failure.
    with tempfile.TemporaryDirectory() as d:
        clip = _three_shot_clip(os.path.join(d, "clip.mp4"))
        real = V._ffmpeg_exe
        V._ffmpeg_exe = lambda: None
        try:
            r = V.split_video_into_shots(file_path=clip, output_dir=os.path.join(d, "s"))
        finally:
            V._ffmpeg_exe = real
        assert r["status"] == "error"
        assert len(r["shots"]) == 3
        assert "ffmpeg" in r["content"][0]["text"].lower()
        assert "00:00:01" in r["content"][0]["text"], "the cut list is still there"


def test_a_missing_file_and_an_unknown_detector_are_refused():
    r = V.split_video_into_shots(file_path="no_such_clip_xyz.mp4")
    assert r["status"] == "error" and "not found" in r["content"][0]["text"]
    with tempfile.TemporaryDirectory() as d:
        clip = _three_shot_clip(os.path.join(d, "clip.mp4"))
        r = V.split_video_into_shots(file_path=clip, detector="magic")
        assert r["status"] == "error"
        assert "content" in r["content"][0]["text"] and "adaptive" in r["content"][0]["text"]


def test_timecodes_read_as_timecodes():
    assert V._timecode(0) == "00:00:00.000"
    assert V._timecode(12.4) == "00:00:12.400"
    assert V._timecode(3671.5) == "01:01:11.500"


if __name__ == "__main__":
    fns = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    for fn in fns:
        fn()
        print(f"ok  {fn.__name__}")
    print(f"\n{len(fns)} shot-splitting tests passed")
