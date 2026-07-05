#!/usr/bin/env python3
"""SCAN SUITE — the playbook Part 8.1 automated scans as ONE command (owner-approved 2026-07-05).

Replaces the per-episode scratch scan scripts: freeze scan, black-frame scan, sharpness sweep,
jitter check and stream checks, run against the FINAL exported file with pass/fail + timestamps.

  PYTHONPATH=. python -m bentley.qa.scan_suite FILE
      [--freeze-thresh 0.35] [--freeze-min 0.2] [--black-max 16] [--jitter-max 10]
      [--sharp-floor 100] [--min-height 1080] [--require-audio | --no-require-audio]

FAIL (exit 1): interior/leading black · freeze run >= --freeze-min (incl. a non-black END freeze —
an EP3 defect class) · sharpness second below --sharp-floor · stream checks (height, audio).
WARN: per-second jitter above --jitter-max (EP3 measured: handheld ~10–13, locked re-render ~4.8) ·
sharpness dip below half the local median (soft push-ins).
OK by design: trailing BLACK (the one closing fade).

Metrics (all measured, none eyeballed): freeze/black/jitter on a 320px gray stream at native fps
(mean |frame-to-frame| diff; mean luma); sharpness = variance of the gradient magnitude on
NATIVE-resolution gray at 1 fps. The --sharp-floor default 100 matches the playbook's edge-var
floor at 1080p; recalibrate with --sharp-floor if the delivery pipeline changes."""
import argparse
import json
import subprocess
import sys

import numpy as np

FREEZE_THRESH, FREEZE_MIN, BLACK_MAX, JITTER_MAX, SHARP_FLOOR = 0.35, 0.2, 16.0, 10.0, 100.0


def _probe(path):
    meta = json.loads(subprocess.check_output(
        ["ffprobe", "-v", "error", "-show_streams", "-show_format", "-of", "json", str(path)]))
    v = next(s for s in meta["streams"] if s["codec_type"] == "video")
    audio = any(s["codec_type"] == "audio" for s in meta["streams"])
    num, _, den = v.get("r_frame_rate", "24/1").partition("/")
    fps = float(num) / float(den or 1)
    return int(v["width"]), int(v["height"]), fps, audio, float(meta["format"]["duration"])


def _stream_gray(path, ow, oh, fps_filter=None):
    """Yield uint8 gray frames (oh, ow) via a rawvideo pipe (streaming — no temp files)."""
    vf = f"scale={ow}:{oh},format=gray"
    if fps_filter:
        vf = f"fps={fps_filter}," + vf
    proc = subprocess.Popen(["ffmpeg", "-v", "error", "-i", str(path), "-vf", vf,
                             "-f", "rawvideo", "-pix_fmt", "gray", "-"], stdout=subprocess.PIPE)
    nbytes = ow * oh
    try:
        while True:
            buf = proc.stdout.read(nbytes)
            if len(buf) < nbytes:
                break
            yield np.frombuffer(buf, np.uint8).reshape(oh, ow)
    finally:
        proc.stdout.close()
        proc.wait()


def _ts(sec):
    return f"{int(sec) // 60}:{sec % 60:04.1f}"


def _runs(flags, min_len_frames):
    """(start_idx, end_idx_exclusive) for every True-run of at least min_len_frames."""
    out, start = [], None
    for i, f in enumerate(flags):
        if f and start is None:
            start = i
        elif not f and start is not None:
            if i - start >= min_len_frames:
                out.append((start, i))
            start = None
    if start is not None and len(flags) - start >= min_len_frames:
        out.append((start, len(flags)))
    return out


def _grad_var(gray):
    g = gray.astype(np.float64)
    gy = np.zeros_like(g)
    gx = np.zeros_like(g)
    gy[1:-1, :] = (g[2:, :] - g[:-2, :]) * 0.5
    gx[:, 1:-1] = (g[:, 2:] - g[:, :-2]) * 0.5
    return float(np.var(np.sqrt(gx * gx + gy * gy)))


def scan(path, freeze_thresh=FREEZE_THRESH, freeze_min=FREEZE_MIN, black_max=BLACK_MAX,
         jitter_max=JITTER_MAX, sharp_floor=SHARP_FLOOR, min_height=1080, require_audio=True):
    """Returns (fails, warns, infos) message lists."""
    fails, warns, infos = [], [], []
    w, h, fps, audio, duration = _probe(path)
    infos.append(f"streams: {w}x{h} @ {fps:.3f}fps, {duration:.2f}s, audio={'yes' if audio else 'NO'}")
    if h < min_height:
        fails.append(f"stream: height {h} < required {min_height}")
    if require_audio and not audio:
        fails.append("stream: no audio track")

    # pass 1 — motion / black / jitter on a 320px gray stream at native fps
    oh = max(2, int(round(h * 320 / w / 2)) * 2)
    lumas, diffs, prev = [], [], None
    for fr in _stream_gray(path, 320, oh):
        lumas.append(float(fr.mean()))
        if prev is not None:
            diffs.append(float(np.abs(fr.astype(np.int16) - prev.astype(np.int16)).mean()))
        prev = fr
    n = len(lumas)
    if n < 3:
        fails.append("decode: fewer than 3 frames")
        return fails, warns, infos
    lumas, diffs = np.array(lumas), np.array(diffs)

    black = lumas < black_max
    for s, e in _runs(black, max(1, int(round(freeze_min * fps)))):
        if e == n:
            infos.append(f"black tail {_ts(s / fps)}–end — OK (the one closing fade)")
        elif s == 0:
            fails.append(f"LEADING black 0:00.0–{_ts(e / fps)} — no opening fade (owner rule)")
        else:
            fails.append(f"INTERIOR black {_ts(s / fps)}–{_ts(e / fps)}")

    frozen = diffs < freeze_thresh
    for s, e in _runs(frozen, max(1, int(round(freeze_min * fps)))):
        f0, f1 = s, e + 1                       # diff i spans frames i..i+1
        if black[f0:f1].all():
            continue                            # already reported as a black run
        where = " (END freeze)" if f1 >= n else ""
        fails.append(f"FREEZE {_ts(f0 / fps)}–{_ts(f1 / fps)} "
                     f"(diff<{freeze_thresh}, {(f1 - f0) / fps:.2f}s){where}")

    sec = (np.arange(len(diffs)) / fps).astype(int)
    for s in np.unique(sec):
        m = float(diffs[sec == s].mean())
        if m > jitter_max:
            warns.append(f"jitter {_ts(float(s))}: mean frame-diff {m:.1f} > {jitter_max:.0f} "
                         f"— intended action, or shake? (locked re-render, never deshake)")

    # pass 2 — sharpness sweep at native resolution, 1 fps
    if sharp_floor > 0:
        ev = [_grad_var(fr) for fr in _stream_gray(path, w, h, fps_filter=1)]
        med = float(np.median(ev)) if ev else 0.0
        for i, v in enumerate(ev):
            if v < sharp_floor:
                fails.append(f"sharpness {_ts(float(i))}: edge-var {v:.0f} < floor {sharp_floor:.0f}")
            elif med > 0 and v < 0.5 * med:
                warns.append(f"sharpness {_ts(float(i))}: edge-var {v:.0f} ≪ median {med:.0f} "
                             f"(soft render / over-stretch?)")
        infos.append(f"sharpness: median edge-var {med:.0f} over {len(ev)} sampled seconds")
    return fails, warns, infos


def main(argv=None):
    ap = argparse.ArgumentParser(description="Part 8.1 automated scans in one command")
    ap.add_argument("file")
    ap.add_argument("--freeze-thresh", type=float, default=FREEZE_THRESH)
    ap.add_argument("--freeze-min", type=float, default=FREEZE_MIN)
    ap.add_argument("--black-max", type=float, default=BLACK_MAX)
    ap.add_argument("--jitter-max", type=float, default=JITTER_MAX)
    ap.add_argument("--sharp-floor", type=float, default=SHARP_FLOOR,
                    help="edge-var floor at native res (0 disables the sharpness pass)")
    ap.add_argument("--min-height", type=int, default=1080)
    ap.add_argument("--require-audio", action=argparse.BooleanOptionalAction, default=True)
    a = ap.parse_args(argv)
    fails, warns, infos = scan(a.file, a.freeze_thresh, a.freeze_min, a.black_max,
                               a.jitter_max, a.sharp_floor, a.min_height, a.require_audio)
    for m in infos:
        print(f"INFO  {m}")
    for m in warns:
        print(f"WARN  {m}")
    for m in fails:
        print(f"FAIL  {m}")
    print(f"scan_suite: {len(fails)} fail / {len(warns)} warn — "
          + ("PASS" if not fails else "NOT PASSED — fix before the owner sees it (§8)"))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
