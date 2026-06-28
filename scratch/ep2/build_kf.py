#!/usr/bin/env python3
"""Ep2 recovery — Stage 2: build the missing motion-shot KEYFRAMES, FROM the approved masters (consistency rule).
Outputs to assets/pilot_shots/ep2/keyframes/. Run: KIE_KEY=... python3 scratch/ep2/build_kf.py"""
import sys, os, time
from concurrent.futures import ThreadPoolExecutor
ROOT = "/project"
sys.path.insert(0, ROOT)
from bentley.shared import kie_client
from bentley.shared.hosting import catbox_host
from bentley.character_framework import BENTLEY, INDI
OUT = f"{ROOT}/assets/pilot_shots/ep2/keyframes"; os.makedirs(OUT, exist_ok=True)

DOG_BAN, OCTO_BAN = BENTLEY.anatomy.ban(), INDI.anatomy.ban()
NOTXT = "No text, no watermark, no captions."
STYLE = "Premium 3D dimensional Pixar soft-fur style, NOT painterly, bright sunny tide-pool."

B   = catbox_host(f"{ROOT}/assets/character_design/Bentley_MASTER_hero.jpg")
I   = catbox_host(f"{ROOT}/assets/character_design/Indi_LOCKED.png")
TWO = catbox_host(f"{ROOT}/scratch/ep2/hero_v2/s16_exchange.png")

def kB(s):   return (f"Keep this EXACT Boxer puppy Bentley from the image — identical face, muzzle, brown eyes, red-fawn coat, "
                     f"black mask, white chest blaze, proportions, teal collar with the gold paw tag, realistic render; do not restyle. "
                     f"{s} Mouth closed and natural. {DOG_BAN}. {NOTXT} {STYLE}")
def kI(s):   return (f"Keep this EXACT octopus Indi from the image — identical teal eyes, two teal ocelli, iridescent purple skin, "
                     f"proportions; do not restyle. {s} {OCTO_BAN}. {NOTXT} {STYLE}")
def kTWO(s): return (f"Keep BOTH characters EXACTLY as in the image — Bentley the red-fawn Boxer (gold paw-tag collar) and Indi the "
                     f"purple two-spot octopus (teal eyes/ocelli); identical faces, proportions, render; do not restyle. {s} "
                     f"{DOG_BAN}. {OCTO_BAN}. {NOTXT} {STYLE}")

# (id, model, image_input, prompt)
SPECS = [
 ("a0_02_boop",   "pro",[B],  kB("Place her in the tide pool, creeping low and curious toward a small cute speckled rock, one front paw lifted, reaching to gently boop the rock; ears down.")),
 ("a1_07_chase",  "pro",[B],  kB("Place her mid-playful-pounce among several speckled tide-pool rocks; a small jet of water squirts up at her surprised face.")),
 ("a1_09_lunge",  "pro",[B],  kB("Place her lunging forward across tide-pool rocks reaching with both front paws as a single curling purple octopus tentacle slips away out of reach; a tiny neat spiral shell sits on the rock.")),
 ("a3_15_settle", "pro",[B],  kB("Place her sitting back calmly on her haunches at the tide pool, backing off, soft gentle eyes, ears down, still and patient.")),
 ("a1_08_camo",   "pro",[I],  kI("Close on her arm and skin against a tide-pool rock, HALF of the skin turned rough, bumpy and stony-grey to camouflage into the rock and the other half still smooth purple — showing the colour-and-texture change.")),
 ("a2_11_bolt",   "pro",[I],  kI("She jets away in a small puff of ink, bolting low toward a dark reef crevice; a sense of speed.")),
 ("a4_25_wedged", "pro",[I],  kI("She is squeezed and wedged into a narrow gap between two tide-pool rocks, eyespots flaring bright, a soft dark eel shadow looming behind.")),
 ("a4_29_reform", "pro",[I],  kI("She has reformed whole and safe on a rock on the far side, body relaxed, eyespots soft, relieved.")),
 ("a2_10_corner", "pro",[TWO],kTWO("Bentley leans in close, gently cornering Indi against a rock crevice; Indi presses back small, her two teal eyespots flaring bright with fear.")),
 ("a4_26_yank",   "pro",[TWO],kTWO("Tension beat: Indi is wedged in a rock gap; Bentley gently grips trying to pull her free, worried and protective; Indi's eyespots flare.")),
 ("a2_12_eelstir","nb", [],   f"A long sinuous moray-eel as a soft dark SILHOUETTE stirring in a shadowy reef crevice, one faint glint of an eye, gentle — NOT scary, suitable for young children. {NOTXT} {STYLE}"),
 ("a6_34_ants",   "nb", [],   f"A perfect long line of cute cartoon ants marching across sunlit beach sand carrying a crumb the SIZE OF A CAR, the tide-pool cove blurred behind, a sense of wonder. {NOTXT} {STYLE}"),
]

def run(spec):
    sid, model, refs, prompt = spec
    outp = f"{OUT}/{sid}.png"
    for i in range(4):
        try:
            if model == "pro":
                r = kie_client.run("nano-banana-pro", {"prompt": prompt, "image_input": refs, "aspect_ratio": "16:9", "resolution": "2K", "output_format": "png"})
            else:
                r = kie_client.run("google/nano-banana", {"prompt": prompt, "image_size": "16:9", "output_format": "png"})
            kie_client.download(r["urls"][0], outp); return (sid, r.get("credits"))
        except Exception as e:
            print(f"  {sid} try {i+1}: {str(e)[:60]}", flush=True); time.sleep(6)
    return (sid, None)

print("bal before:", kie_client.credits(), flush=True)
with ThreadPoolExecutor(max_workers=4) as ex:
    for sid, c in ex.map(run, SPECS):
        print(f"  {sid}: {c}cr" + ("" if c else "  <-- FAILED"), flush=True)
print("bal after:", kie_client.credits(), flush=True)
print("=== KEYFRAMES DONE ===", flush=True)
