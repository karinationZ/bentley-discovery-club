#!/usr/bin/env python3
"""Per-line VO quality check: loudness (LUFS), true peak, 4-10kHz clarity share, spectral centroid,
speech pace. Flags outliers per speaker. Run: python3 scratch/ep4/vo/qa_vo.py"""
import json
import re
import subprocess
import sys
from pathlib import Path

import numpy as np

VO = Path("scratch/ep4/vo")


def pcm(f):
    p = subprocess.run(["ffmpeg", "-v", "error", "-i", str(f), "-ac", "1", "-ar", "44100",
                        "-f", "f32le", "-"], capture_output=True)
    return np.frombuffer(p.stdout, dtype=np.float32)


def loudness(f):
    p = subprocess.run(["ffmpeg", "-i", str(f), "-af", "loudnorm=print_format=json", "-f", "null", "-"],
                       capture_output=True, text=True)
    m = re.search(r"\{[^}]+\}", p.stderr, re.S)
    d = json.loads(m.group(0)) if m else {}
    return float(d.get("input_i", "nan")), float(d.get("input_tp", "nan"))


def spectral(f):
    a = pcm(f)
    if len(a) < 4410:
        return float("nan"), float("nan")
    sp = np.abs(np.fft.rfft(a)) ** 2
    fr = np.fft.rfftfreq(len(a), 1 / 44100)
    band = lambda lo, hi: sp[(fr > lo) & (fr < hi)].sum()
    total = band(100, 16000)
    clar = 100 * band(4000, 10000) / total if total else float("nan")
    cent = float((fr[(fr > 100) & (fr < 16000)] * sp[(fr > 100) & (fr < 16000)]).sum() /
                 (total or 1))
    return clar, cent


rows = []
for f in sorted(VO.glob("*.mp3")):
    if f.stem.endswith(("_raw", "_clean")):
        continue
    spk = f.stem.split("_")[0]
    dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                         "-of", "csv=p=0", str(f)]))
    lufs, tp = loudness(f)
    clar, cent = spectral(f)
    rows.append((f.stem, spk, dur, lufs, tp, clar, cent))

print(f"{'line':15} {'spk':3} {'dur':>6} {'LUFS':>6} {'TP':>5} {'clar%':>6} {'cent':>6}")
print("-" * 60)
flagged = []
by_spk = {}
for r in rows:
    by_spk.setdefault(r[1], []).append(r)
for spk, rs in by_spk.items():
    clars = [r[5] for r in rs if not np.isnan(r[5])]
    med = float(np.median(clars))
    for r in rs:
        name, _, dur, lufs, tp, clar, cent = r
        flags = []
        if not np.isnan(clar) and clar < 0.55 * med:
            flags.append("MUFFLED(clar)")
        if not np.isnan(lufs) and abs(lufs + 16) > 2.5:
            flags.append("LOUDNESS")
        if not np.isnan(tp) and tp > -1.0:
            flags.append("PEAK")
        mark = "  <-- " + ",".join(flags) if flags else ""
        print(f"{name:15} {spk:3} {dur:6.2f} {lufs:6.1f} {tp:5.1f} {clar:6.2f} {cent:6.0f}{mark}")
        if flags:
            flagged.append(name)
    print(f"  ({spk}: median clarity {med:.2f}%)")
print("\nFLAGGED:", flagged or "none")
