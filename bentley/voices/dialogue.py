"""Character dialogue TTS — Bentley (LauraZ), Pip (Callum +10% pitch), Theodore (George, legacy).

Built on bentley.shared.eleven (voice IDs live there). Before the reorg these were embedded in
pipeline.py, and ``tts_theo`` was duplicated verbatim across overlay_vo.py and supp_vo.py.
"""
import subprocess

from bentley.shared import eleven
from bentley.shared.audio import clean_master


def tts_bentley(text, outp):
    """Bentley — EXPRESSIVE config (owner note 2026-07-04: 'genuinely excited/curious/amused, never
    flat'): style 0.85 / stability 0.25 (the energy config the owner picked for Marco) + v3 emotive
    tags in the line text. NOTE: eleven_v3 varies take-to-take — production recording uses BEST-OF-3
    with a measured pick (see scratch/ep4/record_best_of.py pattern), not a single roll."""
    raw = outp.replace(".mp3", "_raw.mp3")
    eleven.speak(eleven.BENTLEY, text, raw,
                 settings={"stability": 0.25, "similarity_boost": 0.75, "style": 0.85, "speed": 1.15})
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


def tts_marco(text, outp):
    """Marco — Ep3 guest harvester ant (boy). Small, bright, quick, brave — a tiny voice with a big
    spark; faster cadence than Indi, lighter than Bentley. Voice owner-picked 2026-06-28; LOCKED
    delivery = +6% pitch, peppier ('marco_younger_excited' take the owner chose)."""
    raw = outp.replace(".mp3", "_raw.mp3")
    cln = outp.replace(".mp3", "_clean.mp3")
    eleven.speak(eleven.MARCO, text, raw,
                 settings={"stability": 0.25, "similarity_boost": 0.7, "style": 0.85, "speed": 1.14})  # energy "A" (owner-picked)
    clean_master(raw, cln)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", cln, "-af",
                    "asetrate=44100*1.06,aresample=44100,atempo=0.99,highpass=f=120,"
                    "loudnorm=I=-16:TP=-1.5:LRA=11", "-b:a", "192k", outp], check=True)
    return outp


def tts_mira(text, outp):
    """Mira — Ep4 guest monarch butterfly (girl). Playful, fearless, giggly — the joy of the journey.
    Voice owner-picked 2026-07-03 (library voice; take 'I_mlv2_clean'): model **eleven_multilingual_v2**
    (preserves the voice's native character/accent; v3 flattened it), NATURAL pitch (no shift), the
    committed clean_master ('D bright') chain. NOTE: mlv2 does NOT support v3 audio tags like
    [giggling] — bracketed tags are stripped here; shape emotion with punctuation and word choice."""
    import re
    text = re.sub(r"\[[^\]]*\]\s*", "", text)  # strip v3-style emotive tags (mlv2 would read them)
    raw = outp.replace(".mp3", "_raw.mp3")
    eleven.speak(eleven.MIRA, text, raw, model="eleven_multilingual_v2",
                 settings={"stability": 0.45, "similarity_boost": 0.9, "style": 0.3})
    clean_master(raw, outp)
    return outp


def tts_catchphrase(outp, gap=0.45):
    """Bentley's signature 'Stop. Look. Listen.' — ALWAYS Bentley's voice, with deliberate pauses between
    each word. Recorded as ONE natural utterance ("Stop. Look. Listen." — the periods give the deliberate
    beats). NOTE: word-by-word generation + silence-stitching (the old method) produced the recurring
    "broken/stuttery" catchphrase across EP1/EP2/EP3; the single utterance is the durable fix.
    Owner-locked take A, 2026-06-28. `gap` kept for signature compatibility (unused). See bentley-catchphrase.
    """
    raw = outp.replace(".mp3", "_raw.mp3")
    eleven.speak(eleven.BENTLEY, "Stop. Look. Listen.", raw,
                 settings={"stability": 0.4, "similarity_boost": 0.8, "style": 0.45, "speed": 1.0})
    clean_master(raw, outp)
    return outp
