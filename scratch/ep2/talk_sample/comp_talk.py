#!/usr/bin/env python3
"""Talking-Bentley model comparison: SAME keyframe + SAME talking prompt, rendered two ways.
  kling   -> kie kling-3.0/video (i2v, locked element)
  seedance-> kie bytedance/seedance-2-mini (i2v, 720P)
Neither does audio lip-sync; both get a mouth-movement prompt, VO muxed over for context.
Run: set -a;source .env;set +a; python3 comp_talk.py <kling|seedance>
"""
import sys, subprocess, time
from pathlib import Path
ROOT = Path("/project")
sys.path.insert(0, str(ROOT))
from bentley.shared import kie_client
from bentley.shared.hosting import catbox_host

OUT = ROOT / "scratch/ep2/talk_sample"; OUT.mkdir(parents=True, exist_ok=True)
KEY = ROOT / "scratch/ep2/hero/H4_stop/still_1.png"
B_MASTER = ROOT / "assets/character_design/Bentley_MASTER_pixar.png"
B_TURN = ROOT / "assets/character_design/Bentley_MODEL_SHEET_turnaround.png"
VO = ROOT / "scratch/ep2/restart_v3/vo/shots/p04_s04_stop.mp3"

PROMPT = (
    "Bentley the red-fawn Boxer puppy talks: her mouth opens and closes naturally as she speaks, small realistic "
    "puppy-mouth movements, a little tongue, only a hint of tiny puppy teeth -- NEVER a wide human grin, NEVER bulging "
    "cartoon eyes, NEVER a caricature. Keep her EXACT on-model proportions and look from the reference: natural Boxer-"
    "puppy head, black face mask, grey chin, normal brown eyes (not enlarged), floppy folded-down ears, teal collar, "
    "gold paw-print tag, solid red-fawn paws, short docked tail stub. Bright and curious: eyes open, ears perked, gentle "
    "head tilt side to side, alive and engaged. Warm tide-pool light. Continuous non-looping motion, no freeze. Do not "
    "redraw or stylize her; stay cartoony-Pixar and strictly ON-MODEL."
)


def qc(outv, tag):
    for t in ["0.3", "0.8", "1.3", "1.8", "2.3", "2.8"]:
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", t, "-i", str(outv), "-frames:v", "1", str(OUT / f"qa_{tag}_{t}.png")], check=False)


def run(which):
    img = catbox_host(str(KEY)); aud = catbox_host(str(VO))
    print(f"[{which}] img:", img, flush=True)
    print("bal before:", kie_client.credits(), flush=True)
    if which == "kling":
        elements = [{"name": "bentley", "description": "Bentley locked red-fawn Boxer puppy, black mask, grey chin, floppy folded ears, normal brown eyes not enlarged, teal collar, gold paw tag, red-fawn paws no socks, docked tail stub, small puppy mouth no human grin", "element_input_urls": [catbox_host(str(B_MASTER)), catbox_host(str(B_TURN))]}]
        payload = {"prompt": PROMPT, "image_urls": [img], "sound": False, "duration": "5", "aspect_ratio": "16:9", "mode": "std", "multi_shots": False, "kling_elements": elements}
        model = "kling-3.0/video"; outv = OUT / "comp_kling.mp4"
    elif which == "seedance":
        payload = {"prompt": PROMPT, "first_frame_url": img, "generate_audio": False, "resolution": "720p", "duration": 5, "aspect_ratio": "16:9"}
        model = "bytedance/seedance-2-mini"; outv = OUT / "comp_seedance.mp4"
    else:  # seedance_audio: audio-driven lip-sync to our VO, Bentley refs (no first_frame, can't mix)
        payload = {"prompt": PROMPT, "reference_image_urls": [img, catbox_host(str(B_MASTER)), catbox_host(str(B_TURN))], "reference_audio_urls": [aud], "generate_audio": False, "resolution": "720p", "aspect_ratio": "16:9"}
        model = "bytedance/seedance-2-mini"; outv = OUT / "comp_seedance_audio.mp4"
    r = None
    for i in range(5):
        try:
            r = kie_client.run(model, payload, timeout=1200, poll=10); break
        except Exception as e:
            print(f"  try {i+1}: {str(e)[:160]}", flush=True); time.sleep(12)
    if r:
        kie_client.download(r["urls"][0], str(outv)); print(f"DONE {which} {r.get('credits')}cr -> {outv}", flush=True)
        # mux VO for context
        muxed = OUT / f"comp_{which}_vo.mp4"
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(outv), "-i", str(VO), "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-shortest", str(muxed)], check=False)
        qc(outv, which)
    else:
        print(f"FAILED {which}", flush=True)
    print("bal after:", kie_client.credits(), flush=True)


if __name__ == "__main__":
    run(sys.argv[1] if len(sys.argv) > 1 else "kling")
