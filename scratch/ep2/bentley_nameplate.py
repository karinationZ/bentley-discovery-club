#!/usr/bin/env python3
"""Test Bentley's NEW collar charm: glowing engraved 'Bentley' name plate replacing the spiral shell
(it becomes her 'listening' charm). Charm-swap ONLY — keep the dog identical. Edit from Bentley master.
Run: KIE_KEY=... python3 scratch/ep2/bentley_nameplate.py
"""
import sys, os, json
ROOT = "/project"
sys.path.insert(0, ROOT)
from bentley.shared import kie_client

OUT = f"{ROOT}/scratch/ep2/bentley_nameplate"; os.makedirs(OUT, exist_ok=True)
BENT_URL = "https://files.catbox.moe/xqf188.png"  # Bentley_MASTER_clean_16x9

PROMPT = (
 "Edit this image of Bentley the red-fawn Boxer puppy into a tight MACRO CLOSE-UP of her chest and teal collar that FILLS the "
 "frame (head partly out of frame is fine). Show the collar charm large and clear: a small polished GOLD bone-shaped dog-tag "
 "NAME PLATE engraved with the name 'Bentley' in clean, legible capital letters, hanging from the teal collar, emitting a soft "
 "warm magical GLOW (this is her 'listening' charm). NO spiral seashell. Keep her red-fawn fur, small white chest blaze, teal "
 "collar, and the Pixar/Bluey 3D style. Clean, sharp, vibrant, NO grain. "
 "NEGATIVE: spiral shell, seashell, conch, blank tag, gibberish text, misspelled name, white socks, human teeth, film grain, watermark.")

import time
print("bal before:", kie_client.credits())
r = None
for i in range(5):
    try:
        r = kie_client.run("google/nano-banana-edit",
                           {"prompt": PROMPT, "image_urls": [BENT_URL], "image_size": "16:9", "output_format": "png"})
        break
    except Exception as e:
        print(f"   attempt {i+1} failed: {str(e)[:80]}"); time.sleep(6)
if r:
    lp = f"{OUT}/bentley_nameplate_CU.png"; kie_client.download(r["urls"][0], lp)
    print(f"nameplate test: {r['credits']}cr {r['secs']}s -> {lp}")
else:
    print("FAILED after retries")
print("bal after:", kie_client.credits())
