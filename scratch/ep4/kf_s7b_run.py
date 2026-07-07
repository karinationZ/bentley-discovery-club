#!/usr/bin/env python3
"""s7b RUN restage keyframes (owner redirect 2026-07-06): drop the drifty "mind-blown reaction" pose and
stage the JOY as a BODY ACTION — a slow-motion GALLOP, ears flying — which fits the VO ("...having the BEST
time?? That is the most DOG thing I've ever heard. I LOVE it!") and is the PROVEN drift-safe staging (s8's
slow-mo run was owner-approved; a coherent natural gait holds where an invented reaction melts).

Kept DISTINCT from s8 (s8 = bound TOWARD camera off the bluff -> glide): s7b = SIDE-PROFILE gallop ACROSS the
meadow, ears streaming back, the monarch river flowing WITH her. Medium-wide, full body (face not the subject
-> low drift). Edit-from-master (§3a lever 1). Model LOCKED = nano-banana-pro. 4 candidates -> image_bestof ->
owner sign-off -> render with the proven s8_run recipe. NO tail-motion / no reaction-pose wording (those
invited the tail + teeth drift last time)."""
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from bentley.shared import kie_client, hosting

CD = "assets/character_design"
OUT = os.path.join(os.path.dirname(__file__), "kf_s7b_run"); os.makedirs(OUT, exist_ok=True)

FIDELITY = ("Render Bentley EXACTLY as in the first reference image — the SAME character, face, fur, "
            "proportions, and the EXACT same cartoony-Pixar render style. SOLID BLACK face mask over the "
            "muzzle and around the eyes, grey chin, floppy folded-down ears, white chest blaze, teal collar "
            "with gold paw-print tag.")
TAIL = "TAIL: Bentley is a DOCKED Boxer — only a SHORT coat-colored STUB, NO long/fluffy/curled tail, NO white tip."
PAW = ("Her paws, feet and lower legs are SOLID RED-FAWN, the exact same color as her coat — "
       "NO white paws, socks or toes.")
EYES = "Natural, normal-sized warm brown puppy eyes — NOT enlarged, NOT bulging, NOT googly."

SCENE = ("ACTION WIDE — Bentley GALLOPS in SIDE PROFILE across the coastal wildflower meadow path, caught "
         "mid-stride in a joyful full run (legs extended, body low and driving forward), her floppy ears "
         "STREAMING back in the wind, mouth open in happy delight. Above and around her a RIVER of orange "
         "monarch butterflies streams across the golden-hour sky in the SAME direction she runs, as if she "
         "runs along with the migration. Slow-motion energy. She is medium-small and FULL-BODY in a wide "
         "frame (side-on, NOT a close-up), the sea and bluff behind. Warm golden light. 16:9.")


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
        outp = f"{OUT}/s7b_run_c{i}.png"
        try:
            r = kie_client.run("nano-banana-pro", inp, timeout=360, poll=6)
            kie_client.download(r["urls"][0], outp)
            print(f"run_c{i} {r['credits']}cr -> {outp}", flush=True)
        except Exception as e:
            print(f"run_c{i} FAIL {e}", flush=True)
    print("DONE", flush=True)


if __name__ == "__main__":
    main()
