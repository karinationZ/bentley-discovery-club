"""Tail Trim (bentley/fix/tail_trim.py) — frozen-Kling-tail detector/cutter.
Verifies: a synthetic clip with a 1s frozen tail is measured and trimmed to its moving part;
a fully-moving clip is left alone; a fully-static clip is refused (that's a §5 defect, not a tail)."""
import shutil
import subprocess

import numpy as np
import pytest
from PIL import Image

from bentley.fix.tail_trim import main, scan_clip, trim_clip

pytestmark = pytest.mark.skipif(shutil.which("ffmpeg") is None, reason="ffmpeg required")

FPS = 12


def make_clip(tmp_path, name, moving_frames, frozen_frames):
    """White square marching over a dark bg for `moving_frames`, then held for `frozen_frames`."""
    fd = tmp_path / f"{name}_frames"
    fd.mkdir()
    total = moving_frames + frozen_frames
    for i in range(total):
        step = min(i, moving_frames - 1)
        arr = np.full((64, 64, 3), 30, np.uint8)
        x = 4 + step * 3
        arr[20:36, x:x + 12] = 220
        Image.fromarray(arr).save(fd / f"f{i:05d}.png")
    out = str(tmp_path / f"{name}.mp4")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS),
                    "-i", str(fd / "f%05d.png"), "-c:v", "libx264", "-crf", "12",
                    "-pix_fmt", "yuv420p", out], check=True)
    return out


def clip_dur(path):
    return float(subprocess.check_output(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "csv=p=0", path]).strip())


def test_scan_finds_frozen_tail(tmp_path):
    clip = make_clip(tmp_path, "frozen", moving_frames=12, frozen_frames=12)  # 1s motion + 1s hold
    tail, keep, n, fps = scan_clip(clip)
    assert n == 24 and abs(fps - FPS) < 0.01
    assert 0.8 <= tail <= 1.1          # ~1s frozen tail found
    assert 0.9 <= keep <= 1.2          # keeps ~the moving second


def test_trim_cuts_the_tail(tmp_path):
    clip = make_clip(tmp_path, "cutme", moving_frames=12, frozen_frames=12)
    out, tail = trim_clip(clip)
    assert out and out.endswith("_trim.mp4")
    assert clip_dur(out) < clip_dur(clip) - 0.6          # ~1s gone
    # the trimmed clip has no frozen tail of its own
    tail2, keep2, _, _ = scan_clip(out)
    assert tail2 < 0.25


def test_moving_clip_untouched(tmp_path):
    clip = make_clip(tmp_path, "alive", moving_frames=18, frozen_frames=0)
    out, tail = trim_clip(clip)
    assert out is None and tail < 0.12


def test_static_clip_refused(tmp_path):
    clip = make_clip(tmp_path, "static", moving_frames=1, frozen_frames=17)
    out, tail = trim_clip(clip)
    assert out is None and tail > 1.0   # reported as static/frozen, nothing written


def test_scan_exit_code_gates(tmp_path):
    bad = make_clip(tmp_path, "bad", moving_frames=12, frozen_frames=12)
    good = make_clip(tmp_path, "good", moving_frames=18, frozen_frames=0)
    assert main(["scan", bad]) == 1
    assert main(["scan", good]) == 0
