#!/usr/bin/env python3
"""s7b reroll #2 (LAST Kling attempt before restage, per the escalation ladder). Owner notes:
real-Boxer jump (back end up + front lowered -> spring off front paws -> grounded/powerful, NOT floaty),
solid black mask matching the master, SHORT DOCKED TAIL STUB coat-colored NO white tip, natural eyes.
Root cause: Kling drifts identity on high motion — so MAX identity lock: 3 element refs (master +
turnaround + talking master) + hammered canon. Model LOCKED = kling-3.0/video."""
import os, sys, time
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from bentley.shared import kie_client
from bentley.shared.hosting import catbox_host

CD = "assets/character_design"
KEY = "assets/pilot_shots/ep4/keyframes_prod/s7b_mindblown.png"
OUT = os.path.join(os.path.dirname(__file__), "renders_w1", "s7b_mindblown_r2.mp4")

ELS = [{"name": "Bentley",
        "description": ("Bentley the red-fawn Boxer puppy — keep her EXACTLY like the references: SOLID "
                        "BLACK face mask over the muzzle and around the eyes, grey chin, floppy folded-down "
                        "ears, white chest blaze, SHORT DOCKED TAIL STUB (a tiny nub, coat-colored, NO white "
                        "tip, NEVER a long tail), teal collar with gold paw-print tag, paws same color as "
                        "coat no white socks, natural puppy eyes (not enlarged), NO human teeth"),
        "element_input_urls": [catbox_host(f"{CD}/Bentley_MASTER_pixar.png"),
                               catbox_host(f"{CD}/Bentley_MODEL_SHEET_turnaround.png"),
                               catbox_host(f"{CD}/Bentley_TALKING_MASTER.png")]}]

PROMPT = ("Bentley does a real Boxer play-leap: first her back end lifts UP and her front lowers in a "
          "play-bow, then she SPRINGS forward off her front paws in one grounded, weighty, powerful "
          "dog-like leap toward the looping monarch — natural, NOT floaty or exaggerated. She stays "
          "centered and large. SOLID BLACK mask, SHORT DOCKED TAIL STUB no white tip, natural eyes, "
          "tongue out NO teeth.")

def main():
    payload = {"prompt": PROMPT[:340], "image_urls": [catbox_host(KEY)], "sound": False, "duration": "5",
               "aspect_ratio": "16:9", "mode": "std", "multi_shots": False, "kling_elements": ELS}
    for a in range(3):
        try:
            r = kie_client.run("kling-3.0/video", payload, timeout=1200, poll=10)
            kie_client.download(r["urls"][0], OUT)
            print(f"s7b_r2: {r['credits']}cr {r['secs']}s -> {OUT}", flush=True); return
        except Exception as e:
            if a == 2: print(f"s7b_r2 FAIL {str(e)[:140]}", flush=True)
            else: time.sleep(20)

if __name__ == "__main__":
    main()
