"""Render the tracked, timed mouth pass over a plate clip (the deterministic replacement for
mouth rerolls). Plate frames + viseme timeline + mouth track + shape sheet -> composited frames
-> mp4 (VO muxed). Compositing details (feather/color-match) live in composite.py."""
import subprocess
import tempfile
from pathlib import Path

from PIL import Image

from bentley.lipsync.composite import place_patch

FPS = 24


def _extract(video, workdir, fps=FPS):
    fr = Path(workdir) / "plate_frames"
    fr.mkdir(parents=True, exist_ok=True)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(video),
                    "-vf", f"fps={fps}", str(fr / "f_%05d.png")], check=True)
    return sorted(fr.glob("f_*.png"))


def viseme_at(cues, t):
    for c in cues:
        if c["start"] <= t < c["end"]:
            return c["viseme"]
    return "REST_CLOSED"


def render(plate, cues, track, sheet, out_mp4, audio=None, mouth_width=None, workdir=None,
           fps=FPS, plate_provides=frozenset({"REST_CLOSED", "MBP"})):
    """plate mp4 + [{start,end,viseme}] (clip-local times) + MouthTrack + MouthSheet -> out_mp4.

    sheet: a MouthSheet, or a callable pos->MouthSheet for per-frame ANGLE selection (v2 —
    front/three-quarter/side sheets picked from the tracker's geometry).
    mouth_width: patch width in plate pixels (defaults to the autotracker's template width).
    plate_provides: visemes rendered by the PLATE itself, no patch — on a closed-mouth plate the
    plate IS the closed mouth; the rig only adds openings (kills patch flicker + edge mismatch)."""
    wd = Path(workdir or tempfile.mkdtemp(prefix="lipsync_render_"))
    frames = _extract(plate, wd, fps)
    outdir = wd / "out_frames"
    outdir.mkdir(exist_ok=True)
    w = mouth_width or getattr(track, "template_width_px", None)
    if not w:
        raise ValueError("mouth_width required (or use an autotracked track)")
    for i, fp in enumerate(frames):
        t = i / fps
        pos = track.at(t)
        base = Image.open(fp).convert("RGB")
        vis = viseme_at(cues, t)
        if pos.get("visible", True) and vis not in plate_provides:
            sh = sheet(pos) if callable(sheet) else sheet
            patch = sh.patch(vis, w * pos.get("scale", 1.0))
            base = place_patch(base, patch, pos, sh.anchor)
        base.save(outdir / fp.name)
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(fps),
           "-i", str(outdir / "f_%05d.png")]
    if audio:
        cmd += ["-i", str(audio), "-map", "0:v", "-map", "1:a", "-c:a", "aac", "-b:a", "192k",
                "-shortest"]
    cmd += ["-c:v", "libx264", "-crf", "17", "-pix_fmt", "yuv420p", str(out_mp4)]
    subprocess.run(cmd, check=True)
    return out_mp4
