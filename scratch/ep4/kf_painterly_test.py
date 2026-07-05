#!/usr/bin/env python3
"""EP4 PAINTERLY calibration (owner locked style B = painterly storybook, 2026-07-05).
QUALITY model nano-banana-pro (owner: no cheap model), anchored on the painterly Meadow plate as the
STYLE reference, with a strong painterly style-lock (pro defaults glossy). Test shot = s3a, so we can
compare directly against the painterly c1 the owner liked. 4 candidates. If pro reliably holds the
painterly look on-model, the full 13-keyframe batch runs this exact recipe."""
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from bentley.shared import kie_client, hosting

CD = "assets/character_design"
PLATE = f"{CD}/Meadow_plate.png"
BODY  = f"{CD}/Bentley_MASTER_pixar.png"
TURN  = f"{CD}/Bentley_MODEL_SHEET_turnaround.png"
MIRA  = f"{CD}/Mira_LOCKED.png"
OUT   = os.path.join(os.path.dirname(__file__), "kf_painterly")
os.makedirs(OUT, exist_ok=True)

STYLE = ("Render the ENTIRE image in the exact same soft, matte, HAND-PAINTED PAINTERLY STORYBOOK "
         "ILLUSTRATION style as the first reference image (the meadow plate): visible gouache/oil "
         "brushwork, flat painterly shading, soft painted edges, warm illustrated look. It must look "
         "hand-painted by the same illustrator — NOT a glossy smooth 3D render, NOT shiny plastic, NOT "
         "CGI, NOT Pixar. Matte finish throughout, Bentley painted into the scene with the same brushwork.")
MASTER = ("Keep Bentley's DESIGN identical to the Bentley reference: red-fawn Boxer puppy, black face "
          "mask, grey chin, brown eyes, floppy folded-down ears, white chest blaze, short docked tail "
          "stub, teal collar with the gold paw-print tag; natural realistic puppy proportions, do NOT "
          "enlarge her eyes or round her out.")
PAW = ("CRITICAL: her paws, feet and lower legs are SOLID RED-FAWN, the exact same color as her coat — "
       "NO white paws, NO white socks, NO white toes.")
PROMPT = (f"A coastal wildflower-meadow scene at dawn: Bentley the Boxer puppy mid-bounce on the dirt "
          f"path, ears flopping, looking up eagerly to follow the monarch butterfly Mira, who loops "
          f"playfully in the air just ahead of her. Keep the meadow, ocean and warm dawn light of the "
          f"plate. {STYLE} {MASTER} {PAW} Mira exactly matches the monarch reference. 16:9.")

def main():
    urls = [hosting.catbox_host(p) for p in (PLATE, BODY, TURN, MIRA)]
    inp = {"prompt": PROMPT, "image_input": urls, "aspect_ratio": "16:9",
           "resolution": "2K", "output_format": "png"}
    for i in range(4):
        print(f"candidate {i} (nano-banana-pro, painterly)...", flush=True)
        try:
            r = kie_client.run("nano-banana-pro", inp, timeout=360, poll=6)
            out = f"{OUT}/s3a_pnt_c{i}.png"
            kie_client.download(r["urls"][0], out)
            print(f"  c{i}: {r['credits']}cr {r['secs']}s -> {out}", flush=True)
        except Exception as e:
            print(f"  c{i} FAILED: {e}", flush=True)
    print("DONE", flush=True)

if __name__ == "__main__":
    main()
