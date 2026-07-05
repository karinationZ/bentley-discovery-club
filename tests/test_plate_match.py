"""Plate Match (bentley/fix/plate_match.py) — keyframe-background conform to the scene plate.
Verifies: the drifted background moves toward the plate's stats, the protected character region
stays byte-identical-ish, and scan reports the delta."""
import numpy as np
from PIL import Image

from bentley.fix.plate_match import fix, scan

DRIFT_BG = (80, 110, 165)      # keyframe background drifted cold/blue
PLATE_BG = (95, 150, 90)       # the locked scene-anchor meadow
COAT = (150, 92, 52)
PROTECT = (70, 70, 60, 60)


def make_pair(tmp_path):
    rng = np.random.default_rng(2)
    kf = np.zeros((200, 200, 3), np.float64)
    kf[..., :] = DRIFT_BG
    x, y, w, h = PROTECT
    kf[y:y + h, x:x + w] = COAT                               # the character (protected)
    kf += rng.normal(0, 3, kf.shape)
    kf_p = str(tmp_path / "keyframe.png")
    Image.fromarray(np.clip(kf, 0, 255).astype(np.uint8)).save(kf_p)

    plate = np.zeros((200, 200, 3), np.float64)
    plate[..., :] = PLATE_BG
    plate += rng.normal(0, 3, plate.shape)
    plate_p = str(tmp_path / "plate.png")
    Image.fromarray(np.clip(plate, 0, 255).astype(np.uint8)).save(plate_p)
    return kf_p, plate_p


def test_background_conforms_character_protected(tmp_path):
    kf_p, plate_p = make_pair(tmp_path)
    before = np.asarray(Image.open(kf_p).convert("RGB")).astype(np.int64)
    out = fix(kf_p, plate_p, protects=[PROTECT])
    after = np.asarray(Image.open(out).convert("RGB")).astype(np.int64)

    bg_before = before[10:50, 10:50].mean(axis=(0, 1))
    bg_after = after[10:50, 10:50].mean(axis=(0, 1))
    target = np.array(PLATE_BG)
    assert np.abs(bg_after - target).sum() < np.abs(bg_before - target).sum() * 0.55
    assert bg_after[1] > bg_after[2]                          # green again, not blue

    x, y, w, h = PROTECT                                      # character core untouched
    core = (slice(y + 15, y + h - 15), slice(x + 15, x + w - 15))
    assert np.abs(after[core] - before[core]).mean() < 1.5


def test_scan_reports_delta(tmp_path, capsys):
    kf_p, plate_p = make_pair(tmp_path)
    d = scan(kf_p, plate_p, protects=[PROTECT])
    outtxt = capsys.readouterr().out
    assert "delta" in outtxt and abs(d[2]) > 5                # the blue cast shows in b*
