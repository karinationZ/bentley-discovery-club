#!/usr/bin/env python3
"""Corrected master: ocelli = dimensional/sharp/IRIDESCENT/mysterious but NOT glowing (no emissive light).
Plus an even-smaller PAW tag for Bentley. Edits from s14 (liked look) + Bentley master. Retry for KIE flakiness.
Run: KIE_KEY=... python3 scratch/ep2/master_v2.py
"""
import sys, os, time
ROOT = "/project"
sys.path.insert(0, ROOT)
from bentley.shared import kie_client

OUT = f"{ROOT}/scratch/ep2/master"; os.makedirs(OUT, exist_ok=True)
S14_URL = "https://files.catbox.moe/cretsx.png"   # s14 hosted last run
BENT_URL = "https://files.catbox.moe/xqf188.png"

JOBS = {
 "INDI_MASTER_v2": ([S14_URL],
   "Keep THIS EXACT octopus (Indi) — same face shape, same SMALL teal lateral eyes, same proportions, same iridescent purple "
   "colour as the image. Present her in a clear three-quarter character-design view, soft plain tide-pool background, both "
   "false-eye ocelli visible. The two OCELLI must be DIMENSIONAL, SHARP-EDGED, deep IRIDESCENT blue chain-link rings with a "
   "darker mysterious center and a subtle pearlescent shimmer — three-dimensional and alive like a REAL octopus's ocellus, "
   "NOT flat painted stains. CRITICAL: nothing GLOWS — the ocelli and the eyes are NOT light sources, NO glow, NO neon, NO "
   "emissive light, NOT bright; the ocelli are iridescent MARKINGS, not lamps. Keep her small teal eyes (NOT glowing, no white "
   "sclera, no line), smooth purple head, NO nose, NO eyebrows, tiny lipless mouth, eight small suckered arms. Premium "
   "Pixar/Bluey 3D, clean, sharp, NO grain. NEGATIVE: glowing eyes, glowing ocelli, glow, neon, emissive, bright light-up "
   "rings, lamp eyes, flat painted stains, dull stains, big round eyes, human eyes, white sclera, nose, eyebrows, film grain, watermark."),
 "TAG_paw_small": ([BENT_URL],
   "Macro close-up of Bentley's teal collar. Replace her charm with a VERY SMALL, neat gold PAW-PRINT-shaped name tag — small "
   "and dainty, EVEN SMALLER than a coin — hanging from the teal collar with a soft subtle sheen. Keep the same dog, red-fawn "
   "fur, teal collar. Clean, sharp, NO grain. NEGATIVE: large tag, big tag, oversized charm, huge pendant, bone shape, spiral shell, film grain."),
}

def run_retry(refs, prompt, tries=5):
    for i in range(tries):
        try:
            return kie_client.run("google/nano-banana-edit",
                                  {"prompt": prompt, "image_urls": refs, "image_size": "16:9", "output_format": "png"})
        except Exception as e:
            print(f"   attempt {i+1}: {str(e)[:70]}"); time.sleep(6)
    return None

print("bal before:", kie_client.credits())
for sid,(refs,prompt) in JOBS.items():
    r = run_retry(refs, prompt)
    if r:
        lp = f"{OUT}/{sid}.png"; kie_client.download(r["urls"][0], lp)
        print(f"{sid}: {r['credits']}cr {r['secs']}s -> {lp}")
    else:
        print(f"{sid}: FAILED")
print("bal after:", kie_client.credits())
