#!/usr/bin/env python3
"""s10a REDO (owner NO x2: eyes too googly/oversized; FLUX recolor didn't shrink them).
Root cause: the 'delighted double-take / surprise' beat drives nano-banana-pro to draw huge round
googly cartoon eyes. Fix = prompt-level: pin eye SIZE to the master, carry the surprise with brows/
ears/mouth, NOT eye size. Model LOCKED = nano-banana-pro. Master-first refs, grove plate last.
s10a was never approved (only its staging was picked), so regenerating this ONE shot is correct."""
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from bentley.shared import kie_client, hosting

CD = "assets/character_design"
REFS = [f"{CD}/Bentley_MASTER_pixar.png", f"{CD}/Bentley_MODEL_SHEET_turnaround.png",
        f"{CD}/Mira_LOCKED.png", f"{CD}/Grove_plate.png"]
OUT = os.path.join(os.path.dirname(__file__), "kf_s10a_redo"); os.makedirs(OUT, exist_ok=True)

FIDELITY = ("Render Bentley EXACTLY as she appears in the first reference image — same character, face, "
            "fur, proportions, and the EXACT same render style and finish. Black face mask, grey chin, "
            "floppy folded-down ears, white chest blaze, short docked tail stub, teal collar with the "
            "gold paw-print tag.")
EYES = ("HER EYES ARE THE MOST IMPORTANT THING: they must be the SAME as the first reference image — "
        "modest almond-shaped, normal-sized, warm BROWN puppy eyes set naturally into her face. Do NOT "
        "enlarge them, do NOT make them round, bulging, wide, white or googly, NOT cartoon eyeballs. Even "
        "though she is surprised, her eyes stay their normal calm size — the surprise is shown ONLY by "
        "slightly raised eyebrows, perked-up ears and a small soft open mouth, never by big eyes.")
PAW = ("Her paws, feet and lower legs are SOLID RED-FAWN, the exact same color as her coat — NO white "
       "paws, socks or toes.")
POSE = ("SCENE: in the sunlit eucalyptus grove (use the last reference image ONLY for setting): Bentley "
        "stands and turns her head with a gentle, curious, pleasantly-surprised look toward Mira the "
        "monarch butterfly, who perches on a twig beside a small green chrysalis. Mira exactly matches "
        "the monarch reference. Warm, wholesome, storybook-cute.")
PROMPT = f"{FIDELITY} {EYES} {PAW} {POSE} 16:9."

def main():
    urls = [hosting.catbox_host(p) for p in REFS]
    inp = {"prompt": PROMPT, "image_input": urls, "aspect_ratio": "16:9",
           "resolution": "2K", "output_format": "png"}
    for i in range(3):
        try:
            r = kie_client.run("nano-banana-pro", inp, timeout=360, poll=6)
            out = f"{OUT}/s10a_c{i}.png"; kie_client.download(r["urls"][0], out)
            print(f"s10a_c{i} {r['credits']}cr -> {out}", flush=True)
        except Exception as e:
            print(f"s10a_c{i} FAIL {e}", flush=True)
    print("DONE", flush=True)

if __name__ == "__main__":
    main()
