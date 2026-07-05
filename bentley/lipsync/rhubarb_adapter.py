"""Run the vendored Rhubarb on a production VO line and emit a project-viseme timeline.

Contract (plan amendment, all pinned): vendored binary tools/rhubarb/... (v1.14.0, NOT on PATH);
MP3 -> 16k mono WAV transcode first (Rhubarb accepts WAV/OGG only); ALWAYS pass --dialogFile with
the line's REAL transcript; -r pocketSphinx; --extendedShapes GHX; validate output cues."""
import json
import subprocess
import tempfile
from pathlib import Path

from bentley.lipsync.visemes import RHUBARB_MAP, map_cue, validate_cues

ROOT = Path(__file__).resolve().parents[2]
RHUBARB = ROOT / "tools/rhubarb/Rhubarb-Lip-Sync-1.14.0-macOS/rhubarb"


def transcript_for(label, script_md=ROOT / "episodes/ep3/EP3_SCRIPT.md"):
    """Look up a line's real transcript from the episode script (`label | speaker | text`)."""
    for line in Path(script_md).read_text().splitlines():
        parts = [p.strip() for p in line.split("|")]
        if len(parts) >= 3 and parts[0] == label:
            return parts[2]
    raise KeyError(f"no transcript for {label!r} in {script_md}")


def run_rhubarb(audio_path, transcript, workdir=None):
    """audio (mp3/wav) + real transcript -> raw Rhubarb mouthCues [{start,end,value}]."""
    if not RHUBARB.exists():
        raise FileNotFoundError(f"vendored rhubarb missing at {RHUBARB}")
    wd = Path(workdir or tempfile.mkdtemp(prefix="lipsync_"))
    wd.mkdir(parents=True, exist_ok=True)
    audio = Path(audio_path)
    wav = wd / (audio.stem + ".wav")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(audio),
                    "-ar", "16000", "-ac", "1", str(wav)], check=True)
    dialog = wd / (audio.stem + ".txt")
    dialog.write_text(transcript)
    out = wd / (audio.stem + ".json")
    subprocess.run([str(RHUBARB), "-r", "pocketSphinx", "--extendedShapes", "GHX",
                    "--dialogFile", str(dialog), "-f", "json", "-o", str(out), str(wav)], check=True)
    cues = json.loads(out.read_text())["mouthCues"]
    for c in cues:  # validate the alphabet before anything downstream trusts it
        if c["value"] not in RHUBARB_MAP:
            raise ValueError(f"rhubarb emitted unknown cue {c['value']!r}")
    return cues


def viseme_timeline(audio_path, transcript, available=None, workdir=None):
    """Full adapter: audio+transcript -> validated project-viseme timeline [{start,end,viseme}]."""
    raw = run_rhubarb(audio_path, transcript, workdir)
    cues = [{"start": c["start"], "end": c["end"],
             "viseme": map_cue(c["value"], available), "source": f"rhubarb:{c['value']}"}
            for c in raw]
    return validate_cues(cues)
