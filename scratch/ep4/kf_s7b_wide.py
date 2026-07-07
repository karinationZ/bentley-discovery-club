#!/usr/bin/env python3
"""s7b WIDE restage keyframes (owner approved Option A — tightened, 2026-07-06).

The close "mind-blown" reaction is a Kling drift trap (the contained close restage MELTED the face mid-clip
+ bug-eyes; QC 5/6 ship-blocking). Today's proven lesson: Kling HOLDS Bentley when she is WIDE / small-in-
frame, and only drifts on a close Boxer face. So restage s7b as a WIDE, small-in-frame BODY beat: Bentley
small on the coastal meadow path, grounded happy two-step + tail-stub wag, looking UP as a river of monarchs
streams past and Mira loops near her — NO leap/spin/close-face. This keeps the beat, obeys the no-static rule
(real motion), and stays in Kling's safe zone.

Edit-from-master (§3a lever 1): master FIRST ref. Model LOCKED = nano-banana-pro. Paw block = the sanctioned
coat-bound emphatic construction (Rule-3 prompt-phrasing law). 4 candidates → image_bestof ranks vs master →
✋ OWNER KEYFRAME SIGN-OFF before any render. NO render here — image tier only (ungated)."""
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from bentley.shared import kie_client, hosting

CD = "assets/character_design"
OUT = os.path.join(os.path.dirname(__file__), "kf_s7b_wide"); os.makedirs(OUT, exist_ok=True)

FIDELITY = ("Render Bentley EXACTLY as in the first reference image — the SAME character, face, fur, "
            "proportions, and the EXACT same cartoony-Pixar render style. SOLID BLACK face mask over the "
            "muzzle and around the eyes, grey chin, floppy folded-down ears, white chest blaze, teal "
            "collar with gold paw-print tag.")
TAIL = ("TAIL: Bentley is a DOCKED Boxer — a SHORT stub only, coat-colored, NO long tail, NO white or "
        "pale tip, NO fluffy or curled tail.")
PAW = ("Her paws, feet and lower legs are SOLID RED-FAWN, the exact same color as her coat — "
       "NO white paws, socks or toes.")
EYES = "Natural, normal-sized warm brown puppy eyes — NOT enlarged, NOT bulging, NOT googly."

SCENE = ("WIDE SHOT — Bentley is SMALL in the frame, full-body, standing on the coastal wildflower meadow "
         "path with the sea and open sky behind her (use the last reference image for the setting). She "
         "looks UP in delighted wonder with a grounded, happy little two-step, all four paws on the ground "
         "and her short tail-stub wagging — NO leaping, NO jumping, NO spinning. Above and around her a "
         "RIVER of orange monarch butterflies streams across the sky, and the monarch Mira loops in the air "
         "near her head. Warm golden-hour light, locked wide camera, Bentley small and full-body in frame "
         "(NOT a close-up). 16:9.")


def refs():
    r = [f"{CD}/Bentley_MASTER_pixar.png", f"{CD}/Bentley_MODEL_SHEET_turnaround.png",
         f"{CD}/Mira_LOCKED.png", f"{CD}/Meadow_plate.png"]
    return [hosting.catbox_host(p) for p in r]


def main():
    urls = refs()
    prompt = f"{FIDELITY} {TAIL} {PAW} {EYES} {SCENE}"
    inp = {"prompt": prompt, "image_input": urls, "aspect_ratio": "16:9",
           "resolution": "2K", "output_format": "png"}
    for i in range(4):
        outp = f"{OUT}/s7b_wide_c{i}.png"
        try:
            r = kie_client.run("nano-banana-pro", inp, timeout=360, poll=6)
            kie_client.download(r["urls"][0], outp)
            print(f"wide_c{i} {r['credits']}cr -> {outp}", flush=True)
        except Exception as e:
            print(f"wide_c{i} FAIL {e}", flush=True)
    print("DONE", flush=True)


if __name__ == "__main__":
    main()
