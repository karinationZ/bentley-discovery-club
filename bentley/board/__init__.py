"""The Bentley Production Board — the single STRUCTURED state model for episode production.

WHY: the pipeline is rule-complete but was state-POOR — state was *narrated* across a long GATES.md
prose ledger, not *stored*. That is how the EP4 s7b shot got re-QC'd after an owner approval and burned
~210cr. The board makes state first-class: one queryable source of truth the agent reads first and
updates after every step, from which GATES.md / BOARD.md are *derived* (never hand-authored).

FILES (per episode):
  episodes/<ep>/board.json   — source of truth (this module reads/writes it)
  episodes/<ep>/BOARD.md     — human-readable view, RENDERED from board.json (see bentley/board/render.py)

THE PER-SHOT STATE MACHINE (forward-only by one step; owner-approval is TERMINAL):
    todo -> keyframe -> kf_approved -> rendered -> qc -> owner_review -> locked
  - LOCKED is immutable: no advance / reroll / re-render / QC may reopen an owner-approved shot (THE s7b rule).
  - reject() sends a rendered shot back to `keyframe` and bumps its reroll counter; at REROLL_CAP the board
    forces a RESTAGE (a new staged ACTION), never reroll #3.

This module is the model + pure logic (no network, no credits). The CLI is bentley/board/__main__.py;
the Markdown renderer is bentley/board/render.py.
"""
import json
import os

STATES = ["todo", "keyframe", "kf_approved", "rendered", "qc", "owner_review", "locked"]
_IDX = {s: i for i, s in enumerate(STATES)}
REROLL_CAP = 2

# Transitions that require recorded gate evidence before advance() will allow them. The value is the
# human description of the gate; the exact exit-coded tool (image_bestof, scan_suite, …) is run by the
# agent, which then passes its result as evidence. owner_review->locked is handled by lock() (terminal).
GATE_EVIDENCE_REQUIRED = {
    ("keyframe", "kf_approved"): "owner keyframe sign-off (image_bestof pick + paw-zoom)",
    ("kf_approved", "rendered"): "the render clip path (--clip)",
    ("rendered", "qc"): "adversarial QC sweep run (PRE-approval only)",
}

# States from which adversarial QC is a legitimate PRE-approval gate. Once a shot is `locked`, QC is
# disabled by construction — assert_qc_allowed() enforces the s7b rule.
QC_ALLOWED_STATES = {"rendered", "qc"}


class BoardError(RuntimeError):
    """Raised on any illegal board operation (bad transition, touching a locked shot, missing gate)."""


# ----------------------------------------------------------------- load / save

def board_path(ep):
    return os.path.join("episodes", ep, "board.json")


def load(ep):
    p = board_path(ep)
    if not os.path.exists(p):
        raise BoardError(f"no board at {p} — run `python -m bentley.board init {ep}` first")
    with open(p, encoding="utf-8") as f:
        return json.load(f)


def save(ep, board):
    p = board_path(ep)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        json.dump(board, f, indent=2, ensure_ascii=False)
        f.write("\n")


def get_shot(board, sid):
    """Look up a shot by full id ('s1b_nose_taste') OR short key ('s1b'). Ambiguity is an error."""
    hits = [s for s in board.get("shots", []) if s.get("id") == sid or s.get("sid") == sid]
    if len(hits) == 1:
        return hits[0]
    if len(hits) > 1:
        raise BoardError(f"ambiguous shot '{sid}' — matches {[s['id'] for s in hits]}")
    raise BoardError(f"no shot '{sid}' on the board")


# ----------------------------------------------------------------- state machine

def can_advance(shot, to):
    """Return (ok: bool, reason: str). Enforces: locked-immutable, forward-only-by-one, valid state."""
    cur = shot.get("state", "todo")
    if shot.get("locked"):
        return False, (f"{shot['id']} is LOCKED (owner-approved) — immutable. QC/reroll/re-render "
                       f"cannot reopen it. (This is the s7b guardrail.)")
    if cur not in _IDX:
        return False, f"{shot['id']}: corrupt current state '{cur}' (valid: {', '.join(STATES)})"
    if to not in _IDX:
        return False, f"unknown state '{to}' — valid: {', '.join(STATES)}"
    if _IDX[to] != _IDX[cur] + 1:
        nxt = STATES[_IDX[cur] + 1] if _IDX[cur] + 1 < len(STATES) else "(already at end)"
        return False, f"{shot['id']}: can only advance {cur} -> {nxt}, not '{to}' (no skipping/rewinding)"
    return True, ""


def advance(board, sid, to, gate=None, clip=None):
    """Move a shot forward one state. Records gate evidence; sets deliverable when a clip is given.

    Raises BoardError if the move is illegal or a required gate/clip evidence is missing.
    Locking (owner_review -> locked) must go through lock(), not advance()."""
    shot = get_shot(board, sid)
    if to == "locked":
        raise BoardError(f"use `lock` for the terminal owner-approval, not `advance {sid} locked`")
    ok, why = can_advance(shot, to)
    if not ok:
        raise BoardError(why)
    cur = shot.get("state", "todo")
    key = (cur, to)
    if key in GATE_EVIDENCE_REQUIRED:
        # the render transition's evidence IS the clip path; the other gated transitions need --gate.
        if to == "rendered" and not clip:
            raise BoardError(f"{sid}: {cur} -> rendered needs the render clip path (--clip <render.mp4>)")
        if to != "rendered" and not gate:
            raise BoardError(f"{sid}: {cur} -> {to} needs gate evidence — "
                             f"{GATE_EVIDENCE_REQUIRED[key]} (pass --gate '...')")
    if to == "rendered":
        _assert_section_order(board, shot)   # in-order, VO-reviewed portions (owner law)
    shot["state"] = to
    if gate:
        shot.setdefault("gates", {})[to] = gate
    if to == "rendered" and clip:      # deliverable is stamped ONLY at the render transition, never earlier
        shot["deliverable"] = clip
    return shot


def lock(board, sid, clip=None, note=None, force=False):
    """TERMINAL owner-approval lock. Idempotent. After this the shot is immutable (see assert_qc_allowed).

    A shot must be at `owner_review` to lock (the whole machine must have run) — `force=True` bypasses this
    ONLY for migrating a historically-approved shot onto a fresh board (the CLI exposes it as --force)."""
    shot = get_shot(board, sid)
    if shot.get("locked"):
        return shot
    if not force and shot.get("state") != "owner_review":
        raise BoardError(f"{sid} must be at 'owner_review' to lock (is '{shot.get('state', 'todo')}'). "
                         f"Advance it through the machine first, or use force/--force to migrate a "
                         f"historically-approved shot.")
    shot["state"] = "locked"
    shot["locked"] = True
    shot["approved_by_owner"] = True
    if clip:
        shot["deliverable"] = clip
    if note:
        shot["notes"] = note
    return shot


def reject(board, sid, reason):
    """Reject a rendered/qc shot -> back to `keyframe`, bump the reroll counter.

    Returns (shot, must_restage). Refuses to reject a LOCKED shot. At REROLL_CAP the board sets
    must_restage=True (the escalation ladder: reroll <=2 -> RESTAGE, never reroll #3)."""
    shot = get_shot(board, sid)
    if shot.get("locked"):
        raise BoardError(f"{sid} is LOCKED (owner-approved) — cannot reject it. QC never reopens an approval.")
    if shot.get("rerolls", 0) >= REROLL_CAP:
        raise BoardError(f"{sid} is at the reroll cap ({REROLL_CAP}) — RESTAGE it (a NEW staged action / "
                         f"framing), do NOT reroll again. This is the escalation ladder (no reroll #3).")
    shot["rerolls"] = shot.get("rerolls", 0) + 1
    shot["state"] = "keyframe"
    shot.setdefault("reject_log", []).append(reason)
    must_restage = shot["rerolls"] >= REROLL_CAP
    if must_restage:
        shot["must_restage"] = True
    return shot, must_restage


def assert_qc_allowed(shot):
    """THE s7b GUARDRAIL. Adversarial QC is a PRE-approval gate only; raise if the shot is locked.

    Call this before running any post-render QC sweep so an owner-approved clip can never be re-QC'd
    into an autonomous reroll."""
    if shot.get("locked") or shot.get("approved_by_owner"):
        raise BoardError(f"{shot['id']} is owner-APPROVED — adversarial QC is a PRE-approval gate only and "
                         f"must NOT run on a locked shot. Surface any observation as ONE advisory line for "
                         f"the owner to decide; never reroll/re-spend. (s7b cost this rule ~210cr.)")
    return True


# ----------------------------------------------------------------- decisions + queries

def log_decision(board, text, scope="general", cost=None, date=""):
    row = {"date": date, "scope": scope, "decision": text, "status": "active"}
    if cost is not None:
        row["cost"] = cost
    board.setdefault("decisions", []).append(row)
    return row


def state_counts(board):
    c = {s: 0 for s in STATES}
    for shot in board.get("shots", []):
        st = shot.get("state", "todo")
        c[st] = c.get(st, 0) + 1
    return c


def open_shots(board):
    """Shots not yet locked, in board order — the remaining work."""
    return [s for s in board.get("shots", []) if not s.get("locked")]


# ----------------------------------------------------------------- SECTIONS (in-order, VO-reviewed portions)
# Owner law (2026-07-07): produce the episode IN ORDER, in logical portions of ~3-4 shots. When a portion's
# hero renders are all locked, ASSEMBLE that portion WITH VO and get an owner review of the section cut
# BEFORE starting the next portion. The board enforces this: `next` walks in board order within the current
# (earliest un-reviewed) section, and a render is REFUSED if any earlier section isn't owner-reviewed.

def sections(board):
    return board.get("sections", [])


def _sec_index(board, sec_id):
    for i, sec in enumerate(sections(board)):
        if sec.get("id") == sec_id:
            return i
    return -1


def shots_in_section(board, sec_id):
    return [s for s in board.get("shots", []) if s.get("section") == sec_id]


def section_renders_done(board, sec_id):
    """True when every HERO (kling) shot in the section is locked (free pieces are built at assembly)."""
    heroes = [s for s in shots_in_section(board, sec_id) if s.get("plan") == "kling"]
    return all(s.get("locked") for s in heroes) if heroes else bool(shots_in_section(board, sec_id))


def section_reviewed(board, sec_id):
    for sec in sections(board):
        if sec.get("id") == sec_id:
            return bool(sec.get("reviewed"))
    return False


def current_section(board):
    """The active portion = the earliest section not yet owner-reviewed."""
    for sec in sections(board):
        if not sec.get("reviewed"):
            return sec
    return None


def next_shot(board):
    """The single next shot to work: first non-locked shot, in board order, within the current section."""
    cur = current_section(board)
    if not cur:
        return None
    for s in board.get("shots", []):
        if s.get("section") == cur["id"] and not s.get("locked"):
            return s
    return None


def _shot_hint(s):
    if s.get("must_restage"):
        return "restage as a natural ACTION per its VO, then render"
    st = s.get("state", "todo")
    if st == "kf_approved":
        return "render (keyframe locked) → QC → owner approve"
    if st in ("rendered", "qc", "owner_review"):
        return "QC → present → owner approve"
    return "keyframe → owner pick → render"


def compute_next_action(board):
    """Derive the in-order next action from state (do NOT hand-set next_action; this is the truth)."""
    if not sections(board):
        return board.get("next_action") or "(no sections defined — run the sectioning seed)"
    cur = current_section(board)
    if not cur:
        return "ALL portions reviewed → assemble the full episode (mix · grade · §9 QA · release)"
    ns = next_shot(board)
    if ns:
        return f"{ns.get('sid', ns['id'])} — {_shot_hint(ns)}  [section {cur['id']}: {cur.get('title','')}]"
    return (f"section {cur['id']} ('{cur.get('title','')}') renders COMPLETE → ASSEMBLE it with VO and get "
            f"owner review, then `board section-review {board.get('episode','<ep>')} {cur['id']} --cut <cut.mp4>` "
            f"BEFORE the next portion")


def _assert_section_order(board, shot):
    """A render is refused while any EARLIER section is not owner-reviewed (in-order, VO-gated portions)."""
    sec_id = shot.get("section")
    if sec_id is None or not sections(board):
        return
    here = _sec_index(board, sec_id)
    for sec in sections(board):
        if _sec_index(board, sec["id"]) < here and not sec.get("reviewed"):
            raise BoardError(
                f"{shot['id']}: cannot render section {sec_id} — finish + owner-review section {sec['id']} "
                f"('{sec.get('title', '')}') first. Produce IN ORDER, one portion at a time; assemble each "
                f"~3-4-shot portion with VO and get owner review before the next (owner law).")


def review_section(board, sec_id, cut=None):
    """Owner gate: mark a portion reviewed (its VO-assembled section cut approved). Unlocks the next portion."""
    for sec in sections(board):
        if sec.get("id") == sec_id:
            if not section_renders_done(board, sec_id):
                pending = [s.get("sid", s["id"]) for s in shots_in_section(board, sec_id)
                           if s.get("plan") == "kling" and not s.get("locked")]
                raise BoardError(f"section {sec_id} isn't render-complete — hero shots not locked: {pending}")
            sec["reviewed"] = True
            if cut:
                sec["cut"] = cut
            return sec
    raise BoardError(f"no section {sec_id} on the board")
