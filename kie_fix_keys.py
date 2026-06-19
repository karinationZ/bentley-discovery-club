#!/usr/bin/env python3
"""Round-2 fixes PHASE 1 — keyframes for BR3 (on-model), a3_02a (live wave), a3_02b (dry Pip CU).
Octopus keyframe extracted from the existing clip (keeps design). Host all on catbox + manifest. QA before videos."""
from kie_client import run, credits, download
import subprocess, json, os
os.makedirs("tests/kie/fix", exist_ok=True)
ROOT = "/home/user/src/youtube/assets/pilot_shots/hybrid_ep1"
BENT = "https://v3b.fal.media/files/b/0a9eb213/K0YEhgC0hRPAknNVA_bSO_Bentley_MASTER_clean_16x9.png"
PIP  = "https://d8j0ntlcm91z4.cloudfront.net/user_3F9AzDc10VXM2MT0k5hLwTCbjQr/hf_20260616_223627_2eb7befd-9545-47ad-9d34-d1f13e108bfa.png"

def host(p):
    u = subprocess.check_output(["curl","-s","-F","reqtype=fileupload","-F",f"fileToUpload=@{p}",
                                 "https://catbox.moe/user/api.php"]).decode().strip()
    if not u.startswith("http"): raise RuntimeError("catbox fail: "+u[:80])
    return u

KF = {
 "BR3_explore": (BENT,
   "Wide shot of Bentley the red-fawn Boxer puppy exploring a Crystal Cove tide-pool at bright golden morning — mid-stride, "
   "nose down curiously sniffing a glassy rock pool, alert and delighted, discovering. CRITICAL: SHORT DOCKED STUBBY tail "
   "(a tiny stub — absolutely NOT a long tail, NOT a raised curved tail, NOT a whip tail), sturdy compact Boxer puppy build "
   "with a broad Boxer head and muzzle. On-model: black mask, grey chin, small white chest blaze, solid red-fawn legs and "
   "paws (NO white socks), BOTH ears soft floppy folded DOWN, soulful well-proportioned eyes (NOT googly), teal collar with "
   "glowing spiral seashell charm. Wet black volcanic rocks and glassy pools, BRIGHT luminous golden daylight, vibrant and "
   "colorful, NOT dim, NOT washed out. Premium dimensional Pixar/Bluey cartoon. Same dog, match exactly."),
 "a3_02a_wave": (PIP,
   "Dramatic WIDE shot at a Crystal Cove tide-pool at golden hour: a BIG ocean wave of white surf rears up and crashes over "
   "the wet black volcanic rocks, foam and spray exploding into the air — and tiny Pip the hermit crab, SMALL in the frame, "
   "scrambles backward in alarm on a foreground rock, away from the towering water. The huge alive wave dominates the frame, "
   "powerful and dramatic. Canonical Pip: reddish-orange body, big soulful eyes set IN his face (NO eye-stalks), dull cracked "
   "brown SPIRAL shell (NOT white, NOT a nautilus), clean face, NO antennae, small natural crab mouth (NO human teeth), smooth "
   "shell. Rich vibrant golden light, colorful, NOT washed out. Premium 3D Pixar style."),
 "a3_02b_pipcu": (PIP,
   "CLOSE-UP of Pip the hermit crab on a DRY wet-black rock, panicking and pleading — little claws raised near his face in "
   "alarm, big soulful frightened eyes, mouth slightly parted mid-plea. Background is ONLY the tide-pool rocks and soft warm "
   "bokeh — NO big wave, NO dominant water behind him (at most a faint distant hint of spray). Canonical Pip: reddish-orange "
   "body, big soulful eyes set IN his face (NO eye-stalks), dull cracked brown SPIRAL shell (NOT white nautilus), clean face, "
   "NO antennae, small natural crab mouth (NO human teeth), smooth shell. Bright warm golden light, vibrant, colorful, NOT "
   "dark. Premium 3D Pixar style."),
}
man = {}
print("bal before:", credits())
for sid, (ref, prompt) in KF.items():
    r = run("google/nano-banana-edit", {"prompt": prompt, "image_urls":[ref], "image_size":"16:9", "output_format":"png"})
    lp = f"tests/kie/fix/{sid}_key.png"; download(r["urls"][0], lp)
    man[sid] = {"local": lp, "cat_url": host(lp), "key_credits": r["credits"]}
    print(f"{sid}: {r['credits']}cr {r['secs']}s")
# octopus keyframe — extract from existing clip (keeps the octopus design consistent)
oct_src = f"{ROOT}/acts456/a6_01_octopus.mp4"; oct_kf = "tests/kie/fix/octopus_key.png"
subprocess.run(["ffmpeg","-y","-loglevel","error","-ss","1.2","-i",oct_src,"-frames:v","1",oct_kf], check=True)
man["octopus"] = {"local": oct_kf, "cat_url": host(oct_kf)}
print("octopus: extracted + hosted")
json.dump(man, open("tests/kie/fix/keys_manifest.json","w"), indent=1)
print("bal after:", credits())
