"""Shot Match (bentley/fix/shot_match.py) — clip-to-reference color/luma conform.
Verifies: a dimmed clip conformed to its bright reference closes most of the L gap (the
Avatar-darkening case), luma-only leaves chroma alone, and the LAB core round-trips."""
import shutil
import subprocess

import numpy as np
import pytest
from PIL import Image

from bentley.fix.color_transfer import lab_to_srgb, srgb_to_lab
from bentley.fix.shot_match import _stats_of, fix

pytestmark = pytest.mark.skipif(shutil.which("ffmpeg") is None, reason="ffmpeg required")

FPS = 12


def make_clip(tmp_path, name, gain=1.0, blue_cast=0):
    fd = tmp_path / f"{name}_frames"
    fd.mkdir()
    rng = np.random.default_rng(9)
    for i in range(18):
        arr = np.zeros((64, 64, 3), np.float64)
        arr[..., :] = (90, 130, 80)
        arr[20:44, 4 + (i * 3) % 40:24 + (i * 3) % 40] = (150, 92, 52)
        arr += rng.normal(0, 2, arr.shape)
        arr = arr * gain
        arr[..., 2] += blue_cast
        Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8)).save(fd / f"f{i:05d}.png")
    out = str(tmp_path / f"{name}.mp4")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS),
                    "-i", str(fd / "f%05d.png"), "-c:v", "libx264", "-crf", "12",
                    "-pix_fmt", "yuv420p", out], check=True)
    return out


def test_lab_round_trip():
    rng = np.random.default_rng(1)
    rgb = rng.uniform(0, 255, (32, 32, 3))
    back = lab_to_srgb(srgb_to_lab(rgb))
    assert np.abs(back - rgb).max() < 1.0


def test_dark_clip_lifted_to_reference(tmp_path):
    ref = make_clip(tmp_path, "ref", gain=1.0)
    dark = make_clip(tmp_path, "dark", gain=0.62)            # the Avatar-darkening magnitude
    (dm, _), (rm, _) = _stats_of(dark), _stats_of(ref)
    gap_before = abs(rm[0] - dm[0])
    assert gap_before > 8                                    # the defect is real
    out = fix(dark, ref)
    (fm, _) = _stats_of(out)[0], None
    gap_after = abs(rm[0] - _stats_of(out)[0][0])
    assert gap_after < gap_before * 0.4                      # most of the gap closed
    assert out.endswith("_match.mp4")


def test_luma_only_leaves_chroma(tmp_path):
    ref = make_clip(tmp_path, "ref2", gain=1.0)
    cast = make_clip(tmp_path, "cast", gain=0.7, blue_cast=25)
    out = fix(cast, ref, luma_only=True)
    (cm, _), (om, _), (rm, _) = _stats_of(cast), _stats_of(out), _stats_of(ref)
    assert abs(om[0] - rm[0]) < abs(cm[0] - rm[0]) * 0.6     # L moved toward ref
    assert abs(om[2] - cm[2]) < 3.0                          # b* (the blue cast) untouched
