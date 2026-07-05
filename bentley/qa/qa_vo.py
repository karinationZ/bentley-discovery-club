#!/usr/bin/env python3
"""Per-line VO quality table (playbook Part 2 step 5) — LUFS, true peak, 4–10kHz clarity share,
spectral centroid; outliers flagged per speaker. A flagged line never reaches the cut.
Speaker = the filename prefix before the first underscore (B_hook1.mp3 -> B).
Files ending _raw/_clean and take files (_t1/_t2/...) are skipped.
Run: python -m bentley.qa.qa_vo <vo_dir>            (productionized from scratch/ep4/vo/qa_vo.py)
Exit 0 = no flags; exit 1 = flagged lines (re-record before the animatic)."""
import json
import re
import subprocess
import sys
from pathlib import Path

import numpy as np

TARGET_LUFS = -16.0


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


def main(argv=None):
    argv = argv if argv is not None else sys.argv[1:]
    if len(argv) != 1:
        print(__doc__)
        return 2
    vo = Path(argv[0])
    rows = []
    for f in sorted(vo.glob("*.mp3")):
        if f.stem.endswith(("_raw", "_clean")) or re.search(r"_t\d+$", f.stem):
            continue
        spk = f.stem.split("_")[0]
        dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries",
                                             "format=duration", "-of", "csv=p=0", str(f)]))
        lufs, tp = loudness(f)
        clar, cent = spectral(f)
        rows.append((f.stem, spk, dur, lufs, tp, clar, cent))
    if not rows:
        print(f"qa_vo: no VO mp3s found in {vo}")
        return 1

    print(f"{'line':22} {'spk':3} {'dur':>6} {'LUFS':>6} {'TP':>5} {'clar%':>6} {'cent':>6}")
    print("-" * 66)
    flagged = []
    by_spk = {}
    for r in rows:
        by_spk.setdefault(r[1], []).append(r)
    for spk, rs in by_spk.items():
        clars = [r[5] for r in rs if not np.isnan(r[5])]
        med = float(np.median(clars)) if clars else float("nan")
        for name, _, dur, lufs, tp, clar, cent in rs:
            flags = []
            if not np.isnan(clar) and not np.isnan(med) and clar < 0.55 * med:
                flags.append("MUFFLED(clar)")
            if not np.isnan(lufs) and abs(lufs - TARGET_LUFS) > 2.5:
                flags.append("LOUDNESS")
            if not np.isnan(tp) and tp > -1.0:
                flags.append("PEAK")
            mark = "  <-- " + ",".join(flags) if flags else ""
            print(f"{name:22} {spk:3} {dur:6.2f} {lufs:6.1f} {tp:5.1f} {clar:6.2f} {cent:6.0f}{mark}")
            if flags:
                flagged.append(name)
        print(f"  ({spk}: median clarity {med:.2f}%)")
    print("\nFLAGGED:", flagged or "none")
    return 1 if flagged else 0


if __name__ == "__main__":
    sys.exit(main())
