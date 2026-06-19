"""Character dialogue TTS — Bentley (LauraZ), Pip (Callum +10% pitch), Theodore (George, legacy).

Built on bentley.shared.eleven (voice IDs live there). Before the reorg these were embedded in
pipeline.py, and ``tts_theo`` was duplicated verbatim across overlay_vo.py and supp_vo.py.
"""
import subprocess

from bentley.shared import eleven
from bentley.shared.audio import clean_master


def tts_bentley(text, outp):
    raw = outp.replace(".mp3", "_raw.mp3")
    eleven.speak(eleven.BENTLEY, text, raw,
                 settings={"stability": 0.3, "similarity_boost": 0.75, "style": 0.6, "speed": 1.12})
    clean_master(raw, outp)
    return outp


def tts_pip(text, outp):
    raw = outp.replace(".mp3", "_raw.mp3")
    eleven.speak(eleven.PIP, text, raw,
                 settings={"stability": 0.35, "similarity_boost": 0.75, "style": 0.65, "speed": 1.05})
    a = round(1 / 1.10, 4)  # pitch +10% (asetrate up, atempo back) -> small crab
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", raw, "-af",
                    f"asetrate={int(44100 * 1.10)},aresample=44100,atempo={a},highpass=f=110,"
                    "equalizer=f=300:t=q:w=1:g=-1,loudnorm=I=-16:TP=-1.5:LRA=11",
                    "-b:a", "192k", outp], check=True)
    return outp


def tts_theo(text, outp):
    """Legacy George narrator. Current narration canon is Bill — see voices/narration.py."""
    raw = outp.replace(".mp3", "_raw.mp3")
    eleven.speak(eleven.THEO_GEORGE, text, raw,
                 settings={"stability": 0.45, "similarity_boost": 0.75, "style": 0.45, "speed": 0.95})
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", raw, "-af",
                    "highpass=f=80,loudnorm=I=-16:TP=-1.5:LRA=11", "-b:a", "192k", outp], check=True)
    return outp
