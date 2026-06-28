#!/usr/bin/env python3
"""Mix EP2 v13 -> 1080p master. Music by mood (bright wonder / suspense for eel+escape / triumph ending),
ambient ocean, SFX, one open/close fade. Run AFTER assemble_v13.py."""
import json, subprocess
from pathlib import Path

ROOT = Path("/project")
OUT = ROOT / "scratch/ep2/final_v13"; SEG = OUT / "segs"
MUS = ROOT / "assets/pilot_shots/ep1/v2/music"; SFX = ROOT / "assets/pilot_shots/ep1/v2/sfx"
CUT = OUT / "EP2_v13_PD.mp4"; MASTER = OUT / "EP2_v13_FINAL.mp4"
AUD = ["-ar", "48000", "-ac", "2"]
SEGLIST = [ln.split("'")[1] for ln in (OUT / "_seglist.txt").read_text().splitlines() if ln.strip()]


def durof(p):
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)]).decode().strip())


def mood_of(name):
    if name == "_00title":
        return "theme_wonder"
    if name == "_99nexttime":
        return "triumph"
    pod = name[:2]
    if pod in ("P1", "P2", "P4"):
        return "theme_wonder"
    if pod in ("P3", "P5"):
        return "suspense"
    return "triumph"


SFX_AT = {"P1_B01": ("chime", 0.4), "P1_I01": ("octo_curl", 0.4), "P2_I02": ("sparkle", 0.45),
          "P3_I03": ("shake", 0.5), "P3_N01": ("shake", 0.4), "P5_I01": ("shake", 0.45),
          "P5_I07": ("octo_curl", 0.4), "P6_I06": ("skitter", 0.45)}

start, t, runs = {}, 0.0, []
for path in SEGLIST:
    name = Path(path).stem; d = durof(path); start[name] = t
    m = mood_of(name)
    if runs and runs[-1][0] == m:
        runs[-1][1] += d
    else:
        runs.append([m, d])
    t += d
total = t
print(f"total {total:.1f}s; runs:", [(m, round(d, 1)) for m, d in runs], flush=True)

parts = []
for i, (m, d) in enumerate(runs):
    o = OUT / f"_mus_{i}.wav"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-stream_loop", "-1", "-i", str(MUS / f"{m}.mp3"),
                    "-t", f"{d:.2f}", "-af", f"afade=t=in:st=0:d=0.8,afade=t=out:st={max(0,d-0.8):.2f}:d=0.8", *AUD, str(o)], check=True)
    parts.append(o)
(OUT / "_muslist.txt").write_text("\n".join(f"file '{p}'" for p in parts))
music = OUT / "_music.wav"
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(OUT / "_muslist.txt"), *AUD, str(music)], check=True)

events = [(start[b], s, v) for b, (s, v) in SFX_AT.items() if b in start and (SFX / f"{s}.mp3").exists()]
sfxtrk = OUT / "_sfx.wav"
if events:
    cmd = ["ffmpeg", "-y", "-loglevel", "error"]
    for _, s, _ in events:
        cmd += ["-i", str(SFX / f"{s}.mp3")]
    flt = "".join(f"[{i}:a]adelay={int(tt*1000)}|{int(tt*1000)},volume={v}[s{i}];" for i, (tt, _, v) in enumerate(events))
    flt += "".join(f"[s{i}]" for i in range(len(events))) + f"amix=inputs={len(events)}:duration=longest:normalize=0,apad=whole_dur={total}[a]"
    subprocess.run(cmd + ["-filter_complex", flt, "-map", "[a]", "-t", f"{total:.2f}", *AUD, str(sfxtrk)], check=True)

amb = SFX / "amb_ocean.mp3"; fo = total - 0.6
cmd = ["ffmpeg", "-y", "-loglevel", "error", "-i", str(CUT), "-stream_loop", "-1", "-i", str(amb), "-i", str(music)]
amix_in, n = "[d][amb][mus]", 3
if events:
    cmd += ["-i", str(sfxtrk)]; amix_in, n = "[d][amb][mus][sfx]", 4
fc = (
    f"[0:v]scale=1920:1080:flags=lanczos,eq=saturation=1.06:contrast=1.03,fade=t=in:st=0:d=0.5,fade=t=out:st={fo:.2f}:d=0.6[v];"
    "[0:a]aresample=48000,volume=1.0,alimiter=limit=0.97[d];[1:a]aresample=48000,volume=0.09[amb];"
    "[2:a]aresample=48000,volume=0.55[mus0];[d]asplit=2[dmix][dkey];"
    "[mus0][dkey]sidechaincompress=threshold=0.03:ratio=8:attack=20:release=350:makeup=1[mus];"
    + ("[3:a]aresample=48000,volume=0.9[sfx];" if events else "")
    + (f"[dmix][amb][mus][sfx]amix=inputs=4:duration=first:normalize=0,afade=t=out:st={fo:.2f}:d=0.6[a]" if events
       else f"[dmix][amb][mus]amix=inputs=3:duration=first:normalize=0,afade=t=out:st={fo:.2f}:d=0.6[a]")
)
subprocess.run(cmd + ["-filter_complex", fc, "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-crf", "17", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", *AUD, str(MASTER)], check=True)
print(f"FINAL MASTER: {durof(MASTER):.1f}s -> {MASTER}", flush=True)
