#!/usr/bin/env python3
"""Tail Trim — ZERO-TOKEN auto-trimmer for frozen Kling clip tails (hard constraint C7).

Kling holds its last frame: every render ends on a frozen tail, and a frozen tail that reaches the
cut reads as a defect (the EP3 4:47 micro-freeze WAS one). The Render-QC gate says "find the last
moving frame and trim the clip there" — this tool does that measurement and the cut mechanically,
so it never depends on eyeballing a filmstrip and never costs a re-render.

Usage:
  PYTHONPATH=. python -m bentley.fix.tail_trim scan CLIP [CLIP ...]
      # measure only (no writes): report each clip's frozen-tail length; exit 1 if any >= --min-tail
  PYTHONPATH=. python -m bentley.fix.tail_trim trim CLIP [CLIP ...] [--out OUT]
      # write <stem>_trim.mp4 (fresh filename law) cut at the last moving frame + --pad
      # --out only with a single clip

Metric: mean |frame-to-frame| grayscale diff at ~320px — the playbook freeze-scan metric
(< 0.35 = frozen; --thresh to override). Tuning: --min-tail 0.12s ignores codec-noise stubs,
--pad keeps a beat of settle after the last moving frame.

Honest limits: END freezes only — mid-clip freezes are the QA scan suite's job, and an entirely
static clip is a §5 defect this tool refuses to "fix" (it reports and skips). A clip that ends on
an INTENTIONAL held emotion will be flagged too — read the scan output before trimming.
"""
import argparse
import os
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np
from PIL import Image

THRESH, MIN_TAIL, PAD = 0.35, 0.12, 0.0


def _probe_fps(path):
    r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                        "stream=r_frame_rate", "-of", "csv=p=0", str(path)],
                       capture_output=True, text=True, check=True).stdout.strip()
    num, _, den = r.partition("/")
    return float(num) / float(den or 1)


def _frame_diffs(path):
    """Per-transition mean |gray diff| at ~320px width, native fps."""
    with tempfile.TemporaryDirectory(prefix="tailtrim_") as td:
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(path),
                        "-vf", "scale=320:-2", f"{td}/f%05d.png"], check=True)
        frames = sorted(Path(td).glob("f*.png"))
        arr = [np.asarray(Image.open(f).convert("L"), dtype=np.int16) for f in frames]
    if len(arr) < 2:
        raise ValueError(f"{path}: fewer than 2 frames — not a clip")
    return np.array([np.abs(b - a).mean() for a, b in zip(arr, arr[1:])])


def scan_clip(path, thresh=THRESH):
    """Return (frozen_tail_seconds, keep_seconds, n_frames, fps). keep = through the end of the
    last moving frame's display. frozen_tail == full duration means the clip never moves."""
    diffs = _frame_diffs(path)
    fps = _probe_fps(path)
    n = len(diffs) + 1
    moving = np.nonzero(diffs >= thresh)[0]
    if len(moving) == 0:
        return n / fps, 0.0, n, fps                     # entirely static
    last_moving_frame = int(moving[-1]) + 1             # frame index the last motion lands on
    keep = (last_moving_frame + 1) / fps
    return (n - 1 - last_moving_frame) / fps, keep, n, fps


def trim_clip(path, out=None, thresh=THRESH, min_tail=MIN_TAIL, pad=PAD):
    """Cut the frozen tail off. Returns (out_path_or_None, frozen_tail_seconds)."""
    tail, keep, n, fps = scan_clip(path, thresh)
    if keep == 0.0:
        print(f"{Path(path).name}: ENTIRELY STATIC ({tail:.2f}s) — a §5 defect, not a tail; skipping")
        return None, tail
    if tail < min_tail:
        print(f"{Path(path).name}: frozen tail {tail:.2f}s < {min_tail:.2f}s — nothing to trim")
        return None, tail
    out = out or os.path.splitext(str(path))[0] + "_trim.mp4"
    t = keep + pad
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(path), "-t", f"{t:.3f}",
                    "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", "-c:a", "aac", out],
                   check=True)
    print(f"{Path(path).name}: frozen tail {tail:.2f}s cut -> {out} (kept {t:.2f}s of {n / fps:.2f}s)")
    return out, tail


def main(argv=None):
    ap = argparse.ArgumentParser(description="Tail Trim — cut frozen Kling clip tails (C7)")
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name in ("scan", "trim"):
        p = sub.add_parser(name)
        p.add_argument("clips", nargs="+")
        p.add_argument("--thresh", type=float, default=THRESH)
        p.add_argument("--min-tail", type=float, default=MIN_TAIL)
        if name == "trim":
            p.add_argument("--out", help="output path (single clip only)")
            p.add_argument("--pad", type=float, default=PAD)
    a = ap.parse_args(argv)

    if a.cmd == "scan":
        worst = 0.0
        for c in a.clips:
            tail, keep, n, fps = scan_clip(c, a.thresh)
            state = ("ENTIRELY STATIC" if keep == 0.0
                     else f"frozen tail {tail:.2f}s" if tail >= a.min_tail else "ok")
            print(f"{Path(c).name:36} {n / fps:6.2f}s  {state}")
            worst = max(worst, tail)
        return 1 if worst >= a.min_tail else 0

    if a.out and len(a.clips) > 1:
        ap.error("--out only with a single clip")
    for c in a.clips:
        trim_clip(c, a.out, a.thresh, a.min_tail, a.pad)
    return 0


if __name__ == "__main__":
    sys.exit(main())
