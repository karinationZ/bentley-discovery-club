"""Magic-Wand variant "chromasoft" — soft low-chroma selection + luminance-preserving
chroma transfer. Zero AI tokens; numpy + PIL only (no scipy).

Idea: "whiteness" of the cream toe-cap is LOW CHROMA (colorfulness), independent of
brightness. Inside each fix box we compute per-pixel chroma C = ||rgb - gray(rgb)||.
  - white/cream cap  -> C low   (recolor these)
  - coat fawn        -> C medium (leave ~unchanged)
  - butterflies      -> C high   (leave)
  - ocean            -> C moderate but BLUE hue -> gate to weight 0 (leave)
Build a SOFT weight w via smoothstep from C_hi down to C_lo (NO hard threshold), zero out
blue pixels, feather with a small separable gaussian blur. Output:
    px = (1-w)*orig + w*recolored
where `recolored` keeps the pixel's own luminance (optionally pulled a little toward coat
luminance) and swaps in the coat's chroma DIRECTION scaled to the coat's chroma magnitude.
"""

import numpy as np
from PIL import Image


# ---- tunables -------------------------------------------------------------
C_LO_FRAC   = 0.16   # chroma below C_LO_FRAC * C_coat  -> full recolor weight
C_HI_FRAC   = 0.62   # chroma above C_HI_FRAC * C_coat  -> zero weight
BLUE_MARGIN = 6.0    # B > R + BLUE_MARGIN  -> ocean, gate out
BLUE_SOFT   = 8.0    # width of the soft blue roll-off
DARK_LO     = 70.0   # luma below DARK_LO -> gate out (butterfly veins/outlines)
DARK_SOFT   = 25.0   # width of the soft dark roll-off
LUMA_PULL   = 0.30   # fraction to pull cap luminance toward coat luminance
CHROMA_GAIN = 1.00   # scale of injected coat chroma (1.0 == coat magnitude)
FEATHER_PX  = 3.0    # gaussian sigma (px) to feather the selection weight
PAD         = 12     # box padding so feather has room and seams vanish
# ---------------------------------------------------------------------------


def _gray(v):
    return v.mean(-1)


def _chroma_norm(v):
    g = _gray(v)
    return np.linalg.norm(v - g[..., None], axis=-1)


def _smoothstep(edge0, edge1, x):
    t = np.clip((x - edge0) / max(edge1 - edge0, 1e-6), 0.0, 1.0)
    return t * t * (3.0 - 2.0 * t)


def _gaussian_blur(img, sigma):
    """Separable gaussian on a float array (H,W) or (H,W,C). numpy-only."""
    if sigma <= 0:
        return img
    radius = max(1, int(round(sigma * 3)))
    xs = np.arange(-radius, radius + 1, dtype=np.float64)
    k = np.exp(-(xs ** 2) / (2 * sigma * sigma))
    k /= k.sum()
    single = img.ndim == 2
    a = img[..., None] if single else img
    # pad reflect to avoid darkening/edge bleed
    ap = np.pad(a, ((radius, radius), (radius, radius), (0, 0)), mode="reflect")
    # horizontal
    tmp = np.zeros_like(a)
    for i, w in enumerate(k):
        tmp += w * ap[radius:radius + a.shape[0], i:i + a.shape[1], :]
    tp = np.pad(tmp, ((radius, radius), (0, 0), (0, 0)), mode="reflect")
    out = np.zeros_like(a)
    for i, w in enumerate(k):
        out += w * tp[i:i + a.shape[0], :, :]
    return out[..., 0] if single else out


def _process_box(arr, box, coat_rgb, coat_gray, coat_chroma_dir, coat_chroma_mag, C_coat):
    H, W = arr.shape[:2]
    x, y, w, h = box
    x0, y0 = max(0, x - PAD), max(0, y - PAD)
    x1, y1 = min(W, x + w + PAD), min(H, y + h + PAD)
    sub = arr[y0:y1, x0:x1].astype(np.float64)

    g = _gray(sub)
    ch = sub - g[..., None]
    C = np.linalg.norm(ch, axis=-1)

    # --- soft low-chroma selection (smoothstep, high->low) ---
    C_lo = C_LO_FRAC * C_coat
    C_hi = C_HI_FRAC * C_coat
    # weight 1 when chroma <= C_lo, 0 when chroma >= C_hi
    w_chroma = 1.0 - _smoothstep(C_lo, C_hi, C)

    # --- blue (ocean) gate: soft roll-off, B over R ---
    R, Bc = sub[..., 0], sub[..., 2]
    blue_excess = Bc - R
    # weight 1 where not-blue, fading to 0 as blue_excess passes BLUE_MARGIN
    w_notblue = 1.0 - _smoothstep(BLUE_MARGIN - BLUE_SOFT, BLUE_MARGIN + BLUE_SOFT, blue_excess)

    # --- dark gate: the cream cap is BRIGHT low-chroma; butterfly outlines/veins
    #     are DARK low-chroma. Protect dark pixels so butterflies survive. ---
    w_bright = _smoothstep(DARK_LO - DARK_SOFT, DARK_LO + DARK_SOFT, g)

    w = w_chroma * w_notblue * w_bright

    # feather so there are no seams / hard edges
    w = _gaussian_blur(w, FEATHER_PX)
    # keep it inside [0,1]; the PAD ring is naturally near-0 (coat/ocean has chroma)
    w = np.clip(w, 0.0, 1.0)[..., None]

    # --- recolor: keep own luminance (pulled toward coat), inject coat chroma dir ---
    own_gray = g[..., None]
    tgt_gray = own_gray * (1.0 - LUMA_PULL) + coat_gray * LUMA_PULL
    recolored = tgt_gray + coat_chroma_dir * (coat_chroma_mag * CHROMA_GAIN)

    out = (1.0 - w) * sub + w * recolored
    arr[y0:y1, x0:x1] = np.clip(out, 0, 255)


def fix(src_path, boxes, coat_xy, out_path):
    """Recolor a wrongly-white toe-cap to the coat's fawn hue.

    src_path : path to the source PNG
    boxes    : iterable of (x, y, w, h) fix boxes (orig-resolution px)
    coat_xy  : (x, y) sample point of correct fawn coat
    out_path : where to write the fixed PNG
    """
    img = Image.open(src_path).convert("RGB")
    arr = np.asarray(img).astype(np.float64)

    cx, cy = coat_xy
    patch = arr[max(0, cy - 8):cy + 9, max(0, cx - 8):cx + 9].reshape(-1, 3)
    coat_rgb = np.median(patch, axis=0)
    coat_gray = float(coat_rgb.mean())
    coat_chroma_vec = coat_rgb - coat_gray
    coat_chroma_mag = float(np.linalg.norm(coat_chroma_vec))
    coat_chroma_dir = coat_chroma_vec / max(coat_chroma_mag, 1e-6)
    C_coat = coat_chroma_mag

    for box in boxes:
        _process_box(arr, box, coat_rgb, coat_gray, coat_chroma_dir,
                     coat_chroma_mag, C_coat)

    out = Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))
    out.save(out_path)
    return out_path


if __name__ == "__main__":
    import os
    SRC = "scratch/ep4/kf_fix/s8_glide_c0.png"
    BOXES = [(1700, 930, 150, 140), (1590, 1030, 110, 110), (1160, 1050, 110, 100)]
    COAT = (1449, 773)
    OUT = os.path.join(os.path.dirname(__file__), "fixed_chromasoft.png")
    fix(SRC, BOXES, COAT, OUT)
    # zoom crop for eyeballing
    z = Image.open(OUT).crop((1500, 900, 1950, 1200))
    z.save(OUT.replace(".png", "_zoom.png"))
    print("wrote", OUT)
