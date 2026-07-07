"""bentley.board CLI — the ONLY sanctioned way to read/mutate the production board.

  python -m bentley.board init   ep4                     scaffold board.json from the shotlist
  python -m bentley.board status ep4                     the header: stage · next · credits · shot-state counts
  python -m bentley.board next    ep4                     the single next action + the target shot's card
  python -m bentley.board advance ep4 s3a keyframe        move a shot forward one state (gate-checked)
  python -m bentley.board lock    ep4 s7b --clip …mp4     TERMINAL owner-approval lock (immutable)
  python -m bentley.board reject  ep4 s3b --reason "…"    reject a render -> keyframe, bump reroll (cap forces RESTAGE)
  python -m bentley.board log     ep4 "…" --scope s7b --cost 70
  python -m bentley.board set-next  ep4 "…"   /   set-stage ep4 renders
  python -m bentley.board render  ep4                     (re)write episodes/ep4/BOARD.md from board.json
  python -m bentley.board check   ep4                     validate (exit 1 on any problem) — usable as a gate
"""
import argparse
import json
import os
import sys

from bentley import board as B
from bentley.board.render import render_md, STATE_TAG


def _beat(sid):
    parts = sid.split("_", 1)
    return parts[1].replace("_", " ") if len(parts) > 1 else sid


def _vo_labels(shot):
    vo = shot.get("vo")
    if not vo:
        return []
    if isinstance(vo, list):
        raw = vo
    else:
        raw = str(vo).split(",")
    out = []
    for r in raw:
        base = os.path.basename(str(r)).strip()
        if base.endswith(".mp3"):
            base = base[:-4]
        if base:
            out.append({"label": base})
    return out


def _plan(shot):
    seq = shot.get("seq") or []
    plans = [q.get("plan") for q in seq if q.get("plan")]
    if "kling" in plans:
        return "kling"
    if plans:
        return plans[0]
    return shot.get("type", "?")


def cmd_init(a):
    sl = a.shotlist or os.path.join("episodes", a.ep, "shotlists", f"{a.ep}_master.json")
    if not os.path.exists(sl):
        sys.exit(f"shotlist not found: {sl}")
    with open(sl, encoding="utf-8") as f:
        data = json.load(f)
    meta = data.get("_meta", {})
    shots = []
    for s in data.get("shots", []):
        shots.append({
            "id": s["id"], "sid": s["id"].split("_")[0], "beat": _beat(s["id"]), "purpose": "", "action": "",
            "vo": _vo_labels(s), "plan": _plan(s), "cards": [],
            "state": "todo", "rerolls": 0, "deliverable": None,
            "approved_by_owner": False, "locked": False,
        })
    cd = "assets/character_design"
    board = {
        "episode": a.ep, "title": meta.get("title", ""), "guest": meta.get("guest", ""),
        "stage": "premise", "next_action": "",
        "credits": {"balance": None, "spent_ep": 0},
        "canon": {
            "style_anchor": f"{cd}/Bentley_MASTER_pixar.png",
            "characters": {
                "bentley": {"master": f"{cd}/Bentley_MASTER_pixar.png",
                            "turnaround": f"{cd}/Bentley_MODEL_SHEET_turnaround.png",
                            "talking": f"{cd}/Bentley_TALKING_MASTER.png", "voice": "LauraZ"},
            },
            "environments": {}, "props": {"collar": "teal + gold paw-print tag"},
            "models_LOCKED": {"keyframe": "nano-banana-pro", "motion": "kling-3.0/video",
                              "talk": "kling/ai-avatar-standard"},
        },
        "spine": {"feeling": "", "lesson": "", "facts": []},
        "decisions": [],
        "shots": shots,
    }
    if os.path.exists(B.board_path(a.ep)) and not a.force:
        sys.exit(f"{B.board_path(a.ep)} exists — pass --force to overwrite")
    B.save(a.ep, board)
    print(f"initialized {B.board_path(a.ep)} with {len(shots)} shots (all 'todo'). "
          f"Fill canon/spine + seed real state, then `render`.")


def cmd_status(a):
    board = B.load(a.ep)
    c = B.state_counts(board)
    cr = board.get("credits", {})
    print(f"{board['episode']} · {board.get('title','')}")
    print(f"  stage:   {board.get('stage','?')}")
    print(f"  next:    {B.compute_next_action(board)}")
    cs = B.current_section(board)
    if cs:
        print(f"  portion: section {cs['id']} · {cs.get('title','')}  (finish + VO-review before the next)")
    print(f"  credits: {cr.get('balance','?')} balance")
    print("  shots:   " + " · ".join(f"{k}={v}" for k, v in c.items() if v))
    locked = [s['id'] for s in board['shots'] if s.get('locked')]
    if locked:
        print("  LOCKED (immutable): " + ", ".join(locked))


def _print_card(s):
    print(f"  ── {s['id']} · {s.get('beat','')} [{STATE_TAG.get(s.get('state'), s.get('state'))}]")
    print(f"     purpose: {s.get('purpose') or '(unset — name the FEELING)'}")
    vo = ", ".join(v.get("label", "?") if isinstance(v, dict) else str(v) for v in s.get("vo", [])) or "—"
    print(f"     vo:      {vo}")
    print(f"     action:  {s.get('action') or '(unset — stage the feeling as an ACTION, not a pose)'}")
    if s.get("cards"):
        print(f"     cards:   {', '.join(s['cards'])}")
    print(f"     plan:    {s.get('plan','?')}   rerolls: {s.get('rerolls',0)}/{B.REROLL_CAP}"
          + ("  ⚠️ CAP HIT → RESTAGE (no reroll #3)" if s.get("must_restage") else ""))
    if s.get("deliverable"):
        print(f"     clip:    {s['deliverable']}")


def cmd_next(a):
    board = B.load(a.ep)
    print(f"NEXT: {B.compute_next_action(board)}")
    cs = B.current_section(board)
    if not cs:
        print("  all portions reviewed — assemble the full episode (mix · grade · QA · release).")
        return
    ns = B.next_shot(board)
    print(f"  current portion → section {cs['id']}: {cs.get('title','')}   (complete IN ORDER, then VO-review before the next)")
    for s in B.shots_in_section(board, cs["id"]):
        mark = "🔒" if s.get("locked") else ("▶" if ns is not None and s["id"] == ns["id"] else "·")
        print(f"   {mark} {s.get('sid', s['id'])} [{STATE_TAG.get(s.get('state'), s.get('state'))}] {s.get('beat','')}")
    if ns:
        _print_card(ns)
    else:
        print(f"   → all hero shots locked. ASSEMBLE section {cs['id']} with VO, get owner review, then "
              f"`board section-review {a.ep} {cs['id']} --cut <cut.mp4>`.")


def cmd_section(a):
    board = B.load(a.ep)
    secs = B.sections(board)
    if not secs:
        print("no sections defined on the board.")
        return
    for sec in secs:
        sh = B.shots_in_section(board, sec["id"])
        locked = sum(1 for s in sh if s.get("locked"))
        done = B.section_renders_done(board, sec["id"])
        tag = "✅ reviewed" if sec.get("reviewed") else ("🎬 renders done → ASSEMBLE + VO-review" if done else "… in progress")
        cur = " ◀ current" if (B.current_section(board) or {}).get("id") == sec["id"] else ""
        print(f"  {sec['id']}. {sec.get('title','')}  [{tag}]  ({locked}/{len(sh)} locked){cur}")


def cmd_section_review(a):
    board = B.load(a.ep)
    B.review_section(board, a.n, cut=a.cut)
    B.save(a.ep, board)
    print(f"✅ section {a.n} REVIEWED — its VO-assembled cut is owner-approved; the next portion is unlocked."
          + (f"  cut: {a.cut}" if a.cut else ""))


def cmd_advance(a):
    board = B.load(a.ep)
    B.advance(board, a.shot, a.state, gate=a.gate, clip=a.clip)
    B.save(a.ep, board)
    print(f"{a.shot} -> {a.state}" + (f"  (gate: {a.gate})" if a.gate else "")
          + (f"  clip: {a.clip}" if a.clip else ""))


def cmd_lock(a):
    board = B.load(a.ep)
    B.lock(board, a.shot, clip=a.clip, note=a.note, force=a.force)
    B.save(a.ep, board)
    print(f"🔒 {a.shot} LOCKED (owner-approved, immutable). QC can no longer reopen it."
          + (f"  clip: {a.clip}" if a.clip else ""))


def cmd_reject(a):
    board = B.load(a.ep)
    _, must = B.reject(board, a.shot, a.reason)
    B.save(a.ep, board)
    msg = f"{a.shot} rejected -> keyframe (reroll {B.get_shot(board, a.shot)['rerolls']}/{B.REROLL_CAP})"
    print(msg + ("  ⚠️ CAP HIT → RESTAGE the shot (new staged action); do NOT reroll again." if must else ""))


def cmd_log(a):
    board = B.load(a.ep)
    B.log_decision(board, a.text, scope=a.scope, cost=a.cost, date=a.date or "")
    B.save(a.ep, board)
    print(f"logged decision [{a.scope}]: {a.text}")


def cmd_set_next(a):
    board = B.load(a.ep)
    board["next_action"] = a.text
    B.save(a.ep, board)
    print(f"next_action = {a.text}")


def cmd_set_stage(a):
    board = B.load(a.ep)
    board["stage"] = a.stage
    B.save(a.ep, board)
    print(f"stage = {a.stage}")


def _write_html(ep, board):
    from bentley.board.html import render_html
    out = os.path.join("episodes", ep, "board.html")
    with open(out, "w", encoding="utf-8") as f:
        f.write(render_html(board))
    return out


def cmd_render(a):
    board = B.load(a.ep)
    out = os.path.join("episodes", a.ep, "BOARD.md")
    with open(out, "w", encoding="utf-8") as f:
        f.write(render_md(board))
    html = _write_html(a.ep, board)
    print(f"wrote {out} + {html}  (open the .html in a browser)")


def cmd_html(a):
    board = B.load(a.ep)
    out = _write_html(a.ep, board)
    print(f"wrote {out} — open it in a browser")


def cmd_serve(a):
    from bentley.board.serve import serve
    _write_html(a.ep, B.load(a.ep))   # ensure the page is fresh before serving
    serve(a.ep, port=a.port, open_browser=not a.no_open)


def cmd_check(a):
    board = B.load(a.ep)
    problems = []
    for s in board.get("shots", []):
        if s.get("locked") and not s.get("deliverable"):
            problems.append(f"{s['id']}: LOCKED but no deliverable path")
        if s.get("locked") and not s.get("approved_by_owner"):
            problems.append(f"{s['id']}: locked without approved_by_owner")
        if s.get("state") not in B.STATES:
            problems.append(f"{s['id']}: invalid state '{s.get('state')}'")
        d = s.get("deliverable")
        if d and not os.path.exists(d):
            problems.append(f"{s['id']}: deliverable missing on disk: {d}")
        if s.get("locked") and d and s.get("sid") and s["sid"] not in os.path.basename(d):
            problems.append(f"{s['id']}: LOCKED deliverable '{os.path.basename(d)}' does not carry its "
                            f"id '{s['sid']}' — likely the WRONG clip")
        if s.get("rerolls", 0) > B.REROLL_CAP and not s.get("must_restage"):
            problems.append(f"{s['id']}: rerolls>{B.REROLL_CAP} but not flagged must_restage")
    ca = board.get("canon", {}).get("style_anchor")
    if ca and not os.path.exists(ca):
        problems.append(f"canon.style_anchor missing on disk: {ca}")
    if problems:
        print("BOARD CHECK: FAIL")
        for p in problems:
            print("  - " + p)
        sys.exit(1)
    print(f"BOARD CHECK: OK ({len(board.get('shots', []))} shots, "
          f"{sum(1 for s in board['shots'] if s.get('locked'))} locked)")


def main(argv=None):
    ap = argparse.ArgumentParser(prog="bentley.board", description="Bentley production board")
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("init"); p.add_argument("ep"); p.add_argument("--shotlist"); p.add_argument("--force", action="store_true"); p.set_defaults(fn=cmd_init)
    p = sub.add_parser("status"); p.add_argument("ep"); p.set_defaults(fn=cmd_status)
    p = sub.add_parser("next"); p.add_argument("ep"); p.set_defaults(fn=cmd_next)
    p = sub.add_parser("section"); p.add_argument("ep"); p.set_defaults(fn=cmd_section)
    p = sub.add_parser("section-review"); p.add_argument("ep"); p.add_argument("n", type=int); p.add_argument("--cut"); p.set_defaults(fn=cmd_section_review)
    p = sub.add_parser("advance"); p.add_argument("ep"); p.add_argument("shot"); p.add_argument("state"); p.add_argument("--gate"); p.add_argument("--clip"); p.set_defaults(fn=cmd_advance)
    p = sub.add_parser("lock"); p.add_argument("ep"); p.add_argument("shot"); p.add_argument("--clip"); p.add_argument("--note"); p.add_argument("--force", action="store_true", help="migrate a historically-approved shot (bypass the owner_review requirement)"); p.set_defaults(fn=cmd_lock)
    p = sub.add_parser("reject"); p.add_argument("ep"); p.add_argument("shot"); p.add_argument("--reason", required=True); p.set_defaults(fn=cmd_reject)
    p = sub.add_parser("log"); p.add_argument("ep"); p.add_argument("text"); p.add_argument("--scope", default="general"); p.add_argument("--cost", type=int); p.add_argument("--date", default=""); p.set_defaults(fn=cmd_log)
    p = sub.add_parser("set-next"); p.add_argument("ep"); p.add_argument("text"); p.set_defaults(fn=cmd_set_next)
    p = sub.add_parser("set-stage"); p.add_argument("ep"); p.add_argument("stage"); p.set_defaults(fn=cmd_set_stage)
    p = sub.add_parser("render"); p.add_argument("ep"); p.set_defaults(fn=cmd_render)
    p = sub.add_parser("html"); p.add_argument("ep"); p.set_defaults(fn=cmd_html)
    p = sub.add_parser("serve"); p.add_argument("ep"); p.add_argument("--port", type=int, default=8713); p.add_argument("--no-open", action="store_true"); p.set_defaults(fn=cmd_serve)
    p = sub.add_parser("check"); p.add_argument("ep"); p.set_defaults(fn=cmd_check)
    args = ap.parse_args(argv)
    try:
        args.fn(args)
    except B.BoardError as e:
        sys.exit(f"BOARD ERROR: {e}")


if __name__ == "__main__":
    main()
