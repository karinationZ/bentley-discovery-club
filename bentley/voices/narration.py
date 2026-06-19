#!/usr/bin/env python3
"""LOCKED narrator = Bill (wise/mature grandpa). Regenerate ALL Theodore narration in Bill's
voice, overwriting the George versions in v2/audio/THEO_*.mp3."""
import os, json, subprocess, urllib.request
from bentley.shared.eleven import KEY, NARRATOR as NARR_VOICE  # Bill — Grandpa Theodore (LOCKED)
OUT = "assets/pilot_shots/hybrid_ep1/v2/audio"; os.makedirs(OUT, exist_ok=True)
def tts(name, text):
    body = json.dumps({"text": text, "model_id": "eleven_v3",
        "voice_settings": {"stability": 0.5, "similarity_boost": 0.75, "style": 0.4, "speed": 1.0}}).encode()
    req = urllib.request.Request(
        f"https://api.elevenlabs.io/v1/text-to-speech/{NARR_VOICE}?output_format=mp3_44100_192",
        data=body, headers={"xi-api-key": KEY, "Content-Type": "application/json", "Accept": "audio/mpeg"})
    out = f"{OUT}/THEO_{name}.mp3"; raw = out.replace(".mp3", "_raw.mp3")
    with urllib.request.urlopen(req) as r, open(raw, "wb") as f: f.write(r.read())
    subprocess.run(["ffmpeg","-y","-loglevel","error","-i",raw,"-af",
        "highpass=f=80,loudnorm=I=-16:TP=-1.5:LRA=11","-b:a","192k",out], check=True)
    d = subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",out]).decode().strip()
    print(f"  {name:8s} {float(d):5.1f}s", flush=True)
L = {
 "INTRO1": "Every morning, before the world wakes up... the ocean leaves Crystal Cove full of secrets.",
 "INTRO2": "And this... is Bentley. She's not the biggest pup on the beach... but nobody, nobody, is more curious.",
 "INTRO3": "While everyone else just runs right past... Bentley stops. She looks. And she listens.",
 "INTRO4": "Because when you really listen... the whole world starts talking back.",
 "FACT1": "That's Pip — a hermit crab. He's so soft, he has to wear a borrowed seashell like a backpack, and carry his whole house on his back everywhere he goes.",
 "FACT2": "A hermit crab can feel when his shell gets too snug — just like outgrowing your favorite shoes. So he has to go shopping for a bigger one.",
 "FACT3": "Here's what the big dog didn't know: little shore crabs like Pip can't swim at all. They walk on the sea floor — so a big wave isn't fun, it's the scariest thing in the world.",
 "FACT4": "Hermit crabs never waste a good home. When one crab leaves a shell behind, it becomes someone else's brand-new house — the ocean's very own hand-me-downs.",
 "FACT5": "Scientists really do call it a vacancy chain — and they've filmed dozens of real crabs doing it on beaches all over the world. It's true!",
 "N02b": "Wherever there's a creature in trouble... that's exactly where Bentley wants to be.",
 "N06": "When a hermit crab grows, its house does not. So it has to find a bigger, empty shell... and move. A brand-new home, every single time it grows.",
 "N10a": "Soaked, and a little shaken, Bentley carried Pip back from the edge — up onto the warm, dry rock — and shook the whole ocean right off.",
 "N11": "So Bentley did the bravest thing of all... she stopped. She looked. And she listened.",
 "N16": "Scientists call it a vacancy chain — a whole neighborhood, trading homes all at once. And it's real. The very last shell... fit Pip perfectly.",
 "N19": "Today, Bentley learned you don't help by grabbing. You help by listening. Stop... look... listen...",
 "outro": "Next time, on Bentley's Big Adventures... The Octopus Escape Artist. Tap to dive in — and don't forget to follow, so Bentley can find you for the next adventure.",
}
if __name__ == "__main__":
    for n, t in L.items(): tts(n, t)
    print("BILL NARRATION DONE", flush=True)
