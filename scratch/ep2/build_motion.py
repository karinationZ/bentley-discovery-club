#!/usr/bin/env python3
"""Ep2 recovery — Stage 3 (motion): i2v the 12 new keyframes into motion clips. Anatomy-safe (framework bans);
Indi kept face-minimal so no teeth creep in. Output assets/pilot_shots/ep2/motion/. Run: KIE_KEY=... python3 ..."""
import sys, os, time
from concurrent.futures import ThreadPoolExecutor
ROOT = "/project"
sys.path.insert(0, ROOT)
from bentley.shared import kie_client
from bentley.shared.hosting import catbox_host
from bentley.character_framework import BENTLEY, INDI
KF = f"{ROOT}/assets/pilot_shots/ep2/keyframes"
OUT = f"{ROOT}/assets/pilot_shots/ep2/motion"; os.makedirs(OUT, exist_ok=True)
DB, OB = BENTLEY.anatomy.ban(), INDI.anatomy.ban()
COMMON = "Keep the EXACT same character(s), colours, proportions and 3D render as the image. Native speed, locked stable camera, no jitter, no shake. No text, no watermark."

# (id, motion, anatomy-ban)
SHOTS = [
 ("a0_02_boop",   "Bentley takes the last slow step and her lifted front paw gently touches and BOOPS the speckled rock; ears down, mouth closed; shallow water ripples.", DB),
 ("a1_07_chase",  "Bentley pounces playfully; a jet of water squirts up into her face and she flinches back, surprised, mouth closed; water sprays and ripples.", DB),
 ("a1_09_lunge",  "Bentley lunges forward reaching with her paws as the curling purple octopus tentacle whips away out of frame; the little spiral shell sits still; water ripples.", DB + ". " + OB),
 ("a3_15_settle", "Bentley settles, sitting back on her haunches, breathing softly, calm and patient, soft eyes, ears down, mouth closed; gentle water ripples.", DB),
 ("a1_08_camo",   "The octopus skin slowly ripples as it shifts from smooth to bumpy and colour-matches the rock and back again — mesmerizing camouflage; only the skin texture and colour animate; keep her face and mouth still and calm.", OB),
 ("a2_11_bolt",   "Indi jets away in a puff of dark ink, bolting low and fast toward the dark crevice; a sense of speed; keep her face and mouth minimal and calm.", OB),
 ("a4_25_wedged", "Indi wriggles and squeezes, wedged tight in the narrow gap, her teal eyespots pulsing brighter with worry; the soft dark shadow looms behind; keep her mouth small and closed.", OB),
 ("a4_29_reform", "Indi's body settles and relaxes, reformed and safe on the rock, her eyespots softening, gentle breathing, calm; keep her mouth small and soft.", OB),
 ("a2_10_corner", "Bentley leans in slightly closer; Indi presses back small, her teal eyespots flaring brighter; tense and held; keep BOTH mouths closed and natural, no teeth.", DB + ". " + OB),
 ("a4_26_yank",   "Bentley gently tugs at the wedged tentacle, worried and careful; Indi resists, eyespots flaring; tension; keep BOTH mouths closed and natural, no teeth.", DB + ". " + OB),
 ("a2_12_eelstir","The dark eel shifts and curls slowly in the dim crevice, a few bubbles rising; quiet and gentle; the water moves softly.", "No scary teeth"),
 ("a6_34_ants",   "The neat line of cartoon ants marches steadily inland across the sand carrying the giant crumb, the crumb swaying slightly; warm heat-shimmer; gentle.", "No text"),
]

def run(s):
    sid, motion, ban = s
    url = catbox_host(f"{KF}/{sid}.png")
    prompt = f"{motion} {ban}. {COMMON}"
    outp = f"{OUT}/{sid}.mp4"
    for i in range(8):
        try:
            r = kie_client.run("kling-2.6/image-to-video", {"prompt": prompt, "image_urls": [url], "sound": False, "duration": "5"}, timeout=600)
            kie_client.download(r["urls"][0], outp); return (sid, r.get("credits"))
        except Exception as e:
            print(f"  {sid} try {i+1}: {str(e)[:60]}", flush=True); time.sleep(12)
    return (sid, None)

print("bal before:", kie_client.credits(), flush=True)
with ThreadPoolExecutor(max_workers=4) as ex:
    for sid, c in ex.map(run, SHOTS):
        print(f"  {sid}: {c}cr" + ("" if c else "  <-- FAILED"), flush=True)
print("bal after:", kie_client.credits(), flush=True)
print("=== MOTION DONE ===", flush=True)
