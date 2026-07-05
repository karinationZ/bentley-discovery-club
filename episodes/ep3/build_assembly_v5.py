#!/usr/bin/env python3
"""EP3 v5 EDL — the team's shot-redesign: NO giant talking heads. Every beat is a SEQUENCE of pieces
(two-shot / wide / action / insert leads) with the lip-synced talking CU demoted to a short ~1.3s
CUT-IN. Emits `seq` per beat (src, dur, lipsync); the assembler fills the VO duration, scaling the
wide pieces and keeping the CU short + time-aligned for sync. Run: python3 episodes/ep3/build_assembly_v5.py"""
import json
from pathlib import Path
ROOT = Path("/project")
VO = "episodes/ep3/vo"; B = "scratch/ep3/bridges"; S = f"{B}/support"; T = "scratch/ep3/talk_graded"
ANTS = "assets/pilot_shots/ep2/motion/a6_34_ants.mp4"; ANT_RELAY = f"{B}/ant_relay/shot.mp4"
def TK(l): return f"{T}/{l}.mp4"
# clips
COLD = f"{B}/coldopen/shot_stab.mp4"; BINTRO = f"{B}/bentley_intro/shot.mp4"; TURN = f"{B}/turn/shot_cool.mp4"
MINTRO = f"{B}/marco_intro/shot_gold2.mp4"; LEAN = f"{B}/lean_help/shot.mp4"; SCOOPUP = f"{B}/scoop_pickup/shot.mp4"
SCOOP = f"{B}/scoop/shot.mp4"; PAW = f"{B}/pawscuff/shot.mp4"; MLOST = f"{B}/marco_lost/shot.mp4"
BRIDGE = f"{B}/bridge/shot.mp4"; BURROW = f"{B}/burrow_twoshot/shot.mp4"; BURROW2 = f"{B}/burrow2/shot.mp4"; CLIFF = f"{B}/cliffhanger/shot.mp4"; CLIFF2 = f"{B}/cliffhanger2/shot.mp4"
# NEW two-shots (v5)
ANT_WS = f"{B}/antenna_ws/shot.mp4"; OOPS_TS = f"{B}/oops_ts/shot.mp4"; IGOTIT = f"{B}/igotit_ots/shot.mp4"
STRONG_TS = f"{B}/strong_ts/shot.mp4"; BIRD = f"{B}/birdshadow/shot.mp4"; WAITNO = f"{B}/waitno_al/shot.mp4"; SMELL_TS = f"{B}/smellpath_ts/shot.mp4"
# stills
SCENT = f"{S}/scent_1.png"; SCENTF = f"{S}/scent_faded_1.png"; SHAD = f"{S}/shadow_solo_1c.png"
CITY1 = f"{S}/city_1.png"; CITY2 = f"{S}/city_2.png"; CITY3 = f"{S}/city_3_1.png"


def P(src, dur, lip=False):
    return {"src": src, "dur": dur, "lipsync": lip}


# (id, voice, [vo], [pieces])  — pieces lead with two-shot/wide/action; TK() cut-ins are lip=True
BEATS = [
 ("00_title",     "narrator", [],               [P("TITLE", 3.5)]),
 ("01_open",      "bentley",  ["B_hook1"],       [P(COLD, 2.6), P(TK("B_hook1"), 1.2, True), P(COLD, 1.5)]),
 ("02_intro",     "narrator", ["N_intro"],       [P(BINTRO, 6), P(TURN, 5)]),
 ("03_reveal",    "bentley",  ["B_findline"],    [P(MINTRO, 4.5), P(TK("B_findline"), 1.3, True), P(MINTRO, 3)]),
 ("04_lean",      "bentley",  ["B_tooheavy"],    [P(LEAN, 2.8), P(TK("B_tooheavy"), 1.3, True), P(LEAN, 3)]),
 ("05_igotit",    "marco",    ["M_igotit"],      [P(IGOTIT, 2.6), P(TK("M_igotit"), 1.2, True), P(IGOTIT, 2)]),
 ("06_whatline",  "bentley",  ["B_whatline"],    [P(LEAN, 1.6), P(TK("B_whatline"), 1.2, True)]),
 ("07_smellpath", "marco",    ["M_smellpath"],   [P(SMELL_TS, 4), P(SCENT, 3.5), P(TK("M_smellpath"), 1.4, True), P(SMELL_TS, 3.5)]),
 ("08_trail",     "narrator", ["N_trail"],       [P(ANTS, 5), P(SCENTF, 5)]),
 ("09_zoom",      "bentley",  ["B_zoomit"],      [P(SCOOPUP, 4), P(TK("B_zoomit"), 1.4, True), P(SCOOP, 3), P(SCOOPUP, 3)]),
 ("10_waitno",    "marco",    ["M_waitno"],      [P(WAITNO, 1.9), P(TK("M_waitno"), 0.7, True)]),
 ("11_scuff",     "narrator", [],                [P(PAW, 3)]),
 ("12_oops",      "bentley",  ["B_oops"],        [P(OOPS_TS, 1.6), P(TK("B_oops"), 1.2, True)]),
 ("13_lost",      "marco",    ["M_lost"],        [P(MLOST, 2.5), P(TK("M_lost"), 1.4, True), P(MLOST, 1.6)]),
 ("14_shadow",    "narrator", ["N_shadow"],      [P(SHAD, 6)]),
 ("15_realize",   "bentley",  ["B_realize"],     [P(OOPS_TS, 4), P(PAW, 4), P(TK("B_realize"), 1.4, True), P(OOPS_TS, 4)]),
 ("17_youstopped","marco",    ["M_youstopped"],  [P(STRONG_TS, 2.5), P(TK("M_youstopped"), 1.4, True)]),
 ("18_smellit",   "bentley",  ["B_smellit"],     [P(TURN, 4.5), P(SCENTF, 3.2), P(TK("B_smellit"), 1.3, True), P(TURN, 3.5)]),
 ("19_checkyou",  "marco",    ["M_checkyou"],    [P(ANT_WS, 2.2), P(TK("M_checkyou"), 1.4, True)]),
 ("20_antennae",  "narrator", ["N_antennae"],    [P(ANT_WS, 6), P(ANT_WS, 6)]),
 ("21_crosseyed", "bentley",  ["B_crosseyed"],   [P(ANT_WS, 2.6), P(TK("B_crosseyed"), 1.4, True)]),
 ("22_brave",     "marco",    ["M_brave"],       [P(ANT_WS, 3), P(TK("M_brave"), 1.4, True)]),
 ("23_bridge",    "bentley",  ["B_dontgrab"],    [P(BIRD, 3), P(BRIDGE, 3), P(TK("B_dontgrab"), 1.4, True), P(BRIDGE, 2)]),
 ("24_rebuild",   "narrator", ["N_rebuild"],     [P(ANT_RELAY, 6), P(MINTRO, 5)]),
 ("25_lift",      "marco",    ["M_together"],    [P(ANTS, 2.5), P(TK("M_together"), 1.4, True), P(ANTS, 1)]),
 ("26_strong",    "bentley",  ["B_strong"],      [P(STRONG_TS, 2), P(TK("B_strong"), 1.3, True), P(STRONG_TS, 1.2)]),
 ("27_city",      "narrator", ["N_city"],        [P(CITY1, 6.5), P(CITY3, 6.5), P(CITY2, 6.5)]),
 ("28_noboss",    "marco",    ["M_noboss"],      [P(BURROW2, 3), P(TK("M_noboss"), 1.4, True), P(BURROW, 3)]),
 ("28b_nobody",   "marco",    ["M_nobody"],      [P(BURROW, 3), P(TK("M_nobody"), 1.4, True), P(BURROW2, 2)]),
 ("29_youarecity","bentley",  ["B_youarecity"],  [P(BURROW, 6), P(TK("B_youarecity"), 1.4, True), P(BURROW2, 6.8)]),
 ("30_lesson",    "bentley",  ["B_lesson"],      [P(STRONG_TS, 5), P(TK("B_lesson"), 1.4, True), P(BURROW, 6.3)]),
 ("31_promise",   "bentley",  ["B_promise"],     [P(BURROW, 1.4), P(TK("B_promise"), 1.6, True)]),
 ("32_button",    "narrator", ["N_button"],      [P(ANTS, 3), P(BURROW2, 3.5)]),
 ("33_comesee",   "marco",    ["M_comesee"],     [P(CLIFF, 2.6), P(TK("M_comesee"), 1.4, True)]),
 ("34_deepdrop",  "bentley",  ["B_deepdrop"],    [P(CLIFF2, 5), P(TK("B_deepdrop"), 1.4, True)]),
 ("35_nexttime",  "narrator", [],                [P("CARD", 3)]),
 ("36_outro",     "narrator", ["N_outro"],       [P(CITY2, 5.5), P(CITY1, 5.5)]),
]


def main():
    shots = []
    for bid, voice, vos, seq in BEATS:
        real = [p["src"] for p in seq if p["src"] not in ("TITLE", "CARD")]
        ready = all((ROOT / s).exists() for s in real)
        shots.append({"id": bid, "voice": voice, "status": "ready" if ready else "todo",
                      "seq": seq, "vo": ", ".join(f"{VO}/{l}.mp3" for l in vos)})
    out = {"_meta": {"episode": "EP3 v5 — two-shots + lip-sync cut-ins",
                     "counts": {"total": len(shots), "ready": sum(1 for s in shots if s["status"] == "ready")}},
           "shots": shots}
    p = ROOT / "episodes/ep3/shotlists/ep3_assembly.json"; p.write_text(json.dumps(out, indent=2))
    print(f"-> {p}  {out['_meta']['counts']}")
    for s in shots:
        if s["status"] != "ready":
            print("  TODO", s["id"], [p["src"] for p in s["seq"] if p["src"] not in ("TITLE", "CARD") and not (ROOT / p["src"]).exists()])


if __name__ == "__main__":
    main()
