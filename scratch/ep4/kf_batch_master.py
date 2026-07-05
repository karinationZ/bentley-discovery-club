#!/usr/bin/env python3
"""EP4 KEYFRAME BATCH — MASTER-ANCHORED (owner "Go" 2026-07-05 on the s1b calibration).
⚖️ Model LOCKED = nano-banana-pro (owner law: NEVER change the model).
⚖️ Style = the LITERAL master images; ref order: MASTER FIRST (style+identity), turnaround,
Mira (when in shot), plate LAST (location only). Prompt = the exact approved-calibration language.
12 remaining shots × 3 candidates ≈ 648 cr -> scratch/ep4/kf_batch_master/. Owner picks at gate 4.
(s1b done+locked; s1a/s4a/s8/s11c already prod in kf_fix master style.)"""
import os, sys, concurrent.futures as cf
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from bentley.shared import kie_client, hosting

CD = "assets/character_design"
OUT = os.path.join(os.path.dirname(__file__), "kf_batch_master"); os.makedirs(OUT, exist_ok=True)

FIDELITY = ("Render Bentley EXACTLY as she appears in the first reference image — same character, same "
            "face, same fur, same eye size and shape, same proportions, and the EXACT same render style, "
            "quality, lighting treatment and finish as that first reference image. Do NOT change or "
            "reinterpret the drawing style in any way; do NOT make her more cartoonish or more realistic; "
            "do NOT enlarge her eyes. She has a black face mask, grey chin, brown eyes, floppy folded-down "
            "ears, white chest blaze, short docked tail stub, teal collar with the gold paw-print tag.")
PAW = ("CRITICAL: her paws, feet and lower legs are SOLID RED-FAWN, the exact same color as her coat — "
       "NO white paws, NO white socks, NO white toes.")
MIRAC = ("Mira the monarch butterfly exactly matches the monarch reference image — same cute face, "
         "same wing pattern.")

# sid, plate, mira_in_shot, identity ("body"|"talk"), pose
SHOTS = [
 ("s3a_meet_comeon","meadow",True,"body","Mira the monarch loops once around Bentley's head and zips off down the coastal bluff path; Bentley mid-bounce, ears flopping, eyes bright, launching forward to follow her"),
 ("s3b_plan_gag","meadow",True,"body","Bentley trotting eagerly after Mira with her head tilted quizzically to one side, having slightly overshot the dirt path; Mira looping in the air just ahead of her"),
 ("s4b_copy_sneeze","meadow",True,"body","Bentley with her nose buried in a wildflower, a puff of yellow pollen rising around her muzzle, eyes scrunched up about to sneeze, ears mid-flap; Mira looping nearby, amused"),
 ("s5a_lead_bound","meadow",True,"body","Bentley bounding proudly ahead down the dirt path as if leading the way, chest out, happy; a few monarch butterflies drifting calmly past above the flowers"),
 ("s5b_flower_flop","meadow",True,"body","Bentley having just face-planted belly-down into the soft flower bank, petals flying up around her, dizzy but happy; Mira looping back to check on her"),
 ("s6_turn_river","meadow",False,"talk","a tight head-and-shoulders close-up of Bentley sitting calm and still, eyes soft and warm, mouth gently closed, the gold paw-print Listening Tag on her teal collar glowing softly; soft golden meadow bokeh behind her"),
 ("s7a_reframe_q","meadow",True,"body","Bentley sitting and gazing up in amazement at Mira looping cheerfully in the air above her, Bentley's mouth slightly open in wonder; a long river of monarch butterflies streaming across the sky behind them"),
 ("s7b_mindblown","meadow",True,"body","Bentley mid joyful spin, tongue out, short docked tail-stub mid-wiggle, pure delight; Mira looping playfully around her head"),
 ("s9b_grove_cluster","grove",True,"body","Bentley and Mira prominent in the foreground gazing up together at tall eucalyptus branches blanketed with thousands of clustered orange monarch butterflies"),
 ("s10a_worm","grove",True,"body","Bentley doing a delighted wide-eyed double-take at Mira, who perches beside a small green chrysalis hanging from a twig"),
 ("s10b_fancyworm","grove",True,"body","a warm two-shot: Bentley marveling with soft eyes as Mira fans her wings open beside the green chrysalis on its twig"),
 ("s11a_dusk_reflect","grove",True,"body","a NIGHTTIME, moonlit version of the grove setting: Bentley curling down cozily on the ground with a big sleepy yawn, Mira settling on a low twig beside her; warm, peaceful, soft moonlight"),
]

def hosts():
    return {
        "body": hosting.catbox_host(f"{CD}/Bentley_MASTER_pixar.png"),
        "talk": hosting.catbox_host(f"{CD}/Bentley_TALKING_MASTER.png"),
        "turn": hosting.catbox_host(f"{CD}/Bentley_MODEL_SHEET_turnaround.png"),
        "mira": hosting.catbox_host(f"{CD}/Mira_LOCKED.png"),
        "meadow": hosting.catbox_host(f"{CD}/Meadow_plate.png"),
        "grove": hosting.catbox_host(f"{CD}/Grove_plate.png"),
    }

def gen(shot, H):
    sid, plate, mira, ident, pose = shot
    refs = [H[ident], H["turn"]] + ([H["mira"]] if mira else []) + [H[plate]]
    prompt = (f"{FIDELITY} {PAW} SCENE: {pose} (use the last reference image ONLY for the setting and "
              f"background). {MIRAC if mira else ''} 16:9.")
    inp = {"prompt": prompt, "image_input": refs, "aspect_ratio": "16:9",
           "resolution": "2K", "output_format": "png"}
    got = []
    for i in range(3):
        outp = f"{OUT}/{sid}_c{i}.png"
        if os.path.exists(outp):
            got.append(f"{sid}_c{i} exists"); continue
        try:
            r = kie_client.run("nano-banana-pro", inp, timeout=360, poll=7)
            kie_client.download(r["urls"][0], outp)
            got.append(f"{sid}_c{i} {r['credits']}cr")
        except Exception as e:
            got.append(f"{sid}_c{i} FAIL {e}")
    return " | ".join(got)

def main():
    H = hosts(); print("refs hosted", flush=True)
    with cf.ThreadPoolExecutor(max_workers=4) as ex:
        futs = {ex.submit(gen, s, H): s[0] for s in SHOTS}
        for fu in cf.as_completed(futs):
            print(fu.result(), flush=True)
    print("BATCH DONE", flush=True)

if __name__ == "__main__":
    main()
