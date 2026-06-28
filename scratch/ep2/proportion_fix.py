#!/usr/bin/env python3
"""Fix Bentley-vs-Indi proportion across the 3 two-shots so it's CONSISTENT: Indi's mantle ~= Bentley's HEAD.
Nano Banana Pro, lock-to-reference both characters. Overwrites hero_v2/{s16,s22,s16a}. Retry for KIE flakiness.
Run: KIE_KEY=... python3 scratch/ep2/proportion_fix.py
"""
import sys, os, time
ROOT = "/project"
sys.path.insert(0, ROOT)
from bentley.shared import kie_client

OUT = f"{ROOT}/scratch/ep2/hero_v2"
INDI_URL = open(f"{ROOT}/assets/character_design/.indi_locked_url.txt").read().strip()  # final Indi master
BENT_URL = "https://files.catbox.moe/21y33x.png"  # Bentley-pawtag master (from re-consolidation)

PROP = ("CRITICAL PROPORTION (keep identical in this shot): Indi is a SMALL octopus — her round head/body (mantle) is ABOUT "
        "THE SAME SIZE AS BENTLEY'S HEAD: clearly smaller than the whole dog, but NOT tiny/insignificant; her arms extend out "
        "from the mantle. Use exactly this size ratio.")

BASE = ("Combine the two reference images into one scene at a bright, colorful tide pool. Keep BENTLEY (first image — red-fawn "
        "Boxer puppy with her gold paw-print 'Bentley' name tag, floppy ears, teal collar) and INDI (second image — small "
        "purple octopus with teal eyes and ocelli) EXACTLY as they are; do not redraw either face. " + PROP +
        " Clean, sharp, no grain. NEGATIVE: redrawing the octopus, eyebrows or nose on octopus, octopus bigger than the dog's "
        "head, giant octopus, tiny invisible octopus, cropped dog face, human teeth, film grain.")

SHOTS = {
 "s16_exchange": "POSE: Bentley lies calmly, her whole face in frame, looking down tenderly at Indi who peeks up from the shallow water just beside her.",
 "s22_pawhold": "POSE: Bentley leans down, whole face in frame, gently reaching one front paw toward Indi, whose arm reaches up to touch her paw at the water's edge.",
 "s16a_colorgame": "POSE: a delighted Bentley (whole face in frame) beside Indi, who is playfully turning a few RED-FAWN patches across her purple skin to 'match' her friend (keep her teal eyes + ocelli). Both happy and bonding.",
}

def runpro(prompt, tries=4):
    for i in range(tries):
        try:
            return kie_client.run("nano-banana-pro",
                {"prompt": prompt, "image_input": [BENT_URL, INDI_URL], "aspect_ratio": "16:9", "resolution": "2K", "output_format": "png"})
        except Exception as e:
            print(f"   attempt {i+1}: {str(e)[:80]}", flush=True); time.sleep(6)
    return None

print("bal before:", kie_client.credits(), flush=True)
for sid, pose in SHOTS.items():
    r = runpro(BASE + " " + pose)
    if r:
        lp = f"{OUT}/{sid}.png"; kie_client.download(r["urls"][0], lp)
        print(f"{sid}: {r.get('credits')}cr {r.get('secs')}s -> {lp}", flush=True)
    else:
        print(f"{sid}: FAILED", flush=True)
print("bal after:", kie_client.credits(), flush=True)
print("=== PROPORTION FIX DONE ===", flush=True)
