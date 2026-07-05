"""Zero-credit placeholder picture generators + the credit guardrail for the Animatic Lock tool.

Two placeholder pictures, both built from EXISTING files with ffmpeg/PIL only (no generation):
- ``ken_burns()``  — a slow zoom over a locked master / plate / keyframe still
  (the ``zoompan`` helper that used to live copy-pasted in ``scratch/ep2/assemble_*.py``,
  extracted here so the assembler and the animatic share one implementation).
- ``labeled_card()`` — a gray card naming the speaking character + beat, for any beat that has
  no shot yet. The text track REUSES ``shorts.make_caption`` (this ffmpeg has no drawtext).

HARD GUARDRAIL (``assert_media_cmd`` / ``run_media``): every subprocess this module — and the
animatic — runs is checked to be ``ffmpeg``/``ffprobe`` ONLY. Anything that could spend
KIE/fal/ElevenLabs credits (the renderer, an API client, curl) is refused. This module imports
nothing that can spend credits (PIL + shorts are imported lazily inside ``card_png``).
"""
import os
import subprocess

# Canonical encode profile — every animatic segment is built to these so they concat by copy
# (matches bentley/episode_builder/assemble.py: 1920x1080 @ 24fps, fixed video timescale).
CANVAS_W, CANVAS_H, FPS = 1920, 1080, 24
NORM = (f"scale={CANVAS_W}:{CANVAS_H}:force_original_aspect_ratio=decrease,"
        f"pad={CANVAS_W}:{CANVAS_H}:(ow-iw)/2:(oh-ih)/2,setsar=1,fps={FPS},format=yuv420p")
VENC = ["-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p",
        "-r", str(FPS), "-video_track_timescale", "12288"]
AENC = ["-c:a", "aac", "-b:a", "160k", "-ar", "48000", "-ac", "2"]

# ----------------------------------------------------------------- credit guardrail

ALLOWED_BINARIES = {"ffmpeg", "ffprobe"}


class CreditGuardError(RuntimeError):
    """Raised when the animatic path tries to run anything other than ffmpeg/ffprobe."""


def assert_media_cmd(cmd):
    """Refuse any subprocess that isn't ffmpeg/ffprobe — the animatic must spend ZERO credits.

    Returns None when the command is allowed; raises ``CreditGuardError`` otherwise.
    """
    if not cmd:
        raise CreditGuardError("empty command")
    binary = os.path.basename(str(cmd[0]))
    if binary not in ALLOWED_BINARIES:
        raise CreditGuardError(
            f"BLOCKED non-media command '{cmd[0]}': the Animatic Lock path may only run "
            f"{sorted(ALLOWED_BINARIES)} (existing-files-only, zero credits)."
        )
    return None


#: tally of media subprocesses run, by binary — surfaced in the build report as proof of spend.
MEDIA_CALLS = {}


def run_media(cmd, **kw):
    """Run a subprocess only after the credit guard approves it."""
    assert_media_cmd(cmd)
    binary = os.path.basename(str(cmd[0]))
    MEDIA_CALLS[binary] = MEDIA_CALLS.get(binary, 0) + 1
    kw.setdefault("check", True)
    return subprocess.run(cmd, **kw)


# ----------------------------------------------------------------- ken-burns still

def ken_burns_cmd(src_img, dur, out, w=CANVAS_W, h=CANVAS_H, fps=FPS):
    """ffmpeg command: a gentle continuous zoom over a single still (the extracted zoompan)."""
    frames = max(1, int(round(dur * fps)))
    vf = (f"scale={2 * w}:{2 * h}:force_original_aspect_ratio=increase,crop={2 * w}:{2 * h},"
          f"zoompan=z='min(zoom+0.0015,1.15)':d={frames}:"
          f"x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s={w}x{h}:fps={fps},"
          f"setsar=1,format=yuv420p")
    return ["ffmpeg", "-y", "-loglevel", "error", "-loop", "1", "-i", src_img,
            "-t", f"{dur:.3f}", "-vf", vf, "-an"] + list(VENC) + [out]


def ken_burns(src_img, dur, out, w=CANVAS_W, h=CANVAS_H, fps=FPS):
    """Render a Ken-Burns (slow-zoom) clip from a still. Video-only; VO is muxed by the caller."""
    run_media(ken_burns_cmd(src_img, dur, out, w=w, h=h, fps=fps))
    return out


# ----------------------------------------------------------------- labeled gray card

def card_png(text, sub, path, w=CANVAS_W, h=CANVAS_H, bg=(28, 32, 42)):
    """Compose a gray placeholder card naming the speaker + beat, REUSING shorts.make_caption.

    PIL + shorts only — imported lazily so importing this module pulls in nothing heavy and runs
    no module-level side effects.
    """
    from PIL import Image, ImageDraw, ImageFont
    from bentley.episode_builder.shorts import make_caption  # the Pillow caption track (no drawtext)

    canvas = Image.new("RGB", (w, h), bg)
    tmp = path + ".cap.png"

    # top banner so a card is unmistakably a placeholder, never a finished shot
    draw = ImageDraw.Draw(canvas)
    try:
        bf = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Rounded Bold.ttf", 30)
    except Exception:
        bf = ImageFont.load_default()
    banner = "ANIMATIC PLACEHOLDER — no shot rendered yet"
    bw = draw.textlength(banner, font=bf)
    draw.text(((w - bw) / 2, h * 0.07), banner, font=bf, fill=(150, 158, 175))

    th = make_caption(text, tmp, size=66)              # the speaker · beat-id line
    timg = Image.open(tmp).convert("RGBA")
    ty = int(h * 0.40 - th / 2)
    canvas.paste(timg, ((w - timg.width) // 2, ty), timg)
    if sub:
        sh = make_caption(sub, tmp, size=40)           # a short descriptor (line / note)
        simg = Image.open(tmp).convert("RGBA")
        canvas.paste(simg, ((w - simg.width) // 2, ty + th + 24), simg)
    if os.path.exists(tmp):
        os.remove(tmp)
    canvas.save(path)
    return path


def labeled_card_cmd(png, dur, out, w=CANVAS_W, h=CANVAS_H, fps=FPS):
    """ffmpeg command: hold a card PNG for ``dur`` seconds. Video-only; VO muxed by the caller."""
    return ["ffmpeg", "-y", "-loglevel", "error", "-loop", "1", "-i", png,
            "-t", f"{dur:.3f}", "-vf", f"scale={w}:{h},setsar=1,fps={fps},format=yuv420p", "-an"] \
        + list(VENC) + [out]


def labeled_card(text, sub, dur, out, w=CANVAS_W, h=CANVAS_H, fps=FPS, png=None):
    """Build a card PNG (speaker + beat) and hold it for ``dur`` seconds as a video clip."""
    png = png or out.rsplit(".", 1)[0] + ".png"
    card_png(text, sub, png, w=w, h=h)
    run_media(labeled_card_cmd(png, dur, out, w=w, h=h, fps=fps))
    return out
