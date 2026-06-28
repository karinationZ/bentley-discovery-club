"""Species anatomy profiles — the CORE lesson of the Talking Character framework.

THE lesson (paid for across Ep1/Ep2): audio-driven avatar + i2v models are trained on **human**
faces/bodies, so they leak human anatomy into non-human characters — human teeth in an octopus's
mouth, a five-fingered hand on a tentacle, a human smile on a dog. A negative prompt ALONE is weak.

What works: **positively DESCRIBE the correct non-human anatomy, THEN ban the human version.**
Every ``AnatomyProfile`` carries both halves, so any prompt built from it does this automatically.
Add a new profile (e.g. INSECT for the Ep3 ants) and every downstream prompt inherits the discipline.
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class AnatomyProfile:
    species: str
    limbs: str        # POSITIVE: what the limbs actually are
    mouth: str        # POSITIVE: the correct talking mouth + how it moves
    teeth: str        # POSITIVE: the teeth rule stated plainly
    forbid: tuple      # NEGATIVE: the human-prior to ban, AFTER the positive description

    def describe(self) -> str:
        """Positive, drawn-true-to-the-real-animal description (goes FIRST in a prompt)."""
        return (f"Its body is non-human and must be drawn true to a real {self.species}: "
                f"{self.limbs}; {self.mouth}; {self.teeth}")

    def ban(self) -> str:
        """The human-prior ban (goes AFTER the positive description)."""
        return "Strictly avoid human anatomy: " + "; ".join(self.forbid)


DOG = AnatomyProfile(
    species="dog",
    limbs="it stands on four dog paws",
    mouth=("a natural dog muzzle whose lower JAW simply drops open and closes for the words — lips loose, "
           "mouth corners staying neutral and slightly DOWN like a real boxer's soft jowls; it does NOT smile"),
    teeth="only small, natural lower dog teeth ever show",
    forbid=("no human hands or fingers", "no human smile or grin", "no upturned or curled-up mouth corners",
            "no wide toothy human grin", "no flat row of human teeth", "no human-like lips"),
)

CEPHALOPOD = AnatomyProfile(
    species="octopus",
    limbs=("it has eight smooth, boneless, tapering tentacles lined with small round suckers and ending in soft "
           "curling tips — every limb stays a tentacle, and a reaching limb is always a curling tentacle, never a hand"),
    mouth="a soft, small, rounded, gently-moving cephalopod mouth",
    teeth="it has NO teeth at all — fully toothless",
    forbid=("no human hands, fingers, palms or thumbs", "no teeth", "no gums", "no human lips", "no human smile"),
)

# Registry so episodes/characters can look a profile up by species name.
PROFILES = {"dog": DOG, "octopus": CEPHALOPOD, "cephalopod": CEPHALOPOD}
