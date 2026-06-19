#!/usr/bin/env python3
"""Reusable 9:16 Shorts builder for Bentley's Big Adventures.
Reframe each source segment (punch-in CROP or BLUR-FILL), concat, overlay Pillow caption PNGs
(this ffmpeg lacks subtitles/drawtext), export 1080x1920 + write a clean .srt. Originals untouched."""
import os, re, json, subprocess
from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1920
FINAL = "assets/pilot_shots/hybrid_ep1/Bentley_Ep1_v2_FINAL_1080p.mp4"
OUT = "assets/pilot_shots/hybrid_ep1/shorts"
CAP, CLIP, EXP = f"{OUT}/captions", f"{OUT}/clips", f"{OUT}/exports"
for d in (CAP, CLIP, EXP): os.makedirs(d, exist_ok=True)
VENC = ["-c:v","libx264","-preset","medium","-crf","19","-pix_fmt","yuv420p","-r","24","-video_track_timescale","12288"]
AENC = ["-c:a","aac","-b:a","160k","-ar","48000","-ac","2"]

def _font(sz):
    for p in ["/System/Library/Fonts/Supplemental/Arial Rounded Bold.ttf",
              "/System/Library/Fonts/Supplemental/Arial Black.ttf",
              "/System/Library/Fonts/SFNSRounded.ttf"]:
        if os.path.exists(p):
            try: return ImageFont.truetype(p, sz)
            except Exception: pass
    return ImageFont.load_default()

_probe = ImageDraw.Draw(Image.new("RGB", (8, 8)))
def make_caption(text, path, size=72, maxw=930):
    """Full-width transparent PNG: wrapped, centered, white + navy outline + shadow on a soft dark pill."""
    # This font has no color-emoji glyphs -> strip emoji/dingbats/arrows so they never render as tofu boxes.
    text = re.sub(r'[\U0001F000-\U0001FAFF☀-➿←-⇿⬀-⯿️•]', '', text)
    text = re.sub(r'\s{2,}', ' ', text).strip()
    f = _font(size)
    words, lines, cur = text.split(), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if _probe.textlength(t, font=f) <= maxw: cur = t
        else:
            if cur: lines.append(cur)
            cur = w_
    if cur: lines.append(cur)
    lh, pad = int(size * 1.18), int(size * 0.45)
    tw = max(_probe.textlength(l, font=f) for l in lines)
    boxw, boxh = int(tw) + pad * 2, lh * len(lines) + pad * 2
    img = Image.new("RGBA", (W, boxh), (0, 0, 0, 0)); d = ImageDraw.Draw(img)
    x0 = (W - boxw) // 2
    d.rounded_rectangle([x0, 0, x0 + boxw, boxh], radius=int(size * 0.45), fill=(8, 12, 40, 145))
    sw, y = max(5, size // 12), pad
    for l in lines:
        lw = _probe.textlength(l, font=f); x = (W - lw) // 2
        d.text((x + 4, y + 5), l, font=f, fill=(0, 0, 15, 140))
        d.text((x, y), l, font=f, fill=(255, 255, 255, 255), stroke_width=sw, stroke_fill=(20, 18, 70, 255))
        y += lh
    img.save(path); return boxh

def dur_of(p): return float(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",p]).strip())

def build_segment(start, end, mode, xoff, out):
    d = round(end - start, 3)
    if mode == "crop":
        vf = f"crop=608:1080:{xoff}:0,scale={W}:{H},setsar=1,fps=24,format=yuv420p"
        cmd = ["ffmpeg","-y","-loglevel","error","-ss",f"{start}","-t",f"{d}","-i",FINAL,
               "-vf",vf,"-map","0:v","-map","0:a"] + VENC + AENC + [out]
    else:  # blurfill — whole 16:9 visible, blurred cover behind
        fc = (f"[0:v]split[bg][fg];"
              f"[bg]scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},gblur=sigma=32,eq=brightness=-0.05[bgb];"
              f"[fg]scale={W}:-2[fgs];[bgb][fgs]overlay=(W-w)/2:(H-h)/2,setsar=1,fps=24,format=yuv420p[v]")
        cmd = ["ffmpeg","-y","-loglevel","error","-ss",f"{start}","-t",f"{d}","-i",FINAL,
               "-filter_complex",fc,"-map","[v]","-map","0:a"] + VENC + AENC + [out]
    subprocess.run(cmd, check=True); return d

def concat(segs, out):
    lst = out + ".txt"; open(lst, "w").write("".join(f"file '{os.path.abspath(s)}'\n" for s in segs))
    subprocess.run(["ffmpeg","-y","-loglevel","error","-f","concat","-safe","0","-i",lst,"-c","copy",out], check=True)

def add_captions(base, caps, out):
    total = dur_of(base)
    inputs = ["-i", base]; pngs = []
    for i, c in enumerate(caps):
        p = f"{CAP}/{os.path.splitext(os.path.basename(out))[0]}_{i}.png"
        boxh = make_caption(c["text"], p, size=c.get("size", 72))
        pngs.append((p, boxh, c)); inputs += ["-i", p]
    fc, prev = [], "0:v"
    for i, (p, boxh, c) in enumerate(pngs):
        y = int(c.get("y", 0.30) * H - boxh / 2)
        lab = f"v{i+1}"
        fc.append(f"[{prev}][{i+1}:v]overlay=0:{y}:enable='between(t,{c['t']:.2f},{c['t']+c['dur']:.2f})'[{lab}]")
        prev = lab
    if not fc:  # no captions
        subprocess.run(["ffmpeg","-y","-loglevel","error","-i",base,"-c","copy",out], check=True); return total
    subprocess.run(["ffmpeg","-y","-loglevel","error"] + inputs +
        ["-filter_complex", ";".join(fc), "-map", f"[{prev}]", "-map", "0:a"] + VENC + AENC + ["-t", f"{total:.3f}", out], check=True)
    return total

def _ts(t):
    h, m, s, ms = int(t//3600), int(t%3600//60), int(t%60), int(round((t-int(t))*1000))
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"
def write_srt(caps, out):
    L = []
    for i, c in enumerate(sorted(caps, key=lambda x: x["t"]), 1):
        txt = re.sub(r'[^\x00-\x7F]+', '', c["text"]).strip()
        L += [str(i), f"{_ts(c['t'])} --> {_ts(c['t']+c['dur'])}", txt, ""]
    open(out, "w").write("\n".join(L))

def build_short(spec):
    segs = []
    for i, s in enumerate(spec["segments"]):
        o = f"{CLIP}/{spec['id']}_seg{i}.mp4"
        build_segment(s["start"], s["end"], s.get("mode", "crop"), s.get("xoff", 656), o)
        segs.append(o)
    base = f"{CLIP}/{spec['id']}_base.mp4"; concat(segs, base)
    outmp4 = f"{EXP}/{spec['out']}"
    total = add_captions(base, spec.get("captions", []), outmp4)
    write_srt(spec.get("captions", []), f"{EXP}/{os.path.splitext(spec['out'])[0]}.srt")
    return outmp4, round(total, 2)

if __name__ == "__main__":
    specs = json.load(open(f"{OUT}/shorts_specs.json"))
    import sys
    want = sys.argv[1:] if len(sys.argv) > 1 else [s["id"] for s in specs]
    for spec in specs:
        if spec["id"] in want:
            mp4, t = build_short(spec)
            print(f"BUILT {spec['id']:22s} {t:5.1f}s -> {mp4}")
