#!/usr/bin/env python3
"""Indi talking-face keyframe set — tight front-facing toothless face CUs (verified style), a few
expressions, from the locked Indi. Run: set -a;source .env;set +a; python3 indi_keys.py"""
import sys, subprocess, time
from pathlib import Path
ROOT = Path("/project")
sys.path.insert(0, str(ROOT))
from bentley.shared import kie_client
from bentley.shared.hosting import catbox_host

OUT = ROOT / "scratch/ep2/talking_v13/indi_keys"; OUT.mkdir(parents=True, exist_ok=True)
INDI = ROOT / "assets/character_design/Indi_LOCKED.png"
SHEET = ROOT / "assets/character_design/Indi_MODEL_SHEET.png"
OPENM = ROOT / "assets/character_design/Indi_openmouth.png"

COMMON = (
    "Tight front-facing FACE close-up of Indi the small purple California two-spot octopus, looking at the camera, bright "
    "daylight on her face. Two large round TEAL eyes and two TEAL ring eyespots clearly visible, soft purple skin, eight "
    "soft curled arms, NO nose, NO eyebrows, a small soft TOOTHLESS mouth slightly open as if mid-speech -- absolutely NO "
    "teeth, NO gums, NO human mouth, NO human face. On-model, warm tide-pool background, soft cartoony-Pixar render. No text. "
)
EXPR = {
    "playful": "Expression: playful and mischievous, a clever sparkle in her teal eyes, a cheeky little tilt.",
    "proud": "Expression: proud and confident, bright confident teal eyes, chin lifted.",
    "tender": "Expression: warm, gentle and tender, soft sweet teal eyes, a little shy.",
}
inp = [catbox_host(str(INDI)), catbox_host(str(SHEET)), catbox_host(str(OPENM))]
print("bal before:", kie_client.credits(), flush=True)
made = []
for expr, etxt in EXPR.items():
    out = OUT / f"indi_{expr}.png"
    if out.exists():
        made.append((expr, out)); continue
    for attempt in range(1, 3):
        try:
            res = kie_client.run("gpt-image-2-image-to-image", {"prompt": COMMON + etxt, "input_urls": inp, "aspect_ratio": "16:9"}, timeout=900, poll=8)
            kie_client.download(res["urls"][0], str(out)); made.append((expr, out)); print(f"{expr}: {res.get('credits')}cr", flush=True); break
        except Exception as e:
            print(f"{expr} fail {attempt}: {str(e)[:140]}", flush=True); time.sleep(8)
if made:
    tmp = OUT / "_s"; tmp.mkdir(exist_ok=True)
    for j, (e, p) in enumerate(made):
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(p), "-vf", "scale=300:300:force_original_aspect_ratio=decrease,pad=300:300:(ow-iw)/2:(oh-ih)/2:color=0x202020", str(tmp / f"s{j}.png")], check=False)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "1", "-i", str(tmp / "s%d.png"), "-vf", f"tile={len(made)}x1", str(OUT / "indi_candidates.png")], check=False)
    print(f"-> {OUT/'indi_candidates.png'}  ({', '.join(e for e,_ in made)})", flush=True)
print("bal after:", kie_client.credits(), flush=True)
