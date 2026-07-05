#!/usr/bin/env python3
"""EP4 KEYFRAME BATCH — PAINTERLY (owner style B, 2026-07-05). nano-banana-pro + painterly style-lock +
plate anchor (calibration proved 4/4 painterly, on-model, clean paws). 3 candidates/shot, threaded.
s3a already done (kf_painterly/). Output -> scratch/ep4/kf_batch/. Owner picks at gate 4."""
import os, sys, concurrent.futures as cf
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from bentley.shared import kie_client, hosting

CD = "assets/character_design"
PLATES = {"meadow": f"{CD}/Meadow_plate.png", "grove": f"{CD}/Grove_plate.png"}
BODY, TURN, MIRA = f"{CD}/Bentley_MASTER_pixar.png", f"{CD}/Bentley_MODEL_SHEET_turnaround.png", f"{CD}/Mira_LOCKED.png"
TALK = f"{CD}/Bentley_TALKING_MASTER.png"
OUT = os.path.join(os.path.dirname(__file__), "kf_batch"); os.makedirs(OUT, exist_ok=True)

STYLE = ("Render the ENTIRE image in the exact same soft, matte, HAND-PAINTED PAINTERLY STORYBOOK "
         "ILLUSTRATION style as the first reference image (the location plate): visible gouache/oil "
         "brushwork, flat painterly shading, soft painted edges, warm illustrated look — hand-painted by "
         "the same illustrator. NOT a glossy smooth 3D render, NOT shiny plastic, NOT CGI, NOT Pixar. "
         "Matte finish; the character painted into the scene with the same brushwork.")
MASTER = ("Keep Bentley's DESIGN identical to the Bentley reference: red-fawn Boxer puppy, black face mask, "
          "grey chin, brown eyes, floppy folded-down ears, white chest blaze, short docked tail stub, teal "
          "collar with the gold paw-print tag; natural realistic puppy proportions, do NOT enlarge her eyes.")
PAW = ("CRITICAL: her paws, feet and lower legs are SOLID RED-FAWN, the exact same color as her coat — "
       "NO white paws, NO white socks, NO white toes.")
MIRAC = "The monarch butterfly Mira exactly matches the monarch reference."

# id, plate, refs-after-plate, needs_mira, pose
SHOTS = [
 ("s1b_nose_taste","meadow",True, "Bentley in 3/4 view, head lowered and eyes crossed looking down at her own nose, where the monarch Mira has just landed and is tapping it; Bentley surprised and delighted, about to yelp"),
 ("s3b_plan_gag","meadow",True, "Bentley trotting eagerly after Mira with her head tilted quizzically to one side, having slightly overshot the dirt path; Mira looping in the air just ahead"),
 ("s4b_copy_sneeze","meadow",True, "Bentley with her nose down in a wildflower, a puff of yellow pollen rising, eyes scrunching for a big sneeze, ears flapping; Mira looping nearby, amused"),
 ("s5a_lead_bound","meadow",True, "Bentley bounding proudly ahead down the dirt path as if leading the way, chest out and happy; a few monarchs drifting calmly past"),
 ("s5b_flower_flop","meadow",True, "Bentley having just face-planted belly-down into the soft flower bank, petals flying up around her, dizzy but happy; Mira looping back to check on her"),
 ("s7a_reframe_q","meadow",True, "Bentley sitting and gazing UP in amazement at Mira, who loops cheerfully in the air above her, Bentley's mouth slightly open in wonder; a river of monarchs streaming in the sky behind"),
 ("s7b_mindblown","meadow",True, "Bentley mid joyful spin, tongue out, short tail-stub wiggling with pure delight; Mira looping playfully around her head"),
 ("s9b_grove_cluster","grove",True, "foreground two-shot: Bentley and the monarch Mira both prominent in the foreground, gazing UP together at eucalyptus branches blanketed with thousands of clustered orange monarchs behind them"),
 ("s10a_worm","grove",True, "Bentley doing a delighted double-take at Mira, who perches beside a green chrysalis on a twig; Bentley's eyes wide with surprise"),
 ("s10b_fancyworm","grove",True, "warm grove two-shot: Bentley marveling with soft eyes as Mira fans her wings open beside the green chrysalis on its twig"),
 ("s11a_dusk_reflect","grove",True, "a NIGHTTIME, moonlit version of the grove: Bentley curling down cozily on the ground with a big sleepy yawn, the monarch Mira settling on a low twig beside her; warm, peaceful, soft moonlight"),
 # catchphrase CU — talking master identity, meadow bokeh, no Mira
 ("s6_turn_river","meadow",False, "a tight head-and-shoulders CLOSE-UP of Bentley (use the Bentley talking-master reference for her face) sitting calm and still, eyes soft and warm, the gold paw-print Listening Tag on her teal collar glowing softly; soft golden-hour meadow bokeh behind"),
]

def hosts():
    h = {k: hosting.catbox_host(v) for k, v in PLATES.items()}
    h["body"], h["turn"], h["mira"], h["talk"] = (hosting.catbox_host(x) for x in (BODY, TURN, MIRA, TALK))
    return h

def gen(shot, H):
    sid, plate, mira, pose = shot
    ident = H["talk"] if sid == "s6_turn_river" else H["body"]
    imgs = [H[plate], ident, H["turn"]] + ([H["mira"]] if mira else [])
    prompt = f"{pose}. {STYLE} {MASTER} {PAW} {MIRAC if mira else ''} 16:9."
    inp = {"prompt": prompt, "image_input": imgs, "aspect_ratio": "16:9", "resolution": "2K", "output_format": "png"}
    done = []
    for i in range(3):
        outp = f"{OUT}/{sid}_c{i}.png"
        if os.path.exists(outp):
            done.append(f"{sid}_c{i} exists"); continue
        try:
            r = kie_client.run("nano-banana-pro", inp, timeout=360, poll=7)
            kie_client.download(r["urls"][0], outp)
            done.append(f"{sid}_c{i} {r['credits']}cr")
        except Exception as e:
            done.append(f"{sid}_c{i} FAIL {e}")
    return " | ".join(done)

def main():
    H = hosts(); print("refs hosted", flush=True)
    with cf.ThreadPoolExecutor(max_workers=4) as ex:
        futs = {ex.submit(gen, s, H): s[0] for s in SHOTS}
        for fu in cf.as_completed(futs):
            print(fu.result(), flush=True)
    print("BATCH DONE", flush=True)

if __name__ == "__main__":
    main()
