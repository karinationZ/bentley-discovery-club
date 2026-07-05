import sys
from bentley.shared.hosting import kie_host
from bentley.shared.kie_client import run, download
key, master, out = sys.argv[1], sys.argv[2], sys.argv[3]
PROMPT=("Using the SECOND image (the canonical character reference) as the exact identity, repaint the FIRST image "
        "so the dog is that SAME charming Boxer puppy — same big round warm dark-brown eyes, same sweet face shape and "
        "proportions, same black mask and markings, same teal collar and gold paw-shaped 'Bentley' name tag. "
        "Keep the FIRST image's head pose, open/closed mouth, and camera framing. High-end animated-film look, "
        "golden-hour desert background, shallow depth of field. No human teeth.")
INP={"prompt":PROMPT, "image_input":[kie_host(key), kie_host(master)], "aspect_ratio":"1:1",
     "resolution":"2K", "output_format":"png"}
r=run("nano-banana-pro", INP)
print(f"nano-banana-pro: {r['credits']}cr {r['secs']}s")
download(r["urls"][0], out); print("saved", out)
