"""Kling payload builder (bentley/shared/kling.py) — first+last frame pinning (drift lever #3)."""
import pytest

from bentley.shared.kling import bentley_element, i2v_payload


def test_first_frame_only():
    p = i2v_payload("run", "http://f/first.png")
    assert p["image_urls"] == ["http://f/first.png"]
    assert p["multi_shots"] is False and p["sound"] is False
    assert "kling_elements" not in p


def test_first_and_last_frame_pinned():
    p = i2v_payload("hold", "http://f/first.png", last_url="http://f/last.png")
    assert p["image_urls"] == ["http://f/first.png", "http://f/last.png"]  # index0=first, index1=last
    assert p["multi_shots"] is False


def test_elements_attached():
    el = bentley_element("http://f/master.png", "http://f/turn.png")
    p = i2v_payload("x", "http://f/first.png", elements=[el])
    assert p["kling_elements"][0]["name"] == "Bentley"
    assert p["kling_elements"][0]["element_input_urls"] == ["http://f/master.png", "http://f/turn.png"]
    assert "no white socks" in p["kling_elements"][0]["description"]


def test_missing_first_frame_rejected():
    with pytest.raises(ValueError, match="first_url"):
        i2v_payload("x", "")


def test_duration_stringified():
    p = i2v_payload("x", "http://f/first.png", duration=5)
    assert p["duration"] == "5"
