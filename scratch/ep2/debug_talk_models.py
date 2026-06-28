#!/usr/bin/env python3
"""Which talking models actually BILL on our KIE account? Print createTask responses."""
import os, json, urllib.request
KEY = os.environ["KIE_KEY"]
URL = "https://api.kie.ai/api/v1/jobs/createTask"
def post(model, inp):
    body = {"model": model, "input": inp}
    req = urllib.request.Request(URL, data=json.dumps(body).encode(),
        headers={"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"})
    try:
        return json.load(urllib.request.urlopen(req))
    except urllib.error.HTTPError as e:
        return {"HTTPError": e.code, "body": e.read().decode()[:400]}

img = "https://files.catbox.moe/6xzwy3.png"
aud = "https://files.catbox.moe/40jtqd.mp3"

tests = [
  ("wan/2-2-a14b-speech-to-video-turbo", {"prompt":"octopus speaking, toothless","image_url":img,"audio_url":aud}),
  ("infinitalk/from-audio", {"prompt":"octopus speaking, toothless","image_url":img,"audio_url":aud,"resolution":"480p"}),
  ("volcengine/video-to-video-lip-sync", {"video_url":"https://files.catbox.moe/6xzwy3.png","audio_url":aud,"mode":"lite"}),
  ("google/nano-banana-edit", {"prompt":"tiny change, keep identical","image_urls":[img],"output_format":"png"}),  # billing sanity (~4cr)
]
for model, inp in tests:
    print(f"=== {model} ===")
    print(json.dumps(post(model, inp))[:300]); print()
