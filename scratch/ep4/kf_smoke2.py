#!/usr/bin/env python3
"""EP4 cheap-keyframe RE-VERIFY (2026-07-05) — owner rejected s3a c0/c2 for STYLE drift (glossy 3D
toy render, not the plate's painterly style) + white paws; c1 (painterly, integrated) = good.
This re-tests the EXACT failure case (foreground bounding Bentley on the meadow) with a prompt that
explicitly LOCKS the painterly/hand-painted render + natural proportions, 4 candidates, to confirm the
cheap plate-edit method can reliably hold the approved STYLE on foreground hero shots before the batch."""
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from bentley.shared import kie_client, hosting

CD = "assets/character_design"
PLATE = f"{CD}/Meadow_plate.png"
BODY  = f"{CD}/Bentley_MASTER_pixar.png"
TURN  = f"{CD}/Bentley_MODEL_SHEET_turnaround.png"
MIRA  = f"{CD}/Mira_LOCKED.png"
OUT   = os.path.join(os.path.dirname(__file__), "kf_smoke2")
os.makedirs(OUT, exist_ok=True)

# STYLE-LOCK is the new/critical clause (owner rejected the glossy-3D drift on c0/c2).
STYLE = ("Render Bentley in the SAME soft, hand-painted, painterly storybook illustration style as this "
         "background plate — matte fur with visible painterly brushwork and the same warm lighting; she "
         "must look PAINTED INTO the scene by the same artist. Do NOT render her as a glossy, smooth, "
         "shiny 3D toy; do NOT enlarge her eyes; do NOT make her rounder, smoother or more cartoonish "
         "than the reference master. Natural, realistic Boxer-puppy proportions, matte finish.")
MASTER = ("Keep Bentley EXACTLY identical to the reference master (the red-fawn Boxer puppy): same face, "
          "black face mask, grey chin, brown eyes, floppy folded-down ears, white chest blaze, short "
          "docked tail stub, teal collar with the gold paw-print tag.")
PAW = ("CRITICAL: her paws, feet and lower legs are SOLID RED-FAWN, the exact same color as her coat — "
       "NO white paws, NO white socks, NO white toes.")
PROMPT = (f"Edit this coastal wildflower-meadow scene (image 1), keeping its meadow, ocean, path, dawn "
          f"light and painterly style EXACTLY as they are. Add BENTLEY mid-bounce on the dirt path, ears "
          f"flopping, looking up eagerly about to follow. {MASTER} {STYLE} {PAW} Also add MIRA — the "
          f"monarch butterfly from the last reference — looping playfully in the air just ahead of "
          f"Bentley, wings open, exactly matching her locked design. 16:9.")

def main():
    urls = [hosting.catbox_host(p) for p in (PLATE, BODY, TURN, MIRA)]
    inp = {"prompt": PROMPT, "image_urls": urls, "image_size": "16:9", "output_format": "png"}
    for i in range(4):
        print(f"candidate {i}...", flush=True)
        try:
            r = kie_client.run("google/nano-banana-edit", inp, timeout=300, poll=5)
            out = f"{OUT}/s3a_v2_c{i}.png"
            kie_client.download(r["urls"][0], out)
            print(f"  c{i}: {r['credits']}cr {r['secs']}s -> {out}", flush=True)
        except Exception as e:
            print(f"  c{i} FAILED: {e}", flush=True)
    print("DONE", flush=True)

if __name__ == "__main__":
    main()
