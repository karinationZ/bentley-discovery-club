#!/usr/bin/env python3
"""EP2 v13 — line-level paced cut (all 6 pods). Bentley lines = lip-synced talking CUs (Avatar pass);
Indi/Narrator lines = held scene shots. Shot-reverse-shot, each held for its full line. Folds in the
defect-list fixes (camo de-loop, 1:20 chase, 2:05 eyes-open via the calm CU, distinct sub-ranges to kill
loops/statics). Driven by vo_timing.json. Run: python3 scratch/ep2/final_v13/assemble_v13.py
"""
import json, subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path("/project")
OUT = ROOT / "scratch/ep2/final_v13"; SEG = OUT / "segs"
for d in (OUT, SEG):
    d.mkdir(parents=True, exist_ok=True)
W, H, FPS = 1280, 720, 24
AUD = ["-ar", "48000", "-ac", "2"]
TAIL = 0.25
FILL = f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},setsar=1"
ENC = ["-c:v", "libx264", "-crf", "17", "-pix_fmt", "yuv420p", "-r", str(FPS)]
TIMING = {e["label"]: e for e in json.load(open(ROOT / "scratch/ep2/restart_v3/vo/vo_timing.json"))["label_audio"]}

DIRS = {
    "AVATAR": ROOT / "scratch/ep2/talking_v13/avatars", "POD1": ROOT / "scratch/ep2/restart_v3/motion",
    "HERO": ROOT / "scratch/ep2/hero", "H1": ROOT / "scratch/ep2/h1_camo", "BR1": ROOT / "scratch/ep2/final_v8/bridge1",
    "AVATAR_INDI": ROOT / "scratch/ep2/talking_v13/indi_avatars",
    "TWOSHOT": ROOT / "scratch/ep2/twoshots",
}
# fresh speaker-talks/listener-still two-shots (override CU only when the shot exists)
TWOSHOTS = {"P1_B03", "P2_B01", "P3_B01", "P4_B03", "P5_B05", "P6_B01", "P1_I04", "P2_I04", "P5_I06", "P6_I05", "P6_I01"}  # P3_I01 is multi-piece (7s line) in PMAP
# Indi DIALOGUE lines -> talking CU (only if the avatar exists; her reveal lines keep scene shots from PMAP)
INDI_CU = {"P1_I02", "P1_I05", "P1_I06", "P2_I04", "P2_I05", "P2_I06", "P3_I01",
           "P3_I04", "P4_I02", "P4_I03", "P4_I04", "P4_I05", "P5_I01", "P5_I04", "P5_I05", "P5_I02", "P5_I03", "P5_I06",
           "P5_I08", "P6_I01", "P6_I02", "P6_I03", "P6_I04", "P6_I05", "P6_I08"}  # P1_I01/I03/I04/I05 + P4_I01 -> two-shots/tag
SEARCH = [ROOT / "scratch/ep2/final_v7/motion", ROOT / "assets/pilot_shots/ep2/motion", ROOT / "scratch/ep2/motion"]
PLATE = ROOT / "assets/pilot_shots/ep2/motion/plate_live.mp4"


def durof(p):
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)]).decode().strip())


def src(spec):
    if "/" in spec:
        base, n = spec.split("/", 1)
        if base == "HERO":
            return DIRS[base] / f"{n}/{n}.mp4"
        if base == "TWOSHOT":
            return DIRS[base] / f"{n}/shot.mp4"
        return DIRS[base] / f"{n}.mp4"
    for d in SEARCH:
        p = d / f"{spec}.mp4"
        if p.exists():
            return p
    raise FileNotFoundError(spec)


# (source, start). Bentley lines -> AVATAR talking CUs. Indi/Narr -> held scene shots (distinct sub-ranges).
PMAP = {
    # POD 1 — cold open
    "P1_B01": [("POD1/p01_s01_boop", 0), ("AVATAR/P1_B01", 0)], "P1_B02": ("AVATAR/P1_B02", 0), "P1_I01": ("POD1/p01_s02_eye", 0),
    "P1_B03": ("AVATAR/P1_B03", 0), "P1_I02": ("POD1/p01_s03_winkers", 0), "P1_B04": ("AVATAR/P1_B04", 0),
    "P1_I03": ("POD1/p01_s03_winkers", 1.5), "P1_B05": ("AVATAR/P1_B05", 0), "P1_I04": ("POD1/p01_s05_found_rules", 0),
    "P1_B06": ("AVATAR/P1_B06", 0), "P1_I05": ("POD1/p01_s01_boop", 2.0), "P1_B07": ("AVATAR/P1_B07", 0),
    "P1_I06": ("POD1/p01_s02_eye", 2.0),  # swapped off p01_s06_no_boop AND p01_s04_names (both star-finger)
    # POD 2 — hide-and-seek + camo (0:47 de-loop: camo shown once, then different footage)
    "P2_I01": ("H1/h1_camo", 0), "P2_B01": ("AVATAR/P2_B01", 0), "P2_B02": ("AVATAR/P2_B02", 0),
    "P2_I02": ("a1_08_camo_long", 0), "P2_I03": ("a1_08_camo_long", 3.76), "P2_B03": ("AVATAR/P2_B03", 0),
    "P2_I04": ("s16a_colorgame_motion", 0), "P2_N01": ("a1_09_lunge", 0), "P2_B04": ("AVATAR/P2_B04", 0),
    "P2_B05": ("AVATAR/P2_B05", 0), "P2_I05": ("s14_emergence_motion", 0), "P2_B06": ("AVATAR/P2_B06", 0),
    "P2_I06": ("s16_exchange_motion", 0),
    # POD 3 — the eel (1:20 chase = a real chase shot under her line)
    "P3_B01": ("AVATAR/P3_B01", 0), "P3_I01": [("TWOSHOT/P3_I01", 0), ("AVATAR_INDI/P3_I01", 0)], "P3_B02": ("AVATAR/P3_B02", 0),
    "P3_I02": ("a2_10_corner_v2", 2.5), "P3_B03": ("AVATAR/P3_B03", 0), "P3_I03": ("BR1/13_eelpath", 0),
    "P3_B04": ("AVATAR/P3_B04", 0), "P3_N01": [("a2_12_eelstir", 0), ("BR1/13_eelpath", 2.5), ("a2_11_bolt", 0)], "P3_B05": ("AVATAR/P3_B05", 0),
    "P3_I04": ("a3_23_colorchange", 0),
    # POD 4 — tag + color copy (2:05 stop = the calm eyes-open talking CU)
    "P4_I01": ("a5_30_pawhold", 0), "P4_B01": ("AVATAR/P4_B01", 0), "P4_I02": ("s22_pawhold_motion", 0),
    "P4_B02": ("AVATAR/P4_B02", 0), "P4_I03": ("a5_30_pawhold", 2.0), "P4_B03": ("AVATAR/P4_B03", 0),
    "P4_N01": [("s22_pawhold_motion", 0), ("a5_30_pawhold", 3.0)], "P4_B04": ("AVATAR/P4_B04", 0), "P4_I04": ("a3_18_why", 0),
    "P4_B05": ("AVATAR/P4_B05", 0), "P4_I05": ("a3_21_snackpouch", 0), "P4_B06": ("AVATAR/P4_B06", 0),
    "P4_I06": ("HERO/H2_extremely_bentley", 0), "P4_B07": [("a3_orange_pose", 0), ("AVATAR/P4_B07", 0)], "P4_I07": ("a3_orange_pose", 2.5),
    "P4_B08": ("AVATAR/P4_B08", 0),
    # POD 5 — escape
    "P5_I01": ("a2_12_eelstir", 2.0), "P5_B01": ("AVATAR/P5_B01", 0), "P5_I02": ("a4_25_wedged_v2", 0),
    "P5_I03": ("a4_25_wedged_v2", 2.0), "P5_B02": ("AVATAR/P5_B02", 0), "P5_B03": ("AVATAR/P5_B03", 0),
    "P5_I04": ("HERO/H6_champion", 0), "P5_B04": ("AVATAR/P5_B04", 0), "P5_I05": ("HERO/H6_champion", 2.5),
    "P5_B05": ("AVATAR/P5_B05", 0), "P5_I06": ("a4_27_breathe", 0), "P5_B06": ("AVATAR/P5_B06", 0),
    "P5_B07": ("AVATAR/P5_B07", 0), "P5_I07": ("HERO/H5_escape", 0), "P5_N01": ("a4_29_reform", 0),
    "P5_B08": ("AVATAR/P5_B08", 0), "P5_I08": ("HERO/H8_friendship", 0),
    # POD 6 — hearts + ants (3:24 blueblood = distinct sub-ranges)
    "P6_B01": ("AVATAR/P6_B01", 0), "P6_I01": ("a5_31_button", 0), "P6_B02": ("AVATAR/P6_B02", 0),
    "P6_I02": ("a5_32_science", 0), "P6_B03": ("AVATAR/P6_B03", 0), "P6_I03": ("a5_32_science", 2.5),
    "P6_N01": [("a5_32_science", 0), ("a5_31_button", 0)], "P6_B04": ("AVATAR/P6_B04", 0), "P6_I04": ("HERO/H8_friendship", 0),
    "P6_B05": ("AVATAR/P6_B05", 0), "P6_I05": ("a5_31_button", 2.5), "P6_B06": ("AVATAR/P6_B06", 0),
    "P6_I06": ("a6_34_ants", 0), "P6_B07": ("AVATAR/P6_B07", 0), "P6_I07": ("a6_35_whereGoing", 1.0),
    "P6_B08": ("AVATAR/P6_B08", 0), "P6_I08": ("a6_35_whereGoing", 0), "P6_B09": ("AVATAR/P6_B09", 0),
    "P6_N02": [("a6_35_whereGoing", 0), ("a6_34_ants", 3.0)],
}


def build_seg(label):
    """Multi-piece: split the line across its clip(s); gently retime (<=1.35x) any piece shorter than its
    share; tiny clone-pad only for residual. No frozen last frames, no loops."""
    info = TIMING[label]; aud = info["path"]; dur = durof(aud) + TAIL
    if label in TWOSHOTS and (DIRS["TWOSHOT"] / f"{label}/shot.mp4").exists():
        pieces = [(f"TWOSHOT/{label}", 0)]       # fresh speaker-talks two-shot
    elif label in INDI_CU and (DIRS["AVATAR_INDI"] / f"{label}.mp4").exists():
        pieces = [(f"AVATAR_INDI/{label}", 0)]   # selective Indi talking CU
    else:
        pieces = PMAP[label]
    if isinstance(pieces, tuple):
        pieces = [pieces]
    n = len(pieces); pdur = dur / n
    out = SEG / f"{label}.mp4"
    in_args, vf = [], []
    for i, (spec, start) in enumerate(pieces):
        p = src(spec); avail = max(0.1, durof(p) - start); take = min(pdur, avail)
        if start:
            in_args += ["-ss", f"{start:.3f}"]
        in_args += ["-t", f"{take + 0.06:.3f}", "-i", str(p)]
        rt = min(1.35, pdur / take) if take < pdur - 0.02 else 1.0
        sp = f",setpts={rt:.4f}*PTS" if rt > 1.002 else ""
        crop = "crop=iw:ih*0.84:0:0," if spec.startswith("AVATAR") else ""  # drop bottom 16% (baked Avatar captions; P4_B01 leaked at 10%)
        vf.append(f"[{i}:v]{crop}{FILL}{sp},fps={FPS},format=yuv420p[v{i}]")
    in_args += ["-i", str(aud)]
    cat = "".join(f"[v{i}]" for i in range(n))
    fc = ";".join(vf) + f";{cat}concat=n={n}:v=1:a=0[vc];[vc]tpad=stop_mode=clone:stop_duration=2,format=yuv420p[vout]"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *in_args, "-filter_complex", fc,
                    "-map", "[vout]", "-map", f"{n}:a", "-af", "apad", "-t", f"{dur:.3f}",
                    *ENC, "-c:a", "aac", "-b:a", "192k", *AUD, str(out)], check=True)
    return out


def make_card_png(text, sub, out):
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    try:
        f1 = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Rounded Bold.ttf", 72)
        f2 = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Rounded Bold.ttf", 38)
    except Exception:
        f1 = f2 = ImageFont.load_default()
    tw = d.textlength(text, font=f1); d.text(((W - tw) / 2, H * 0.38), text, fill=(255, 222, 120, 255), font=f1, stroke_width=5, stroke_fill=(20, 12, 0, 235))
    if sub:
        sw = d.textlength(sub, font=f2); d.text(((W - sw) / 2, H * 0.53), sub, fill=(250, 252, 255, 255), font=f2, stroke_width=3, stroke_fill=(0, 8, 18, 225))
    img.save(out)


def build_card_seg(name, text, sub, dur, vo=None, title_fade=None, bg=None):
    tp = SEG / f"_card_{name}.png"; make_card_png(text, sub, tp)
    tf = title_fade if title_fade is not None else dur - 0.7
    voi = ["-i", str(vo)] if vo else ["-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo"]
    out = SEG / f"_{name}.mp4"
    bgp = str(bg or PLATE)
    is_img = bgp.lower().endswith((".png", ".jpg", ".jpeg"))
    bg_in = ["-loop", "1", "-i", bgp] if is_img else ["-stream_loop", "-1", "-i", bgp]
    bg_fil = (f"[0:v]scale={int(W * 1.18)}:{int(H * 1.18)},zoompan=z='min(zoom+0.0006,1.12)':d={int(dur * FPS)}:s={W}x{H}:fps={FPS},setsar=1,unsharp=5:5:0.7,eq=brightness=-0.02:saturation=1.05[bg];"
              if is_img else f"[0:v]{FILL},eq=brightness=-0.02:saturation=1.05[bg];")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *bg_in, "-loop", "1", "-i", str(tp), *voi, "-t", f"{dur:.2f}",
        "-filter_complex",
        bg_fil
        + f"[1:v]format=rgba,fade=t=in:st=0.3:d=0.5:alpha=1,fade=t=out:st={max(0.5,tf):.2f}:d=0.6:alpha=1[t];"
        + "[bg][t]overlay,format=yuv420p[v]",
        "-map", "[v]", "-map", "2:a", "-af", "apad", "-t", f"{dur:.2f}",
        *ENC, "-c:a", "aac", "-b:a", "192k", *AUD, str(out)], check=True)
    return out


def main():
    order = [l for l in TIMING if l in PMAP]
    segs, errs = [], []
    intro = ROOT / "scratch/ep2/restart_v3/vo/labels/P0_N00.mp3"
    segs.append(build_card_seg("00title", "BENTLEY'S BIG ADVENTURES", "The Octopus Escape Artist", durof(intro) + 0.4, vo=intro, title_fade=3.2, bg=OUT / "_titlebg.png"))
    for label in order:
        try:
            segs.append(build_seg(label))
        except Exception as e:
            errs.append(f"{label}: {str(e)[:80]}")
    for e in errs:
        print("  ERR", e, flush=True)
    segs.append(build_card_seg("99nexttime", "NEXT TIME", "The Ant City Beneath Our Feet", 3.6))
    lst = OUT / "_seglist.txt"; lst.write_text("\n".join(f"file '{p}'" for p in segs))
    out = OUT / "EP2_v13_PD.mp4"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy", str(out)], check=True)
    print(f"\nv13 PICTURE+DIALOGUE -> {out}  {durof(out):.1f}s ({durof(out)/60:.2f} min); {len(segs)}/{len(order)} segs, {len(errs)} errors", flush=True)


if __name__ == "__main__":
    main()
