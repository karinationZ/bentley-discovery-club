"""Composite a mouth patch into a plate frame so it doesn't read as a sticker (plan Phase 4,
minimal pass pulled into Phase 3 per review): soft alpha feather + local color match."""
import numpy as np
from PIL import Image, ImageFilter


def _feather(patch, radius=3):
    """Soften the patch's alpha edge so it blends into muzzle fur."""
    a = patch.getchannel("A").filter(ImageFilter.GaussianBlur(radius))
    out = patch.copy()
    out.putalpha(a)
    return out


def _color_match(patch, plate, box, strength=0.5):
    """Shift the patch's mean RGB toward the plate region it covers (local lighting match)."""
    region = np.asarray(plate.crop(box).convert("RGB"), dtype=np.float32)
    p = np.asarray(patch.convert("RGBA"), dtype=np.float32)
    mask = p[:, :, 3:4] / 255.0
    if mask.sum() < 1:
        return patch
    p_mean = (p[:, :, :3] * mask).sum((0, 1)) / mask.sum()
    shift = (region.reshape(-1, 3).mean(0) - p_mean) * strength
    p[:, :, :3] = np.clip(p[:, :, :3] + shift, 0, 255)
    return Image.fromarray(p.astype(np.uint8), "RGBA")


def place_patch(plate, patch, pos, anchor, feather=3, match=0.5):
    """Place a shape patch on the plate. pos={x,y,scale,rotation_deg}; anchor=(ax,ay) normalized
    point of the patch that sits at (x,y). Returns the composited RGB frame."""
    if abs(pos.get("rotation_deg", 0.0)) > 0.1:
        patch = patch.rotate(-pos["rotation_deg"], expand=True,
                             resample=Image.Resampling.BICUBIC)
    px = int(round(pos["x"] - anchor[0] * patch.width))
    py = int(round(pos["y"] - anchor[1] * patch.height))
    box = (px, py, px + patch.width, py + patch.height)
    patch = _color_match(patch, plate, box, match)
    patch = _feather(patch, feather)
    out = plate.convert("RGBA")
    out.alpha_composite(patch, (px, py))
    return out.convert("RGB")
