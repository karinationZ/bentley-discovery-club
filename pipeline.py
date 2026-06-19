#!/usr/bin/env python3
"""Bentley's Discovery Club — production pipeline on the new stack.
Stages per shot: keyframe (Nano-Banana, fal) -> video (Kling 2.5) OR talking (Kling Avatar v2)
                 + voice (ElevenLabs LauraZ v3, cleaned). All locked-design rules baked in.
Resumable: skips a shot whose .mp4 already exists. Per-shot error isolation.
Usage: .venv/bin/python pipeline.py <shotlist.json>
"""
import os, sys, json, subprocess, urllib.request, traceback, fal_client, concurrent.futures

def fsub(model, arguments=None, timeout=420):
    """fal_client.subscribe with a HARD timeout — a balance-lock/queue hang must never silently
    eat hours again (a single Kling render is minutes, not hours)."""
    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as ex:
        try:
            return ex.submit(fal_client.subscribe, model, arguments=arguments).result(timeout=timeout)
        except concurrent.futures.TimeoutError:
            raise RuntimeError(f"FAL_TIMEOUT after {timeout}s on {model} (likely exhausted balance or queue hang)")

ROOT = os.path.dirname(os.path.abspath(__file__))
ELEVEN_KEY = os.environ["ELEVENLABS_API_KEY"]
BENTLEY_VOICE = "jkNABRZGatAuwawcS9xX"
PIP_VOICE     = "N2lVS1w4EtoT3dr4eOWO"  # Callum (husky trickster), pitched +10% -> small fussy crab

M_T2I    = "fal-ai/nano-banana"
M_EDIT   = "fal-ai/nano-banana/edit"
M_VIDEO  = "fal-ai/kling-video/v2.5-turbo/pro/image-to-video"
M_AVATAR = "fal-ai/kling-video/ai-avatar/v2/standard"

REFS = {
  "bentley": "https://v3b.fal.media/files/b/0a9eb213/K0YEhgC0hRPAknNVA_bSO_Bentley_MASTER_clean_16x9.png",  # APPROVED clean master (paws fixed, 16:9, ears down, short tail)
  "pip":     "https://d8j0ntlcm91z4.cloudfront.net/user_3F9AzDc10VXM2MT0k5hLwTCbjQr/hf_20260616_223627_2eb7befd-9545-47ad-9d34-d1f13e108bfa.png",
}
ENV = (" Setting: the same Crystal Cove tide pool — wet black volcanic rocks and glassy pools at golden dawn, "
       "NOT a sandy beach. Consistent premium 3D dimensional Pixar soft-fur style, matching warm lighting and color across every shot, NOT painterly, NOT flat.")

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

def tts_pip(text, outp):
    body = json.dumps({"text":text,"model_id":"eleven_v3",
        "voice_settings":{"stability":0.35,"similarity_boost":0.75,"style":0.65,"speed":1.05}}).encode()
    req = urllib.request.Request(
        f"https://api.elevenlabs.io/v1/text-to-speech/{PIP_VOICE}?output_format=mp3_44100_192",
        data=body, headers={"xi-api-key":ELEVEN_KEY,"Content-Type":"application/json","Accept":"audio/mpeg"})
    raw = outp.replace(".mp3","_raw.mp3")
    with urllib.request.urlopen(req) as r, open(raw,"wb") as f: f.write(r.read())
    a = round(1/1.10, 4)  # pitch +10% (asetrate up, atempo back) -> small crab
    subprocess.run(["ffmpeg","-y","-loglevel","error","-i",raw,"-af",
      f"asetrate={int(44100*1.10)},aresample=44100,atempo={a},highpass=f=110,equalizer=f=300:t=q:w=1:g=-1,loudnorm=I=-16:TP=-1.5:LRA=11",
      "-b:a","192k",outp], check=True)
    return outp

def keyframe(prompt, ref_key=None):
    p = prompt + ENV
    if ref_key:
        res = fsub(M_EDIT, arguments={"prompt":p,"image_urls":[REFS[ref_key]],"aspect_ratio":"16:9"})
    else:
        res = fsub(M_T2I, arguments={"prompt":p,"aspect_ratio":"16:9"})
    return res["images"][0]["url"]

def paw_fix(image_url):
    p = ("Recolor ONLY the dog's paws and lower legs to SOLID rich red-fawn fur exactly matching the body, "
         "completely removing all white and cream from the feet, toes and paws. Keep everything else identical: "
         "same pose, body, both floppy folded-down ears, short tail, teal collar with seashell charm, rocks, water and lighting.")
    res = fsub(M_EDIT, arguments={"prompt":p,"image_urls":[image_url],"aspect_ratio":"16:9"})
    return res["images"][0]["url"]

def video(image_url, prompt, dur="5"):
    p = prompt + (" Keep the consistent 3D dimensional Pixar soft-fur style and warm dawn lighting throughout, NOT painterly. "
                  "Water must actually MOVE — ripples, foam, gentle wave motion; subtle natural character motion (breathing, blinking, small shifts).")
    res = fsub(M_VIDEO, arguments={"prompt":p,"image_url":image_url,"duration":dur,"aspect_ratio":"16:9"})
    return res["video"]["url"]

def avatar(image_url, audio_url):
    res = fsub(M_AVATAR, arguments={"image_url":image_url,"audio_url":audio_url})
    return res["video"]["url"]

def dl(url, path):
    urllib.request.urlretrieve(url, path); return path

def produce(shot, work):
    sid = shot["id"]; out = f"{work}/{sid}.mp4"; kpath = f"{work}/{sid}_key.png"
    if os.path.exists(out): print(f"[skip] {sid}"); return out
    print(f"[run] {sid} ({shot['type']})", flush=True)
    if os.path.exists(kpath):
        kf = fal_client.upload_file(kpath); print("      reuse approved keyframe", flush=True)
    else:
        kf = keyframe(shot["keyframe"], shot.get("ref"))
        if shot.get("ref") == "bentley" and shot["type"] == "motion": kf = paw_fix(kf)  # clean paws only on full-body shots
        dl(kf, kpath); print("      keyframe ok", flush=True)
    if os.environ.get("KEYFRAMES_ONLY"):
        print("      keyframe-only -> skip video", flush=True); return kpath
    if shot["type"] == "motion":
        v = video(kf, shot["motion"], shot.get("dur","5"))
    else:  # talk
        if shot.get("voice") == "bentley":
            a = tts_bentley(shot["line"], f"{work}/{sid}_vo.mp3")
        elif shot.get("voice") == "pip":
            a = tts_pip(shot["line"], f"{work}/{sid}_vo.mp3")
        else:
            a = os.path.join(ROOT, shot["audio_file"])
        au = fal_client.upload_file(a)
        print(f"      audio uploaded", flush=True)
        v = avatar(kf, au)
    dl(v, out)
    print(f"      DONE -> {sid}.mp4", flush=True)
    return out

if __name__ == "__main__":
    spec = json.load(open(sys.argv[1]))
    work = os.path.join(ROOT, spec["work"]); os.makedirs(work, exist_ok=True)
    print(f"=== producing {len(spec['shots'])} shots -> {work} ===", flush=True)
    for s in spec["shots"]:
        try: produce(s, work)
        except Exception as e:
            msg = str(e)
            if "Exhausted balance" in msg or "User is locked" in msg or "FAL_TIMEOUT" in msg:
                print("\n!!! FAL BALANCE EXHAUSTED — top up at fal.ai/dashboard/billing, then re-run (resumable; finished shots are skipped). Stopping now.\n", flush=True)
                sys.exit(2)
            print(f"      ERROR {s['id']}: {e}", flush=True); traceback.print_exc()
    print("=== pipeline run complete ===", flush=True)
