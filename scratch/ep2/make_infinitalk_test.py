#!/usr/bin/env python3
"""TALKING test #3 — Indi via Infinitalk (different model family). Retry on transient 'internal error'.
Run: KIE_KEY=... python3 scratch/ep2/make_infinitalk_test.py"""
import sys, os, time, subprocess
ROOT = "/project"
sys.path.insert(0, ROOT)
from bentley.shared import kie_client
OUT = f"{ROOT}/scratch/ep2/talking"; os.makedirs(OUT, exist_ok=True)
img = "https://files.catbox.moe/6xzwy3.png"   # Indi_openmouth.png
aud = "https://files.catbox.moe/40jtqd.mp3"   # I_hide.mp3
PROMPT = ("Pixar-style 3D California two-spot octopus speaking softly. Non-human cephalopod face, smooth dark toothless "
          "mouth opening, no lips, no gums, no teeth, no human smile. Express with eyes, head and arms. Keep her teal eyes, "
          "purple skin and teal ocelli; do not redraw her.")
INP = {"prompt": PROMPT, "image_url": img, "audio_url": aud, "resolution": "480p"}
OUTV = f"{OUT}/_indi_infinitalk_test.mp4"

print("bal before:", kie_client.credits())
r = None
for attempt in range(5):
    try:
        r = kie_client.run("infinitalk/from-audio", INP, timeout=600); break
    except Exception as e:
        print(f"  attempt {attempt+1}: {str(e)[:90]}"); time.sleep(15)
if r:
    kie_client.download(r["urls"][0], OUTV); print(f"DONE {r.get('credits')}cr -> {OUTV}")
    res = subprocess.check_output(["ffprobe","-v","error","-select_streams","v:0","-show_entries",
        "stream=width,height","-of","csv=p=0:s=x",OUTV]).decode().strip(); print("resolution:", res)
    for t in ["0.6","1.5","2.5","3.5","4.5"]:
        subprocess.run(["ffmpeg","-y","-loglevel","error","-ss",t,"-i",OUTV,"-frames:v","1",f"{OUT}/_iinf_{t}.png"], check=False)
        subprocess.run(["ffmpeg","-y","-loglevel","error","-ss",t,"-i",OUTV,"-frames:v","1","-vf",
                        "crop=iw*0.34:ih*0.30:iw*0.20:ih*0.40,scale=900:-1:flags=lanczos",f"{OUT}/_iinfz_{t}.png"], check=False)
    print("frames + zooms ready")
else:
    print("FAILED ALL RETRIES")
print("bal after:", kie_client.credits())
print("=== INFINITALK TEST DONE ===")
