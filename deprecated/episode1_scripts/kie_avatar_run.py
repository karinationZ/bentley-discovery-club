#!/usr/bin/env python3
"""kie.ai Kling Avatar (talking/lip-sync) — image_url + audio_url both public (catbox).
Reads the hosted URLs from files. Reports avatar credit cost + seconds."""
from kie_client import run, credits, download
img_url = open("tests/kie/N6_key_cat_url.txt").read().strip()
aud_url = open("tests/kie/N6_vo_url.txt").read().strip()
print("img_url:", img_url)
print("aud_url:", aud_url)
print("bal before:", credits())
r = run("kling/ai-avatar-standard", {
    "image_url": img_url, "audio_url": aud_url,
    "prompt": ("Bentley the red-fawn Boxer puppy speaks warmly and fondly straight to camera with a gentle affectionate "
               "head-tilt; soft natural small-dog mouth movements in time with her words, soulful loving eyes, calm and "
               "tender. Bright daylight on her face, ears stay floppy down, no human teeth.")
}, timeout=900)
download(r["urls"][0], "tests/kie/N6_kie_talk.mp4")
print(f"DONE AVATAR  credits={r['credits']}  secs={r['secs']}  tid={r['tid']}")
print("url:", r["urls"][0])
print("bal after:", credits())
