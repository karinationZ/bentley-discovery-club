#!/usr/bin/env python3
"""(1) Build the DEFINITIVE Indi master from s14 (the liked look) + UPGRADED ocelli (glowing/dimensional/sharp).
   (2) Two smaller Bentley tag options (coin + paw). Retry logic for KIE flakiness.
Run: KIE_KEY=... python3 scratch/ep2/master_and_tag.py
"""
import sys, os, json, time, subprocess
ROOT = "/project"
sys.path.insert(0, ROOT)
from bentley.shared import kie_client

OUT = f"{ROOT}/scratch/ep2/master"; os.makedirs(OUT, exist_ok=True)
BENT_URL = "https://files.catbox.moe/xqf188.png"

def host(p):
    u = subprocess.check_output(["curl","-s","-F","reqtype=fileupload","-F",f"fileToUpload=@{p}",
                                 "https://catbox.moe/user/api.php"]).decode().strip()
    if not u.startswith("http"): raise RuntimeError("catbox fail")
    return u

S14_URL = host(f"{ROOT}/scratch/ep2/hero/s14_emergence.png")
print("S14_URL:", S14_URL)

JOBS = {
 "INDI_MASTER": ([S14_URL],
   "Keep THIS EXACT octopus (Indi) — same face shape, same SMALL teal lateral eyes, same proportions, same iridescent purple "
   "colour as in the image. Re-present her in a clear three-quarter CHARACTER-DESIGN MASTER view on a simple wet rock with a "
   "soft, plain, slightly blurred tide-pool background, evenly and warmly lit, with BOTH of her false-eye ocelli visible. "
   "UPGRADE ONLY the two ocelli: make them GLOWING, dimensional, sharp-edged iridescent-blue rings with a luminous, mysterious, "
   "intelligent CENTER and real depth — NOT flat blue painted stains; one sits low, just below and in front of each eye. Keep "
   "her small teal eyes (no white sclera, no line), smooth purple head, NO nose, NO eyebrows, tiny lipless mouth, eight small "
   "suckered arms. Premium Pixar/Bluey 3D, clean, sharp, vibrant, NO grain. NEGATIVE: flat ocelli, dull painted stains, big "
   "round eyes, human eyes, white sclera, nose, eyebrows, giant octopus, film grain, watermark."),
 "TAG_coin": ([BENT_URL],
   "Macro close-up of Bentley's teal collar. Replace her charm with a SMALL, COIN-SIZED round gold name tag (small and neat, "
   "about the size of a coin — NOT large), softly glowing, engraved 'Bentley'. Keep the same dog, red-fawn fur, teal collar. "
   "Clean, sharp, NO grain. NEGATIVE: huge tag, oversized tag, big charm, bone shape, spiral shell, blank tag, film grain."),
 "TAG_paw": ([BENT_URL],
   "Macro close-up of Bentley's teal collar. Replace her charm with a SMALL gold PAW-PRINT-shaped name tag (small and neat — "
   "NOT large), softly glowing, with 'Bentley' on it. Keep the same dog, red-fawn fur, teal collar. Clean, sharp, NO grain. "
   "NEGATIVE: huge tag, oversized tag, big charm, bone shape, spiral shell, blank tag, film grain."),
}

def run_retry(refs, prompt, tries=5):
    for i in range(tries):
        try:
            return kie_client.run("google/nano-banana-edit",
                                  {"prompt": prompt, "image_urls": refs, "image_size": "16:9", "output_format": "png"})
        except Exception as e:
            print(f"   attempt {i+1}: {str(e)[:70]}"); time.sleep(6)
    return None

print("bal before:", kie_client.credits())
for sid,(refs,prompt) in JOBS.items():
    r = run_retry(refs, prompt)
    if r:
        lp = f"{OUT}/{sid}.png"; kie_client.download(r["urls"][0], lp)
        print(f"{sid}: {r['credits']}cr {r['secs']}s -> {lp}")
    else:
        print(f"{sid}: FAILED")
print("bal after:", kie_client.credits())
