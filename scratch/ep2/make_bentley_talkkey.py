#!/usr/bin/env python3
"""Bentley talking keyframe: close the mouth on a bright paw-tag CU (near-closed-mouth = cleaner avatar lip-sync).
Run: KIE_KEY=... python3 scratch/ep2/make_bentley_talkkey.py"""
import sys, os, time, subprocess
ROOT = "/project"
sys.path.insert(0, ROOT)
from bentley.shared import kie_client
OUT = f"{ROOT}/assets/character_design/Bentley_talkkey.png"

def host(p):
    return subprocess.check_output(["curl","-s","-F","reqtype=fileupload","-F",f"fileToUpload=@{p}",
                                    "https://catbox.moe/user/api.php"]).decode().strip()

base = host(f"{ROOT}/scratch/ep2/master/bentley_cu_ears.png")
PROMPT = ("Keep this Boxer puppy Bentley EXACTLY the same — identical face, big brown eyes, red-fawn fur, the gold 'Bentley' "
          "paw-print tag, head pose, tide-pool background and bright lighting. Change ONLY her mouth: close it into a soft, "
          "natural, gently-closed dog mouth — NO tongue sticking out, lips softly together, calm friendly expression, NO "
          "human teeth. Do not redraw anything else. No text, no watermark.")
print("bal before:", kie_client.credits())
for i in range(4):
    try:
        r = kie_client.run("nano-banana-pro", {"prompt": PROMPT, "image_input": [base],
                                               "aspect_ratio": "16:9", "resolution": "2K", "output_format": "png"})
        kie_client.download(r["urls"][0], OUT); print(f"DONE {r.get('credits')}cr -> {OUT}"); break
    except Exception as e:
        print(f"  try {i+1}: {str(e)[:70]}"); time.sleep(6)
print("bal after:", kie_client.credits())
