#!/usr/bin/env python3
"""Generate Episode 2 v3 locked VO and timing artifacts.

Source of truth:
  docs/series/season_1/ep2/EP2_v3_PRODUCTION_CUE_SHEET.md

Outputs:
  scratch/ep2/restart_v3/vo/labels/*.mp3
  scratch/ep2/restart_v3/vo/shots/*.mp3
  scratch/ep2/restart_v3/vo/EP2_v3_VO_READTHROUGH.mp3
  scratch/ep2/restart_v3/vo/vo_timing.json
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

ROOT = Path("/project")
CUE = ROOT / "docs/series/season_1/ep2/EP2_v3_PRODUCTION_CUE_SHEET.md"
SHOTLIST = ROOT / "episodes/ep2/shotlists/ep2_v3_character_driven.json"
OUT = ROOT / "scratch/ep2/restart_v3/vo"
LABELS = OUT / "labels"
SHOTS = OUT / "shots"
TMP = OUT / "_tmp"


def load_dotenv() -> None:
    env = ROOT / ".env"
    if not env.exists():
        return
    for raw in env.read_text().splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        os.environ.setdefault(key, value)


load_dotenv()
sys.path.insert(0, str(ROOT))

from bentley.shared import eleven  # noqa: E402
from bentley.voices.dialogue import tts_bentley, tts_catchphrase, tts_indi  # noqa: E402


@dataclass(frozen=True)
class Line:
    label: str
    speaker: str
    text: str


def run(cmd: list[str]) -> None:
    subprocess.run(cmd, check=True)


def duration(path: Path) -> float:
    return float(
        subprocess.check_output(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)]
        )
        .decode()
        .strip()
    )


def tts_bill(text: str, outp: Path) -> Path:
    raw = outp.with_name(outp.stem + "_raw.mp3")
    eleven.speak(
        eleven.NARRATOR,
        text,
        str(raw),
        settings={"stability": 0.5, "similarity_boost": 0.75, "style": 0.4, "speed": 1.0},
    )
    run(
        [
            "ffmpeg",
            "-y",
            "-loglevel",
            "error",
            "-i",
            str(raw),
            "-af",
            "highpass=f=80,loudnorm=I=-16:TP=-1.5:LRA=11",
            "-b:a",
            "192k",
            str(outp),
        ]
    )
    return outp


def parse_locked_lines() -> list[Line]:
    text = CUE.read_text()
    block = re.search(r"```text\n(?P<body>.*?)\n```", text, flags=re.S)
    if not block:
        raise RuntimeError(f"No locked VO block found in {CUE}")
    lines: list[Line] = []
    for raw in block.group("body").splitlines():
        raw = raw.strip()
        if not raw or "|" not in raw:
            continue
        parts = [p.strip() for p in raw.split("|", 2)]
        if len(parts) != 3 or not parts[0].startswith("P"):
            continue
        lines.append(Line(*parts))
    if not lines:
        raise RuntimeError("Locked VO block parsed to zero lines")
    return lines


def generate_label(line: Line, force: bool) -> dict:
    LABELS.mkdir(parents=True, exist_ok=True)
    outp = LABELS / f"{line.label}.mp3"
    if force or not outp.exists() or outp.stat().st_size < 10_000:
        if line.speaker == "Bentley":
            if line.text == "Stop. Look. Listen.":
                tts_catchphrase(str(outp))
            else:
                tts_bentley(line.text, str(outp))
        elif line.speaker == "Indi":
            tts_indi(line.text, str(outp))
        elif line.speaker == "Narrator":
            tts_bill(line.text, outp)
        else:
            raise RuntimeError(f"Unknown speaker {line.speaker!r} for {line.label}")
    return {
        "label": line.label,
        "speaker": line.speaker,
        "text": line.text,
        "path": str(outp),
        "duration": round(duration(outp), 3),
    }


def silence(path: Path, seconds: float) -> Path:
    if not path.exists():
        run(
            [
                "ffmpeg",
                "-y",
                "-loglevel",
                "error",
                "-f",
                "lavfi",
                "-i",
                "anullsrc=r=44100:cl=mono",
                "-t",
                f"{seconds:.3f}",
                "-ac",
                "1",
                "-ar",
                "44100",
                "-b:a",
                "192k",
                str(path),
            ]
        )
    return path


def concat_audio(parts: list[Path], outp: Path) -> None:
    outp.parent.mkdir(parents=True, exist_ok=True)
    listf = TMP / f"{outp.stem}_list.txt"
    listf.write_text("".join(f"file '{p}'\n" for p in parts))
    run(
        [
            "ffmpeg",
            "-y",
            "-loglevel",
            "error",
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            str(listf),
            "-c:a",
            "libmp3lame",
            "-b:a",
            "192k",
            str(outp),
        ]
    )


def build_readthrough(lines: list[Line]) -> dict:
    TMP.mkdir(parents=True, exist_ok=True)
    gap = silence(TMP / "gap_350ms.mp3", 0.35)
    parts: list[Path] = []
    for line in lines:
        parts.append(LABELS / f"{line.label}.mp3")
        parts.append(gap)
    outp = OUT / "EP2_v3_VO_READTHROUGH.mp3"
    concat_audio(parts, outp)
    return {"path": str(outp), "duration": round(duration(outp), 3)}


def build_shot_audio(label_meta: dict[str, dict]) -> list[dict]:
    TMP.mkdir(parents=True, exist_ok=True)
    gap = silence(TMP / "gap_140ms.mp3", 0.14)
    data = json.loads(SHOTLIST.read_text())
    out: list[dict] = []
    for shot in data["shots"]:
        labels = shot.get("vo", [])
        if not labels:
            continue
        parts: list[Path] = []
        for i, label in enumerate(labels):
            parts.append(LABELS / f"{label}.mp3")
            if i != len(labels) - 1:
                parts.append(gap)
        outp = SHOTS / f"{shot['id']}.mp3"
        concat_audio(parts, outp)
        aud = duration(outp)
        visual = float(shot["duration"])
        out.append(
            {
                "shot_id": shot["id"],
                "labels": labels,
                "speakers": sorted({label_meta[label]["speaker"] for label in labels}),
                "audio_path": str(outp),
                "audio_duration": round(aud, 3),
                "planned_visual_duration": visual,
                "timing_delta": round(aud - visual, 3),
                "needs_visual_extension": aud > visual + 0.25,
            }
        )
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--force", action="store_true", help="Regenerate existing label audio.")
    args = ap.parse_args()

    OUT.mkdir(parents=True, exist_ok=True)
    LABELS.mkdir(parents=True, exist_ok=True)
    SHOTS.mkdir(parents=True, exist_ok=True)
    TMP.mkdir(parents=True, exist_ok=True)

    lines = parse_locked_lines()
    label_items = [generate_label(line, args.force) for line in lines]
    label_meta = {item["label"]: item for item in label_items}
    readthrough = build_readthrough(lines)
    shot_audio = build_shot_audio(label_meta)

    timing = {
        "source_cue_sheet": str(CUE),
        "source_shotlist": str(SHOTLIST),
        "line_count": len(lines),
        "label_audio": label_items,
        "readthrough": readthrough,
        "shot_audio": shot_audio,
    }
    (OUT / "vo_timing.json").write_text(json.dumps(timing, indent=2))

    print(f"Generated/verified {len(lines)} VO labels")
    print(f"Readthrough: {readthrough['duration']:.1f}s -> {readthrough['path']}")
    over = [s for s in shot_audio if s["needs_visual_extension"]]
    print(f"Shot audio files: {len(shot_audio)}; timing extensions flagged: {len(over)}")
    for item in over:
        print(
            f"  {item['shot_id']}: audio {item['audio_duration']:.1f}s vs planned "
            f"{item['planned_visual_duration']:.1f}s ({item['timing_delta']:+.1f}s)"
        )


if __name__ == "__main__":
    main()
