#!/usr/bin/env python3
"""TALKING test #2 — Indi via WAN 2.2 Speech-to-Video Turbo (different model family + negative_prompt).
Same keyframe (toothless prop) + audio (I_hide) as the Kling-Avatar test, for a fair compare. QA: lip-sync + NO teeth.
Run: KIE_KEY=... python3 scratch/ep2/make_wan_test.py"""
import sys, os, time, subprocess
ROOT = "/project"
sys.path.insert(0, ROOT)
from bentley.shared import kie_client
OUT = f"{ROOT}/scratch/ep2/talking"; os.makedirs(OUT, exist_ok=True)

# reuse the URLs hosted in the Kling test (catbox is permanent)
img = "https://files.catbox.moe/6xzwy3.png"   # Indi_openmouth.png
aud = "https://files.catbox.moe/40jtqd.mp3"   # I_hide.mp3

PROMPT = ("Pixar-style 3D California two-spot octopus character speaking softly. Non-human cephalopod face. Smooth dark "
          "toothless beak-like mouth opening. No lips, no gums, no white teeth, no human smile. Express speech mostly with "
          "the eyes, head motion, arms, and subtle mouth movement. Keep her exact teal eyes, iridescent purple skin and two "
          "teal ocelli; do not redraw her.")
NEG = "human teeth, teeth, flat teeth, white teeth, gums, human smile, human lips, lips, dentures, human mouth, human face, grin"
INP = {"prompt": PROMPT, "image_url": img, "audio_url": aud, "negative_prompt": NEG,
       "resolution": "580p", "num_frames": 84, "frames_per_second": 16,
       "num_inference_steps": 27, "guidance_scale": 3.5}
OUTV = f"{OUT}/_indi_wan_test.mp4"

print("bal before:", kie_client.credits())
r = None
for i in range(8):
    try:
        r = kie_client.run("wan/2-2-a14b-speech-to-video-turbo", INP, timeout=600); break
    except Exception as e:
        print(f"  try {i+1}: {str(e)[:90]}"); time.sleep(12)
if r:
    kie_client.download(r["urls"][0], OUTV); print(f"DONE {r.get('credits')}cr -> {OUTV}")
    for t in ["0.6","1.5","2.5","3.5","4.5"]:
        subprocess.run(["ffmpeg","-y","-loglevel","error","-ss",t,"-i",OUTV,"-frames:v","1",f"{OUT}/_iwan_{t}.png"], check=False)
else:
    print("FAILED")
print("bal after:", kie_client.credits())
print("=== INDI WAN TEST DONE ===")
