#!/usr/bin/env python3
"""Retry s22_pawhold + s16_exchange (transient KIE 422s) with internal retries. Edits from BOTH locks."""
import sys, os, json, time
ROOT = "/project"
sys.path.insert(0, ROOT)
from bentley.shared import kie_client

OUT = f"{ROOT}/scratch/ep2/hero"
BENT_URL = "https://files.catbox.moe/xqf188.png"
INDI_URL = open(f"{ROOT}/assets/character_design/.indi_locked_url.txt").read().strip()

BENT = ("Bentley, a young red-fawn Boxer puppy — black mask, floppy folded ears, short docked stubby tail, small white "
        "chest blaze, solid red-fawn paws (NO white socks), teal collar with a glowing spiral shell, natural dog mouth "
        "(soft pink tongue, small dog teeth, NO human teeth).")
INDI = ("Indi, a SMALL octopus — iridescent purple, TEAL lateral eyes (no white sclera), NO nose, NO eyebrows, tiny lipless "
        "mouth, two low blue ocelli, eight suckered arms; octopus-first, never humanlike.")
SCALE = ("CRITICAL SCALE: Indi is a SMALL octopus, about the size of Bentley's HEAD — clearly MUCH smaller than the dog. "
         "Keep Bentley's WHOLE HEAD AND FACE in frame; do NOT crop her face.")
LOOK = ("Premium Pixar/Bluey 3D cartoon, bright colorful tide-pool cove, clean and sharp, NO grain. First reference image = "
        "the dog (Bentley); second = the small purple octopus (Indi, keep her teal-eye identity). NEGATIVE: cropped face, "
        "Bentley's face cut off, giant octopus, octopus as big as the dog, human teeth, white socks, long tail, nose on "
        "octopus, human eyes on octopus, film grain, noise, watermark.")

SHOTS = {
 "s22_pawhold": ("Tender MEDIUM two-shot at the water's edge: Bentley leans down with a gentle caring face and reaches one "
   "front paw toward tiny Indi, whose small slender purple arm reaches up to touch Bentley's paw. " + BENT + " " + INDI + " " + SCALE + " " + LOOK),
 "s16_exchange": ("Heart-to-heart two-shot: Bentley lies calmly, head and face fully in frame, looking down tenderly at tiny "
   "Indi who peeks up from the shallow water beside her. " + BENT + " " + INDI + " " + SCALE + " " + LOOK),
}

def run_retry(prompt, tries=4):
    for i in range(tries):
        try:
            return kie_client.run("google/nano-banana-edit",
                                  {"prompt": prompt, "image_urls": [BENT_URL, INDI_URL], "image_size": "16:9", "output_format": "png"})
        except Exception as e:
            print(f"   attempt {i+1} failed: {str(e)[:90]}"); time.sleep(6)
    return None

print("bal before:", kie_client.credits())
for sid, prompt in SHOTS.items():
    r = run_retry(prompt)
    if r:
        lp = f"{OUT}/{sid}.png"; kie_client.download(r["urls"][0], lp)
        print(f"{sid}: {r['credits']}cr {r['secs']}s -> {lp}")
    else:
        print(f"{sid}: STILL FAILING after retries")
print("bal after:", kie_client.credits())
