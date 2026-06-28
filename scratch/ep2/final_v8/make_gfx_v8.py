#!/usr/bin/env python3
"""Ep2 v8 procedural shots (NO KIE): improved camo color/texture change + clean three-hearts.
Outputs -> scratch/ep2/final_v8/gfx/{camo_v8.mp4, hearts_v8.mp4}.  Run: python3 .../make_gfx_v8.py
"""
import math, subprocess
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter

ROOT = Path("/project")
OUT = ROOT / "scratch/ep2/final_v8/gfx"; OUT.mkdir(parents=True, exist_ok=True)
W, H, FPS = 1280, 720, 24
AUD = ["-ar", "48000", "-ac", "2"]
FILL = f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H},setsar=1"
CAMO = ROOT / "assets/pilot_shots/ep2/motion/a1_08_camo.mp4"     # real Indi shot
REEF = ROOT / "assets/pilot_shots/ep2/motion/plate_live.mp4"     # empty tide pool to vanish into


def make_camo(dur=5.8):
    """Indi's skin shifts colour + desaturates, then she dissolves into the bare reef = camouflage."""
    out = OUT / "camo_v8.mp4"
    off = dur - 1.7
    fc = (
        f"[0:v]{FILL},hue=h='-70*t/{dur}':s='1-0.4*t/{dur}',eq=contrast=1.05:brightness=0.01[a];"
        f"[1:v]{FILL},eq=saturation=1.05[b];"
        f"[a][b]xfade=transition=dissolve:duration=1.7:offset={off:.2f},format=yuv420p[v]"
    )
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(CAMO), "-i", str(REEF),
                    "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo", "-t", f"{dur:.2f}",
                    "-filter_complex", fc, "-map", "[v]", "-map", "2:a", "-r", str(FPS),
                    "-c:v", "libx264", "-crf", "18", "-c:a", "aac", "-b:a", "192k", *AUD, str(out)], check=True)
    print(f"camo  -> {out}")


def _heart(cx, cy, s):
    pts = []
    for i in range(120):
        t = math.pi * 2 * i / 120
        x = 16 * math.sin(t) ** 3
        y = -(13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t))
        pts.append((cx + x * s / 18, cy + y * s / 18))
    return pts


def make_hearts(dur=5.2):
    """Three soft-glow blue hearts pulsing in sequence + faint blue-blood current, over the live Indi shot."""
    out = OUT / "hearts_v8.mp4"
    frames = OUT / "_hearts_frames"; frames.mkdir(exist_ok=True)
    n = int(round(dur * FPS))
    centers = ((512, 250), (640, 212), (768, 250))   # the 'three hearts'
    for i in range(n):
        ph = i / max(1, n - 1)
        glow = Image.new("RGBA", (W, H), (0, 0, 0, 0)); gd = ImageDraw.Draw(glow)
        core = Image.new("RGBA", (W, H), (0, 0, 0, 0)); cd = ImageDraw.Draw(core)
        for k, (cx, cy) in enumerate(centers):
            beat = 0.5 + 0.5 * math.sin(ph * math.pi * 6 - k * 2.1)   # staggered triple pulse
            s = 78 * (0.92 + 0.16 * beat)
            gd.polygon(_heart(cx, cy, s * 1.35), fill=(80, 180, 255, int(70 + 60 * beat)))
            cd.polygon(_heart(cx, cy, s), fill=(150, 220, 255, 235))
            cd.line(_heart(cx, cy, s) + [_heart(cx, cy, s)[0]], fill=(225, 245, 255, 255), width=3)
        glow = glow.filter(ImageFilter.GaussianBlur(22))
        # faint blue-blood current
        for k in range(4):
            y0 = 430 + 70 * k + math.sin(ph * math.pi * 2 + k) * 14
            x0 = 300 + math.sin(ph * math.pi * 2 + k * 1.3) * 26
            gd2 = ImageDraw.Draw(glow)
            gd2.arc((x0, y0, x0 + 240, y0 + 90), 195, 345, fill=(70, 170, 255, 90), width=7)
        Image.alpha_composite(glow, core).convert("RGB").save(frames / f"f_{i:04d}.png")
    bg = ROOT / "assets/pilot_shots/ep2/motion/a5_32_science.mp4"
    fc = (f"[0:v]{FILL},eq=brightness=-0.02:saturation=1.04[bg];[1:v]format=rgba[ov];"
          f"[bg][ov]overlay,format=yuv420p[v]")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(bg), "-framerate", str(FPS),
                    "-i", str(frames / "f_%04d.png"), "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo",
                    "-t", f"{dur:.2f}", "-filter_complex", fc, "-map", "[v]", "-map", "2:a", "-r", str(FPS),
                    "-c:v", "libx264", "-crf", "18", "-c:a", "aac", "-b:a", "192k", *AUD, str(out)], check=True)
    print(f"hearts-> {out}")


if __name__ == "__main__":
    make_camo()
    make_hearts()
