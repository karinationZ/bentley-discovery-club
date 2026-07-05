#!/usr/bin/env python3
"""EDL LINT — the freeze-push math, mechanical (playbook Part 2 step 4 / Part 3.4; SKILL §9).

Every EP3 freeze-stretch defect (0:12, 4:47, the 2s end freeze) traced to EDL arithmetic done by
eye: VO longer than the picture under it, or a piece stretched past the 1.3x retime ceiling (C2).
This makes `wants Xs / clip Ys / push=0.00` free arithmetic on any shotlist — run it at EDL
authoring time AND again after every clip swap (real durations change the math).

Run: PYTHONPATH=. python -m bentley.qa.edl_lint episodes/<ep>/shotlists/<list>.json
       [--root .] [--retime 1.3]

Checks (flat and seq schemas — same conventions as shot_ratios / mouthmotion / animatic):
  FAIL — VO outlasts its section's picture (the assembler would freeze-pad exactly that gap)
  FAIL — a piece wants more than its real clip can give at <= --retime stretch
  FAIL — a `vo` mp3 named in the EDL is missing on disk
  FAIL — same src file on two consecutive pieces with no distinct sub-range (§5a loop defect)
  WARN — legal-but-noted retime (1.0x < stretch <= ceiling), missing `scale`/`sync` tags,
         adjacent same-src pieces with distinct sub-ranges
  INFO — `todo` pieces (no real clip yet: only planned-duration math applies)

Exit 0 = clean; 1 = any FAIL (usable as an Animatic-Lock / assembly gate).
Ratios themselves stay with `python -m bentley.qa.shot_ratios` (Shot-Flow Law).
"""
import argparse
import json
import os
import subprocess
import sys
from pathlib import Path

from bentley.episode_builder.animatic import parse_dur, vo_paths

VIDEO_EXT = {".mp4", ".mov", ".mkv", ".webm", ".m4v"}
EPS = 0.05


def media_dur(path):
    """ffprobe duration, or None when the file is unreadable."""
    try:
        return float(subprocess.check_output(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "csv=p=0", str(path)], stderr=subprocess.DEVNULL).strip())
    except (subprocess.CalledProcessError, ValueError):
        return None


def _abs(root, p):
    return p if os.path.isabs(p) else os.path.normpath(os.path.join(root, p))


def pieces(shot):
    """Yield piece dicts (a flat shot is its own single piece)."""
    for p in (shot.get("seq") or [shot]):
        yield p


def _piece_src(piece, shot):
    src = piece.get("src") or ("" if piece is not shot else shot.get("src") or "")
    src = str(src)
    return src if Path(src).suffix.lower() in VIDEO_EXT else ""


def _subrange(piece):
    for k in ("in", "start", "offset", "ss"):
        if piece.get(k) is not None:
            return str(piece[k])
    return None


def lint(shotlist, root=".", retime=1.3):
    """Returns (fails, warns, infos) — lists of message strings."""
    data = json.loads(Path(shotlist).read_text())
    shots = data["shots"] if isinstance(data, dict) else data
    fails, warns, infos = [], [], []
    todo = 0
    prev_src, prev_label, prev_range = "", "", None

    for shot in shots:
        sid = shot.get("id", "?")
        planned = 0.0
        for i, p in enumerate(pieces(shot)):
            label = sid if p is shot else f"{sid}[{i}]"
            wants = parse_dur(p.get("dur"), parse_dur(shot.get("dur"), 0.0))
            planned += wants
            if not (p.get("scale") or shot.get("scale")):
                warns.append(f"{label}: no `scale` tag (Shot-Flow ratios need it — shot_ratios will FAIL)")
            if shot.get("vo") and not (p.get("sync") or p.get("lipsync")):
                warns.append(f"{label}: dialogue piece without a `sync` tag (Sync-or-Hide EDL trace)")

            src = _piece_src(p, shot)
            if not src:
                if str(shot.get("status", "")).lower() == "todo":
                    todo += 1
                continue
            ap = _abs(root, src)
            if not os.path.exists(ap):
                if str(shot.get("status", "")).lower() == "todo":
                    todo += 1
                else:
                    fails.append(f"{label}: src missing on disk: {src}")
                continue

            # §5a: same clip on consecutive pieces
            if src == prev_src:
                rng = _subrange(p)
                if rng is not None and prev_range is not None and rng != prev_range:
                    warns.append(f"{prev_label} -> {label}: same clip back-to-back "
                                 f"(distinct sub-ranges — still §5a-adjacent, check the cut)")
                else:
                    fails.append(f"{prev_label} -> {label}: same clip back-to-back with no distinct "
                                 f"sub-range ({Path(src).name}) — reads as a loop (§5a)")
            prev_src, prev_label, prev_range = src, label, _subrange(p)

            has = media_dur(ap)
            if has is None:
                fails.append(f"{label}: unreadable clip: {src}")
                continue
            if wants > has * retime + EPS:
                push = wants - has * retime
                fails.append(f"{label}: wants {wants:.2f}s / clip {has:.2f}s / max@{retime:.1f}x "
                             f"{has * retime:.2f}s / push={push:.2f}s — plan another clip, don't stretch")
            elif wants > has + EPS:
                warns.append(f"{label}: retime x{wants / has:.2f} ({wants:.2f}s from {has:.2f}s) — "
                             f"legal (<= {retime:.1f}x) but verify it doesn't read as slow-mo")

        # VO coverage per section
        mp3s = vo_paths(shot)
        if mp3s:
            missing = [m for m in mp3s if not os.path.exists(_abs(root, m))]
            for m in missing:
                fails.append(f"{sid}: vo mp3 missing on disk: {m}")
            vo_dur = sum(media_dur(_abs(root, m)) or 0.0 for m in mp3s if m not in missing)
            if not missing and vo_dur > planned + EPS:
                fails.append(f"{sid}: VO {vo_dur:.2f}s outlasts picture {planned:.2f}s "
                             f"(push={vo_dur - planned:.2f}s) — the assembler would freeze-pad this")

    if todo:
        infos.append(f"{todo} todo piece(s) without a rendered clip yet — planned-duration math only; "
                     f"RE-RUN this lint after the real clips land")
    return fails, warns, infos


def main(argv=None):
    ap = argparse.ArgumentParser(description="EDL lint — mechanical freeze-push / coverage checks")
    ap.add_argument("shotlist")
    ap.add_argument("--root", default=".", help="repo root the EDL paths are relative to")
    ap.add_argument("--retime", type=float, default=1.3, help="retime ceiling (owner law: 1.3)")
    a = ap.parse_args(argv)

    fails, warns, infos = lint(a.shotlist, a.root, a.retime)
    for m in infos:
        print(f"INFO  {m}")
    for m in warns:
        print(f"WARN  {m}")
    for m in fails:
        print(f"FAIL  {m}")
    print(f"{Path(a.shotlist).name}: {len(fails)} fail / {len(warns)} warn / {len(infos)} info — "
          + ("PASS" if not fails else "NOT PASSED — fix the EDL before it goes anywhere near a render"))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
