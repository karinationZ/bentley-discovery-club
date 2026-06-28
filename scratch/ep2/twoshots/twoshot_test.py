#!/usr/bin/env python3
"""Verify the 'speaker-talks, listener-still' two-shot approach: a two-shot keyframe (Bentley mouth-open
talking, Indi calm listening) + Kling 3.0 i2v that animates ONLY the speaker's mouth. Tests whether the
RIGHT character reads as talking, both on-model, both on screen. Run: set -a;source .env;set +a; python3 ..."""
import sys, subprocess, time
from pathlib import Path
ROOT = Path("/project")
sys.path.insert(0, str(ROOT))
from bentley.shared import kie_client
from bentley.shared.hosting import catbox_host

OUT = ROOT / "scratch/ep2/twoshots"; OUT.mkdir(parents=True, exist_ok=True)
B_MASTER = ROOT / "assets/character_design/Bentley_MASTER_pixar.png"
B_TURN = ROOT / "assets/character_design/Bentley_MODEL_SHEET_turnaround.png"
INDI = ROOT / "assets/character_design/Indi_LOCKED.png"
INDI_SHEET = ROOT / "assets/character_design/Indi_MODEL_SHEET.png"

KEY_PROMPT = (
    "16:9 premium 3D animated kids-show TWO-SHOT, warm bright tide-pool, cartoony-Pixar style. BENTLEY the red-fawn Boxer "
    "puppy on the LEFT, leaning toward her friend, her mouth softly open as she happily chats (small natural puppy mouth, a "
    "little tongue, no human grin), bright happy curious eyes, ears perked. INDI the small purple octopus on the RIGHT, LISTENING "
    "quietly, her small mouth CLOSED, calm attentive teal eyes, two teal ring eyespots, soft curled arms. Both characters "
    "clearly on screen together, interacting in one frame. On-model: Bentley black face mask, grey chin, floppy folded "
    "ears, white chest blaze, teal collar, gold paw-print tag, solid red-fawn paws no socks, short docked tail stub; Indi "
    "purple, teal eyes, two ring spots, no nose, no eyebrows, toothless, no human face. Warm cove light. No text, no watermark."
)
MOTION = (
    "Bentley talks animatedly to Indi -- her mouth opens and closes as she speaks, ears bouncing, bright engaged eyes, a "
    "small lean-in. Indi LISTENS quietly and mostly still -- her mouth stays CLOSED, gentle blinks and one soft arm shift "
    "only. Only the SPEAKER (Bentley) moves her mouth. A warm little conversation, both on screen. Keep both on-model: "
    "Bentley docked tail stub, floppy ears, red-fawn paws no socks, teal collar, gold tag, no human grin; Indi purple, teal "
    "eyes, two ring spots, toothless, no human face. Continuous non-looping motion, no freeze. No text, no watermark."
)
inp = [catbox_host(str(B_MASTER)), catbox_host(str(B_TURN)), catbox_host(str(INDI)), catbox_host(str(INDI_SHEET))]
print("bal before:", kie_client.credits(), flush=True)
key = OUT / "test_key.png"
if not key.exists():
    for attempt in range(1, 5):
        try:
            res = kie_client.run("gpt-image-2-image-to-image", {"prompt": KEY_PROMPT, "input_urls": inp, "aspect_ratio": "16:9"}, timeout=900, poll=8)
            kie_client.download(res["urls"][0], str(key)); print(f"key: {res.get('credits')}cr", flush=True); break
        except Exception as e:
            print(f"key attempt {attempt}: {str(e)[:110]}", flush=True); time.sleep(6)
    if not key.exists():
        sys.exit("keyframe failed after retries")
elements = [
    {"name": "bentley", "description": "Bentley locked red-fawn Boxer puppy, black mask, floppy folded ears, red-fawn paws no socks, teal collar, gold paw tag, docked tail stub, small puppy mouth no human grin", "element_input_urls": [catbox_host(str(B_MASTER)), catbox_host(str(B_TURN))]},
    {"name": "indi", "description": "Indi locked small purple two-spot octopus, teal eyes, two teal ring eyespots, no nose, no eyebrows, tiny toothless mouth", "element_input_urls": [catbox_host(str(INDI)), catbox_host(str(INDI_SHEET))]},
]
payload = {"prompt": MOTION, "image_urls": [catbox_host(str(key))], "sound": False, "duration": "5", "aspect_ratio": "16:9", "mode": "std", "multi_shots": False, "kling_elements": elements}
r = None
for i in range(2):
    try:
        r = kie_client.run("kling-3.0/video", payload, timeout=1200, poll=10); break
    except Exception as e:
        print(f"  try {i+1}: {str(e)[:160]}", flush=True); time.sleep(10)
if r:
    kie_client.download(r["urls"][0], str(OUT / "test_twoshot.mp4")); print(f"DONE {r.get('credits')}cr -> {OUT/'test_twoshot.mp4'}", flush=True)
    for t in ["0.4", "1.5", "2.5", "3.5", "4.5"]:
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", t, "-i", str(OUT / "test_twoshot.mp4"), "-frames:v", "1", str(OUT / f"qa_{t}.png")], check=False)
print("bal after:", kie_client.credits(), flush=True)
