"""Rig-as-control restyle test: take a rig frame (perfect pose/mouth) -> nano-banana-edit ->
photoreal Bentley that PRESERVES the pose+mouth. Proves the hybrid before we spend on a whole clip."""
import sys
from bentley.shared.hosting import kie_host
from bentley.shared.kie_client import run, download

frame, out = sys.argv[1], sys.argv[2]
anchor = sys.argv[3] if len(sys.argv) > 3 else None
PROMPT = (
    "Make this cartoon dog a photorealistic CGI Boxer puppy, high-end animated-film quality. "
    "KEEP THE EXACT SAME pose, head angle, framing and mouth position — do NOT close, move, or reshape the mouth or tongue. "
    "Add realistic short fur with fine individual hairs, a wet glossy black nose, soft subsurface skin. "
    "EYES: large, deep DARK-BROWN almost-black eyes with a single bright catchlight and a soulful, warm, intelligent "
    "gaze looking directly into the camera lens — expressive and full of feeling, like she is looking into your soul. "
    "Preserve exactly: her red-fawn coat, black face mask, grey chin, floppy folded-down ears, white chest blaze, "
    "teal collar with a round gold paw-print tag. Keep the golden-hour desert background with shallow depth of field. "
    "Photorealistic, cinematic, sharp fur detail. No human features, no human teeth."
)
url = kie_host(frame)
imgs = [url]
prompt = PROMPT
if anchor:
    imgs.append(kie_host(anchor))
    prompt = ("Match the dog's EXACT identity — face shape, proportions, fur color and markings, and especially "
              "the dark near-black soulful eyes — to the SECOND reference image. ") + PROMPT
print("hosted:", url[:70], "anchor:" , bool(anchor))
r = run("google/nano-banana-edit", {"prompt": prompt, "image_urls": imgs})
print(f"credits={r['credits']} secs={r['secs']} tid={r['tid']}")
download(r["urls"][0], out)
print("saved:", out)
