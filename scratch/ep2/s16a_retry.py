#!/usr/bin/env python3
"""Retry the #16A bonding color-game two-shot (transient 422 on first run). Edits from BOTH locks."""
import sys, os, json
ROOT = "/project"
sys.path.insert(0, ROOT)
from bentley.shared import kie_client

OUT = f"{ROOT}/scratch/ep2/hero"
BENT_URL = "https://files.catbox.moe/xqf188.png"
INDI_URL = open(f"{ROOT}/assets/character_design/.indi_locked_url.txt").read().strip()

PROMPT = (
 "Playful, joyful TWO-SHOT of two friends at a bright tide pool: BENTLEY, a red-fawn Boxer puppy (black mask, floppy folded "
 "ears, short docked tail, teal collar with a glowing spiral shell, natural dog mouth, NO human teeth) looks delighted and "
 "surprised at INDI the octopus — who is playfully CHANGING COLOR to match her friend: patches of warm RED-FAWN blooming "
 "across her iridescent purple skin (mid color-change), while she KEEPS her TEAL eyes, smooth noseless octopus face and eight "
 "suckered arms, looking pleased with her clever trick. The first reference image = the dog; the second = the purple octopus "
 "(keep her teal-eye identity). Premium Pixar/Bluey 3D cartoon, bright colorful daylight, clean and sharp, NO grain. "
 "NEGATIVE: human teeth, white socks, long tail, nose on the octopus, human eyes on the octopus, film grain, noise, watermark.")

print("bal before:", kie_client.credits())
r = kie_client.run("google/nano-banana-edit",
                   {"prompt": PROMPT, "image_urls": [BENT_URL, INDI_URL], "image_size": "16:9", "output_format": "png"})
lp = f"{OUT}/s16a_colorgame.png"; kie_client.download(r["urls"][0], lp)
print(f"s16a: {r['credits']}cr {r['secs']}s -> {lp}")
print("bal after:", kie_client.credits())
