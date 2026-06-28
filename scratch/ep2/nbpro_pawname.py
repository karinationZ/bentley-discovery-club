#!/usr/bin/env python3
"""Add the name 'Bentley' inside the paw-print tag on TAG_paw_small via Nano Banana Pro (best text rendering).
Charm-name only; keep the dog + everything else identical. Then I zoom-QA the spelling.
Run: KIE_KEY=... python3 scratch/ep2/nbpro_pawname.py
"""
import sys, os, time, subprocess
ROOT = "/project"
sys.path.insert(0, ROOT)
from bentley.shared import kie_client

SRC = f"{ROOT}/scratch/ep2/master/TAG_paw.png"
OUT = f"{ROOT}/scratch/ep2/master/TAG_paw_LOVED_named.png"

def host(p):
    u = subprocess.check_output(["curl","-s","-F","reqtype=fileupload","-F",f"fileToUpload=@{p}",
                                 "https://catbox.moe/user/api.php"]).decode().strip()
    if not u.startswith("http"): raise RuntimeError("catbox fail")
    return u

PROMPT = ("Keep this image of Bentley the red-fawn Boxer puppy EXACTLY the same in every way. ONLY edit the small gold "
          "paw-print name tag on her teal collar: engrave the name 'Bentley' clearly and legibly across the large central "
          "pad of the paw print, in small neat letters, correctly spelled B-E-N-T-L-E-Y. Keep the paw-print shape, the small "
          "tag size, the dog, the collar, the lighting and everything else identical. Add nothing except the legible, "
          "correctly-spelled name 'Bentley' inside the paw.")

url = host(SRC); print("input:", url)
INP = {"prompt": PROMPT, "image_input": [url], "aspect_ratio": "16:9", "resolution": "2K", "output_format": "png"}
print("bal before:", kie_client.credits())
done = False
for i in range(4):
    try:
        r = kie_client.run("nano-banana-pro", INP)
        kie_client.download(r["urls"][0], OUT)
        print(f"OK {r.get('credits')}cr {r.get('secs')}s -> {OUT}"); done = True; break
    except Exception as e:
        print(f"  attempt {i+1}: {str(e)[:90]}"); time.sleep(6)
if not done:
    print("FAILED")
print("bal after:", kie_client.credits())
