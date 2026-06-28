#!/usr/bin/env python3
"""Assemble Ep2 v7 picture/dialogue from approved v7 replacements.

Inputs stay read-only. Outputs go to scratch/ep2/final_v7/assembly.
"""
import json
import math
import os
import re
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps

ROOT = Path("/project")
OUTROOT = ROOT / "scratch/ep2/final_v7"
ASM = OUTROOT / "assembly"
SEG = ASM / "segs"
SEG.mkdir(parents=True, exist_ok=True)

W, H, FPS = 1280, 720, 24
AUD = ["-ar", "48000", "-ac", "2"]
VO = ROOT / "scratch/ep2/vo"
OLD_ASM = ROOT / "scratch/ep2/assembly/segs"
OLD_MOTION = ROOT / "assets/pilot_shots/ep2/motion"
OLD_SCRATCH_MOTION = ROOT / "scratch/ep2/motion"
V7_MOTION = OUTROOT / "motion"
PLATE = ROOT / "assets/character_design/TidePool_plate.jpg"
FILL = f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},setsar=1"


def durof(path):
    return float(
        subprocess.check_output(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)]
        )
        .decode()
        .strip()
    )


def mk_silence(path, dur):
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-loglevel",
            "error",
            "-f",
            "lavfi",
            "-i",
            "anullsrc=r=48000:cl=stereo",
            "-t",
            f"{dur:.3f}",
            "-c:a",
            "aac",
            "-b:a",
            "192k",
            str(path),
        ],
        check=True,
    )


def make_chase_audio():
    out = ASM / "_B_chase_rude.wav"
    if out.exists():
        return out
    gap = ASM / "_gap_020.wav"
    mk_silence(gap, 0.20)
    lst = ASM / "_chase_audio.txt"
    lst.write_text(
        "\n".join(
            [
                f"file '{VO / 'B_chase.mp3'}'",
                f"file '{gap}'",
                f"file '{VO / 'B_rude.mp3'}'",
            ]
        )
    )
    subprocess.run(
        ["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(lst), "-ar", "48000", "-ac", "2", str(out)],
        check=True,
    )
    return out


def make_title_png(path, text, sub=""):
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    try:
        f1 = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Rounded Bold.ttf", 64)
        f2 = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Rounded Bold.ttf", 34)
    except Exception:
        f1 = f2 = ImageFont.load_default()
    tw = d.textlength(text, font=f1)
    d.text(((W - tw) / 2, H * (0.38 if sub else 0.46)), text, fill=(255, 222, 120, 255), font=f1, stroke_width=5, stroke_fill=(20, 12, 0, 235))
    if sub:
        sw = d.textlength(sub, font=f2)
        d.text(((W - sw) / 2, H * 0.54), sub, fill=(250, 252, 255, 255), font=f2, stroke_width=3, stroke_fill=(0, 8, 18, 225))
    img.save(path)


def title_establish(out, dur=4.0):
    title = ASM / "_title_v7.png"
    make_title_png(title, "BENTLEY'S BIG ADVENTURES", "The Octopus Escape Artist")
    live = OLD_MOTION / "plate_live.mp4"
    base = live if live.exists() else PLATE
    in_args = ["-i", str(base)] if str(base).endswith(".mp4") else ["-loop", "1", "-i", str(base)]
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-loglevel",
            "error",
            *in_args,
            "-loop",
            "1",
            "-i",
            str(title),
            "-f",
            "lavfi",
            "-i",
            "anullsrc=r=48000:cl=stereo",
            "-t",
            f"{dur:.2f}",
            "-filter_complex",
            f"[0:v]{FILL},eq=brightness=-0.02:saturation=1.06,fade=t=in:st=0:d=0.35[bg];"
            f"[1:v]format=rgba,fade=t=in:st=0.35:d=0.55:alpha=1,fade=t=out:st={max(0, dur - 0.85):.2f}:d=0.7:alpha=1[t];"
            f"[bg][t]overlay,format=yuv420p[v]",
            "-map",
            "[v]",
            "-map",
            "2:a",
            "-c:v",
            "libx264",
            "-crf",
            "18",
            "-c:a",
            "aac",
            "-b:a",
            "192k",
            *AUD,
            str(out),
        ],
        check=True,
    )


def seg_video(video, dur, out, vo=None, start=0.0, retime=False, fade=False, crop_frac=None):
    filters = []
    if crop_frac:
        filters.append(f"crop=iw:ih*{crop_frac}:0:0")
    is_image = str(video).lower().endswith((".png", ".jpg", ".jpeg"))
    if is_image:
        filters.append(
            f"scale={W*2}:{H*2}:force_original_aspect_ratio=increase,"
            f"zoompan=z='min(zoom+0.0008,1.05)':d={int(dur*FPS)}:"
            f"x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s={W}x{H}:fps={FPS}"
        )
    else:
        filters.append(FILL)
    if retime and not is_image:
        src_d = max(0.01, durof(video) - start)
        filters.append(f"setpts={dur / src_d:.6f}*PTS")
    if fade and dur > 0.7:
        filters.append(f"fade=t=in:st=0:d=0.18,fade=t=out:st={max(0, dur - 0.25):.2f}:d=0.2")
    filters.append("format=yuv420p")
    cmd = ["ffmpeg", "-y", "-loglevel", "error"]
    if start:
        cmd += ["-ss", f"{start:.3f}"]
    cmd += ["-loop", "1", "-i", str(video)] if is_image else ["-i", str(video)]
    cmd += ["-i", str(vo)] if vo else ["-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo"]
    cmd += [
        "-t",
        f"{dur:.3f}",
        "-r",
        str(FPS),
        "-vf",
        ",".join(filters),
        "-af",
        "apad",
        "-map",
        "0:v",
        "-map",
        "1:a",
        "-c:v",
        "libx264",
        "-crf",
        "18",
        "-c:a",
        "aac",
        "-b:a",
        "192k",
        *AUD,
        str(out),
    ]
    subprocess.run(cmd, check=True)


def concat_segments(parts, out, reencode=False):
    lst = out.with_suffix(".txt")
    lst.write_text("\n".join(f"file '{p}'" for p in parts))
    if reencode:
        cmd = [
            "ffmpeg",
            "-y",
            "-loglevel",
            "error",
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            str(lst),
            "-c:v",
            "libx264",
            "-crf",
            "18",
            "-pix_fmt",
            "yuv420p",
            "-c:a",
            "aac",
            "-b:a",
            "192k",
            *AUD,
            str(out),
        ]
    else:
        cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy", str(out)]
    subprocess.run(cmd, check=True)


def make_composite(sid, pieces, out):
    tmp = []
    vo = next((item.get("vo") for item in pieces if item.get("vo")), None)
    for idx, item in enumerate(pieces):
        p = SEG / f"_{sid}_{idx}.mp4"
        seg_video(item["video"], item["dur"], p, start=item.get("start", 0.0), retime=item.get("retime", False), fade=item.get("fade", False), crop_frac=item.get("crop"))
        tmp.append(p)
    silent = out.with_name(out.stem + "_silent.mp4")
    concat_segments(tmp, silent, reencode=True)
    if not vo:
        os.replace(silent, out)
        return
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-loglevel",
            "error",
            "-i",
            str(silent),
            "-i",
            str(vo),
            "-t",
            f"{durof(silent):.3f}",
            "-map",
            "0:v",
            "-map",
            "1:a",
            "-af",
            "apad",
            "-c:v",
            "copy",
            "-c:a",
            "aac",
            "-b:a",
            "192k",
            *AUD,
            str(out),
        ],
        check=True,
    )


def make_card(out, text, sub, dur, vo=None):
    overlay = out.with_suffix(".png")
    make_title_png(overlay, text, sub)
    live = OLD_MOTION / "plate_live.mp4"
    seg_video(live, dur, out.with_name(out.stem + "_bg.mp4"), retime=True, fade=True)
    bg = out.with_name(out.stem + "_bg.mp4")
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-i", str(bg), "-loop", "1", "-i", str(overlay)]
    cmd += ["-i", str(vo)] if vo else ["-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo"]
    subprocess.run(
        cmd
        + [
            "-t",
            f"{dur:.2f}",
            "-filter_complex",
            f"[1:v]format=rgba,fade=t=in:st=0:d=0.25:alpha=1,fade=t=out:st={max(0, dur - 0.35):.2f}:d=0.3:alpha=1[t];[0:v][t]overlay,format=yuv420p[v]",
            "-map",
            "[v]",
            "-map",
            "2:a",
            "-af",
            "apad",
            "-c:v",
            "libx264",
            "-crf",
            "18",
            "-c:a",
            "aac",
            "-b:a",
            "192k",
            *AUD,
            str(out),
        ],
        check=True,
    )


def _heart_points(cx, cy, size):
    pts = []
    for i in range(80):
        t = math.pi * 2 * i / 80
        x = 16 * math.sin(t) ** 3
        y = -(13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t))
        pts.append((cx + x * size / 18, cy + y * size / 18))
    return pts


def make_science_hearts(out, dur=5.04, vo=None):
    """Moving non-text science payoff: three pulsing hearts + blue blood shimmer."""
    frames = ASM / "_science_frames"
    frames.mkdir(exist_ok=True)
    n = int(round(dur * FPS))
    for i in range(n):
        phase = i / max(1, n - 1)
        img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        d = ImageDraw.Draw(img, "RGBA")
        d.rectangle((0, 0, W, H), fill=(0, 32, 70, 72))
        for k, (cx, cy) in enumerate(((500, 265), (640, 220), (780, 265))):
            pulse = 1.0 + 0.16 * math.sin(phase * math.pi * 8 + k * 0.9)
            pts = _heart_points(cx, cy, 82 * pulse)
            d.polygon(pts, fill=(70, 190, 255, 168), outline=(220, 248, 255, 220))
            d.line(pts + [pts[0]], fill=(220, 248, 255, 220), width=3)
        # blue-blood current, intentionally iconographic rather than text.
        for k in range(5):
            x0 = 320 + k * 150 + math.sin(phase * math.pi * 2 + k) * 20
            y0 = 420 + math.sin(phase * math.pi * 4 + k) * 18
            d.arc((x0, y0, x0 + 170, y0 + 75), 190, 350, fill=(60, 170, 255, 138), width=8)
        img.save(frames / f"f_{i:04d}.png")

    bg = OLD_MOTION / "a5_32_science.mp4"
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-loglevel",
            "error",
            "-i",
            str(bg),
            "-framerate",
            str(FPS),
            "-i",
            str(frames / "f_%04d.png"),
            "-i",
            str(vo) if vo else "anullsrc=r=48000:cl=stereo",
            "-t",
            f"{dur:.2f}",
            "-filter_complex",
            f"[0:v]{FILL},eq=brightness=-0.015:saturation=1.05[bg];[1:v]format=rgba[ov];[bg][ov]overlay,format=yuv420p[v]",
            "-map",
            "[v]",
            "-map",
            "2:a",
            "-af",
            "apad",
            "-c:v",
            "libx264",
            "-crf",
            "18",
            "-c:a",
            "aac",
            "-b:a",
            "192k",
            *AUD,
            str(out),
        ],
        check=True,
    )


def make_camo_shimmer(out, dur=5.44, vo=None):
    """Animated macro skin camouflage from the approved no-face, no-mouth still."""
    src = OUTROOT / "keyframes/a1_08_camo_v2.png"
    base = ImageOps.fit(Image.open(src).convert("RGB"), (W, H), method=Image.Resampling.LANCZOS)
    frames = ASM / "_camo_frames"
    frames.mkdir(exist_ok=True)
    n = int(round(dur * FPS))
    palette = [
        (45, 35, 78),
        (82, 54, 132),
        (31, 112, 132),
        (148, 92, 42),
        (210, 174, 92),
    ]
    speckles = []
    for i in range(220):
        x = (i * 73 + 41) % W
        y = (i * 191 + 17) % H
        r = 3 + (i * 11) % 16
        phase = (i * 0.73) % (math.pi * 2)
        speckles.append((x, y, r, phase, palette[i % len(palette)]))

    for i in range(n):
        t = i / max(1, n - 1)
        zoom = 1.025 + 0.012 * math.sin(t * math.pi * 2)
        zw, zh = int(W * zoom), int(H * zoom)
        pan_x = int((zw - W) * (0.5 + 0.32 * math.sin(t * math.pi * 2.4)))
        pan_y = int((zh - H) * (0.5 + 0.24 * math.cos(t * math.pi * 1.8)))
        img = base.resize((zw, zh), Image.Resampling.LANCZOS).crop((pan_x, pan_y, pan_x + W, pan_y + H)).convert("RGBA")
        overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        d = ImageDraw.Draw(overlay, "RGBA")
        for x, y, r, phase, color in speckles:
            pulse = 0.5 + 0.5 * math.sin(t * math.pi * 7.5 + phase)
            rr = r * (0.65 + 0.55 * pulse)
            alpha = int(18 + 42 * pulse)
            drift_x = 7 * math.sin(t * math.pi * 2 + phase)
            drift_y = 5 * math.cos(t * math.pi * 2.6 + phase)
            d.ellipse((x + drift_x - rr, y + drift_y - rr, x + drift_x + rr, y + drift_y + rr), fill=(*color, alpha))
        for k in range(9):
            y = (k * 96 + t * 230) % (H + 130) - 65
            d.arc((-80, y, W + 80, y + 170), 188, 350, fill=(118, 205, 255, 42), width=4)
        Image.alpha_composite(img, overlay).convert("RGB").save(frames / f"f_{i:04d}.png")

    cmd = [
        "ffmpeg",
        "-y",
        "-loglevel",
        "error",
        "-framerate",
        str(FPS),
        "-i",
        str(frames / "f_%04d.png"),
    ]
    cmd += ["-i", str(vo)] if vo else ["-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo"]
    cmd += [
        "-t",
        f"{dur:.2f}",
        "-vf",
        "format=yuv420p",
        "-af",
        "apad",
        "-map",
        "0:v",
        "-map",
        "1:a",
        "-c:v",
        "libx264",
        "-crf",
        "18",
        "-c:a",
        "aac",
        "-b:a",
        "192k",
        *AUD,
        str(out),
    ]
    subprocess.run(cmd, check=True)


def old_seg(name):
    matches = sorted(OLD_ASM.glob(f"*_{name}.mp4"))
    if not matches:
        raise FileNotFoundError(name)
    return matches[0]


def motion(name):
    p = V7_MOTION / f"{name}.mp4"
    if p.exists():
        return p
    p = OLD_MOTION / f"{name}.mp4"
    if p.exists():
        return p
    p = OLD_SCRATCH_MOTION / f"{name}.mp4"
    if p.exists():
        return p
    raise FileNotFoundError(name)


def build():
    chase_audio = make_chase_audio()
    segs = []

    def add(sid, maker):
        out = SEG / f"{len(segs):02d}_{sid}.mp4"
        maker(out)
        segs.append(out)
        print(f"{len(segs)-1:02d} {sid}: {durof(out):.2f}s", flush=True)

    add("a0_01_establish", lambda out: title_establish(out, 4.0))
    add("a0_02_boop", lambda out: seg_video(motion("a0_02_boop"), 4.0, out, fade=True))
    add("a0_03_eye", lambda out: seg_video(OLD_SCRATCH_MOTION / "s03_rock_eye_motion.mp4", 4.0, out, fade=True))
    add("a0_04_ink_reaction", lambda out: make_composite("a0_04_ink_reaction", [
        {"video": OLD_SCRATCH_MOTION / "s03_rock_eye_motion.mp4", "dur": 1.2, "start": 2.6, "fade": True},
        {"video": motion("a2_13_realize"), "dur": 3.84, "vo": VO / "B_hook2.mp3", "retime": True, "fade": True},
    ], out))
    add("a1_06_reintro", lambda out: seg_video(motion("a3_14_stoplook"), 5.6, out, vo=VO / "N_intro.mp3", retime=True, fade=True))
    add("a1_07_chase", lambda out: make_composite("a1_07_chase", [
        {"video": motion("a0_02_boop"), "dur": 1.7, "start": 0.8, "fade": True},
        {"video": motion("a1_07_chase"), "dur": 2.2, "start": 0.0, "vo": chase_audio, "fade": True},
        {"video": motion("a1_09_lunge"), "dur": 3.2, "start": 0.7, "fade": True},
    ], out))
    add("a1_08_camo", lambda out: make_camo_shimmer(out, 5.44, vo=VO / "N_camo.mp3"))
    add("a1_09_lunge", lambda out: seg_video(motion("a1_09_lunge"), 5.0, out, fade=True))
    add("a2_10_corner", lambda out: seg_video(motion("a2_10_corner_v2"), 5.0, out, fade=True))
    add("a2_11_bolt", lambda out: seg_video(OLD_MOTION / "a2_11_bolt.mp4", 5.0, out, fade=True))
    add("a2_12_eelstir", lambda out: seg_video(OLD_MOTION / "a2_12_eelstir.mp4", 3.0, out, fade=True))
    add("a2_13_realize", lambda out: seg_video(motion("a2_13_realize"), 2.17, out, vo=VO / "B_realize.mp3", retime=True, fade=True))
    add("a3_15_settle", lambda out: seg_video(motion("a3_14_stoplook"), 3.0, out, start=0.4, fade=True))
    add("a3_14_stoplook", lambda out: seg_video(motion("a3_14_stoplook"), 3.5, out, vo=VO / "B_stoplook.mp3", retime=True, fade=True))
    add("a3_16_emerge", lambda out: seg_video(OLD_SCRATCH_MOTION / "s14_emergence_motion.mp4", 5.0, out, fade=True))
    add("a3_17_stopped", lambda out: seg_video(OLD_SCRATCH_MOTION / "s14_emergence_motion.mp4", 1.25, out, vo=VO / "I_stopped.mp3", start=2.8, fade=True))
    add("a3_18_why", lambda out: seg_video(motion("a3_18_why"), 1.96, out, vo=VO / "B_why.mp3", retime=True, fade=True))
    add("a3_20_pre_twoshot", lambda out: seg_video(motion("a3_18_why"), 2.0, out, start=0.2, fade=True))
    add("a3_19_hide", lambda out: make_composite("a3_19_hide", [
        {"video": OLD_SCRATCH_MOTION / "s14_emergence_motion.mp4", "dur": 3.5, "vo": VO / "I_hide.mp3", "fade": True},
        {"video": motion("a3_18_why"), "dur": 3.5, "start": 0.8, "fade": True},
        {"video": OLD_SCRATCH_MOTION / "s16_exchange_motion.mp4", "dur": 4.63, "retime": True, "fade": True},
    ], out))
    add("a3_20_twoshot", lambda out: seg_video(motion("a3_18_why"), 4.0, out, start=0.7, fade=True))
    add("a3_21_snackpouch", lambda out: seg_video(motion("a3_21_snackpouch"), 7.21, out, vo=VO / "B_snackpouch.mp3", retime=True, fade=True))
    add("a3_22_confess", lambda out: make_composite("a3_22_confess", [
        {"video": OLD_SCRATCH_MOTION / "s16_exchange_motion.mp4", "dur": 4.8, "vo": VO / "I_confess.mp3", "fade": True},
        {"video": OLD_MOTION / "a2_12_eelstir.mp4", "dur": 3.2, "start": 0.8, "fade": True},
        {"video": motion("a3_21_snackpouch"), "dur": 3.2, "start": 1.5, "fade": True},
        {"video": OLD_SCRATCH_MOTION / "s14_emergence_motion.mp4", "dur": 3.22, "start": 1.2, "fade": True},
    ], out))
    add("a3_23_colorchange", lambda out: seg_video(motion("a3_23_colorchange"), 5.0, out, fade=True))
    add("a3_24_youdidme", lambda out: seg_video(motion("a3_24_youdidme"), 6.75, out, vo=VO / "B_colorgame.mp3", retime=True, fade=True))
    add("a4_24b_shadow_trigger", lambda out: seg_video(OLD_MOTION / "a2_12_eelstir.mp4", 1.2, out, start=1.2, fade=True))
    add("a4_25_wedged", lambda out: seg_video(OUTROOT / "keyframes/a4_25_wedged_v2.png", 2.4, out, vo=VO / "I_hurt.mp3", fade=True))
    add("a4_27_breathe", lambda out: seg_video(motion("a4_27_breathe"), 9.33, out, vo=VO / "B_breathe.mp3", retime=True, fade=True))
    add("a4_28_squeeze", lambda out: make_composite("a4_28_squeeze", [
        {"video": OUTROOT / "keyframes/a4_25_wedged_v2.png", "dur": 1.65, "vo": VO / "N_boneless.mp3", "fade": True},
        {"video": motion("a4_27_breathe"), "dur": 1.55, "start": 2.1, "fade": True},
        {"video": OLD_MOTION / "a4_29_reform.mp4", "dur": 2.16, "retime": True, "fade": True},
    ], out))
    add("a4_29_reform", lambda out: seg_video(OLD_MOTION / "a4_29_reform.mp4", 4.0, out, fade=True))
    add("a5_30_pawhold", lambda out: seg_video(motion("a5_30_pawhold"), 5.04, out, fade=True))
    add("a5_31_button", lambda out: make_composite("a5_31_button", [
        {"video": motion("a5_31_button"), "dur": 4.8, "vo": VO / "B_button.mp3", "fade": True},
        {"video": motion("a5_30_pawhold"), "dur": 5.08, "start": 0.2, "fade": True},
    ], out))
    add("a5_32_science", lambda out: make_science_hearts(out, 5.04, vo=VO / "N_hearts.mp3"))
    add("a6_33_message", lambda out: seg_video(OLD_MOTION / "a6_34_ants.mp4", 3.75, out, vo=VO / "I_gathering.mp3", retime=True, fade=True))
    add("a6_34_ants", lambda out: seg_video(OLD_MOTION / "a6_34_ants.mp4", 5.04, out, fade=True))
    add("a6_35_whereGoing", lambda out: seg_video(motion("a6_35_whereGoing"), 2.71, out, vo=VO / "B_ants.mp3", retime=True, fade=True))
    add("a6_36_teasecard", lambda out: make_card(out, "NEXT TIME", "The Ant City Beneath Our Feet", 3.0))
    add("a6_37_outro", lambda out: make_card(out, "Subscribe for the next adventure", "", 5.04, vo=VO / "N_outro.mp3"))

    concat_segments(segs, ASM / "EP2_v7_PICTURE_DIALOGUE.mp4", reencode=True)
    print(f"PICTURE+DIALOGUE -> {ASM / 'EP2_v7_PICTURE_DIALOGUE.mp4'} {durof(ASM / 'EP2_v7_PICTURE_DIALOGUE.mp4'):.2f}s")


if __name__ == "__main__":
    build()
