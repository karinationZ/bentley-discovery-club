#!/usr/bin/env python3
"""Generate the non-shot (overlaid) VO for the 4:45 cut: Theodore narration (George),
Pip cold-open 'Help' O.S. (Callum), Bentley O.S. lines (LauraZ). ElevenLabs only — no fal."""
import os, sys, json, subprocess, urllib.request
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pipeline import tts_bentley, tts_pip, ELEVEN_KEY

THEO_VOICE = "JBFqnCBsd6RMkjVDRZzb"  # George — warm captivating storyteller
def tts_theo(text, outp):
    body = json.dumps({"text": text, "model_id": "eleven_v3",
        "voice_settings": {"stability": 0.45, "similarity_boost": 0.75, "style": 0.45, "speed": 0.95}}).encode()
    req = urllib.request.Request(
        f"https://api.elevenlabs.io/v1/text-to-speech/{THEO_VOICE}?output_format=mp3_44100_192",
        data=body, headers={"xi-api-key": ELEVEN_KEY, "Content-Type": "application/json", "Accept": "audio/mpeg"})
    raw = outp.replace(".mp3", "_raw.mp3")
    with urllib.request.urlopen(req) as r, open(raw, "wb") as f: f.write(r.read())
    subprocess.run(["ffmpeg","-y","-loglevel","error","-i",raw,"-af",
        "highpass=f=80,loudnorm=I=-16:TP=-1.5:LRA=11","-b:a","192k",outp], check=True)
    print("  theo ok ->", os.path.basename(outp), flush=True); return outp

OUT = "assets/pilot_shots/hybrid_ep1/v2/audio"; os.makedirs(OUT, exist_ok=True)

THEO = {
 "N02b": "Wherever there's a creature in trouble... that's exactly where Bentley wants to be.",
 "N06":  "When a hermit crab grows, its house does NOT. So it has to find a bigger, empty shell... and move. A brand-new home, every single time it grows.",
 "N10a": "Soaked, and a little shaken, Bentley carried Pip back from the edge — up onto the warm, dry rock — and shook the whole ocean right off.",
 "N11":  "So Bentley did the bravest thing of all... she stopped. She looked. And she listened.",
 "N16":  "Scientists call it a vacancy chain — a whole neighborhood, trading homes all at once. And it's real. The very last shell... fit Pip perfectly.",
 "N19":  "Today, Bentley learned you don't help by grabbing. You help by listening. Stop... look... listen...",
 "outro":"Next time, on Bentley's Big Adventures... The Octopus Escape Artist. Tap to dive in — and don't forget to follow, so Bentley can find YOU for the next adventure.",
}
PIP_OS = {
 "help1": "[frightened, trembling] ...H-help? Is — is anybody out there? Please?",
 "help2": "[anxious] It's getting hot out here... and I am NOT okay with that.",
}
BENT_OS = {
 "track":  "[murmuring, sniffing] Okay okay okay — this way... little voice, where ARE you...",
 "awe_n2": "[quiet awe] Whoa... a whole new house, just for getting bigger?",
 "chain":  "[building, dawning] One moves... and they ALL move... ohh—!",
 "octo":   "[delighted] ...Wait. Did that octopus just WAVE at me?! Ooh — new friend!",
}
for k, v in THEO.items():    tts_theo(v, f"{OUT}/THEO_{k}.mp3")
for k, v in PIP_OS.items():  print("  pip", k, flush=True);  tts_pip(v, f"{OUT}/PIPOS_{k}.mp3")
for k, v in BENT_OS.items(): print("  bent", k, flush=True); tts_bentley(v, f"{OUT}/BENTOS_{k}.mp3")
print("OVERLAY VO DONE ->", OUT, flush=True)
