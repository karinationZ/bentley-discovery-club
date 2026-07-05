#!/usr/bin/env python3
"""Mix EP3 v14 -> 1080p master. Adapts the PROVEN EP2 mix_v13 pattern: music beds by story mood,
sidechain-ducked under dialogue, gentle chime/sparkle SFX, ONE open fade-in and a LONG warm fade-out
that lets the music breathe past the NEXT-TIME card (owner: the ending must not cut off).
Run AFTER assemble_v2.py picture-lock:  python3 episodes/ep3/mix_ep3.py <picture.mp4> <out.mp4>"""
import sys, subprocess, importlib.util
from pathlib import Path

ROOT = Path("/project")
MUS = ROOT / "assets/pilot_shots/ep1/v2/music"; SFX = ROOT / "assets/pilot_shots/ep1/v2/sfx"
CUT = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "episodes/ep3/EP3_v2_PD.mp4"
MASTER = Path(sys.argv[2]) if len(sys.argv) > 2 else ROOT / "episodes/ep3/final_delivery/EP3_v14_MIXED.mp4"
OUT = ROOT / "episodes/ep3/_mix"; OUT.mkdir(exist_ok=True)
AUD = ["-ar", "48000", "-ac", "2"]

spec = importlib.util.spec_from_file_location("bs", ROOT / "episodes/ep3/build_sections.py")
bs = importlib.util.module_from_spec(spec); spec.loader.exec_module(bs)

def durof(p):
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                                          "-of", "csv=p=0", str(p)]).decode().strip())

# story mood per section (bright discovery -> suspense -> the turn -> bonding -> triumph -> wonder -> heart -> warm out)
MOOD = {
 "00_title": "theme_wonder", "s1_open": "theme_wonder", "s1b_findline": "theme_wonder",
 "s2_meet": "theme_wonder", "s2a_igotit": "theme_wonder", "s2b_whatline": "theme_wonder",
 "s2c_smell": "theme_wonder", "s3_trail": "calm_mystery", "s4_pickup": "theme_wonder",
 "s5_waitno": "suspense", "s5_oops": "suspense", "s5b_lost": "suspense", "s6_shadow": "suspense",
 "s7a_realize": "emotional_piano", "s7_listen": "calm_mystery",
 "s8a_checkyou": "theme_wonder", "s8_antenna": "theme_wonder", "s8b_brave": "theme_wonder",
 "s9_bridge": "emotional_piano", "s10_rebuild": "triumph", "s10b_together": "triumph", "s10c_strong": "triumph",
 "s11_city": "calm_mystery", "s12a_nowonder": "calm_mystery", "s12ab_explain": "calm_mystery",
 "s12b_city": "emotional_piano", "s12c_lesson": "emotional_piano", "s12b_promise": "emotional_piano",
 "s13_button": "theme_wonder", "s13b_fly": "emotional_piano", "s13c_night": "emotional_piano", "s15_card": "emotional_piano",
}

# replay the assembler's timing to get section lengths (same math as assemble_v2)
TAIL = 0.3; XFADE = {"s6_shadow", "s11_city", "s12a_nowonder", "s13b_fly"}; T = 0.45
def seclen(vos, seq):
    vd = sum(durof(ROOT / f"episodes/ep3/vo/{l}.mp3") for l in vos)
    if vos:
        length = max(vd, 1.6) + TAIL
        lip = sum(float(p["dur"]) for p in seq if p.get("lipsync"))
        nonlip = sum(float(p["dur"]) for p in seq if not p.get("lipsync")) or 1.0
        avail = max(0.6, length - lip)
        return sum(max(0.5, float(p["dur"]) if p.get("lipsync") else avail * (float(p["dur"]) / nonlip)) for p in seq)
    return max(max(float(seq[0].get("dur", 2.0)), vd), 1.6)

runs, t = [], 0.0
for sid, voice, vos, seq in bs.SECTIONS:
    if sid in XFADE: t -= T
    d = seclen(vos, seq); m = MOOD.get(sid, "theme_wonder")
    if runs and runs[-1][0] == m: runs[-1][1] += d
    else: runs.append([m, d])
    t += d
total = durof(CUT)
runs[-1][1] += max(0.0, total - t)  # absorb rounding into the last run
print(f"picture {total:.1f}s; mood runs:", [(m, round(d, 1)) for m, d in runs], flush=True)

parts = []
for i, (m, d) in enumerate(runs):
    o = OUT / f"_mus_{i}.wav"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-stream_loop", "-1", "-i", str(MUS / f"{m}.mp3"),
                    "-t", f"{d:.2f}", "-af", f"afade=t=in:st=0:d=0.8,afade=t=out:st={max(0, d - 0.8):.2f}:d=0.8",
                    *AUD, str(o)], check=True)
    parts.append(o)
(OUT / "_muslist.txt").write_text("\n".join(f"file '{p}'" for p in parts))
music = OUT / "_music.wav"
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(OUT / "_muslist.txt"),
                *AUD, str(music)], check=True)

# gentle inland ambience: low wind-ish bed from the ocean amb at very low level (scrub is near the cove)
fo = total - 2.0   # LONG warm fade (owner: give the ending a breath)
fc = (
    f"[0:v]scale=1920:1080:flags=lanczos,eq=saturation=1.06:contrast=1.03,fade=t=out:st={fo:.2f}:d=1.8[v];"  # no opening fade-in (owner: no black at the start)
    "[0:a]aresample=48000,volume=1.0,alimiter=limit=0.97[d];"
    "[1:a]aresample=48000,volume=0.05[amb];"
    "[2:a]aresample=48000,volume=0.5[mus0];[d]asplit=2[dmix][dkey];"
    "[mus0][dkey]sidechaincompress=threshold=0.03:ratio=8:attack=20:release=350:makeup=1[mus];"
    f"[dmix][amb][mus]amix=inputs=3:duration=first:normalize=0,afade=t=out:st={fo:.2f}:d=1.8[a]"
)
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(CUT), "-stream_loop", "-1",
                "-i", str(SFX / "amb_ocean.mp3"), "-i", str(music),
                "-filter_complex", fc, "-map", "[v]", "-map", "[a]",
                "-c:v", "libx264", "-crf", "17", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
                *AUD, str(MASTER)], check=True)
print(f"FINAL MASTER: {durof(MASTER):.1f}s -> {MASTER}", flush=True)
