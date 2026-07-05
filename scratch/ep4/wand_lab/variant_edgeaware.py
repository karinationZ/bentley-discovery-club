"""Magic-Wand white-paw fixer — variant "edgeaware".

Zero-AI, numpy+PIL only. The selection is built as a smooth field that respects
image edges: start from confident white/cream seeds inside the fix boxes, then
propagate the selection weight through each box with an edge-aware iterative
diffusion. Each iteration is a cheap box-blur of the weight map multiplied by a
per-pixel affinity term derived from the local colour-gradient magnitude — the
weight cannot flow across strong edges. Blue (ocean) and high-chroma (orange
butterfly) pixels are hard barriers (affinity 0). Finally the white cap is
recoloured under the resulting soft mask, preserving per-pixel luminance texture
and pulling chroma toward the coat with a gentle luminance pull.

Public API:  fix(src_path, boxes, coat_xy, out_path)
"""
from __future__ import annotations

import numpy as np
from PIL import Image


# ----------------------------------------------------------------------------- helpers
def _box_blur(a: np.ndarray, radius: int = 1) -> np.ndarray:
    """Separable mean filter via cumulative sums. Works on 2-D float arrays.
    Edge handling: clamp (reflect-free) — good enough for a small box crop."""
    if radius < 1:
        return a
    k = 2 * radius + 1
    # pad by replicating edges so the window is well defined near borders
    pad = np.pad(a, radius, mode="edge")
    # horizontal
    cs = np.cumsum(pad, axis=1)
    cs = np.pad(cs, ((0, 0), (1, 0)), mode="constant")
    horiz = (cs[:, k:] - cs[:, :-k]) / k
    # vertical
    cs = np.cumsum(horiz, axis=0)
    cs = np.pad(cs, ((1, 0), (0, 0)), mode="constant")
    out = (cs[k:, :] - cs[:-k, :]) / k
    return out


def _grad_mag(gray: np.ndarray) -> np.ndarray:
    """Local gradient magnitude of a 2-D array via central differences."""
    gy = np.zeros_like(gray)
    gx = np.zeros_like(gray)
    gy[1:-1, :] = (gray[2:, :] - gray[:-2, :]) * 0.5
    gx[:, 1:-1] = (gray[:, 2:] - gray[:, :-2]) * 0.5
    return np.sqrt(gx * gx + gy * gy)


def _smoothstep(x: np.ndarray, lo: float, hi: float) -> np.ndarray:
    t = np.clip((x - lo) / max(hi - lo, 1e-6), 0.0, 1.0)
    return t * t * (3.0 - 2.0 * t)


# ----------------------------------------------------------------------------- core
def _process_box(img: np.ndarray, box, coat_rgb: np.ndarray) -> None:
    """Recolour the white cap inside one box, in place, on `img` (float H,W,3)."""
    x, y, w, h = box
    H, W = img.shape[:2]
    x0, y0 = max(0, x), max(0, y)
    x1, y1 = min(W, x + w), min(H, y + h)
    if x1 <= x0 or y1 <= y0:
        return
    crop = img[y0:y1, x0:x1]  # view
    c = crop.astype(np.float64)

    r, g, b = c[..., 0], c[..., 1], c[..., 2]
    gray = c.mean(-1)
    gmn = c.min(-1)
    gmx = c.max(-1)
    sat = gmx - gmn                       # 0 = neutral, big = colourful
    warm = r - b                          # >0 warm (fur), <0 blue (ocean)
    chroma = c - gray[..., None]
    chroma_mag = np.linalg.norm(chroma, axis=-1)

    coat_gray = float(coat_rgb.mean())
    coat_chroma = coat_rgb - coat_gray
    coat_cmag = float(np.linalg.norm(coat_chroma))

    # ---- confident white/cream seeds -------------------------------------
    # The wrong toe-cap is bright, desaturated and NOT blue. Coat fawn is warm
    # but SATURATED; ocean is blue; butterfly is very high chroma. Seeds are the
    # intersection of "bright" and "low saturation" and "not blue".
    seed = (
        (gray > 132.0)
        & (sat < 82.0)
        & (warm > -6.0)
        & (chroma_mag < 62.0)
    ).astype(np.float64)

    # ---- hard diffusion barriers -----------------------------------------
    # Ocean (blue) and butterfly (very high chroma / very saturated) must never
    # be reached by the growing selection.
    blue = warm < -8.0
    hot = (chroma_mag > 95.0) | (sat > 120.0)
    barrier = blue | hot

    # ---- edge-aware affinity field ---------------------------------------
    # Affinity is high in flat fur, low across strong colour edges. Built from
    # the gradient magnitude of luminance + chroma channels.
    gm = _grad_mag(gray) + _grad_mag(warm) + _grad_mag(g - b)
    gm = _box_blur(gm, 1)
    # normalise to a soft affinity in (0,1]; strong edges -> ~0
    affinity = np.exp(-(gm * gm) / (2.0 * (18.0 ** 2)))
    affinity[barrier] = 0.0

    # ---- iterative edge-aware diffusion ----------------------------------
    weight = seed.copy()
    for _ in range(60):
        weight = _box_blur(weight, 1) * affinity
        # keep confident seeds pinned so the field has a source to grow from
        weight = np.maximum(weight, seed)
        weight[barrier] = 0.0
    # a couple of extra plain smoothing passes to remove any residual graininess
    for _ in range(2):
        weight = _box_blur(weight, 1)
        weight[barrier] = 0.0

    # normalise & shape into a soft alpha mask
    if weight.max() > 1e-6:
        weight = weight / weight.max()
    mask = _smoothstep(weight, 0.12, 0.6)
    # never touch the barriers even after smoothing
    mask[barrier] = 0.0

    if mask.max() < 1e-6:
        return

    # ---- recolour under the soft mask ------------------------------------
    # Preserve each pixel's own luminance texture; give it the coat's chroma
    # direction scaled to a sensible magnitude, plus a gentle luminance pull
    # toward the coat so the cap doesn't read as a bright blob.
    unit_coat = coat_chroma / (coat_cmag + 1e-6)

    # target chroma magnitude per pixel: blend the pixel's own chroma strength
    # toward the coat's, so shaded parts stay shaded.
    px_cmag = chroma_mag
    tgt_cmag = 0.45 * px_cmag + 0.55 * coat_cmag
    tgt_cmag = np.clip(tgt_cmag, 0.0, coat_cmag * 1.35)

    new_chroma = unit_coat[None, None, :] * tgt_cmag[..., None]

    # luminance: pull toward the coat luminance, keeping local variation. The
    # pull is ADAPTIVE — the brighter (more clearly "wrong cream") a pixel is
    # above the coat's own luminance, the harder it is pulled down, so the pale
    # cap loses its blob-brightness while shaded fur is barely touched.
    px_gray = gray
    over = np.clip((px_gray - coat_gray) / 90.0, 0.0, 1.0)  # 0 at coat, 1 far above
    pull = 0.22 + 0.45 * over                               # 0.22..0.67
    tgt_gray = (1.0 - pull) * px_gray + pull * coat_gray
    recolored = tgt_gray[..., None] + new_chroma

    m3 = mask[..., None]
    blended = c * (1.0 - m3) + recolored * m3
    crop[...] = np.clip(blended, 0, 255).astype(img.dtype)


def fix(src_path: str, boxes, coat_xy, out_path: str) -> str:
    """Recolour wrong white toe-cap(s) inside `boxes` to match the coat.

    boxes:   iterable of (x, y, w, h) in original-image pixels.
    coat_xy: (x, y) of a clean fawn coat sample.
    """
    im = Image.open(src_path).convert("RGB")
    arr = np.asarray(im).astype(np.uint8).copy()

    cx, cy = coat_xy
    H, W = arr.shape[:2]
    sx0, sy0 = max(0, cx - 8), max(0, cy - 8)
    sx1, sy1 = min(W, cx + 9), min(H, cy + 9)
    coat_rgb = np.median(
        arr[sy0:sy1, sx0:sx1].reshape(-1, 3).astype(np.float64), axis=0
    )

    for box in boxes:
        _process_box(arr, box, coat_rgb)

    Image.fromarray(arr, "RGB").save(out_path)
    return out_path


if __name__ == "__main__":
    import os

    HERE = os.path.dirname(os.path.abspath(__file__))
    ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
    SRC = os.path.join(ROOT, "scratch/ep4/kf_fix/s8_glide_c0.png")
    OUT = os.path.join(HERE, "fixed_edgeaware.png")
    BOXES = [(1700, 930, 150, 140), (1590, 1030, 110, 110), (1160, 1050, 110, 100)]
    COAT = (1449, 773)
    fix(SRC, BOXES, COAT, OUT)

    # zoom crop (1500,900)-(1950,1200)
    z = np.asarray(Image.open(OUT).convert("RGB"))[900:1200, 1500:1950]
    Image.fromarray(z).save(OUT.replace(".png", "_zoom.png"))
    print("wrote", OUT)
