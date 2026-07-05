#!/usr/bin/env python3
"""EP1 companion Short — PURE DOCUMENTARY (real hermit-crab video). Mirrors the EP2 doc format.

One real world: 4 real Pexels hermit-crab clips, full-bleed vertical. Bill narrates; clean per-beat
captions; full-bleed EP1-thumbnail end-card. Demonstrates the "vacancy chain" + EP1's heart ("nobody
finds their home alone") and names Pip. Zero Kling/KIE; ~pennies of cached ElevenLabs Bill VO.

Run:  set -a; . ./.env; set +a; PYTHONPATH=. python3 scratch/ep1/build_doc_short_ep1.py
"""
import os, subprocess
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance, ImageOps
_LANCZOS = getattr(getattr(Image, "Resampling", Image), "LANCZOS")

from bentley.shared import eleven
from bentley.shared.ffio import dur as dur_of
import bentley.episode_builder.shorts as S

DL = os.path.expanduser("~/Downloads")
BASE = "assets/pilot_shots/ep1/shorts"
CLIP, EXP, VO = f"{BASE}/clips", f"{BASE}/exports", f"{BASE}/vo"
for d in (CLIP, EXP, VO):
    os.makedirs(d, exist_ok=True)
OUT = "episodes/ep1/EP1_Short_HermitCrab.mp4"
MUSIC = "assets/pilot_shots/ep1/build/music_bed.wav"
THUMB = "assets/approved/episodes/Bentley_Ep1_thumbnail.jpg"
W, H = 1080, 1920

CLIPS = {
    "walk":  f"{DL}/crab.mp4",     # crab walking + others visible (vertical)
    "body":  f"{DL}/crab_1.mp4",   # close body/legs out of shell (landscape)
    "grip":  f"{DL}/crab_2.mp4",   # golden close, legs gripping shell (vertical)
    "hero":  f"{DL}/crab_3.mp4",   # dreamy sunrise atmosphere (vertical 4K)
}
VENC = ["-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p",
        "-r", "30", "-video_track_timescale", "15360", "-an"]

def ff(args): subprocess.run(["ffmpeg", "-y", "-loglevel", "error"] + args, check=True)

def font(sz):
    for p in ("/System/Library/Fonts/Supplemental/Arial Rounded Bold.ttf", "/Library/Fonts/Arial.ttf"):
        try: return ImageFont.truetype(p, sz)
        except Exception: pass
    return ImageFont.load_default()

def bill(text, out):
    if os.path.exists(out): return out
    raw = out.replace(".mp3", "_raw.mp3")
    eleven.speak(eleven.NARRATOR, text, raw,
                 settings={"stability": 0.5, "similarity_boost": 0.75, "style": 0.4, "speed": 1.0})
    ff(["-i", raw, "-af", "highpass=f=80,loudnorm=I=-16:TP=-1.5:LRA=11", "-ac", "1", "-ar", "44100",
        "-b:a", "192k", out])
    return out

def reframe(src, ss, dur, out, native_vertical):
    vf = ("scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920" if native_vertical
          else "scale=-2:1920,crop=1080:1920") + ",fps=30,setsar=1,format=yuv420p"
    ff(["-ss", f"{ss}", "-t", f"{dur}", "-i", src, "-vf", vf] + VENC + [out]); return out

def caption_segment(seg, text, y, size, out):
    png = f"{CLIP}/_cap_{os.path.basename(out)}.png"; boxh = S.make_caption(text, png, size=size)
    ypx = max(20, int(y * H - boxh / 2))
    ff(["-i", seg, "-loop", "1", "-i", png, "-filter_complex",
        f"[0:v][1:v]overlay=0:{ypx}:shortest=1[v]", "-map", "[v]"] + VENC + [out]); return out

# ---------------------------------------------------------------- 1) VO (Bill)
print("== VO ==", flush=True)
LINES = [
    "See this little crab? He's carrying his whole house on his back.",
    "He's soft, so he borrows an empty seashell to stay safe.",
    "But as he grows, his shell gets too tight — like outgrowing your shoes.",
    "So when a big empty shell washes up... something wonderful happens.",
    "A whole line of crabs trades up, one by one — a vacancy chain.",
    "Because a hermit crab never finds his home alone. And neither did Pip.",
]
vo = [bill(t, f"{VO}/e1_{i}.mp3") for i, t in enumerate(LINES)]
PAD = 0.40
sdur = [round(dur_of(v) + PAD, 3) for v in vo]; ENDCARD = 3.0
print("  durs:", [round(dur_of(v), 2) for v in vo], "-> body", round(sum(sdur), 2), flush=True)

# ---------------------------------------------------------------- 2) picture beats + captions
print("== picture ==", flush=True)
BEATS = [  # (clip, in-point, native_vertical, caption, y, size)
    ("walk", 1.0,  True,  "He carries his house on his back", 0.12, 54),
    ("body", 3.0,  False, "...in a borrowed shell",           0.82, 56),
    ("grip", 1.5,  True,  "...but he keeps outgrowing it",    0.82, 54),
    ("walk", 10.0, True,  "Then a big shell washes up...",    0.12, 54),
    ("grip", 7.0,  True,  "a \"vacancy chain\"",              0.82, 58),
    ("hero", 6.5,  True,  "Nobody finds home alone",          0.12, 54),
]
segs = []
for i, (key, ss, vert, cap, y, size) in enumerate(BEATS):
    cd = dur_of(CLIPS[key]); ss = min(ss, max(0.0, cd - sdur[i] - 0.08))   # clamp so the clip never overruns
    raw = f"{CLIP}/e1_seg{i}.mp4"; reframe(CLIPS[key], ss, sdur[i], raw, vert)
    segs.append(caption_segment(raw, cap, y, size, f"{CLIP}/e1_seg{i}_cap.mp4"))

# ---------------------------------------------------------------- 3) full-bleed EP1-thumbnail end-card
def make_endcard(path, dur):
    GOLD, TEAL = (243, 195, 74), (205, 230, 232)
    src = Image.open(THUMB).convert("RGB")
    bg = ImageOps.fit(src, (W, H), method=_LANCZOS).filter(ImageFilter.GaussianBlur(48))
    canvas = ImageEnhance.Brightness(bg).enhance(0.42).convert("RGBA")
    canvas.alpha_composite(Image.new("RGBA", (W, H), (6, 16, 20, 95)))
    tw = 1010; th = int(round(tw * src.height / src.width)); thumb = src.resize((tw, th), _LANCZOS)
    tx, ty = (W - tw) // 2, (H - th) // 2 - 30
    canvas.alpha_composite(Image.new("RGBA", (tw + 14, th + 14), (*GOLD, 255)), (tx - 7, ty - 7))
    canvas.alpha_composite(thumb.convert("RGBA"), (tx, ty))
    d = ImageDraw.Draw(canvas)
    def center(t, y, fnt, fill): w = d.textlength(t, font=fnt); d.text(((W - w) / 2, y), t, font=fnt, fill=fill)
    center("BENTLEY'S BIG ADVENTURES", ty - 100, font(46), TEAL)
    center("Find the full episode on our channel", ty + th + 58, font(42), (255, 255, 255))
    label, fnt = "EPISODE 1", font(60); lw = d.textlength(label, font=fnt); tri, gap = 44, 28
    x0 = (W - (tri + gap + lw)) / 2; yb = ty + th + 150
    d.polygon([(x0, yb), (x0, yb + 52), (x0 + tri, yb + 26)], fill=GOLD)
    d.text((x0 + tri + gap, yb - 4), label, font=fnt, fill=GOLD)
    p = path + ".png"; canvas.convert("RGB").save(p)
    ff(["-loop", "1", "-t", f"{dur}", "-i", p, "-vf", "fps=30,setsar=1,format=yuv420p"] + VENC + [path]); return path
segs.append(make_endcard(f"{CLIP}/e1_endcard.mp4", ENDCARD))

base = f"{CLIP}/_e1_base.mp4"; S.concat(segs, base)

# ---------------------------------------------------------------- 4) audio: VO + music
print("== audio ==", flush=True)
pads = []
for i, v in enumerate(vo):
    pf = f"{VO}/_e1pad{i}.wav"; ff(["-i", v, "-af", f"apad=whole_dur={sdur[i]},aresample=48000", "-ac", "2", pf]); pads.append(pf)
sil = f"{VO}/_e1sil.wav"; ff(["-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo", "-t", f"{ENDCARD}", sil]); pads.append(sil)
listf = f"{VO}/_e1list.txt"; open(listf, "w").write("".join(f"file '{os.path.abspath(p)}'\n" for p in pads))
votrack = f"{VO}/_e1_vo.wav"; ff(["-f", "concat", "-safe", "0", "-i", listf, "-c:a", "pcm_s16le", votrack])
final_audio = f"{VO}/_e1_audio.wav"
ff(["-i", votrack, "-stream_loop", "-1", "-i", MUSIC, "-filter_complex",
    "[1:a]volume=0.13,afade=t=in:d=0.6[m];[0:a]volume=1.12[v];[v][m]amix=inputs=2:duration=first:normalize=0[a]",
    "-map", "[a]", final_audio])

# ---------------------------------------------------------------- 5) mux + QA frames
print("== mux ==", flush=True)
ff(["-i", base, "-i", final_audio, "-map", "0:v:0", "-map", "1:a:0", "-c:v", "copy", "-c:a", "aac",
    "-b:a", "192k", "-shortest", OUT])
d = dur_of(OUT)
for t in (1.0, 6.0, 12.0, 18.0, 24.0, round(d - 1.3, 1)):
    ff(["-ss", f"{t}", "-i", OUT, "-frames:v", "1", f"{EXP}/_e1qa_{t}.png"])
print(f"\nBUILT {OUT}\n  duration={d:.1f}s  abs={os.path.abspath(OUT)}", flush=True)
