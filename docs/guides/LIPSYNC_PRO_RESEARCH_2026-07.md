# How Lip-Sync Is Actually Done — Research Report (2026-07-02)

*Commissioned after the 2.5D mouth-patch system was owner-rejected 3× (anatomically wrong on
free-posed heads). 5 search angles, 15 sources fetched, 25 source-backed claims extracted.
Caveat: the adversarial verification round was cut short by session rate limits — claims below are
labeled by source class: **[VENDOR-DOC]** = the tool's own official docs (reliable for stated
capabilities/limits), **[MARKETING]** = vendor promotion (treat capability claims skeptically).*

---

## 1. Why our 2.5D patch approach was doomed (confirmed by the domain itself)

- **[VENDOR-DOC]** Rhubarb Lip Sync is *audio-only* — timing in, viseme cues out. Its native domain
  is **2D switch-mouth animation on characters DESIGNED with flat replacement-mouth zones**
  (cutout/South-Park style, front-facing by construction). Nothing in its domain covers freely-posed
  3D heads. ([github.com/DanielSWolf/rhubarb-lip-sync](https://github.com/DanielSWolf/rhubarb-lip-sync))
- **[VENDOR-DOC]** Even sync.so's own docs say their re-sync models (lipsync-2/-pro, sync-3)
  **do not support animal/non-humanoid characters** and **degrade on profile views** even for humans.
  Our 2026-06-17 test result is the documented, expected behavior. ([sync.so/docs/models/lipsync](https://sync.so/docs/models/lipsync))
- Conclusion (confirms our failure analysis): **post-hoc flat mouth replacement is only valid on
  characters designed for it, in mouth-visible framings.** On a ¾/down-facing 3D-look muzzle the
  mouth is an occluded seam; no tracking accuracy fixes anatomy. High-end mesh tracking
  (**[VENDOR-DOC]** Lockdown 3, aescripts) can track a deforming muzzle surface and even export the
  solve to Blender — but tracking was never our real problem; **pose/anatomy was.**

## 2. What pros do when sync must be word-accurate on a 3D character: the mouth lives ON the head

- **[VENDOR-DOC]** `blender_rhubarb_lipsync_ng` — free/MIT, maintained (Blender 3.3–5.1) — sequences
  **pre-authored viseme poses** (bone or shape-key Actions) to Rhubarb timing automatically.
  ([github.com/Premik/blender_rhubarb_lipsync_ng](https://github.com/Premik/blender_rhubarb_lipsync_ng))
- **[VENDOR-DOC]** The one-time authoring cost is small and quantified: **5–8 mouth shapes + one idle**
  (classic Hanna-Barbera viseme chart) — not a full facial rig.
  ([superhivemarket.com/products/rhubarb-lipsync-ng](https://superhivemarket.com/products/rhubarb-lipsync-ng))
- Because the visemes are sculpted on the 3D head, **the mouth turns WITH the head** — the exact
  failure of our patch approach disappears *by construction*, along with drift and human-teeth risk
  (the rig physically can't grin). This matches our own verified 2026-06-24 research
  (`ANIMATION_PIPELINE_RESEARCH.md`: Blender + Rhubarb, Tripo3D bootstrap of the mesh from the
  locked master).
- Cost profile: **days of one-time build** (mesh from master, ~9 viseme shapes per character), then
  ~zero marginal cost per line forever. Dialogue shots are re-rendered from the rig (or comped over
  plates via a mesh-track solve — Lockdown-style — but re-render is the honest path for a tiny team).

## 3. The 2026 AI-native path: dialogue is GENERATED WITH the shot, not added after

The market moved decisively to **generation-time dialogue**. Nobody credible offers post-hoc
animal-mouth re-sync; the working tools bake sync into generation:

| Tool | What it is | Animal/stylized? | Fits our stack? |
|---|---|---|---|
| **OmniHuman-1.5** (ByteDance, on Replicate) | **image + OUR audio → video** with synced performance | **[MARKETING]** explicitly claims real animals, anthropomorphic + stylized cartoon characters; **multi-character scenes with per-character audio routing** | ⭐ Best architectural fit: keyframes are already our craft, and it takes **our ElevenLabs VO directly** (locked voices preserved). Replaces Kling i2v on dialogue sections. Needs ONE smoke test. |
| **Kling 3.0 native audio** (already on KIE!) | dialogue generated in-shot; roles assigned per character in the prompt | **[MARKETING]** "accurate lip sync", multi-character; **no animal/stylized evidence shown** | On our backend today; with-audio = **$0.10/s vs $0.07/s** (≈ +$0.03/s). ⚠️ It generates **its own TTS voice** — conflicts with locked ElevenLabs voices unless voice input/dubbing works out. Smoke test ≈ $1. |
| **Veo 3.1** (Google) | native multi-speaker dialogue via quote-syntax prompts; reference-image character lock; works in medium shots | **[VENDOR-DOC]** official guide shows non-CU dialogue; animals unproven | Off-backend; same voice-conflict caveat as Kling. Fallback candidate. |
| **Runway Act-Two** | performance transfer from a **human actor video** | **[MARKETING]** claims non-human characters | Requires acting every line on camera; input must be a **single subject, waist-up, mouth visible** — rules out our wides/two-shots/down-poses. Niche only. |

## 4. The constraint that must bend

Our demand was: **continuous two-shots + totally free head poses + word-accurate sync.** The
evidence says no professional pipeline satisfies all three by adding sync afterwards. Pros bend one:

1. **Bend "free head poses" → STAGING (cheapest, universal):** dialogue shots are *designed* so the
   speaker's mouth reads (¾-front minimum). When a head faces away, sync is simply not shown — you
   hold the listener, cut to reaction, or accept VO-over. This is a shot-design rule that belongs in
   `cinematic-episode-writer`, whatever tech we adopt.
2. **Bend "already-generated shots" → generation-time dialogue (AI-native, 2026):** generate the
   dialogue section WITH the performance (OmniHuman-1.5 from our keyframe + our VO; or
   Kling 3.0/Veo 3.1 native audio). The shot is continuous, the mouth is right, because it was never
   a post-process.
3. **Bend "no animator" slightly → the Blender rig (the strategic fix):** one-time build, then every
   episode gets consistency + sync + teeth-safety for free. This remains the endgame our June
   research already recommended.

## 5. Recommended sequence (cheapest-information-first)

1. **Smoke test OmniHuman-1.5** (~$1–3): `strong_ts` keyframe + `B_strong.mp3` → 5s. It's the only
   candidate that claims stylized animals AND accepts our own VO AND fits keyframe→video. Judge
   against canon (on-model? no human teeth? mouth right in ¾ pose?).
2. **Smoke test Kling 3.0 native audio** (~$1 on KIE): our strong_ts keyframe, role-assigned line.
   Judge sync + whether the generated voice can be replaced by ElevenLabs without visible mismatch.
3. **Adopt the STAGING rule now** (free): dialogue sections are staged mouth-visible; no sync shown
   on away-facing heads. Goes into `cinematic-episode-writer` + `episode-production`.
4. If (1)/(2) pass canon: adopt for dialogue sections going forward (EP4+; EP3 patch-fix only where
   the owner asks). If both fail: **fund the Blender rig build** — it is the only path with a
   guaranteed ceiling, and every month of Kling spend makes it comparatively cheaper.

## Appendix — what did NOT survive

- 2.5D mouth-patch overlay on free-posed video: rejected by owner 3×; confirmed architecturally
  wrong (this report §1). The `bentley/lipsync/` TIMING layer (Rhubarb adapter, viseme mapping,
  QA-sweep tooling) remains valid for the rig route; the patch renderer is retired.
- Post-hoc video re-sync of any kind for animal faces (sync.so's own docs).
- Act-Two for our shot grammar (single-subject waist-up constraint).
