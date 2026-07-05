#!/usr/bin/env python3
"""Build the EP2 companion Short — "The Octopus That Disappears" (camouflage / color-change).

Zero Kling/KIE. Real octopus stills (Pexels, license-clean) animated with the package ken_burns(),
cartoon Bentley bookends reused from the EP1 master, Bill narration + LauraZ catchphrase, music bed.
Each picture beat is sized to its actual recorded VO length so no line outruns its shot.

Run:  set -a; . ./.env; set +a; PYTHONPATH=. python scratch/ep2/build_camo_short.py
"""
import os, shutil, subprocess

from bentley.shared import eleven
from bentley.shared.audio import clean_master
from bentley.shared.ffio import dur as dur_of
from bentley.voices.dialogue import tts_bentley, tts_catchphrase
import bentley.episode_builder.shorts as S
from bentley.episode_builder.placeholders import ken_burns

# ---------------------------------------------------------------- paths
DL = os.path.expanduser("~/Downloads")
BASE = "assets/pilot_shots/ep2/shorts"
CLIP, EXP, CAP, VO = f"{BASE}/clips", f"{BASE}/exports", f"{BASE}/captions", f"{BASE}/vo"
for d in (CLIP, EXP, CAP, VO):
    os.makedirs(d, exist_ok=True)
OUT = f"{EXP}/EP2_Short_The_Octopus_That_Disappears.mp4"
MUSIC = "assets/pilot_shots/ep1/build/music_bed.wav"

# Pexels stills (license-clean) → project clips, mapped to beats
STILLS = {
    "hook":    "pexels-pspov-3046629.jpg",          # camouflaged on the reef floor — "find the octopus"
    "texture": "pexels-andromeda99-9004403.jpg",    # white octopus on vivid coral — color+texture match
    "macro":   "pexels-1051250151-20985390.jpg",    # sucker/arm macro — the "color sacs" detail
    "full":    "pexels-annantonova-5986729.jpg",    # full-body swim — the colorblind reveal
}
for k, fn in STILLS.items():
    dst = f"{CLIP}/oct_{k}.jpg"
    if not os.path.exists(dst):
        shutil.copy(f"{DL}/{fn}", dst)

def ff(args):
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error"] + args, check=True)

def bill(text, out):
    """Grandpa Bill narrator line (locked NARRATOR voice) + loudnorm cleanup."""
    raw = out.replace(".mp3", "_raw.mp3")
    eleven.speak(eleven.NARRATOR, text, raw,
                 settings={"stability": 0.5, "similarity_boost": 0.75, "style": 0.4, "speed": 1.0})
    ff(["-i", raw, "-af", "highpass=f=80,loudnorm=I=-16:TP=-1.5:LRA=11", "-ac", "1", "-ar", "44100",
        "-b:a", "192k", out])
    return out

# ---------------------------------------------------------------- 1) VO
print("== VO ==", flush=True)
vo = {}
vo[0] = bill("There's an octopus hiding right here... can you spot her?", f"{VO}/l0_hook.mp3")
vo[1] = tts_catchphrase(f"{VO}/l1_catchphrase.mp3")                       # Bentley — Stop. Look. Listen.
vo[2] = bill("In a blink, an octopus can change her color — and even her bumpy skin — to match almost "
             "anything around her.", f"{VO}/l2_change.mp3")
vo[3] = bill("She does it with millions of tiny color sacs in her skin, called chromatophores, that open "
             "and close in a flash.", f"{VO}/l3_chromatophores.mp3")
vo[4] = bill("And the wildest part? She's colorblind. She can't even see the colors she's copying.",
             f"{VO}/l4_colorblind.mp3")
vo[5] = tts_bentley("That's Indi's secret too — and there's a whole adventure about her.",
                    f"{VO}/l5_signoff.mp3")

PAD = 0.40                                   # breathing room after each line
vdur = {i: dur_of(vo[i]) for i in vo}
sdur = {i: round(vdur[i] + PAD, 3) for i in vo}
total = round(sum(sdur.values()), 3)
print("  line durs:", {i: round(vdur[i], 2) for i in vo}, "-> total", total, flush=True)

# ---------------------------------------------------------------- 2) picture segments
print("== picture ==", flush=True)
# octopus beats: ken_burns the still (landscape), then shorts blurfill -> vertical 1080x1920
kb = {}
for i, key in {0: "hook", 2: "texture", 3: "macro", 4: "full"}.items():
    kb[i] = f"{CLIP}/oct_{key}_kb.mp4"
    ken_burns(f"{CLIP}/oct_{key}.jpg", sdur[i], kb[i])     # default 1920x1080 + slow zoom

segs = []
# seg layout: 0 hook(oct) · 1 Bentley(catchphrase) · 2 change(oct) · 3 macro(oct) · 4 colorblind(oct) · 5 Bentley(signoff)
plan = [
    (0, dict(start=0,     mode="blurfill", src=kb[0])),
    (1, dict(start=182.4, mode="crop", xoff=656, src=None)),   # reused on-model Bentley CU (EP1 master)
    (2, dict(start=0,     mode="blurfill", src=kb[2])),
    (3, dict(start=0,     mode="blurfill", src=kb[3])),
    (4, dict(start=0,     mode="blurfill", src=kb[4])),
    (5, dict(start=220.2, mode="crop", xoff=656, src=None)),   # different reused Bentley beat (EP1 master)
]
for i, p in plan:
    o = f"{CLIP}/seg{i}.mp4"
    S.build_segment(p["start"], p["start"] + sdur[i], p["mode"], p.get("xoff", 656), o, p["src"])
    segs.append(o)

base = f"{CLIP}/_base.mp4"; S.concat(segs, base)

# ---------------------------------------------------------------- 3) captions (no emoji — PIL font has no glyphs)
caps_text = [
    ("FIND THE OCTOPUS",                0.10, 64),
    ("Stop.  Look.  Listen.",           0.13, 60),
    ("Color AND texture — in 1 second", 0.10, 52),
    ("chromatophores = \"color sacs\"", 0.83, 52),
    ("...and she's COLORBLIND",         0.83, 58),
    ("Indi does this in Episode 2  >>", 0.13, 52),
]
caps, t = [], 0.0
for i, (txt, y, size) in enumerate(caps_text):
    caps.append({"text": txt, "t": round(t + 0.15, 2), "dur": round(sdur[i] - 0.3, 2), "y": y, "size": size})
    t += sdur[i]
capped = f"{CLIP}/_capped.mp4"
S.add_captions(base, caps, capped)
S.write_srt(caps, OUT.replace(".mp4", ".srt"), total)

# ---------------------------------------------------------------- 4) audio: VO track + music bed
print("== audio ==", flush=True)
pad_files = []
for i in sorted(vo):
    pf = f"{VO}/_pad{i}.wav"
    ff(["-i", vo[i], "-af", f"apad=whole_dur={sdur[i]},aresample=48000", "-ac", "2", pf])
    pad_files.append(pf)
listf = f"{VO}/_list.txt"
with open(listf, "w") as f:
    for pf in pad_files:
        f.write(f"file '{os.path.abspath(pf)}'\n")
votrack = f"{VO}/_vo_track.wav"
ff(["-f", "concat", "-safe", "0", "-i", listf, "-c:a", "pcm_s16le", votrack])

final_audio = f"{VO}/_final_audio.wav"
ff(["-i", votrack, "-stream_loop", "-1", "-i", MUSIC, "-filter_complex",
    "[1:a]volume=0.15,afade=t=in:d=0.6[m];[0:a]volume=1.12[v];"
    "[v][m]amix=inputs=2:duration=first:normalize=0[a]", "-map", "[a]", final_audio])

# ---------------------------------------------------------------- 5) mux + QA
print("== mux ==", flush=True)
ff(["-i", capped, "-i", final_audio, "-map", "0:v:0", "-map", "1:a:0",
    "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", OUT])

d = dur_of(OUT)
ff(["-ss", "1.0", "-i", OUT, "-frames:v", "1", f"{EXP}/_qa_frame_hook.png"])
ff(["-ss", str(round(d - 2, 2)), "-i", OUT, "-frames:v", "1", f"{EXP}/_qa_frame_end.png"])
streams = subprocess.check_output(["ffprobe", "-v", "error", "-show_entries",
    "stream=codec_type,width,height", "-of", "csv=p=0", OUT]).decode().strip()
print(f"\nBUILT {OUT}\n  duration={d:.1f}s  streams=[{streams.replace(chr(10), ' | ')}]", flush=True)
print(f"  abs: {os.path.abspath(OUT)}", flush=True)
