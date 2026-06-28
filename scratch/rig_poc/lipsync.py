#!/usr/bin/env python3
"""POC building block of the rigged pipeline: FREE deterministic lip-sync via Rhubarb (MIT).

VO mp3 (+ optional transcript for accuracy) -> list of mouth-shape cues {start,end,value}.
Each `value` (X/A/B/C/D/E/F/G/H, Preston-Blair set) maps to ONE pose on the character rig. Author a
TOOTHLESS dog/cephalopod mouth set once, and every line lip-syncs for $0, with no human teeth possible.
This replaces per-shot AI rolls for the talking layer. Whole thing is plain Python + a CLI.

Install (production): download Rhubarb from github.com/DanielSWolf/rhubarb-lip-sync/releases and point
RHUBARB at the binary (or put it on PATH).
"""
import json, subprocess, tempfile
from pathlib import Path

RHUBARB = Path("/tmp/rhubarb_poc/Rhubarb-Lip-Sync-1.14.0-macOS/rhubarb")  # POC path


def lipsync(vo_path, transcript=None):
    """Return mouth cues for a VO file. transcript (the line's text) improves accuracy."""
    wav = Path(tempfile.mktemp(suffix=".wav"))
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(vo_path), "-ar", "44100", "-ac", "1", str(wav)], check=True)
    cmd = [str(RHUBARB), "-f", "json", str(wav)]
    if transcript:
        tf = Path(tempfile.mktemp(suffix=".txt")); tf.write_text(transcript)
        cmd = [str(RHUBARB), "-f", "json", "--dialogFile", str(tf), str(wav)]
    cues = json.loads(subprocess.check_output(cmd, stderr=subprocess.DEVNULL).decode())["mouthCues"]
    wav.unlink(missing_ok=True)
    return cues


if __name__ == "__main__":
    import sys
    cues = lipsync(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None)
    print(f"{len(cues)} cues:", " ".join(c["value"] for c in cues))
