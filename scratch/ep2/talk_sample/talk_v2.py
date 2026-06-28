#!/usr/bin/env python3
"""Talking-Bentley v2 — ai-engineer's fix: open-mouth keyframe + articulating-mouth element + counted-beat
prompt, Kling 3.0 i2v, sound OFF (no audio -> no human-face caricature). Stages:
  key    -> generate 4 on-model open-mouth Bentley keyframes (hand-pick)
  render -> Kling 3.0 talking test from a picked keyframe  (--pick N)
Run: set -a;source .env;set +a; python3 talk_v2.py key   |   python3 talk_v2.py render --pick N
"""
import sys, argparse, subprocess, time
from pathlib import Path
ROOT = Path("/project")
sys.path.insert(0, str(ROOT))
from bentley.shared import kie_client
from bentley.shared.hosting import catbox_host

OUT = ROOT / "scratch/ep2/talk_sample/v2"; OUT.mkdir(parents=True, exist_ok=True)
B_MASTER = ROOT / "assets/character_design/Bentley_MASTER_pixar.png"
B_TURN = ROOT / "assets/character_design/Bentley_MODEL_SHEET_turnaround.png"
VO = ROOT / "scratch/ep2/restart_v3/vo/shots/p04_s04_stop.mp3"

KEY_PROMPT = (
    "Edit this exact Bentley puppy, keeping her 100% on-model and identical in style, color, and proportion. Change ONLY "
    "her pose and expression to mid-speech: she sits upright in the bright tide-pool, EYES OPEN (bright, warm, NORMAL-sized "
    "round brown eyes -- not enlarged), EARS perked slightly forward, and her MOUTH OPEN as if barking out a short word -- "
    "lower jaw dropped, lips parted, soft pink tongue visible inside, a glimpse of tiny lower puppy teeth, like a real puppy "
    "mid-bark. A natural open DOG mouth, NOT a human grin, NOT a human smile, NOT teeth-baring across the face. Keep the black "
    "face mask, grey chin, white chest blaze, teal collar, glowing gold paw-print tag, solid red-fawn paws (no white socks), "
    "short docked tail stub. Keep the warm golden sunset tide-pool background and the soft cartoony-Pixar render. Do not "
    "restyle, do not change her breed or proportions. No text, no watermark."
)
PROMPT = (
    "Bentley the red-fawn Boxer puppy is speaking three words out loud, one at a time, and her jaw clearly articulates each "
    "word. ACTION BEATS, in order: she opens her mouth wide on the first word, closes it, opens her mouth again on the second "
    "word, closes it, then opens wide a third time on the last word and closes. Three distinct big mouth-open-and-close cycles "
    "across the clip, jaw dropping and lips parting each time, lower jaw visibly moving up and down, soft pink tongue flicking "
    "inside, a glimpse of tiny lower puppy teeth -- like a real puppy barking out short words. Keep it lively and continuous, "
    "never a frozen or sealed mouth. IDENTITY LOCK (do not change): her eyes stay OPEN, bright, warm, NORMAL-SIZED round brown "
    "eyes -- never enlarged, never bulging, never cartoon-huge. Natural Boxer-puppy head and muzzle in correct proportion, "
    "black face mask, grey chin, floppy folded-down ears, teal collar, gold paw-print tag, solid red-fawn paws, short docked "
    "tail stub. This is a real dog mouth opening to bark words -- it is NEVER a wide human grin, NEVER a human smile, NEVER a "
    "smug human expression, NEVER a caricature. Expressive and curious through perked ears, a small head tilt, and a body "
    "bounce, with the mouth doing the talking. Warm golden tide-pool light, soft cartoony-Pixar render, strictly ON-MODEL. "
    "Continuous non-looping performance, no repeated gesture, no freeze-frame, no visible restart."
)
ELEMENT_DESC = (
    "Bentley, locked red-fawn Boxer puppy: black face mask, grey chin, floppy folded-down ears, NORMAL-sized round brown eyes "
    "(never enlarged or bulging), teal collar, gold paw-print tag, solid red-fawn paws no socks, short docked tail stub, natural "
    "Boxer muzzle in correct proportion. Mouth is an articulating real-dog mouth that can open and close to speak, showing soft "
    "tongue and only tiny lower puppy teeth; never a human grin, never a human smile, never gums-baring, never a wide flat smile "
    "across the face. Identity is fixed by the eyes, mask, ears, and head proportions, not by a closed mouth."
)


def make_keys(n=4):
    inp = [catbox_host(str(B_MASTER)), catbox_host(str(B_TURN))]
    print("bal before:", kie_client.credits(), flush=True)
    made = []
    for i in range(n):
        out = OUT / f"key_{i}.png"
        if out.exists() and out.stat().st_size > 100_000:
            made.append(out); continue
        for attempt in range(1, 3):
            try:
                res = kie_client.run("gpt-image-2-image-to-image", {"prompt": KEY_PROMPT, "input_urls": inp, "aspect_ratio": "16:9"}, timeout=900, poll=8)
                kie_client.download(res["urls"][0], str(out)); made.append(out); print(f"key {i}: {res.get('credits')}cr", flush=True); break
            except Exception as e:
                print(f"key {i} fail {attempt}: {str(e)[:140]}", flush=True); time.sleep(8)
    if made:
        tmp = OUT / "_s"; tmp.mkdir(exist_ok=True)
        for j, p in enumerate(made):
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(p), "-vf", "scale=440:248:force_original_aspect_ratio=decrease,pad=440:248:(ow-iw)/2:(oh-ih)/2:color=0x202020", str(tmp / f"s{j}.png")], check=False)
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", "1", "-i", str(tmp / "s%d.png"), "-vf", f"tile={len(made)}x1", str(OUT / "key_candidates.png")], check=False)
        print(f"-> {OUT/'key_candidates.png'}", flush=True)
    print("bal after:", kie_client.credits(), flush=True)


def scout(pick):
    """CHEAP scout (Kling 2.6) to validate the open-mouth + counted-beat prompt before any Kling 3.0 final."""
    key = OUT / f"key_{pick}.png"
    if not key.exists():
        sys.exit(f"no {key}")
    refs = [catbox_host(str(key))]  # kling-2.6 i2v accepts ONE image only; the on-model open-mouth keyframe anchors identity
    outv = OUT / "talk_v2_scout.mp4"
    print("[scout kling-2.6] bal before:", kie_client.credits(), flush=True)
    r = None
    for i in range(3):
        try:
            r = kie_client.run("kling-2.6/image-to-video", {"prompt": PROMPT, "image_urls": refs, "sound": False, "duration": "5"}, timeout=900, poll=10); break
        except Exception as e:
            print(f"  try {i+1}: {str(e)[:160]}", flush=True); time.sleep(12)
    if r:
        kie_client.download(r["urls"][0], str(outv)); print(f"DONE scout {r.get('credits')}cr -> {outv}", flush=True)
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(outv), "-i", str(VO), "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-shortest", str(OUT / "talk_v2_scout_vo.mp4")], check=False)
    else:
        print("FAILED", flush=True)
    print("bal after:", kie_client.credits(), flush=True)


def render(pick, mode):
    key = OUT / f"key_{pick}.png"
    if not key.exists():
        sys.exit(f"no {key}")
    img = catbox_host(str(key)); aud = catbox_host(str(VO))
    elements = [{"name": "bentley", "description": ELEMENT_DESC, "element_input_urls": [catbox_host(str(B_MASTER)), catbox_host(str(B_TURN))]}]
    payload = {"prompt": PROMPT, "image_urls": [img], "sound": False, "duration": "5", "aspect_ratio": "16:9", "mode": mode, "multi_shots": False, "kling_elements": elements}
    outv = OUT / f"talk_v2_{mode}.mp4"
    print(f"[render mode={mode}] key_{pick}; bal before:", kie_client.credits(), flush=True)
    r = None
    for i in range(3):
        try:
            r = kie_client.run("kling-3.0/video", payload, timeout=1200, poll=10); break
        except Exception as e:
            print(f"  try {i+1}: {str(e)[:160]}", flush=True); time.sleep(12)
    if r:
        kie_client.download(r["urls"][0], str(outv)); print(f"DONE {r.get('credits')}cr -> {outv}", flush=True)
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(outv), "-i", str(VO), "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-shortest", str(OUT / f"talk_v2_{mode}_vo.mp4")], check=False)
    else:
        print("FAILED", flush=True)
    print("bal after:", kie_client.credits(), flush=True)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("stage", choices=["key", "scout", "render"]); ap.add_argument("--pick", type=int, default=0); ap.add_argument("--mode", default="std")
    a = ap.parse_args()
    if a.stage == "key":
        make_keys()
    elif a.stage == "scout":
        scout(a.pick)
    else:
        render(a.pick, a.mode)
