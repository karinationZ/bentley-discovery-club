#!/usr/bin/env python3
"""EP3 ASSEMBLY shotlist (v2 — corrected mapping + intercuts). Every VO line plays over the RIGHT
character, and every long beat lists MULTIPLE sources so the assembler intercuts (speaker -> relevant
cutaway -> speaker) instead of pushing one short clip. Emits episodes/ep3/shotlists/ep3_assembly.json.
Run: python3 episodes/ep3/build_assembly.py"""
import json
from pathlib import Path
ROOT = Path("/project")
VO = "episodes/ep3/vo"
B = "scratch/ep3/bridges"
S = f"{B}/support"
ANTS = "assets/pilot_shots/ep2/motion/a6_34_ants.mp4"
# shot library
COLD = f"{B}/coldopen/shot.mp4"; BINTRO = f"{B}/bentley_intro/shot.mp4"; LEAN = f"{B}/lean_help/shot.mp4"
MINTRO = f"{B}/marco_intro/shot_gold.mp4"; MCU = f"{B}/marco_cu/shot.mp4"; SCOOP = f"{B}/scoop/shot.mp4"
MHOPE = f"{B}/marco_hopeful/shot.mp4"; CLIFF2 = f"{B}/cliffhanger2/shot.mp4"
PAW = f"{B}/pawscuff/shot.mp4"; OOPS = f"{B}/realize/shot_oops.mp4"; STRONG = f"{B}/realize/shot_strong.mp4"
MLOST = f"{B}/marco_lost/shot.mp4"; TURN = f"{B}/turn/shot.mp4"; ANT = f"{B}/antenna/shot.mp4"
BRIDGE = f"{B}/bridge/shot.mp4"; MQ = f"{B}/marco_q/shot.mp4"; CITYBTN = f"{B}/city_button/shot.mp4"
BYOU = f"{B}/bentley_youcity/shot.mp4"; BLESS = f"{B}/bentley_lesson/shot.mp4"; CLIFF = f"{B}/cliffhanger/shot.mp4"
SCENT = f"{S}/scent_1.png"; SCENTFADE = f"{S}/scent_faded_1.png"; SHAD1 = f"{S}/shadow_1.png"; SHAD2 = f"{S}/shadow_2.png"; SHADSOLO = f"{S}/shadow_solo_1.png"
CITY1 = f"{S}/city_1.png"; CITY2 = f"{S}/city_2.png"; CITY3 = f"{S}/city_3_1.png"

# (id, dur, [vo labels], [sources -> intercut in order], voice, note)
BEATS = [
    ("00_title",      3.5, [],                ["TITLE"],            "narrator", "Title card"),
    ("01_open",       5.0, ["B_hook1"],       [COLD],              "bentley",  "Cold open: Bentley boops the walking crumb"),
    ("02_intro",     11.0, ["N_intro"],       [BINTRO, TURN],      "narrator", "That's Bentley + her glowing Listening Tag (intro + tag-glow)"),
    ("03_reveal",     5.0, ["B_findline"],    [MINTRO],            "bentley",  "Reveal: a whole parade of ants"),
    ("04_lean",       5.0, ["B_tooheavy"],    [LEAN],              "bentley",  "Let me carry it, little one"),
    ("05_igotit",     5.0, ["M_igotit"],      [MCU],               "marco",    "I've got it -- six legs"),
    ("06_whatline",   2.8, ["B_whatline"],    [LEAN],              "bentley",  "What line?"),
    ("07_smellpath", 12.0, ["M_smellpath"],   [MCU, SCENT],        "marco",    "You smell the path (Marco + the scent road)"),
    ("08_trail",     10.0, ["N_trail"],       [MINTRO, SCENTFADE], "narrator", "The scent-road secret (trail fades -> road is gone)"),
    ("09_zoom",       4.0, ["B_zoomit"],      [SCOOP],             "bentley",  "I'll zoom it to the front!"),
    ("10_waitno",     2.2, ["M_waitno"],      [MCU],               "marco",    "Not over the PATH!"),
    ("11_scuff",      3.0, [],                [PAW],               "narrator", "Paws scuff the trail (causal hinge)"),
    ("12_oops",       2.5, ["B_oops"],        [OOPS],              "bentley",  "Did I do a oops?"),
    ("13_lost",       5.5, ["M_lost"],        [MLOST],             "marco",    "The smell's gone -- I can't find home!"),
    ("14_shadow",     6.0, ["N_shadow"],      [SHADSOLO],          "narrator", "A SINGLE ant, alone under the bird-shadow"),
    ("15_realize",   13.7, ["B_realize"],     [OOPS, PAW],         "bentley",  "My big paws wiped the road (realize)"),
    ("16_stoplook",   3.4, ["B_stoplook"],    [TURN],              "bentley",  "Stop. Look. Listen + Tag glow"),
    ("17_youstopped", 2.0, ["M_youstopped"],  [MHOPE],             "marco",    "You STOPPED! (hopeful look up)"),
    ("18_smellit",   12.0, ["B_smellit"],     [TURN, PAW],         "bentley",  "I'm SMELLING -- a thread left where my PAWS never touched"),
    ("19_checkyou",   2.0, ["M_checkyou"],    [MHOPE],             "marco",    "Let me read you first (Marco)"),
    ("20_antennae",  12.0, ["N_antennae"],    [ANT, MCU],          "narrator", "Ants say hello by antennae"),
    ("21_crosseyed",  3.0, ["B_crosseyed"],   [ANT],               "bentley",  "Hee -- that tickles!"),
    ("22_brave",      4.0, ["M_brave"],       [MHOPE],             "marco",    "You smell brave (Marco)"),
    ("23_bridge",     9.5, ["B_dontgrab"],    [BRIDGE],            "bentley",  "I'm a BRIDGE -- climb on, Marco"),
    ("24_rebuild",   11.0, ["N_rebuild"],     [ANTS, MINTRO],      "narrator", "The road comes back to life"),
    ("25_lift",       5.0, ["M_together"],    [MCU],               "marco",    "Lift -- together -- HEAVE! (Marco rallying)"),
    ("26_strong",     4.5, ["B_strong"],      [BLESS],             "bentley",  "You're a hundred strong (clean Bentley -- avoid the human-teeth frame in shot_strong)"),
    ("27_city",      19.5, ["N_city"],        [CITY1, CITY3, CITY2], "narrator", "The ant CITY reveal: food-store -> nursery -> tunnels (3 interiors)"),
    ("28_nobody",     6.0, ["M_nobody"],      [MQ],                "marco",    "Then I'm... nobody?"),
    ("29_youarecity",14.2, ["B_youarecity"],  [BYOU, CITYBTN, BYOU], "bentley",  "You ARE the city! (Bentley + city intercut)"),
    ("30_lesson",    12.7, ["B_lesson"],      [BLESS, PAW],        "bentley",  "Bentley's earned lesson"),
    ("31_promise",    2.0, ["B_promise"],     [TURN],              "bentley",  "Stop. Look. Listen (earned)"),
    ("32_button",     6.5, ["N_button"],      [MCU, ANTS],         "narrator", "The smallest helper carrying a crumb (Marco + ants hauling the crumb)"),
    ("33_comesee",    3.5, ["M_comesee"],     [MHOPE, CLIFF],      "marco",    "Come see -- hurry! (urgent live Marco lead-in -> the deep room)"),
    ("34_deepdrop",   6.0, ["B_deepdrop"],    [CLIFF2],            "bentley",  "Is that water? eggs carried UP (distinct cliffhanger angle)"),
    ("35_nexttime",   3.0, [],                ["CARD"],            "narrator", "NEXT TIME card"),
    ("36_outro",     11.0, ["N_outro"],       [CITY2, CITY1],      "narrator", "Outro: the cozy glowing city (no cliffhanger repeat)"),
]


def main():
    shots = []
    for bid, dur, vos, srcs, voice, note in BEATS:
        # mark ready if all real-file sources exist (TITLE/CARD are generated)
        real = [s for s in srcs if s not in ("TITLE", "CARD")]
        ready = all((ROOT / s).exists() for s in real)
        shots.append({"id": bid, "dur": dur, "status": "ready" if ready else "todo",
                      "voice": voice, "note": note, "srcs": srcs,
                      "vo": ", ".join(f"{VO}/{l}.mp3" for l in vos)})
    out = {"_meta": {"episode": "Episode 3 — The Ant City Beneath Our Feet (ASSEMBLY v2 intercut)",
                     "counts": {"total": len(shots), "ready": sum(1 for s in shots if s["status"] == "ready")}},
           "shots": shots}
    p = ROOT / "episodes/ep3/shotlists/ep3_assembly.json"
    p.write_text(json.dumps(out, indent=2))
    print(f"-> {p}  {out['_meta']['counts']}")
    miss = [(s["id"], [x for x in s["srcs"] if x not in ('TITLE', 'CARD') and not (ROOT / x).exists()])
            for s in shots if s["status"] != "ready"]
    for mid, mx in miss:
        print("  TODO", mid, mx)


if __name__ == "__main__":
    main()
