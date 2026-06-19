"""Shared ffprobe/ffmpeg helpers.

Single source for the media-duration probe that was copy-pasted into assemble, mix,
verify_sync and shorts before the reorg.
"""
import subprocess


def dur(path):
    """Return media duration in seconds via ffprobe."""
    return float(subprocess.check_output(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "csv=p=0", path]).strip())
