#!/usr/bin/env python3
"""Build a Bentley "companion Short" — a real-footage documentary that mirrors an episode's science.

ONE real world (no cartoon spliced into the footage), full-bleed vertical, Bill narrates, ONE caption
burned per beat, a full-bleed episode-thumbnail end-card. ~$0: free footage + reused thumbnail/music +
a few cents of CACHED ElevenLabs VO. No Kling/KIE.

Drive it with a SPEC (dict or JSON). Run from the repo root so `bentley.*` imports resolve and the
ElevenLabs key is present:

    set -a; . ./.env; set +a
    PYTHONPATH=. python3 .claude/skills/companion-short/scripts/build_short.py path/to/spec.json

SPEC schema (see the companion-short SKILL.md for the full example):
    {
      "episode_no": 2,
      "thumbnail": "episodes/ep2/EP2_thumbnail.jpg",
      "out": "episodes/ep2/EP2_Short_Octopus_Camouflage.mp4",
      "clips": {"hook": "~/Downloads/reveal.mp4", "hero": "~/Downloads/hero.mp4"},
      "beats": [
        {"clip":"hook","ss":0.3,"vertical":false,"line":"Wait... can you spot the octopus?",
         "cap":"Can you find the octopus?","cy":0.12,"size":58}
      ],
      "music": null,          // optional; defaults to the EP1 music bed
      "voice": "narrator"     // optional; "narrator" (Bill, default) or "bentley"
    }
"""
import os
import subprocess

from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance, ImageOps

from bentley.shared import eleven
from bentley.shared.ffio import dur as dur_of
import bentley.episode_builder.shorts as S

_LANCZOS = getattr(getattr(Image, "Resampling", Image), "LANCZOS")
W, H = 1080, 1920
PAD = 0.40                      # breathing room after each VO line
ENDCARD = 3.0                   # end-card seconds
DEFAULT_MUSIC = "assets/pilot_shots/ep1/build/music_bed.wav"
VENC = ["-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p",
        "-r", "30", "-video_track_timescale", "15360", "-an"]


def _ff(args): subprocess.run(["ffmpeg", "-y", "-loglevel", "error"] + args, check=True)
def _x(p): return os.path.expanduser(p)


def _font(sz):
    for p in ("/System/Library/Fonts/Supplemental/Arial Rounded Bold.ttf", "/Library/Fonts/Arial.ttf"):
        try: return ImageFont.truetype(p, sz)
        except Exception: pass
    return ImageFont.load_default()


def _vo(text, out, voice_id):
    """Narrate one line. CACHED by filename — a rebuild never re-spends ElevenLabs. (Change a line's
    text => delete its vo/b<i>.mp3, or you'll keep the old audio.)"""
    if os.path.exists(out): return out
    raw = out.replace(".mp3", "_raw.mp3")
    eleven.speak(voice_id, text, raw,
                 settings={"stability": 0.5, "similarity_boost": 0.75, "style": 0.4, "speed": 1.0})
    _ff(["-i", raw, "-af", "highpass=f=80,loudnorm=I=-16:TP=-1.5:LRA=11", "-ac", "1", "-ar", "44100",
         "-b:a", "192k", out])
    return out


def _reframe(src, ss, dur, out, vertical):
    """Reframe to full-bleed 1080x1920. Vertical source = scale to fill; landscape = scale-up + center
    crop. `ss` is CLAMPED so the requested window can never overrun the clip (overrun => truncation)."""
    cd = dur_of(src); ss = min(ss, max(0.0, cd - dur - 0.08))
    vf = ("scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920" if vertical
          else "scale=-2:1920,crop=1080:1920") + ",fps=30,setsar=1,format=yuv420p"
    _ff(["-ss", f"{ss}", "-t", f"{dur}", "-i", src, "-vf", vf] + VENC + [out])
    return out


def _caption(seg, text, cy, size, out):
    """Burn ONE caption (single looped overlay). Do NOT batch captions through shorts.add_captions —
    its multi-image overlay chain silently drops every caption after the second."""
    png = out + ".cap.png"; boxh = S.make_caption(text, png, size=size)
    ypx = max(20, int(cy * H - boxh / 2))
    _ff(["-i", seg, "-loop", "1", "-i", png, "-filter_complex",
         f"[0:v][1:v]overlay=0:{ypx}:shortest=1[v]", "-map", "[v]"] + VENC + [out])
    return out


def _endcard(thumb, ep_no, out, dur):
    """Full-bleed: blurred + darkened episode thumbnail fills the frame (no flat dead space); the sharp
    thumbnail is framed and centered; CTA below. NO center play button (implies a tap Made-for-Kids
    forbids + covers the art). The gold triangle is drawn (the font has no '->' glyph)."""
    GOLD, TEAL = (243, 195, 74), (205, 230, 232)
    src = Image.open(thumb).convert("RGB")
    bg = ImageOps.fit(src, (W, H), method=_LANCZOS).filter(ImageFilter.GaussianBlur(48))
    cv = ImageEnhance.Brightness(bg).enhance(0.42).convert("RGBA")
    cv.alpha_composite(Image.new("RGBA", (W, H), (6, 16, 20, 95)))
    tw = 1010; th = int(round(tw * src.height / src.width)); t = src.resize((tw, th), _LANCZOS)
    tx, ty = (W - tw) // 2, (H - th) // 2 - 30
    cv.alpha_composite(Image.new("RGBA", (tw + 14, th + 14), (*GOLD, 255)), (tx - 7, ty - 7))
    cv.alpha_composite(t.convert("RGBA"), (tx, ty))
    d = ImageDraw.Draw(cv)
    def ctr(s, y, f, c): w = d.textlength(s, font=f); d.text(((W - w) / 2, y), s, font=f, fill=c)
    ctr("BENTLEY'S BIG ADVENTURES", ty - 100, _font(46), TEAL)
    ctr("Find the full episode on our channel", ty + th + 58, _font(42), (255, 255, 255))
    label, f = f"EPISODE {ep_no}", _font(60)
    lw = d.textlength(label, font=f); tri, gap = 44, 28; x0 = (W - (tri + gap + lw)) / 2; yb = ty + th + 150
    d.polygon([(x0, yb), (x0, yb + 52), (x0 + tri, yb + 26)], fill=GOLD)
    d.text((x0 + tri + gap, yb - 4), label, font=f, fill=GOLD)
    p = out + ".png"; cv.convert("RGB").save(p)
    _ff(["-loop", "1", "-t", f"{dur}", "-i", p, "-vf", "fps=30,setsar=1,format=yuv420p"] + VENC + [out])
    return out


def build(spec):
    out = spec["out"]
    work = os.path.join(os.path.dirname(out) or ".", "_short_build"); vodir = os.path.join(work, "vo")
    os.makedirs(vodir, exist_ok=True)
    voice = {"narrator": eleven.NARRATOR, "bentley": eleven.BENTLEY}.get(spec.get("voice", "narrator"), eleven.NARRATOR)
    music = spec.get("music") or DEFAULT_MUSIC
    beats = spec["beats"]; clips = {k: _x(v) for k, v in spec["clips"].items()}

    print("== VO ==", flush=True)
    vo = [_vo(b["line"], f"{vodir}/b{i}.mp3", voice) for i, b in enumerate(beats)]
    sdur = [round(dur_of(v) + PAD, 3) for v in vo]
    print("  durs:", [round(dur_of(v), 2) for v in vo], "-> body", round(sum(sdur), 2), flush=True)

    print("== picture ==", flush=True)
    segs = []
    for i, b in enumerate(beats):
        raw = f"{work}/seg{i}.mp4"; _reframe(clips[b["clip"]], b["ss"], sdur[i], raw, b.get("vertical", True))
        segs.append(_caption(raw, b["cap"], b.get("cy", 0.12), b.get("size", 54), f"{work}/seg{i}_cap.mp4"))
    segs.append(_endcard(spec["thumbnail"], spec["episode_no"], f"{work}/endcard.mp4", ENDCARD))
    base = f"{work}/_base.mp4"; S.concat(segs, base)

    print("== audio ==", flush=True)
    pads = []
    for i, v in enumerate(vo):
        pf = f"{vodir}/_pad{i}.wav"
        _ff(["-i", v, "-af", f"apad=whole_dur={sdur[i]},aresample=48000", "-ac", "2", pf]); pads.append(pf)
    sil = f"{vodir}/_sil.wav"; _ff(["-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo", "-t", f"{ENDCARD}", sil]); pads.append(sil)
    lst = f"{vodir}/_list.txt"; open(lst, "w").write("".join(f"file '{os.path.abspath(p)}'\n" for p in pads))
    vt = f"{vodir}/_vo.wav"; _ff(["-f", "concat", "-safe", "0", "-i", lst, "-c:a", "pcm_s16le", vt])
    fa = f"{vodir}/_audio.wav"
    _ff(["-i", vt, "-stream_loop", "-1", "-i", music, "-filter_complex",
         "[1:a]volume=0.13,afade=t=in:d=0.6[m];[0:a]volume=1.12[v];[v][m]amix=inputs=2:duration=first:normalize=0[a]",
         "-map", "[a]", fa])

    print("== mux ==", flush=True)
    _ff(["-i", base, "-i", fa, "-map", "0:v:0", "-map", "1:a:0", "-c:v", "copy", "-c:a", "aac",
         "-b:a", "192k", "-shortest", out])
    S.write_srt([{"text": b["cap"], "t": round(sum(sdur[:i]) + 0.2, 2), "dur": round(sdur[i] - 0.4, 2)}
                 for i, b in enumerate(beats)], out.replace(".mp4", ".srt"), sum(sdur) + ENDCARD)

    d = dur_of(out); qa = os.path.join(work, "qa"); os.makedirs(qa, exist_ok=True)  # under _short_build (avoids colliding with an episode's own _qa/)
    body = sum(sdur)
    for t in sorted({1.0, round(body * 0.4, 1), round(body * 0.8, 1), round(d - 1.3, 1)}):
        _ff(["-ss", f"{t}", "-i", out, "-frames:v", "1", f"{qa}/qa_{t}.png"])
    print(f"\nBUILT {out}\n  duration={d:.1f}s  abs={os.path.abspath(out)}\n  QA frames in {qa}/ — "
          f"check every caption renders, the animal stays in frame, and the end-card reads right.", flush=True)
    return out


if __name__ == "__main__":
    import json, sys
    if len(sys.argv) > 1:
        build(json.load(open(sys.argv[1])))
    else:
        print(__doc__)
