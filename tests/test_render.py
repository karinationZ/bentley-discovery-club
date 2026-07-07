"""Sanctioned render builder (bentley/shared/render.py) — bakes in the Bentley element + last-frame pin.
Verifies build_render assembles a pinned payload with the element, and that it round-trips through the
drift guard cleanly (pinned) or raises (unpinned) — proving the sanctioned path satisfies the guard."""
import pytest

from bentley.shared.drift_guard import assert_pin_ok
from bentley.shared.render import build_render


def test_build_render_pins_and_attaches_element():
    model, payload = build_render("leap", "http://f/first.png", last_url="http://f/last.png",
                                  master_url="http://f/m.png", turnaround_url="http://f/t.png")
    assert model == "kling-3.0/video"
    assert payload["image_urls"] == ["http://f/first.png", "http://f/last.png"]
    assert payload["multi_shots"] is False
    el = payload["kling_elements"][0]
    assert el["name"] == "Bentley" and el["element_input_urls"] == ["http://f/m.png", "http://f/t.png"]


def test_sanctioned_pinned_payload_passes_guard():
    _, payload = build_render("hold", "http://f/first.png", last_url="http://f/last.png",
                              master_url="http://f/m.png", turnaround_url="http://f/t.png")
    assert_pin_ok("kling-3.0/video", payload)   # the sanctioned path satisfies the mechanical guard


def test_unpinned_build_would_fail_guard():
    _, payload = build_render("run", "http://f/first.png", last_url=None,
                              master_url="http://f/m.png", turnaround_url="http://f/t.png")
    with pytest.raises(PermissionError):
        assert_pin_ok("kling-3.0/video", payload)
