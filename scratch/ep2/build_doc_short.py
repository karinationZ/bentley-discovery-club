#!/usr/bin/env python3
"""EP2 companion Short v2 — PURE DOCUMENTARY (real octopus video only, no cartoon in the body).

One real world: 3 real Pexels octopus clips, full-bleed vertical. Bill narrates (the thread back to the
show); clean typographic captions (burned per-beat); a typographic end-card (show name + CTA). The brand
lives in the VOICE and the outro, never spliced over footage. The lesson ("you just had to look") is
DEMONSTRATED by the camouflage, never recited. Zero Kling/KIE; only ~pennies of ElevenLabs VO (cached).

Run:  set -a; . ./.env; set +a; PYTHONPATH=. python3 scratch/ep2/build_doc_short.py
"""
import os, subprocess
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance, ImageOps
_LANCZOS = getattr(getattr(Image, "Resampling", Image), "LANCZOS")

from bentley.shared import eleven
from bentley.shared.ffio import dur as dur_of
import bentley.episode_builder.shorts as S

DL = os.path.expanduser("~/Downloads")
BASE = "assets/pilot_shots/ep2/shorts"
CLIP, EXP, VO = f"{BASE}/clips", f"{BASE}/exports", f"{BASE}/vo"
for d in (CLIP, EXP, VO):
    os.makedirs(d, exist_ok=True)
OUT = "episodes/ep2/EP2_Short_Octopus_Camouflage.mp4"
MUSIC = "assets/pilot_shots/ep1/build/music_bed.wav"
W, H = 1080, 1920

CLIPS = {
    "reveal": f"{DL}/14464967_1920_1080_60fps (1).mp4",   # camouflage → reveal (landscape)
    "hero":   f"{DL}/17836505-uhd_2160_3840_25fps.mp4",   # gorgeous close-up (NATIVE VERTICAL)
    "world":  f"{DL}/14514171_1920_1080_60fps.mp4",       # wide reef establishing (landscape)
}
VENC = ["-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p",
        "-r", "30", "-video_track_timescale", "15360", "-an"]

def ff(args):
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error"] + args, check=True)

def font(sz):
    for p in ("/System/Library/Fonts/Supplemental/Arial Rounded Bold.ttf",
              "/Library/Fonts/Arial.ttf"):
        try: return ImageFont.truetype(p, sz)
        except Exception: pass
    return ImageFont.load_default()

def bill(text, out):
    if os.path.exists(out):           # cache — don't re-spend ElevenLabs on rebuilds
        return out
    raw = out.replace(".mp3", "_raw.mp3")
    eleven.speak(eleven.NARRATOR, text, raw,
                 settings={"stability": 0.5, "similarity_boost": 0.75, "style": 0.4, "speed": 1.0})
    ff(["-i", raw, "-af", "highpass=f=80,loudnorm=I=-16:TP=-1.5:LRA=11", "-ac", "1", "-ar", "44100",
        "-b:a", "192k", out])
    return out

def reframe(src, ss, dur, out, native_vertical):
    vf = ("scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920" if native_vertical
          else "scale=-2:1920,crop=1080:1920") + ",fps=30,setsar=1,format=yuv420p"
    ff(["-ss", f"{ss}", "-t", f"{dur}", "-i", src, "-vf", vf] + VENC + [out])
    return out

def caption_segment(seg, text, y, size, out):
    """Burn ONE caption onto a beat (single looped overlay — avoids the multi-image framesync bug)."""
    png = f"{CLIP}/_cap_{os.path.basename(out)}.png"
    boxh = S.make_caption(text, png, size=size)
    ypx = max(20, int(y * H - boxh / 2))
    ff(["-i", seg, "-loop", "1", "-i", png, "-filter_complex",
        f"[0:v][1:v]overlay=0:{ypx}:shortest=1[v]", "-map", "[v]"] + VENC + [out])
    return out

# ---------------------------------------------------------------- 1) VO (all Bill — documentary)
print("== VO ==", flush=True)
LINES = [
    "Wait — there's an octopus hiding right here. Can you spot her?",
    "There she is. Right in front of you the whole time.",
    "In a blink, she changes her color and her skin to vanish into the reef.",
    "Millions of tiny color sacs in her skin — called chromatophores — do it.",
    "And she's colorblind. She matches colors she can't even see.",
    "You met Indi last time. Her secret? She was right there — you just had to look.",
]
vo = [bill(t, f"{VO}/d{i}.mp3") for i, t in enumerate(LINES)]
PAD = 0.40
sdur = [round(dur_of(v) + PAD, 3) for v in vo]
ENDCARD = 3.0
print("  line durs:", [round(dur_of(v), 2) for v in vo], "-> body", round(sum(sdur), 2), flush=True)

# ---------------------------------------------------------------- 2) picture beats + per-beat caption
print("== picture ==", flush=True)
BEATS = [  # (clip, in-point, native_vertical, caption, y, size)
    ("reveal", 0.3,  False, "Can you find the octopus?",      0.12, 58),
    ("reveal", 7.0,  False, "...hiding in plain sight",       0.82, 56),
    ("hero",   0.5,  True,  "Color + texture, in 1 second",   0.12, 54),
    ("hero",   6.5,  True,  "chromatophores = \"color sacs\"", 0.82, 52),
    ("world",  3.0,  False, "...and she's COLORBLIND",        0.82, 58),
    ("hero",  11.0,  True,  "She was right there all along",  0.12, 54),
]
segs = []
for i, (key, ss, vert, cap, y, size) in enumerate(BEATS):
    raw = f"{CLIP}/doc_seg{i}.mp4"; reframe(CLIPS[key], ss, sdur[i], raw, vert)
    capd = f"{CLIP}/doc_seg{i}_cap.mp4"; caption_segment(raw, cap, y, size, capd)
    segs.append(capd)

# ---------------------------------------------------------------- 3) typographic end-card (no cartoon)
THUMB = "episodes/ep2/EP2_thumbnail.jpg"
def make_endcard(path, dur):
    """End-card = FULL-BLEED blurred EP2 scene + the framed thumbnail (play button) + CTA. Fills the frame."""
    GOLD, TEAL = (243, 195, 74), (205, 230, 232)
    src = Image.open(THUMB).convert("RGB")
    # full-bleed blurred + darkened background — no flat dead space
    bg = ImageOps.fit(src, (W, H), method=_LANCZOS).filter(ImageFilter.GaussianBlur(48))
    canvas = ImageEnhance.Brightness(bg).enhance(0.42).convert("RGBA")
    canvas.alpha_composite(Image.new("RGBA", (W, H), (6, 16, 20, 95)))           # subtle scrim
    # sharp framed thumbnail, vertically centered
    tw = 1010; th = int(round(tw * src.height / src.width)); thumb = src.resize((tw, th), _LANCZOS)
    tx, ty = (W - tw) // 2, (H - th) // 2 - 30
    canvas.alpha_composite(Image.new("RGBA", (tw + 14, th + 14), (*GOLD, 255)), (tx - 7, ty - 7))
    canvas.alpha_composite(thumb.convert("RGBA"), (tx, ty))
    d = ImageDraw.Draw(canvas)
    def center(text, y, fnt, fill):
        w = d.textlength(text, font=fnt); d.text(((W - w) / 2, y), text, font=fnt, fill=fill)
    center("BENTLEY'S BIG ADVENTURES", ty - 100, font(46), TEAL)
    center("Find the full episode on our channel", ty + th + 58, font(42), (255, 255, 255))
    label, fnt = "EPISODE 2", font(60)                       # gold play-triangle + label (→ glyph missing)
    lw = d.textlength(label, font=fnt); tri, gap = 44, 28
    x0 = (W - (tri + gap + lw)) / 2; yb = ty + th + 154
    d.polygon([(x0, yb), (x0, yb + 52), (x0 + tri, yb + 26)], fill=GOLD)
    d.text((x0 + tri + gap, yb - 4), label, font=fnt, fill=GOLD)
    p = path + ".png"; canvas.convert("RGB").save(p)
    ff(["-loop", "1", "-t", f"{dur}", "-i", p, "-vf", "fps=30,setsar=1,format=yuv420p"] + VENC + [path])
    return path
segs.append(make_endcard(f"{CLIP}/doc_endcard.mp4", ENDCARD))

base = f"{CLIP}/_doc_base.mp4"; S.concat(segs, base)

# ---------------------------------------------------------------- 4) audio: VO + music
print("== audio ==", flush=True)
pads = []
for i, v in enumerate(vo):
    pf = f"{VO}/_dpad{i}.wav"; ff(["-i", v, "-af", f"apad=whole_dur={sdur[i]},aresample=48000", "-ac", "2", pf]); pads.append(pf)
sil = f"{VO}/_endsil.wav"; ff(["-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo", "-t", f"{ENDCARD}", sil]); pads.append(sil)
listf = f"{VO}/_dlist.txt"; open(listf, "w").write("".join(f"file '{os.path.abspath(p)}'\n" for p in pads))
votrack = f"{VO}/_doc_vo.wav"; ff(["-f", "concat", "-safe", "0", "-i", listf, "-c:a", "pcm_s16le", votrack])
final_audio = f"{VO}/_doc_audio.wav"
ff(["-i", votrack, "-stream_loop", "-1", "-i", MUSIC, "-filter_complex",
    "[1:a]volume=0.13,afade=t=in:d=0.6[m];[0:a]volume=1.12[v];[v][m]amix=inputs=2:duration=first:normalize=0[a]",
    "-map", "[a]", final_audio])

# ---------------------------------------------------------------- 5) mux + QA
print("== mux ==", flush=True)
ff(["-i", base, "-i", final_audio, "-map", "0:v:0", "-map", "1:a:0", "-c:v", "copy", "-c:a", "aac",
    "-b:a", "192k", "-shortest", OUT])
S.write_srt([{"text": b[3], "t": round(sum(sdur[:i]) + 0.2, 2), "dur": round(sdur[i] - 0.4, 2)}
             for i, b in enumerate(BEATS)], OUT.replace(".mp4", ".srt"), sum(sdur) + ENDCARD)
d = dur_of(OUT)
for t in (1.0, 7.5, 12.0, 17.0, 24.5, round(d - 1.2, 1)):
    ff(["-ss", f"{t}", "-i", OUT, "-frames:v", "1", f"{EXP}/_docqa_{t}.png"])
print(f"\nBUILT {OUT}\n  duration={d:.1f}s  abs={os.path.abspath(OUT)}", flush=True)
