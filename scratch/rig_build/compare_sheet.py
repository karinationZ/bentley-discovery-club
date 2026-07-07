"""Build a labeled side-by-side comparison sheet for the owner sign-off gate.
  python compare_sheet.py OUT.png "LABEL::img.png" "LABEL::img2.png" ...
Each panel is letterboxed to a common height; label bar on top. No deps beyond Pillow.
"""
import sys
from PIL import Image, ImageDraw, ImageFont

H = 620          # panel image height
PAD = 12
BAR = 34


def load_font(size):
    for p in ("/System/Library/Fonts/Supplemental/Arial Bold.ttf",
              "/System/Library/Fonts/Helvetica.ttc"):
        try:
            return ImageFont.truetype(p, size)
        except OSError:
            continue
    return ImageFont.load_default()


def main():
    out = sys.argv[1]
    panels = []
    for spec in sys.argv[2:]:
        label, _, path = spec.partition("::")
        im = Image.open(path).convert("RGB")
        w = max(1, round(im.width * H / im.height))
        panels.append((label, im.resize((w, H), Image.LANCZOS)))

    font = load_font(20)
    total_w = sum(p[1].width for p in panels) + PAD * (len(panels) + 1)
    sheet = Image.new("RGB", (total_w, H + BAR + PAD * 2), (24, 24, 28))
    d = ImageDraw.Draw(sheet)
    x = PAD
    for label, im in panels:
        sheet.paste(im, (x, BAR + PAD))
        tw = d.textlength(label, font=font)
        d.text((x + (im.width - tw) / 2, PAD), label, fill=(240, 236, 220), font=font)
        x += im.width + PAD
    sheet.save(out)
    print(f"sheet -> {out}  ({total_w}x{H + BAR + PAD * 2}, {len(panels)} panels)")


if __name__ == "__main__":
    main()
