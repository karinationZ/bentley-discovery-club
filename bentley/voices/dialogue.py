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


def tts_indi(text, outp):
    """Indi — Ep2 guest octopus. Shy, intelligent, guarded-but-warm. Voice LOCKED 2026-06-20."""
    raw = outp.replace(".mp3", "_raw.mp3")
    eleven.speak(eleven.INDI, text, raw,
                 settings={"stability": 0.4, "similarity_boost": 0.75, "style": 0.45, "speed": 0.95})
    clean_master(raw, outp)
    return outp


def tts_catchphrase(outp, gap=0.45):
    """Bentley's signature 'Stop. Look. Listen.' — ALWAYS Bentley's voice, ALWAYS with a deliberate
    pause between each word (like Ep1). HARD RULE for every episode. Each word is generated, trimmed of
    lead/tail silence, then stitched with a fixed `gap` of silence so the pacing is identical every time.
    See memory: bentley-catchphrase.
    """
    import os
    d = os.path.dirname(os.path.abspath(outp)) or "."
    words = ["Stop.", "Look.", "Listen."]
    segs = []
    for i, w in enumerate(words):
        seg = os.path.join(d, f"_cp_{i}.mp3"); raw = seg.replace(".mp3", "_raw.mp3")
        eleven.speak(eleven.BENTLEY, w, raw,
                     settings={"stability": 0.35, "similarity_boost": 0.8, "style": 0.5, "speed": 1.0})
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", raw, "-af",
                        "silenceremove=start_periods=1:start_silence=0.03:start_threshold=-40dB,areverse,"
                        "silenceremove=start_periods=1:start_silence=0.03:start_threshold=-40dB,areverse,"
                        "highpass=f=80,loudnorm=I=-16:TP=-1.5:LRA=11",
                        "-ac", "1", "-ar", "44100", "-b:a", "192k", seg], check=True)
        segs.append(seg)
    sil = os.path.join(d, "_cp_sil.mp3")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "lavfi", "-i", "anullsrc=r=44100:cl=mono",
                    "-t", str(gap), "-ac", "1", "-ar", "44100", "-b:a", "192k", sil], check=True)
    listf = os.path.join(d, "_cp_list.txt")
    with open(listf, "w") as f:
        f.write(f"file '{segs[0]}'\n")
        for s in segs[1:]:
            f.write(f"file '{sil}'\nfile '{s}'\n")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", listf,
                    "-c:a", "libmp3lame", "-b:a", "192k", outp], check=True)
    return outp
