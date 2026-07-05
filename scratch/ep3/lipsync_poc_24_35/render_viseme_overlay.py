#!/usr/bin/env python3
"""Rhubarb-driven toothless mouth overlay for EP3 00:24-00:35.

This is intentionally a plate-preserving experiment: it does not alter EP3 v8.
It covers the generated human-looking teeth with a soft, dark dog-mouth shape
whose openness follows Rhubarb Preston-Blair cues for the two Bentley lines in
this exact clip window.
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter


ROOT = Path(__file__).resolve().parent
FRAMES = ROOT / "frames"
OUT = ROOT / "rendered"
OUT.mkdir(exist_ok=True)

FPS = 24
CLIP_START = 24.0
CLIP_DUR = 11.0

# Global starts from episodes/ep3/assemble_v2.py timing for v8 sections.
LINES = [
    ("B_findline", 19.58),
    ("B_tooheavy", 28.76),
]

OPEN = {
    "X": 0.00,
    "A": 0.10,
    "B": 0.30,
    "C": 0.50,
    "D": 0.92,
    "E": 0.78,
    "F": 0.42,
    "G": 0.34,
    "H": 0.55,
}


def load_cues() -> list[dict]:
    cues: list[dict] = []
    for label, global_start in LINES:
        data = json.loads((ROOT / "cues" / f"{label}.json").read_text())
        shift = global_start - CLIP_START
        for cue in data["mouthCues"]:
            start = cue["start"] + shift
            end = cue["end"] + shift
            if end <= 0 or start >= CLIP_DUR:
                continue
            cues.append(
                {
                    "start": max(0.0, start),
                    "end": min(CLIP_DUR, end),
                    "value": cue["value"],
                    "label": label,
                }
            )
    return sorted(cues, key=lambda c: c["start"])


CUES = load_cues()


def cue_value_at(t: float) -> str:
    for cue in CUES:
        if cue["start"] <= t < cue["end"]:
            return cue["value"]
    return "X"


def smooth_open(t: float) -> float:
    """Blend current/neighbor cues slightly so the overlay doesn't chatter."""
    value = OPEN.get(cue_value_at(t), 0.0)
    prev_v = OPEN.get(cue_value_at(max(0.0, t - 1 / FPS)), 0.0)
    next_v = OPEN.get(cue_value_at(min(CLIP_DUR, t + 1 / FPS)), 0.0)
    return value * 0.62 + prev_v * 0.19 + next_v * 0.19


def estimate_mouth_center(base: Image.Image) -> tuple[int, int]:
    """Find the existing mouth/tongue/teeth area so the patch follows the plate."""
    arr = np.asarray(base.convert("RGB"))
    y0, y1, x0, x1 = 500, 585, 535, 700
    roi = arr[y0:y1, x0:x1]
    r, g, b = roi[:, :, 0], roi[:, :, 1], roi[:, :, 2]
    yy, _ = np.indices(r.shape)
    red_mouth = (r > 85) & (g < 70) & (b < 75) & (r > g * 1.5)
    pale_teeth = (r > 165) & (g > 145) & (b > 120) & (yy > 20) & (yy < 70)
    ys, xs = np.where(red_mouth | pale_teeth)
    if len(xs) < 120:
        return 624, 548
    cx = int(x0 + (xs.min() + xs.max()) / 2)
    cy = int(y0 + (ys.min() + ys.max()) / 2)
    return max(600, min(646, cx)), max(536, min(558, cy))


def paint_out_teeth(im: Image.Image, base: Image.Image) -> None:
    """Remove human-tooth highlights while leaving surrounding muzzle intact."""
    arr = np.asarray(base.convert("RGB"))
    y0, y1, x0, x1 = 510, 586, 535, 705
    roi = arr[y0:y1, x0:x1]
    r, g, b = roi[:, :, 0], roi[:, :, 1], roi[:, :, 2]
    yy, _ = np.indices(r.shape)
    pale = (r > 145) & (g > 120) & (b > 95) & (yy > 12)
    if pale.sum() < 8:
        return
    mask_arr = np.zeros((im.height, im.width), dtype=np.uint8)
    mask_arr[y0:y1, x0:x1][pale] = 255
    mask = Image.fromarray(mask_arr, "L").filter(ImageFilter.MaxFilter(9)).filter(ImageFilter.GaussianBlur(2.0))
    cover = Image.new("RGBA", im.size, (18, 8, 6, 232))
    im.alpha_composite(Image.composite(cover, Image.new("RGBA", im.size, (0, 0, 0, 0)), mask))


def draw_mouth(base: Image.Image, t: float) -> Image.Image:
    im = base.convert("RGBA")
    o = smooth_open(t)
    paint_out_teeth(im, base)

    # The v8 plate is very stable in this window. Coordinates are tuned to the
    # real muzzle in the 1280x720 frames and avoid teeth by drawing only a dark
    # inner-mouth shape, never white highlights.
    cx, cy = estimate_mouth_center(base)
    width = 58 + int(48 * o)
    height = 3 + int(46 * o)
    slant = -5

    patch = Image.new("RGBA", im.size, (0, 0, 0, 0))
    mask = Image.new("L", im.size, 0)
    md = ImageDraw.Draw(mask)

    # Softly darken the existing mouth pixels only while Bentley is speaking.
    # This hides generated teeth without creating a rectangular patch.
    speaking = 1.0 if o > 0.03 else 0.0
    md.rounded_rectangle(
        [cx - 62, cy - 15, cx + 66, cy + 29],
        radius=18,
        fill=int(175 * speaking),
    )

    # Viseme mouth: a sideways rounded oval following the muzzle angle.
    box = [cx - width // 2, cy - height // 2, cx + width // 2, cy + height // 2]
    mouth_mask = Image.new("L", im.size, 0)
    dd = ImageDraw.Draw(mouth_mask)
    dd.ellipse(box, fill=220)
    if height <= 11:
        dd.rounded_rectangle(
            [cx - width // 2, cy - 2, cx + width // 2, cy + 3],
            radius=3,
            fill=235,
        )
    mouth_mask = mouth_mask.rotate(slant, center=(cx, cy), resample=Image.Resampling.BICUBIC)
    mask = Image.composite(Image.new("L", im.size, 245), mask, mouth_mask)

    mask = mask.filter(ImageFilter.GaussianBlur(3.2))
    pd = ImageDraw.Draw(patch)
    pd.bitmap((0, 0), mask, fill=(10, 6, 5, 244))

    # A tiny lower-lip shadow sells the muzzle without introducing teeth.
    lip = Image.new("RGBA", im.size, (0, 0, 0, 0))
    ld = ImageDraw.Draw(lip)
    ld.arc(
        [cx - width // 2 - 4, cy - height // 2 - 1, cx + width // 2 + 4, cy + height // 2 + 11],
        start=15,
        end=170,
        fill=(76, 35, 25, 96),
        width=2,
    )
    lip = lip.filter(ImageFilter.GaussianBlur(0.8))

    im.alpha_composite(patch)
    im.alpha_composite(lip)
    return im.convert("RGB")


def main() -> None:
    frames = sorted(FRAMES.glob("f_*.png"))
    for idx, frame in enumerate(frames):
        t = idx / FPS
        out = OUT / frame.name
        draw_mouth(Image.open(frame), t).save(out)
    (ROOT / "combined_cues.json").write_text(json.dumps(CUES, indent=2))
    print(f"rendered {len(frames)} frames -> {OUT}")


if __name__ == "__main__":
    main()
