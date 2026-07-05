#!/usr/bin/env python3
"""WAVE 1 rerolls (#1 of ≤2) — the 4 render-level fails from adversarial QC. Regen-only defect classes
(human teeth / motion / distortion) per the fix-first law. Improved prompts: no-teeth HAMMERED, cameras
PINNED, s3a restaged facing/prominent. Model LOCKED = kling-3.0/video. (s5a is keyframe-level → handled
separately.) Gate: BENTLEY_EPISODE=ep4."""
import os, sys, time, concurrent.futures as cf
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from bentley.shared import kie_client
from bentley.shared.hosting import catbox_host

CD  = "assets/character_design"
KFD = "assets/pilot_shots/ep4/keyframes_prod"
OUT = os.path.join(os.path.dirname(__file__), "renders_w1")

ELS = [{"name": "Bentley",
        "description": ("Bentley the red-fawn Boxer puppy: black face mask, grey chin, floppy folded-down "
                        "ears, white chest blaze, SHORT DOCKED TAIL STUB only, teal collar with gold "
                        "paw-print tag, paws the same color as her coat, no white socks, natural dog "
                        "mouth NO human teeth")}]

NOTEETH = "mouth gently closed or soft with tongue only, ABSOLUTELY NO teeth, no human grin, calm natural eyes"
TAG = "SHORT DOCKED TAIL STUB, paws same color as her coat."

CLIPS = [
 ("s3a_meet_comeon", f"{KFD}/s3a_meet_comeon.png",
  f"Bentley bounces up eagerly and trots FORWARD toward camera to follow, staying prominent and facing "
  f"front, ears bouncing, happy; the monarch loops ahead. LOCKED camera, Bentley large and centered, she "
  f"does NOT turn away. {NOTEETH.split(',')[1].strip()}. {TAG}"),
 ("s3b_plan_gag", f"{KFD}/s3b_plan_gag.png",
  f"Bentley trots after the looping monarch with a quizzical head-tilt, {NOTEETH}; the monarch loops "
  f"ahead. Camera tracks beside her at constant distance, Bentley large. {TAG}"),
 ("s5b_flower_flop", f"{KFD}/s5b_flower_flop.png",
  f"Bentley flops belly-first into the soft flower bank, petals puffing up, happy, {NOTEETH}, eyes not "
  f"wide or bulging; the monarch loops back. LOCKED static camera. {TAG}"),
 ("s7b_mindblown", f"{KFD}/s7b_mindblown.png",
  f"Bentley bounces happily IN PLACE with joy, tongue out but NO teeth, tail-stub wiggling, staying "
  f"CENTERED and LARGE; the monarch loops around her head. LOCKED camera, she never wanders or shrinks. {TAG}"),
]

def render(cid, key, prompt):
    outp = f"{OUT}/{cid}_r1.mp4"
    if os.path.exists(outp):
        return f"{cid}_r1: exists"
    payload = {"prompt": prompt[:320], "image_urls": [catbox_host(key)], "sound": False, "duration": "5",
               "aspect_ratio": "16:9", "mode": "std", "multi_shots": False,
               "kling_elements": [{**ELS[0], "element_input_urls": [catbox_host(f"{CD}/Bentley_MASTER_pixar.png"),
                                                                    catbox_host(f"{CD}/Bentley_MODEL_SHEET_turnaround.png")]}]}
    for a in range(3):
        try:
            r = kie_client.run("kling-3.0/video", payload, timeout=1200, poll=10)
            kie_client.download(r["urls"][0], outp)
            return f"{cid}_r1: {r['credits']}cr {r['secs']}s"
        except Exception as e:
            if a == 2:
                return f"{cid}_r1: FAIL {str(e)[:140]}"
            time.sleep(20)

def main():
    with cf.ThreadPoolExecutor(max_workers=3) as ex:
        futs = {ex.submit(render, *c): c[0] for c in CLIPS}
        for fu in cf.as_completed(futs):
            print(fu.result(), flush=True)
    print("W1 REROLLS DONE", flush=True)

if __name__ == "__main__":
    main()
