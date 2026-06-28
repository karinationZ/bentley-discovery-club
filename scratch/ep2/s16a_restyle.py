#!/usr/bin/env python3
"""Re-do s16a_colorgame: keep the good proportion but LOCK the 3D render style (it drifted to flat 2D illustration).
Nano Banana Pro, lock-to-reference both chars. Run: KIE_KEY=... python3 scratch/ep2/s16a_restyle.py
"""
import sys, os, time
ROOT = "/project"
sys.path.insert(0, ROOT)
from bentley.shared import kie_client
INDI_URL = open(f"{ROOT}/assets/character_design/.indi_locked_url.txt").read().strip()
BENT_URL = "https://files.catbox.moe/21y33x.png"
OUT = f"{ROOT}/scratch/ep2/hero_v2/s16a_colorgame.png"

PROMPT = ("Combine the two reference images into one scene at a bright, colorful tide pool, rendered as a PREMIUM DIMENSIONAL "
  "3D CGI ANIMATION (Pixar / Bluey style — soft dimensional fur, realistic 3D depth and lighting). Keep BENTLEY (first image — "
  "red-fawn Boxer puppy with her gold paw-print 'Bentley' name tag, floppy ears, teal collar, SOLID red-fawn legs and paws "
  "with NO white socks) and INDI (second image — small "
  "purple octopus with teal eyes and ocelli) EXACTLY as they are; do not redraw either face. PROPORTION: Indi's round "
  "head/body (mantle) is about the same size as Bentley's HEAD — clearly smaller than the dog, not tiny; her arms extend out. "
  "POSE: a delighted Bentley (whole face in frame) beside Indi, who is playfully turning a few RED-FAWN patches across her "
  "purple skin to 'match' her friend (keep her teal eyes + ocelli); both happy and bonding. Clean, sharp, no grain. "
  "Match a realistic, dimensional, high-end 3D animated-film look (like the other shots in this set). "
  "NEGATIVE: flat 2D, 2D illustration, painterly, storybook drawing, cel-shaded, cartoon outline, overly flat toony cartoon, "
  "white socks, white paws, white feet, white toes, redrawing the octopus, eyebrows or nose on octopus, octopus bigger than "
  "the dog's head, giant octopus, tiny octopus, cropped dog face, human teeth, film grain.")

def runpro(tries=4):
    for i in range(tries):
        try:
            return kie_client.run("nano-banana-pro",
                {"prompt": PROMPT, "image_input": [BENT_URL, INDI_URL], "aspect_ratio": "16:9", "resolution": "2K", "output_format": "png"})
        except Exception as e:
            print(f"  attempt {i+1}: {str(e)[:80]}"); time.sleep(6)
    return None

print("bal before:", kie_client.credits())
r = runpro()
if r:
    kie_client.download(r["urls"][0], OUT); print(f"s16a re-done: {r.get('credits')}cr {r.get('secs')}s -> {OUT}")
else:
    print("FAILED")
print("bal after:", kie_client.credits())
