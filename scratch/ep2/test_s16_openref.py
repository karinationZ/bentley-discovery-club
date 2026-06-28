#!/usr/bin/env python3
"""TEST: re-render s16 with the open-mouth PROPS as reference images, to see if Kling i2v uses them to avoid teeth.
image_urls = [scene keyframe, Indi_openmouth, Bentley_openmouth]. Run: KIE_KEY=... python3 scratch/ep2/test_s16_openref.py
"""
import sys, os, time, subprocess
ROOT = "/project"
sys.path.insert(0, ROOT)
from bentley.shared import kie_client
OUT = f"{ROOT}/scratch/ep2/motion/_s16_openref_test.mp4"
urls = open(f"{ROOT}/scratch/ep2/_openmouth_urls.txt").read().split()
INDI_OPEN, BENT_OPEN = urls[0], urls[1]

def host(p):
    return subprocess.check_output(["curl","-s","-F","reqtype=fileupload","-F",f"fileToUpload=@{p}",
                                    "https://catbox.moe/user/api.php"]).decode().strip()

s16kf = host(f"{ROOT}/scratch/ep2/hero_v2/s16_exchange.png")
print("s16 keyframe:", s16kf)

PROMPT = ("Animate the FIRST image as the scene: gentle tender motion — Indi the octopus gently sways and slowly raises one "
          "arm, soft water ripples, slow blinks; Bentley breathes softly. Keep the EXACT scene, characters, colours, "
          "proportions and 3D rendering style of the FIRST image. CRITICAL mouths: if any mouth opens it must match the "
          "REFERENCE props — the octopus a soft TOOTHLESS open mouth (image 2), the dog a natural dog mouth with tongue and "
          "NO human teeth (image 3). NO human teeth and NO human smile on either creature; the octopus has NO teeth at all. "
          "Locked camera, minimal, smooth, slow.")

print("bal before:", kie_client.credits())
r = None
for i in range(8):
    try:
        r = kie_client.run("kling-2.6/image-to-video",
                           {"prompt": PROMPT, "image_urls": [s16kf, INDI_OPEN, BENT_OPEN], "sound": False, "duration": "5"}, timeout=600)
        break
    except Exception as e:
        print(f"  try {i+1}: {str(e)[:80]}"); time.sleep(12)
if r:
    kie_client.download(r["urls"][0], OUT); print(f"DONE {r.get('credits')}cr -> {OUT}")
    for t in ["0.5","1.5","2.5","3.5","4.5"]:
        subprocess.run(["ffmpeg","-y","-loglevel","error","-ss",t,"-i",OUT,"-frames:v","1",
                        f"{ROOT}/scratch/ep2/motion/_oref_{t}.png"], check=False)
else:
    print("FAILED")
print("bal after:", kie_client.credits())
print("=== S16 OPENREF TEST DONE ===")
