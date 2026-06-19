#!/usr/bin/env python3
"""Forceful white-sock -> red-fawn paw recolor for specific keyframes.
Usage: .venv/bin/python fix_paws.py <img.png> [<img2.png> ...]
Overwrites in place (back up first). Resumable-safe: just re-run."""
import sys, urllib.request, fal_client
M_EDIT = "fal-ai/nano-banana/edit"
STRONG = (
  "This image is a red-fawn Boxer puppy that WRONGLY has WHITE feet and white lower legs (white socks). "
  "Repaint ALL FOUR feet, every toe, every paw and the entire lower legs to the EXACT same solid rich red-fawn brown fur as the rest of her body. "
  "There must be ZERO white, ZERO cream, ZERO pale or light fur anywhere on her legs, ankles, feet or toes — "
  "each leg is uniformly red-fawn brown from the shoulder/hip all the way down to the toes, perfectly matching her coat color. "
  "Keep EVERYTHING else perfectly identical and unchanged: same pose, same body and proportions, "
  "same soulful well-proportioned eyes (NOT googly, NOT oversized), same floppy folded-DOWN ears, same short docked stubby tail, "
  "same black mask, same small white chest blaze, same teal collar with glowing spiral seashell charm, "
  "same rocks, tide pools, waves, foam, spray and warm dawn lighting. Premium 3D dimensional Pixar soft-fur style, NOT painterly."
)
def fix(path, passes=1):
    url = fal_client.upload_file(path)
    for i in range(passes):
        res = fal_client.subscribe(M_EDIT, arguments={"prompt": STRONG, "image_urls": [url], "aspect_ratio": "16:9"})
        url = res["images"][0]["url"]
        print(f"      pass {i+1} ok", flush=True)
    urllib.request.urlretrieve(url, path)
    print(f"fixed -> {path}", flush=True)
if __name__ == "__main__":
    for p in sys.argv[1:]:
        print(f"[paw-fix] {p}", flush=True); fix(p, passes=1)
