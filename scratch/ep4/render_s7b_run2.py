#!/usr/bin/env python3
"""s7b RUN v2 render — ¾-FRONT toward-camera joyful run (RESTAGE to root-fix the chronic tail/gait/eyes).
Keyframe = owner-direction-approved run, ¾-front pick s7b_run2_c0 (body occludes the tail; soft warm eyes
locked in). Proven s8_run recipe: first-frame-only + pin_override (a run is big motion), @Bentley element,
camera tracks to keep her a CONSTANT size. Prompt: graceful slow lope (fewer footfalls = clean legs), tail
stays hidden behind the body, soft eyes, no leaping. Model LOCKED = kling-3.0/video via render_shot."""
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
os.environ["BENTLEY_EPISODE"] = "ep4"
from bentley.shared.render import render_shot

KEY = "scratch/ep4/kf_s7b_run2/s7b_run2_c0.png"
OUT = "scratch/ep4/renders_w1/s7b_run2.mp4"

PROMPT = (
    "SLOW MOTION: Bentley the red-fawn Boxer puppy runs happily TOWARD the camera in a graceful, floating "
    "bounding lope down the coastal meadow path — long smooth strides, her floppy ears flying UP and back "
    "in the wind, mouth open in a happy tongue-out pant. A river of orange monarch butterflies streams "
    "across the golden sky behind her. The camera moves WITH her, keeping her the SAME size and centered "
    "the whole shot — she never grows, never shrinks, never leaves the ground, never spins. Her body faces "
    "the camera so her REAR AND TAIL STAY HIDDEN behind her; she is a docked Boxer with only a tiny stub. "
    "Exactly FOUR clean distinct legs, each paw fully toed (no fused, extra, or stump legs). Soft, warm, "
    "dark-brown eyes with a gentle happy gaze — NOT wide, NOT startled, NO white around the iris. SOLID "
    "BLACK face mask, NO human teeth, paws the same red-fawn as her coat. Smooth, graceful, ears-in-the-wind. 16:9.")


def main():
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    r = render_shot(PROMPT, first_frame=KEY, out=OUT, duration="5",
                    pin_override="big-motion slow-mo toward-camera lope; a last-frame pin would warp the gait (proven s8_run recipe)")
    print(f"s7b_run2 {r['credits']}cr -> {r['out']}", flush=True)
    print("DONE", flush=True)


if __name__ == "__main__":
    main()
