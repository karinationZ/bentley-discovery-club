"""Spend-guard regression tests — the Animatic Lock gate must actually block (bentley/shared/gates.py)."""
import pytest

from bentley.shared import gates

PASSED = """# EP9 GATE LEDGER
| 3 | **✋ ANIMATIC LOCK** (story + cut) | ✅ PASSED | 2026-07-04 | owner watched REV6 end to end |
"""
PENDING = """# EP9 GATE LEDGER
| 3 | **✋ ANIMATIC LOCK** (story + cut) | ⬜ PENDING | — | |
"""


def ledger(tmp_path, text):
    d = tmp_path / "episodes" / "ep9"
    d.mkdir(parents=True)
    (d / "GATES.md").write_text(text)
    return tmp_path


def test_image_models_are_not_gated(monkeypatch):
    monkeypatch.delenv("BENTLEY_EPISODE", raising=False)
    monkeypatch.delenv("BENTLEY_GATE_OVERRIDE", raising=False)
    gates.assert_spend_allowed("google/nano-banana")       # masters/keyframes: pre-animatic tier
    gates.assert_spend_allowed("google/nano-banana-edit")


@pytest.mark.parametrize("model", [
    "kling-3.0/video", "kling-2.6/image-to-video", "kling/ai-avatar-standard", "omnihuman-1.5"])
def test_video_models_are_detected(model):
    assert gates.is_video_model(model)


def test_video_blocked_without_episode(monkeypatch):
    monkeypatch.delenv("BENTLEY_EPISODE", raising=False)
    monkeypatch.delenv("BENTLEY_GATE_OVERRIDE", raising=False)
    with pytest.raises(PermissionError, match="no episode is declared"):
        gates.assert_spend_allowed("kling-3.0/video")


def test_video_blocked_when_gate_pending(tmp_path, monkeypatch):
    root = ledger(tmp_path, PENDING)
    monkeypatch.setenv("BENTLEY_EPISODE", "ep9")
    monkeypatch.delenv("BENTLEY_GATE_OVERRIDE", raising=False)
    with pytest.raises(PermissionError, match="unrecorded gate"):
        gates.assert_spend_allowed("kling-3.0/video", root=root)


def test_video_blocked_when_ledger_missing(tmp_path, monkeypatch):
    monkeypatch.setenv("BENTLEY_EPISODE", "ep9")
    monkeypatch.delenv("BENTLEY_GATE_OVERRIDE", raising=False)
    with pytest.raises(PermissionError):
        gates.assert_spend_allowed("kling-3.0/video", root=tmp_path)


def test_video_allowed_when_gate_passed(tmp_path, monkeypatch):
    root = ledger(tmp_path, PASSED)
    monkeypatch.setenv("BENTLEY_EPISODE", "ep9")
    monkeypatch.delenv("BENTLEY_GATE_OVERRIDE", raising=False)
    gates.assert_spend_allowed("kling-3.0/video", root=root)


def test_override_allows_with_loud_banner(monkeypatch, capsys):
    monkeypatch.delenv("BENTLEY_EPISODE", raising=False)
    monkeypatch.setenv("BENTLEY_GATE_OVERRIDE", "owner-approved smoke test")
    gates.assert_spend_allowed("kling-3.0/video")
    assert "GATE OVERRIDE ACTIVE" in capsys.readouterr().err
