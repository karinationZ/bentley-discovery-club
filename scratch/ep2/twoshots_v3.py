#!/usr/bin/env python3
"""Ep2 — two-shots v3: PRESERVE Indi (do not redraw her). Technique fix per research: let the reference image
do the work, minimal text, explicit 'keep the octopus EXACTLY as in reference 2'. Indi small; Bentley face in frame.
Retry logic for KIE's transient 422s. Run: KIE_KEY=... python3 scratch/ep2/twoshots_v3.py
"""
import sys, os, json, time
ROOT = "/project"
sys.path.insert(0, ROOT)
from bentley.shared import kie_client

OUT = f"{ROOT}/scratch/ep2/hero"
BENT_URL = "https://files.catbox.moe/xqf188.png"
INDI_URL = open(f"{ROOT}/assets/character_design/.indi_locked_url.txt").read().strip()

# Identity-lock: reference does the work; do NOT re-describe Indi's face.
LOCK = ("Combine the two reference images into ONE scene at a bright, colorful tide-pool cove. From the FIRST image keep "
        "BENTLEY the red-fawn Boxer puppy exactly (floppy ears, teal collar with glowing spiral shell, natural dog mouth, "
        "no human teeth), with her WHOLE HEAD AND FACE in frame. From the SECOND image keep INDI the small purple octopus "
        "EXACTLY AS SHE IS — do NOT redraw, restyle, or change her face, eyes, colour or shape in ANY way; she must look "
        "identical to the second reference (small teal eyes, NO nose, NO eyebrows, smooth purple head, two low blue ocelli). "
        "Indi is SMALL — about the size of Bentley's head, much smaller than the dog. Premium Pixar/Bluey 3D, clean, sharp, "
        "no grain. NEGATIVE: changing the octopus, redrawing the octopus, eyebrows on octopus, nose on octopus, human face "
        "on octopus, big/giant octopus, cropped dog face, human teeth, white socks, film grain, watermark.")

SHOTS = {
 "s16_exchange":  LOCK + " POSE: Bentley lies calmly facing tiny Indi, who peeks up from the shallow water on a rock beside her; a tender heart-to-heart, the two looking at each other.",
 "s22_pawhold":   LOCK + " POSE: Bentley leans down and reaches one front paw toward tiny Indi, whose small purple arm reaches up to touch Bentley's paw at the water's edge.",
 "s16a_colorgame":LOCK + " POSE: a delighted Bentley beside tiny Indi, who is playfully turning a few RED-FAWN patches across her purple skin to 'match' her friend (keep her teal eyes + smooth noseless face); both happy and bonding.",
}

def run_retry(prompt, tries=4):
    for i in range(tries):
        try:
            return kie_client.run("google/nano-banana-edit",
                                  {"prompt": prompt, "image_urls": [BENT_URL, INDI_URL], "image_size": "16:9", "output_format": "png"})
        except Exception as e:
            print(f"   attempt {i+1} failed: {str(e)[:80]}"); time.sleep(6)
    return None

print("bal before:", kie_client.credits())
for sid, prompt in SHOTS.items():
    r = run_retry(prompt)
    if r:
        lp = f"{OUT}/{sid}.png"; kie_client.download(r["urls"][0], lp)
        print(f"{sid}: {r['credits']}cr {r['secs']}s -> {lp}")
    else:
        print(f"{sid}: STILL FAILING")
print("bal after:", kie_client.credits())
