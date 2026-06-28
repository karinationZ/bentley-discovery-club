#!/usr/bin/env python3
"""Ep2 — regenerate the 3 Bentley+Indi TWO-SHOTS with fixes: (1) Indi SMALL (head-sized, not dog-sized) —
consistent proportion; (2) Bentley's WHOLE FACE in frame (no crop). Edits from BOTH locks.
Run: KIE_KEY=... python3 scratch/ep2/twoshots_v2.py
"""
import sys, os, json
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
LOOK = ("Premium Pixar/Bluey 3D cartoon, bright colorful tide-pool cove, clean and sharp, NO grain. "
        "First reference image = the dog (Bentley); second = the small purple octopus (Indi, keep her teal-eye identity). "
        "NEGATIVE: cropped face, Bentley's face cut off, giant octopus, octopus as big as the dog, human teeth, white socks, "
        "long tail, nose on octopus, human eyes on octopus, film grain, noise, watermark.")

SHOTS = {
 "s22_pawhold": ("Tender MEDIUM two-shot at the water's edge: Bentley leans down with a gentle caring face and reaches one "
   "front paw toward tiny Indi, whose small slender purple arm reaches up to touch Bentley's paw. " + BENT + " " + INDI + " " + SCALE + " " + LOOK),
 "s16_exchange": ("Heart-to-heart two-shot: Bentley lies calmly, head and face fully in frame, looking down tenderly at tiny "
   "Indi who peeks up from the shallow water beside her. " + BENT + " " + INDI + " " + SCALE + " " + LOOK),
 "s16a_colorgame": ("Playful, joyful two-shot: a delighted, surprised Bentley (whole face in frame) beside tiny Indi, who is "
   "playfully color-matching toward Bentley — patches of red-fawn blooming across her purple skin while she keeps her TEAL "
   "eyes and smooth noseless octopus face. " + BENT + " " + INDI + " " + SCALE + " " + LOOK),
}

print("bal before:", kie_client.credits())
man = {}
for sid, prompt in SHOTS.items():
    try:
        r = kie_client.run("google/nano-banana-edit",
                           {"prompt": prompt, "image_urls": [BENT_URL, INDI_URL], "image_size": "16:9", "output_format": "png"})
        lp = f"{OUT}/{sid}.png"; kie_client.download(r["urls"][0], lp)   # overwrite the v1 two-shots
        man[sid] = {"path": lp, "credits": r["credits"], "secs": r["secs"]}
        print(f"{sid}: {r['credits']}cr {r['secs']}s -> {lp}")
    except Exception as e:
        man[sid] = {"error": str(e)[:200]}; print(f"{sid}: FAILED {str(e)[:200]}")
json.dump(man, open(f"{OUT}/_twoshots_v2.json", "w"), indent=1)
print("bal after:", kie_client.credits())
