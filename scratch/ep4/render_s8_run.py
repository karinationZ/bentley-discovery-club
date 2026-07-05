#!/usr/bin/env python3
"""s8 RESTAGE render — SLOW-MOTION RUN (owner: 'she should be running, slow-motion
running-with-the-wind... slow the camera to emphasize how her ears flap in the wind').
From the owner-picked keyframe (s8_run_c2 -> keyframes_prod/s8_glide.png). Model LOCKED =
kling-3.0/video, exact EP3 payload. Camera PINNED (wave-0 lesson: unpinned camera flew her away)."""
import os, sys, time
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from bentley.shared import kie_client
from bentley.shared.hosting import catbox_host

CD  = "assets/character_design"
KEY = "assets/pilot_shots/ep4/keyframes_prod/s8_glide.png"
OUT = os.path.join(os.path.dirname(__file__), "renders_w0", "s8_run.mp4")

ELS = [{"name": "Bentley",
        "description": ("Bentley the red-fawn Boxer puppy: black face mask, grey chin, floppy folded-down "
                        "ears, white chest blaze, SHORT DOCKED TAIL STUB only, teal collar with gold "
                        "paw-print tag, paws the same color as her coat, no white socks"),
        "element_input_urls": [catbox_host(f"{CD}/Bentley_MASTER_pixar.png"),
                               catbox_host(f"{CD}/Bentley_MODEL_SHEET_turnaround.png")]}]

PROMPT = ("SLOW MOTION: Bentley gallops on the meadow path, all four paws driving the ground, ears "
          "streaming and flapping in the wind, tongue out, joyful; monarch butterflies drift alongside. "
          "Camera tracks beside her at a CONSTANT distance — she stays large and centered the whole "
          "shot, never flies, never leaves the ground. No human teeth, paws same color as her coat.")

def main():
    payload = {"prompt": PROMPT, "image_urls": [catbox_host(KEY)], "sound": False, "duration": "5",
               "aspect_ratio": "16:9", "mode": "std", "multi_shots": False, "kling_elements": ELS}
    for a in range(3):
        try:
            r = kie_client.run("kling-3.0/video", payload, timeout=1200, poll=10)
            kie_client.download(r["urls"][0], OUT)
            print(f"s8_run: {r['credits']}cr {r['secs']}s -> {OUT}", flush=True); return
        except Exception as e:
            if a == 2: print(f"s8_run FAIL {str(e)[:140]}", flush=True)
            else: time.sleep(20)

if __name__ == "__main__":
    main()
