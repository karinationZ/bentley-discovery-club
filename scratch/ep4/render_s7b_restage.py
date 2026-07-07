#!/usr/bin/env python3
"""s7b RESTAGE — REJECTED / DO NOT RERUN without a new owner-approved direction.

  START (image_urls[0]) = approved c1  — alert Boxer, head lifting.
  END   (image_urls[1]) = endc1_c1     — delighted tongue-out pop; PINS the last frame on-model.

Historical result: this pinned render was run once and failed adversarial QC (mid-clip face/mask melt,
bug-eyes, tail drift). The generated Ken-Burns fallback was then owner-rejected as static zoom-only, which
violates episode-production's no-static-animation rule. s7b is reopened at Gate 5; the next attempt must be
a new real-motion restage/coverage decision, not this same contained close reaction and not static Ken-Burns.
"""
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
os.environ["BENTLEY_EPISODE"] = "ep4"          # spend gate: ep4 Animatic Lock recorded PASSED
from bentley.shared.render import render_shot

START = "scratch/ep4/kf_s7b_restage/s7b_start_c1.png"
END   = "scratch/ep4/kf_s7b_restage/s7b_endc1_c1.png"
OUT   = "scratch/ep4/renders_w1/s7b_restage.mp4"

# Frame-faithful + motion-only. The two pinned frames own the STYLE and IDENTITY; the prompt only
# describes the small contained motion between them, and re-hammers the canon anchors as guardrails.
PROMPT = (
    "Animate BETWEEN the two reference frames with gentle, contained motion — keep Bentley's character "
    "design, face, fur, colors, and the render style EXACTLY as in the reference frames. Bentley the "
    "red-fawn Boxer puppy stands planted and centered on the coastal wildflower path; she lifts her head "
    "to look up and her eyes widen with delighted, mind-blown wonder, then gives a small happy pop on the "
    "spot (front paws barely leave the ground), tongue out in a joyful dog pant, short docked tail-stub "
    "wagging. A monarch butterfly loops gently in the air near her head. NO leaping away, NO spinning, NO "
    "running, NO travel across the frame. SOLID BLACK face mask, natural warm brown puppy eyes (not "
    "enlarged, not googly), NO human teeth, short DOCKED tail stub with no white tip, paws the same "
    "red-fawn as her coat. Camera is LOCKED and still — no push-in, no zoom, no pan, no shake. 16:9.")


def main():
    if os.environ.get("BENTLEY_ALLOW_REJECTED_S7B_RESTAGE") != "1":
        raise SystemExit(
            "s7b_restage is rejected and must not be rerun. See episodes/ep4/GATES.md Gate 5. "
            "Set BENTLEY_ALLOW_REJECTED_S7B_RESTAGE=1 only after a new owner-approved direction."
        )
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    r = render_shot(PROMPT, first_frame=START, last_frame=END, out=OUT, duration="5")
    print(f"s7b_restage {r['credits']}cr -> {r['out']}", flush=True)
    print("DONE", flush=True)


if __name__ == "__main__":
    main()
