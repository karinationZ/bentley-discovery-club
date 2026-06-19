"""Kling AI-Avatar talking / lip-sync shots. Extracted from pipeline.py."""
from bentley.shared.fal import M_AVATAR, fsub


def avatar(image_url, audio_url):
    res = fsub(M_AVATAR, arguments={"image_url": image_url, "audio_url": audio_url})
    return res["video"]["url"]
