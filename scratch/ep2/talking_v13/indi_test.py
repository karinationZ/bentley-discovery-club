#!/usr/bin/env python3
"""Indi lip-sync VERIFICATION: one tight Indi face-CU keyframe + Kling-Avatar on her 1:50 line, hard
toothless prompt. QA: does the octopus lip-sync on-model WITHOUT growing teeth? Run: set -a;source .env;set +a"""
import sys, subprocess
from pathlib import Path
ROOT = Path("/project")
sys.path.insert(0, str(ROOT))
from bentley.shared import kie_client
from bentley.shared.hosting import catbox_host

OUT = ROOT / "scratch/ep2/talking_v13/indi_test"; OUT.mkdir(parents=True, exist_ok=True)
INDI = ROOT / "assets/character_design/Indi_LOCKED.png"
SHEET = ROOT / "assets/character_design/Indi_MODEL_SHEET.png"
OPENM = ROOT / "assets/character_design/Indi_openmouth.png"
VO = ROOT / "scratch/ep2/restart_v3/vo/labels/P4_I03.mp3"   # "It tastes like sunshine and wet dog." (1:50)

KEY_PROMPT = (
    "Tight front-facing FACE close-up of Indi the small purple California two-spot octopus, looking at the camera, bright "
    "daylight on her face. Two large round TEAL eyes and two TEAL ring eyespots clearly visible, soft purple skin, eight "
    "soft curled arms, NO nose, NO eyebrows, a small soft TOOTHLESS mouth slightly open as if mid-speech -- absolutely NO "
    "teeth, NO gums, NO human mouth, NO human face. On-model, warm tide-pool background, soft cartoony-Pixar render. No text."
)
AVA_PROMPT = (
    "Indi the small purple octopus gently speaks; her small soft TOOTHLESS mouth opens and closes softly in time with her "
    "words, calm expressive teal eyes with gentle blinks, soft arms drifting. ABSOLUTELY NO teeth, NO gums, NO human mouth, "
    "NO human smile, NO human face. Keep her exact purple colour, teal eyes and two ring spots; do not redraw her."
)
key = OUT / "indi_key.png"
print("bal before:", kie_client.credits(), flush=True)
if not key.exists():
    res = kie_client.run("gpt-image-2-image-to-image", {"prompt": KEY_PROMPT, "input_urls": [catbox_host(str(INDI)), catbox_host(str(SHEET)), catbox_host(str(OPENM))], "aspect_ratio": "16:9"}, timeout=900, poll=8)
    kie_client.download(res["urls"][0], str(key)); print(f"key: {res.get('credits')}cr", flush=True)
r = kie_client.run("kling/ai-avatar-standard", {"image_url": catbox_host(str(key)), "audio_url": catbox_host(str(VO)), "prompt": AVA_PROMPT}, timeout=900, poll=10)
kie_client.download(r["urls"][0], str(OUT / "indi_talk.mp4")); print(f"avatar: {r.get('credits')}cr -> {OUT/'indi_talk.mp4'}", flush=True)
for t in ["0.3", "0.8", "1.3", "1.8", "2.3"]:
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", t, "-i", str(OUT / "indi_talk.mp4"), "-frames:v", "1", str(OUT / f"qa_{t}.png")], check=False)
print("bal after:", kie_client.credits(), flush=True)
