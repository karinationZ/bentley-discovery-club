#!/usr/bin/env python3
"""EP3 v4 EDL — LIP-SYNC cut. Every Bentley/Marco dialogue beat plays its Kling-Avatar talking CU
(scratch/ep3/talk/<LABEL>.mp4, lip-synced to the same clean VO that plays), intercut with two-shots so
the characters are visibly TALKING TO EACH OTHER (lean, antenna, burrow). Narrator/action beats keep
scene footage. Emits episodes/ep3/shotlists/ep3_assembly.json. Run: python3 episodes/ep3/build_assembly_v4.py"""
import json
from pathlib import Path
ROOT = Path("/project")
VO = "episodes/ep3/vo"; B = "scratch/ep3/bridges"; S = f"{B}/support"; T = "scratch/ep3/talk"
ANTS = "assets/pilot_shots/ep2/motion/a6_34_ants.mp4"
def TK(l): return f"{T}/{l}.mp4"
COLD = f"{B}/coldopen/shot_stab.mp4"; MINTRO = f"{B}/marco_intro/shot_gold2.mp4"; LEAN = f"{B}/lean_help/shot.mp4"
BINTRO = f"{B}/bentley_intro/shot.mp4"; TURN = f"{B}/turn/shot.mp4"; SCOOP = f"{B}/scoop/shot.mp4"
SCOOPUP = f"{B}/scoop_pickup/shot.mp4"; PAW = f"{B}/pawscuff/shot.mp4"; MLOST = f"{B}/marco_lost/shot.mp4"
ANT = f"{B}/antenna/shot.mp4"; BRIDGE = f"{B}/bridge/shot.mp4"; CLIFF = f"{B}/cliffhanger/shot.mp4"
CLIFF2 = f"{B}/cliffhanger2/shot.mp4"; BURROW = f"{B}/burrow_twoshot/shot.mp4"
SCENT = f"{S}/scent_1.png"; SCENTFADE = f"{S}/scent_faded_1.png"; SHADSOLO = f"{S}/shadow_solo_1.png"
CITY1 = f"{S}/city_1.png"; CITY2 = f"{S}/city_2.png"; CITY3 = f"{S}/city_3_1.png"

# (id, dur, [vo], [srcs], voice, note)
BEATS = [
 ("00_title",      3.5, [],               ["TITLE"],                    "narrator", "Title card"),
 ("01_open",       5.0, ["B_hook1"],      [COLD, TK("B_hook1")],        "bentley",  "Cold open: boop the walking crumb + her line"),
 ("02_intro",     11.0, ["N_intro"],      [BINTRO, TURN],               "narrator", "That's Bentley + glowing tag"),
 ("03_reveal",     6.0, ["B_findline"],   [MINTRO, TK("B_findline")],   "bentley",  "The parade of ants + her delighted reaction"),
 ("04_lean",       6.0, ["B_tooheavy"],   [TK("B_tooheavy"), LEAN],     "bentley",  "You're so teeny -- let me carry it (two-shot)"),
 ("05_igotit",     5.0, ["M_igotit"],     [TK("M_igotit")],             "marco",    "Marco: I've got it (lip-sync)"),
 ("06_whatline",   3.0, ["B_whatline"],   [TK("B_whatline")],           "bentley",  "What line? (lip-sync)"),
 ("07_smellpath", 12.0, ["M_smellpath"],  [TK("M_smellpath"), SCENT],   "marco",    "You smell the path (Marco + scent)"),
 ("08_trail",     10.0, ["N_trail"],      [MINTRO, SCENTFADE],          "narrator", "Scent-road secret (fades)"),
 ("09_zoom",      11.5, ["B_zoomit"],     [SCOOPUP, TK("B_zoomit"), SCOOP], "bentley", "Nose/pick up the crumb FIRST, then zoom"),
 ("10_waitno",     2.5, ["M_waitno"],     [TK("M_waitno")],             "marco",    "Not over the PATH!"),
 ("11_scuff",      3.0, [],               [PAW],                        "narrator", "Paws scuff the trail"),
 ("12_oops",       2.8, ["B_oops"],       [TK("B_oops")],               "bentley",  "Did I do a oops?"),
 ("13_lost",       5.5, ["M_lost"],       [TK("M_lost"), MLOST],        "marco",    "Can't find home! (CU + lone ant)"),
 ("14_shadow",     6.0, ["N_shadow"],     [SHADSOLO],                   "narrator", "A single ant, alone"),
 ("15_realize",   13.7, ["B_realize"],    [TK("B_realize"), PAW],       "bentley",  "My paws wiped the road -> stop/look/listen"),
 ("17_youstopped", 4.0, ["M_youstopped"], [TK("M_youstopped")],         "marco",    "You STOPPED! (hopeful)"),
 ("18_smellit",   12.0, ["B_smellit"],    [TK("B_smellit"), PAW],       "bentley",  "I'm SMELLING -- thread where paws never touched"),
 # --- antenna scene: two-shot anchored, Marco stays on her nose ---
 ("19_checkyou",   3.5, ["M_checkyou"],   [ANT, TK("M_checkyou")],      "marco",    "Hold still, let me read you (on her nose)"),
 ("20_antennae",  12.0, ["N_antennae"],   [ANT, TK("M_brave")],         "narrator", "Antennae hello (two-shot)"),
 ("21_crosseyed",  4.0, ["B_crosseyed"],  [ANT, TK("B_crosseyed")],     "bentley",  "Hee -- that tickles! (on her nose)"),
 ("22_brave",      4.5, ["M_brave"],      [ANT, TK("M_brave")],         "marco",    "You smell brave (on her nose)"),
 ("23_bridge",     9.5, ["B_dontgrab"],   [TK("B_dontgrab"), BRIDGE],   "bentley",  "I'm a BRIDGE -- climb on"),
 ("24_rebuild",   11.0, ["N_rebuild"],    [ANTS, MINTRO],               "narrator", "The road comes back to life"),
 ("25_lift",       5.0, ["M_together"],   [TK("M_together"), ANTS],     "marco",    "Lift together HEAVE! + the lift"),
 ("26_strong",     4.5, ["B_strong"],     [TK("B_strong")],             "bentley",  "You're a hundred strong (warm)"),
 ("27_city",      19.5, ["N_city"],       [CITY1, CITY3, CITY2],        "narrator", "The ant CITY reveal (3 interiors)"),
 # --- climax: burrow two-shot anchored, one continuous conversation ---
 ("28_noboss",     7.5, ["M_noboss"],     [BURROW, TK("M_noboss")],     "marco",    "NEW bridge: no boss? all the same?"),
 ("28b_nobody",    6.5, ["M_nobody"],     [TK("M_nobody"), BURROW],     "marco",    "Then I'm... nobody (two-shot reacts)"),
 ("29_youarecity",14.2, ["B_youarecity"], [TK("B_youarecity"), BURROW], "bentley",  "You ARE the city! (leaning in)"),
 ("30_lesson",    12.7, ["B_lesson"],     [TK("B_lesson"), BURROW],     "bentley",  "Her earned lesson (Marco climbs on nose)"),
 ("31_promise",    3.0, ["B_promise"],    [TK("B_promise"), BURROW],    "bentley",  "Stop. Look. Listen. (earned, tag glow)"),
 ("32_button",     6.5, ["N_button"],     [ANTS, BURROW],               "narrator", "Smallest helper carrying a crumb (no talking mouth)"),
 ("33_comesee",    4.0, ["M_comesee"],    [TK("M_comesee"), CLIFF],     "marco",    "Come see -- hurry! + the room"),
 ("34_deepdrop",   6.5, ["B_deepdrop"],   [TK("B_deepdrop"), CLIFF2],   "bentley",  "Is that water? eggs UP"),
 ("35_nexttime",   3.0, [],               ["CARD"],                     "narrator", "NEXT TIME card (real bg)"),
 ("36_outro",     11.0, ["N_outro"],      [CITY2, CITY1],               "narrator", "Outro: the cozy city"),
]


def main():
    shots = []
    for bid, dur, vos, srcs, voice, note in BEATS:
        real = [s for s in srcs if s not in ("TITLE", "CARD")]
        ready = all((ROOT / s).exists() for s in real)
        shots.append({"id": bid, "dur": dur, "status": "ready" if ready else "todo",
                      "voice": voice, "note": note, "srcs": srcs,
                      "vo": ", ".join(f"{VO}/{l}.mp3" for l in vos)})
    out = {"_meta": {"episode": "EP3 v4 — lip-sync + two-shots",
                     "counts": {"total": len(shots), "ready": sum(1 for s in shots if s["status"] == "ready")}},
           "shots": shots}
    p = ROOT / "episodes/ep3/shotlists/ep3_assembly.json"; p.write_text(json.dumps(out, indent=2))
    print(f"-> {p}  {out['_meta']['counts']}")
    for s in shots:
        if s["status"] != "ready":
            print("  TODO", s["id"], [x for x in s["srcs"] if x not in ("TITLE", "CARD") and not (ROOT / x).exists()])


if __name__ == "__main__":
    main()
