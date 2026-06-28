#!/usr/bin/env python3
"""Prove the EP1 talking method on an EP2 line: tight bright front-facing FACE-CU keyframe + Kling-Avatar.
Keyframe = the proven Ep1 N6_kie_key_bright2.png; VO = Ep2 "Stop. Look. Listen." Run: set -a;source .env;set +a; python3 ...
"""
import sys, subprocess
from pathlib import Path
ROOT = Path("/project")
sys.path.insert(0, str(ROOT))
from bentley.shared import kie_client
from bentley.shared.hosting import catbox_host

OUT = ROOT / "scratch/ep2/talk_sample/ep1method"; OUT.mkdir(parents=True, exist_ok=True)
KEY = ROOT / "assets/approved/bentley/N6_kie_key_bright2.png"   # proven Ep1 tight bright face CU
VO = ROOT / "scratch/ep2/restart_v3/vo/shots/p04_s04_stop.mp3"  # Ep2 "Stop. Look. Listen."
PROMPT = (
    "Bentley the red-fawn Boxer puppy speaks straight to camera with a gentle affectionate head-tilt; soft natural "
    "small-dog mouth movements in time with her words, bright soulful eyes, ears floppy down, no human teeth. Bright "
    "daylight on her face. Keep her exact look, do not redraw her."
)
OUTV = OUT / "ep1method_stop.mp4"
img = catbox_host(str(KEY)); aud = catbox_host(str(VO))
print("img:", img, "\naud:", aud)
print("bal before:", kie_client.credits(), flush=True)
r = kie_client.run("kling/ai-avatar-standard", {"image_url": img, "audio_url": aud, "prompt": PROMPT}, timeout=900, poll=10)
kie_client.download(r["urls"][0], str(OUTV)); print(f"DONE {r.get('credits')}cr -> {OUTV}", flush=True)
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(OUTV), "-i", str(VO), "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-shortest", str(OUT / "ep1method_stop_vo.mp4")], check=False)
for t in ["0.3", "0.7", "1.1", "1.5", "1.9", "2.3", "2.7", "3.1"]:
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", t, "-i", str(OUTV), "-frames:v", "1", str(OUT / f"qa_{t}.png")], check=False)
print("bal after:", kie_client.credits(), flush=True)
