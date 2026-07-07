"""Tests for the production-board package (bentley/board) — the STRUCTURED state model.

Covers the per-shot state machine (forward-only-by-one), the LOCKED guardrail (the s7b rule),
the reroll cap → RESTAGE escalation, gate-evidence enforcement, shot lookup by id/sid, the
decision/query helpers, `init` shotlist parsing (via the CLI cmd_* functions), and the BOARD.md
renderer. Pure logic + tmp_path + monkeypatch chdir; no network, no credits, no real episode files.
"""
import argparse
import json
import os

import pytest

from bentley import board as B
from bentley.board import __main__ as M
from bentley.board.render import render_md, PROTOCOL


# --------------------------------------------------------------------- helpers

def make_shot(sid="s1", state="todo", **extra):
    """A minimal shot dict; id defaults to '<sid>_beat' so short-sid lookup differs from full id."""
    shot = {"id": f"{sid}_beat", "sid": sid, "state": state, "rerolls": 0}
    shot.update(extra)
    return shot


def make_board(shots=None, **extra):
    board = {"episode": "epX", "shots": shots if shots is not None else []}
    board.update(extra)
    return board


# --------------------------------------------------------------------- state machine

def test_advance_forward_one_step():
    board = make_board([make_shot("s1", "todo")])
    shot = B.advance(board, "s1", "keyframe")
    assert shot["state"] == "keyframe"


def test_advance_by_more_than_one_raises():
    board = make_board([make_shot("s1", "todo")])
    with pytest.raises(B.BoardError, match="only advance"):
        B.advance(board, "s1", "kf_approved")  # skips 'keyframe'


def test_rewind_raises():
    board = make_board([make_shot("s1", "rendered")])
    with pytest.raises(B.BoardError, match="only advance"):
        B.advance(board, "s1", "keyframe")  # backwards


def test_advance_to_unknown_state_raises():
    board = make_board([make_shot("s1", "todo")])
    with pytest.raises(B.BoardError, match="unknown state"):
        B.advance(board, "s1", "banana")


def test_can_advance_reports_valid_next():
    ok, why = B.can_advance(make_shot("s1", "todo"), "keyframe")
    assert ok and why == ""
    ok, why = B.can_advance(make_shot("s1", "todo"), "rendered")
    assert not ok and "only advance" in why


def test_advance_locked_state_word_routes_to_lock():
    board = make_board([make_shot("s1", "owner_review")])
    with pytest.raises(B.BoardError, match="use `lock`"):
        B.advance(board, "s1", "locked")


# --------------------------------------------------------------------- gate evidence

def test_keyframe_to_kf_approved_needs_gate():
    board = make_board([make_shot("s1", "keyframe")])
    with pytest.raises(B.BoardError, match="needs gate evidence"):
        B.advance(board, "s1", "kf_approved")


def test_keyframe_to_kf_approved_with_gate_succeeds():
    board = make_board([make_shot("s1", "keyframe")])
    shot = B.advance(board, "s1", "kf_approved", gate="owner picked c2")
    assert shot["state"] == "kf_approved"
    assert shot["gates"]["kf_approved"] == "owner picked c2"


def test_kf_approved_to_rendered_accepts_clip_as_evidence():
    board = make_board([make_shot("s1", "kf_approved")])
    shot = B.advance(board, "s1", "rendered", clip="episodes/epX/renders/s1.mp4")
    assert shot["state"] == "rendered"
    assert shot["deliverable"] == "episodes/epX/renders/s1.mp4"


def test_rendered_to_qc_needs_gate():
    board = make_board([make_shot("s1", "rendered")])
    with pytest.raises(B.BoardError, match="needs gate evidence"):
        B.advance(board, "s1", "qc")


def test_ungated_transition_needs_no_evidence():
    # todo -> keyframe is not in GATE_EVIDENCE_REQUIRED
    board = make_board([make_shot("s1", "todo")])
    shot = B.advance(board, "s1", "keyframe")
    assert shot["state"] == "keyframe"


# --------------------------------------------------------------------- LOCKED guardrail (the s7b rule)

def test_advance_on_locked_raises():
    board = make_board([make_shot("s1", "locked", locked=True)])
    with pytest.raises(B.BoardError, match="LOCKED"):
        B.advance(board, "s1", "qc")


def test_reject_on_locked_raises():
    board = make_board([make_shot("s1", "locked", locked=True)])
    with pytest.raises(B.BoardError, match="LOCKED"):
        B.reject(board, "s1", "looks off")


def test_assert_qc_allowed_raises_on_locked():
    with pytest.raises(B.BoardError, match="PRE-approval gate only"):
        B.assert_qc_allowed(make_shot("s1", "locked", locked=True))


def test_assert_qc_allowed_raises_on_owner_approved():
    # approved_by_owner alone (no locked flag) still forbids QC
    with pytest.raises(B.BoardError, match="PRE-approval"):
        B.assert_qc_allowed(make_shot("s1", "rendered", approved_by_owner=True))


def test_assert_qc_allowed_ok_pre_approval():
    assert B.assert_qc_allowed(make_shot("s1", "rendered")) is True
    assert B.assert_qc_allowed(make_shot("s1", "qc")) is True


def test_lock_sets_terminal_flags():
    board = make_board([make_shot("s1", "owner_review")])
    shot = B.lock(board, "s1", clip="final.mp4", note="owner ok")
    assert shot["state"] == "locked"
    assert shot["locked"] is True
    assert shot["approved_by_owner"] is True
    assert shot["deliverable"] == "final.mp4"
    assert shot["notes"] == "owner ok"


def test_lock_is_idempotent():
    board = make_board([make_shot("s1", "owner_review")])
    B.lock(board, "s1", clip="final.mp4")
    # second lock must not clobber the deliverable or raise
    shot = B.lock(board, "s1", clip="OTHER.mp4", note="ignored")
    assert shot["deliverable"] == "final.mp4"
    assert "notes" not in shot
    assert shot["locked"] is True


# --------------------------------------------------------------------- reroll cap → RESTAGE

def test_reject_bumps_reroll_and_returns_to_keyframe():
    board = make_board([make_shot("s1", "rendered")])
    shot, must = B.reject(board, "s1", "drift")
    assert shot["state"] == "keyframe"
    assert shot["rerolls"] == 1
    assert must is False
    assert shot["reject_log"] == ["drift"]
    assert "must_restage" not in shot


def test_reject_hits_cap_forces_restage():
    board = make_board([make_shot("s1", "rendered")])
    B.reject(board, "s1", "reroll #1")
    # bring it back to a rejectable state and reject again to hit the cap
    board["shots"][0]["state"] = "rendered"
    shot, must = B.reject(board, "s1", "reroll #2")
    assert shot["rerolls"] == B.REROLL_CAP == 2
    assert must is True
    assert shot["must_restage"] is True


# --------------------------------------------------------------------- get_shot lookup

def test_get_shot_by_full_id():
    board = make_board([make_shot("s1"), make_shot("s2")])
    assert B.get_shot(board, "s1_beat")["sid"] == "s1"


def test_get_shot_by_short_sid():
    board = make_board([make_shot("s1"), make_shot("s2")])
    assert B.get_shot(board, "s2")["id"] == "s2_beat"


def test_get_shot_missing_raises():
    board = make_board([make_shot("s1")])
    with pytest.raises(B.BoardError, match="no shot"):
        B.get_shot(board, "nope")


def test_get_shot_ambiguous_raises():
    # two shots that both answer to the lookup key 'dup'
    a = {"id": "dup", "sid": "sA", "state": "todo"}
    b = {"id": "other", "sid": "dup", "state": "todo"}
    board = make_board([a, b])
    with pytest.raises(B.BoardError, match="ambiguous"):
        B.get_shot(board, "dup")


# --------------------------------------------------------------------- decisions + queries

def test_log_decision_appends_row():
    board = make_board()
    row = B.log_decision(board, "chose c2", scope="s1", cost=70, date="2026-07-07")
    assert board["decisions"][-1] is row
    assert row == {"date": "2026-07-07", "scope": "s1", "decision": "chose c2",
                   "status": "active", "cost": 70}


def test_log_decision_omits_cost_when_none():
    board = make_board()
    row = B.log_decision(board, "note only")
    assert "cost" not in row
    assert row["scope"] == "general"


def test_state_counts():
    board = make_board([make_shot("s1", "todo"), make_shot("s2", "todo"),
                        make_shot("s3", "locked", locked=True)])
    c = B.state_counts(board)
    assert c["todo"] == 2
    assert c["locked"] == 1
    assert c["rendered"] == 0
    # every canonical state is present as a key
    assert set(B.STATES) <= set(c)


def test_open_shots_excludes_locked_in_order():
    board = make_board([make_shot("s1", "todo"),
                        make_shot("s2", "locked", locked=True),
                        make_shot("s3", "keyframe")])
    ids = [s["sid"] for s in B.open_shots(board)]
    assert ids == ["s1", "s3"]


# --------------------------------------------------------------------- board_path / load / save

def test_load_missing_board_raises(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    with pytest.raises(B.BoardError, match="no board"):
        B.load("epZ")


def test_save_then_load_roundtrips(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    board = make_board([make_shot("s1", "keyframe")], stage="keyframes")
    B.save("epZ", board)
    assert os.path.exists(tmp_path / "episodes" / "epZ" / "board.json")
    loaded = B.load("epZ")
    assert loaded["stage"] == "keyframes"
    assert loaded["shots"][0]["sid"] == "s1"


# --------------------------------------------------------------------- init parsing (via the CLI cmd_ functions)

def _write_shotlist(tmp_path):
    """A tiny fake shotlist: comma-joined vo string, a seq whose plan is kling, a plain type shot."""
    sl = {
        "_meta": {"title": "The Test Episode", "guest": "Testy"},
        "shots": [
            {
                "id": "s1a_nose_taste",
                "type": "beat",
                "vo": "vo/n_intro.mp3, vo/bentley_hi.mp3",
                "seq": [{"plan": "still"}, {"plan": "kling"}],
            },
            {
                "id": "s2b_wide_reveal",
                "type": "broll",
                "vo": ["vo/narrator_line.mp3"],
            },
        ],
    }
    d = tmp_path / "shotlists"
    d.mkdir(parents=True)
    p = d / "epT_master.json"
    p.write_text(json.dumps(sl), encoding="utf-8")
    return str(p)


def _init_args(ep, shotlist, force=False):
    return argparse.Namespace(ep=ep, shotlist=shotlist, force=force)


def test_init_parses_shotlist_into_board(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    sl = _write_shotlist(tmp_path)
    M.cmd_init(_init_args("epT", sl))

    board = B.load("epT")
    assert board["title"] == "The Test Episode"
    assert board["guest"] == "Testy"
    assert board["stage"] == "premise"
    assert len(board["shots"]) == 2

    s1 = B.get_shot(board, "s1a")
    assert s1["id"] == "s1a_nose_taste"
    assert s1["sid"] == "s1a"
    assert s1["beat"] == "nose taste"
    assert s1["state"] == "todo"
    assert s1["rerolls"] == 0
    assert s1["locked"] is False
    # comma-joined vo string parsed into labels, .mp3 stripped, basename only
    assert [v["label"] for v in s1["vo"]] == ["n_intro", "bentley_hi"]
    # a seq containing plan 'kling' wins the plan
    assert s1["plan"] == "kling"

    s2 = B.get_shot(board, "s2b")
    # no seq → falls back to the shot 'type'
    assert s2["plan"] == "broll"
    assert [v["label"] for v in s2["vo"]] == ["narrator_line"]

    out = capsys.readouterr().out
    assert "initialized" in out and "2 shots" in out


def test_init_refuses_overwrite_without_force(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    sl = _write_shotlist(tmp_path)
    M.cmd_init(_init_args("epT", sl))
    with pytest.raises(SystemExit, match="--force"):
        M.cmd_init(_init_args("epT", sl))


def test_init_force_overwrites(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    sl = _write_shotlist(tmp_path)
    M.cmd_init(_init_args("epT", sl))
    M.cmd_init(_init_args("epT", sl, force=True))  # must not raise
    assert len(B.load("epT")["shots"]) == 2


def test_init_missing_shotlist_exits(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    with pytest.raises(SystemExit, match="shotlist not found"):
        M.cmd_init(_init_args("epT", str(tmp_path / "nope.json")))


# --------------------------------------------------------------------- render_md

def _render_board():
    return make_board(
        shots=[
            {"id": "s1_a", "sid": "s1", "state": "keyframe", "purpose": "the hook",
             "vo": [{"label": "n_intro"}], "action": "Bentley sniffs", "rerolls": 1},
            {"id": "s7b_x", "sid": "s7b", "state": "locked", "locked": True,
             "purpose": "reveal", "vo": [{"label": "reveal"}], "action": "big reveal",
             "deliverable": "final/s7b.mp4", "rerolls": 0},
        ],
        title="Render Test",
        stage="renders",
        next_action="render s1",
        credits={"balance": 1200},
        canon={"style_anchor": "assets/anchor.png",
               "characters": {"bentley": {"master": "m.png", "voice": "LauraZ"}},
               "props": {"collar": "teal"}},
        spine={"feeling": "curiosity", "lesson": "look closely", "facts": ["dogs smell"]},
        decisions=[{"date": "2026-07-07", "scope": "s1", "decision": "chose c2",
                    "cost": 70, "status": "active"}],
    )


def test_render_md_has_shot_table_and_states():
    md = render_md(_render_board())
    # the shot table header
    assert "| Shot | State | Purpose | VO | Action / staging | Deliverable | Rerolls |" in md
    # both shots appear as rows (rendered by short sid)
    assert "| s1 |" in md
    assert "| s7b |" in md


def test_render_md_marks_locked_shot():
    md = render_md(_render_board())
    # the locked state tag renders in bold
    assert "**LOCKED**" in md


def test_render_md_includes_agent_protocol():
    md = render_md(_render_board())
    assert "## Agent protocol (the rails)" in md
    for rule in PROTOCOL:
        assert rule in md


def test_render_md_includes_manifest_spine_and_decisions():
    md = render_md(_render_board())
    assert "Locked asset manifest" in md
    assert "assets/anchor.png" in md
    assert "Story spine" in md
    assert "curiosity" in md
    assert "Decisions log" in md
    assert "chose c2" in md


def test_render_md_flags_restage():
    board = make_board(shots=[
        {"id": "s1_a", "sid": "s1", "state": "keyframe", "rerolls": 2, "must_restage": True},
    ])
    md = render_md(board)
    assert "RESTAGE" in md


# ------------------------------------------------- regression tests for the hardening fixes (2026-07-07)

def test_reject_refuses_third_reroll():
    """The reroll cap is ENFORCED, not advisory — a shot already at the cap cannot be rejected again."""
    board = make_board([make_shot("s1", state="rendered", rerolls=B.REROLL_CAP, must_restage=True)])
    with pytest.raises(B.BoardError):
        B.reject(board, "s1", "would be reroll #3")
    assert B.get_shot(board, "s1")["rerolls"] == B.REROLL_CAP  # unchanged


def test_lock_requires_owner_review_or_force():
    """lock() may only fire from owner_review; --force is the migration escape hatch."""
    board = make_board([make_shot("s1", state="todo")])
    with pytest.raises(B.BoardError):
        B.lock(board, "s1", clip="x.mp4")                       # can't skip the machine
    B.lock(board, "s1", clip="x.mp4", force=True)               # migration path
    assert B.get_shot(board, "s1")["locked"] is True
    board2 = make_board([make_shot("s2", state="owner_review")])
    B.lock(board2, "s2", clip="y.mp4")                          # normal terminal path
    assert B.get_shot(board2, "s2")["state"] == "locked"


def test_clip_is_honored_only_on_the_render_transition():
    """A clip must not spoof a keyframe gate, and a deliverable is stamped ONLY at 'rendered'."""
    board = make_board([make_shot("s1", state="keyframe")])
    with pytest.raises(B.BoardError):
        B.advance(board, "s1", "kf_approved", clip="x.mp4")     # gated transition needs --gate, not a clip
    B.advance(board, "s1", "kf_approved", gate="owner pick")
    assert "deliverable" not in B.get_shot(board, "s1") or not B.get_shot(board, "s1")["deliverable"]
    B.advance(board, "s1", "rendered", clip="r.mp4")
    assert B.get_shot(board, "s1")["deliverable"] == "r.mp4"


def test_corrupt_state_raises_boarderror_not_keyerror():
    """A hand-corrupted state must surface as a clean BoardError, not a leaked KeyError."""
    board = make_board([make_shot("s1", state="renderd")])     # typo'd state
    with pytest.raises(B.BoardError):
        B.advance(board, "s1", "qc")


def test_render_html_is_self_contained_and_carries_state():
    """The browser board inlines board.json + renders every shot; no unreplaced template holes."""
    from bentley.board.html import render_html
    board = make_board(
        [make_shot("s1", state="locked", locked=True, deliverable="r/s1_x.mp4", purpose="JOY"),
         make_shot("s2", state="keyframe", must_restage=True)],
        episode="ep9", title="Test", credits={"balance": 1234}, decisions=[{"date": "2026-01-01", "scope": "x", "decision": "d"}])
    html = render_html(board)
    assert "__BOARD_JSON__" not in html and "__TITLE__" not in html
    assert "<!doctype html>" in html and "const INLINE = {" in html
    import re, json
    m = re.search(r"const INLINE = (\{.*?\});\nlet BOARD", html, re.S)
    assert json.loads(m.group(1))["episode"] == "ep9"       # data round-trips
    assert "RESTAGE" in html and "locked" in html           # state surfaced in the view


# ------------------------------------------------- section / in-order production (owner law 2026-07-07)

def _sectioned_board():
    shots = [make_shot("s1", section=1, plan="kling"), make_shot("s2", section=1, plan="card"),
             make_shot("s3", section=2, plan="kling")]
    return make_board(shots, episode="ep9",
                      sections=[{"id": 1, "title": "A", "reviewed": False},
                                {"id": 2, "title": "B", "reviewed": False}])


def test_next_shot_is_first_open_in_current_section():
    b = _sectioned_board()
    assert B.next_shot(b)["sid"] == "s1"
    assert B.current_section(b)["id"] == 1
    assert "s1" in B.compute_next_action(b)


def test_render_gate_blocks_a_later_section():
    b = _sectioned_board()
    B.advance(b, "s3", "keyframe"); B.advance(b, "s3", "kf_approved", gate="p")
    with pytest.raises(B.BoardError):            # section 1 not reviewed → can't render section 2
        B.advance(b, "s3", "rendered", clip="x.mp4")


def test_review_section_gates_and_unlocks_next():
    b = _sectioned_board()
    with pytest.raises(B.BoardError):            # sec 1 hero not locked yet
        B.review_section(b, 1)
    for st, g, c in [("keyframe", None, None), ("kf_approved", "p", None),
                     ("rendered", None, "r.mp4"), ("qc", "q", None), ("owner_review", None, None)]:
        B.advance(b, "s1", st, gate=g, clip=c)
    B.lock(b, "s1", clip="r.mp4")
    B.review_section(b, 1, cut="cut1.mp4")
    assert B.current_section(b)["id"] == 2       # next portion unlocked
    B.advance(b, "s3", "keyframe"); B.advance(b, "s3", "kf_approved", gate="p")
    B.advance(b, "s3", "rendered", clip="x.mp4")  # no longer blocked
    assert B.get_shot(b, "s3")["state"] == "rendered"


def test_serve_reveal_is_sandboxed(tmp_path):
    """The /__open reveal endpoint opens files INSIDE the repo and refuses anything outside it."""
    from bentley.board.serve import reveal
    (tmp_path / "sub").mkdir()
    f = tmp_path / "sub" / "clip.mp4"
    f.write_text("x")
    opened = []
    fake = lambda t: opened.append(t)
    ok, msg = reveal(str(tmp_path), "sub/clip.mp4", opener=fake)
    assert ok and opened == [str(f)]                         # valid in-repo path -> opened
    ok, msg = reveal(str(tmp_path), "../../../etc/passwd", opener=fake)
    assert not ok and "outside" in msg                       # escape attempt -> refused (no open)
    ok, msg = reveal(str(tmp_path), "sub/missing.mp4", opener=fake)
    assert not ok and "not found" in msg
    assert opened == [str(f)]                                 # opener never ran on the bad paths
