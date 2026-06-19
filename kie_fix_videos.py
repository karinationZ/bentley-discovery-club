#!/usr/bin/env python3
"""Round-2 fixes PHASE 2 — 2 Pip VO segments + 4 videos in parallel:
   BR3 (motion 5s), a3_02a wave (motion 10s, ALIVE water), octopus (motion 10s + splash), a3_02b Pip CU (Avatar, lip-synced)."""
import os, json, subprocess, urllib.request, concurrent.futures
from kie_client import run, download
ELEVEN_KEY = os.environ["ELEVENLABS_API_KEY"]
PIP_VOICE = "N2lVS1w4EtoT3dr4eOWO"
AUD = "assets/pilot_shots/hybrid_ep1/v2/audio"
FIX = "tests/kie/fix"

def tts_pip(text, outp):
    body = json.dumps({"text":text,"model_id":"eleven_v3",
        "voice_settings":{"stability":0.35,"similarity_boost":0.75,"style":0.65,"speed":1.05}}).encode()
    req = urllib.request.Request(f"https://api.elevenlabs.io/v1/text-to-speech/{PIP_VOICE}?output_format=mp3_44100_192",
        data=body, headers={"xi-api-key":ELEVEN_KEY,"Content-Type":"application/json","Accept":"audio/mpeg"})
    raw = outp.replace(".mp3","_raw.mp3")
    with urllib.request.urlopen(req) as r, open(raw,"wb") as f: f.write(r.read())
    a = round(1/1.10,4)
    subprocess.run(["ffmpeg","-y","-loglevel","error","-i",raw,"-af",
      f"asetrate={int(44100*1.10)},aresample=44100,atempo={a},highpass=f=110,equalizer=f=300:t=q:w=1:g=-1,loudnorm=I=-16:TP=-1.5:LRA=11",
      "-b:a","192k",outp], check=True)
    return outp
def host(p):
    u = subprocess.check_output(["curl","-s","-F","reqtype=fileupload","-F",f"fileToUpload=@{p}",
                                 "https://catbox.moe/user/api.php"]).decode().strip()
    if not u.startswith("http"): raise RuntimeError("catbox fail: "+u[:80])
    return u
def vdur(p): return float(subprocess.check_output(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",p]).strip())

# --- VO segments (locked Pip = Callum +10%) ---
SEG1 = "[full panic] NO no no — look at it! That's the OPEN surf! I can't swim — crabs like me walk, we don't swim!"
SEG2 = "[panic, pleading] Those waves would smash me on the rocks and tumble me right OUT of my shell! And you said it — my shell isn't part of me. It'd float away, and I'd be soft, and bare... and gone."
vo1 = f"{AUD}/PIPOS_wave1.mp3"; vo2 = f"{AUD}/PIPOS_wave2.mp3"
tts_pip(SEG1, vo1); tts_pip(SEG2, vo2)
print(f"VO seg1={vdur(vo1):.2f}s  seg2={vdur(vo2):.2f}s")
seg2_url = host(vo2)

man = json.load(open(f"{FIX}/keys_manifest.json"))
MOTION = {
 "BR3_explore": ("5", "Bentley the red-fawn Boxer puppy explores the tide-pool: she sniffs along the glassy rock pool, paws "
   "stepping carefully over wet rock, then lifts her head and her ears perk as she hears something far off, turning toward it, "
   "curious and alert. Natural lively puppy motion, short docked tail. Living water ripples in the pool. Smooth locked camera, "
   "no jitter, everything alive."),
 "a3_02a_wave": ("10", "The big ocean wave CRASHES and CHURNS dramatically over the rocks — white foam surging up and falling, "
   "sea-spray flying through the air, the water alive and constantly moving, the wave NEVER frozen, powerful and continuous. "
   "Tiny Pip the hermit crab scrambles backward in alarm on the foreground rock. Strong continuous violent water motion "
   "throughout the whole clip. Smooth locked camera, no jitter."),
 "octopus": ("10", "A purple octopus tentacle rises up out of the tide-pool, curls and gives a playful little WAVE, then "
   "SPLASHES back down into the water — a big dramatic splash, water droplets and spray flying up catching the golden sunset "
   "light, ripples spreading across the pool. Lively, magical, exciting. Smooth locked camera, no jitter, water fully alive."),
}
PIPCU_PROMPT = ("Pip the little hermit crab panics and pleads, claws gesturing near his face in alarm, big frightened soulful "
   "eyes, small natural crab mouth moving in time with his frightened words, body trembling slightly. Warm bright light, no human teeth.")

def do_motion(sid):
    dur, prompt = MOTION[sid]
    r = run("kling-2.6/image-to-video", {"prompt": prompt, "image_urls":[man[sid]["cat_url"]], "sound": False, "duration": dur}, timeout=900)
    raw = f"{FIX}/{sid}_clip.mp4"; download(r["urls"][0], raw)
    return {"sid": sid, "credits": r["credits"], "secs": r["secs"], "raw": raw, "dur": round(vdur(raw),2)}
def do_avatar():
    r = run("kling/ai-avatar-standard", {"image_url": man["a3_02b_pipcu"]["cat_url"], "audio_url": seg2_url, "prompt": PIPCU_PROMPT}, timeout=900)
    raw = f"{FIX}/a3_02b_pipcu_clip.mp4"; download(r["urls"][0], raw)
    return {"sid": "a3_02b_pipcu", "credits": r["credits"], "secs": r["secs"], "raw": raw, "dur": round(vdur(raw),2)}

results = {}
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:
    futs = {ex.submit(do_motion, s): s for s in MOTION}
    futs[ex.submit(do_avatar)] = "a3_02b_pipcu"
    for f in concurrent.futures.as_completed(futs):
        try:
            d = f.result(); results[d["sid"]] = d
            print(f"DONE {d['sid']}: {d['credits']}cr {d['secs']}s  dur={d['dur']}s")
        except Exception as e:
            print(f"FAIL {futs[f]}: {type(e).__name__}: {e}")
json.dump(results, open(f"{FIX}/videos_result.json","w"), indent=1)
print("total video credits:", sum(d["credits"] for d in results.values()))
