#!/usr/bin/env python3
"""EP3 v2 assembler — INTERCUT, NO LOOPS, NO FREEZES. Each beat lists `srcs` (one or more sources). The
beat's VO duration is split across its sources, so a long line intercuts speaker -> cutaway -> speaker
with real motion instead of pushing/looping one short clip. Per-piece:
- clip  -> a DISTINCT live window (rotating per-clip offset); if a piece outlasts the clip, gentle
  retime (<=1.5x) then a real Ken-Burns push (never a frozen hold or a loop).
- still -> a strong Ken-Burns (zoom + alternating pan).
Final = runs hard-cut internally, ~0.45s crossfades at scene boundaries. Run: python3 episodes/ep3/assemble_v2.py
"""
import json, subprocess, re
from pathlib import Path
ROOT = Path("/project")
SHOT = json.load(open(ROOT / "episodes/ep3/shotlists/ep3_assembly.json"))["shots"]
SEG = ROOT / "episodes/ep3/_segs"; SEG.mkdir(parents=True, exist_ok=True)
PLATE = ROOT / "assets/character_design/InlandScrub_plate.png"
W, H, FPS = 1280, 720, 24
FILL = f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},setsar=1"
ENC = ["-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", "-r", str(FPS)]
AUD = ["-ar", "48000", "-ac", "2"]
TAIL = 0.3
XFADE_AT = {"s6_shadow", "s11_city", "s12a_nowonder", "s13b_fly"}
offsets = {}


def dur(p):
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)]).decode())


def vo_files(beat):
    return [str(ROOT / p) for p in re.findall(r"[^\s,]+\.mp3", str(beat.get("vo", ""))) if (ROOT / p).exists()]


def vo_dur(beat):
    return sum(dur(p) for p in vo_files(beat))


def kb(img, out, dur_s, dx, dz=0.0016, dy=24):
    n = max(1, int(dur_s * FPS))
    vf = (f"scale={int(W*1.30)}:{int(H*1.30)},zoompan=z='min(zoom+{dz},1.20)':"
          f"x='iw/2-(iw/zoom/2)+(on/{n})*{dx}':y='ih/2-(ih/zoom/2)+(on/{n})*{dy}':"
          f"d={n}:s={W}x{H}:fps={FPS},setsar=1,eq=saturation=1.05,format=yuv420p")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-loop", "1", "-i", str(img),
                    "-vf", vf, "-frames:v", str(n), "-an", str(out)], check=True)
    return out


def concat_pieces(parts, out):
    cat = Path(str(out) + ".txt"); cat.write_text("\n".join(f"file '{p}'" for p in parts))
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(cat), *ENC, "-an", str(out)], check=True)
    return out


def build_piece(bid, k, source, dur_s, off_override=None):
    """One picture piece of exactly dur_s, no audio. off_override pins the clip window start (used to
    keep a lip-sync CU time-aligned to the beat's audio); otherwise a rotating offset is used."""
    out = SEG / f"_{bid}_p{k}.mp4"
    if source.lower().endswith((".png", ".jpg", ".jpeg")):
        return kb(ROOT / source, out, dur_s, dx=(80 if k % 2 == 0 else -80))
    clip = ROOT / source; cd = dur(clip)
    if dur_s <= cd + 0.2:  # live window
        if off_override is not None:
            off = min(max(0.0, off_override), max(0.0, cd - dur_s))
        else:
            off = offsets.get(source, 0.0)
            if off + dur_s > cd:
                off = max(0.0, cd - dur_s)
            offsets[source] = (off + dur_s) if (off + 2 * dur_s <= cd) else 0.0
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{off:.3f}", "-t", f"{dur_s + 0.08:.3f}", "-i", str(clip),
                        "-vf", f"{FILL},fps={FPS},format=yuv420p,trim=0:{dur_s:.2f},setpts=PTS-STARTPTS", "-an", str(out)], check=True)
        return out
    # piece longer than clip: retime <=1.5x then real push
    rt = min(1.5, dur_s / cd); played = cd * rt; ext = max(0.0, dur_s - played)
    base = SEG / f"_{bid}_p{k}_a.mp4"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(clip),
                    "-vf", f"{FILL},setpts={rt:.4f}*PTS,fps={FPS},format=yuv420p", "-an", str(base)], check=True)
    if ext > 0.15:
        last = SEG / f"_{bid}_p{k}_last.png"
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-sseof", "-0.1", "-i", str(base), "-frames:v", "1", str(last)], check=True)
        push = kb(last, SEG / f"_{bid}_p{k}_push.mp4", ext, dx=70, dz=0.0024)
        return concat_pieces([base, push], out)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(base), "-t", f"{dur_s:.2f}", *ENC, "-an", str(out)], check=True)
    return out


def kb_smooth(img, out, dur_s):
    """Pan-free, SUPERSAMPLED gentle zoom for cards. No zoompan pan term -> no per-frame x/y rounding
    jitter (the 'shaking title' defect); render at 2x then lanczos-downscale for sub-pixel smoothness."""
    n = max(1, int(dur_s * FPS)); SS = 2
    vf = (f"scale={W * SS}:{H * SS}:flags=lanczos,zoompan=z='min(zoom+0.0005,1.06)':"
          f"x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={n}:s={W * SS}x{H * SS}:fps={FPS},"
          f"scale={W}:{H}:flags=lanczos,setsar=1,format=yuv420p")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-loop", "1", "-i", str(img),
                    "-vf", vf, "-frames:v", str(n), "-an", str(out)], check=True)
    return out


def title_card(out, dur_s):
    from PIL import Image, ImageDraw, ImageFont, ImageFilter
    # v14d: bright, SHARP backdrop from the locked-camera opening (Bentley + crumb) instead of the dim plate;
    # only lightly darkened so it doesn't read as low-quality; motion via kb_smooth (no pan -> no shake).
    tbg = ROOT / "scratch/ep3/v14fix/opening_v3.mp4"
    tpng = SEG / "_title_src.png"
    if tbg.exists():
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", "3.4", "-i", str(tbg), "-frames:v", "1",
                        "-vf", f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H}", str(tpng)], check=True)
        base = Image.open(tpng).convert("RGB")
    else:
        base = Image.open(PLATE).convert("RGB").resize((W, H))
    ov = Image.new("RGB", (W, H), (8, 12, 26))
    base = Image.blend(base, ov, 0.32)
    d = ImageDraw.Draw(base)

    def fnt(sz):
        for p in ["/System/Library/Fonts/Supplemental/Arial Rounded Bold.ttf", "/System/Library/Fonts/Helvetica.ttc"]:
            try:
                return ImageFont.truetype(p, sz)
            except Exception:
                pass
        return ImageFont.load_default()
    def ctext(y, s, f, fill, stroke=(20, 14, 60), sw=4):
        w = d.textlength(s, font=f); d.text(((W - w) / 2, y), s, font=f, fill=fill, stroke_width=sw, stroke_fill=stroke)
    ctext(H * 0.30, "BENTLEY'S BIG ADVENTURES", fnt(40), (120, 220, 235))
    ctext(H * 0.43, "The Ant City", fnt(78), (255, 255, 255))
    ctext(H * 0.58, "Beneath Our Feet", fnt(78), (255, 255, 255))
    cp = SEG / "_title.png"; base.save(cp)
    return kb_smooth(cp, out, dur_s)


def nexttime_card(out, dur_s):
    from PIL import Image, ImageDraw, ImageFont
    # real episode environment as bg (the butterfly landing), darkened for legible text -> "The Butterfly Highway"
    bgsrc = ROOT / "scratch/ep3/v14fix/butterfly_land_v2s.mp4"  # v14e: crisp re-render + sharpen
    bgpng = SEG / "_nt_bg.png"
    if bgsrc.exists():
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", "2", "-i", str(bgsrc), "-frames:v", "1",
                        "-vf", f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H}", str(bgpng)], check=True)
        base = Image.open(bgpng).convert("RGB")
        base = Image.blend(base, Image.new("RGB", (W, H), (6, 10, 24)), 0.5)
    else:
        base = Image.new("RGB", (W, H), (10, 14, 26))
    d = ImageDraw.Draw(base)
    def fnt(sz):
        try:
            return ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Rounded Bold.ttf", sz)
        except Exception:
            return ImageFont.load_default()
    for i, (s, sz, c) in enumerate([("NEXT TIME", 46, (255, 222, 120)), ("The Butterfly Highway", 60, (255, 255, 255))]):
        w = d.textlength(s, font=fnt(sz)); d.text(((W - w) / 2, H * 0.38 + i * 84), s, font=fnt(sz), fill=c, stroke_width=4, stroke_fill=(10, 8, 40))
    cp = SEG / "_nexttime.png"; base.save(cp)
    return kb(cp, out, dur_s, dx=30, dz=0.0009)


def build_seq(bid, seq, vf, vd, pic):
    """seq = [{src,dur,lipsync}]. Fill the VO duration: lip-sync cut-ins keep their short fixed dur and
    are time-aligned to the beat's audio (off=cumulative time); other pieces scale to fill the rest."""
    if vf:
        length = max(vd, 1.6) + TAIL
        lip_total = sum(float(p["dur"]) for p in seq if p.get("lipsync"))
        nonlip_w = sum(float(p["dur"]) for p in seq if not p.get("lipsync")) or 1.0
        avail = max(0.6, length - lip_total)
    else:
        length = sum(float(p["dur"]) for p in seq)
    pieces = []; cum = 0.0
    for k, p in enumerate(seq):
        src = p["src"]
        d = float(p["dur"]) if (not vf or p.get("lipsync")) else avail * (float(p["dur"]) / nonlip_w)
        d = max(0.5, d)
        if src == "TITLE":
            pieces.append(title_card(SEG / f"_{bid}_p{k}.mp4", d))
        elif src == "CARD":
            pieces.append(nexttime_card(SEG / f"_{bid}_p{k}.mp4", d))
        else:
            pieces.append(build_piece(bid, k, src, d, off_override=(cum if p.get("lipsync") else None)))
        cum += d
    concat_pieces([Path(x) for x in pieces], pic)
    return cum


def build_seg(beat):
    bid = beat["id"]; out = SEG / f"{bid}.mp4"
    vf = vo_files(beat); vd = vo_dur(beat)
    pic = SEG / f"_{bid}_pic.mp4"
    seq = beat.get("seq")
    if seq:
        length = build_seq(bid, seq, vf, vd, pic)
    else:
        length = max(float(beat.get("dur", 2.0)), vd) + (TAIL if vf else 0.0)
        length = max(length, 1.6)
        srcs = beat.get("srcs") or []
        if srcs == ["TITLE"]:
            title_card(pic, length)
        elif srcs == ["CARD"]:
            nexttime_card(pic, length)
        else:
            n = len(srcs)
            shares = [length / n] * n
            shares[-1] = length - sum(shares[:-1])
            pieces = [build_piece(bid, k, s, max(0.6, shares[k])) for k, s in enumerate(srcs)]
            if len(pieces) == 1:
                pic = Path(pieces[0])
            else:
                concat_pieces(pieces, pic)
    aud = ["-i", vf[0]] if vf else ["-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo"]
    if len(vf) > 1:
        vl = SEG / f"_{bid}_vo.txt"; vl.write_text("\n".join(f"file '{p}'" for p in vf))
        voc = SEG / f"_{bid}_vo.mp3"
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(vl), *AUD, str(voc)], check=True)
        aud = ["-i", str(voc)]
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(pic), *aud,
                    "-filter_complex", f"[0:v]trim=0:{length:.2f},setpts=PTS-STARTPTS[v]",
                    "-map", "[v]", "-map", "1:a", "-af", "apad", "-t", f"{length:.2f}",
                    *ENC, "-c:a", "aac", "-b:a", "192k", *AUD, str(out)], check=True)
    return out, length


def main():
    segs = []
    for b in SHOT:
        if b.get("status") != "ready" and b.get("srcs") not in (["TITLE"], ["CARD"]):
            print(f"  SKIP {b['id']} (not ready: {b.get('srcs')})", flush=True); continue
        p, ln = build_seg(b); segs.append((b["id"], p, ln)); print(f"  {b['id']:16} {ln:5.2f}s", flush=True)
    runs = []; cur = []
    for sid, p, ln in segs:
        if sid in XFADE_AT and cur:
            runs.append(cur); cur = []
        cur.append((sid, p, ln))
    if cur:
        runs.append(cur)
    runclips = []
    for k, run in enumerate(runs):
        lst = SEG / f"_run{k}.txt"; lst.write_text("\n".join(f"file '{p}'" for _, p, _ in run))
        rc = SEG / f"_run{k}.mp4"
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(lst),
                        *ENC, "-c:a", "aac", "-b:a", "192k", *AUD, str(rc)], check=True)
        runclips.append((rc, sum(ln for _, _, ln in run)))
    T = 0.45
    inputs = []
    for rc, _ in runclips:
        inputs += ["-i", str(rc)]
    chain = []
    for i in range(len(runclips)):
        chain.append(f"[{i}:v]settb=AVTB,fps={FPS},format=yuv420p[v{i}]")
        chain.append(f"[{i}:a]aresample=48000,asettb=1/48000[a{i}]")
    vcur, acur, acc = "v0", "a0", runclips[0][1]
    for i in range(1, len(runclips)):
        off = max(0.0, acc - T)
        chain.append(f"[{vcur}][v{i}]xfade=transition=fade:duration={T}:offset={off:.3f}[vx{i}]")
        chain.append(f"[{acur}][a{i}]acrossfade=d={T}:c1=tri:c2=tri[ax{i}]")
        vcur, acur = f"vx{i}", f"ax{i}"; acc = acc + runclips[i][1] - T
    out = ROOT / "episodes/ep3/EP3_v2_PD.mp4"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *inputs, "-filter_complex", ";".join(chain),
                    "-map", f"[{vcur}]", "-map", f"[{acur}]", "-c:v", "libx264", "-crf", "17",
                    "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", *AUD, str(out)], check=True)
    print(f"PD -> {out}  {dur(out):.1f}s  runs={len(runclips)}", flush=True)


if __name__ == "__main__":
    main()
