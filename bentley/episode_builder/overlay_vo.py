#!/usr/bin/env python3
"""Generate the non-shot (overlaid) VO for the 4:45 cut: Theodore narration (George),
Pip cold-open 'Help' O.S. (Callum), Bentley O.S. lines (LauraZ). ElevenLabs only — no fal."""
import os
from bentley.voices.dialogue import tts_bentley, tts_pip, tts_theo

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
if __name__ == "__main__":
    for k, v in THEO.items():    tts_theo(v, f"{OUT}/THEO_{k}.mp3")
    for k, v in PIP_OS.items():  print("  pip", k, flush=True);  tts_pip(v, f"{OUT}/PIPOS_{k}.mp3")
    for k, v in BENT_OS.items(): print("  bent", k, flush=True); tts_bentley(v, f"{OUT}/BENTOS_{k}.mp3")
    print("OVERLAY VO DONE ->", OUT, flush=True)
