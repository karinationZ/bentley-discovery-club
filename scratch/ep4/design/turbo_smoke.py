#!/usr/bin/env python3
"""EP4 Kling-Turbo SMOKE TEST — confirm the KIE slug runs AND holds our env style.
Confirmed slug (docs.kie.ai/market/kling/v3-turbo-image-to-video): kling/v3-turbo-image-to-video
Same Kling-3.0 family as our hero `kling-3.0/video` → best style match for env coverage.
Pure butterfly-sky still (NO Bentley) so this only tests environment motion + style hold.
Gate: BENTLEY_EPISODE=ep4 + Animatic Lock PASSED in GATES.md (spend guard in gates.py)."""
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..")))
from bentley.shared import kie_client, hosting

STILL = os.path.join(os.path.dirname(__file__), "turbo_smoke_still.png")
MODEL = "kling/v3-turbo-image-to-video"
PROMPT = ("A dozen orange-and-black monarch butterflies drift and flutter gently across a soft "
          "sunlit sky above a wildflower meadow; flowers sway in a light breeze, warm golden "
          "afternoon light, dreamy painterly cartoon style, calm continuous motion, no camera shake.")

def main():
    print(f"hosting {STILL} ...", flush=True)
    url = hosting.catbox_host(STILL)
    print(f"hosted: {url}", flush=True)
    inp = {"prompt": PROMPT, "image_urls": [url], "duration": "5", "resolution": "720p"}
    print(f"createTask model={MODEL} dur=5 res=720p ...", flush=True)
    r = kie_client.run(MODEL, inp, timeout=600, poll=6)
    out = os.path.join(os.path.dirname(__file__), "turbo_smoke_out.mp4")
    kie_client.download(r["urls"][0], out)
    print(f"SMOKE OK  credits={r['credits']}  secs={r['secs']}  tid={r['tid']}", flush=True)
    print(f"SAVED {out}", flush=True)

if __name__ == "__main__":
    main()
