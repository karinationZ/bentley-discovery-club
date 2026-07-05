#!/usr/bin/env python3
"""s8 RESTAGE — RUN, not glide (owner 2026-07-05: 'flying looks ridiculous; she should be running,
slow-motion running-with-the-wind, ears flapping'). New keyframe: Bentley RUNNING on the ground through
the meadow, ears streaming in the wind, monarchs alongside. Model LOCKED = nano-banana-pro. Master-first
refs, plate last. Hard PAW + hard DOCKED-TAIL locks (both drifted on the wave-0 render). 3 candidates."""
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from bentley.shared import kie_client, hosting

CD = "assets/character_design"
REFS = [f"{CD}/Bentley_MASTER_pixar.png", f"{CD}/Bentley_MODEL_SHEET_turnaround.png",
        f"{CD}/Mira_LOCKED.png", f"{CD}/Meadow_plate.png"]
OUT = os.path.join(os.path.dirname(__file__), "kf_s8_run"); os.makedirs(OUT, exist_ok=True)

FIDELITY = ("Render Bentley EXACTLY as she appears in the first reference image — same character, face, "
            "fur, proportions, and the EXACT same painterly render style and finish. Black face mask, grey "
            "chin, floppy folded-down ears, white chest blaze, teal collar with the gold paw-print tag.")
TAIL = ("TAIL: Bentley is a DOCKED Boxer — her tail is a SHORT stub only. NO long tail, NO fluffy or hairy "
        "tail, NO curled tail — just the short docked stub as in the reference master.")
PAW = ("Her paws, feet and lower legs are SOLID RED-FAWN, the exact same color as her coat — NO white "
       "paws, NO white socks, NO white toes.")
POSE = ("SCENE: Bentley runs at a joyful full gallop through the coastal wildflower meadow along the "
        "bluff (use the last reference image ONLY for the setting), her body low, dynamic and mid-stride, "
        "all four legs driving, ears streaming straight back in the wind, tongue out with pure delight; a "
        "swirling river of orange monarch butterflies streams alongside and behind her; warm dawn light, "
        "sea beyond. Bentley is PROMINENT and large in the frame. Mira the monarch matches her reference.")
PROMPT = f"{FIDELITY} {TAIL} {PAW} {POSE} 16:9."

def main():
    urls = [hosting.catbox_host(p) for p in REFS]
    inp = {"prompt": PROMPT, "image_input": urls, "aspect_ratio": "16:9",
           "resolution": "2K", "output_format": "png"}
    for i in range(3):
        try:
            r = kie_client.run("nano-banana-pro", inp, timeout=360, poll=6)
            out = f"{OUT}/s8_run_c{i}.png"; kie_client.download(r["urls"][0], out)
            print(f"s8_run_c{i} {r['credits']}cr -> {out}", flush=True)
        except Exception as e:
            print(f"s8_run_c{i} FAIL {e}", flush=True)
    print("DONE", flush=True)

if __name__ == "__main__":
    main()
