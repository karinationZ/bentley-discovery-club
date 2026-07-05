"""Prop Paste (bentley/fix/prop_paste.py) — locked-prop composite.
Verifies: an RGBA cutout lands where aimed with the rest untouched, alpha is respected,
--key cuts a flat background, RGB-without-key is rejected, preview writes the overlay."""
import numpy as np
import pytest
from PIL import Image

from bentley.fix.prop_paste import fix_image, load_prop, preview_image

GOLD = (212, 175, 55)


def make_dest(tmp_path):
    arr = np.full((120, 120, 3), 100, np.uint8)
    p = str(tmp_path / "dest.png")
    Image.fromarray(arr).save(p)
    return p


def make_prop_rgba(tmp_path):
    """20x20 gold disc on transparent."""
    arr = np.zeros((20, 20, 4), np.uint8)
    yy, xx = np.mgrid[:20, :20]
    disc = (yy - 10) ** 2 + (xx - 10) ** 2 <= 64
    arr[disc, :3] = GOLD
    arr[disc, 3] = 255
    p = str(tmp_path / "tag.png")
    Image.fromarray(arr).save(p)
    return p


def test_paste_lands_and_rest_untouched(tmp_path):
    dest, prop = make_dest(tmp_path), make_prop_rgba(tmp_path)
    out = fix_image(dest, prop, at=(60, 60), feather=0.0)
    after = np.asarray(Image.open(out).convert("RGB")).astype(np.int64)
    assert np.abs(after[60, 60] - np.array(GOLD)).max() < 12          # disc center = gold
    assert (after[:20, :20] == 100).all()                             # far corner untouched
    assert (after[60, 40] == 100).all()                               # transparent ring = dest


def test_key_mode_cuts_flat_background(tmp_path):
    dest = make_dest(tmp_path)
    flat = np.full((20, 20, 3), 250, np.uint8)                        # white master background
    yy, xx = np.mgrid[:20, :20]
    disc = (yy - 10) ** 2 + (xx - 10) ** 2 <= 64
    flat[disc] = GOLD
    prop = str(tmp_path / "flat.png")
    Image.fromarray(flat).save(prop)
    out = fix_image(dest, prop, at=(60, 60), key=True, feather=0.0)
    after = np.asarray(Image.open(out).convert("RGB")).astype(np.int64)
    assert np.abs(after[60, 60] - np.array(GOLD)).max() < 12
    assert np.abs(after[52, 52] - 100).max() < 12                     # keyed corner = dest gray


def test_rgb_without_key_rejected(tmp_path):
    flat = np.full((20, 20, 3), 250, np.uint8)
    prop = str(tmp_path / "nokey.png")
    Image.fromarray(flat).save(prop)
    with pytest.raises(ValueError, match="alpha"):
        load_prop(prop)


def test_preview_writes_overlay(tmp_path):
    dest, prop = make_dest(tmp_path), make_prop_rgba(tmp_path)
    out = preview_image(dest, prop, at=(60, 60))
    assert out.endswith("_pastepreview.png")
    after = np.asarray(Image.open(out).convert("RGB"))
    assert (after != 100).any()                                       # something drawn
