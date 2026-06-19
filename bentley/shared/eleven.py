"""ElevenLabs config — API key + LOCKED voice IDs (single source) + low-level TTS POST.

Voice canon (see docs/rules/ and the youtube_vault Voice Rules note):
the voice IDs were previously scattered across pipeline.py, overlay_vo.py, supp_vo.py
and narration_bill.py. They live here now.
"""
import json
import os
import urllib.request

KEY = os.environ["ELEVENLABS_API_KEY"]

# ── LOCKED voice IDs ────────────────────────────────────────────────
BENTLEY = "jkNABRZGatAuwawcS9xX"      # LauraZ — Bentley
PIP = "N2lVS1w4EtoT3dr4eOWO"          # Callum — Pip (pitched +10% at render time)
NARRATOR = "pqHfZKP75CvOlQylNhV4"     # Bill   — Grandpa Theodore narrator (LOCKED, current canon)
THEO_GEORGE = "JBFqnCBsd6RMkjVDRZzb"  # George — legacy narrator, superseded by Bill

_TTS_URL = "https://api.elevenlabs.io/v1/text-to-speech/{voice}?output_format={fmt}"


def speak(voice_id, text, out_raw, *, model="eleven_v3", settings=None,
          fmt="mp3_44100_192"):
    """POST ``text`` to ElevenLabs TTS and write the raw mp3 to ``out_raw``.

    Callers apply their own ffmpeg cleanup / pitch afterward (see voices.dialogue).
    """
    body = json.dumps({"text": text, "model_id": model,
                       "voice_settings": settings}).encode()
    req = urllib.request.Request(
        _TTS_URL.format(voice=voice_id, fmt=fmt), data=body,
        headers={"xi-api-key": KEY, "Content-Type": "application/json",
                 "Accept": "audio/mpeg"})
    with urllib.request.urlopen(req) as r, open(out_raw, "wb") as f:
        f.write(r.read())
    return out_raw
