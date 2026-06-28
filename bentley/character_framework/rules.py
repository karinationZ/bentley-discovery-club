"""Codified, reusable rules for talking-character animation.

Extracted from the Ep1/Ep2 post-mortems so future episodes inherit them instead of re-deriving:
  - youtube_vault/Lessons Learned.md
  - youtube_vault/Rules/Animation Rules.md
  - docs/rules/MASTER_PROP_RULES.md

Each Rule has a one-line ``summary``, an optional ``prompt_fragment`` that the prompt builder injects,
the ``rationale`` (why), and its ``source``. Import these; do not paraphrase the lessons by hand.
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class Rule:
    name: str
    summary: str
    prompt_fragment: str   # injected into image/video prompts ("" if editorial-only)
    rationale: str
    source: str


ANIMATION = Rule(
    "animation",
    "The world breathes: every outdoor shot needs continuous environmental motion (water ripples/waves, "
    "drifting light). Native speed only — no slow-mo as fake animation. Motion is purposeful. Hold the "
    "character ON-MODEL through the whole clip (check mid-frames, not just frame 0).",
    "with continuous gentle environmental motion and purposeful, natural character motion at native speed",
    "A static frame reads as cheap and breaks the spell; characters drift off-model mid-clip if not held.",
    "Animation Rules.md / Lessons Learned.md",
)

LIP_SYNC = Rule(
    "lip_sync",
    "Talking shots use Kling-Avatar driven by the character's LOCKED VO (mouth matches voice by construction). "
    "Give the Avatar a BRIGHT, near-closed, clean-mouth keyframe so lip-sync opens it naturally. The Avatar "
    "DARKENS output (lift in the grade) and FREEZES the background — when live motion is needed behind a "
    "speaker, SPLIT the beat (an i2v shot for the motion + voice over it, plus a dry talking close-up). It also "
    "intermittently hallucinates on-screen TEXT/captions, worst on SHORT EXCLAMATORY lines; 'no text' in the "
    "prompt reduces but does not kill it — render reaction/exclamation lines as VO over an action shot, not a talking CU.",
    "the mouth moves naturally and minimally, opening only as much as the words require",
    "The Avatar is human-trained: a clean near-closed-mouth keyframe avoids invented teeth; it only animates "
    "the face, so backgrounds freeze (cost 5 failed wave 'fixes' in Ep1).",
    "Animation Rules.md (frozen-background law) / Lessons Learned.md",
)

EYE_CONTACT = Rule(
    "eye_contact",
    "Eyes do the acting — especially for non-human characters. Big, soft, expressive eyes that blink "
    "naturally; gaze anchored on the scene partner, or gently toward camera for a warm beat. Never a dead, "
    "bug-eyed, or mis-proportioned stare.",
    "with big, soft, expressive eyes that blink naturally and stay alive, gaze gently engaged",
    "Creatures that cannot use a human face (octopus, etc.) carry the performance through eyes + body "
    "(the WALL-E / Gromit principle).",
    "Ep2 talking-shot work",
)

EXPRESSION = Rule(
    "expression",
    "Express through species-true body language, not human facial expressions: dog = ears, tail, tongue, "
    "head-tilt; octopus = colour shifts, posture, arm gestures. Choose the beat from EMOTION_TEMPLATES.",
    "",  # the emotion fragment is injected separately by the prompt builder
    "Human expressions on animals read as uncanny; species-true body language is believable and on-brand.",
    "Lessons Learned.md / Ep2",
)

CAMERA = Rule(
    "camera",
    "Talking close-ups use a LOCKED / minimal camera. Choose framing by intent: CU for emotion, MCU for "
    "dialogue, MS for action, WIDE to establish. Vary framing between adjacent shots of the same character.",
    "with a locked, minimal camera",
    "A moving camera fights lip-sync; two near-identical adjacent framings read as a glitch (match-jump).",
    "Animation Rules.md (scene-transition standards)",
)

TRANSITION = Rule(
    "transition",
    "Hard cuts on the action/dialogue rhythm; keep a CONTINUOUS ambient + music bed across the seam. Never "
    "match-cut between two near-identical shots of the same character. Never re-anchor (restart) a music cue "
    "mid-beat — let it ride.",
    "",  # editorial-only (used by the assembly/timeline, not the image prompt)
    "Continuous beds hide the seams; match-jumps and restarted cues read as glitches.",
    "Animation Rules.md (scene-transition standards)",
)

CONSISTENCY = Rule(
    "consistency",
    "ALWAYS derive a shot keyframe FROM the APPROVED MASTER — never from a drifted AI close-up, never from "
    "scratch. Edit the master (nano-banana-pro) so face/muzzle/markings stay locked. QA every render against "
    "the character's MUST-HAVE / MUST-NEVER (mid-frames included); reject to a regenerate-FROM-MASTER, not a "
    "from-scratch reroll. One consistent grade across the whole episode.",
    "keep the EXACT approved character — same face, muzzle, markings, proportions and render; do not redraw or restyle",
    "Ep2 cost: a drifted CU (bentley_cu_ears) produced an off-model, human-teeth Bentley that 'isn't original "
    "Bentley'. The master is the single source of truth.",
    "MASTER_PROP_RULES.md / Lessons Learned.md",
)

ALL = (ANIMATION, LIP_SYNC, EYE_CONTACT, EXPRESSION, CAMERA, TRANSITION, CONSISTENCY)
BY_NAME = {r.name: r for r in ALL}
