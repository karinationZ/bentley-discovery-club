"""Grid -> mouth-shape sheet cutter — the one-time step when onboarding a character/angle.

Takes a 3x3 labeled viseme grid (generated with our image models from the locked master +
a PLATE FRAME CROP as the angle/lighting reference), NCC-registers every cell to cell 1 on a
stable feature (grid cells drift between generations — fixed boxes fail), cuts TIGHT mouth
patches (a generous crop duplicates the nose on composite), auto-darkens any white tooth-hints
(toothless policy), applies the soft elliptical alpha, and writes the sheet manifest.

    python -m bentley.lipsync.sheet_cutter grid.png out_dir/ \
        --order REST_CLOSED MBP CONS AI E O U FV L \
        --ref-box 0.60 0.28 0.92 0.52 --mouth 0.75 0.645 --half 0.125 0.085 [--mirror]
"""
import argparse
import json
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

from bentley.lipsync.mouth_autotrack import _ncc_best
from bentley.lipsync.visemes import SHAPES

DEFAULT_ORDER = ["REST_CLOSED", "MBP", "CONS", "AI", "E", "O", "U", "FV", "L"]


def cut(grid_path, out_dir, ref_box, mouth_center, patch_half, order=None, mirror=False,
        character="bentley", version=None, ds=3, teeth_policy="toothless v1 (owner-locked)"):
    """ref_box/mouth_center/patch_half are CELL-FRACTION coords measured on cell 1."""
    order = order or DEFAULT_ORDER
    for n in order:
        if n not in SHAPES and n != "OPEN_JAW":
            raise ValueError(f"unknown viseme {n!r} in order")
    im = Image.open(grid_path).convert("RGB")
    w, h = im.size
    cw, ch = w / 3, h / 3
    cells = {}
    for i, name in enumerate(order):
        r, c = divmod(i, 3)
        cells[name] = im.crop((int(c * cw), int(r * ch), int((c + 1) * cw), int((r + 1) * ch)))
    ref = np.asarray(cells[order[0]].convert("L"), dtype=np.float32)[::ds, ::ds]
    nx0, ny0 = int(ref_box[0] * cw), int(ref_box[1] * ch)
    nx1, ny1 = int(ref_box[2] * cw), int(ref_box[3] * ch)
    tpl = ref[ny0 // ds:ny1 // ds, nx0 // ds:nx1 // ds]
    rel = (mouth_center[0] * cw - nx0, mouth_center[1] * ch - ny0)
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    pw, ph = int(patch_half[0] * cw) * 2, int(patch_half[1] * ch) * 2
    shapes, scores = {}, {}
    for name, cell in cells.items():
        g = np.asarray(cell.convert("L"), dtype=np.float32)[::ds, ::ds]
        y, x, s = _ncc_best(g, tpl)
        cx, cy = x * ds + rel[0], y * ds + rel[1]
        patch = cell.crop((int(cx - pw / 2), int(cy - ph / 2),
                           int(cx + pw / 2), int(cy + ph / 2))).convert("RGBA")
        if mirror:
            patch = patch.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
        a = np.asarray(patch).copy()  # toothless enforcement: darken near-white pixels
        r_, g_, b_ = a[:, :, 0].astype(int), a[:, :, 1].astype(int), a[:, :, 2].astype(int)
        white = (r_ > 150) & (g_ > 135) & (b_ > 120) & (abs(r_ - g_) < 45)
        a[:, :, 0][white], a[:, :, 1][white], a[:, :, 2][white] = 40, 18, 16
        patch = Image.fromarray(a)
        mask = Image.new("L", patch.size, 0)
        d = ImageDraw.Draw(mask)
        d.ellipse([patch.width * 0.06, patch.height * 0.06,
                   patch.width * 0.94, patch.height * 0.94], fill=255)
        mask = mask.filter(ImageFilter.GaussianBlur(patch.width * 0.07))
        patch.putalpha(mask)
        patch.save(out / f"{name.lower()}.png")
        shapes[name] = {"file": f"{name.lower()}.png"}
        scores[name] = round(s, 2)
    (out / "manifest.json").write_text(json.dumps(
        {"character": character, "version": version or out.name,
         "coordinate_space": "normalized_mouth_patch", "anchor": {"x": 0.5, "y": 0.5},
         "teeth_policy": teeth_policy, "source_grid": str(grid_path), "mirrored": mirror,
         "registration_scores": scores, "shapes": shapes}, indent=2))
    return out / "manifest.json", scores


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("grid")
    ap.add_argument("out_dir")
    ap.add_argument("--order", nargs=9, default=DEFAULT_ORDER)
    ap.add_argument("--ref-box", nargs=4, type=float, required=True)
    ap.add_argument("--mouth", nargs=2, type=float, required=True)
    ap.add_argument("--half", nargs=2, type=float, default=[0.125, 0.085])
    ap.add_argument("--mirror", action="store_true")
    ap.add_argument("--character", default="bentley")
    a = ap.parse_args(argv)
    m, scores = cut(a.grid, a.out_dir, a.ref_box, a.mouth, a.half, a.order, a.mirror, a.character)
    print(f"sheet -> {m}\nregistration scores: {scores}\n"
          "NOW: build a proof montage and OWNER-approve the sheet before production use.")


if __name__ == "__main__":
    main()
