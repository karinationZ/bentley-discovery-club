#!/usr/bin/env python3
"""Ep2 keyframe FIX batch (Stage-2 gate re-do): Bentley solo (swap shell->paw tag, NO white socks) + eel silhouette
+ car-sized-crumb ants. Overwrites in assets/pilot_shots/ep2/keyframes/. Run: KIE_KEY=... python3 scratch/ep2/build_kf_fix.py"""
import sys, os, time
from concurrent.futures import ThreadPoolExecutor
ROOT = "/project"
sys.path.insert(0, ROOT)
from bentley.shared import kie_client
from bentley.shared.hosting import catbox_host
from bentley.character_framework import BENTLEY
OUT = f"{ROOT}/assets/pilot_shots/ep2/keyframes"
DOG_BAN = BENTLEY.anatomy.ban()
NOTXT = "No text, no watermark, no captions."
STYLE = "Premium 3D dimensional Pixar soft-fur style, NOT painterly, bright sunny tide-pool."

B   = catbox_host(f"{ROOT}/assets/character_design/Bentley_MASTER_hero.jpg")
PAW = catbox_host(f"{ROOT}/assets/character_design/Bentley_paw_tag.png")

def kBfix(s):
    return (f"Keep this EXACT Boxer puppy Bentley from the FIRST image — identical face, muzzle, brown eyes, red-fawn coat, "
            f"black mask, white chest blaze, proportions, realistic render; do not restyle. SWAP the spiral shell charm on her "
            f"teal collar for the gold paw-print 'Bentley' tag shown in the SECOND image. Her paws are SOLID red-fawn — NO "
            f"white socks, NO white toes, NO white feet. {s} Mouth closed and natural. {DOG_BAN}. {NOTXT} {STYLE}")

SPECS = [
 ("a0_02_boop",   "pro",[B,PAW], kBfix("Place her in the tide pool, creeping low and curious toward a small cute speckled rock, one front paw lifted, reaching to gently boop the rock; ears down.")),
 ("a1_07_chase",  "pro",[B,PAW], kBfix("Place her mid-playful-pounce among several speckled tide-pool rocks; a small jet of water squirts up at her surprised face.")),
 ("a1_09_lunge",  "pro",[B,PAW], kBfix("Place her lunging forward across tide-pool rocks reaching with both front paws as a single curling purple octopus tentacle slips away out of reach; a tiny neat spiral shell sits on the rock.")),
 ("a3_15_settle", "pro",[B,PAW], kBfix("Place her sitting back calmly on her haunches at the tide pool, backing off, soft gentle eyes, ears down, still and patient.")),
 ("a2_12_eelstir","nb", [], f"A long sinuous moray eel rendered as a SOFT DARK SILHOUETTE deep in a shadowy reef crevice — mostly shadow and shape with only a faint single eye-glint, a quiet sense of a lurking predator but GENTLE and not frightening, suitable for ages 4-8. Dim cool light, deep shadow. {NOTXT} {STYLE}"),
 ("a6_34_ants",   "nb", [], f"Cute friendly cartoon ants in a neat line marching across sunlit beach sand, carrying a crumb that is COMICALLY ENORMOUS — about the SIZE OF A CAR compared to the tiny ants — exaggerated playful scale, wonder; the tide-pool cove blurred behind. {NOTXT} {STYLE}"),
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
with ThreadPoolExecutor(max_workers=3) as ex:
    for sid, c in ex.map(run, SPECS):
        print(f"  {sid}: {c}cr" + ("" if c else "  <-- FAILED"), flush=True)
print("bal after:", kie_client.credits(), flush=True)
print("=== KEYFRAME FIX DONE ===", flush=True)
