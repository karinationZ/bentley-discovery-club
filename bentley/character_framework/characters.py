"""Character registry for the Talking Character framework.

Each Character binds a creature to its anatomy profile, its locked voice, its APPROVED MASTER
keyframe (the single source of truth for consistency), and its MUST-HAVE / MUST-NEVER QA table.
Episodes look characters up by key — they never re-describe the character.

Add a new character (e.g. an Ep3 ant) here once; every prompt, pipeline call and QA gate inherits it.
"""
from dataclasses import dataclass, field

from bentley.character_framework.anatomy import AnatomyProfile, DOG, CEPHALOPOD


@dataclass(frozen=True)
class Character:
    key: str
    name: str
    descriptor: str               # noun phrase used in prompts
    anatomy: AnatomyProfile
    voice: str                    # function name in bentley.voices.dialogue
    master_keyframe: str          # path RELATIVE to repo ROOT — the approved master
    collar: str = ""              # collar/charm description (configurable per episode)
    must_have: tuple = ()
    must_never: tuple = ()
    default_emotion: str = "calm"
    notes: str = ""


BENTLEY = Character(
    key="bentley",
    name="Bentley",
    descriptor="young red-fawn Boxer puppy",
    anatomy=DOG,
    voice="tts_bentley",
    master_keyframe="assets/character_design/Bentley_MASTER_pixar.png",
    collar="teal collar with the glowing gold paw-print 'Bentley' tag",
    must_have=("short docked tail", "black face mask", "grey chin", "white chest blaze",
               "paws the same color as her coat (NO white socks)", "floppy ears folded down",
               "soulful well-proportioned eyes", "natural boxer proportions"),
    must_never=("long or upright tail", "different muzzle/face", "white socks", "upright/pricked ears",
                "human teeth or a human grin", "bug-eyes", "fur on the collar/charm"),
    notes=("Catchphrase 'Stop. Look. Listen.' is ALWAYS Bentley's voice, paced with beats. "
           "Ep1 wore a spiral seashell charm; Ep2 swapped to the gold paw tag (owner-approved). "
           "DERIVE talking keyframes FROM the master — never from a drifted CU (that caused the Ep2 off-model Bentley). "
           "MASTER RE-BASELINED (Ep2): the photoreal Bentley_MASTER_hero.jpg is RETIRED to assets/character_design/reference/ "
           "because the AI animation (Kling-Avatar/i2v) only renders cartoony-Pixar and could not reproduce photoreal. "
           "The canonical master is now Bentley_MASTER_pixar.png (cartoony-Pixar, short docked tail), matching the animation + Indi."),
)

INDI = Character(
    key="indi",
    name="Indi",
    descriptor="shy California two-spot octopus",
    anatomy=CEPHALOPOD,
    voice="tts_indi",
    master_keyframe="assets/character_design/Indi_LOCKED.png",
    collar="",
    must_have=("teal eyes", "two teal ocelli (false eyespots)", "iridescent purple skin", "eight suckered tentacles"),
    must_never=("human eyes", "a nose", "eyebrows", "any teeth", "human hands/fingers"),
    default_emotion="shy",
    notes=("Octopus-first: edit FROM Indi_LOCKED, never text-to-image (it drifts to a human face). "
           "Does NOT mouth-sync wide openings (avatar adds teeth) — keep deliveries soft/closed."),
)

REGISTRY = {c.key: c for c in (BENTLEY, INDI)}


def get(key):
    """Return a Character by key (or pass a Character through unchanged)."""
    if isinstance(key, Character):
        return key
    try:
        return REGISTRY[key]
    except KeyError:
        raise KeyError(f"Unknown character {key!r}. Known: {sorted(REGISTRY)}")
