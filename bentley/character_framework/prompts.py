"""Prompt library + builder for the Talking Character framework.

``talking_prompt(character, emotion, camera)`` assembles a Kling-Avatar prompt from the character's
anatomy profile + consistency rule + an emotion template + a camera template, automatically applying
the codified rules (eye-contact, no-text, style) so NO episode rewrites them. Add a character or an
emotion and every shot inherits the discipline. ``motion_prompt`` does the same for silent i2v shots.

Reused templates live here (EMOTION_TEMPLATES, CAMERA_TEMPLATES, TRANSITION_TEMPLATES); episode code
just picks a key.
"""
from bentley.character_framework import rules

# --- Emotion templates (performance beat) -----------------------------------------------------
EMOTION_TEMPLATES = {
    "calm":      "calm and gentle",
    "shy":       "warm but shy — a little guarded, yet hopeful",
    "delighted": "bright and delighted, eyes shining",
    "playful":   "giddy and playful",
    "awe":       "wide-eyed with wonder",
    "worried":   "quiet and worried",
    "tender":    "soft and tender",
    "urgent":    "alarmed and urgent",
    "proud":     "proud and pleased with itself",
    "stunned":   "stunned and wide-eyed",
}

# --- Camera templates (framing) ---------------------------------------------------------------
CAMERA_TEMPLATES = {
    "cu":   "framed as a close-up on the face",
    "mcu":  "framed as a medium close-up of the head and chest, facing the camera",
    "ms":   "framed as a medium shot",
    "wide": "framed as a wide establishing shot",
    "ots":  "framed as an over-the-shoulder two-shot",
}

# --- Transition templates (EDITORIAL — for the assembler/timeline, not the image prompt) ------
TRANSITION_TEMPLATES = {
    "hard_cut":         "Hard cut on the dialogue/action beat; keep ambient + music continuous across the seam.",
    "avoid_match_jump": "Do not cut to a near-identical framing of the same character — vary pose/angle.",
    "hold_music":       "Let the music cue ride across the cut; do not re-anchor (restart) it.",
    "split_the_beat":   "Live background motion + a speaker → split into an i2v motion shot (VO over it) + a dry talking CU.",
}

_GLOBAL_NEGATIVES = "No text, no watermark, no captions."
_STYLE = "Bright, warm, premium 3D animated kids'-show style."


def _article(word):
    return "An" if word[:1].lower() in "aeiou" else "A"


def talking_prompt(character, emotion=None, camera="mcu", extra=None):
    """Build a Kling-Avatar talking-shot prompt for ``character``.

    Order matters (the core lesson): performance → eyes → POSITIVE anatomy → BAN human anatomy →
    consistency/charm → camera → global negatives → style.
    """
    a = character.anatomy
    emo = EMOTION_TEMPLATES.get(emotion or character.default_emotion, emotion or "calm")
    cam = CAMERA_TEMPLATES.get(camera, camera)
    collar = f" Keep its {character.collar}." if character.collar else ""
    parts = [
        f"{_article(character.descriptor)} {character.descriptor}, {emo}, gently speaking its line.",
        f"It has {rules.EYE_CONTACT.prompt_fragment.split('with ', 1)[-1]}.",
        f"{a.describe()}; {rules.LIP_SYNC.prompt_fragment}.",
        f"{a.ban()}.",
        f"{rules.CONSISTENCY.prompt_fragment.capitalize()}.{collar}",
        f"It is {cam}, {rules.CAMERA.prompt_fragment}.",
        _GLOBAL_NEGATIVES,
        _STYLE,
    ]
    if extra:
        parts.append(extra)
    return " ".join(p.strip() for p in parts if p.strip())


def motion_prompt(character, action, camera="ms", extra=None):
    """Build a SILENT i2v motion prompt (no lip-sync) for ``character`` — anatomy-safe + alive."""
    a = character.anatomy
    cam = CAMERA_TEMPLATES.get(camera, camera)
    parts = [
        f"{_article(character.descriptor)} {character.descriptor}: {action}.",
        f"{a.describe()}.",
        f"{a.ban()}.",
        rules.ANIMATION.summary.split(":", 1)[-1].strip(),
        f"{rules.CONSISTENCY.prompt_fragment.capitalize()}.",
        f"It is {cam}, {rules.CAMERA.prompt_fragment}.",
        _GLOBAL_NEGATIVES, _STYLE,
    ]
    if extra:
        parts.append(extra)
    return " ".join(p.strip() for p in parts if p.strip())
