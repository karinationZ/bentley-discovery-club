#!/usr/bin/env python3
"""s7b RESTAGE keyframes (owner approved direction A, 2026-07-06) — a CONTAINED mind-blown reaction
(no leap/travel/spin, the high-motion drift trigger). Two CLOSE poses so the last-frame pin is honored:
  START = Bentley planted centered, alert, head lifting to look up.
  END   = Bentley eyes-wide delight, small pop on the spot, tail-stub wag (this frame PINS the render
          end on-model — solid mask + SHORT DOCKED TAIL, no white tip).
Model LOCKED = nano-banana-pro. Edit-from-master (§3a lever 1). 4 candidates each; image_bestof ranks
them vs the master. Image tier = ungated. NO render here — keyframes only, for owner sign-off."""
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from bentley.shared import kie_client, hosting

CD = "assets/character_design"
OUT = os.path.join(os.path.dirname(__file__), "kf_s7b_restage"); os.makedirs(OUT, exist_ok=True)

FIDELITY = ("Render Bentley EXACTLY as in the first reference image — same character, face, fur, "
            "proportions, and the EXACT same matte painterly render style. SOLID BLACK face mask over "
            "the muzzle and around the eyes, grey chin, floppy folded-down ears, white chest blaze, teal "
            "collar with gold paw-print tag.")
TAIL = ("TAIL: Bentley is a DOCKED Boxer — a SHORT stub only, coat-colored, NO long tail, NO white or "
        "pale tip, NO fluffy or curled tail.")
PAW = "Her paws, feet and lower legs are SOLID RED-FAWN, the exact same color as her coat — no white socks/toes."
EYES = "Natural, normal-sized warm brown puppy eyes — NOT enlarged, NOT bulging, NOT googly."

POSES = {
 "start": ("SCENE: Bentley stands PLANTED and CENTERED on the coastal meadow path (use the last reference "
           "for the setting only), alert, her head just beginning to lift to look UP toward the sky, "
           "mouth gently closed, calm and ready. Locked, centered composition, Bentley large in frame."),
 "end":   ("SCENE: Bentley stands CENTERED on the same meadow spot in a burst of joyful wonder — her head "
           "is UP, front paws just hopped a little off the ground in a small delighted pop, tongue out "
           "happily (soft mouth, NO teeth), short tail-stub mid-wag; the monarch butterfly Mira loops in "
           "the air near her head. Locked, centered composition, Bentley large in frame."),
}

def refs(with_mira):
    r = [f"{CD}/Bentley_MASTER_pixar.png", f"{CD}/Bentley_MODEL_SHEET_turnaround.png"]
    if with_mira: r.append(f"{CD}/Mira_LOCKED.png")
    r.append(f"{CD}/Meadow_plate.png")
    return [hosting.catbox_host(p) for p in r]

def main():
    for pose, scene in POSES.items():
        urls = refs(with_mira=(pose == "end"))
        prompt = f"{FIDELITY} {TAIL} {PAW} {EYES} {scene} 16:9."
        inp = {"prompt": prompt, "image_input": urls, "aspect_ratio": "16:9",
               "resolution": "2K", "output_format": "png"}
        for i in range(4):
            outp = f"{OUT}/s7b_{pose}_c{i}.png"
            if os.path.exists(outp):
                print(f"{pose}_c{i} exists", flush=True); continue
            try:
                r = kie_client.run("nano-banana-pro", inp, timeout=360, poll=6)
                kie_client.download(r["urls"][0], outp)
                print(f"{pose}_c{i} {r['credits']}cr", flush=True)
            except Exception as e:
                print(f"{pose}_c{i} FAIL {e}", flush=True)
    print("DONE", flush=True)

if __name__ == "__main__":
    main()
