"""Shared audio post-processing (ffmpeg)."""
import subprocess

# Committed "clean master" chain for dialogue: de-rumble, de-mud, REAL de-esser, presence, sparkle,
# loudnorm -16. Owner-picked "D bright" 2026-07-03 (EP4+): the OLD chain's blunt -2dB EQ cut at 5.8kHz
# was the root cause of the "muffled / inside-a-jar" Bentley — it dulled ALL consonants (measured 0.28%
# 4-10kHz energy vs 0.33% raw). The deesser tames S-hiss only; presence + treble restore clarity (0.44%).
_CLEAN_AF = ("highpass=f=85,equalizer=f=220:t=q:w=1.2:g=-1.5,"
             "deesser=i=0.35,equalizer=f=3400:t=q:w=1.6:g=2,"
             "treble=g=2.5:f=7500:w=0.6,loudnorm=I=-16:TP=-1.5:LRA=11")


def clean_master(inp, outp):
    """Apply the committed dialogue clean-up chain: inp -> outp (192k mp3)."""
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", inp,
                    "-af", _CLEAN_AF, "-b:a", "192k", outp], check=True)
