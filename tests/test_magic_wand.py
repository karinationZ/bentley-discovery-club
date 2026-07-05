"""Magic Wand (bentley/fix/magic_wand.py) — zero-token white-paw fixer.
Verifies: sock recolored to coat (hue moves, texture kept), everything OUTSIDE the selection
byte-identical-ish (blaze/collar/background untouched), leak + bad-seed protection, video mode."""
import os, shutil, subprocess
import numpy as np
import pytest
from PIL import Image

from bentley.fix.magic_wand import fix_image, preview_image, wand_mask, sample_coat, fix_video

COAT = (150, 92, 52)      # fawn
SOCK = (232, 229, 224)    # white sock
BLAZE = (240, 238, 235)   # canon white chest blaze (must NOT change)
TEAL = (28, 160, 155)


def make_img(path):
    """220x220: coat body, white sock bottom-left (connected blob), separate blaze, teal collar."""
    rng = np.random.default_rng(7)
    arr = np.zeros((220, 220, 3), np.float64)
    arr[..., :] = (90, 130, 80)                        # meadow bg
    arr[40:200, 60:160] = COAT                          # body/leg
    arr[160:200, 70:110] = SOCK                         # sock ON the leg (connected)
    arr[60:90, 95:125] = BLAZE                          # blaze (NOT connected to sock)
    arr[52:58, 80:140] = TEAL                           # collar
    arr += rng.normal(0, 3, arr.shape)                  # fur-ish noise
    arr = np.clip(arr, 0, 255).astype(np.uint8)
    Image.fromarray(arr).save(path)
    return arr


def test_fix_recolors_sock_and_preserves_rest(tmp_path):
    p = str(tmp_path / "dog.png")
    before = make_img(p)
    out, n = fix_image(p, seeds=[(90, 180)], coat_xy=(110, 120))
    after = np.asarray(Image.open(out).convert("RGB")).astype(np.int64)
    before = before.astype(np.int64)
    assert n > 500                                           # a real sock-sized selection
    # sock became coat-like: red channel dominates, hue near coat, not white
    sock = after[165:195, 75:105]
    assert sock[..., 0].mean() > sock[..., 2].mean() + 30    # fawn = R >> B
    assert abs(sock.mean() - np.array(COAT).mean()) < 60     # in the coat brightness family
    # texture preserved (not a flat fill)
    assert sock.std() > 1.0
    # blaze, collar, background untouched (allow feather-edge tolerance)
    for (ys, xs) in [(slice(62, 88), slice(97, 123)),        # blaze core
                     (slice(53, 57), slice(82, 138)),        # collar
                     (slice(0, 30), slice(0, 30))]:          # bg corner
        assert np.abs(after[ys, xs] - before[ys, xs]).mean() < 2.0


def test_leak_protection(tmp_path):
    p = str(tmp_path / "white.png")
    arr = np.full((200, 200, 3), 245, np.uint8)              # all-white image
    Image.fromarray(arr).save(p)
    with pytest.raises(ValueError, match="exceeded"):
        wand_mask(np.asarray(Image.open(p).convert("RGB")), [(100, 100)])


def test_bad_seed_rejected(tmp_path):
    p = str(tmp_path / "dog.png")
    make_img(p)
    with pytest.raises(ValueError, match="not a whitish"):   # seed on the coat, not the sock
        fix_image(p, seeds=[(110, 120)], coat_xy=(110, 120))


def test_preview_writes_overlay(tmp_path):
    p = str(tmp_path / "dog.png")
    make_img(p)
    out, n = preview_image(p, seeds=[(90, 180)])
    assert os.path.exists(out) and n > 500


def test_coat_sample(tmp_path):
    p = str(tmp_path / "dog.png")
    make_img(p)
    c = sample_coat(np.asarray(Image.open(p).convert("RGB")), (110, 120))
    assert np.abs(c - np.array(COAT)).max() < 12


@pytest.mark.skipif(shutil.which("ffmpeg") is None, reason="ffmpeg required")
def test_fix_video_roi(tmp_path):
    # 6-frame clip: coat block with a white sock inside the ROI; sock must turn fawn, bg stay
    fd = tmp_path / "frames"; fd.mkdir()
    for i in range(6):
        arr = np.zeros((64, 64, 3), np.uint8); arr[...] = (90, 130, 80)
        arr[10:54, 16:48] = COAT
        arr[40 + (i % 2):52, 20:32] = SOCK                   # sock wiggles a bit per frame
        Image.fromarray(arr).save(fd / f"f{i:05d}.png")
    vid = str(tmp_path / "in.mp4")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "12", "-i", str(fd / "f%05d.png"),
                    "-c:v", "libx264", "-crf", "12", "-pix_fmt", "yuv420p", vid], check=True)
    out = fix_video(vid, rois=[(18, 38, 18, 16)], coat_xy=(30, 20))
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", out, str(tmp_path / "o%05d.png")], check=True)
    o = np.asarray(Image.open(tmp_path / "o00003.png").convert("RGB")).astype(np.int64)
    sock_after = o[43:51, 21:31]
    assert sock_after[..., 0].mean() > sock_after[..., 2].mean() + 25   # fawn now
    assert np.abs(o[2:8, 2:8].astype(float) - np.array((90, 130, 80))).mean() < 12  # bg (codec tol)
