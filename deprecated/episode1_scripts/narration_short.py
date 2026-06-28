#!/usr/bin/env python3
"""Re-record the 3 single-shot narration beats SHORTER (Bill) so they fit one native 5s motion
shot cleanly (no overlap, no truncation). Overwrites THEO_FACT1/N06/N10a."""
import os, json, subprocess, urllib.request
KEY = os.environ["ELEVENLABS_API_KEY"]
NARR_VOICE = "pqHfZKP75CvOlQylNhV4"  # Bill (locked narrator)
OUT = "assets/pilot_shots/ep1/v2/audio"
def tts(name, text):
    body = json.dumps({"text": text, "model_id": "eleven_v3",
        "voice_settings": {"stability": 0.5, "similarity_boost": 0.75, "style": 0.4, "speed": 1.04}}).encode()
    req = urllib.request.Request(
        f"https://api.elevenlabs.io/v1/text-to-speech/{NARR_VOICE}?output_format=mp3_44100_192",
        data=body, headers={"xi-api-key": KEY, "Content-Type": "application/json", "Accept": "audio/mpeg"})
    out = f"{OUT}/THEO_{name}.mp3"; raw = out.replace(".mp3", "_raw.mp3")
    with urllib.request.urlopen(req) as r, open(raw, "wb") as f: f.write(r.read())
    subprocess.run(["ffmpeg","-y","-loglevel","error","-i",raw,"-af",
        "highpass=f=80,loudnorm=I=-16:TP=-1.5:LRA=11","-b:a","192k",out], check=True)
    print(f"  {name:6s} {float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',out]).decode().strip()):.1f}s", flush=True)
L = {
 "FACT1": "That's Pip — a hermit crab. He's so soft, he carries his whole house on his back!",
 "N06":   "When a hermit crab grows, his shell does not — so he has to go and find a bigger one.",
 "N10a":  "Soaked and shaken, Bentley carried Pip safely back, up onto the warm, dry rock.",
}
for n, t in L.items(): tts(n, t)
print("SHORT NARRATION DONE", flush=True)
