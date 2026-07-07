#!/usr/bin/env python3
"""s7b RUN restage render — SLOW-MOTION side-profile GALLOP (owner redirect 2026-07-06: "running Bentley,
slow motion, flying ears"). Matches the PROVEN s8_run recipe (owner-approved): first-frame ONLY (a run is
big motion — a last-frame pin would warp the gait, so pin_override), the @Bentley element, and a camera that
TRACKS BESIDE at a CONSTANT distance so her scale stays locked (the wave-0/framing lesson).

Fixes the two prompt mistakes that drifted the reaction render: (1) NO tail-motion wording ("wags" invented a
long tail) — only "short docked stub"; (2) hard no-human-teeth. Keyframe = owner-picked s7b_run_c3.
Model LOCKED = kling-3.0/video via render_shot. ≤2 rerolls then FLAG."""
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
os.environ["BENTLEY_EPISODE"] = "ep4"
from bentley.shared.render import render_shot

KEY = "scratch/ep4/kf_s7b_run/s7b_run_c3.png"
OUT = "scratch/ep4/renders_w1/s7b_run_r1.mp4"   # reroll #1 (first run had long tail + t4 leg-tangle + googly eyes)

PROMPT = (
    "SLOW MOTION: Bentley the red-fawn Boxer puppy moves in a graceful, floating BOUNDING LOPE in side "
    "profile across the coastal meadow path — long, smooth, extended strides (NOT a frantic gallop), her "
    "floppy ears STREAMING and flapping back in the wind, tongue out in gentle delight. A river of orange "
    "monarch butterflies streams across the golden sky in the same direction, moving WITH her. The camera "
    "TRACKS BESIDE her at a CONSTANT distance — she stays the SAME size and centered the whole shot, never "
    "grows, never flies off, never leaves the ground, never spins. Exactly FOUR legs, clean and distinct at "
    "every stride, each paw fully toed (no fused, extra, or stump legs). She is a DOCKED Boxer with NO tail "
    "— only a tiny rounded coat-colored STUB at her rump; NEVER a long, raised, curling or plume tail. "
    "Soft, warm, dark-brown eyes with a gentle relaxed gaze — NOT wide, NOT startled, NO white showing "
    "around the iris. SOLID BLACK face mask, NO human teeth, paws the same red-fawn as her coat with no "
    "white socks or pale toes. Slow, smooth, ears-in-the-wind motion. 16:9.")


def main():
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    r = render_shot(PROMPT, first_frame=KEY, out=OUT, duration="5",
                    pin_override="big-motion slow-mo gallop; a last-frame pin would warp the running gait (proven s8_run recipe)")
    print(f"s7b_run {r['credits']}cr -> {r['out']}", flush=True)
    print("DONE", flush=True)


if __name__ == "__main__":
    main()
