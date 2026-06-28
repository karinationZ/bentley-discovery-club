#!/usr/bin/env python3
"""Refine bentley_cu_awe: (1) settle the EARS to fold softly DOWN against the head (not flying/sticking out);
(2) add more natural BOXER wrinkles (forehead/brow). Keep the tongue-out mouth + everything else. Nano Banana Pro,
edit the approved frame. QA before promoting. Run: KIE_KEY=... python3 scratch/ep2/fix_cu_ears.py
"""
import sys, os, time, subprocess
ROOT = "/project"
sys.path.insert(0, ROOT)
from bentley.shared import kie_client
SRC = f"{ROOT}/scratch/ep2/hero_v2/bentley_cu_awe.png"
OUT = f"{ROOT}/scratch/ep2/master/bentley_cu_ears.png"

def host(p):
    u = subprocess.check_output(["curl","-s","-F","reqtype=fileupload","-F",f"fileToUpload=@{p}",
                                 "https://catbox.moe/user/api.php"]).decode().strip()
    if not u.startswith("http"): raise RuntimeError("catbox fail")
    return u

PROMPT = ("Keep this image of Bentley the red-fawn Boxer puppy EXACTLY the same — same dog, the open mouth with the soft pink "
          "TONGUE lolling out (do NOT change the mouth), same eyes, fur, teal collar, gold paw tag, background, lighting and "
          "rendering style. Make TWO refinements: (1) settle her EARS so they fold softly DOWN against the sides of her head "
          "(relaxed, natural floppy Boxer ears) — NOT sticking out, NOT flying up or out to the sides; (2) add more natural "
          "BOXER facial WRINKLES — gentle folds across her forehead and brow (and a little on the muzzle), like a real Boxer "
          "dog. Keep everything else identical. NO human teeth, NO human grin.")

url = host(SRC)
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
if not done: print("FAILED")
print("bal after:", kie_client.credits())
