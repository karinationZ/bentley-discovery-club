"""Batch restyle a folder of rig frames -> photoreal, to test temporal consistency of the hybrid.
Independent per-frame nano-banana-edit (baseline flicker test). Optional identity anchor ref."""
import sys
from pathlib import Path
from bentley.shared.hosting import kie_host
from bentley.shared.kie_client import run, download

indir, outdir = Path(sys.argv[1]), Path(sys.argv[2])
anchor = sys.argv[3] if len(sys.argv) > 3 else None
outdir.mkdir(parents=True, exist_ok=True)
PROMPT = (
    "Make this cartoon dog a photorealistic CGI Boxer puppy, high-end animated-film quality. "
    "KEEP THE EXACT SAME pose, head angle, framing and mouth/tongue position — do NOT close, move, or reshape the mouth. "
    "Add realistic short fur with fine individual hairs, a wet glossy black nose, lifelike brown eyes with catchlights, "
    "soft subsurface skin. Preserve exactly: red-fawn coat, black face mask, grey chin, floppy folded-down ears, white chest blaze, "
    "teal collar with round gold paw-print tag, and the golden-hour desert background with shallow depth of field. "
    "Photorealistic, cinematic, sharp fur detail. No human features, no human teeth."
)
anchor_url = kie_host(anchor) if anchor else None
if anchor_url:
    PROMPT = "Match the dog's identity, colors and markings to the SECOND reference image. " + PROMPT

frames = sorted(indir.glob("*.png"))
total_cr = 0
for f in frames:
    out = outdir / f.name
    if out.exists():
        continue
    url = kie_host(str(f))
    imgs = [url, anchor_url] if anchor_url else [url]
    r = run("google/nano-banana-edit", {"prompt": PROMPT, "image_urls": imgs})
    download(r["urls"][0], str(out))
    total_cr += r["credits"] or 0
    print(f"  {f.name}: {r['credits']}cr {r['secs']}s")
print(f"TOTAL {total_cr}cr over {len(frames)} frames")
