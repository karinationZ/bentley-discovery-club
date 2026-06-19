#!/usr/bin/env python3
"""kie.ai Kling 2.6 image-to-video test — drive a motion clip from the N6 kie keyframe.
Reports credits + seconds vs fal Kling 2.5 (~$0.35/5s)."""
from kie_client import run, credits, download
KEY_URL = "https://tempfile.aiquickdraw.com/workers/nano/image_1781825351947_p9ae3v.png"
PROMPT = ("Bentley the red-fawn Boxer puppy holds her warm, fond gaze directly into camera and gives a tiny "
 "affectionate head-tilt; she blinks softly, her ears shift slightly, her chest breathes gently, a few fur "
 "strands and the soft background bokeh drift — everything subtly alive with natural living motion. Bright warm "
 "golden-dawn light on her face, rich vibrant colorful red-fawn fur, NOT dark. Locked camera, no speech, mouth stays soft and closed.")
print("bal before:", credits())
r = run("kling-2.6/image-to-video", {"prompt": PROMPT, "image_urls": [KEY_URL], "sound": False, "duration": "5"})
download(r["urls"][0], "tests/kie/N6_kie_clip.mp4")
print(f"DONE  credits={r['credits']}  secs={r['secs']}  tid={r['tid']}")
print("url:", r["urls"][0])
print("bal after:", credits())
