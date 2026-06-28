#!/usr/bin/env python3
"""Check Episode 2 v3 generated assets against the retimed shotlist."""
from __future__ import annotations

import json
import subprocess
from pathlib import Path

ROOT = Path("/project")
SHOTLIST = ROOT / "episodes/ep2/shotlists/ep2_v3_character_driven.json"
WORK = ROOT / "scratch/ep2/restart_v3"
KF = WORK / "keyframes"
MO = WORK / "motion"
VO = WORK / "vo" / "shots"


def duration(path: Path) -> float | None:
    if not path.exists():
        return None
    try:
        return float(
            subprocess.check_output(
                ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)]
            )
            .decode()
            .strip()
        )
    except Exception:
        return None


def main() -> None:
    data = json.loads(SHOTLIST.read_text())
    missing_stills = []
    missing_motion = []
    short_motion = []
    missing_audio = []
    total = 0.0
    for shot in data["shots"]:
        sid = shot["id"]
        total += float(shot["duration"])
        if shot["type"] != "card":
            if not (KF / f"{sid}.png").exists():
                missing_stills.append(sid)
            md = duration(MO / f"{sid}.mp4")
            if md is None:
                missing_motion.append(sid)
            elif md < float(shot["duration"]) - 0.2:
                short_motion.append((sid, round(md, 2), shot["duration"]))
        if not (VO / f"{sid}.mp3").exists():
            missing_audio.append(sid)

    print(f"planned_duration={total:.1f}s")
    print(f"missing_stills={len(missing_stills)}")
    print(f"missing_motion={len(missing_motion)}")
    print(f"short_motion={len(short_motion)}")
    print(f"missing_audio={len(missing_audio)}")
    if missing_stills:
        print("missing_stills_list=" + ",".join(missing_stills))
    if missing_motion:
        print("missing_motion_list=" + ",".join(missing_motion))
    if short_motion:
        print("short_motion_list=" + ",".join(f"{sid}:{got}/{need}" for sid, got, need in short_motion))
    if missing_audio:
        print("missing_audio_list=" + ",".join(missing_audio))


if __name__ == "__main__":
    main()
