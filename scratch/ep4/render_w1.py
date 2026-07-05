#!/usr/bin/env python3
"""EP4 RENDER — WAVE 1 (Rule 11 gated wave). 6 painterly MEADOW HERO clips from the owner-approved
gate-4 keyframes, on the LOCKED model kling-3.0/video (never change the model). Wave-0 lessons baked in:
CAMERA PINNED per shot (unpinned flew the subject away / over-pushed), docked-tail + paw language in
every prompt. Prompts <=300 chars. ✋ owner reviews the wave before wave 2. Gate: BENTLEY_EPISODE=ep4."""
import os, sys, time, concurrent.futures as cf
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from bentley.shared import kie_client
from bentley.shared.hosting import catbox_host

CD  = "assets/character_design"
KFD = "assets/pilot_shots/ep4/keyframes_prod"
OUT = os.path.join(os.path.dirname(__file__), "renders_w1"); os.makedirs(OUT, exist_ok=True)

ELS = [{"name": "Bentley",
        "description": ("Bentley the red-fawn Boxer puppy: black face mask, grey chin, floppy folded-down "
                        "ears, white chest blaze, SHORT DOCKED TAIL STUB only, teal collar with gold "
                        "paw-print tag, paws the same color as her coat, no white socks"),
        "element_input_urls": [catbox_host(f"{CD}/Bentley_MASTER_pixar.png"),
                               catbox_host(f"{CD}/Bentley_MODEL_SHEET_turnaround.png")]}]

TAG = "SHORT DOCKED TAIL STUB, no human teeth, paws same color as her coat."
# (id, keyframe, motion prompt) — camera pinned per shot
CLIPS = [
 ("s3a_meet_comeon", f"{KFD}/s3a_meet_comeon.png",
  f"Bentley bounces up eagerly and trots forward to follow; the small monarch loops in the air ahead "
  f"and flutters onward. LOCKED camera, both stay framed, Bentley large. {TAG}"),
 ("s3b_plan_gag", f"{KFD}/s3b_plan_gag.png",
  f"Bentley trots after the butterfly with her head tilted quizzically, slightly overshooting; the "
  f"monarch loops ahead. Camera tracks beside her at CONSTANT distance, Bentley large. {TAG}"),
 ("s4b_copy_sneeze", f"{KFD}/s4b_copy_sneeze.png",
  f"Bentley dips her nose into a wildflower, a puff of yellow pollen rises, then a BIG sneeze, head "
  f"recoiling, ears flapping; the monarch loops nearby. LOCKED static camera. {TAG}"),
 ("s5a_lead_bound", f"{KFD}/s5a_lead_bound.png",
  f"Bentley bounds proudly ahead down the meadow path, leading, chest out, happy; monarchs drift past. "
  f"Camera tracks beside her at CONSTANT distance, she stays large, on the ground. {TAG}"),
 ("s5b_flower_flop", f"{KFD}/s5b_flower_flop.png",
  f"Bentley flops belly-first into the soft flower bank, petals puffing up, dizzy and happy; the monarch "
  f"loops back to check on her. LOCKED static camera. {TAG}"),
 ("s7b_mindblown", f"{KFD}/s7b_mindblown.png",
  f"Bentley spins on the spot in pure joy, tongue out, tail-stub wiggling; the monarch loops playfully "
  f"around her head. Gentle LOCKED camera, Bentley centered and large. {TAG}"),
]

def render(cid, key, prompt):
    outp = f"{OUT}/{cid}.mp4"
    if os.path.exists(outp):
        return f"{cid}: exists"
    payload = {"prompt": prompt, "image_urls": [catbox_host(key)], "sound": False, "duration": "5",
               "aspect_ratio": "16:9", "mode": "std", "multi_shots": False, "kling_elements": ELS}
    for a in range(3):
        try:
            r = kie_client.run("kling-3.0/video", payload, timeout=1200, poll=10)
            kie_client.download(r["urls"][0], outp)
            return f"{cid}: {r['credits']}cr {r['secs']}s"
        except Exception as e:
            if a == 2:
                return f"{cid}: FAIL {str(e)[:140]}"
            time.sleep(20)

def main():
    for c in CLIPS:
        assert len(c[2]) <= 320, f"{c[0]} prompt {len(c[2])} chars"
    with cf.ThreadPoolExecutor(max_workers=3) as ex:
        futs = {ex.submit(render, *c): c[0] for c in CLIPS}
        for fu in cf.as_completed(futs):
            print(fu.result(), flush=True)
    print("WAVE1 DONE", flush=True)

if __name__ == "__main__":
    main()
