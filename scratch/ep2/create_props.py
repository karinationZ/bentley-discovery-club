#!/usr/bin/env python3
"""Create OPEN-MOUTH master props so the AI has a correct reference (no human teeth):
 - Indi_openmouth: soft open octopus mouth, NO teeth (nano-banana-pro edit of Indi_LOCKED).
 - Bentley_openmouth: copy the approved happy CU (tongue out, natural dog mouth, no human teeth).
Run: KIE_KEY=... python3 scratch/ep2/create_props.py
"""
import sys, os, time, shutil, subprocess
ROOT = "/project"
sys.path.insert(0, ROOT)
from bentley.shared import kie_client
CD = f"{ROOT}/assets/character_design"
INDI_URL = open(f"{CD}/.indi_locked_url.txt").read().strip()
OUT_INDI = f"{ROOT}/scratch/ep2/master/Indi_openmouth.png"

PROMPT = ("Keep this octopus Indi EXACTLY the same — same face shape, teal eyes, ocelli, iridescent purple colour and overall "
          "look; do NOT redraw or restyle her. Change ONLY her mouth: open it into a SMALL, SOFT, gentle open mouth — a soft "
          "rounded dark 'oh' opening, as if she is softly speaking or saying 'oh'. It must have NO teeth at all, NO smile, NO "
          "grin — just a soft, smooth, toothless little open octopus mouth. Keep everything else identical. Clean, sharp, no grain.")
INP = {"prompt": PROMPT, "image_input": [INDI_URL], "aspect_ratio": "16:9", "resolution": "2K", "output_format": "png"}

print("bal before:", kie_client.credits())
for i in range(4):
    try:
        r = kie_client.run("nano-banana-pro", INP)
        kie_client.download(r["urls"][0], OUT_INDI)
        print(f"Indi_openmouth: {r.get('credits')}cr -> {OUT_INDI}"); break
    except Exception as e:
        print(f"  try {i+1}: {str(e)[:80]}"); time.sleep(6)
# Bentley open-mouth = the approved happy CU
shutil.copy(f"{ROOT}/scratch/ep2/hero_v2/bentley_cu_awe.png", f"{CD}/Bentley_openmouth.png")
print("Bentley_openmouth: copied from approved happy CU ->", f"{CD}/Bentley_openmouth.png")
print("bal after:", kie_client.credits())
