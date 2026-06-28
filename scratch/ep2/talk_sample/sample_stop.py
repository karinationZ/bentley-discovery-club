#!/usr/bin/env python3
"""SAMPLE: talking-Bentley lip-sync quality test (Kling-Avatar, kling/ai-avatar-standard).
Line = "Stop. Look. Listen." (catchphrase, LauraZ). Keyframe = Bentley in the cove (H4 still).
Doubles as the 2:05 fix preview: eyes OPEN, head-tilt, cute/curious. Run: set -a;source .env;set +a; python3 ...
"""
import sys, os, subprocess, time
from pathlib import Path
ROOT = Path("/project")
sys.path.insert(0, str(ROOT))
from bentley.shared import kie_client
from bentley.shared.hosting import catbox_host

OUT = ROOT / "scratch/ep2/talk_sample"; OUT.mkdir(parents=True, exist_ok=True)
KEY = ROOT / "scratch/ep2/hero/H4_stop/still_1.png"          # Bentley in the cove, on-model
VO = ROOT / "scratch/ep2/restart_v3/vo/shots/p04_s04_stop.mp3"  # "Stop. Look. Listen." (LauraZ)

PROMPT = (
    "Bentley the red-fawn Boxer puppy speaks the words clearly, her mouth opening and closing in time with the speech "
    "(real lip movement, not a closed mouth). Bright, curious and engaged: eyes WIDE OPEN and shining, ears perked, head "
    "tilting cutely from side to side, alert, happy and a little excited. Small natural puppy-mouth movements -- a little "
    "puppy tongue and a hint of small puppy teeth may show briefly, but NEVER a wide human grin or human smile. Keep her "
    "EXACT look: black face mask, grey chin, brown eyes, floppy folded-down ears, teal collar, gold paw-print tag, solid "
    "red-fawn paws, cartoony-Pixar puppy. Warm tide-pool light. Do not redraw her, keep her on-model."
)
OUTV = OUT / "sample_stop.mp4"

img = catbox_host(str(KEY)); aud = catbox_host(str(VO))
print("img:", img); print("aud:", aud)
print("VO dur:", subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",str(VO)]).decode().strip(), "s")
print("bal before:", kie_client.credits(), flush=True)
r = None
for i in range(6):
    try:
        r = kie_client.run("kling/ai-avatar-standard", {"image_url": img, "audio_url": aud, "prompt": PROMPT}, timeout=900, poll=10); break
    except Exception as e:
        print(f"  try {i+1}: {str(e)[:120]}", flush=True); time.sleep(12)
if r:
    kie_client.download(r["urls"][0], str(OUTV)); print(f"DONE {r.get('credits')}cr -> {OUTV}", flush=True)
    for t in ["0.3","0.8","1.3","1.8","2.3"]:
        subprocess.run(["ffmpeg","-y","-loglevel","error","-ss",t,"-i",str(OUTV),"-frames:v","1",str(OUT/f"qa_{t}.png")], check=False)
else:
    print("FAILED", flush=True)
print("bal after:", kie_client.credits(), flush=True)
