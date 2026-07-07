#!/usr/bin/env python3
"""s7b WIDE restage — the ONE pinned render (owner signed off the wide keyframe pair 2026-07-06).

  START (image_urls[0]) = s7b_wide_c1_fixed.png  — wide, Bentley small, alert, looking up at Mira.
  END   (image_urls[1]) = s7b_wide_end_c0.png    — same wide framing/scale, mouth opens to a happy
                                                    tongue-out pant, head lifts; PINS the last frame.

Bentley is SMALL in frame → Kling is NOT asked to hold a close Boxer face (the drift trap that failed every
close s7b). START/END are tightly matched (only her mouth/head change) → the pin barely has to move her. The
MOTION the viewer sees is the streaming river of monarchs + Mira looping + Bentley's small tongue-out reaction
— real, alive, not static. Model LOCKED = kling-3.0/video via render_shot (pin #3 + @Bentley element baked in).
Reroll policy: ONE render, ≤2 rerolls, then FLAG — no reroll #3, no further restage (owner law)."""
import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
os.environ["BENTLEY_EPISODE"] = "ep4"          # spend gate: ep4 Animatic Lock recorded PASSED
from bentley.shared.render import render_shot

START = "scratch/ep4/kf_s7b_wide/s7b_wide_c1_fixed.png"
END   = "scratch/ep4/kf_s7b_wide/s7b_wide_end_c0.png"
OUT   = "scratch/ep4/renders_w1/s7b_wide.mp4"

PROMPT = (
    "Animate BETWEEN the two reference frames — keep Bentley's character design, the WIDE framing, her SMALL "
    "size and position in the frame, the coastal meadow, and the render style EXACTLY as in the frames. "
    "Bentley the red-fawn Boxer puppy stands small on the wildflower path and looks UP in delighted wonder; "
    "her mouth opens into a happy tongue-out dog pant (NO teeth, no human grin) and her short docked tail-stub "
    "wags. All around her a RIVER of orange monarch butterflies streams gently across the sky and the monarch "
    "near her loops softly in the air. She stays PLANTED in the same spot — NO running, NO leaping, NO spinning, "
    "NO travel across the frame, NO big body movement. SOLID BLACK face mask, natural warm brown puppy eyes "
    "(not enlarged, not googly), paws the same red-fawn as her coat with no white socks, short docked tail stub "
    "with no white tip. Camera is LOCKED and still — no push-in, no zoom, no pan, no shake. 16:9.")


def main():
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    r = render_shot(PROMPT, first_frame=START, last_frame=END, out=OUT, duration="5")
    print(f"s7b_wide {r['credits']}cr -> {r['out']}", flush=True)
    print("DONE", flush=True)


if __name__ == "__main__":
    main()
