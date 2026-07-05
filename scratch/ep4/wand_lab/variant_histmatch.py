#!/usr/bin/env python3
"""Magic-Wand white-paw fixer — variant "histmatch".

Approach: local color-distribution normalization toward the coat.

We model the coat's fawn chroma distribution (mean + covariance in YCbCr's Cb,Cr
plane) from a generous set of KNOWN-correct fawn samples (the main coat swatch plus
the fawn parts of the lead paw). Every pixel inside a fix box is scored by how much
it needs correcting toward that distribution:

  * A pixel that is already coat-like (Mahalanobis distance to the coat CbCr blob is
    small) gets weight ~0 -> no change.
  * A pixel on the WHITE / CREAM side of the cap (low chroma magnitude, or warm-but-
    desaturated) gets a high correction weight: its (Cb,Cr) is pulled toward the coat
    mean, and if it is much brighter than the coat it is partially darkened.
  * OCEAN pixels (blue: Cb>Cr, chroma pointing the opposite way from the coat) get
    weight forced to 0.
  * BUTTERFLY pixels (very high chroma, far more saturated than any coat pixel) get
    weight forced to 0.

Everything is per-pixel and smooth (no hard thresholds on the RGB values); the only
"hard" gates are the ocean/butterfly protection multipliers, and even those are soft
sigmoids. A final feathered box mask (cosine-tapered edge + light blur of the weight
field) removes any box seam so the correction blends into surrounding fawn fur. Fur
texture is preserved because we only shift chroma (and gently scale luma) while
keeping each pixel's own Y detail.

Pure numpy + PIL. No scipy, no AI, no network.
"""
import numpy as np
from PIL import Image


# ----------------------------- color helpers ------------------------------- #
def rgb_to_ycc(rgb):
    R, G, B = rgb[..., 0], rgb[..., 1], rgb[..., 2]
    Y = 0.299 * R + 0.587 * G + 0.114 * B
    Cb = 128.0 - 0.168736 * R - 0.331264 * G + 0.5 * B
    Cr = 128.0 + 0.5 * R - 0.418688 * G - 0.081312 * B
    return np.stack([Y, Cb, Cr], -1)


def ycc_to_rgb(ycc):
    Y, Cb, Cr = ycc[..., 0], ycc[..., 1], ycc[..., 2]
    R = Y + 1.402 * (Cr - 128.0)
    G = Y - 0.344136 * (Cb - 128.0) - 0.714136 * (Cr - 128.0)
    B = Y + 1.772 * (Cb - 128.0)
    return np.stack([R, G, B], -1)


def _box_blur(a, radius):
    """Separable box blur via cumulative sums (float, edge-padded). Works on 2-D.

    Returns an array the SAME shape as the input.
    """
    if radius < 1:
        return a
    k = 2 * radius + 1
    # pad only on the axis being processed, so shapes stay clean.
    padh = np.pad(a, ((0, 0), (radius, radius)), mode="edge")
    cs = np.cumsum(padh, axis=1)
    cs = np.pad(cs, ((0, 0), (1, 0)), mode="constant")
    horiz = (cs[:, k:] - cs[:, :-k]) / k          # same shape as `a`

    padv = np.pad(horiz, ((radius, radius), (0, 0)), mode="edge")
    cs = np.cumsum(padv, axis=0)
    cs = np.pad(cs, ((1, 0), (0, 0)), mode="constant")
    out = (cs[k:, :] - cs[:-k, :]) / k            # same shape as `a`
    return out


def _smoothstep(edge0, edge1, x):
    t = np.clip((x - edge0) / (edge1 - edge0 + 1e-9), 0.0, 1.0)
    return t * t * (3.0 - 2.0 * t)


# ------------------------------- main fix ---------------------------------- #
def fix(src_path, boxes, coat_xy, out_path):
    img = Image.open(src_path).convert("RGB")
    arr = np.asarray(img).astype(np.float64)
    H, W, _ = arr.shape
    out = arr.copy()

    # --- 1. model the coat fawn distribution (mean + cov in Cb,Cr) --------- #
    cx, cy = coat_xy
    fawn_swatches = []

    def grab(x, y, w, h):
        x0, y0 = max(0, x), max(0, y)
        x1, y1 = min(W, x + w), min(H, y + h)
        if x1 > x0 and y1 > y0:
            fawn_swatches.append(arr[y0:y1, x0:x1].reshape(-1, 3))

    # generous main coat patch around the sample point
    grab(cx - 22, cy - 22, 44, 44)
    # fawn parts of the lead paw (VERIFIED fawn, adjacent to the cap — do NOT
    # sample the lower paw area near 1730,1052: that is ocean, not fur).
    grab(1705, 940, 50, 40)     # coat_ctl fawn on the paw
    grab(1735, 995, 30, 25)     # verified fawn spot near the toe
    grab(1775, 995, 30, 25)     # verified fawn spot near the toe
    coat_px = np.concatenate(fawn_swatches, 0)
    coat_ycc = rgb_to_ycc(coat_px)

    # robust guard against any stray non-fawn (blue) pixels that slipped into
    # the swatches: keep only warm pixels (Cr > Cb, i.e. R-leaning fawn).
    warm_mask = coat_ycc[:, 2] > coat_ycc[:, 1]
    if warm_mask.sum() > 50:
        coat_ycc = coat_ycc[warm_mask]

    coat_Y = float(np.median(coat_ycc[:, 0]))
    mu = coat_ycc[:, 1:].mean(0)                 # [Cb, Cr] mean
    cov = np.cov(coat_ycc[:, 1:].T)
    cov = cov + np.eye(2) * 4.0                  # regularize (avoid singular / too tight)
    inv = np.linalg.inv(cov)
    # coat chroma direction (unit vector from neutral 128,128 toward coat mean)
    coat_dir = mu - 128.0
    coat_dir_n = coat_dir / (np.linalg.norm(coat_dir) + 1e-9)
    coat_chroma_mag = float(np.linalg.norm(coat_dir))

    # spread of coat chroma magnitude (to know what "over-saturated" means).
    coat_mags = np.linalg.norm(coat_ycc[:, 1:] - 128.0, axis=1)
    coat_mag_med = float(np.median(coat_mags))
    coat_mag_hi = float(np.percentile(coat_mags, 75))     # robust "typical high" fawn chroma
    # coat Cr range (butterflies are extreme-Cr orange, well past the coat)
    coat_Cr_hi = float(np.percentile(coat_ycc[:, 2], 92))
    coat_Y_hi = float(np.percentile(coat_ycc[:, 0], 92))

    # --- 2. process each fix box ------------------------------------------- #
    for (bx, by, bw, bh) in boxes:
        x0, y0 = max(0, bx), max(0, by)
        x1, y1 = min(W, bx + bw), min(H, by + bh)
        if x1 <= x0 or y1 <= y0:
            continue
        sub = arr[y0:y1, x0:x1]                  # (h,w,3)
        ycc = rgb_to_ycc(sub)
        Y = ycc[..., 0]
        Cb = ycc[..., 1]
        Cr = ycc[..., 2]
        chroma = np.stack([Cb, Cr], -1)          # (h,w,2)
        d = chroma - mu                          # deviation from coat mean

        # Mahalanobis distance to coat blob (how far from being coat-colored)
        maha = np.sqrt(np.einsum("...i,ij,...j->...", d, inv, d) + 1e-9)

        cvec = chroma - 128.0
        cmag = np.linalg.norm(cvec, axis=-1)
        # cosine alignment with the coat direction (+1 warm/fawn, -1 blue/ocean)
        align = (cvec @ coat_dir_n) / (cmag + 1e-6)

        # --- correction NEED -------------------------------------------------
        # The white/cream cap is a WASHED-OUT version of fawn: its chroma is
        # DESATURATED relative to the coat (drawn toward neutral by the white),
        # while its hue stays warm. So "needs correcting" = warm-ish hue AND
        # chroma below the coat's typical level AND off the coat blob (maha).
        # This deliberately does NOT fire on saturated butterfly wings (their
        # chroma is ABOVE the coat) nor on ocean (wrong hue, handled below).
        desat = 1.0 - _smoothstep(coat_mag_med * 0.55, coat_mag_hi, cmag)
        off_coat = _smoothstep(1.6, 5.0, maha)
        need = desat * off_coat

        # --- protection multipliers (soft, coat-derived, no RGB thresholds) --
        # OCEAN: blue -> chroma points AWAY from the coat (align negative).
        ocean_keep = _smoothstep(-0.10, 0.55, align)   # 0 for ocean, 1 for warm

        # BUTTERFLY / over-saturated warm px: chroma magnitude above the coat.
        sat_keep = 1.0 - _smoothstep(coat_mag_hi + 4.0, coat_mag_hi + 26.0, cmag)
        # extra butterfly guard: extreme-Cr orange beyond the coat's Cr range.
        cr_keep = 1.0 - _smoothstep(coat_Cr_hi + 4.0, coat_Cr_hi + 24.0, Cr)

        weight = need * ocean_keep * sat_keep * cr_keep   # (h,w) in [0,1]

        # --- feathered box mask to kill seams ------------------------------ #
        h, w = weight.shape
        yy = (np.arange(h) + 0.5) / h
        xx = (np.arange(w) + 0.5) / w
        fedge = max(4, int(round(0.16 * min(h, w))))  # feather width in px
        fx = np.minimum(_smoothstep(0, fedge / w, xx),
                        _smoothstep(0, fedge / w, 1.0 - xx))
        fy = np.minimum(_smoothstep(0, fedge / h, yy),
                        _smoothstep(0, fedge / h, 1.0 - yy))
        feather = np.outer(fy, fx)
        weight = weight * feather

        # smooth the weight field so there are no per-pixel speckles / seams
        weight = _box_blur(weight, radius=3)
        weight = np.clip(weight, 0.0, 1.0)

        # --- remap chroma toward coat mean, weighted ----------------------- #
        new_Cb = Cb + weight * (mu[0] - Cb)
        new_Cr = Cr + weight * (mu[1] - Cr)

        # gently pull luma toward coat luma ONLY for pixels whose local mean is
        # well above the coat's bright end (the cream/white part). Preserve
        # local Y texture by shifting only the LOW-frequency luma offset.
        Y_lo = _box_blur(Y, radius=6)
        Y_hi = Y - Y_lo                              # texture / detail (kept)
        over = _smoothstep(coat_Y_hi, coat_Y_hi + 55.0, Y_lo)
        lum_pull = weight * over * 0.40              # partial darken, keep it sane
        new_Y_lo = Y_lo + lum_pull * (coat_Y - Y_lo)
        new_Y = new_Y_lo + Y_hi                      # re-add preserved texture

        new_ycc = np.stack([new_Y, new_Cb, new_Cr], -1)
        new_rgb = ycc_to_rgb(new_ycc)
        out[y0:y1, x0:x1] = new_rgb

    out = np.clip(out, 0, 255).astype(np.uint8)
    Image.fromarray(out).save(out_path)
    return out_path


# --------------------------------- CLI ------------------------------------- #
if __name__ == "__main__":
    SRC = "scratch/ep4/kf_fix/s8_glide_c0.png"
    COAT = (1449, 773)
    BOXES = [(1700, 930, 150, 140), (1590, 1030, 110, 110), (1160, 1050, 110, 100)]
    OUT = "scratch/ep4/wand_lab/fixed_histmatch.png"
    fix(SRC, BOXES, COAT, OUT)

    # zoom crop for visual inspection
    z = Image.open(OUT).convert("RGB").crop((1500, 900, 1950, 1200))
    z.save("scratch/ep4/wand_lab/fixed_histmatch_zoom.png")
    print("wrote", OUT)
