"""Drift guard (bentley/shared/drift_guard.py) — mechanically enforces last-frame pinning (lever #3).
Verifies: an un-pinned character video render RAISES; a pinned one passes; the override lets it through
with a reason; non-character / non-video calls are ignored."""
import pytest

from bentley.shared.drift_guard import assert_pin_ok

ELEM = [{"name": "Bentley", "element_input_urls": ["u1", "u2"]}]


def test_unpinned_character_shot_raises():
    inp = {"prompt": "p", "image_urls": ["first.png"], "kling_elements": ELEM}
    with pytest.raises(PermissionError, match="NOT last-frame-pinned"):
        assert_pin_ok("kling-3.0/video", inp)


def test_pinned_character_shot_passes():
    inp = {"prompt": "p", "image_urls": ["first.png", "last.png"], "kling_elements": ELEM}
    assert_pin_ok("kling-3.0/video", inp)   # no raise


def test_override_allows_first_frame_only(monkeypatch, capsys):
    monkeypatch.setenv("BENTLEY_PIN_OVERRIDE", "big play-leap; pin would warp")
    inp = {"prompt": "p", "image_urls": ["first.png"], "kling_elements": ELEM}
    assert_pin_ok("kling-3.0/video", inp)   # no raise
    assert "OVERRIDE" in capsys.readouterr().err


def test_environment_shot_not_gated():
    # no kling_elements → not a character shot → ignored even with a single frame
    inp = {"prompt": "waves", "image_urls": ["plate.png"]}
    assert_pin_ok("kling-3.0/video", inp)


def test_non_video_models_ignored():
    inp = {"prompt": "p", "image_urls": ["x"], "kling_elements": ELEM}
    assert_pin_ok("google/nano-banana-edit", inp)   # image model → ignored
    assert_pin_ok("nano-banana-pro", inp)
