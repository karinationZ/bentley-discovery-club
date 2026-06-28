#!/usr/bin/env python3
"""Print the raw KIE createTask response for the WAN model to see the real rejection message."""
import os, json, urllib.request
KEY = os.environ["KIE_KEY"]
URL = "https://api.kie.ai/api/v1/jobs/createTask"
def post(body):
    req = urllib.request.Request(URL, data=json.dumps(body).encode(),
        headers={"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"})
    try:
        return json.load(urllib.request.urlopen(req))
    except urllib.error.HTTPError as e:
        return {"HTTPError": e.code, "body": e.read().decode()[:500]}

img = "https://files.catbox.moe/6xzwy3.png"
aud = "https://files.catbox.moe/40jtqd.mp3"
full = {"prompt": "octopus speaking softly, toothless", "image_url": img, "audio_url": aud,
        "negative_prompt": "human teeth", "resolution": "580p", "num_frames": 84,
        "frames_per_second": 16, "num_inference_steps": 27, "guidance_scale": 3.5}
minimal = {"prompt": "octopus speaking softly, toothless", "image_url": img, "audio_url": aud}

print("=== FULL INPUT ===")
print(json.dumps(post({"model": "wan/2-2-a14b-speech-to-video-turbo", "input": full}), indent=2)[:900])
print("\n=== MINIMAL INPUT (3 required only) ===")
print(json.dumps(post({"model": "wan/2-2-a14b-speech-to-video-turbo", "input": minimal}), indent=2)[:900])
