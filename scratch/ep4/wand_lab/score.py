#!/usr/bin/env python3
"""Magic-Wand bake-off scorer — SAME yardstick for every variant.
Target asset: scratch/ep4/kf_fix/s8_glide_c0.png (subtle cream toe-cap gradient, butterflies+ocean
adjacent — the hard real case). Regions (orig px):
  CAP       (1720,935,105,85)   defect: must become fawn (chroma toward coat, brightness sane)
  BUTTERFLY (1600,1080,60,50)   control INSIDE a fix box: must NOT change
  OCEAN     (1815,1035,30,30)   control INSIDE a fix box: must NOT change
  COAT      (1705,940,50,40)    proper fawn inside box: near-no-op
Pass: cap_fawn_sim >= 0.90 AND cap_bright_ratio in [0.95,1.5] AND butterfly/ocean delta < 2.5
AND coat delta < 8 AND cap texture std in [0.4,1.6]x of before.
Usage: python3 score.py FIXED.png"""
import json, sys
import numpy as np
from PIL import Image

SRC = "scratch/ep4/kf_fix/s8_glide_c0.png"
COAT_XY = (1449, 773)
R = {"cap": (1720, 935, 105, 85), "butterfly": (1600, 1080, 60, 50),
     "ocean": (1815, 1035, 30, 30), "coat_ctl": (1705, 940, 50, 40)}


def crop(a, r):
    x, y, w, h = r
    return a[y:y+h, x:x+w].astype(np.float64)


def fawn_sim(region, coat):
    """Mean cosine similarity of chroma vectors (rgb minus own gray) vs the coat's."""
    def chroma(v):
        g = v.mean(-1, keepdims=True)
        return v - g
    c = chroma(region.reshape(-1, 3))
    k = chroma(coat[None, :])[0]
    denom = (np.linalg.norm(c, axis=1) * np.linalg.norm(k) + 1e-6)
    sim = (c @ k) / denom
    return float(np.median(sim))


def main(fixed_path):
    a = np.asarray(Image.open(SRC).convert("RGB"))
    b = np.asarray(Image.open(fixed_path).convert("RGB"))
    assert a.shape == b.shape, "size mismatch"
    coat = np.median(crop(a, (COAT_XY[0]-8, COAT_XY[1]-8, 17, 17)).reshape(-1, 3), axis=0)
    capA, capB = crop(a, R["cap"]), crop(b, R["cap"])
    res = {
        "cap_fawn_sim_before": round(fawn_sim(capA, coat), 3),
        "cap_fawn_sim_after": round(fawn_sim(capB, coat), 3),
        "cap_bright_ratio": round(float(capB.mean() / max(coat.mean(), 1e-3)), 3),
        "cap_texture_ratio": round(float(capB.std() / max(capA.std(), 1e-3)), 3),
        "butterfly_delta": round(float(np.abs(crop(b, R["butterfly"]) - crop(a, R["butterfly"])).mean()), 3),
        "ocean_delta": round(float(np.abs(crop(b, R["ocean"]) - crop(a, R["ocean"])).mean()), 3),
        "coat_ctl_delta": round(float(np.abs(crop(b, R["coat_ctl"]) - crop(a, R["coat_ctl"])).mean()), 3),
    }
    res["PASS"] = bool(res["cap_fawn_sim_after"] >= 0.90 and 0.95 <= res["cap_bright_ratio"] <= 1.5
                       and res["butterfly_delta"] < 2.5 and res["ocean_delta"] < 2.5
                       and res["coat_ctl_delta"] < 8 and 0.4 <= res["cap_texture_ratio"] <= 1.6)
    print(json.dumps(res, indent=1))
    return res


if __name__ == "__main__":
    main(sys.argv[1])
