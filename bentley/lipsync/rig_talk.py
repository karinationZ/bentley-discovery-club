"""One-command 3D-rig lip-sync: a VO line -> a synced talking clip. Deterministic, $0, no drift.

Reusable for ANY line and ANY rigged character (pass a different --rig .blend).
Chain: rhubarb (audio+transcript) -> project viseme timeline -> jaw-openness curve -> Blender jaw
bone render -> ffmpeg mux with the original audio.

  python -m bentley.lipsync.rig_talk \
      --audio episodes/ep3/vo/B_strong.mp3 --label B_strong \
      --out scratch/rig_build/B_strong_talk.mp4
"""
import argparse
import subprocess
import tempfile
from pathlib import Path

from bentley.lipsync.rhubarb_adapter import viseme_timeline, transcript_for
from bentley.lipsync.openness import write_openness

ROOT = Path(__file__).resolve().parents[2]
BLENDER = "/Applications/Blender.app/Contents/MacOS/Blender"
RENDER_SCRIPT = ROOT / "scratch/rig_build/render_talk.py"
DEFAULT_RIG = ROOT / "scratch/rig_build/bentley_rig_v1.blend"


def rig_talk(audio, transcript, out, rig=DEFAULT_RIG, max_deg=8.0, fps=24, workdir=None):
    audio, rig, out = Path(audio), Path(rig), Path(out)
    wd = Path(workdir or tempfile.mkdtemp(prefix="rigtalk_"))
    frames = wd / "frames"
    frames.mkdir(parents=True, exist_ok=True)
    # 1) audio + real transcript -> validated project viseme timeline
    cues = viseme_timeline(str(audio), transcript, workdir=str(wd / "rh"))
    # 2) viseme timeline -> per-frame jaw-openness curve
    op = wd / "openness.json"
    data = write_openness(cues, op, fps=fps)
    # 3) drive the rig's jaw bone + render frames (Blender headless)
    subprocess.run([BLENDER, "-b", str(rig), "-P", str(RENDER_SCRIPT), "--",
                    str(op), str(frames), str(max_deg)], check=True)
    # 4) mux frames + the ORIGINAL locked-voice audio
    pngs = sorted(frames.glob("f_*.png"))
    if not pngs:
        raise RuntimeError(f"no frames rendered in {frames}")
    start = int(pngs[0].stem.split("_")[1])
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(fps),
                    "-start_number", str(start), "-i", str(frames / "f_%04d.png"),
                    "-i", str(audio), "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18",
                    "-c:a", "aac", "-shortest", str(out)], check=True)
    return out, data


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--audio", required=True)
    ap.add_argument("--transcript", help="the line text; omit to resolve from --label")
    ap.add_argument("--label", help="VO label to look up in the episode script")
    ap.add_argument("--rig", default=str(DEFAULT_RIG))
    ap.add_argument("--out", required=True)
    ap.add_argument("--max-deg", type=float, default=8.0)
    ap.add_argument("--fps", type=int, default=24)
    a = ap.parse_args()
    transcript = a.transcript or transcript_for(a.label)
    out, data = rig_talk(a.audio, transcript, a.out, rig=a.rig, max_deg=a.max_deg, fps=a.fps)
    print(f"-> {out}  ({data['dur']}s, {len(data['open'])} frames, deterministic, $0)")


if __name__ == "__main__":
    main()
