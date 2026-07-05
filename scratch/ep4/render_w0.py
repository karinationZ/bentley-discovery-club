#!/usr/bin/env python3
"""EP4 RENDER — WAVE 0 (validation, Rule 11). 3 clips spanning the risk classes, from the APPROVED
keyframes, on the LOCKED model kling-3.0/video (owner law: never change the model). Exact EP3 proven
payload (image_urls=[keyframe], kling_elements=[Bentley master+turnaround], multi_shots False, 5s, std).
Purpose: validate the motion recipe (drift-in-motion, camera, butterfly-stream, two-char) BEFORE any
further render spend. ✋ owner reviews all 3 → then wave 1. Gate: BENTLEY_EPISODE=ep4 + Animatic Lock."""
import os, sys, time, concurrent.futures as cf
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from bentley.shared import kie_client
from bentley.shared.hosting import catbox_host

CD  = "assets/character_design"
KFD = "assets/pilot_shots/ep4/keyframes_prod"
OUT = os.path.join(os.path.dirname(__file__), "renders_w0"); os.makedirs(OUT, exist_ok=True)
MASTER, TURN = f"{CD}/Bentley_MASTER_pixar.png", f"{CD}/Bentley_MODEL_SHEET_turnaround.png"

def elements():
    return [{"name": "Bentley",
             "description": ("Bentley the red-fawn Boxer puppy: black face mask, grey chin, floppy folded-down "
                             "ears, white chest blaze, short docked tail stub, teal collar with gold paw-print "
                             "tag, paws the same color as her coat, no white socks"),
             "element_input_urls": [catbox_host(MASTER), catbox_host(TURN)]}]

# (id, keyframe, motion prompt ≤300 chars)  — risk classes: two-shot / solo action hero / butterfly-stream env
CLIPS = [
 ("s1b_nose_taste", f"{KFD}/s1b_nose_taste.png",
  "The small monarch butterfly on Bentley's nose taste-taps it with her feet, wings fluttering; Bentley "
  "crosses her eyes looking down at it and gives a tiny happy surprised recoil, ears flicking, mouth "
  "closed. Soft gentle camera drift. No human teeth, paws same color as her coat."),
 ("s8_glide", f"{KFD}/s8_glide.png",
  "Bentley soars in a joyful glide through a swirling river of orange monarch butterflies over the sea, "
  "ears streaming back, legs tucked, pure delight; the little monarch loops at her nose; hundreds of "
  "butterflies flutter past. Camera follows her flight. No human teeth, paws same color as her coat."),
 ("s7a_reframe_q", f"{KFD}/s7a_reframe_q.png",
  "Bentley sits and gazes up in wonder, tail-stub wagging, mouth softly open in awe; behind her a huge "
  "river of orange monarch butterflies streams across the sky, wings fluttering. Slow gentle camera push "
  "in. No human teeth, paws same color as her coat."),
]

ELS = elements()  # host refs once

def render(cid, key, prompt):
    outp = f"{OUT}/{cid}.mp4"
    if os.path.exists(outp): return f"{cid}: exists"
    payload = {"prompt": prompt, "image_urls": [catbox_host(key)], "sound": False, "duration": "5",
               "aspect_ratio": "16:9", "mode": "std", "multi_shots": False, "kling_elements": ELS}
    for a in range(3):
        try:
            r = kie_client.run("kling-3.0/video", payload, timeout=1200, poll=10)
            kie_client.download(r["urls"][0], outp)
            return f"{cid}: {r['credits']}cr {r['secs']}s"
        except Exception as e:
            if a == 2: return f"{cid}: FAIL {str(e)[:140]}"
            time.sleep(20)

def main():
    with cf.ThreadPoolExecutor(max_workers=3) as ex:
        futs = {ex.submit(render, *c): c[0] for c in CLIPS}
        for fu in cf.as_completed(futs):
            print(fu.result(), flush=True)
    print("WAVE0 DONE", flush=True)

if __name__ == "__main__":
    main()
