#!/usr/bin/env python3
"""s7b WIDE — END keyframe, DERIVED FROM the approved wide START (ai-engineer lever 1a).

START = scratch/ep4/kf_s7b_wide/s7b_wide_c1_fixed.png (owner-approved wide reaction; paws box-wand fixed).
Put the START FIRST in image_input (nano-banana-pro weights earlier refs most), master to reinforce canon.
Change ONE thing as a SMALL delta (subtle reaction — head up a touch, happy tongue-out pant, tail wag),
same wide framing/composition/background/butterflies → the END inherits the START's exact identity + scene
and pins the render's last frame on-model. Regenerating the paw region here also renders them clean fawn.
Model LOCKED = nano-banana-pro. 3 candidates → image_bestof ranks vs master → owner signs the START+END pair."""
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from bentley.shared import kie_client, hosting

CD = "assets/character_design"
START = "scratch/ep4/kf_s7b_wide/s7b_wide_c1_fixed.png"
OUT = os.path.join(os.path.dirname(__file__), "kf_s7b_wide"); os.makedirs(OUT, exist_ok=True)

REFS = [START, f"{CD}/Bentley_MASTER_pixar.png"]   # START FIRST = dominant identity + composition anchor

PROMPT = ("Recreate the FIRST reference image EXACTLY — the SAME wide shot, the SAME small Bentley standing "
          "in the SAME spot on the coastal wildflower meadow path, SAME pose and framing, SAME sky full of "
          "streaming monarch butterflies, SAME monarch near her, SAME golden-hour light and cartoony-Pixar "
          "render style. Change ONLY her reaction, a SMALL delta: her head tilts up a little more in "
          "delight, her mouth opens into a happy tongue-out dog pant (NO teeth, NO human grin), and her "
          "short docked tail-stub wags. Her paws, feet and toes are SOLID RED-FAWN, the exact same color as "
          "her coat — NO white socks or toes. Everything else identical to the first image. Natural "
          "normal-sized warm brown puppy eyes (not enlarged/googly). 16:9.")


def main():
    urls = [hosting.catbox_host(p) for p in REFS]
    inp = {"prompt": PROMPT, "image_input": urls, "aspect_ratio": "16:9",
           "resolution": "2K", "output_format": "png"}
    for i in range(3):
        outp = f"{OUT}/s7b_wide_end_c{i}.png"
        try:
            r = kie_client.run("nano-banana-pro", inp, timeout=360, poll=6)
            kie_client.download(r["urls"][0], outp)
            print(f"end_c{i} {r['credits']}cr -> {outp}", flush=True)
        except Exception as e:
            print(f"end_c{i} FAIL {e}", flush=True)
    print("DONE", flush=True)


if __name__ == "__main__":
    main()
