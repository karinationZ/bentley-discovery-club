"""Recolor (bentley/fix/recolor.py) — generalized canon-color drift fixer.
Verifies: a drifted teal collar recolors to canon gold (texture kept), nothing outside the box
changes, target can be sampled from a reference master, empty selections are rejected."""
import numpy as np
import pytest
from PIL import Image

from bentley.fix.recolor import fix_image, preview_image

COAT = (150, 92, 52)
TEAL = (28, 160, 155)      # the drifted collar we fix
GOLD = (212, 175, 55)      # canon Listening-Tag gold
BG = (90, 130, 80)


def make_img(path):
    rng = np.random.default_rng(3)
    arr = np.zeros((200, 200, 3), np.float64)
    arr[..., :] = BG
    arr[40:180, 50:150] = COAT                    # body
    arr[60:78, 60:140] = TEAL                     # drifted collar band
    arr += rng.normal(0, 3, arr.shape)
    arr = np.clip(arr, 0, 255).astype(np.uint8)
    Image.fromarray(arr).save(path)
    return arr


def test_recolor_to_rgb_and_preserve_rest(tmp_path):
    p = str(tmp_path / "dog.png")
    before = make_img(p).astype(np.int64)
    out, n = fix_image(p, boxes=[(55, 55, 92, 28)], from_xy=(100, 69), to_rgb=GOLD)
    after = np.asarray(Image.open(out).convert("RGB")).astype(np.int64)
    assert n > 400
    band = after[63:75, 65:135]
    assert band[..., 0].mean() > band[..., 2].mean() + 40     # gold = warm, R >> B
    assert band.std() > 1.0                                   # texture kept, not a flat fill
    # outside the box: byte-identical-ish
    for (ys, xs) in [(slice(120, 170), slice(60, 140)),       # body below
                     (slice(0, 30), slice(0, 30))]:           # background corner
        assert np.abs(after[ys, xs] - before[ys, xs]).mean() < 2.0


def test_target_from_reference_master(tmp_path):
    p = str(tmp_path / "dog.png")
    make_img(p)
    ref = str(tmp_path / "master.png")
    m = np.zeros((40, 40, 3), np.uint8)
    m[...] = GOLD
    Image.fromarray(m).save(ref)
    out, n = fix_image(p, boxes=[(55, 55, 92, 28)], from_xy=(100, 69),
                       to_ref=ref, to_xy=(20, 20))
    after = np.asarray(Image.open(out).convert("RGB")).astype(np.int64)
    band = after[63:75, 65:135]
    assert band[..., 0].mean() > band[..., 2].mean() + 40 and n > 400


def test_empty_selection_rejected(tmp_path):
    p = str(tmp_path / "dog.png")
    make_img(p)
    with pytest.raises(ValueError, match="almost no pixels"):
        # sample the collar but box only background — nothing near the sample inside the box
        fix_image(p, boxes=[(0, 0, 30, 30)], from_xy=(100, 69), to_rgb=GOLD)


def test_missing_target_rejected(tmp_path):
    p = str(tmp_path / "dog.png")
    make_img(p)
    with pytest.raises(ValueError, match="to-rgb|to-ref"):
        fix_image(p, boxes=[(55, 55, 92, 28)], from_xy=(100, 69))


def test_preview_overlay(tmp_path):
    p = str(tmp_path / "dog.png")
    make_img(p)
    out, n = preview_image(p, boxes=[(55, 55, 92, 28)], from_xy=(100, 69))
    assert out.endswith("_recolormask.png") and n > 400
