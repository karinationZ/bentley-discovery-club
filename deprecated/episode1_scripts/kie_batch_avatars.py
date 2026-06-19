#!/usr/bin/env python3
"""Tier-1 batch PHASE 2 — 3 talking Avatars in parallel, then grade each.
Reads tests/kie/batch/manifest.json (keyframe catbox URLs). a1_02/a5_04 reuse existing VO; N1 VO generated."""
import os, json, subprocess, urllib.request, concurrent.futures
from kie_client import run, download

ELEVEN_KEY = os.environ["ELEVENLABS_API_KEY"]
BENTLEY_VOICE = "jkNABRZGatAuwawcS9xX"
def clean_master(inp, outp):
    subprocess.run(["ffmpeg","-y","-loglevel","error","-i",inp,"-af",
      "highpass=f=85,equalizer=f=220:t=q:w=1.2:g=-1.5,equalizer=f=5800:t=q:w=2:g=-2,equalizer=f=10000:t=h:w=1:g=2,loudnorm=I=-16:TP=-1.5:LRA=11",
      "-b:a","192k",outp], check=True)
def tts_bentley(text, outp):
    body = json.dumps({"text":text,"model_id":"eleven_v3",
        "voice_settings":{"stability":0.3,"similarity_boost":0.75,"style":0.6,"speed":1.12}}).encode()
    req = urllib.request.Request(f"https://api.elevenlabs.io/v1/text-to-speech/{BENTLEY_VOICE}?output_format=mp3_44100_192",
        data=body, headers={"xi-api-key":ELEVEN_KEY,"Content-Type":"application/json","Accept":"audio/mpeg"})
    raw = outp.replace(".mp3","_raw.mp3")
    with urllib.request.urlopen(req) as r, open(raw,"wb") as f: f.write(r.read())
    clean_master(raw, outp); return outp

def host(path):
    u = subprocess.check_output(["curl","-s","-F","reqtype=fileupload","-F",f"fileToUpload=@{path}",
                                 "https://catbox.moe/user/api.php"]).decode().strip()
    if not u.startswith("http"): raise RuntimeError("catbox fail: "+u[:80])
    return u

GRADE = ("curves=master='0/0.045 0.25/0.30 0.5/0.58 0.78/0.85 1/0.965',eq=saturation=1.22:contrast=1.05:brightness=0.02,"
         "colorbalance=rs=.01:gs=0:bs=.01:rm=.04:gm=0:bm=-.03:rh=.02:gh=.01:bh=-.02,unsharp=3:3:0.35:3:3:0.0,format=yuv420p")
AUD = "assets/pilot_shots/hybrid_ep1/v2/audio"
manifest = json.load(open("tests/kie/batch/manifest.json"))
SHOTS = {
 "a1_02_react": {"vo": f"{AUD}/a1_02_NEW.mp3",
   "prompt": ("Bentley the red-fawn Boxer puppy reacts with bright surprise and delighted curiosity as she hears a faraway "
              "cry — eyes wide, head lifting and turning, soft natural small-dog mouth moving gently in time with her words, "
              "ears floppy down, no human teeth. Bright daylight on her face.")},
 "a5_04_tag": {"vo": f"{AUD}/a5_04_NEW.mp3",
   "prompt": ("Bentley the red-fawn Boxer puppy speaks warmly and playfully straight to camera with a gentle affectionate "
              "head-tilt, soft natural small-dog mouth in time with her words, soulful loving eyes, ears floppy down, no "
              "human teeth. Bright daylight on her face.")},
 "N1_guess": {"vo": f"{AUD}/BENTOS_n1guess.mp3",
   "line": "[playful, delighted, rapid-fire] Ooh — are you a snail? A teeny tiny knight in shiny armor? A rock that talks?!",
   "prompt": ("Bentley the red-fawn Boxer puppy delightedly rattles off playful guesses to camera with bright happy energy "
              "and a gentle head-tilt, soft natural small-dog mouth moving in time with her rapid words, sparkling eyes, "
              "ears floppy down, no human teeth. Bright daylight on her face.")},
}

def worker(sid):
    s = SHOTS[sid]; vo = s["vo"]
    if "line" in s and not os.path.exists(vo): tts_bentley(s["line"], vo)
    aud = host(vo); img = manifest[sid]["cat_url"]
    r = run("kling/ai-avatar-standard", {"image_url": img, "audio_url": aud, "prompt": s["prompt"]}, timeout=900)
    raw = f"tests/kie/batch/{sid}_talk.mp4"; download(r["urls"][0], raw)
    grd = f"tests/kie/batch/{sid}_talk_graded.mp4"
    subprocess.run(["ffmpeg","-y","-loglevel","error","-i",raw,"-vf",GRADE,
                    "-c:v","libx264","-crf","18","-preset","medium","-c:a","copy",grd], check=True)
    vodur = float(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",vo]).strip())
    return {"sid": sid, "credits": r["credits"], "secs": r["secs"], "vo_dur": round(vodur,2), "raw": raw, "graded": grd}

results = {}
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:
    futs = {ex.submit(worker, s): s for s in SHOTS}
    for f in concurrent.futures.as_completed(futs):
        sid = futs[f]
        try:
            d = f.result(); results[sid] = d
            print(f"DONE {sid}: {d['credits']}cr {d['secs']}s  VO={d['vo_dur']}s")
        except Exception as e:
            print(f"FAIL {sid}: {type(e).__name__}: {e}")
json.dump(results, open("tests/kie/batch/avatars_result.json","w"), indent=1)
print("total avatar credits:", sum(d["credits"] for d in results.values()))
