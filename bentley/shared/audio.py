"""Shared audio post-processing (ffmpeg)."""
import subprocess

# Committed "clean master" chain for dialogue: de-rumble, de-mud, de-ess, presence, loudnorm -16.
_CLEAN_AF = ("highpass=f=85,equalizer=f=220:t=q:w=1.2:g=-1.5,"
             "equalizer=f=5800:t=q:w=2:g=-2,equalizer=f=10000:t=h:w=1:g=2,"
             "loudnorm=I=-16:TP=-1.5:LRA=11")


def clean_master(inp, outp):
    """Apply the committed dialogue clean-up chain: inp -> outp (192k mp3)."""
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", inp,
                    "-af", _CLEAN_AF, "-b:a", "192k", outp], check=True)
