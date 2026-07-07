# The Bentley Production Board — a canvas-style orchestration layer for episode production

**Status:** proposal (2026-07-07) · **Motivation:** the EP4 s7b saga — one shot burned ~810 cr across 5
renders + an owner-approval override, because there was no single, persistent surface holding the plan, the
decisions, and each shot's state. This document analyzes the TopView Canvas workflow, compares it to our
`/episode-production` skill, and proposes a concrete board that keeps an AI agent on-rails from premise to release.

---

## 1. What TopView Canvas actually does (and why it's relevant)

TopView Canvas is "Cursor, but for AI video." Its whole value is **one visual workspace that holds the entire
project in front of the agent** so continuity can't slip:

1. **Story first, not clips first.** A one-sentence idea → agent extracts character / conflict / turning point /
   outcome → an approved story draft, *before* any generation.
2. **Locked "asset cards" on the canvas** — a **style card** (the look), **character cards** (reference +
   costume), **environment cards** (locations), **object/prop cards** (the hero props). Everything the project
   must keep consistent lives in one place, not scattered across tabs and the creator's memory.
3. **Scene → shot breakdown with "asset chips."** Each scene decomposes into shots with camera notes, and every
   shot carries **chips linking back to the cards it uses** — so a shot is never "floating," it's tied to its
   character, style, location, and props.
4. **Storyboard / keyframe FIRST.** You review an approved still (composition, emotion, lighting) *before*
   spending on video — "at the image stage, a mistake costs less than a full clip."
5. **Local edits, no rebuild.** Fix one scene/frame in plain English without re-generating the project; if a
   character drifts, point back to its card.
6. **The canvas is the memory.** "Instead of trying to keep everything in my head, I can see the whole video set
   up in front of me" — the exact failure it's designed against: *"the character reference is in one place, the
   scene idea is in another, and by the next generation you're already trying to remind the model what this
   person looked like."*

**The honest caveat (from the video itself):** even with all this, "the final video can drift a little from the
exact character identity — that is just part of the process." Consistency is *managed*, not solved — which is
exactly our situation with Kling.

---

## 2. Where we already match — or beat — TopView

Our `/episode-production` system is **rule-complete and unusually disciplined** for an AI-media pipeline. We are
not behind TopView on process; in several places we're ahead:

| TopView concept | We already have it |
|---|---|
| Story-first | The **cinematic-episode-writer** skill + the **Animatic Lock** gate (zero-credit timed animatic, story+cut validated before any Kling spend) — stronger than TopView's story draft |
| Storyboard/keyframe-first | The **keyframe QC gate (gate 4)** — 4 candidates, `image_bestof` measured ranking, owner pick, paw-zoom QC — *before* the render. This is TopView's storyboard-first, formalized |
| Local edits, no rebuild | The **fix-first ladder (§1b)** — 4 tiers (edit 0cr → local pixel 0cr → surgical AI ~4cr → re-render 70cr) with named deterministic tools (`magic_wand`, `recolor`, `plate_match`, `kontext_edit`, `tail_trim`) |
| Consistency management | The **drift-reduction stack (§3a)** — 8 stacked levers, two **mechanically enforced in code** (`drift_guard` refuses un-pinned character renders; `render_shot` bakes in best-of + pin + element). TopView has nothing comparable |
| Cost discipline | The **mechanical spend fuse** (`gates.py`: no video render without a PASSED Animatic Lock) + Rule-11 waves + the reroll ladder |
| Measured QA | Exit-coded scanners: `edl_lint`, `shot_ratios`, `scan_suite`, `qa_vo`, `image_bestof` — *measured*, not eyeballed |

**Our constitution (the 11 Rules), our procedure (the playbook + tools), and our cost enforcement are all
first-class.** We do not need to rebuild any of that.

---

## 3. The one thing we're missing: a first-class STATE model

The audit finding, in one line: **our system is rule-complete but state-poor.** We narrate state; we don't
store it. The smoking gun:

> Every one of the 22 shots in `episodes/ep4/shotlists/ep4_master.json` still reads `"status": "todo"` — while
> `GATES.md` prose records s1b, s7a, s8, s5a, s4b, and s7b as owner-approved with delivered clips. **The
> structured data and the ledger have fully diverged.** An agent trusting the JSON would conclude nothing has
> been made — the opposite of reality.

Concretely, an agent resuming an episode cold has **no single, structured, trustworthy place** to learn "where
are we, what's approved, what's next." It must replay a ~230-line prose ledger and reconcile supersessions in
its head. Six specific gaps:

| Gap | Today |
|---|---|
| (a) One place to read FIRST for current state | No. `GATES.md` is a 230-line narrative; `HANDOFF.md` is a *second* would-be source of truth. The critical fact "s7b is LOCKED, don't re-touch" is prose buried mid-file, contradicting a paragraph 15 lines above |
| (b) Decisions as structured data | No. Approved paths, reroll counts, verdicts, credit balance all live only as free text inside paragraphs. None queryable |
| (c) A per-shot **state machine** | No. One `status` field, stuck at `todo` for every shot. No `keyframe→approved→rendered→qc→locked` ladder |
| (d) "owner-APPROVED" ≠ "QC-passed" | Only as reactive prose, added *after* the s7b override wasted ~210cr. Nothing marks a shot frozen |
| (e) A "NEXT ACTION" pointer | No. Re-derived every session from prose; the one "state at pause" block is itself obsolete/self-contradictory |
| (f) A locked-asset manifest | No. Masters/keyframes/clips scattered across prose + filesystem; the shotlist's `still` fields still point at **known-wrong animatic placeholders** |

**Every one of the six s7b failures was a state-visibility or state-boundary failure** (§6). The fix is not more
rules — it's a **structured state model** the agent reads first and updates after every step, from which
`GATES.md` and "what's next" are *derived* instead of hand-narrated.

---

## 4. The Bentley Production Board

A single per-episode board that IS the canvas. Two files, one truth:

- **`episodes/ep<N>/board.json`** — the machine-readable state (source of truth).
- **`episodes/ep<N>/BOARD.md`** — a human-readable view *rendered from* `board.json` (never hand-edited). This
  is the "canvas" a person (or agent) reads.

`GATES.md` stops being the source of truth and becomes a *derived* export (the owner-gate ledger view).

### 4.1 `board.json` schema

```jsonc
{
  "episode": "ep4",
  "title": "The Butterfly Highway",
  "guest": "Mira the Monarch",
  "stage": "renders",                    // premise|vo|animatic|keyframes|renders|assemble|mix_grade|qa|release
  "next_action": "s3a: restage as a natural ACTION per its VO, then render",
  "credits": { "balance": 9900, "spent_ep": 2000 },

  "canon": {                             // the LOCKED ASSET MANIFEST — TopView's asset cards
    "style_anchor": "assets/character_design/Bentley_MASTER_pixar.png",  // literal master; painterly is VOID
    "characters": {
      "bentley": { "master": "…/Bentley_MASTER_pixar.png", "turnaround": "…", "talking": "…/Bentley_TALKING_MASTER.png", "voice": "LauraZ" },
      "mira":    { "master": "assets/character_design/Mira_LOCKED.png", "voice": "eleven.MIRA" }
    },
    "environments": { "meadow": "…/Meadow_plate.png", "grove": "…/Grove_plate.png" },
    "props": { "collar": "teal + gold paw-print tag" },
    "models_LOCKED": { "keyframe": "nano-banana-pro", "motion": "kling-3.0/video", "talk": "kling/ai-avatar-standard" }
  },

  "spine": { "feeling": "…", "lesson": "…", "facts": ["…"] },   // always visible → never "lose the track"

  "decisions": [                          // append-only, STRUCTURED (replaces GATES prose)
    { "date": "2026-07-05", "scope": "style", "decision": "anchor = literal master; painterly VOID", "cost": 720, "status": "active" },
    { "date": "2026-07-06", "scope": "s7b", "decision": "stage as a RUN (action), ¾-front to occlude tail", "cost": 810, "status": "active" },
    { "date": "2026-07-07", "scope": "policy", "decision": "owner-APPROVED = LOCKED; QC is pre-approval only", "status": "active" }
  ],

  "shots": [
    {
      "id": "s7b", "beat": "mind-blown", "purpose": "JOY",         // intent, not a frozen pose
      "vo": [ { "label": "B_mindblown", "text": "…the most DOG thing I've ever heard. I LOVE it!" }, { "label": "N_generations" } ],
      "action": "slow-mo run, ¾-front, ears flying",              // the staged ACTION (not a reaction pose)
      "cards": ["bentley", "mira", "meadow"],                     // asset chips
      "plan": "kling",
      "state": "locked",                                          // the STATE MACHINE (see 4.2)
      "keyframe": "scratch/ep4/kf_s7b_run/s7b_run_c3.png",
      "deliverable": "scratch/ep4/renders_w1/s7b_run.mp4",        // OWNER-APPROVED clip
      "approved_by_owner": true, "locked": true,                  // QC CANNOT reopen this
      "rerolls": 0,
      "notes": "owner: 'amazing, I like it!' 2026-07-06"
    }
  ]
}
```

### 4.2 The per-shot STATE MACHINE (the heart)

```
 todo ─▶ keyframe ─▶ kf_approved ─▶ rendered ─▶ qc ─▶ owner_review ─▶ 🔒 LOCKED
   │         │            │            │         │          │
   └── each transition requires its GATE to pass; the gate is recorded on the shot ──┘
                                                             │
                             reject → RESTAGE (new staging)  │  approve → LOCKED (terminal, immutable)
                             reroll ≤2 then restage then trim/downgrade then flag
```

- **`LOCKED` is terminal and immutable.** Once `approved_by_owner: true`, **no tool — including adversarial QC —
  may reopen, re-render, or re-spend on that shot.** This single rule would have saved the ~210 cr wasted when
  s7b's approval was overridden.
- **`rerolls` is a counter on the shot.** At 2 it hard-stops → the board forces RESTAGE (not reroll #3).
- Adversarial QC runs **only on `rendered`/`qc` state, before `owner_review`.** After `LOCKED` it is disabled;
  any later observation is surfaced as **one advisory line for the owner**, never an autonomous action.

### 4.3 The agent protocol (what makes it deterministic)

Seven rules, enforced by reading/writing the board:

1. **Read `board.json` FIRST, every session.** It is the single source of truth. Do not reconstruct state from prose.
2. **Act only on `next_action`.** One shot / one wave at a time (Rule 11). If a task isn't the current stage's next action → stop.
3. **Update the board after every step** — state transition + a `decisions` row + the asset path. *An action not on the board didn't happen.*
4. **Never touch a `LOCKED` shot.** Owner approval = lock. QC is a **pre-approval gate only**.
5. **A shot advances state only by passing its gate;** record the gate result on the shot.
6. **Reroll ≤2 → RESTAGE → trim/downgrade → flag.** The counter lives on the shot; the board refuses reroll #3.
7. **Cosmetic ≠ blocking.** Each defect is tagged `ship_blocking` or `cosmetic`; cosmetic items get one 0-cr pass
   then defer to assembly — the board won't gate an approval on a cosmetic item (kills the s7b paw-pixel rabbit hole).

### 4.4 Gate enforcement (wire the tools we already have)

Each stage transition has a gate; most are the **exit-coded tools that already exist** — so the board doesn't
invent checks, it *orchestrates* ours:

| Transition | Gate (auto unless noted) |
|---|---|
| premise → vo | ✋ owner premise lock |
| vo → animatic | `qa_vo` exit 0 (no flagged lines) |
| animatic → keyframes | `edl_lint` + `shot_ratios` exit 0 **and** ✋ owner Animatic-Lock + credit estimate |
| keyframes → renders | `image_bestof` shortlist **and** ✋ owner keyframe pick (paw-zoom) |
| rendered → qc | adversarial QC sweep (pre-approval) + `tail_trim scan` |
| qc → owner_review | agent presents; **no auto-advance** |
| owner_review → LOCKED | ✋ owner approval at **normal-speed** view → terminal lock |
| all shots locked → assemble → mix/grade → qa | `scan_suite` + `mouthmotion` + §9 checklist |

The two **mechanical spend fuses stay exactly as they are** (`gates.assert_spend_allowed`, `drift_guard.assert_pin_ok`
fire inside `kie_client.run`) — the board sits *above* them, never around them.

---

## 5. Implementation — a `bentley.board` CLI

Small, deterministic, resumable. The board is data; the CLI is the only sanctioned way to mutate it (so it never
drifts from reality the way the `todo` shotlist did):

| Command | Does |
|---|---|
| `python -m bentley.board init ep4` | Scaffold `board.json` from `shotlists/ep4_master.json` + canon masters; every shot `state: todo` |
| `python -m bentley.board status` | Print the header: stage · next_action · credit balance · per-shot state counts. **The first thing every session runs.** |
| `python -m bentley.board next` | Print the single next action + the target shot's full card (VO, purpose, action, cards, gate) |
| `python -m bentley.board advance <shot> <state>` | Transition a shot; **refuses** if the gate for that transition isn't recorded/passed |
| `python -m bentley.board lock <shot> --clip <path>` | Owner-approval terminal lock (records deliverable). Locked shots reject all further `advance` |
| `python -m bentley.board log "<decision>" --scope <s> [--cost N]` | Append a structured decision row |
| `python -m bentley.board render` | Regenerate `BOARD.md` (+ the derived `GATES.md` gate-ledger view) from `board.json` |
| `python -m bentley.board check` | Validate: no shot references a stale placeholder; every locked shot has a real deliverable; credit math balances |

**Migration is cheap:** `init` reads the existing shotlist; a one-time `import-gates` seeds the `decisions` log
and current shot states from the EP4 ledger. From then on `GATES.md` and `HANDOFF.md` are *rendered outputs*, not
authored — ending the two-sources-of-truth problem.

**Skill integration:** `episode-production` gets one new first line — *"Before any episode action, run
`python -m bentley.board status` and act only on `next`. The board is the single source of truth; update it after
every step."* The 11 Rules, playbook, and tools stay unchanged; the board is the **execution layer** that makes an
agent actually follow them.

---

## 6. What it fixes — the s7b failures, mapped

| # | s7b failure | Board feature that prevents it |
|---|---|---|
| 1 | Chased a "reaction POSE" through 5 renders / ~620 cr before re-staging as a RUN | Shot card carries `purpose: JOY` + `action` (not a frozen frame) + the rule "stage the feeling as an action, never a pose" — surfaced on the card |
| 2 | "Lost the track" — forgot the VO until the owner asked | Card always shows `vo` + text + `purpose` at the top of every render decision |
| 3 | Decisions scattered across 230 lines of prose | Structured `decisions[]` log — one scannable row each, supersessions explicit |
| 4 | Re-QC'd + rerolled an **owner-approved** clip (~210 cr) | `locked: true` terminal state; QC disabled on locked shots — **the single highest-value guardrail** |
| 5 | Paw-pixel rabbit hole on a keyframe | `cosmetic` tag + fix-effort ceiling; cosmetic defects can't gate an approval, route to assembly |
| 6 | No "where are we / what's next" view | `bentley.board status` / `next` — one live pointer, no re-derivation, no hand-written resumption note |

---

## 7. Recommendation

Build it in three small phases (each independently useful):

1. **`board.json` + `bentley.board status/next/render`** — the read layer. Immediately gives every agent a single
   "you are here" and kills the re-derivation tax. (Half a day; no risk — read-only over existing files.)
2. **`advance`/`lock`/`log` + gate wiring** — the write layer + the `LOCKED`-is-immutable guarantee (fixes the
   #1 cost failure). `GATES.md` becomes a derived view.
3. **`check` + skill integration** — the validator (no stale placeholders, credit math) + the one-line skill hook
   that makes reading the board mandatory.

The objective is met by construction: a repeatable pipeline where the agent always knows the stage, sees every
shot's state and its VO/purpose/cards, can't reopen an approval, can't batch, can't lose a decision, and can't
get lost — because the board, not the chat history, is the memory.
