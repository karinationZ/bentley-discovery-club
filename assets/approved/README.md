# approved/ — Source-of-Truth Assets

These are the **canonical, owner-approved** assets for *Bentley's Big Adventures* Episode 1.
Everything here is a **copy** — the live originals still sit in their original
build locations (mostly under `assets/pilot_shots/hybrid_ep1/`), so the production
scripts continue to work untouched. Treat this folder as the clean reference set
you reach for FIRST before generating anything new (see the token-reuse rule in
the episode-production skill §1–2).

For the full repo asset map and naming conventions see `/ASSET_GUIDE.md`.
For the locked character rules every render must pass see `/MASTER_PROP_RULES.md`.

---

## Remote master images (source of truth for character identity)

These two URLs are the **master reference images** every keyframe is edited *from*
(they live in `pipeline.py` → `REFS`). Do **not** download or commit them here — link only.

| Character | Master image URL |
|-----------|------------------|
| **Bentley** (approved clean master — paws fixed, 16:9, ears down, short docked tail) | `https://v3b.fal.media/files/b/0a9eb213/K0YEhgC0hRPAknNVA_bSO_Bentley_MASTER_clean_16x9.png` |
| **Pip** (hermit-crab master keyframe) | `https://d8j0ntlcm91z4.cloudfront.net/user_3F9AzDc10VXM2MT0k5hLwTCbjQr/hf_20260616_223627_2eb7befd-9545-47ad-9d34-d1f13e108bfa.png` |

> Always run new character keyframes through `nano-banana/edit` **from these masters**
> so the face/markings stay consistent shot to shot.

---

## Subfolders

### `episodes/`
The finished, shippable Episode 1 master and its YouTube thumbnail.
- `Bentley_Ep1_v2_FINAL_1080p.mp4` — the graded, mixed, sync-corrected final cut (1080p). This is the deliverable.
- `Bentley_Ep1_thumbnail.jpg` — the published thumbnail.
- Source: `assets/pilot_shots/hybrid_ep1/`.

### `scenes/`
The **approved kie.ai re-renders** that replaced the broken/superseded shots in the
final v2 cut. These are the `*_NEW.mp4` shots wired into `assemble_v2_final.py`.
- `BR3_explore_NEW.mp4` — Bentley exploring the tide pool (motion/i2v).
- `N1_guess_NEW.mp4` — Bentley "guess" talking beat.
- `N6_payoff_armor_NEW.mp4` — payoff/armor talking beat.
- `a1_02_react_NEW.mp4` — early reaction beat.
- `a3_02a_wave_NEW.mp4` — the **live wave** motion shot (i2v) — replaces the old frozen-wave talking shot. See the avatar-freezes-background gotcha in the episode-production skill's references/PRODUCTION_PLAYBOOK.md (Part 6).
- `a3_02b_pipcu_NEW.mp4` — the split-out Pip close-up that paired with the wave shot.
- `a5_04_tag_NEW.mp4` — end-tag beat.
- `octopus_NEW.mp4` — octopus reveal.
- Source: `assets/pilot_shots/hybrid_ep1/v2/fixed/`.

### `bentley/`
The best **on-model** Bentley stills (short docked tail, ears folded down, solid
red-fawn paws, teal collar + glowing spiral seashell charm). Use as visual QA
references and as edit bases.
- `N6_kie_key_bright2.png` — the approved, well-lit hero close-up (supersedes the darker `N6_kie_key` / `N6_kie_key_bright`).
- `BR3_explore_key.png` — approved full-body exploring pose (good for proportions + paws).
- `N6_kie_key.png` — earlier dusk-lit close-up; kept as a secondary reference (it is still referenced by `test_kie_n6.py`, so its original must remain in place).
- Source: `tests/kie/` and `tests/kie/fix/`.

### `crab/`
The clean canonical **Pip** keyframe (reddish-orange hermit crab, eyes set IN the
face — no eye-stalks, dull cracked brown SPIRAL shell — not a white nautilus,
clean face, smooth shell).
- `a3_02b_pipcu_key.png` — approved Pip close-up.
- Source: `tests/kie/fix/`.

### `shells/`
The clean **smooth** glowing spiral seashell (NO fur — the furry-shell bug is fixed here).
- `CLEAN_shell_key.png` — approved still.
- `CLEAN_shell.mp4` — approved motion clip.
- Source: `assets/pilot_shots/hybrid_ep1/v2/`.

### `voices/`
ONE–TWO cleaned samples of each **LOCKED** voice (cleaned masters, **never** the
`_raw` un-processed exports). Refer to voices by **name** only — the ElevenLabs
voice IDs live in `pipeline.py`.
- **Bentley = "Laura Z"**: `BENTOS_n1guess.mp3`, `BENTOS_awe_n2.mp3`
- **Pip = "Callum" (pitched +10%)**: `PIPOS_help1.mp3`, `PIPOS_wave1.mp3`
- **Narrator = "Bill"**: `THEO_INTRO1.mp3`, `THEO_FACT1.mp3`
- Source: `assets/pilot_shots/hybrid_ep1/v2/audio/`.

---

*Rejected / superseded assets are not here — they live in `assets/deprecated/`,
each logged with a reason in `assets/deprecated/DEPRECATED_LOG.md`.*
