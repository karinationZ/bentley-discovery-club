"""Render episodes/<ep>/BOARD.md — the human-readable production canvas — from board.json.

BOARD.md is a DERIVED view: never hand-edit it (edits are overwritten). It exists so a person can read
the board at a glance; the agent reads board.json (or `python -m bentley.board status`). This is what
replaces the hand-narrated GATES.md / HANDOFF.md as the single source of truth."""
from bentley.board import (STATES, state_counts, compute_next_action, sections,
                           shots_in_section, section_renders_done, current_section)

STATE_TAG = {
    "todo": "todo", "keyframe": "keyframe", "kf_approved": "kf-approved",
    "rendered": "rendered", "qc": "qc", "owner_review": "owner-review", "locked": "**LOCKED**",
}

PROTOCOL = [
    "Read the board FIRST, every session — it is the single source of truth (not chat, not prose).",
    "Act only on `next_action` — one shot / one wave at a time (Rule 11).",
    "Update the board after every step (state + a decision row + the asset path).",
    "NEVER touch a LOCKED shot — owner-approval is terminal; QC is a PRE-approval gate only.",
    "A shot advances state only by passing its gate; record the gate.",
    "Reroll ≤2 → RESTAGE → trim/downgrade → flag (the counter lives on the shot).",
    "Cosmetic ≠ ship-blocking — never gate an approval on a cosmetic defect; defer it to assembly.",
]


def _vo_str(shot):
    out = []
    for v in shot.get("vo", []):
        if isinstance(v, dict):
            out.append(v.get("label", "?"))
        else:
            out.append(str(v))
    return ", ".join(out) or "—"


def render_md(board):
    L = []
    ep = board.get("episode", "?")
    L.append(f"# {ep} · {board.get('title','')} — PRODUCTION BOARD")
    L.append("")
    L.append("> **DERIVED VIEW — do not hand-edit.** Rendered from `board.json` by `python -m bentley.board "
             "render`. The board is the single source of truth; `GATES.md`/`HANDOFF.md` are also derived. "
             "Mutate state only through the `bentley.board` CLI.")
    L.append("")
    cr = board.get("credits", {})
    L.append(f"**Stage:** `{board.get('stage','?')}` · **Next action (in order):** {compute_next_action(board)} · "
             f"**Credits:** {cr.get('balance','?')} balance")
    c = state_counts(board)
    L.append("")
    L.append("**Stages:** " + " → ".join(
        (f"**[{s}]**" if s == board.get("stage") else s)
        for s in ["premise", "vo", "animatic", "keyframes", "renders", "assemble", "mix_grade", "qa", "release"]))
    L.append("")
    L.append("**Shot states:** " + " · ".join(f"{k} {v}" for k, v in c.items() if v))
    L.append("")

    # ---- asset manifest
    canon = board.get("canon", {})
    if canon:
        L.append("## Locked asset manifest (the canon — one reference for every shot)")
        L.append("")
        if canon.get("style_anchor"):
            L.append(f"- **Style anchor:** `{canon['style_anchor']}`")
        for name, c2 in (canon.get("characters") or {}).items():
            bits = " · ".join(f"{k}: `{v}`" for k, v in c2.items())
            L.append(f"- **{name}:** {bits}")
        if canon.get("environments"):
            L.append("- **Environments:** " + " · ".join(f"{k} `{v}`" for k, v in canon["environments"].items()))
        if canon.get("props"):
            L.append("- **Props:** " + " · ".join(f"{k}: {v}" for k, v in canon["props"].items()))
        if canon.get("models_LOCKED"):
            L.append("- **Models LOCKED:** " + " · ".join(f"{k}=`{v}`" for k, v in canon["models_LOCKED"].items())
                     + " — never change the model")
        L.append("")

    # ---- spine
    sp = board.get("spine", {})
    if sp:
        L.append("## Story spine (keep visible — never 'lose the track')")
        L.append("")
        if sp.get("feeling"):
            L.append(f"- **Feeling:** {sp['feeling']}")
        if sp.get("lesson"):
            L.append(f"- **Lesson:** {sp['lesson']}")
        if sp.get("facts"):
            L.append("- **Facts:** " + " · ".join(sp["facts"]))
        L.append("")

    # ---- shot board (grouped by section — produced IN ORDER, one portion at a time)
    L.append("## Shot board")
    L.append("")
    cur = current_section(board)

    def _table(shot_list):
        out = ["| Shot | State | Purpose | VO | Action / staging | Deliverable | Rerolls |",
               "|------|-------|---------|----|------------------|-------------|---------|"]
        for s in shot_list:
            flags = []
            if s.get("must_restage"):
                flags.append("⚠️RESTAGE")
            if s.get("cosmetic_defer"):
                flags.append("cosmetic→assembly")
            tag = STATE_TAG.get(s.get("state", "todo"), s.get("state"))
            out.append(f"| {s.get('sid', s['id'])} | {tag}{(' ' + ' '.join(flags)) if flags else ''} | "
                       f"{s.get('purpose', '—')} | {_vo_str(s)} | {s.get('action', '—')} | "
                       f"{('`' + s['deliverable'] + '`') if s.get('deliverable') else '—'} | {s.get('rerolls', 0)} |")
        return out

    if sections(board):
        for sec in sections(board):
            done = section_renders_done(board, sec["id"])
            st = "✅ reviewed" if sec.get("reviewed") else \
                ("🎬 renders done → ASSEMBLE + VO-review" if done else "… in progress")
            mark = "  ◀ current portion" if cur and cur["id"] == sec["id"] else ""
            L.append(f"### Section {sec['id']} · {sec.get('title', '')} — {st}{mark}")
            L.append("")
            L += _table(shots_in_section(board, sec["id"]))
            L.append("")
    else:
        L += _table(board.get("shots", []))
        L.append("")

    # ---- decisions
    dec = board.get("decisions", [])
    if dec:
        L.append("## Decisions log (structured — supersedes prose)")
        L.append("")
        L.append("| Date | Scope | Decision | Cost | Status |")
        L.append("|------|-------|----------|------|--------|")
        for d in dec:
            L.append(f"| {d.get('date','')} | {d.get('scope','')} | {d.get('decision','')} | "
                     f"{d.get('cost','—')} | {d.get('status','active')} |")
        L.append("")

    # ---- protocol
    L.append("## Agent protocol (the rails)")
    L.append("")
    for i, r in enumerate(PROTOCOL, 1):
        L.append(f"{i}. {r}")
    L.append("")
    return "\n".join(L)
