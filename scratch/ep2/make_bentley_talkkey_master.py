#!/usr/bin/env python3
"""Bentley talking keyframe DERIVED FROM THE APPROVED MASTER (exact Ep1 Bentley). Swap shell->paw tag, into tide-pool,
near-closed mouth. Nano-Banana Pro, [master, pawtag] refs. Run: KIE_KEY=... python3 scratch/ep2/make_bentley_talkkey_master.py"""
import sys, os, time, subprocess
ROOT = "/project"
sys.path.insert(0, ROOT)
from bentley.shared import kie_client
os.makedirs(f"{ROOT}/scratch/ep2/bentley", exist_ok=True)
OUT = f"{ROOT}/scratch/ep2/bentley/Bentley_talkkey_master.png"

def host(p):
    return subprocess.check_output(["curl","-s","-F","reqtype=fileupload","-F",f"fileToUpload=@{p}",
                                    "https://catbox.moe/user/api.php"]).decode().strip()

master = host(f"{ROOT}/assets/character_design/Bentley_MASTER_hero.jpg")
pawtag = host(f"{ROOT}/assets/character_design/Bentley_paw_tag.png")
print("master:", master); print("pawtag:", pawtag)
PROMPT = ("Keep this EXACT Boxer puppy from the FIRST image — identical face, muzzle, big brown eyes, red-fawn fur, white "
          "chest blaze, body proportions, and the same realistic 3D render and style. Do NOT redraw, restyle or change his "
          "face or proportions in any way. Make ONLY these changes: (1) replace the round spiral shell charm on his teal "
          "collar with the glowing gold paw-print 'Bentley' tag from the SECOND image; (2) change the plain studio "
          "background to a bright, sunny, shallow tide-pool with wet rocks, colourful anemones and soft bokeh; (3) frame as "
          "a close-up / medium close-up of his head and chest, facing the camera. Keep his mouth gently CLOSED, soft and "
          "natural — no open mouth, no teeth, no tongue. No text, no watermark, no captions.")
print("bal before:", kie_client.credits())
for i in range(4):
    try:
        r = kie_client.run("nano-banana-pro", {"prompt": PROMPT, "image_input": [master, pawtag],
                                               "aspect_ratio": "16:9", "resolution": "2K", "output_format": "png"})
        kie_client.download(r["urls"][0], OUT); print(f"DONE {r.get('credits')}cr -> {OUT}"); break
    except Exception as e:
        print(f"  try {i+1}: {str(e)[:70]}"); time.sleep(6)
print("bal after:", kie_client.credits())
