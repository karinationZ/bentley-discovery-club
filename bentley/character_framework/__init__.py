"""Talking Character framework — shared, reusable character-animation logic for ALL episodes.

Codifies everything we paid to learn in Ep1/Ep2 so future episodes inherit it automatically:
  * characters   — the registry (Bentley, Indi, ...) bound to anatomy + voice + approved master
  * anatomy      — species profiles (describe correct anatomy, THEN ban the human version)
  * rules        — the 7 rule categories (animation, lip_sync, eye_contact, expression, camera,
                   transition, consistency) with sources + injectable prompt fragments
  * prompts      — emotion/camera/transition templates + talking_prompt()/motion_prompt() builders
  * pipeline     — talk(), batch(), derive_keyframe() (KIE Kling-Avatar + nano-banana-pro)

Episode-specific code (which lines, which scene, VO paths) stays in the episode and calls this.

Quick start (an episode):
    from bentley.character_framework import talk, batch, derive_keyframe, BENTLEY, INDI
    talk(BENTLEY, "vo/B_button.mp3", "out/B_button.mp4", emotion="tender")
"""
from bentley.character_framework.anatomy import AnatomyProfile, DOG, CEPHALOPOD, PROFILES
from bentley.character_framework.characters import Character, BENTLEY, INDI, REGISTRY, get
from bentley.character_framework import rules
from bentley.character_framework.prompts import (
    talking_prompt, motion_prompt,
    EMOTION_TEMPLATES, CAMERA_TEMPLATES, TRANSITION_TEMPLATES,
)
from bentley.character_framework.pipeline import talk, batch, derive_keyframe, AVATAR_MODEL, KEYFRAME_MODEL

__all__ = [
    "AnatomyProfile", "DOG", "CEPHALOPOD", "PROFILES",
    "Character", "BENTLEY", "INDI", "REGISTRY", "get",
    "rules",
    "talking_prompt", "motion_prompt", "EMOTION_TEMPLATES", "CAMERA_TEMPLATES", "TRANSITION_TEMPLATES",
    "talk", "batch", "derive_keyframe", "AVATAR_MODEL", "KEYFRAME_MODEL",
]
