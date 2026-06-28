#!/usr/bin/env python3
"""One-shot Bentley identity-lock keyframe test.

Writes only into scratch/ep2/identity_lock_test/. This is a gate test before
touching Ep2 keyframes or motion assets.
"""
import os
import sys
import time
from pathlib import Path

ROOT = Path("/project")
sys.path.insert(0, str(ROOT))

from bentley.shared import kie_client
from bentley.shared.hosting import catbox_host

OUT = ROOT / "scratch/ep2/identity_lock_test"
OUT.mkdir(parents=True, exist_ok=True)

MASTER = ROOT / "assets/character_design/Bentley_MASTER_pixar.png"
TURNAROUND = ROOT / "assets/character_design/Bentley_MODEL_SHEET_turnaround.png"

NEG = (
    "long tail, upright tail, curled tail, white paws, white socks, white toes, "
    "upright ears, pricked ears, pointed ears, adult dog, realistic dog, different breed, "
    "human smile, human teeth, text, watermark, captions"
)

PROMPT = (
    "Create a 16:9 premium 3D animated kids-show keyframe in a sunny tide pool. "
    "Use Bentley, the exact young red-fawn Boxer puppy from the references. "
    "Identity must match the front master exactly: black face mask, grey chin, brown eyes, "
    "floppy folded ears down, teal collar, gold paw-print Bentley tag, white chest blaze, "
    "solid red-fawn paws with no white socks or toes. Use the turnaround reference only for "
    "body anatomy: short docked tail stub, puppy proportions, solid red-fawn legs and paws. "
    "Ignore the shell charm in the turnaround sheet; the gold paw tag from the master is correct. "
    "Scene: Bentley creeps low and curious toward a cute speckled tide-pool rock, one front paw "
    "lifted and reaching to gently boop the rock. Mouth closed and natural. Soft Pixar-like 3D "
    "render, warm shallow water, rocks, anemones, cinematic dawn light."
)

MODELS = [
    (
        "ideogram_character",
        "ideogram/character",
        {
            "prompt": PROMPT,
            "reference_image_urls": None,
            "rendering_speed": "BALANCED",
            "style": "AUTO",
            "expand_prompt": False,
            "num_images": "1",
            "image_size": "landscape_16_9",
            "negative_prompt": NEG,
        },
    ),
    (
        "nano_banana_pro_multiref",
        "nano-banana-pro",
        {
            "prompt": PROMPT + " Preserve the referenced character identity more strongly than the scene.",
            "image_input": None,
            "aspect_ratio": "16:9",
            "resolution": "2K",
            "output_format": "png",
        },
    ),
]


def run_one(label, model, payload, refs):
    payload = dict(payload)
    if "reference_image_urls" in payload:
        payload["reference_image_urls"] = refs
    if "image_input" in payload:
        payload["image_input"] = refs

    for attempt in range(1, 4):
        try:
            print(f"{label}: submitting {model} attempt {attempt}", flush=True)
            result = kie_client.run(model, payload, timeout=900, poll=8)
            for idx, url in enumerate(result["urls"], start=1):
                out = OUT / f"{label}_{idx}.png"
                kie_client.download(url, str(out))
                print(f"{label}: wrote {out} ({result.get('credits')} cr)", flush=True)
            return True
        except Exception as exc:
            print(f"{label}: attempt {attempt} failed: {str(exc)[:180]}", flush=True)
            time.sleep(10)
    return False


def main():
    print("credits before:", kie_client.credits(), flush=True)
    refs = [catbox_host(str(MASTER)), catbox_host(str(TURNAROUND))]
    print("uploaded reference count:", len(refs), flush=True)
    for label, model, payload in MODELS:
        run_one(label, model, payload, refs)
    print("credits after:", kie_client.credits(), flush=True)


if __name__ == "__main__":
    main()
