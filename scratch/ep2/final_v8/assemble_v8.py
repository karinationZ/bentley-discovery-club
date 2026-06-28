#!/usr/bin/env python3
"""Ep2 v8 — STORY-REPAIR re-cut driven by docs/series/season_1/ep2/EP2_STORY_REPAIR_EDL.md.

What changed vs v7 (the source of the owner's notes):
  * NO per-segment fade-to-black. Hard cuts between clean segments + one global fade in/out only.
  * NO reused frames: where a clip recurs it is a DIFFERENT (start) window.
  * Recorded ORDER restored incl. the 4 dropped lines (B_hook1, B_help, N_taste, N_friends).
  * Act-2 causal hinge rebuilt (corner->bolt->INTO-EEL->eel->realize).
  * Every line plays over its SPEAKER, kept alive; long lines covered by multiple angles of the
    same speaker (no loop, no >1.3x slow-mo).

Three beats use TEMP stand-ins until their final asset lands (search "TEMP"):
  * 08_camo  -> improved procedural camo (pending)        -> stand-in: a1_08_camo
  * 13_eelpath -> BRIDGE-1 generated Indi+eel shot (pending) -> stand-in: bolt-tail + eelstir-head
  * 34_hearts -> three-hearts motion-graphic (pending)    -> stand-in: a5_32_science

Inputs are read-only. Output: scratch/ep2/final_v8/assembly/EP2_v8_PICTURE_DIALOGUE.mp4
Run: python3 scratch/ep2/final_v8/assemble_v8.py
"""
import os, subprocess
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = Path("/project")
OUTROOT = ROOT / "scratch/ep2/final_v8"
ASM = OUTROOT / "assembly"
SEG = ASM / "segs"
PCS = ASM / "_pieces"
for d in (ASM, SEG, PCS):
    d.mkdir(parents=True, exist_ok=True)

W, H, FPS = 1280, 720, 24
AUD = ["-ar", "48000", "-ac", "2"]
TAIL = 0.30                       # breath after a line
FILL = f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},setsar=1"
VO = ROOT / "scratch/ep2/vo"
V7 = OUTROOT.parent / "final_v7/motion"
OLD = ROOT / "assets/pilot_shots/ep2/motion"
SCR = ROOT / "scratch/ep2/motion"
GFX = OUTROOT / "gfx"        # procedural camo/hearts (make_gfx_v8.py)
BR1 = OUTROOT / "bridge1"    # generated eel+Indi shot (generate_bridge1.py)
PLATE = OLD / "plate_live.mp4"


def durof(p):
    return float(subprocess.check_output(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)]).decode().strip())


def src(name):
    """Resolve a short clip name to a path, preferring approved V7 > OLD > SCR."""
    if "/" in name:
        base, n = name.split("/", 1)
        d = {"V7": V7, "OLD": OLD, "SCR": SCR, "GFX": GFX, "BR1": BR1}[base]
        return d / f"{n}.mp4"
    for d in (GFX, BR1, V7, OLD, SCR):
        p = d / f"{name}.mp4"
        if p.exists():
            return p
    raise FileNotFoundError(name)


# ---------- low-level builders ----------
def render_piece(path, start, dur, out):
    avail = max(0.1, durof(path) - start)
    d = min(dur, avail)
    cmd = ["ffmpeg", "-y", "-loglevel", "error"]
    if start:
        cmd += ["-ss", f"{start:.3f}"]
    cmd += ["-i", str(path), "-t", f"{d:.3f}", "-an", "-vf", f"{FILL},format=yuv420p",
            "-r", str(FPS), "-c:v", "libx264", "-crf", "18", str(out)]
    subprocess.run(cmd, check=True)
    return out


def concat_videos(parts, out, reencode=True):
    lst = out.with_suffix(".txt")
    lst.write_text("\n".join(f"file '{p}'" for p in parts))
    if reencode:
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(lst),
                        "-r", str(FPS), "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", "-an", str(out)], check=True)
    else:
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(lst),
                        "-c", "copy", str(out)], check=True)
    return out


def pad_video(video, dur, out):
    cur = durof(video)
    if cur < dur - 0.04:
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(video), "-vf",
                        f"tpad=stop_mode=clone:stop_duration={dur - cur:.3f}", "-r", str(FPS),
                        "-c:v", "libx264", "-crf", "18", "-an", str(out)], check=True)
    else:
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(video), "-t", f"{dur:.3f}",
                        "-c", "copy", "-an", str(out)], check=True)
    return out


def mux(video, dur, out, vo=None):
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-i", str(video)]
    cmd += ["-i", str(vo)] if vo else ["-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo"]
    cmd += ["-t", f"{dur:.3f}", "-map", "0:v", "-map", "1:a", "-af", "apad",
            "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", *AUD, str(out)]
    subprocess.run(cmd, check=True)
    return out


# ---------- grade (port of v7: normalize toward neutral daylight; mood/colour beats exempt) ----------
GRADE_EXEMPT = ("01_title", "38_teasecard", "39_outro", "08_camo", "24_blush", "25_youdidme",
                "12_bolt", "13_eelpath", "14_eel", "27_shadow")
GRADE_DARK = {"12_bolt": 40, "13_eelpath": 38, "14_eel": 36, "27_shadow": 38}


def grade(path, bid):
    if any(bid.endswith(e) or bid == e for e in GRADE_EXEMPT):
        return
    tV = GRADE_DARK.get(bid, 57); tS = 32
    d = durof(path); fr = path.with_name(path.stem + "_probe.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{d/2:.2f}", "-i", str(path),
                    "-frames:v", "1", "-vf", "scale=240:-1", str(fr)], check=True)
    im = np.asarray(Image.open(fr).convert("HSV")).astype(float); fr.unlink()
    V = im[..., 2].mean() / 255 * 100; S = im[..., 1].mean() / 255 * 100
    db = max(-0.16, min(0.16, (tV - V) / 100 * 0.85))
    ms = max(0.78, min(1.45, (tS / max(S, 1.0)) ** 0.6))
    if abs(db) < 0.02 and 0.94 < ms < 1.06:
        return
    tmp = path.with_name(path.stem + "_g.mp4")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(path), "-vf",
                    f"eq=brightness={db:.3f}:saturation={ms:.3f}", "-c:v", "libx264", "-crf", "18",
                    "-pix_fmt", "yuv420p", "-c:a", "copy", str(tmp)], check=True)
    os.replace(tmp, path)


# ---------- title + card ----------
def _title_png(out, text, sub):
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
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
    img.save(out)


def make_title(out, text, sub, dur, vo=None):
    tp = ASM / f"_t_{Path(out).stem}.png"; _title_png(tp, text, sub)
    bg = PLATE
    sub_in = ["-i", str(bg)] if str(bg).endswith(".mp4") else ["-loop", "1", "-i", str(bg)]
    voi = ["-i", str(vo)] if vo else ["-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo"]
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *sub_in, "-loop", "1", "-i", str(tp), *voi,
        "-t", f"{dur:.2f}", "-filter_complex",
        f"[0:v]{FILL},eq=brightness=-0.02:saturation=1.06[bg];"
        f"[1:v]format=rgba,fade=t=in:st=0.3:d=0.5:alpha=1,fade=t=out:st={max(0,dur-0.7):.2f}:d=0.6:alpha=1[t];"
        f"[bg][t]overlay,format=yuv420p[v]",
        "-map", "[v]", "-map", "2:a", "-af", "apad", "-r", str(FPS),
        "-c:v", "libx264", "-crf", "18", "-c:a", "aac", "-b:a", "192k", *AUD, str(out)], check=True)
    return out


# ---------- the cue sheet (EDL) ----------
# kind: beat | title | card.  pieces: list of (clipname, start).  vo: label or None.  dur: explicit secs.
CUE = [
    dict(id="01_title", kind="title", text="BENTLEY'S BIG ADVENTURES", sub="The Octopus Escape Artist", dur=4.0),
    dict(id="02_boop", pieces=[("a0_02_boop", 0.0)], vo="B_hook1"),
    dict(id="03_eye", pieces=[("SCR/s03_rock_eye_motion", 0.4)], dur=2.6),
    dict(id="04_inkreact", pieces=[("SCR/bentley_cu_awe_motion", 0.4)], vo="B_hook2"),
    dict(id="05_intro", pieces=[("a1_07_chase", 0.0), ("a3_14_stoplook", 0.0)], vo="N_intro"),
    dict(id="06_chase", pieces=[("a0_02_boop", 1.2), ("a1_07_chase", 2.4)], vo="B_chase"),
    dict(id="07_rude", pieces=[("a1_07_chase", 3.6)], vo="B_rude"),
    dict(id="08_camo", pieces=[("camo_v8", 0.0)], vo="N_camo"),                        # improved procedural camo
    dict(id="09_lunge", pieces=[("a1_09_lunge", 0.0)], dur=3.0),
    dict(id="10_shell", pieces=[("a1_09_lunge", 3.2)], dur=1.8),
    dict(id="11_corner", pieces=[("a2_10_corner_v2", 0.0)], vo="B_help"),
    dict(id="12_bolt", pieces=[("OLD/a2_11_bolt", 0.0)], dur=2.5),
    dict(id="13_eelpath", pieces=[("OLD/a2_11_bolt", 2.6), ("OLD/a2_12_eelstir", 0.0)], dur=3.0),  # TEMP BRIDGE-1
    dict(id="14_eel", pieces=[("OLD/a2_12_eelstir", 1.6)], dur=2.0),
    dict(id="15_realize", pieces=[("a2_13_realize", 0.0)], vo="B_realize"),
    dict(id="16_stoplook", pieces=[("a3_14_stoplook", 0.6)], vo="B_stoplook"),
    dict(id="17_emerge", pieces=[("SCR/s14_emergence_motion", 0.0)], dur=2.5),
    dict(id="18_stopped", pieces=[("SCR/s14_emergence_motion", 2.6)], vo="I_stopped"),
    dict(id="19_why", pieces=[("a3_18_why", 0.0)], vo="B_why"),
    dict(id="20_champion", pieces=[("SCR/s16a_colorgame_motion", 0.0), ("SCR/s14_emergence_motion", 0.5), ("OLD/a4_29_reform", 0.0)], vo="I_hide"),
    dict(id="21_notleaving", pieces=[("a3_21_snackpouch", 0.0), ("a3_20_twoshot", 0.0)], vo="B_snackpouch"),
    dict(id="22_paw", pieces=[("a5_30_pawhold", 0.0), ("SCR/s22_pawhold_motion", 0.0), ("SCR/s16_exchange_motion", 0.5)], vo="N_taste"),
    dict(id="23_confess", pieces=[("SCR/s16_exchange_motion", 0.0), ("OLD/a4_29_reform", 0.0), ("SCR/s16a_colorgame_motion", 0.6)], vo="I_confess"),
    dict(id="24_blush", pieces=[("a3_23_colorchange", 0.0)], dur=3.0),
    dict(id="25_youdidme", pieces=[("a3_24_youdidme", 0.0), ("a3_23_colorchange", 2.2)], vo="B_colorgame"),
    dict(id="26_play", pieces=[("a3_20_twoshot", 0.6), ("SCR/s16_exchange_motion", 1.2)], vo="N_friends"),
    dict(id="27_shadow", pieces=[("OLD/a2_12_eelstir", 3.2)], dur=1.2),
    dict(id="28_wedged", pieces=[("a4_25_wedged_v2", 0.0)], vo="I_hurt"),
    dict(id="29_breathe", pieces=[("a4_27_breathe", 0.0), ("a4_25_wedged_v2", 2.6)], vo="B_breathe"),
    dict(id="30_squeeze", pieces=[("SCR/s20_squeeze_motion", 0.0)], dur=3.0),
    dict(id="31_boneless", pieces=[("SCR/s20_squeeze_motion", 2.2), ("OLD/a4_29_reform", 0.0)], vo="N_boneless"),
    dict(id="32_reform", pieces=[("OLD/a4_29_reform", 2.2)], dur=2.0),
    dict(id="33_button", pieces=[("a5_31_button", 0.0), ("a5_30_pawhold", 0.0)], vo="B_button"),
    dict(id="34_hearts", pieces=[("hearts_v8", 0.0)], vo="N_hearts"),                  # clean three-hearts gfx
    dict(id="35_gathering", pieces=[("OLD/a6_34_ants", 0.0)], vo="I_gathering"),
    dict(id="36_ants", pieces=[("OLD/a6_34_ants", 2.6)], dur=3.0),
    dict(id="37_wheregoing", pieces=[("a6_35_whereGoing", 0.0)], vo="B_ants"),
    dict(id="38_teasecard", kind="card", text="NEXT TIME", sub="The Ant City Beneath Our Feet", dur=3.0),
    dict(id="39_outro", kind="card", text="Subscribe for the next adventure", sub="", vo="N_outro"),
]


def build_beat(beat):
    bid = beat["id"]; out = SEG / f"{bid}.mp4"
    kind = beat.get("kind", "beat")
    vo = (VO / f"{beat['vo']}.mp3") if beat.get("vo") else None
    if kind == "title":
        return make_title(out, beat["text"], beat["sub"], beat.get("dur", 4.0))
    if kind == "card":
        dur = (durof(vo) + TAIL) if vo else beat.get("dur", 4.0)
        return make_title(out, beat["text"], beat["sub"], dur, vo=vo)
    # normal beat
    target = (durof(vo) + TAIL) if vo else beat["dur"]
    pieces = beat["pieces"]; pdur = target / len(pieces)
    pfiles = []
    for i, (cname, start) in enumerate(pieces):
        pf = PCS / f"{bid}_{i}.mp4"
        render_piece(src(cname), start, pdur + 0.05, pf)
        pfiles.append(pf)
    vid = concat_videos(pfiles, PCS / f"{bid}_cat.mp4") if len(pfiles) > 1 else pfiles[0]
    padded = pad_video(vid, target, PCS / f"{bid}_pad.mp4")
    mux(padded, target, out, vo=vo)
    grade(out, bid)
    return out


def main():
    # swap in the generated eel+Indi shot once it lands; else keep the temp bolt+eelstir stand-in
    if (BR1 / "13_eelpath.mp4").exists():
        for b in CUE:
            if b["id"] == "13_eelpath":
                b["pieces"] = [("BR1/13_eelpath", 0.6)]
                print("  [bridge1] using generated 13_eelpath.mp4", flush=True)
    segs = []
    for beat in CUE:
        f = build_beat(beat)
        segs.append(f)
        print(f"  {beat['id']:14s} {durof(f):4.1f}s", flush=True)
    # concat all (hard cuts), then ONE global fade in/out
    cat = concat_videos(segs, ASM / "_picdial_raw.mp4", reencode=True)
    # _picdial_raw is video-only (concat dropped audio path); rebuild with audio via concat demuxer w/ audio
    lst = ASM / "_seglist.txt"; lst.write_text("\n".join(f"file '{p}'" for p in segs))
    withaud = ASM / "_picdial_aud.mp4"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(lst),
                    "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", *AUD, str(withaud)], check=True)
    total = durof(withaud)
    out = ASM / "EP2_v8_PICTURE_DIALOGUE.mp4"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(withaud), "-vf",
                    f"fade=t=in:st=0:d=0.5,fade=t=out:st={total-0.6:.2f}:d=0.6", "-af",
                    f"afade=t=in:st=0:d=0.5,afade=t=out:st={total-0.6:.2f}:d=0.6",
                    "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", *AUD, str(out)], check=True)
    print(f"\nPICTURE+DIALOGUE -> {out}  {durof(out):.1f}s ({durof(out)/60:.2f} min)", flush=True)


if __name__ == "__main__":
    main()
