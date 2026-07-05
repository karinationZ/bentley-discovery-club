"""Hybrid sync step: photoreal rig keyframe + our locked-voice audio -> Kling-Avatar synced clip.
The keyframe is a perfect bright front-facing single-character face-CU (the winning Avatar condition)."""
import sys
from bentley.shared.hosting import kie_host
from bentley.shared.kie_client import run, download

img, aud, out = sys.argv[1], sys.argv[2], sys.argv[3]
PROMPT = (
    "A red-fawn Boxer puppy with a black face mask speaks warmly and gently to a small friend. "
    "Soft happy expression, natural subtle mouth movements, tongue visible but NO human teeth. "
    "Keep her exact appearance, floppy folded ears, teal collar and round gold paw-print tag, "
    "and the golden-hour desert background. Calm cinematic close-up, minimal head movement."
)
iu = kie_host(img)
au = kie_host(aud)
print("hosted image + audio")
r = run("kling/ai-avatar-standard", {"image_url": iu, "audio_url": au, "prompt": PROMPT}, timeout=900, poll=10)
print(f"credits={r['credits']} secs={r['secs']} tid={r['tid']}")
download(r["urls"][0], out)
print("saved:", out)
