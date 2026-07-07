#!/usr/bin/env python3
"""s7b END keyframe — DERIVED FROM the approved START c1 (ai-engineer lever A, 2026-07-06).
Root cause of the churn: the END was generated from the MASTER (fresh identity synthesis = drift) and
then FLUX-edited (warped the Boxer muzzle). FIX: condition on the frame that ALREADY WON — put approved
c1 FIRST in image_input (nano-banana-pro weights earlier refs more), master+turnaround after to reinforce.
Change ONLY the expression, small delta, same pose/composition → the end pose inherits c1's exact Boxer
face. Model LOCKED = nano-banana-pro. 4 candidates → image_bestof ranks vs master → owner signs off."""
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from bentley.shared import kie_client, hosting

CD = "assets/character_design"
C1 = "scratch/ep4/kf_s7b_restage/s7b_start_c1.png"   # the APPROVED, Boxer-correct start frame
OUT = os.path.join(os.path.dirname(__file__), "kf_s7b_restage"); os.makedirs(OUT, exist_ok=True)

# c1 FIRST (dominant identity anchor) → master → turnaround. No plate: c1 already carries the meadow.
REFS = [C1, f"{CD}/Bentley_MASTER_pixar.png", f"{CD}/Bentley_MODEL_SHEET_turnaround.png"]

PROMPT = ("Recreate the FIRST reference image EXACTLY — the SAME Bentley (same broad Boxer muzzle, same "
          "jowls, same SOLID BLACK mask, same eyes, same stocky proportions, same short docked tail "
          "stub), the SAME matte painterly render style, the SAME meadow background, and the SAME "
          "standing pose and composition. Change ONLY her expression to a burst of joyful mind-blown "
          "wonder: eyes a little wider (still natural puppy size, not googly), mouth open in a happy "
          "tongue-out dog pant (NO teeth, no human grin), ears perked with excitement. A SMALL change "
          "only — everything else identical to the first image. 16:9.")

def main():
    urls = [hosting.catbox_host(p) for p in REFS]
    inp = {"prompt": PROMPT, "image_input": urls, "aspect_ratio": "16:9",
           "resolution": "2K", "output_format": "png"}
    for i in range(4):
        try:
            r = kie_client.run("nano-banana-pro", inp, timeout=360, poll=6)
            out = f"{OUT}/s7b_endc1_c{i}.png"; kie_client.download(r["urls"][0], out)
            print(f"endc1_c{i} {r['credits']}cr -> {out}", flush=True)
        except Exception as e:
            print(f"endc1_c{i} FAIL {e}", flush=True)
    print("DONE", flush=True)

if __name__ == "__main__":
    main()
