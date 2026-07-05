#!/usr/bin/env python3
"""Contact sheets for the two EP4 design gates (owner pick). Labels each candidate A/B/C/D."""
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

ROOT = Path("/project")


def sheet(indir, out, title, tile_w=640):
    files = sorted(Path(indir).glob("*.png"))
    if not files:
        print(f"(no candidates in {indir})"); return
    ims = []
    for f in files:
        im = Image.open(f).convert("RGB")
        h = int(tile_w * im.height / im.width)
        ims.append((f.stem, im.resize((tile_w, h))))
    cols = 2
    rows = (len(ims) + cols - 1) // cols
    th = max(h for _, i in ims for h in [i.height])
    W, H = cols * tile_w + (cols + 1) * 12, rows * (th + 46) + 60
    s = Image.new("RGB", (W, H), (18, 18, 24))
    d = ImageDraw.Draw(s)
    try:
        f_big = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Rounded Bold.ttf", 30)
        f_lab = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Rounded Bold.ttf", 26)
    except Exception:
        f_big = f_lab = ImageFont.load_default()
    d.text((16, 12), title, font=f_big, fill=(255, 230, 140))
    for i, (name, im) in enumerate(ims):
        x = 12 + (i % cols) * (tile_w + 12)
        y = 60 + (i // cols) * (th + 46)
        s.paste(im, (x, y))
        letter = chr(ord("A") + i)
        d.text((x + 4, y + im.height + 6), f"{letter} — {name}", font=f_lab, fill=(160, 230, 255))
    s.save(out)
    print(f"sheet -> {out} ({len(ims)} candidates)")


sheet(ROOT / "scratch/ep4/design/talking", ROOT / "scratch/ep4/design/TALKING_BENTLEY_PICK.png",
      "GATE 1 — pick ONE Talking Bentley master prop (drives EVERY future talking CU)")
sheet(ROOT / "scratch/ep4/design/mira", ROOT / "scratch/ep4/design/MIRA_PICK.png",
      "GATE 2 — pick ONE Mira the Monarch design (EP4 guest master)")
