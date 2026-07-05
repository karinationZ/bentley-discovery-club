"""Registry + plate calibration layers: configs load, fail loudly, and honor the hard rules."""
import json

import pytest

from bentley.lipsync import characters
from bentley.lipsync.plates import Plate
from bentley.lipsync.visemes import CLOSED_SHAPES


def test_bentley_is_onboarded():
    c = characters.load("bentley")
    assert c.name == "bentley"
    assert "three_quarter" in c.sheets and "side" in c.sheets
    assert c.sheet().available >= {"REST_CLOSED", "MBP", "CONS", "AI", "E", "O", "U", "FV", "L"}


def test_character_map_overrides_cannot_close_speech_cues():
    c = characters.load("bentley")
    for cue, vis in c.rhubarb_map.items():
        if cue in ("X", "A"):
            continue
        assert vis not in CLOSED_SHAPES, f"{cue} maps closed via character override"


def test_unknown_character_lists_onboarded():
    with pytest.raises(FileNotFoundError) as e:
        characters.load("nonexistent_character")
    assert "bentley" in str(e.value)


def test_plate_loads_and_visibility_windows():
    p = Plate("episodes/ep3/lipsync/plates/ep3_strong_ts.json")
    assert p.character == "bentley" and p.angle == "three_quarter"
    assert p._visible(1.0) and not p._visible(3.5)


def test_plate_missing_video_fails(tmp_path):
    cfg = json.loads(open("episodes/ep3/lipsync/plates/ep3_strong_ts.json").read())
    cfg["video"] = "does/not/exist.mp4"
    f = tmp_path / "bad.json"
    f.write_text(json.dumps(cfg))
    with pytest.raises(FileNotFoundError):
        Plate(f)
