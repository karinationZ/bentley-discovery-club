#!/usr/bin/env python3
"""Thumbnail base images (no text — text added later via Pillow). 2 compositions to choose from."""
from bentley.shared.kie_client import run, download, credits
BENT = "https://v3b.fal.media/files/b/0a9eb213/K0YEhgC0hRPAknNVA_bSO_Bentley_MASTER_clean_16x9.png"
V = {
 "thumb_v1": ("YouTube thumbnail, 16:9, eye-catching poster composition. Bentley the red-fawn Boxer puppy fills the RIGHT "
   "half of the frame — her face large and close, HUGE wide curious surprised eyes, eyebrows up, a cute tilted head, looking "
   "down toward a magical seashell that GLOWS with warm golden light sitting on a wet rock in the LOWER-LEFT. The UPPER-LEFT "
   "area is open bright sky and soft bokeh (clear, less busy — room for a title). Bright, punchy, HIGH-CONTRAST, vibrant "
   "saturated colors, dramatic warm rim light on Bentley. On-model: black mask, grey chin, white chest blaze, BOTH ears soft "
   "floppy folded DOWN, big soulful expressive eyes, natural dog mouth slightly open in a curious 'ooh' (NO human teeth, NO "
   "grin), teal collar with a small glowing spiral shell charm. Premium dimensional Pixar/Bluey 3D cartoon, poster-quality, "
   "crisp, NOT dark, NOT washed out."),
 "thumb_v2": ("YouTube thumbnail, 16:9, dramatic magical poster composition. Bentley the red-fawn Boxer puppy in the "
   "LOWER-RIGHT, looking UP with huge wide AMAZED sparkling eyes and a tilted head at a big magical spiral SEASHELL that "
   "glows with radiant golden light, light-rays and sparkles, in the UPPER-LEFT of the frame. Strong magical glow, vibrant "
   "saturated colors, HIGH-CONTRAST, bright and exciting, sense of wonder. On-model: black mask, grey chin, white chest "
   "blaze, BOTH ears soft floppy folded DOWN, soulful expressive eyes, natural dog mouth slightly open in wonder (NO human "
   "teeth), teal collar. Premium dimensional Pixar/Bluey 3D cartoon, poster-quality, eye-catching, NOT dark."),
}
if __name__ == "__main__":
    print("bal:", credits())
    for sid, prompt in V.items():
        r = run("google/nano-banana-edit", {"prompt": prompt, "image_urls":[BENT], "image_size":"16:9", "output_format":"png"})
        download(r["urls"][0], f"scratch/kie/{sid}.png")
        print(f"{sid}: {r['credits']}cr {r['secs']}s")
