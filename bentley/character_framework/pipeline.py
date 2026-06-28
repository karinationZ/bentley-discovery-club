"""Reusable talking-shot production pipeline for the Talking Character framework (KIE backend).

Episode code calls:
  - ``talk(character, vo, out, ...)``          one Kling-Avatar lip-sync shot
  - ``batch(character, items, ...)``           many shots in parallel (hosts the keyframe once)
  - ``derive_keyframe(character, scene, out)`` an in-scene talking keyframe EDITED FROM THE MASTER

The framework supplies the prompt (from rules+anatomy), the master-keyframe default, hosting, retries
and download. Episodes supply only episode-specific inputs (which lines, which scene, VO paths).
"""
import os
import time
from concurrent.futures import ThreadPoolExecutor

from bentley.shared.hosting import catbox_host
from bentley.shared.paths import ROOT
from bentley.character_framework.characters import get
from bentley.character_framework.prompts import talking_prompt

AVATAR_MODEL = "kling/ai-avatar-standard"   # ~40 cr, 720p, audio embedded (mouth == voice)
KEYFRAME_MODEL = "nano-banana-pro"          # best for on-model edits FROM the master


def _kie():
    """Lazy import so the framework (prompts/rules/characters) can be imported without KIE_KEY set —
    only rendering needs the API key."""
    from bentley.shared import kie_client
    return kie_client


def _abs(p):
    p = str(p)
    return p if os.path.isabs(p) else str(ROOT / p)


def talk(character, vo, out, keyframe=None, emotion=None, camera="mcu", prompt=None, retries=8, img_url=None):
    """Render one talking shot. Defaults the keyframe to the character's APPROVED MASTER and the prompt
    to the framework's ``talking_prompt`` (anatomy + rules). Returns credits consumed, or None on failure."""
    char = get(character)
    kf = _abs(keyframe or char.master_keyframe)
    prompt = prompt or talking_prompt(char, emotion=emotion, camera=camera)
    img = img_url or catbox_host(kf)
    aud = catbox_host(_abs(vo))
    for i in range(retries):
        try:
            r = _kie().run(AVATAR_MODEL, {"image_url": img, "audio_url": aud, "prompt": prompt}, timeout=600)
            _kie().download(r["urls"][0], _abs(out))
            return r.get("credits")
        except Exception as e:
            print(f"  [{os.path.basename(str(out))}] try {i+1}: {str(e)[:70]}", flush=True)
            time.sleep(12)
    return None


def batch(character, items, keyframe=None, emotion=None, camera="mcu", workers=4):
    """Render many talking shots in parallel. ``items``: iterable of (vo, out) or (vo, out, emotion).
    Hosts the keyframe ONCE and reuses the URL. Returns list of (out, credits)."""
    char = get(character)
    kf = _abs(keyframe or char.master_keyframe)
    img = catbox_host(kf)

    def run(it):
        vo, out = it[0], it[1]
        emo = it[2] if len(it) > 2 else emotion
        return os.path.basename(str(out)), talk(char, vo, out, keyframe=kf, emotion=emo, camera=camera, img_url=img)

    with ThreadPoolExecutor(max_workers=workers) as ex:
        return list(ex.map(run, list(items)))


def derive_keyframe(character, scene, out, mouth="gently closed, soft and natural (no teeth)",
                    camera="mcu", extra_refs=(), retries=4):
    """Create an in-scene talking keyframe EDITED FROM THE APPROVED MASTER (the consistency rule).

    ``scene``: short description of the setting/pose. ``extra_refs``: extra reference images (e.g. a new
    charm prop) composed in via nano-banana-pro's multi-image input. Returns credits, or None on failure.
    """
    char = get(character)
    refs = [catbox_host(_abs(char.master_keyframe))] + [catbox_host(_abs(r)) for r in extra_refs]
    a = char.anatomy
    collar = f"Keep its {char.collar}. " if char.collar else ""
    prompt = (f"Keep this EXACT {char.descriptor} from the first image — identical face, muzzle, markings, "
              f"proportions, render and style; do NOT redraw or restyle. Place it in this scene: {scene}. "
              f"{a.ban()}. Keep its mouth {mouth}. {collar}No text, no watermark.")
    for i in range(retries):
        try:
            r = _kie().run(KEYFRAME_MODEL, {"prompt": prompt, "image_input": refs,
                                            "aspect_ratio": "16:9", "resolution": "2K", "output_format": "png"})
            _kie().download(r["urls"][0], _abs(out))
            return r.get("credits")
        except Exception as e:
            print(f"  [derive {char.key}] try {i+1}: {str(e)[:70]}", flush=True)
            time.sleep(8)
    return None
