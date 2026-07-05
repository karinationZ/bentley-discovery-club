"""Shared CIELAB color-transfer core for shot_match / plate_match (fix-first tiers 1.5/2).

Reinhard-style statistics transfer: move the target's per-channel LAB mean/std toward the
reference's, with clipped gains (a flat source can't explode) and a strength blend. Pure
numpy — the fix package stays free of OpenCV."""
import numpy as np

_M_RGB2XYZ = np.array([[0.4124564, 0.3575761, 0.1804375],
                       [0.2126729, 0.7151522, 0.0721750],
                       [0.0193339, 0.1191920, 0.9503041]])
_M_XYZ2RGB = np.linalg.inv(_M_RGB2XYZ)
_WHITE = np.array([0.95047, 1.0, 1.08883])
_EPS, _KAPPA = 216 / 24389, 24389 / 27


def srgb_to_lab(rgb):
    """float RGB 0..255 (..,3) -> LAB (L 0..100, a/b roughly -128..127)."""
    c = np.clip(np.asarray(rgb, np.float64), 0, 255) / 255.0
    lin = np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)
    xyz = lin @ _M_RGB2XYZ.T / _WHITE
    f = np.where(xyz > _EPS, np.cbrt(xyz), (_KAPPA * xyz + 16) / 116)
    return np.stack([116 * f[..., 1] - 16,
                     500 * (f[..., 0] - f[..., 1]),
                     200 * (f[..., 1] - f[..., 2])], axis=-1)


def lab_to_srgb(lab):
    L, a, b = lab[..., 0], lab[..., 1], lab[..., 2]
    fy = (L + 16) / 116
    fx, fz = fy + a / 500, fy - b / 200

    def inv(f):
        f3 = f ** 3
        return np.where(f3 > _EPS, f3, (116 * f - 16) / _KAPPA)

    xyz = np.stack([inv(fx), inv(fy), inv(fz)], axis=-1) * _WHITE
    lin = xyz @ _M_XYZ2RGB.T
    c = np.where(lin <= 0.0031308, 12.92 * lin,
                 1.055 * np.clip(lin, 0, None) ** (1 / 2.4) - 0.055)
    return np.clip(c * 255.0, 0, 255)


def lab_stats(rgb, mask=None):
    """(mean3, std3) of the LAB pixels under a bool mask (None = the whole image)."""
    lab = srgb_to_lab(rgb)
    px = lab[mask] if mask is not None else lab.reshape(-1, 3)
    if px.size == 0:
        raise ValueError("empty stats region — check the mask/protect boxes")
    return px.mean(axis=0), px.std(axis=0) + 1e-6


def transfer(rgb, src_stats, ref_stats, strength=1.0, luma_only=False, gain_clip=(0.6, 1.6)):
    """Map rgb so its LAB statistics move from src_stats toward ref_stats. Returns float RGB."""
    (sm, ss), (rm, rs) = src_stats, ref_stats
    gain = np.clip(rs / ss, *gain_clip)
    lab = srgb_to_lab(rgb)
    out = (lab - sm) * gain + rm
    if luma_only:
        out[..., 1:] = lab[..., 1:]
    out = lab * (1.0 - strength) + out * strength
    return lab_to_srgb(out)
