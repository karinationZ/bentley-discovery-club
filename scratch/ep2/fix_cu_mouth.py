#!/usr/bin/env python3
"""Fix bentley_cu_awe: change ONLY the mouth (open row of human-looking teeth) to a NATURAL dog mouth with the
soft pink tongue lolling out (like the real Bentley) — no human teeth. Edit the approved frame (Nano Banana Pro),
preserve everything else. Output to scratch for QA before promoting. Run: KIE_KEY=... python3 scratch/ep2/fix_cu_mouth.py
"""
import sys, os, time, subprocess
ROOT = "/project"
sys.path.insert(0, ROOT)
from bentley.shared import kie_client
SRC = f"{ROOT}/scratch/ep2/hero_v2/bentley_cu_awe.png"
OUT = f"{ROOT}/scratch/ep2/master/bentley_cu_fixed.png"

def host(p):
    u = subprocess.check_output(["curl","-s","-F","reqtype=fileupload","-F",f"fileToUpload=@{p}",
                                 "https://catbox.moe/user/api.php"]).decode().strip()
    if not u.startswith("http"): raise RuntimeError("catbox fail")
    return u

PROMPT = ("Keep this image of Bentley the red-fawn Boxer puppy EXACTLY the same — same dog, same face, eyes, fur, floppy "
          "ears, teal collar, gold paw tag, background, lighting and rendering style. Change ONLY HER MOUTH: instead of the "
          "open mouth showing a row of teeth, give her a happy NATURAL DOG mouth — open and relaxed with her soft pink TONGUE "
          "lolling out to one side (like a real happy Boxer dog panting), jowls relaxed. NO human teeth, NO upper row of "
          "teeth, NO human grin, NO bared teeth. Keep her soft wide wondering eyes. Change nothing else.")

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
