#!/usr/bin/env python3
"""Assemble Episode 2 v3 picture+VO from generated clips.

Default mode is strict: every non-card shot must have a motion clip. Use
--allow-placeholders only for an internal animatic.
"""
from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path("/project")
SHOTLIST = ROOT / "episodes/ep2/shotlists/ep2_v3_character_driven.json"
WORK = ROOT / "scratch/ep2/restart_v3"
MO = WORK / "motion"
KF = WORK / "keyframes"
VO = WORK / "vo" / "shots"
ASM = WORK / "assembly"
SEG = ASM / "segs"

W, H, FPS = 1280, 720, 24
FILL = f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},setsar=1"
ENC = ["-c:v", "libx264", "-crf", "16", "-pix_fmt", "yuv420p", "-r", str(FPS)]
AUD = ["-ar", "48000", "-ac", "2"]


def run(cmd: list[str], *, check: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(cmd, check=check)


def duration(path: Path) -> float:
    return float(
        subprocess.check_output(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)]
        )
        .decode()
        .strip()
    )


def load_shots() -> list[dict]:
    return json.loads(SHOTLIST.read_text())["shots"]


def make_card(shot: dict, out: Path) -> Path:
    dur = float(shot["duration"])
    voice = VO / f"{shot['id']}.mp3"
    img = Image.new("RGB", (W, H), (21, 72, 84))
    d = ImageDraw.Draw(img)
    try:
        title_font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Rounded Bold.ttf", 60)
        sub_font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Rounded Bold.ttf", 36)
    except Exception:
        title_font = sub_font = ImageFont.load_default()
    title = "NEXT TIME"
    sub = "THE ANT CITY BENEATH OUR FEET"
    d.rectangle([0, 0, W, H], fill=(17, 86, 94))
    for y, color in ((H * 0.34, (255, 224, 126)), (H * 0.50, (255, 255, 245))):
        text = title if color[0] == 255 and color[1] == 224 else sub
        font = title_font if text == title else sub_font
        tw = d.textlength(text, font=font)
        d.text(((W - tw) / 2, y), text, fill=color, font=font, stroke_width=4, stroke_fill=(7, 28, 35))
    png = ASM / f"_{shot['id']}.png"
    img.save(png)
    audio_in = ["-i", str(voice)] if voice.exists() else ["-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo"]
    run(
        [
            "ffmpeg",
            "-y",
            "-loglevel",
            "error",
            "-loop",
            "1",
            "-i",
            str(png),
            *audio_in,
            "-t",
            f"{dur:.3f}",
            "-vf",
            f"scale={W}:{H},format=yuv420p",
            "-map",
            "0:v",
            "-map",
            "1:a",
            "-af",
            "apad",
            *ENC,
            "-c:a",
            "aac",
            "-b:a",
            "192k",
            *AUD,
            str(out),
        ]
    )
    return out


def make_placeholder(shot: dict, out: Path) -> Path:
    dur = float(shot["duration"])
    key = KF / f"{shot['id']}.png"
    if not key.exists():
        img = Image.new("RGB", (W, H), (30, 30, 36))
        d = ImageDraw.Draw(img)
        d.text((40, 40), f"MISSING: {shot['id']}", fill=(255, 240, 180))
        key = ASM / f"_{shot['id']}_missing.png"
        img.save(key)
    voice = VO / f"{shot['id']}.mp3"
    audio_in = ["-i", str(voice)] if voice.exists() else ["-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo"]
    run(
        [
            "ffmpeg",
            "-y",
            "-loglevel",
            "error",
            "-loop",
            "1",
            "-i",
            str(key),
            *audio_in,
            "-t",
            f"{dur:.3f}",
            "-vf",
            f"{FILL},format=yuv420p",
            "-map",
            "0:v",
            "-map",
            "1:a",
            "-af",
            "apad",
            *ENC,
            "-c:a",
            "aac",
            "-b:a",
            "192k",
            *AUD,
            str(out),
        ]
    )
    return out


def make_segment(shot: dict, out: Path, *, allow_placeholders: bool) -> Path:
    if shot["type"] == "card":
        return make_card(shot, out)
    src = MO / f"{shot['id']}.mp4"
    if not src.exists():
        if allow_placeholders:
            return make_placeholder(shot, out)
        raise FileNotFoundError(f"Missing motion clip for {shot['id']}: {src}")
    voice = VO / f"{shot['id']}.mp3"
    if not voice.exists():
        raise FileNotFoundError(f"Missing shot audio for {shot['id']}: {voice}")
    dur = float(shot["duration"])
    src_dur = duration(src)
    if src_dur < dur - 0.2 and not allow_placeholders:
        raise RuntimeError(f"{shot['id']} clip too short: {src_dur:.2f}s for {dur:.2f}s")
    run(
        [
            "ffmpeg",
            "-y",
            "-loglevel",
            "error",
            "-i",
            str(src),
            "-i",
            str(voice),
            "-t",
            f"{dur:.3f}",
            "-filter_complex",
            f"[0:v]{FILL},fps={FPS},format=yuv420p[v]",
            "-map",
            "[v]",
            "-map",
            "1:a",
            "-af",
            "apad",
            *ENC,
            "-c:a",
            "aac",
            "-b:a",
            "192k",
            *AUD,
            str(out),
        ]
    )
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--allow-placeholders", action="store_true")
    ap.add_argument("--pod", help="Assemble only one pod, e.g. p01, for review.")
    args = ap.parse_args()

    ASM.mkdir(parents=True, exist_ok=True)
    SEG.mkdir(parents=True, exist_ok=True)
    shots = load_shots()
    if args.pod:
        shots = [shot for shot in shots if shot.get("pod") == args.pod]
        if not shots:
            raise SystemExit(f"No shots found for pod {args.pod}")
    segs: list[Path] = []
    for idx, shot in enumerate(shots, 1):
        out = SEG / f"{idx:02d}_{shot['id']}.mp4"
        make_segment(shot, out, allow_placeholders=args.allow_placeholders)
        segs.append(out)
        print(f"{idx:02d} {shot['id']:24s} {duration(out):5.1f}s", flush=True)

    listf = ASM / "_seglist.txt"
    listf.write_text("".join(f"file '{p}'\n" for p in segs))
    stem = f"EP2_v3_{args.pod.upper()}_PREVIEW" if args.pod else "EP2_v3"
    if args.allow_placeholders:
        stem += "_ANIMATIC"
    elif not args.pod:
        stem += "_PICTURE_DIALOGUE"
    out = ASM / f"{stem}.mp4"
    result = run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(listf), "-c", "copy", str(out)], check=False)
    if result.returncode != 0:
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
                *ENC,
                "-c:a",
                "aac",
                "-b:a",
                "192k",
                *AUD,
                str(out),
            ]
        )
    print(f"ASSEMBLY -> {out} ({duration(out):.1f}s)")


if __name__ == "__main__":
    main()
