# DEPRECATED_LOG

Assets retired here are **rejected or superseded**. Nothing is ever deleted —
these are **moved** out of the working tree so the live build only sees the
approved set. This is NOT a git repo, so before any move each file's basename
(stem) was grep-checked across every `*.py`; **only files with ZERO `*.py`
references were moved.** Anything still referenced by a script was left in place
(logged under "Skipped" below).

Format: `path` — reason.

---

## bentley/
- `N6_kie_key_bright.png` — superseded intermediate brightening pass of the N6 hero close-up; replaced by `N6_kie_key_bright2.png` (now in `approved/bentley/`). Earlier dusk/toothy look. Zero `*.py` refs.

## crab/
- *(none)* — no standalone rejected Pip stills exist on disk. The eye-stalk / white-nautilus / antennae variants were transient renders that were never saved as discrete named files; they were superseded by the clean keyframe `a3_02b_pipcu_key.png` (now in `approved/crab/`). Per safety rule 5, nothing ambiguous was moved.

## shells/
- *(none)* — no standalone "furry shell" render exists on disk as an identifiable reject file. The furry-shell bug (the global Pixar-soft-fur suffix bleeding onto the shell prop) was fixed by regenerating with `shell_gen.py` → `CLEAN_shell*` (now in `approved/shells/`); the bad versions were overwritten/superseded, not saved separately. Ambiguous shell shots that ARE script-referenced (e.g. `a1_01_shell.mp4`) were left in place (see Skipped).

## scenes/
- *(none moved)* — see Skipped: the one rejected "frozen-wave" shot is still referenced by assembly scripts, so it stays live.

## voices/
All un-cleaned `_raw.mp3` exports and all rejected/superseded voice auditions.
The three **locked** voices were kept in place and copied to `approved/voices/`:
Bentley = "Laura Z" (`BENTOS_*`), Pip = "Callum"+10% (`pip_callum*`/`PIPOS_*`),
Narrator = "Bill" (`narr_Bill_grandpa*`/`THEO_*`).

**Rejected Pip auditions** (locked pick = Callum):
- `pip_liam.mp3`, `pip_liam_raw.mp3` — rejected Pip audition (Liam).
- `pip_will.mp3`, `pip_will_raw.mp3` — rejected Pip audition (Will).

**Rejected Narrator auditions, round 2** (`tests/eleven/narrator/`; locked pick = Bill):
- `narr_Brian_comfort.mp3`, `narr_Brian_comfort_raw.mp3` — rejected narrator candidate (Brian).
- `narr_George_current.mp3`, `narr_George_current_raw.mp3` — rejected narrator candidate (George).
- `narr_Pharaoh_wisdom.mp3`, `narr_Pharaoh_wisdom_raw.mp3` — rejected narrator candidate (Pharaoh).

**Rejected Narrator/grandparent auditions, round 1** (old `NARRATOR_AUDITIONS/`; superseded by Bill):
- `0_REEL_grandparents.mp3`, `0_REEL_warm.mp3` — early audition reels.
- `Theodore_REAL_LINE.mp3` — early Theodore line test.
- `grandpa_1_Theodore.mp3`, `grandpa_2_Mortimer.mp3`, `grandpa_3_Graham.mp3` — rejected grandpa-voice candidates.
- `grandma_4_Loretta.mp3`, `grandma_5_Marlene.mp3`, `grandma_6_Darlene.mp3` — rejected grandma-voice candidates (project went with a grandpa narrator).

**Superseded Bentley voice-test takes** (`tests/eleven/`; locked = Laura Z):
- `bentley_voicetest.mp3` — first raw voice probe.
- `bentley_EXPR_v2.mp3`, `bentley_EXPR_v3.mp3` — expressiveness variants.
- `bentley_FIX_A_slower.mp3`, `bentley_FIX_B_lower_slower.mp3`, `bentley_FIX_C_lower_only.mp3` — pitch/pace fix experiments.
- `bentley_v2_rerecorded.mp3`, `bentley_v3_fast1.mp3`, `bentley_v3_fast2.mp3` — re-record / speed variants.
- `bentley_clean_192.mp3`, `bentley_clean_isolated.mp3`, `bentley_clean_mastered.mp3` — cleaning-chain experiments (the final clean chain lives in `pipeline.py`).
- `bentley_fast1_CLEAN.mp3` — superseded "fast" cleaned take.

---

## Skipped — candidates NOT moved because a `*.py` script still references them

Per safety rule 4, these were grep-flagged as live and **left in their original
location** even though they look superseded/rejected:

- `assets/pilot_shots/hybrid_ep1/v2/a3_02_pip_flip.mp4` — the rejected **frozen-wave** talking shot (superseded by the split `a3_02a_wave_NEW` motion shot + `a3_02b_pipcu_NEW` close-up). Referenced by shot-id stem `"a3_02_pip_flip"` in **`assemble_acts123.py`** and **`assemble_v2.py`**, so it is still wired into those assembly paths. *(It was briefly moved during cleanup and immediately reverted when the stem reference was caught.)*
- `tests/kie/N6_kie_key.png` — earlier dusk-lit N6 close-up. Referenced by **`test_kie_n6.py`**. (Copied to `approved/bentley/` as a secondary reference; original left in place.)
- `assets/pilot_shots/hybrid_ep1/acts123/a1_01_shell.mp4` (and related `a1_01_shell*`) — older establish-shell shot, ambiguous vs. the CLEAN shell. Referenced by stem `"a1_01_shell"` in **`assemble_acts123.py`** and **`assemble_v2.py`**. Left in place (also per safety rule 5 — not a confirmed furry-shell reject).
