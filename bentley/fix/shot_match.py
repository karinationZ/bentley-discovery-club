#!/usr/bin/env python3
"""Shot Match — ZERO-TOKEN color/luma conform of a drifted clip to a scene reference (tier 1.5).

Owns two recurring QA failures WITHOUT touching the render: (1) "grade inconsistent across shots"
— one clip in a scene came back warmer/darker than its neighbors; (2) the known KLING-AVATAR
DARKENING (playbook Part 6 gotcha: Avatar darkens the image — lift it in the grade): conform the
Avatar CU back to its SOURCE KEYFRAME with --luma-only.

Usage:
  PYTHONPATH=. python -m bentley.fix.shot_match scan TARGET --ref REF
      # measure only: LAB mean/std of both + the delta (REF = clip or still)
  PYTHONPATH=. python -m bentley.fix.shot_match fix TARGET --ref REF
      [--strength 1.0] [--luma-only] [--out OUT]

Method: Reinhard statistics transfer in CIELAB (bentley/fix/color_transfer.py) — global, gains
clipped to [0.6, 1.6], applied per frame, so texture/motion are untouched; only the overall color
and level move. Always `scan` first: a delta-L beyond ~15 or big chroma deltas usually mean the
shot is WRONG (drifted render), not mis-graded — that's a regen question, not a grade fix.

Honest limits: global conform only — it cannot fix a color cast that varies WITHIN the frame,
identity drift, or content. Intentional mood grading (a scene MEANT darker) must use the mood
shot as --ref, not a bright neighbor. Re-check §9 "grade consistent" on the re-cut after."""
import argparse
import os
import subprocess
import tempfile
from pathlib import Path

import numpy as np
from PIL import Image

from bentley.fix.color_transfer import lab_stats, transfer

IMAGE_EXT = {".png", ".jpg", ".jpeg", ".webp", ".bmp"}
N_SAMPLE = 12


def _sample_arrays(path, n=N_SAMPLE, width=320):
    """Up to n evenly-spaced RGB frames (downscaled) from a clip, or the single still."""
    if Path(path).suffix.lower() in IMAGE_EXT:
        im = Image.open(path).convert("RGB")
        im.thumbnail((width, width * 4))
        return [np.asarray(im, np.float64)]
    dur = float(subprocess.check_output(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0",
         str(path)]).strip())
    fps = max(n / max(dur, 0.1), 0.2)
    with tempfile.TemporaryDirectory(prefix="shotmatch_") as td:
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(path),
                        "-vf", f"fps={fps},scale={width}:-2", f"{td}/f%03d.png"], check=True)
        return [np.asarray(Image.open(f).convert("RGB"), np.float64)
                for f in sorted(Path(td).glob("f*.png"))[:n]]


def _stats_of(path):
    frames = _sample_arrays(path)
    px = np.concatenate([f.reshape(-1, 3) for f in frames])
    return lab_stats(px.reshape(1, -1, 3))


def scan(target, ref):
    (tm, ts), (rm, rs) = _stats_of(target), _stats_of(ref)
    print(f"target {Path(target).name}: L {tm[0]:6.1f}±{ts[0]:.1f}  a {tm[1]:6.1f}  b {tm[2]:6.1f}")
    print(f"ref    {Path(ref).name}: L {rm[0]:6.1f}±{rs[0]:.1f}  a {rm[1]:6.1f}  b {rm[2]:6.1f}")
    d = rm - tm
    print(f"delta  L {d[0]:+.1f}  a {d[1]:+.1f}  b {d[2]:+.1f}"
          + ("   << big delta — is the shot mis-graded, or just WRONG (regen question)?"
             if abs(d[0]) > 15 or abs(d[1]) > 12 or abs(d[2]) > 12 else ""))
    return d


def fix(target, ref, strength=1.0, luma_only=False, out=None):
    src_stats, ref_stats = _stats_of(target), _stats_of(ref)
    out = out or os.path.splitext(str(target))[0] + "_match.mp4"
    fps = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                          "stream=r_frame_rate", "-of", "csv=p=0", str(target)],
                         capture_output=True, text=True, check=True).stdout.strip() or "24/1"
    with tempfile.TemporaryDirectory(prefix="shotmatch_") as td:
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(target),
                        f"{td}/f%05d.png"], check=True)
        for fn in sorted(os.listdir(td)):
            fp = os.path.join(td, fn)
            arr = np.asarray(Image.open(fp).convert("RGB"), np.float64)
            Image.fromarray(transfer(arr, src_stats, ref_stats, strength, luma_only)
                            .astype(np.uint8)).save(fp)
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", fps,
                        "-i", f"{td}/f%05d.png", "-c:v", "libx264", "-crf", "18",
                        "-pix_fmt", "yuv420p", out], check=True)
    return out


def main(argv=None):
    ap = argparse.ArgumentParser(description="Conform a clip's color/luma to a scene reference")
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("scan")
    s.add_argument("target")
    s.add_argument("--ref", required=True)
    f = sub.add_parser("fix")
    f.add_argument("target")
    f.add_argument("--ref", required=True)
    f.add_argument("--strength", type=float, default=1.0)
    f.add_argument("--luma-only", action="store_true",
                   help="levels only (the Avatar-darkening lift) — chroma untouched")
    f.add_argument("--out")
    a = ap.parse_args(argv)
    if a.cmd == "scan":
        scan(a.target, a.ref)
    else:
        print(f"matched -> {fix(a.target, a.ref, a.strength, a.luma_only, a.out)}")
    return 0


if __name__ == "__main__":
    import sys
    sys.exit(main())
