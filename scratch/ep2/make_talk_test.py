#!/usr/bin/env python3
"""TALKING test #1 — Indi lip-sync (highest teeth-risk). Keyframe = toothless open-mouth prop, audio = I_hide.
Kling-Avatar (kling/ai-avatar-standard). QA: lip-sync quality + NO teeth. Run: KIE_KEY=... python3 ..."""
import sys, os, time, subprocess
ROOT = "/project"
sys.path.insert(0, ROOT)
from bentley.shared import kie_client
OUT = f"{ROOT}/scratch/ep2/talking"; os.makedirs(OUT, exist_ok=True)

def host(p):
    return subprocess.check_output(["curl","-s","-F","reqtype=fileupload","-F",f"fileToUpload=@{p}",
                                    "https://catbox.moe/user/api.php"]).decode().strip()

img = host(f"{ROOT}/assets/character_design/Indi_openmouth.png")
aud = host(f"{ROOT}/scratch/ep2/vo/I_hide.mp3")
print("img:", img); print("aud:", aud)
PROMPT = ("A shy purple octopus gently speaks; calm, sincere, soft expressive eyes with gentle blinks. Her mouth is only a "
          "small, soft, TOOTHLESS opening -- absolutely NO teeth, NO human smile, NO human-like mouth or lips. Tender, a "
          "little sad. Keep her exact colour, teal eyes and look; do not redraw her.")
OUTV = f"{OUT}/_indi_hide_test.mp4"
print("bal before:", kie_client.credits())
r = None
for i in range(8):
    try:
        r = kie_client.run("kling/ai-avatar-standard", {"image_url": img, "audio_url": aud, "prompt": PROMPT}, timeout=600); break
    except Exception as e:
        print(f"  try {i+1}: {str(e)[:80]}"); time.sleep(12)
if r:
    kie_client.download(r["urls"][0], OUTV); print(f"DONE {r.get('credits')}cr -> {OUTV}")
    for t in ["0.6","1.5","2.5","3.5","4.5"]:
        subprocess.run(["ffmpeg","-y","-loglevel","error","-ss",t,"-i",OUTV,"-frames:v","1",f"{OUT}/_ith_{t}.png"], check=False)
else:
    print("FAILED")
print("bal after:", kie_client.credits())
print("=== INDI TALK TEST DONE ===")
