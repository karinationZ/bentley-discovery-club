#!/usr/bin/env python3
"""Ep2 v10 — build the cinematic v2 revision (docs/series/season_1/ep2/EPISODE2_SCRIPT_v2.md §4).
Same 2-pass quality pipeline as v9 (one ffmpeg per beat: trim+retime+concat+grade+VO; concat by copy;
single final encode in mix). Changes vs v9: the v2 cue order/coverage, the new BRIDGE-CAMO shot (beat
07, swapped in once generated), the new B_lunge beat, the trimmed narrator lines, and a Bentley
catchphrase reprise on the outro card. Run: python3 scratch/ep2/final_v10/assemble_v10.py
"""
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path("/project")
OUTROOT = ROOT / "scratch/ep2/final_v10"
ASM = OUTROOT / "assembly"
SEG = ASM / "segs"
for d in (ASM, SEG):
    d.mkdir(parents=True, exist_ok=True)

W, H, FPS = 1280, 720, 24
AUD = ["-ar", "48000", "-ac", "2"]
TAIL = 0.30
FILL = f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},setsar=1"
ENC = ["-c:v", "libx264", "-crf", "16", "-pix_fmt", "yuv420p", "-x264-params", "keyint=48:min-keyint=48", "-r", str(FPS)]
VO = ROOT / "scratch/ep2/vo"
V7 = ROOT / "scratch/ep2/final_v7/motion"
OLD = ROOT / "assets/pilot_shots/ep2/motion"
SCR = ROOT / "scratch/ep2/motion"
BR1 = ROOT / "scratch/ep2/final_v8/bridge1"
CAMO = OUTROOT / "camo"
PLATE = OLD / "plate_live.mp4"
LIFT = "eq=brightness=0.05:saturation=1.06"


def durof(p):
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)]).decode().strip())


def src(name):
    if "/" in name:
        base, n = name.split("/", 1)
        return {"V7": V7, "OLD": OLD, "SCR": SCR, "BR1": BR1, "CAMO": CAMO}[base] / f"{n}.mp4"
    for d in (V7, OLD, SCR):
        p = d / f"{name}.mp4"
        if p.exists():
            return p
    raise FileNotFoundError(name)


def make_title(out, text, sub, dur, vo=None):
    tp = ASM / f"_t_{Path(out).stem}.png"
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
    img.save(tp)
    voi = ["-i", str(vo)] if vo else ["-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo"]
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(PLATE), "-loop", "1", "-i", str(tp), *voi,
        "-t", f"{dur:.2f}", "-filter_complex",
        f"[0:v]{FILL},eq=brightness=-0.02:saturation=1.06[bg];"
        f"[1:v]format=rgba,fade=t=in:st=0.3:d=0.5:alpha=1,fade=t=out:st={max(0,dur-0.7):.2f}:d=0.6:alpha=1[t];"
        f"[bg][t]overlay,format=yuv420p[v]",
        "-map", "[v]", "-map", "2:a", "-af", "apad", *ENC, "-c:a", "aac", "-b:a", "192k", *AUD, str(out)], check=True)
    return out


# v2 cue. pieces: [(clip,start)]. vo: label. dur: explicit secs. lift: dark beats.
CUE = [
    dict(id="01_title", kind="title", text="BENTLEY'S BIG ADVENTURES", sub="The Octopus Escape Artist", vo="B_hook1"),
    dict(id="02_eye", pieces=[("SCR/s03_rock_eye_motion", 0.4)], dur=2.6),
    dict(id="03_inkreact", pieces=[("SCR/bentley_cu_awe_motion", 0.4)], vo="B_hook2"),
    # the water-squirt is at a1_07_chase ~0.5s, so intro/chase/camo use POST-squirt ranges,
    # and the squirt plays ONCE under B_rude ("that was rude") where it's caused.
    dict(id="04_intro", pieces=[("a1_07_chase", 1.6), ("a3_14_stoplook", 0.0)], vo="N_intro"),
    dict(id="05_chase", pieces=[("a0_02_boop", 1.2), ("a1_07_chase", 2.6)], vo="B_chase"),
    dict(id="06_rude", pieces=[("a1_07_chase", 0.0)], vo="B_rude"),                 # THE squirt + flinch, under "that was rude"
    # BRIDGE-CAMO leads; N_camo (long) spreads over the morph + an Indi + a chase-miss (post-squirt)
    dict(id="07_camo", pieces=[("CAMO/07_camo", 0.0), ("OLD/a1_08_camo", 0.0), ("a1_07_chase", 2.2)], vo="N_camo"),
    dict(id="08_lunge", pieces=[("a1_09_lunge", 0.0)], vo="B_lunge"),
    dict(id="09_shell", pieces=[("a1_09_lunge", 3.2)], dur=2.0),
    dict(id="10_corner", pieces=[("a2_10_corner_v2", 0.0)], vo="B_help"),
    dict(id="11_bolt", pieces=[("OLD/a2_11_bolt", 0.0)], vo="B_eel"),
    dict(id="12_eelpath", pieces=[("BR1/13_eelpath", 0.6)], dur=3.0),
    dict(id="13_eel", pieces=[("OLD/a2_12_eelstir", 1.6)], dur=2.0),
    dict(id="14_realize", pieces=[("a2_13_realize", 0.0)], vo="B_realize"),
    dict(id="15_stoplook", pieces=[("a3_14_stoplook", 0.6)], vo="B_stoplook"),
    dict(id="16_emerge", pieces=[("SCR/s14_emergence_motion", 0.0)], dur=2.0),
    dict(id="17_creep", pieces=[("SCR/s14_emergence_motion", 2.6)], vo="I_creep"),
    dict(id="18_why", pieces=[("a3_18_why", 0.0)], vo="B_why"),
    dict(id="19_champion", pieces=[("SCR/s16a_colorgame_motion", 0.0), ("SCR/s14_emergence_motion", 0.5), ("OLD/a4_29_reform", 0.0)], vo="I_hide"),
    dict(id="20_snackpouch", pieces=[("a3_21_snackpouch", 0.0), ("SCR/s16_exchange_motion", 0.0)], vo="B_snackpouch"),
    dict(id="21_paw", pieces=[("a5_30_pawhold", 0.0), ("SCR/s22_pawhold_motion", 0.0), ("a5_30_pawhold", 2.5)], vo="N_taste", lift=True),
    dict(id="22_confess", pieces=[("SCR/s16_exchange_motion", 0.0), ("OLD/a4_29_reform", 0.0), ("SCR/s16a_colorgame_motion", 0.6)], vo="I_confess", lift=True),
    dict(id="23_colorturn", pieces=[("a3_23_colorchange", 0.0)], vo="I_colorturn"),
    dict(id="24_colorland", pieces=[("a3_23_colorchange", 2.2)], dur=2.0),
    dict(id="25_youdidme", pieces=[("a3_24_youdidme", 0.0)], vo="B_colorgame"),
    dict(id="26_play", pieces=[("SCR/s16a_colorgame_motion", 1.0), ("SCR/s14_emergence_motion", 1.0)], vo="N_friends"),
    dict(id="27_shadow", pieces=[("OLD/a2_12_eelstir", 3.2), ("a2_13_realize", 0.0)], vo="N_shadow"),
    dict(id="28_wedged", pieces=[("a4_25_wedged_v2", 0.0)], vo="I_hurt"),
    dict(id="29_breathe", pieces=[("a4_27_breathe", 0.0), ("a4_25_wedged_v2", 2.6)], vo="B_breathe"),
    dict(id="30_squeeze", pieces=[("SCR/s20_squeeze_motion", 0.0), ("OLD/a4_29_reform", 0.0)], vo="N_boneless"),
    dict(id="31_reform", pieces=[("OLD/a4_29_reform", 2.5)], dur=2.0),
    dict(id="32_button", pieces=[("a5_31_button", 0.0), ("a5_30_pawhold", 0.0)], vo="B_button"),
    dict(id="33_closer", pieces=[("OLD/a5_32_science", 0.0), ("a5_31_button", 0.0), ("SCR/s16_exchange_motion", 0.0)], vo="N_hearts", lift=True),
    dict(id="34_gathering", pieces=[("OLD/a6_34_ants", 0.0)], vo="I_gathering"),
    dict(id="35_ants", pieces=[("OLD/a6_34_ants", 2.6)], dur=3.0),
    dict(id="36_wheregoing", pieces=[("a6_35_whereGoing", 0.0)], vo="B_ants"),
    dict(id="37_outro", kind="card", text="NEXT TIME", sub="The Ant City Beneath Our Feet", vo="_outro_v10"),
]


def build_beat(beat):
    bid = beat["id"]; out = SEG / f"{bid}.mp4"
    kind = beat.get("kind", "beat")
    vo = (VO / f"{beat['vo']}.mp3") if beat.get("vo") else None
    if kind in ("title", "card"):
        dur = (durof(vo) + TAIL) if vo else beat.get("dur", 4.0)
        return make_title(out, beat["text"], beat["sub"], dur, vo=vo)
    target = (durof(vo) + TAIL) if vo else beat["dur"]
    pieces = beat["pieces"]; n = len(pieces); pdur = target / n
    in_args, vf = [], []
    for i, (cname, start) in enumerate(pieces):
        p = src(cname); avail = max(0.1, durof(p) - start); take = min(pdur, avail)
        if start:
            in_args += ["-ss", f"{start:.3f}"]
        in_args += ["-t", f"{take + 0.06:.3f}", "-i", str(p)]
        rt = min(1.35, pdur / take) if take < pdur - 0.02 else 1.0
        sp = f",setpts={rt:.4f}*PTS" if rt > 1.002 else ""
        vf.append(f"[{i}:v]{FILL}{sp},fps={FPS},format=yuv420p[v{i}]")
    aidx = n
    in_args += ["-i", str(vo)] if vo else ["-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo"]
    cat = "".join(f"[v{i}]" for i in range(n))
    post = f"[vc]{LIFT},format=yuv420p[vout]" if beat.get("lift") else "[vc]format=yuv420p[vout]"
    fc = ";".join(vf) + f";{cat}concat=n={n}:v=1:a=0[vc];" + post
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *in_args, "-filter_complex", fc,
                    "-map", "[vout]", "-map", f"{aidx}:a", "-af", "apad", "-t", f"{target:.3f}",
                    *ENC, "-c:a", "aac", "-b:a", "192k", *AUD, str(out)], check=True)
    return out


def main():
    # build the outro VO: narrator tag + a Bentley catchphrase reprise (catchphrase stays Bentley)
    oc = VO / "_outro_v10.mp3"
    gap = ASM / "_gap.wav"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo", "-t", "0.45", str(gap)], check=True)
    lst = ASM / "_outro_list.txt"
    lst.write_text("\n".join(f"file '{p}'" for p in [VO / "N_outro.mp3", gap, VO / "B_stoplook.mp3"]))
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(lst), *AUD, str(oc)], check=True)

    # swap the generated camo shot in once it exists (else temp stand-in a1_08_camo leads)
    if (CAMO / "07_camo.mp4").exists():
        for b in CUE:
            if b["id"] == "07_camo":
                b["pieces"][0] = ("CAMO/07_camo", 0.0)
                print("  [camo] using generated 07_camo.mp4", flush=True)
    else:
        for b in CUE:
            if b["id"] == "07_camo":
                b["pieces"] = [("OLD/a1_08_camo", 0.0), ("a1_07_chase", 1.0)]   # TEMP until BRIDGE-CAMO lands
                print("  [camo] TEMP stand-in (BRIDGE-CAMO not generated yet)", flush=True)

    segs = []
    for beat in CUE:
        f = build_beat(beat)
        segs.append(f)
        print(f"  {beat['id']:14s} {durof(f):5.1f}s", flush=True)
    lst2 = ASM / "_seglist.txt"; lst2.write_text("\n".join(f"file '{p}'" for p in segs))
    out = ASM / "EP2_v10_PICTURE_DIALOGUE.mp4"
    r = subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(lst2), "-c", "copy", str(out)])
    if r.returncode != 0 or abs(durof(out) - sum(durof(s) for s in segs)) > 1.0:
        print("  [concat] copy failed -> re-encoding once", flush=True)
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(lst2), *ENC, "-c:a", "aac", "-b:a", "192k", *AUD, str(out)], check=True)
    print(f"\nPICTURE+DIALOGUE -> {out}  {durof(out):.1f}s ({durof(out)/60:.2f} min)", flush=True)


if __name__ == "__main__":
    main()
