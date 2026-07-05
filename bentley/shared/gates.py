#!/usr/bin/env python3
"""Render-spend guard — mechanical enforcement of the Animatic Lock gate (SKILL §1/§10, playbook C10).
Video generation is the expensive failure class (EP3 ran out of credits mid-episode). Any video-model
createTask must trace to an episode whose Animatic Lock is RECORDED as passed in
episodes/<ep>/GATES.md — the same guard idea as episode_builder/animatic.py's ffmpeg-only rule,
applied at the paid layer, so it binds even an agent that read none of the rules.

Usage: export BENTLEY_EPISODE=ep4 before episode renders (the ledger is checked).
       export BENTLEY_GATE_OVERRIDE="<reason>" ONLY for owner-approved non-episode video
       (model smoke tests, channel art) — it prints a loud banner, never silent.
Image models (nano-banana*) are NOT gated: masters/keyframes/plates are the cheap pre-animatic
tier by design (playbook §3.1–3.2)."""
import os
import sys
from pathlib import Path

VIDEO_MARKERS = ("video", "i2v", "image-to-video", "text-to-video", "avatar", "omnihuman",
                 "veo", "seedance", "hailuo", "runway", "pixverse", "wan", "sora", "lipsync")


def repo_root():
    """The repo root = two levels above this file (bentley/shared/gates.py)."""
    return Path(__file__).resolve().parent.parent.parent


def is_video_model(model):
    m = model.lower()
    return any(k in m for k in VIDEO_MARKERS)


def animatic_locked(episode, root=None):
    """True iff episodes/<ep>/GATES.md records the Animatic Lock gate as passed."""
    ledger = Path(root or repo_root()) / "episodes" / episode / "GATES.md"
    if not ledger.exists():
        return False
    for line in ledger.read_text().splitlines():
        low = line.lower()
        if "animatic lock" in low and "pending" not in low and ("✅" in line or "passed" in low):
            return True
    return False


def assert_spend_allowed(model, root=None):
    """Raise PermissionError before a paid VIDEO createTask unless the gate chain allows it."""
    if not is_video_model(model):
        return
    override = os.environ.get("BENTLEY_GATE_OVERRIDE")
    if override:
        print(f"⚠️  GATE OVERRIDE ACTIVE for '{model}': {override} "
              f"(owner-approved non-episode spend only — see CLAUDE.md)", file=sys.stderr)
        return
    episode = os.environ.get("BENTLEY_EPISODE")
    if not episode:
        raise PermissionError(
            f"BLOCKED: '{model}' is a paid VIDEO render and no episode is declared.\n"
            f"  Set BENTLEY_EPISODE=ep<N>  (checks episodes/ep<N>/GATES.md for a PASSED Animatic Lock)\n"
            f"  or BENTLEY_GATE_OVERRIDE='<reason>' for owner-approved non-episode video.\n"
            f"  Rule: no render before the story is locked — episode-production SKILL §1/§10, playbook C10.")
    if not animatic_locked(episode, root):
        ledger = Path(root or repo_root()) / "episodes" / episode / "GATES.md"
        raise PermissionError(
            f"BLOCKED: {ledger} does not record the Animatic Lock as PASSED — an unrecorded gate is\n"
            f"  an unpassed gate. Get owner sign-off on the animatic + credit estimate, record it in\n"
            f"  the ledger, then render. (episode-production SKILL §10 step 4, playbook Part 2 step 6)")
