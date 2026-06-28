#!/usr/bin/env python3
"""BRIDGE-1 — the ONE shot Ep2 must generate: "Indi flees straight into the eel's path."
This is the Act-2 causal connector that makes the danger real (owner notes #3/#9/#10).

Method = the locked v7 pipeline (KIE): gpt-image-2-image-to-image stills -> kling-3.0/video motion,
with Indi + eel element refs. Honors the never-auto-batch rule: STAGE 1 makes candidate stills for a
HUMAN pick; STAGE 2 animates only the chosen still.

Refs: Indi_LOCKED.png + the chosen eel keyframe a2_12_eelstir_v4_chosen.png.

Run (env must have KIE_KEY):
  set -a; source .env; set +a
  python3 scratch/ep2/final_v8/generate_bridge1.py stills          # -> 6 candidates + contact sheet
  python3 scratch/ep2/final_v8/generate_bridge1.py motion --pick 3 # -> 13_eelpath.mp4 from still #3
"""
import argparse, subprocess, sys, time
from pathlib import Path

ROOT = Path("/project")
sys.path.insert(0, str(ROOT))
from bentley.shared import kie_client
from bentley.shared.hosting import catbox_host

OUT = ROOT / "scratch/ep2/final_v8/bridge1"
OUT.mkdir(parents=True, exist_ok=True)
INDI = ROOT / "assets/character_design/Indi_LOCKED.png"
EEL = ROOT / "assets/pilot_shots/ep2/keyframes/a2_12_eelstir_v4_chosen.png"

BASE = (
    "16:9 premium 3D animated kids-show keyframe in a warm tide-pool / shallow-reef world, cinematic but soft for ages 4-8. "
    "INDI is a small soft purple California two-spot octopus: teal eyes, two teal ring spots, eight tentacles, no nose, "
    "no eyebrows, tiny toothless mouth, no teeth, no human face. She is small and vulnerable, darting low and fast across pale "
    "sand in fear, ink wisp trailing. Behind/above her, emerging from a dark rocky crevice, a long sinuous MORAY EEL silhouette "
    "leans out of the shadow, head turned toward the fleeing octopus, jaw just beginning to part — clearly aimed at her. "
    "The eel is a soft menacing shadow shape, NOT gory, NOT cute, no blood, no human face, mouth not graphic. "
    "Both characters readable in ONE frame so the danger is obviously aimed at Indi. Natural underwater light, gentle caustics, "
    "no text, no watermark, no captions."
)
# 6 candidate variations (composition / eel position / distance) for a human pick.
VARIANTS = [
    "Wide establishing: Indi lower-left foreground, eel large in upper-right shadow, big diagonal of motion between them.",
    "Medium: Indi center-low and close, eel emerging directly ahead of her from a black reef gap, dramatic depth.",
    "Low side angle: Indi skimming the sand left-to-right, eel uncoiling from a dark overhang on the right.",
    "Over-the-shoulder behind Indi: we follow her toward the looming dark crevice where the eel's eye glints.",
    "High three-quarter: Indi small against pale sand, the eel's long shadow sweeping toward her from deep reef shade.",
    "Tense near-miss framing: Indi mid-dart, the eel's parting jaw filling the upper third in soft shadow.",
]
MOTION = (
    "The small purple octopus Indi darts forward low and fast in fear, ink wisp trailing; the moray eel's long shadow surges "
    "out of the dark crevice toward her, head tracking her, jaw parting slightly. Water swirls; a beat of real danger. "
    "Indi stays small, toothless, cephalopod, teal eyes and teal ring spots. The eel is a soft menacing silhouette — no gore, "
    "no graphic mouth, no human face. Slight push-in, stable framing. No text, no watermark, no captions."
)


def refs():
    return {"indi": catbox_host(str(INDI)), "eel": catbox_host(str(EEL))}


def make_stills(n=6):
    r = refs()
    print("credits before:", kie_client.credits(), flush=True)
    made = []
    for i in range(n):
        out = OUT / f"still_{i}.png"
        if out.exists() and out.stat().st_size > 100_000:
            made.append(out); print(f"still {i}: exists"); continue
        payload = {"prompt": BASE + " " + VARIANTS[i % len(VARIANTS)],
                   "input_urls": [r["indi"], r["eel"]], "aspect_ratio": "16:9"}
        for attempt in range(1, 4):
            try:
                res = kie_client.run("gpt-image-2-image-to-image", payload, timeout=900, poll=8)
                kie_client.download(res["urls"][0], str(out))
                made.append(out); print(f"still {i}: {res.get('credits')} cr ({res.get('secs')}s)", flush=True)
                break
            except Exception as e:
                print(f"still {i} attempt {attempt} failed: {str(e)[:200]}", flush=True); time.sleep(8)
    # contact sheet for the pick
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
        sys.exit(f"no still_{pick}.png — run `stills` and pick first")
    out = OUT / "13_eelpath.mp4"
    still_url = catbox_host(str(still))
    elements = [{
        "name": "indi",
        "description": "Indi locked small soft purple California two-spot octopus, teal eyes, two teal ring spots, no nose, no eyebrows, tiny toothless mouth",
        "element_input_urls": [catbox_host(str(INDI)), catbox_host(str(INDI))],
    }]
    payload = {"prompt": MOTION, "image_urls": [still_url], "sound": False, "duration": "5",
               "aspect_ratio": "16:9", "mode": "std", "multi_shots": False, "kling_elements": elements}
    print("credits before:", kie_client.credits(), flush=True)
    for attempt in range(1, 3):
        try:
            res = kie_client.run("kling-3.0/video", payload, timeout=1200, poll=10)
            kie_client.download(res["urls"][0], str(out))
            print(f"motion: {res.get('credits')} cr ({res.get('secs')}s) -> {out}", flush=True)
            for t in ("0.5", "2.5", "4.5"):
                subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", t, "-i", str(out),
                                "-frames:v", "1", str(OUT / f"qa_{t}.png")], check=False)
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
    if a.stage == "stills":
        make_stills(a.n)
    else:
        if a.pick is None:
            sys.exit("motion needs --pick N")
        make_motion(a.pick)
