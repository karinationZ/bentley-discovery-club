"""Kontext Edit (bentley/fix/kontext_edit.py) — offline checks only (the tool itself spends KIE
credits; never call the API from tests). Verifies the pure helpers + the no-key guard."""
import pytest

from bentley.fix.kontext_edit import default_out, kontext_edit, tmpfiles_dl_url


def test_default_out():
    assert default_out("/a/b/s10a_worm_c1.png") == "/a/b/s10a_worm_c1_kontext.png"
    assert default_out("frame.jpg") == "frame_kontext.png"


def test_tmpfiles_dl_url():
    assert tmpfiles_dl_url("https://tmpfiles.org/12345/f.png") == "https://tmpfiles.org/dl/12345/f.png"
    # already-direct URLs are left alone
    assert tmpfiles_dl_url("https://tmpfiles.org/dl/12345/f.png") == "https://tmpfiles.org/dl/12345/f.png"


def test_requires_key(monkeypatch, tmp_path):
    monkeypatch.delenv("KIE_KEY", raising=False)
    with pytest.raises(SystemExit, match="KIE_KEY"):
        kontext_edit(str(tmp_path / "x.png"), "Fix ONLY the tail")
