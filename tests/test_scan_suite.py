"""Scan suite (bentley/qa/scan_suite.py) — Part 8.1 scans in one command.
Verifies on synthetic clips: freeze run flagged, interior black flagged, trailing black allowed
(the closing fade), leading black flagged (no opening fade — owner rule), clean clip passes."""
import shutil
import subprocess

import numpy as np
import pytest
from PIL import Image

from bentley.qa.scan_suite import main, scan

pytestmark = pytest.mark.skipif(shutil.which("ffmpeg") is None, reason="ffmpeg required")

FPS = 12


def build(tmp_path, name, segments):
    """segments: list of (kind, n_frames) with kind in {motion, freeze, black}."""
    fd = tmp_path / f"{name}_frames"
    fd.mkdir()
    i, step = 0, 0
    held = None
    for kind, n in segments:
        for _ in range(n):
            if kind == "black":
                arr = np.zeros((64, 64, 3), np.uint8)
            elif kind == "freeze":
                arr = held.copy()
            else:
                step += 1
                arr = np.full((64, 64, 3), 30, np.uint8)
                arr[20:36, 4 + (step * 3) % 40:16 + (step * 3) % 40] = 220
                held = arr
            Image.fromarray(arr).save(fd / f"f{i:05d}.png")
            i += 1
    out = str(tmp_path / f"{name}.mp4")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS),
                    "-i", str(fd / "f%05d.png"), "-c:v", "libx264", "-crf", "12",
                    "-pix_fmt", "yuv420p", out], check=True)
    return out


def run(path):
    return scan(path, sharp_floor=0, min_height=0, require_audio=False)


def test_freeze_and_interior_black_fail_trailing_black_ok(tmp_path):
    clip = build(tmp_path, "bad", [("motion", 12), ("freeze", 8), ("motion", 12),
                                   ("black", 8), ("motion", 12), ("black", 8)])
    fails, warns, infos = run(clip)
    assert any("FREEZE" in f for f in fails)
    assert any("INTERIOR black" in f for f in fails)
    assert not any("LEADING" in f for f in fails)
    assert any("closing fade" in i for i in infos)          # trailing black tolerated


def test_leading_black_fails(tmp_path):
    clip = build(tmp_path, "lead", [("black", 8), ("motion", 24)])
    fails, _, _ = run(clip)
    assert any("LEADING black" in f for f in fails)


def test_clean_clip_passes(tmp_path):
    clip = build(tmp_path, "clean", [("motion", 36)])
    fails, warns, infos = run(clip)
    assert not fails


def test_main_exit_codes_and_stream_checks(tmp_path):
    clip = build(tmp_path, "cli", [("motion", 24)])
    ok = main([clip, "--sharp-floor", "0", "--min-height", "0", "--no-require-audio"])
    assert ok == 0
    # default gates: 64px tall + no audio must FAIL the stream checks
    assert main([clip, "--sharp-floor", "0"]) == 1


def test_sharpness_pass_runs(tmp_path):
    clip = build(tmp_path, "sharp", [("motion", 36)])
    fails, warns, infos = scan(clip, sharp_floor=0.001, min_height=0, require_audio=False)
    assert any("sharpness: median edge-var" in i for i in infos)
