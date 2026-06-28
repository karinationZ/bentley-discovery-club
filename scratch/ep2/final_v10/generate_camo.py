#!/usr/bin/env python3
"""BRIDGE-CAMO — the ONE new render for EP2 v2: a real camouflage CHANGE (grey->gold, smooth->spiky)
that resolves into Indi and melts back. Makes the episode's #1 fact visible instead of narrated.

Locked pipeline (KIE): gpt-image-2-image-to-image stills -> kling-3.0/video motion, with Indi refs.
Honors never-auto-batch: STAGE 1 makes candidate stills for a HUMAN pick; STAGE 2 animates the chosen one.

Run (env needs KIE_KEY):
  set -a; source .env; set +a
  python3 scratch/ep2/final_v10/generate_camo.py stills           # 6 candidates + contact sheet
  python3 scratch/ep2/final_v10/generate_camo.py motion --pick 2  # -> 07_camo.mp4 from still #2
"""
import argparse, subprocess, sys, time
from pathlib import Path

ROOT = Path("/project")
sys.path.insert(0, str(ROOT))
from bentley.shared import kie_client
from bentley.shared.hosting import catbox_host

OUT = ROOT / "scratch/ep2/final_v10/camo"
OUT.mkdir(parents=True, exist_ok=True)
INDI = ROOT / "assets/character_design/Indi_LOCKED.png"
SHEET = ROOT / "assets/character_design/Indi_MODEL_SHEET.png"
ENV_SRC = ROOT / "assets/pilot_shots/ep2/motion/a1_08_camo.mp4"   # tide-pool rock palette


def env_ref():
    p = OUT / "_env.png"
    if not p.exists():
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", "1.0", "-i", str(ENV_SRC),
                        "-frames:v", "1", str(p)], check=True)
    return p


BASE = (
    "16:9 premium 3D animated kids-show keyframe, warm tide-pool world, bright and magical -- WONDER, not peril. "
    "A patch of speckled wet tide-pool rock is CAUGHT MID-CAMOUFLAGE: part of it is still grey, bumpy, rocky, and part "
    "has shifted into the smooth warm-purple skin of INDI, a small California two-spot octopus -- teal eyes, two teal "
    "ring eyespots, eight tentacles, no nose, no eyebrows, tiny toothless mouth, no teeth, no human face. One teal eyespot "
    "catches the light as she resolves out of the stone. The skin shows a chromatophore colour-shift (grey -> gold -> "
    "warm purple) and raised papillae texture (smooth -> bumpy -> spiky). On-model Indi. Natural tide-pool light, gentle "
    "caustics, no text, no watermark, no captions."
)
VARIANTS = [
    "Mostly rock, just beginning: only one tentacle and one eyespot have emerged from the speckled stone.",
    "Half and half: a clean diagonal where grey bumpy rock becomes smooth purple octopus.",
    "Mostly resolved: Indi nearly whole, a last patch of her still textured like the rock behind her.",
    "Close macro on the skin itself: the colour sweep and the rising papillae bumps fill the frame, eyespot at the edge.",
    "Indi resolved and holding, perched where the rock was, one eyespot bright, faint rocky texture still ghosting on her arms.",
    "Wide: the speckled rock shelf with Indi blooming out of its center in warm colour against the grey.",
]
MOTION = (
    "Indi's skin morphs continuously -- colour sweeping grey to gold to warm purple, and texture rising from smooth to "
    "bumpy to spiky -- as she RESOLVES out of the speckled rock, holds for a beat with one teal eyespot bright, then "
    "melts back down into the stone and is gone. A living camouflage morph, not a hard dissolve. Locked camera, let the "
    "skin do the moving. On-model Indi: teal eyes and two teal ring eyespots, toothless, no human face. Bright and "
    "magical. No text, no watermark, no captions."
)


def refs():
    return {"indi": catbox_host(str(INDI)), "sheet": catbox_host(str(SHEET)), "env": catbox_host(str(env_ref()))}


def make_stills(n=6):
    r = refs()
    print("credits before:", kie_client.credits(), flush=True)
    made = []
    for i in range(n):
        out = OUT / f"still_{i}.png"
        if out.exists() and out.stat().st_size > 100_000:
            made.append(out); print(f"still {i}: exists"); continue
        payload = {"prompt": BASE + " " + VARIANTS[i % len(VARIANTS)],
                   "input_urls": [r["indi"], r["sheet"], r["env"]], "aspect_ratio": "16:9"}
        for attempt in range(1, 4):
            try:
                res = kie_client.run("gpt-image-2-image-to-image", payload, timeout=900, poll=8)
                kie_client.download(res["urls"][0], str(out))
                made.append(out); print(f"still {i}: {res.get('credits')} cr ({res.get('secs')}s)", flush=True)
                break
            except Exception as e:
                print(f"still {i} attempt {attempt} failed: {str(e)[:200]}", flush=True); time.sleep(8)
    if made:
        tmp = OUT / "_sheet_src"; tmp.mkdir(exist_ok=True)
        for j, p in enumerate(made):
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(p), "-vf",
                            "scale=480:270:force_original_aspect_ratio=decrease,pad=480:270:(ow-iw)/2:(oh-ih)/2:color=0x202020",
                            str(tmp / f"s{j:02d}.png")], check=False)
        cols = min(3, len(made)); rows = (len(made) + cols - 1) // cols
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "1", "-i", str(tmp / "s%02d.png"),
                        "-vf", f"tile={cols}x{rows}", str(OUT / "candidates.png")], check=False)
        print(f"\nPICK SHEET -> {OUT/'candidates.png'}  (indices left->right, top->bottom)", flush=True)
    print("credits after:", kie_client.credits(), flush=True)


def make_motion(pick):
    still = OUT / f"still_{pick}.png"
    if not still.exists():
        sys.exit(f"no still_{pick}.png -- run `stills` and pick first")
    out = OUT / "07_camo.mp4"
    elements = [{
        "name": "indi",
        "description": "Indi locked small soft purple California two-spot octopus, teal eyes, two teal ring eyespots, no nose, no eyebrows, tiny toothless mouth",
        "element_input_urls": [catbox_host(str(INDI)), catbox_host(str(SHEET))],
    }]
    payload = {"prompt": MOTION, "image_urls": [catbox_host(str(still))], "sound": False, "duration": "5",
               "aspect_ratio": "16:9", "mode": "std", "multi_shots": False, "kling_elements": elements}
    print("credits before:", kie_client.credits(), flush=True)
    for attempt in range(1, 3):
        try:
            res = kie_client.run("kling-3.0/video", payload, timeout=1200, poll=10)
            kie_client.download(res["urls"][0], str(out))
            print(f"motion: {res.get('credits')} cr ({res.get('secs')}s) -> {out}", flush=True)
            for t in ("0.5", "2.5", "4.5"):
                subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", t, "-i", str(out), "-frames:v", "1", str(OUT / f"qa_{t}.png")], check=False)
            break
        except Exception as e:
            print(f"motion attempt {attempt} failed: {str(e)[:220]}", flush=True); time.sleep(10)
    print("credits after:", kie_client.credits(), flush=True)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("stage", choices=["stills", "motion"])
    ap.add_argument("--pick", type=int, default=None)
    ap.add_argument("-n", type=int, default=6)
    a = ap.parse_args()
    make_stills(a.n) if a.stage == "stills" else (make_motion(a.pick) if a.pick is not None else sys.exit("motion needs --pick N"))
