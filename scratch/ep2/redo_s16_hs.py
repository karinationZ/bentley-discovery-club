#!/usr/bin/env python3
"""s16 head-still re-render: Indi's head/face/mouth held still (only an arm + water move), so composite-lock aligns.
Run: KIE_KEY=... python3 scratch/ep2/redo_s16_hs.py
"""
import sys, os, time, subprocess
ROOT = "/project"
sys.path.insert(0, ROOT)
from bentley.shared import kie_client
OUT = f"{ROOT}/scratch/ep2/motion/_s16_hs.mp4"

def host(p):
    return subprocess.check_output(["curl","-s","-F","reqtype=fileupload","-F",f"fileToUpload=@{p}",
                                    "https://catbox.moe/user/api.php"]).decode().strip()

url = host(f"{ROOT}/scratch/ep2/hero_v2/s16_exchange.png")
PROMPT = ("Animate this scene with VERY MINIMAL motion. Bentley the dog stays still — only soft breathing, mouth closed, ears "
          "down (no mouth movement, no teeth). The octopus Indi keeps her HEAD and FACE COMPLETELY STILL in place and her "
          "mouth CLOSED — do NOT move, open or reshape her mouth, no teeth, no smile. ONLY her one arm slowly rises a little "
          "and the water gently ripples with soft sparkles. Locked camera, slow, minimal. Keep the EXACT same characters, "
          "colours, faces, mouths, proportions and 3D rendering style as the image.")
print("bal before:", kie_client.credits())
r = None
for i in range(8):
    try:
        r = kie_client.run("kling-2.6/image-to-video",
                           {"prompt": PROMPT, "image_urls": [url], "sound": False, "duration": "5"}, timeout=600); break
    except Exception as e:
        print(f"  try {i+1}: {str(e)[:70]}"); time.sleep(12)
if r:
    kie_client.download(r["urls"][0], OUT); print(f"DONE {r.get('credits')}cr -> {OUT}")
else:
    print("FAILED")
print("bal after:", kie_client.credits())
