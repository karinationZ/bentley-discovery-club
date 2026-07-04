# MASTER_PROP_RULES — Locked character & prop rules

Every render is QA'd against these tables **before it is accepted**. If a frame
breaks a MUST-NEVER, it is rejected and regenerated — do not ship it.

> **Master-prop workflow (always):**
> 1. Start from the **approved master**, never from scratch:
>    - Bentley master image → `pipeline.py` `REFS["bentley"]` (URL in `assets/approved/README.md`)
>    - Pip master image → `pipeline.py` `REFS["pip"]`
>    - Approved stills → `assets/approved/bentley/`, `assets/approved/crab/`, `assets/approved/shells/`
> 2. Edit **from** that master (`nano-banana/edit`) so face / muzzle / markings stay consistent shot to shot.
> 3. QA the result against the tables below. Reject on any MUST-NEVER hit.
> 4. Only when a needed asset truly doesn't exist do you generate new — and get
>    owner sign-off before significant credit spend (see the episode-production skill §1 cost gate).

---

## BENTLEY — female red-fawn Boxer puppy

> **Canonical master (RE-BASELINED Ep2):** `assets/character_design/Bentley_MASTER_pixar.png` — cartoony-Pixar style, **short docked tail**, all features on-model. The photoreal `Bentley_MASTER_hero.jpg` is **retired** to `assets/character_design/reference/` because the AI animation (Kling-Avatar / i2v) only renders cartoony-Pixar and cannot reproduce photorealism — so the master matches the animation + the rest of the world. Derive every Bentley keyframe FROM the Pixar master.

| ✅ MUST HAVE | ❌ MUST NEVER |
|-------------|--------------|
| Short **docked** tail | Long or upright tail |
| Black mask on the face | Different face / muzzle shape |
| Grey chin | Different age (older/adult) |
| White chest blaze | Different coat markings |
| **Solid red-fawn paws — no white socks** | White socks / white paws |
| Floppy ears folded **DOWN** | Upright / pricked ears |
| Natural dog mouth — **small lower teeth only** | Human teeth or a wide human grin |
| Soulful, well-proportioned eyes | Bug-eyed / mis-proportioned eyes |
| Teal collar with a glowing **spiral seashell** charm | Missing/!changed collar or charm |
| Natural Boxer proportions | Distorted proportions |
| Consistent face / muzzle / markings across shots | Fur on shells or props |

> ✅ **PAWS — RESOLVED (owner-confirmed):** Bentley has **solid red-fawn paws, NO
> white socks**. An earlier draft spec briefly listed "white paws" — that was a slip;
> the owner confirmed **Episode 1's look is canonical**. The `paw_fix()` / `fix_paws.py`
> step correctly **removes** any white socks a render adds — **keep that behavior**.
> The approved Bentley master is the "paws fixed" (solid red-fawn) version.

---

## PIP — reddish-orange hermit crab

| ✅ MUST HAVE | ❌ MUST NEVER |
|-------------|--------------|
| Reddish-orange body/coloring | — |
| Big soulful eyes set **IN the face** | Eye-stalks (eyes on stalks) |
| Dull, cracked **brown SPIRAL shell** | A white nautilus shell |
| Clean face | Antennae / whiskers |
| Small natural crab mouth | Human teeth |
| **SMOOTH** shell surface | Fur / hair / fuzz on the shell |

The clean canonical Pip keyframe is `assets/approved/crab/a3_02b_pipcu_key.png`.

---

## Shared prop note — the furry-shell bug

The global "premium 3D Pixar **soft-fur** style" prompt suffix used for characters
must **never** be applied to the seashell (or any hard prop) — it makes the shell
grow fur. The fix is a dedicated clean prompt (`shell_gen.py`) that explicitly
forbids fur/hair/fuzz. The approved smooth shell is `assets/approved/shells/CLEAN_shell_key.png`.
Same principle for any future hard prop: **hard surfaces get a no-fur prompt.**

---

## QA gate

Run every accepted render through `QA_CHECKLIST.md` (Character + Fact sections at
minimum). Anything that fails a MUST-NEVER goes back for a regenerate **from the
approved master** — not a from-scratch reroll.
