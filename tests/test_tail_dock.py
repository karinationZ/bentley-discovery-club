"""Tail Dock (bentley/fix/tail_dock.py) — over-long-tail removal against clean background.
Verifies: the excess tail region fills with the surrounding sky, everything outside the box stays,
--keep protects the stub, empty selections are rejected."""
import numpy as np
import pytest
from PIL import Image

from bentley.fix.tail_dock import fix_image, preview_image

SKY = (140, 180, 220)
COAT = (150, 92, 52)


def make_img(path):
    rng = np.random.default_rng(5)
    arr = np.zeros((220, 220, 3), np.float64)
    arr[..., :] = SKY
    arr[60:200, 10:80] = COAT                     # body at the left
    arr[100:122, 80:200] = COAT                   # the WRONG long tail across the sky
    arr += rng.normal(0, 2.5, arr.shape)
    arr = np.clip(arr, 0, 255).astype(np.uint8)
    Image.fromarray(arr).save(path)
    return arr


def test_dock_fills_tail_with_sky_and_preserves_rest(tmp_path):
    p = str(tmp_path / "long.png")
    before = make_img(p).astype(np.int64)
    out, n = fix_image(p, box=(92, 88, 120, 48), tail_xy=(150, 110))
    after = np.asarray(Image.open(out).convert("RGB")).astype(np.int64)
    assert n > 1200                                          # a real tail-sized selection
    filled = after[104:118, 110:190]
    assert np.abs(filled.mean(axis=(0, 1)) - np.array(SKY)).max() < 25   # sky-family fill
    assert filled[..., 2].mean() > filled[..., 0].mean() + 30            # blue again, not coat
    # body and far background untouched
    for (ys, xs) in [(slice(120, 190), slice(15, 75)),       # body core
                     (slice(0, 40), slice(0, 40))]:          # sky corner
        assert np.abs(after[ys, xs] - before[ys, xs]).mean() < 2.0


def test_keep_box_protects_the_stub(tmp_path):
    p = str(tmp_path / "stub.png")
    before = make_img(p).astype(np.int64)
    out, n = fix_image(p, box=(80, 88, 132, 48), tail_xy=(160, 110),
                       keeps=[(80, 88, 24, 48)])             # the stub next to the body stays
    after = np.asarray(Image.open(out).convert("RGB")).astype(np.int64)
    stub = after[104:118, 84:100]
    assert stub[..., 0].mean() > stub[..., 2].mean() + 30    # still coat-colored
    assert np.abs(after[104:118, 130:190].mean(axis=(0, 1)) - np.array(SKY)).max() < 25


def test_bad_sample_rejected(tmp_path):
    p = str(tmp_path / "long.png")
    make_img(p)
    with pytest.raises(ValueError, match="almost no pixels"):
        fix_image(p, box=(120, 10, 60, 50), tail_xy=(150, 110))  # sky-only box, tail sample


def test_preview_overlay(tmp_path):
    p = str(tmp_path / "long.png")
    make_img(p)
    out, n = preview_image(p, box=(92, 88, 120, 48), tail_xy=(150, 110))
    assert out.endswith("_dockmask.png") and n > 1200
