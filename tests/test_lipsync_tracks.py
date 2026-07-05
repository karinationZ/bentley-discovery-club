"""MouthTrack interpolation is deterministic and clamped; manifest loading fails loudly."""
import json

import pytest

from bentley.lipsync.mouth_sheet import MouthSheet
from bentley.lipsync.mouth_track import MouthTrack

KF = [{"time": 0.0, "x": 100.0, "y": 200.0, "scale": 1.0, "rotation_deg": 0.0, "visible": True},
      {"time": 2.0, "x": 120.0, "y": 210.0, "scale": 1.2, "rotation_deg": -4.0, "visible": True}]


def test_track_interpolates_midpoint():
    t = MouthTrack(KF)
    mid = t.at(1.0)
    assert mid["x"] == pytest.approx(110.0)
    assert mid["y"] == pytest.approx(205.0)
    assert mid["scale"] == pytest.approx(1.1)
    assert mid["rotation_deg"] == pytest.approx(-2.0)


def test_track_clamps_out_of_range():
    t = MouthTrack(KF)
    assert t.at(-5.0)["x"] == 100.0
    assert t.at(99.0)["x"] == 120.0


def test_track_roundtrip(tmp_path):
    t = MouthTrack(KF)
    p = tmp_path / "track.json"
    t.save(p)
    t2 = MouthTrack.load(p)
    assert t2.at(1.0)["x"] == pytest.approx(t.at(1.0)["x"])


def test_empty_track_rejected():
    with pytest.raises(ValueError):
        MouthTrack([])


def test_manifest_missing_png_fails(tmp_path):
    m = {"character": "bentley", "version": "v1", "anchor": {"x": 0.5, "y": 0.45},
         "shapes": {"REST_CLOSED": {"file": "missing.png"}}}
    mp = tmp_path / "manifest.json"
    mp.write_text(json.dumps(m))
    with pytest.raises(FileNotFoundError):
        MouthSheet(mp)


def test_manifest_unknown_shape_fails(tmp_path):
    m = {"character": "bentley", "version": "v1", "anchor": {"x": 0.5, "y": 0.45},
         "shapes": {"HUMAN_GRIN": {"file": "x.png"}}}
    mp = tmp_path / "manifest.json"
    mp.write_text(json.dumps(m))
    with pytest.raises(ValueError):
        MouthSheet(mp)
