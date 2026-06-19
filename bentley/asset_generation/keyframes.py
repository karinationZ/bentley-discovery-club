"""Keyframe generation (Nano-Banana via fal) + paw recolor. Extracted from pipeline.py."""
from bentley.shared.fal import M_EDIT, M_T2I, REFS, fsub

# Global style/setting suffix appended to every keyframe prompt (locked-design rule).
ENV = (" Setting: the same Crystal Cove tide pool — wet black volcanic rocks and glassy pools at golden dawn, "
       "NOT a sandy beach. Consistent premium 3D dimensional Pixar soft-fur style, matching warm lighting and color across every shot, NOT painterly, NOT flat.")


def keyframe(prompt, ref_key=None):
    p = prompt + ENV
    if ref_key:
        res = fsub(M_EDIT, arguments={"prompt": p, "image_urls": [REFS[ref_key]], "aspect_ratio": "16:9"})
    else:
        res = fsub(M_T2I, arguments={"prompt": p, "aspect_ratio": "16:9"})
    return res["images"][0]["url"]


def paw_fix(image_url):
    p = ("Recolor ONLY the dog's paws and lower legs to SOLID rich red-fawn fur exactly matching the body, "
         "completely removing all white and cream from the feet, toes and paws. Keep everything else identical: "
         "same pose, body, both floppy folded-down ears, short tail, teal collar with seashell charm, rocks, water and lighting.")
    res = fsub(M_EDIT, arguments={"prompt": p, "image_urls": [image_url], "aspect_ratio": "16:9"})
    return res["images"][0]["url"]
