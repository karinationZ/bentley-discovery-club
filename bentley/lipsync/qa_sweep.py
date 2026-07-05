"""MANDATORY QA for rig output (hard rule, learned 2026-07-01): a DENSE frame sweep of the
rendered clip, built automatically after every render. Spot-checked stills MISS bad frames."""
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw


def sweep(video, out_png, step=0.15, crop=None, cols=4, start=0.0, end=None):
    """Contact sheet of frames every `step` seconds. crop=(x0,y0,x1,y1) zooms the mouth region."""
    video = Path(video)
    dur = float(subprocess.check_output(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "csv=p=0", str(video)]).decode())
    end = min(end or dur, dur - 0.08)  # a seek at/past EOF yields no frame
    ts, t = [], start + step / 3
    while t < end:
        ts.append(round(t, 2))
        t += step
    tiles = []
    for i, t in enumerate(ts):
        f = Path(f"/tmp/_qasweep_{video.stem}_{i:03d}.png")
        f.unlink(missing_ok=True)
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", str(t), "-i", str(video),
                        "-frames:v", "1", str(f)], check=True)
        if not f.exists():  # decoder gave nothing (edge seek) — skip, don't crash the sweep
            continue
        im = Image.open(f).convert("RGB")
        if crop:
            im = im.crop(crop)
        im.thumbnail((420, 280))
        d = ImageDraw.Draw(im)
        d.rectangle([0, 0, 66, 20], fill=(0, 0, 0))
        d.text((4, 3), f"{t}s", fill=(255, 255, 0))
        tiles.append(im)
    w = max(t.width for t in tiles)
    h = max(t.height for t in tiles)
    rows = (len(tiles) + cols - 1) // cols
    g = Image.new("RGB", (w * cols, h * rows), (15, 15, 15))
    for i, im in enumerate(tiles):
        g.paste(im, ((i % cols) * w, (i // cols) * h))
    g.save(out_png)
    return Path(out_png), len(tiles)
