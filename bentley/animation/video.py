"""Kling image-to-video motion shots. Extracted from pipeline.py."""
from bentley.shared.fal import M_VIDEO, fsub


def video(image_url, prompt, dur="5"):
    p = prompt + (" Keep the consistent 3D dimensional Pixar soft-fur style and warm dawn lighting throughout, NOT painterly. "
                  "Water must actually MOVE — ripples, foam, gentle wave motion; subtle natural character motion (breathing, blinking, small shifts).")
    res = fsub(M_VIDEO, arguments={"prompt": p, "image_url": image_url, "duration": dur, "aspect_ratio": "16:9"})
    return res["video"]["url"]
