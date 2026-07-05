#!/usr/bin/env python3
"""Emit the EP3 animatic shotlist JSON from the EDL. Un-rendered bridges have no src/still ->
animatic auto-cards them (speaker + note). Reuse beats point at EP2 ant footage; establishing at the
inland plate still. Run: python3 episodes/ep3/build_shotlist.py"""
import json
from pathlib import Path
ROOT = Path("/project")
VO = "episodes/ep3/vo"
ANTS = "assets/pilot_shots/ep2/motion/a6_34_ants.mp4"      # REUSE (EP2 ants column)
PLATE = "scratch/ep3/design/inland_plate_1.png"            # establishing still (provisional pick)

# (id, dur, [vo labels], picture(mp4=src / png=still / None=card), voice, note)
BEATS = [
    ("01_title",        4.0, [],                       PLATE, "narrator", "TITLE over inland sand — a crumb glides past, alone (no animal yet)"),
    ("02_boop",         4.5, ["B_hook1"],              PLATE, "bentley",  "Bentley boops the crumb; it keeps moving"),
    ("03_intro",       13.5, ["N_intro"],              None,  "narrator", "Narrator frames Bentley + the Tag; she pads after the crumb"),
    ("04_reveal_line",  5.0, ["B_findline"],           ANTS,  "bentley",  "Reveal: the crumb rides a line of ants, Marco at the front"),
    ("05_lean_help",    5.0, ["B_tooheavy"],           None,  "bentley",  "Bentley leans to help the tiny one (two-shot scale)"),
    ("06_igotit",       5.0, ["M_igotit"],             None,  "marco",    "Marco plants six legs: I've got it... don't break the line"),
    ("07_whatline",     2.5, ["B_whatline"],           None,  "bentley",  "What line? I don't see a line"),
    ("08_smellpath",    6.0, ["M_smellpath"],          None,  "marco",    "Marco: you smell the path, not see it"),
    ("09_scent_road",  11.0, ["N_trail"],              ANTS,  "narrator", "The scent road (fact 1) — ants nose-down following the trail"),
    ("10_zoom",         4.0, ["B_zoomit"],             None,  "bentley",  "I'll zoom it to the front! Bentley scoops the crumb"),
    ("11_waitno",       2.0, ["M_waitno"],             None,  "marco",    "Marco: not over the PATH!"),
    ("12_scuff",        3.0, [],                        None,  "narrator", "Paws scuff the trail flat — THE causal connector (sfx)"),
    ("13_oops",         2.5, ["B_oops"],               None,  "bentley",  "Did I do a oops? (ears drop)"),
    ("14_lost",         5.5, ["M_lost"],               None,  "marco",    "Ants mill in circles; Marco lost, alone on open sand"),
    ("15_shadow",       6.0, ["N_shadow"],             None,  "narrator", "Shadow sweeps; scrub-jay silhouette (soft menace, silhouette only)"),
    ("16_realize",      5.0, ["B_realize"],            None,  "bentley",  "Bentley sees what she did — nose to sand, horrified"),
    ("17_stoplook",     3.4, ["B_stoplook"],           None,  "bentley",  "Stop. Look. Listen. — Listening Tag GLOWS (the turn)"),
    ("18_youstopped",   2.0, ["M_youstopped"],         None,  "marco",    "Marco creeps over, wary: you're not grabbing anymore"),
    ("19_smellit",      8.5, ["B_smellit"],            None,  "bentley",  "Bentley smells the surviving thread (fact 1 used for good)"),
    ("20_checkyou",     2.0, ["M_checkyou"],           None,  "marco",    "Hold still — let me read you"),
    ("21_antennae",     9.5, ["N_antennae"],           None,  "narrator", "Antennae greeting (fact 4) — Marco taps Bentley's nose"),
    ("22_crosseyed",    3.0, ["B_crosseyed"],          None,  "bentley",  "Cross-eyed Bentley, giggling (bonding beat — dog joy)"),
    ("23_brave",        4.0, ["M_brave"],              None,  "marco",    "Seaweed... and dog... and brave. You smell brave"),
    ("24_bridge",       9.5, ["B_dontgrab"],           None,  "bentley",  "Shadow returns; Bentley chooses NOT to scoop — lies flat as a bridge"),
    ("25_rebuild",     11.0, ["N_rebuild"],            ANTS,  "narrator", "Trail rebuilt antenna to antenna (facts 1+4)"),
    ("26_lift",         5.0, ["M_together"],           ANTS,  "marco",    "Lift -- together -- HEAVE! (fact 2 payoff)"),
    ("27_strong",       4.5, ["B_strong"],             None,  "bentley",  "You were never the little one — a hundred strong"),
    ("28_city",        15.0, ["N_city"],               None,  "narrator", "THE ANT CITY reveal (fact 3) — cutaway: tunnels, nursery, jobs"),
    ("29_nobody",       6.0, ["M_nobody"],             None,  "marco",    "Marco, small: if nobody's in charge... am I nobody?"),
    ("30_youarecity",   9.0, ["B_youarecity"],         None,  "bentley",  "You ARE the city! (two-shot thesis, energetic)"),
    ("30b_lesson",     11.4, ["B_lesson"],             None,  "bentley",  "Bentley's EARNED lesson: listening (her nose) beat grabbing"),
    ("30c_promise",     2.0, ["B_promise"],            None,  "bentley",  "Stop. Look. Listen. — the earned catchphrase (button)"),
    ("31_button",       6.5, ["N_button"],             None,  "narrator", "Cozy closing fact over the two of them"),
    ("32_comesee",      3.5, ["M_comesee"],            None,  "marco",    "Marco leads to the deep chamber: come see, hurry"),
    ("33_deepdrop",     6.0, ["B_deepdrop"],           None,  "bentley",  "Water drop in the deep; ants carry eggs UP (cliffhanger)"),
    ("34_nexttime",     3.0, [],                        None,  "narrator", "NEXT TIME: THE FLOOD BENEATH THE SAND (card)"),
    ("35_outro",        6.0, ["N_outro"],              None,  "narrator", "Outro / subscribe (cozy cliffhanger; catchphrase now earned in the button)"),
]


def pic_fields(p):
    if p is None:
        return {}
    if p.lower().endswith((".png", ".jpg", ".jpeg")):
        return {"still": p}
    return {"src": p}


def main():
    shots = []
    for bid, dur, vos, pic, voice, note in BEATS:
        pf = pic_fields(pic)
        ready = bool(pf) and (ROOT / list(pf.values())[0]).exists()
        shots.append({
            "id": bid, "type": ("card" if bid in ("34_nexttime",) else "motion"),
            "dur": dur, "status": "ready" if ready else "todo",
            "voice": voice, "note": note,
            "vo": ", ".join(f"{VO}/{l}.mp3" for l in vos),
            **pf,
        })
    out = {
        "_meta": {
            "episode": "Episode 3 — The Ant City Beneath Our Feet",
            "script": "episodes/ep3/EP3_SCRIPT.md",
            "guest": "Marco (golden-amber boy harvester ant, LOCKED)",
            "note": "Animatic shotlist (zero-credit). todo beats auto-card; ANTS=EP2 reuse; PLATE=inland still. "
                    "This is the STARTING EDL — bridges graduate in place once rendered.",
            "counts": {"total": len(shots), "reuse": sum(1 for s in shots if s["status"] == "ready"),
                       "todo": sum(1 for s in shots if s["status"] == "todo")},
        },
        "shots": shots,
    }
    p = ROOT / "episodes/ep3/shotlists/ep3_animatic.json"
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(out, indent=2))
    print(f"-> {p}  ({len(shots)} beats; {out['_meta']['counts']})")


if __name__ == "__main__":
    main()
