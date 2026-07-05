#!/usr/bin/env python3
"""EP4 CHEAPER-KEYFRAME smoke test (owner-approved 2026-07-05): build a hero keyframe by EDITING the
LOCKED Meadow plate to drop in on-model Bentley + Mira via google/nano-banana-edit (~4cr/candidate)
instead of nano-banana-pro from scratch (~18cr). If it holds on paw-zoom QC, the 13-keyframe batch
drops ~800cr -> ~250cr. Test shot = s3a_meet_comeon (Bentley bounces to follow, Mira looping ahead):
a two-shot, so it tests BOTH characters + the #1 paw-drift risk. Image model = ungated (pre-animatic)."""
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from bentley.shared import kie_client, hosting

CD = "assets/character_design"
PLATE = f"{CD}/Meadow_plate.png"
BODY  = f"{CD}/Bentley_MASTER_pixar.png"
TURN  = f"{CD}/Bentley_MODEL_SHEET_turnaround.png"
MIRA  = f"{CD}/Mira_LOCKED.png"
OUT   = os.path.join(os.path.dirname(__file__), "kf_smoke")
os.makedirs(OUT, exist_ok=True)

# Proven recipe (playbook §3.2): master-fidelity lead + EMPHATIC coat-bound paw block.
PROMPT = (
    "Edit this coastal wildflower-meadow scene (image 1) to add two characters, keeping the meadow, "
    "ocean, dawn light and painterly cartoon style EXACTLY as they are. "
    "Add BENTLEY — the red-fawn Boxer puppy from the reference master (images 2-3) — mid-bounce on the "
    "dirt path, ears flopping, looking up eagerly and about to follow. Keep Bentley EXACTLY identical to "
    "the reference master: same face, black mask, grey chin, brown eyes, floppy folded ears, white chest "
    "blaze, short docked tail stub, teal collar with the gold paw-print tag; refined proportions and the "
    "same cartoony-Pixar render — do NOT make her more cartoonish or enlarge her eyes. "
    "CRITICAL: her paws, feet and lower legs are SOLID RED-FAWN, the exact same color as her coat — NO "
    "white paws, NO white socks, NO white toes. "
    "Also add MIRA — the monarch butterfly from image 4 — looping playfully in the air just ahead of "
    "Bentley, wings open, EXACTLY matching her locked design. Natural scale, both characters grounded in "
    "the scene's light. 16:9."
)

def main():
    print("hosting refs...", flush=True)
    urls = [hosting.catbox_host(p) for p in (PLATE, BODY, TURN, MIRA)]
    for p, u in zip((PLATE, BODY, TURN, MIRA), urls):
        print(f"  {os.path.basename(p)} -> {u}", flush=True)
    inp = {"prompt": PROMPT, "image_urls": urls, "image_size": "16:9", "output_format": "png"}
    for i in range(3):
        print(f"candidate {i} (google/nano-banana-edit)...", flush=True)
        try:
            r = kie_client.run("google/nano-banana-edit", inp, timeout=300, poll=5)
            out = f"{OUT}/s3a_edit_c{i}.png"
            kie_client.download(r["urls"][0], out)
            print(f"  c{i}: {r['credits']}cr {r['secs']}s -> {out}", flush=True)
        except Exception as e:
            print(f"  c{i} FAILED: {e}", flush=True)
    print("DONE", flush=True)

if __name__ == "__main__":
    main()
