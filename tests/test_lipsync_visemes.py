"""Viseme mapping + cue validation. The load-bearing test: no speech cue may close the mouth."""
import pytest

from bentley.lipsync.visemes import CLOSED_SHAPES, RHUBARB_MAP, SHAPES, map_cue, validate_cues


def test_only_x_and_a_map_closed():
    """Review blocker: Rhubarb B fires ~half of voiced time — it must NEVER map to a closed shape."""
    for cue, viseme in RHUBARB_MAP.items():
        if cue in ("X", "A"):
            continue
        assert viseme not in CLOSED_SHAPES, f"speech cue {cue} maps to closed shape {viseme}"


def test_b_is_speech_shape():
    assert RHUBARB_MAP["B"] == "CONS"


def test_d_deterministic_fallback_and_upgrade():
    assert map_cue("D") == "AI"
    assert map_cue("D", available={"AI", "OPEN_JAW"}) == "OPEN_JAW"


def test_unknown_cue_rejected():
    with pytest.raises(ValueError):
        map_cue("Z")


def test_map_respects_available_set():
    with pytest.raises(ValueError):
        map_cue("C", available={"REST_CLOSED"})


def test_all_mapped_visemes_are_known():
    for v in RHUBARB_MAP.values():
        assert v in SHAPES


def test_validate_rejects_overlap_and_bad_duration():
    ok = [{"start": 0.0, "end": 0.2, "viseme": "MBP"},
          {"start": 0.2, "end": 0.5, "viseme": "AI"}]
    assert validate_cues(ok) == ok
    with pytest.raises(ValueError):
        validate_cues([{"start": 0.0, "end": 0.0, "viseme": "AI"}])
    with pytest.raises(ValueError):
        validate_cues([{"start": 0.0, "end": 0.4, "viseme": "AI"},
                       {"start": 0.2, "end": 0.6, "viseme": "O"}])
    with pytest.raises(ValueError):
        validate_cues([{"start": 0.0, "end": 0.2, "viseme": "NOPE"}])
