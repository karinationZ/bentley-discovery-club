#!/usr/bin/env python3
"""EP2 H1 — the real multi-color camouflage change (fixes the prior purple/grey + tooth-sucker + teardrop).
KIE: gpt-image-2 stills -> pick -> kling-3.0/video motion. Never auto-batch (human picks the still).
Run: set -a;source .env;set +a
  python3 scratch/ep2/h1_camo/generate_camo_h1.py stills
  python3 scratch/ep2/h1_camo/generate_camo_h1.py motion --pick N
"""
import argparse, subprocess, sys, time
from pathlib import Path
ROOT = Path("/project")
sys.path.insert(0, str(ROOT))
from bentley.shared import kie_client
from bentley.shared.hosting import catbox_host

OUT = ROOT / "scratch/ep2/h1_camo"; OUT.mkdir(parents=True, exist_ok=True)
INDI = ROOT / "assets/character_design/Indi_LOCKED.png"
SHEET = ROOT / "assets/character_design/Indi_MODEL_SHEET.png"
ENV_SRC = ROOT / "assets/pilot_shots/ep2/motion/a1_08_camo.mp4"

BASE = (
    "16:9 premium 3D animated kids-show keyframe, warm tide-pool world, bright and magical -- wonder, not peril. "
    "A patch of speckled tide-pool rock is mid-CAMOUFLAGE CHANGE: its skin sweeping through MANY colors at once -- "
    "patches of GREY stone, warm GOLD, mossy GREEN, and INDI's signature PURPLE -- while the texture shifts from smooth "
    "to bumpy and spiky (octopus papillae rising). INDI, the small California two-spot octopus, is half-resolved out of "
    "the rock: teal eyes, two teal ring eyespots, no nose, no eyebrows, a TINY closed TOOTHLESS mouth, soft arms gently "
    "curled and tucked. NO rows of suckers facing the camera, NO teeth, nothing tooth-like, NO tear, no human face, no "
    "sad look. The multi-color skin and the rising bumps are the hero of the frame -- a living chromatophore display. "
    "On-model Indi. Natural tide-pool light, gentle caustics. No text, no watermark, no captions."
)
VARIANTS = [
    "Half rock, half octopus: a clear diagonal where grey/gold/green stone becomes smooth purple Indi, colors blooming across the seam.",
    "Mostly resolved Indi, her body still rippling with leftover gold/green/grey camouflage patches over the purple.",
    "Macro on the skin: the gold-green-purple colour sweep and the rising papillae bumps fill the frame, one teal eyespot at the edge.",
    "Indi blooming out of a rock shelf, a rainbow of grey/gold/green/purple washing head-to-arm-tips, arms curled low.",
    "Wide: speckled rock with Indi emerging from the center in a burst of shifting colour against the duller stone around her.",
    "Indi resolved and holding, one teal eyespot bright, faint gold and green camouflage still ghosting across her purple skin.",
]
MOTION = (
    "Indi runs a continuous camouflage display: colour sweeping across her whole body through grey, gold, green and purple "
    "while the texture rises smooth->bumpy->spiky and settles -- as she resolves out of the speckled rock, holds a beat with "
    "the colours rippling, then melts back into the stone and is gone. A living, magical chromatophore morph, not a hard "
    "dissolve. On-model Indi: teal eyes, two teal ring eyespots, tiny closed toothless mouth, soft curled arms, NO rows of "
    "teeth-like suckers facing camera, no human face, no tear. Bright and wondrous. Locked camera. No text, no watermark."
)


def env_ref():
    p = OUT / "_env.png"
    if not p.exists():
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", "1.0", "-i", str(ENV_SRC), "-frames:v", "1", str(p)], check=True)
    return p


def make_stills(n=6):
    r = {"indi": catbox_host(str(INDI)), "sheet": catbox_host(str(SHEET)), "env": catbox_host(str(env_ref()))}
    print("credits before:", kie_client.credits(), flush=True)
    made = []
    for i in range(n):
        out = OUT / f"still_{i}.png"
        if out.exists() and out.stat().st_size > 100_000:
            made.append(out); print(f"still {i}: exists"); continue
        payload = {"prompt": BASE + " " + VARIANTS[i % len(VARIANTS)], "input_urls": [r["indi"], r["sheet"], r["env"]], "aspect_ratio": "16:9"}
        for attempt in range(1, 4):
            try:
                res = kie_client.run("gpt-image-2-image-to-image", payload, timeout=900, poll=8)
                kie_client.download(res["urls"][0], str(out)); made.append(out)
                print(f"still {i}: {res.get('credits')} cr ({res.get('secs')}s)", flush=True); break
            except Exception as e:
                print(f"still {i} attempt {attempt} failed: {str(e)[:200]}", flush=True); time.sleep(8)
    if made:
        tmp = OUT / "_sheet_src"; tmp.mkdir(exist_ok=True)
        for j, p in enumerate(made):
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(p), "-vf", "scale=480:270:force_original_aspect_ratio=decrease,pad=480:270:(ow-iw)/2:(oh-ih)/2:color=0x202020", str(tmp / f"s{j:02d}.png")], check=False)
        cols = min(3, len(made)); rows = (len(made) + cols - 1) // cols
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "1", "-i", str(tmp / "s%02d.png"), "-vf", f"tile={cols}x{rows}", str(OUT / "candidates.png")], check=False)
        print(f"\nPICK SHEET -> {OUT/'candidates.png'}", flush=True)
    print("credits after:", kie_client.credits(), flush=True)


def make_motion(pick):
    still = OUT / f"still_{pick}.png"
    if not still.exists():
        sys.exit(f"no still_{pick}.png")
    out = OUT / "h1_camo.mp4"
    elements = [{"name": "indi", "description": "Indi locked small purple California two-spot octopus, teal eyes, two teal ring eyespots, no nose, no eyebrows, tiny toothless mouth", "element_input_urls": [catbox_host(str(INDI)), catbox_host(str(SHEET))]}]
    payload = {"prompt": MOTION, "image_urls": [catbox_host(str(still))], "sound": False, "duration": "5", "aspect_ratio": "16:9", "mode": "std", "multi_shots": False, "kling_elements": elements}
    print("credits before:", kie_client.credits(), flush=True)
    for attempt in range(1, 3):
        try:
            res = kie_client.run("kling-3.0/video", payload, timeout=1200, poll=10)
            kie_client.download(res["urls"][0], str(out)); print(f"motion: {res.get('credits')} cr -> {out}", flush=True)
            for t in ("0.5", "2.5", "4.5"):
                subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", t, "-i", str(out), "-frames:v", "1", str(OUT / f"qa_{t}.png")], check=False)
            break
        except Exception as e:
            print(f"motion attempt {attempt} failed: {str(e)[:220]}", flush=True); time.sleep(10)
    print("credits after:", kie_client.credits(), flush=True)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("stage", choices=["stills", "motion"]); ap.add_argument("--pick", type=int); ap.add_argument("-n", type=int, default=6)
    a = ap.parse_args()
    make_stills(a.n) if a.stage == "stills" else (make_motion(a.pick) if a.pick is not None else sys.exit("motion needs --pick"))
