#!/usr/bin/env python3
"""Ep2 v11 — CONSOLIDATED cost-gated finish.
ChatGPT's wittier v3 script + its already-recorded v3 VO (scratch/ep2/restart_v3/vo/shots) +
Pod 1's 6 rendered hero shots, produced for the REST by REUSING the existing approved footage
library (+ my camo & eel bridges). ZERO new Kling renders. Built on the v10 2-pass pipeline.
Run: python3 scratch/ep2/final_v11/assemble_v11.py
"""
import subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path("/project")
OUTROOT = ROOT / "scratch/ep2/final_v11"
ASM = OUTROOT / "assembly"; SEG = ASM / "segs"
for d in (ASM, SEG):
    d.mkdir(parents=True, exist_ok=True)

W, H, FPS = 1280, 720, 24
AUD = ["-ar", "48000", "-ac", "2"]
TAIL = 0.30
FILL = f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},setsar=1"
ENC = ["-c:v", "libx264", "-crf", "16", "-pix_fmt", "yuv420p", "-x264-params", "keyint=48:min-keyint=48", "-r", str(FPS)]
LIFT = "eq=brightness=0.05:saturation=1.06"
VO_SHOTS = ROOT / "scratch/ep2/restart_v3/vo/shots"
POD1 = ROOT / "scratch/ep2/restart_v3/motion"
CAMO = ROOT / "scratch/ep2/final_v10/camo"
BR1 = ROOT / "scratch/ep2/final_v8/bridge1"
V7 = ROOT / "scratch/ep2/final_v7/motion"
OLD = ROOT / "assets/pilot_shots/ep2/motion"
SCR = ROOT / "scratch/ep2/motion"
PLATE = OLD / "plate_live.mp4"


def durof(p):
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)]).decode().strip())


def src(name):
    if "/" in name:
        base, n = name.split("/", 1)
        return {"POD1": POD1, "CAMO": CAMO, "BR1": BR1, "V7": V7, "OLD": OLD, "SCR": SCR}[base] / f"{n}.mp4"
    for d in (POD1, CAMO, BR1, V7, OLD, SCR):
        p = d / f"{name}.mp4"
        if p.exists():
            return p
    raise FileNotFoundError(name)


def make_card(out, text, sub, dur, vo=None):
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


# v3 cue: every beat reuses footage (or Pod1 / my bridges); vo = restart_v3 per-shot audio stem.
CUE = [
    dict(id="00_title", kind="card", text="BENTLEY'S BIG ADVENTURES", sub="The Octopus Escape Artist", dur=3.5),
    # POD 1 — ChatGPT's rendered hero shots
    dict(id="01_boop", pieces=[("POD1/p01_s01_boop", 0.0)], vo="p01_s01_boop"),
    dict(id="02_eye", pieces=[("POD1/p01_s02_eye", 0.0)], vo="p01_s02_eye"),
    dict(id="03_winkers", pieces=[("POD1/p01_s03_winkers", 0.0)], vo="p01_s03_winkers"),
    dict(id="04_names", pieces=[("POD1/p01_s04_names", 0.0)], vo="p01_s04_names"),
    dict(id="05_found_rules", pieces=[("POD1/p01_s05_found_rules", 0.0)], vo="p01_s05_found_rules"),
    dict(id="06_no_boop", pieces=[("POD1/p01_s06_no_boop", 0.0)], vo="p01_s06_no_boop"),
    # POD 2 — hide-and-seek + camo (reuse + my camo bridge)
    dict(id="07_watch", pieces=[("SCR/s16_exchange_motion", 0.0)], vo="p02_s01_watch"),
    dict(id="08_costume", pieces=[("CAMO/07_camo", 0.0), ("OLD/a1_08_camo", 0.0)], vo="p02_s02_costume"),
    dict(id="09_camo_fact", pieces=[("OLD/a1_08_camo", 2.5), ("a1_07_chase", 2.0)], vo="p02_s03_camo_fact", lift=True),
    dict(id="10_hidden", pieces=[("SCR/s16a_colorgame_motion", 0.0)], vo="p02_s04_hidden"),
    dict(id="11_smug", pieces=[("a1_09_lunge", 0.0)], vo="p02_s05_smug"),
    dict(id="12_geology", pieces=[("SCR/bentley_cu_awe_motion", 0.0)], vo="p02_s06_geology"),
    dict(id="13_shell_trail", pieces=[("a1_09_lunge", 2.0), ("SCR/s14_emergence_motion", 0.0)], vo="p02_s07_shell_trail"),
    # POD 3 — the eel (reuse + my eel bridge)
    dict(id="14_fun_mouths", pieces=[("a2_10_corner_v2", 0.0), ("SCR/s16_exchange_motion", 1.5), ("SCR/s14_emergence_motion", 2.0)], vo="p03_s01_fun_mouths"),
    dict(id="15_flashlight", pieces=[("a2_10_corner_v2", 2.0)], vo="p03_s02_flashlight"),
    dict(id="16_no_chasing", pieces=[("BR1/13_eelpath", 0.6), ("OLD/a2_11_bolt", 0.0)], vo="p03_s03_no_chasing"),
    dict(id="17_moray_fact", pieces=[("OLD/a2_12_eelstir", 0.0), ("OLD/a2_11_bolt", 2.0), ("SCR/s14_emergence_motion", 0.5)], vo="p03_s04_moray_fact"),
    dict(id="18_relief", pieces=[("a3_23_colorchange", 0.0)], vo="p03_s05_relief"),
    # POD 4 — tag + color copy
    dict(id="19_shiny_paw", pieces=[("a5_30_pawhold", 0.0), ("SCR/s22_pawhold_motion", 2.5)], vo="p04_s01_shiny_paw"),
    dict(id="20_tag_taste", pieces=[("SCR/s22_pawhold_motion", 0.0), ("a5_30_pawhold", 2.0)], vo="p04_s02_tag_taste"),
    dict(id="21_touch_fact", pieces=[("SCR/s16_exchange_motion", 1.0), ("a5_30_pawhold", 3.0)], vo="p04_s03_touch_fact", lift=True),
    dict(id="22_stop", pieces=[("a3_14_stoplook", 0.5)], vo="p04_s04_stop"),
    dict(id="23_important", pieces=[("a3_18_why", 0.0), ("a3_21_snackpouch", 0.0)], vo="p04_s05_important"),
    dict(id="24_extremely_bentley", pieces=[("a3_23_colorchange", 1.5), ("a3_24_youdidme", 2.0)], vo="p04_s06_extremely_bentley"),
    dict(id="25_brave_outfit", pieces=[("a3_24_youdidme", 0.0)], vo="p04_s07_brave_outfit"),
    # POD 5 — escape
    dict(id="26_shadow_return", pieces=[("OLD/a2_12_eelstir", 2.0)], vo="p05_s01_shadow_return"),
    dict(id="27_wedged", pieces=[("a4_25_wedged_v2", 0.0), ("a2_13_realize", 0.0)], vo="p05_s02_wedged"),
    dict(id="28_champion", pieces=[("a3_18_why", 2.0), ("a4_27_breathe", 0.0)], vo="p05_s03_champion"),
    dict(id="29_fancy_soup", pieces=[("a4_27_breathe", 0.0), ("a3_21_snackpouch", 2.5), ("a3_18_why", 3.0)], vo="p05_s04_fancy_soup"),
    dict(id="30_escape", pieces=[("SCR/s20_squeeze_motion", 0.0), ("OLD/a4_29_reform", 0.0)], vo="p05_s05_escape"),
    dict(id="31_beak_fact", pieces=[("SCR/s20_squeeze_motion", 2.5), ("OLD/a4_29_reform", 2.2)], vo="p05_s06_beak_fact", lift=True),
    dict(id="32_safe_twoshot", pieces=[("SCR/s16_exchange_motion", 2.5)], vo="p05_s07_safe_twoshot"),
    # POD 6 — hearts + ants tag
    dict(id="33_recap", pieces=[("a5_31_button", 0.0)], vo="p06_s01_recap"),
    dict(id="34_hearts", pieces=[("OLD/a5_32_science", 0.0)], vo="p06_s02_hearts"),
    dict(id="35_blueblood", pieces=[("OLD/a5_32_science", 2.5), ("a5_31_button", 2.5), ("SCR/s16_exchange_motion", 3.0)], vo="p06_s03_blueblood", lift=True),
    dict(id="36_friendship", pieces=[("a5_30_pawhold", 1.0)], vo="p06_s04_friendship"),
    dict(id="37_shell_handoff", pieces=[("SCR/s16a_colorgame_motion", 2.0)], vo="p06_s05_shell_handoff"),
    dict(id="38_ants", pieces=[("OLD/a6_34_ants", 0.0)], vo="p06_s06_ants"),
    dict(id="39_boops", pieces=[("a6_35_whereGoing", 0.0)], vo="p06_s07_boops"),
    dict(id="40_catchphrase", pieces=[("a3_14_stoplook", 2.5)], vo="p06_s08_catchphrase"),
    dict(id="41_next_card", kind="card", text="NEXT TIME", sub="The Ant City Beneath Our Feet", vo="p06_s09_next_card"),
]


def build_beat(beat):
    bid = beat["id"]; out = SEG / f"{bid}.mp4"
    kind = beat.get("kind", "beat")
    vp = VO_SHOTS / f"{beat['vo']}.mp3" if beat.get("vo") else None
    vo = vp if (vp and vp.exists()) else None
    if kind == "card":
        dur = (durof(vo) + TAIL) if vo else beat.get("dur", 3.5)
        return make_card(out, beat["text"], beat["sub"], dur, vo=vo)
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
    # clone-pad fallback: if pieces underrun the VO, hold the last frame to reach target (the -t below
    # trims well-covered beats before any pad shows, so this only fills genuine residual, not a freeze).
    pad = "tpad=stop_mode=clone:stop_duration=12"
    post = f"[vc]{pad},{LIFT},format=yuv420p[vout]" if beat.get("lift") else f"[vc]{pad},format=yuv420p[vout]"
    fc = ";".join(vf) + f";{cat}concat=n={n}:v=1:a=0[vc];" + post
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *in_args, "-filter_complex", fc,
                    "-map", "[vout]", "-map", f"{aidx}:a", "-af", "apad", "-t", f"{target:.3f}",
                    *ENC, "-c:a", "aac", "-b:a", "192k", *AUD, str(out)], check=True)
    return out


def main():
    segs = []
    for beat in CUE:
        f = build_beat(beat)
        segs.append(f)
        print(f"  {beat['id']:18s} {durof(f):5.1f}s", flush=True)
    lst = ASM / "_seglist.txt"; lst.write_text("\n".join(f"file '{p}'" for p in segs))
    out = ASM / "EP2_v11_PICTURE_DIALOGUE.mp4"
    r = subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(lst), "-c", "copy", str(out)])
    if r.returncode != 0 or abs(durof(out) - sum(durof(s) for s in segs)) > 1.0:
        print("  [concat] copy failed -> re-encode", flush=True)
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(lst), *ENC, "-c:a", "aac", "-b:a", "192k", *AUD, str(out)], check=True)
    print(f"\nPICTURE+DIALOGUE -> {out}  {durof(out):.1f}s ({durof(out)/60:.2f} min)", flush=True)


if __name__ == "__main__":
    main()
