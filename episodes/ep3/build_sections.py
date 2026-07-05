#!/usr/bin/env python3
"""EP3 v8 — SECTION-based EDL. One CONTINUOUS scene per logical story section (no per-sentence cuts).
Each section = its concatenated VO over 1-3 continuous shots (each >=3s) of the SAME scene, VO-over-alive.
The ONLY tight-CU with true Avatar sync is Bentley's catchphrase (B_promise). Reuses existing footage.
Emits episodes/ep3/shotlists/ep3_assembly.json. Run: python3 episodes/ep3/build_sections.py"""
import json
from pathlib import Path
ROOT = Path("/project")
VO = "episodes/ep3/vo"; B = "scratch/ep3/bridges"; S = f"{B}/support"; T = "scratch/ep3/talk_graded"
ANTS = "assets/pilot_shots/ep2/motion/a6_34_ants.mp4"
def TK(l): return f"{T}/{l}.mp4"
OMNI_TOGETHER = "scratch/omni_ep3/out/M_together.mp4"  # OmniHuman synced Marco hero shot (pilot win)
# v11 CONVERSATION FIXES (lipsync-pro §2b): in-frame masked Marco + Bentley cut-in. Wrong-speaker gone.
CHECKYOU_FIX   = "scratch/omni_ep3/masktest/antenna_checkyou.mp4"  # M_checkyou: Marco masked, Bentley still
BRAVE_FIX      = "scratch/omni_ep3/masktest/brave_masked.mp4"      # M_brave: Marco masked, Bentley still
# v12 FIXES (motion-QA sweep 2026-07-03): flappers re-shot w/ plate hygiene, style-matched CU, paw law
# v14 FIXES (owner production review 2026-07-03 + butterfly handoff)
OPENING_STAB = "scratch/ep3/v14fix/opening_v2_stab.mp4" # v14b: deshaked cold-open (RETIRED v14d — deshake ADDED wobble)
OPENING_V3   = "scratch/ep3/v14fix/opening_v3.mp4"     # v14d: LOCKED-camera re-render, sharp + smooth (jitter 4.8 vs 10-13)
GOLDANTS     = "scratch/ep3/v14fix/goldants_col.mp4"    # golden-ant column (replaces EP2-style ants)
ANTS_TUNNEL  = "scratch/ep3/v14fix/ants_tunnel.mp4"     # ants file into burrow one by one
BUTTERFLY    = "scratch/ep3/v14fix/butterfly_land_v2st.mp4"  # v14f: locked-cam + sharpen, TAIL-TRIMMED to drop Kling's held last frame (was a 0.17s micro-freeze at the cut)
BUTTERFLY_MID= "scratch/ep3/v14fix/butterfly_mid_v2s.mp4"   # v14f: 3rd beat (watch the monarch) so N_outro's 17.3s spreads over 3 clips -> no freeze-stretch
BUTTERFLY_FLY= "scratch/ep3/v14fix/butterfly_fly_v2s.mp4"   # v14e: crisp re-render + sharpen pass; monarch flies up, Bentley watches -> EP4 hook
TOOHEAVY_FIX   = "scratch/ep3/v12fix/tooheavy_plate.mp4"   # Bentley FULLY visible speaking, Marco still
IGOTIT_FIX     = "scratch/ep3/v12fix/igotit_fix_trim.mp4"  # Marco braces, Bentley MOUTH CLOSED (clean 3s window)
SMELL_MASKED   = "scratch/omni_ep3/masktest/SMELLPATH_masked.mp4"  # Marco synced in-frame, Bentley still
PAWPLAY        = "scratch/ep3/v12fix/pawplay_v3.mp4"       # paw-play: edited FROM coldopen (right scrub bg + small crumb + docked tail)
BIRD_FIX       = "scratch/ep3/v12fix/birdshadow_fix2.mp4"  # QC-passed: coat paws, ONE ant
COLD = f"{B}/coldopen/shot_stab.mp4"; MINTRO = f"{B}/marco_intro/shot_gold2.mp4"; LEAN = f"{B}/lean_help/shot_fix.mp4"; BINTRO = f"{B}/bentley_intro/shot.mp4"
SHOTGOLD = f"{B}/marco_intro/shot_gold.mp4"  # v14d: front team-carrying (twin of MINTRO, kept distinct-by-section)
IGOTIT = f"{B}/igotit_ots/shot_fix.mp4"; SMELL = f"{B}/smellpath_ts/shot.mp4"; SCOOPUP = f"{B}/scoop_pickup/shot.mp4"
SCOOP = f"{B}/scoop/shot.mp4"; PAW = f"{B}/pawscuff/shot.mp4"; WAITNO = f"{B}/waitno_al/shot.mp4"
OOPS = f"{B}/oops_ts/shot.mp4"; MLOST = f"{B}/marco_lost/shot.mp4"; BIRD = f"{B}/birdshadow/shot.mp4"
# lying-Bentley TURN replaced by active-sniffing SNIFF/SNIFF2; antenna gets a TICKLE bonding shot
SNIFF = f"{B}/sniff/shot.mp4"; SNIFF2 = f"{B}/sniff2/shot.mp4"; TICKLE = f"{B}/tickle/shot.mp4"
ANT_WS = f"{B}/antenna_ws/shot_fix.mp4"; BRIDGE = f"{B}/bridge/shot.mp4"
ANT_RELAY = f"{B}/ant_relay/shot.mp4"; STRONG = f"{B}/strong_ts/shot_fix.mp4"; BURROW = f"{B}/burrow_twoshot/shot_fix.mp4"
BURROW2 = f"{B}/burrow2/shot_fix.mp4"; MQ = f"{B}/marco_q/shot.mp4"; CLIFF = f"{B}/cliffhanger/shot.mp4"; CLIFF2 = f"{B}/cliffhanger2/shot.mp4"
# stills replaced by ANIMATED versions (kill the "static scene" complaints)
SCENT = f"{B}/scent_move/shot.mp4"; SCENTF = f"{B}/scentf_move/shot.mp4"; SHAD = f"{B}/shadow_move/shot.mp4"
CITY1 = f"{B}/city1_move/shot.mp4"; CITY2 = f"{B}/city2_move/shot.mp4"; CITY3 = f"{B}/city3_move/shot.mp4"


def P(src, w, lip=False):
    return {"src": src, "dur": w, "lipsync": lip}


# (id, voice, [vo labels in order], [continuous shots — each a scene chunk >=3s])
SECTIONS = [
 ("00_title",   "narrator", [],                                  [P("TITLE", 3.5)]),
 ("s1_open",    "bentley",  ["B_hook1", "N_intro", "B_findline"], [P(OPENING_V3, 5), P(BINTRO, 5), P(MINTRO, 5), P(GOLDANTS, 5)]),  # v14d: sharp locked-cam open; Bentley BEFORE ants (un-flip); 4 clips over 25s VO kills the 0:12 freeze; reveal = front parade -> ant column
 ("s2_meet",    "bentley",  ["B_tooheavy"],  [P(TK("B_tooheavy"), 6.88, True)]),  # v13: synced Avatar CU (was VO-over flap)
 ("s2a_igotit", "marco",    ["M_igotit"],    [P(IGOTIT_FIX, 3), P(SHOTGOLD, 4)]),   # v14d: goldants column moved to s1_open reveal; s2a keeps the team-carrying beat via shot_gold (front) so footage stays distinct
 ("s2b_whatline","bentley", ["B_whatline"],  [P(TK("B_whatline"), 2.3, True)]),   # house-style graded Avatar CU
 ("s2c_smell",  "marco",    ["M_smellpath"], [P(SMELL_MASKED, 5.48, True), P(SCENT, 5)]),  # masked sync then ants
 ("s3_trail",   "narrator", ["N_trail"],                          [P(ANT_RELAY, 5), P(SCENT, 4)]),
 ("s4_pickup",  "bentley",  ["B_zoomit"],                         [P(SCOOPUP, 5), P(SCOOP, 5)]),  # v14b: original scoop scene (owner rejected crumb_nudge: round crumb + blur + freeze)
 ("s5_waitno",  "marco",    ["M_waitno"],    [P(TK("M_waitno"), 2.23, True)]),   # v13: synced Marco CU
 ("s5_oops",    "bentley",  ["B_oops"],      [P(PAW, 4)]),  # B_oops VO-over paw-scuff (no face — staging law OK)
 ("s5b_lost",   "marco",    ["M_lost"],                           [P(TK("M_lost"), 8.53, True)]),   # held Avatar CU (EP2 grammar)
 ("s6_shadow",  "narrator", ["N_shadow"],                         [P(BIRD_FIX, 5), P(SHAD, 3)]),
 ("s7a_realize","bentley",  ["B_realize"],                        [P(TK("B_realize"), 13.87, True)]),  # held Avatar CU
 ("s7_listen",  "bentley",  ["M_youstopped", "B_smellit"],        [P(SNIFF, 5), P(SCENTF, 5), P(SCENT, 5), P(SNIFF2, 5)]),
 ("s8a_checkyou","marco",   ["M_checkyou"],  [P(CHECKYOU_FIX, 1.96, True)]),   # Marco masked on the nose, Bentley still
 ("s8_antenna", "narrator", ["N_antennae", "B_crosseyed_tickle"], [P(ANT_RELAY, 4), P(TICKLE, 5)]),  # v14: "that tickles!" VO-over the tickle animation (owner: fits perfectly); head CU removed
 ("s8b_brave",  "marco",    ["M_brave"],     [P(BRAVE_FIX, 7.24, True)]),      # Marco masked on the nose, Bentley still
 ("s9_bridge",  "bentley",  ["B_dontgrab_v2"], [P(BRIDGE, 7)]),  # v14: warm invitation VO-over the nose-bridge action (bird + "grab and run" removed)
 ("s10_rebuild","narrator", ["N_rebuild"],                        [P(ANT_RELAY, 5), P(GOLDANTS, 5)]),  # v14: golden ants replace EP2-style clip (style match)
 ("s10b_together","marco",  ["M_together"],                       [P(OMNI_TOGETHER, 8.36, True)]),  # OmniHuman synced (pilot-approved)
 ("s10c_strong","bentley",  ["B_strong"],    [P(TK("B_strong"), 5.28, True)]),  # v13: synced Avatar CU (was VO-over flap)
 ("s11_city",   "narrator", ["N_city"],                           [P(CITY1, 5), P(CITY3, 5), P(CITY2, 5)]),
 ("s12a_nowonder","bentley",["B_nowonder"],                       [P(TK("B_nowonder"), 7.1, True)]),   # v14: Bentley wonders (Marco knowing "no boss" was illogical)
 ("s12ab_explain","marco",  ["M_explain"],                        [P(TK("M_explain"), 6.0, True), P(CITY2, 1), P(TK("M_explain"), 8.4, True)]),  # Marco explains, city cutaway breaks the head
 ("s12b_city",  "bentley",  ["B_youarecity_v2"], [P(TK("B_youarecity_v2"), 6.0, True), P(CITY1, 5), P(CITY3, 5)]),  # revised reassurance
 ("s12c_lesson","bentley",  ["B_lesson"],                         [P(TK("B_lesson"), 6.0, True), P(PAW, 1), P(TK("B_lesson"), 6.43, True)]),  # v14: intercut w/ grab-callback (was 15s static head)
 ("s12b_promise","bentley", ["B_promise"],                        [P(TK("B_promise"), 4.5, True)]),  # the ONE Avatar-synced moment
 ("s13_button", "narrator", ["N_button", "M_comesee_v2"],         [P(ANT_RELAY, 3), P(ANTS_TUNNEL, 5), P(BURROW, 3)]),  # trail home -> ants file in -> Bentley peers at hole
 ("s13b_fly",   "narrator", ["N_outro_v2"],                       [P(BUTTERFLY, 5), P(BUTTERFLY_MID, 5), P(BUTTERFLY_FLY, 5)]),  # v14f: 3 beats (land->watch->fly) so 17.3s outro retimes ~1.16x each — NO frozen-push (killed the 4:47 freeze + the 2s end freeze); silent girl, narrator hook
 ("s13c_night", "bentley",  ["B_goodnight"],                      [P(BUTTERFLY_FLY, 3)]),  # v14b: goodnight over the butterfly (Bentley's line; no Marco to mis-flap)
 ("s15_card",   "narrator", [],                                   [P("CARD", 3.5)]),
]


def main():
    shots = []
    for sid, voice, vos, seq in SECTIONS:
        real = [p["src"] for p in seq if p["src"] not in ("TITLE", "CARD")]
        ready = all((ROOT / s).exists() for s in real)
        shots.append({"id": sid, "voice": voice, "status": "ready" if ready else "todo",
                      "seq": seq, "vo": ", ".join(f"{VO}/{l}.mp3" for l in vos)})
    out = {"_meta": {"episode": "EP3 v8 — continuous sections",
                     "counts": {"total": len(shots), "ready": sum(1 for s in shots if s["status"] == "ready")}},
           "shots": shots}
    (ROOT / "episodes/ep3/shotlists/ep3_assembly.json").write_text(json.dumps(out, indent=2))
    print(f"-> ep3_assembly.json  {out['_meta']['counts']}")
    for s in shots:
        if s["status"] != "ready":
            print("  TODO", s["id"], [p["src"] for p in s["seq"] if p["src"] not in ("TITLE", "CARD") and not (ROOT / p["src"]).exists()])


if __name__ == "__main__":
    main()
