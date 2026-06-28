#!/usr/bin/env python3
"""Ep2 GATE C — hero shot keyframes (stills only, NO motion). Edits from the locked characters:
Indi from Indi_LOCKED (afdwlt url), Bentley from Bentley_MASTER_clean_16x9. Two-shots pass BOTH refs.
Shots: #3 rock-eye reveal, #14 emergence, #20 squeeze (Indi solo); Bentley talking CU;
       #22 paw-hold, #16 exchange, #16A color-game (Bentley+Indi two-shots).
Run: KIE_KEY=... python3 scratch/ep2/hero_keyframes.py
"""
import sys, os, json, subprocess
ROOT = "/project"
sys.path.insert(0, ROOT)
from bentley.shared import kie_client

OUT = f"{ROOT}/scratch/ep2/hero"; os.makedirs(OUT, exist_ok=True)
INDI_URL = open(f"{ROOT}/assets/character_design/.indi_locked_url.txt").read().strip()

def host(p):
    u = subprocess.check_output(["curl", "-s", "-F", "reqtype=fileupload", "-F", f"fileToUpload=@{p}",
                                 "https://catbox.moe/user/api.php"]).decode().strip()
    if not u.startswith("http"):
        raise RuntimeError("catbox fail: " + u[:120])
    return u

BENT_URL = host(f"{ROOT}/assets/character_design/Bentley_MASTER_clean_16x9.png")
print("INDI_URL:", INDI_URL, "\nBENT_URL:", BENT_URL)

BENT = ("Bentley, a young red-fawn Boxer puppy — black mask, grey chin, small white chest blaze, solid red-fawn legs and "
        "paws (NO white socks), BOTH ears soft floppy folded DOWN, SHORT docked stubby tail, soulful well-proportioned "
        "dark-brown eyes (not googly), teal collar with a softly glowing spiral seashell charm; natural dog mouth with soft "
        "pink tongue and small dog teeth, NO human teeth, NO human grin.")
INDI = ("Indi the octopus — iridescent grape-purple, TEAL lateral eyes (no white sclera, no line), NO nose, NO eyebrows, "
        "tiny soft lipless mouth, two low blue ocelli below the eyes, eight suckered arms; octopus-first, never humanlike.")
LOOK = ("Premium dimensional Pixar/Bluey 3D cartoon, on the reef-edge of a bright tide-pool cove, glassy water, warm but "
        "BRIGHT clean daylight, colorful, sharp, high clarity, NO grain. No text, no watermark.")
NEG_B = "NEGATIVE: white socks, long tail, pricked/up ears, human teeth, human grin, googly eyes, film grain, noise, watermark."
NEG_I = "NEGATIVE: human eyes, white sclera, nose, eyebrows, human face, brown eyes, teeth, film grain, noise, blue-ringed octopus, watermark."

SHOTS = {
 # Indi-solo (edit from Indi locked)
 "s03_rock_eye": ([INDI_URL],
   "A speckled tide-pool rock at the water's edge that is actually INDI camouflaged as a mottled RED-BROWN bumpy rock — now "
   "betrayed by ONE large TEAL octopus eye opening on its surface, with a flush of deep red beginning to bloom across the 'rock' "
   "and a tiny wisp of ink. The 'rock had an eyeball' surprise. Keep Indi's identity (teal eye). " + LOOK + " " + NEG_I),
 "s14_emergence": ([INDI_URL],
   "INDI shyly creeping out from a dark rock crevice into soft light — mantle low, one arm reaching out tentatively, teal eyes "
   "peeking, her two low blue ocelli visible, hopeful and timid: the moment she chooses to come out. " + INDI + " " + LOOK + " " + NEG_I),
 "s20_squeeze": ([INDI_URL],
   "INDI pouring her boneless purple body through an impossibly tiny coin-size GAP between two rocks — her soft body streaming "
   "through, arms trailing, determined and focused. Shows how only her hidden beak limits the gap. " + INDI + " " + LOOK + " " + NEG_I),
 # Bentley-solo CU (edit from Bentley master)
 "bentley_cu_awe": ([BENT_URL],
   "CLOSE-UP of BENTLEY mid-gasp of wonder at the tide pool, eyes wide and soulful, natural dog mouth slightly open (soft pink "
   "tongue, small dog teeth, NO human teeth), her glowing teal-collar shell charm catching the light. " + BENT + " " + LOOK + " " + NEG_B),
 # Two-shots (edit from BOTH locks)
 "s22_pawhold": ([BENT_URL, INDI_URL],
   "Tender MACRO two-shot: BENTLEY's red-fawn paw and INDI's slender purple arm gently touching at the water's edge, soft golden "
   "light, a quiet moment of trust between the dog and the octopus. Use the FIRST reference for the dog/paw, the SECOND for the "
   "purple octopus arm (teal-eye identity). " + BENT + " " + INDI + " " + LOOK),
 "s16_exchange": ([BENT_URL, INDI_URL],
   "Heart-to-heart TWO-SHOT: BENTLEY (red-fawn Boxer, floppy ears, short docked tail) lies calmly at the tide pool facing INDI "
   "(purple octopus, teal eyes) who peeks from the shallow water; the two look at each other tenderly, close and intimate. First "
   "reference = the dog, second = the octopus. " + BENT + " " + INDI + " " + LOOK + " NEGATIVE: human teeth, white socks, nose on octopus, film grain."),
 "s16a_colorgame": ([BENT_URL, INDI_URL],
   "Playful, joyful TWO-SHOT: INDI has playfully turned the exact RED-FAWN color of Bentley's coat to 'match' her new friend "
   "(her skin is now red-fawn, but she KEEPS her teal eyes and octopus shape), side by side with a delighted, surprised BENTLEY "
   "at the tide pool — both happy, cute, bonding. First reference = the dog, second = the octopus. " + BENT + " " + LOOK + " NEGATIVE: human teeth, white socks, nose on octopus, film grain."),
}

print("bal before:", kie_client.credits())
man = {"indi_url": INDI_URL, "bent_url": BENT_URL}
for sid, (refs, prompt) in SHOTS.items():
    try:
        r = kie_client.run("google/nano-banana-edit",
                           {"prompt": prompt, "image_urls": refs, "image_size": "16:9", "output_format": "png"})
        lp = f"{OUT}/{sid}.png"; kie_client.download(r["urls"][0], lp)
        man[sid] = {"path": lp, "refs": len(refs), "credits": r["credits"], "secs": r["secs"]}
        print(f"{sid}: {r['credits']}cr {r['secs']}s -> {lp}")
    except Exception as e:
        man[sid] = {"error": str(e)[:200]}; print(f"{sid}: FAILED {str(e)[:200]}")
json.dump(man, open(f"{OUT}/_hero.json", "w"), indent=1)
print("bal after:", kie_client.credits())
