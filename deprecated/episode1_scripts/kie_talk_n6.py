#!/usr/bin/env python3
"""Prove the kie.ai TALKING path end-to-end:
   1) generate N6 Bentley VO (locked LauraZ eleven_v3, cleaned)
   2) host keyframe + VO publicly on fal storage (kie avatar needs public URLs)
   3) drive kie.ai kling/ai-avatar-standard -> lip-synced N6 clip
Reports avatar credit cost + seconds."""
import os, json, subprocess, urllib.request, fal_client
from kie_client import run, credits, download

ELEVEN_KEY = os.environ["ELEVENLABS_API_KEY"]
BENTLEY_VOICE = "jkNABRZGatAuwawcS9xX"

def clean_master(inp, outp):
    subprocess.run(["ffmpeg","-y","-loglevel","error","-i",inp,"-af",
      "highpass=f=85,equalizer=f=220:t=q:w=1.2:g=-1.5,equalizer=f=5800:t=q:w=2:g=-2,equalizer=f=10000:t=h:w=1:g=2,loudnorm=I=-16:TP=-1.5:LRA=11",
      "-b:a","192k",outp], check=True)

def tts_bentley(text, outp):
    body = json.dumps({"text":text,"model_id":"eleven_v3",
        "voice_settings":{"stability":0.3,"similarity_boost":0.75,"style":0.6,"speed":1.12}}).encode()
    req = urllib.request.Request(
        f"https://api.elevenlabs.io/v1/text-to-speech/{BENTLEY_VOICE}?output_format=mp3_44100_192",
        data=body, headers={"xi-api-key":ELEVEN_KEY,"Content-Type":"application/json","Accept":"audio/mpeg"})
    raw = outp.replace(".mp3","_raw.mp3")
    with urllib.request.urlopen(req) as r, open(raw,"wb") as f: f.write(r.read())
    clean_master(raw, outp); return outp

# 1) VO
LINE = "[warm, fond] And hey — turns out I was a little bit right. You ARE a tiny knight... in brand-new shiny armor."
VO = "assets/pilot_shots/hybrid_ep1/v2/audio/BENTOS_n6armor.mp3"
tts_bentley(LINE, VO)
dur = float(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",VO]).strip())
print(f"VO -> {VO}  ({dur:.2f}s)")

# 2) host on fal (stable public URLs)
img_url = fal_client.upload_file("tests/kie/N6_kie_key_bright2.png")
aud_url = fal_client.upload_file(VO)
print("img_url:", img_url)
print("aud_url:", aud_url)

# 3) kie avatar
print("bal before:", credits())
r = run("kling/ai-avatar-standard", {
    "image_url": img_url, "audio_url": aud_url,
    "prompt": ("Bentley the red-fawn Boxer puppy speaks warmly and fondly straight to camera with a gentle affectionate "
               "head-tilt; soft natural small-dog mouth movements in time with her words, soulful loving eyes, calm and "
               "tender. Bright daylight on her face, ears stay floppy down, no human teeth.")
}, timeout=600)
download(r["urls"][0], "tests/kie/N6_kie_talk.mp4")
print(f"DONE AVATAR  credits={r['credits']}  secs={r['secs']}")
print("url:", r["urls"][0])
print("bal after:", credits())
