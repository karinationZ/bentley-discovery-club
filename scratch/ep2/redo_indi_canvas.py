#!/usr/bin/env python3
"""Head-still i2v CANVAS for Indi's talking CU: eyes blink + arm/water move, head LOCKED (so the mouth overlay aligns),
mouth stays closed/still (it gets overwritten by the toothless atlas). Run: KIE_KEY=... python3 scratch/ep2/redo_indi_canvas.py"""
import sys, os, time, subprocess
ROOT = "/project"
sys.path.insert(0, ROOT)
from bentley.shared import kie_client
OUT = f"{ROOT}/scratch/ep2/talking/_indi_canvas.mp4"

def host(p):
    return subprocess.check_output(["curl","-s","-F","reqtype=fileupload","-F",f"fileToUpload=@{p}",
                                    "https://catbox.moe/user/api.php"]).decode().strip()

url = host(f"{ROOT}/scratch/ep2/atlas/indi_closed.png")
PROMPT = ("Indi the octopus stays in EXACTLY the same place — her head and body do NOT move, drift, or change scale; locked "
          "in position. ONLY: her large eyes blink softly a couple of times and glance gently, one arm slowly curls and "
          "settles, and the shallow water ripples with soft moving light reflections. Her mouth stays CLOSED and still. "
          "Locked, static camera, slow and minimal. Keep her exact colour, teal eyes, ocelli, the rock and background "
          "identical and on-model.")
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
print("=== INDI CANVAS DONE ===")
