#!/usr/bin/env python3
"""Keyframe fix #2: eel slimier+blacker; ants clearly INLAND on dry sand (not on the ocean).
Run: KIE_KEY=... python3 scratch/ep2/build_kf_fix2.py"""
import sys, os, time
ROOT = "/project"
sys.path.insert(0, ROOT)
from bentley.shared import kie_client
OUT = f"{ROOT}/assets/pilot_shots/ep2/keyframes"
NOTXT = "No text, no watermark, no captions."
STYLE = "Premium 3D dimensional Pixar soft-fur style, NOT painterly."

SPECS = [
 ("a2_12_eelstir", f"A long sinuous moray eel as a glistening, SLIMY, JET-BLACK silhouette curling out of a shadowy reef "
                   f"crevice — wet slick gleaming black skin with subtle wet highlights, a faint single eye-glint, a quiet "
                   f"lurking-predator menace but gentle enough for ages 4-8. Dim cool underwater light, deep shadow. {NOTXT} {STYLE}"),
 ("a6_34_ants",    f"Cute friendly cartoon ants in a neat line marching across DRY golden BEACH SAND, heading INLAND toward "
                   f"grassy dunes and AWAY from the water, carrying a crumb that is COMICALLY the SIZE OF A CAR; warm "
                   f"sunlight, a sense of wonder. They are on DRY LAND — the ocean is only a thin distant strip far in the "
                   f"background, NOT near or under the ants. {NOTXT} {STYLE}"),
]

print("bal before:", kie_client.credits(), flush=True)
for sid, prompt in SPECS:
    outp = f"{OUT}/{sid}.png"
    for i in range(4):
        try:
            r = kie_client.run("google/nano-banana", {"prompt": prompt, "image_size": "16:9", "output_format": "png"})
            kie_client.download(r["urls"][0], outp); print(f"  {sid}: {r.get('credits')}cr", flush=True); break
        except Exception as e:
            print(f"  {sid} try {i+1}: {str(e)[:60]}", flush=True); time.sleep(6)
print("bal after:", kie_client.credits(), flush=True)
print("=== FIX2 DONE ===", flush=True)
