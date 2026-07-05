"""Plate calibration helper — the one-time step when onboarding a new plate.

    python -m bentley.lipsync.calibrate <video> [--t 0] [--out /tmp/calib.png]

Writes a grid-overlaid frame so you can read off the MOUTH-REGION template_box and mouth anchor
in pixels, plus a skeleton plate json to fill in. Rules learned the hard way (EP3 2026-07-01):
- template_box = the MOUTH REGION itself (closed on the plate), NEVER nose/eye + offset — head
  rotation changes any fixed offset and the mouth drifts onto the cheek.
- keep search_radius_px small (~60): stops teleports to look-alike dark blobs (paws, tags).
- visibility windows: exclude spans where the camera leaves the speaker / the mouth is a sliver
  (film grammar: don't sync a mouth the viewer can't read)."""
import argparse
import json
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw


def grid_frame(video, t=0.0, out_png="/tmp/calib.png", step=40):
    f = "/tmp/_calib_frame.png"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", str(t), "-i", str(video),
                    "-frames:v", "1", f], check=True)
    im = Image.open(f).convert("RGB")
    d = ImageDraw.Draw(im)
    for x in range(0, im.width, step):
        d.line([(x, 0), (x, im.height)], fill=(0, 255, 0), width=1)
        d.text((x + 2, 2), str(x), fill=(255, 255, 0))
    for y in range(0, im.height, step):
        d.line([(0, y), (im.width, y)], fill=(0, 255, 0), width=1)
        d.text((2, y + 2), str(y), fill=(255, 255, 0))
    im.save(out_png)
    return out_png


SKELETON = {
    "plate_id": "<episode>_<plate_name>",
    "video": "<repo-relative mp4>",
    "character": "bentley",
    "angle": "three_quarter",
    "template_box": [0, 0, 0, 0],
    "mouth_offset": [0, 0],
    "mouth_width": 140,
    "track_fps": 12, "min_score": 0.60, "search_radius_px": 60,
    "visibility": [],
}


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("video")
    ap.add_argument("--t", type=float, default=0.0)
    ap.add_argument("--out", default="/tmp/calib.png")
    ap.add_argument("--skeleton", help="also write a skeleton plate json here")
    a = ap.parse_args(argv)
    p = grid_frame(a.video, a.t, a.out)
    print(f"grid frame -> {p}  (read template_box + mouth anchor off the grid)")
    if a.skeleton:
        sk = dict(SKELETON)
        sk["video"] = str(a.video)
        Path(a.skeleton).write_text(json.dumps(sk, indent=2))
        print(f"skeleton -> {a.skeleton}")


if __name__ == "__main__":
    main()
