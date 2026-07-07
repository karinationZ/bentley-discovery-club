#!/usr/bin/env python3
"""s7b RUN v2 keyframe — ¾-FRONT (toward-camera) restage to ROOT-FIX the chronic tail (owner "you take on",
2026-07-06). The side-profile run exposed the rump, and Kling's running-dog prior grew a long tail in BOTH
run renders (and even a pinned wide render) — unbeatable by prompt. Fix per §3a lever 6 (stage around the
weak spot): frame her ¾-FRONT so her BODY OCCLUDES the tail (this is exactly why s8's toward-camera run had
no tail defect). Bonus: front-on legs render cleaner (kills the fused-leg/stump-paw gait glitch), and a
face-forward keyframe lets me LOCK soft warm eyes (kills the googly-eye drift). Kept DISTINCT from s8:
grounded MEADOW run, no bluff-leap. Edit-from-master. Model LOCKED = nano-banana-pro. 4 candidates."""
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from bentley.shared import kie_client, hosting

CD = "assets/character_design"
OUT = os.path.join(os.path.dirname(__file__), "kf_s7b_run2"); os.makedirs(OUT, exist_ok=True)

FIDELITY = ("Render Bentley EXACTLY as in the first reference image — the SAME character, face, fur, "
            "proportions, and the EXACT same cartoony-Pixar render style. SOLID BLACK face mask over the "
            "muzzle and around the eyes, grey chin, floppy folded-down ears, white chest blaze, teal collar "
            "with gold paw-print tag.")
EYES = ("Soft, warm, dark-brown almond eyes with a gentle, HAPPY, relaxed gaze — the iris fills the eye, "
        "only a thin sliver of white at the inner corner. NOT wide, NOT round, NOT bulging, NOT startled, "
        "NO white showing above or around the iris.")
PAW = "Her paws, feet and lower legs are SOLID RED-FAWN, the same color as her coat — NO white paws, socks or toes."

SCENE = ("ACTION shot, THREE-QUARTER FRONT view: Bentley runs happily TOWARD the camera and slightly across "
         "the frame, down the coastal wildflower meadow path, caught mid-stride in a joyful bounding run, "
         "her floppy ears flying UP and back in the wind, mouth open in a happy tongue-out pant (NO human "
         "teeth). Her body faces the camera so her REAR AND TAIL ARE BEHIND HER, hidden from view. Exactly "
         "FOUR clean legs with toed paws, driving forward, all near the ground (grounded — not leaping or "
         "flying). Behind and above her a river of orange monarch butterflies streams across the golden-hour "
         "sky. She is MEDIUM in a wide frame, coastal bluff + sea behind. Warm golden light. 16:9.")


def refs():
    r = [f"{CD}/Bentley_MASTER_pixar.png", f"{CD}/Bentley_MODEL_SHEET_turnaround.png",
         f"{CD}/Mira_LOCKED.png", f"{CD}/Meadow_plate.png"]
    return [hosting.catbox_host(p) for p in r]


def main():
    urls = refs()
    prompt = f"{FIDELITY} {EYES} {PAW} {SCENE}"
    inp = {"prompt": prompt, "image_input": urls, "aspect_ratio": "16:9",
           "resolution": "2K", "output_format": "png"}
    for i in range(4):
        outp = f"{OUT}/s7b_run2_c{i}.png"
        try:
            r = kie_client.run("nano-banana-pro", inp, timeout=360, poll=6)
            kie_client.download(r["urls"][0], outp)
            print(f"run2_c{i} {r['credits']}cr -> {outp}", flush=True)
        except Exception as e:
            print(f"run2_c{i} FAIL {e}", flush=True)
    print("DONE", flush=True)


if __name__ == "__main__":
    main()
