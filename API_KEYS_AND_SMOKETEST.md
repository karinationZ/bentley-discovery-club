# API keys + smoke-test plan — get the stack ready
> Follow this to grab keys, hand them to me securely, and I'll run the two decisive tests (~$1–2 total) before any migration. Pairs with `EXECUTIVE_STACK_DECISION.md`.

## 1. What to sign up for
You only need **2 keys to run the smoke test** (the first two). ElevenLabs is for production voice later.

| # | Service | Sign up at | Plan to start | Cost | Give me (env var) |
|---|---|---|---|---|---|
| 1 | **sync.so** (lip-sync) | https://sync.so | Hobbyist or pay-as-you-go | $5 (or PAYG) | `SYNC_API_KEY` |
| 2 | **fal.ai** (video Kling + images) | https://fal.ai | add ~$5–10 credit | ~$5 | `FAL_KEY` |
| — | *(cheaper alt to #2)* **KIE.ai** | https://kie.ai | buy $5 credits | $5 | `KIE_API_KEY` |
| 3 | **ElevenLabs** (voices — later) | https://elevenlabs.io | Starter $5 / Creator $11 | $5–11/mo | `ELEVENLABS_API_KEY` |

**How to get each key:** sign in → open your account **Dashboard → API Keys** → **Create key** → copy it. (fal.ai: also add a payment method / credits. KIE.ai & sync.so: buy a small credit pack.)

**Pick fal.ai for the test** (more production-reliable, hosts Kling + images + some lip-sync). Use **KIE.ai** later for rock-bottom-cost bulk if you want.

## 2. Hand me the keys SECURELY (don't paste them in chat)
Create a local file the tests will read — it stays on your machine:

```
# file:  /home/user/src/youtube/.keys.env
SYNC_API_KEY=sk_...your_sync_key...
FAL_KEY=...your_fal_key...
# optional now, needed for production voice:
ELEVENLABS_API_KEY=...your_elevenlabs_key...
# optional cheaper video alt:
KIE_API_KEY=...your_kie_key...
```

Then just tell me **"keys are in .keys.env"** and I'll `source` it in each test (never printed, never committed). *(If we ever put this folder in git, add `.keys.env` to `.gitignore` first.)*

## 3. The smoke test — what I'll run the moment keys exist
Uses assets we already have (locked Bentley keyframes + existing Bentley VO) — no new spend on images/voice.

| Test | What I do | Proves | ~Cost | Pass = |
|---|---|---|---|---|
| **T1 — Animal-face lip-sync** ⭐ | our locked Bentley talking keyframe + existing VO ("Let's go find the WONDER!") → **sync.so `lipsync-2`** | the muzzle actually syncs (THE risk) | ~$0.25 | mouth tracks the words, on-model, not uncanny |
| **T2 — Kling consistency + living water** | our locked Bentley keyframe → **Kling image-to-video** via fal.ai (locked-camera, living water) | character holds + water moves at the cheap rate | ~$0.30–0.50 | Bentley matches keyframe, water alive, no jitter |
| **T3 — (bonus) ElevenLabs voice** | one line via a designed Bentley/Theodore voice *(only if you add the ElevenLabs key)* | voice quality + cloneable consistency | ~free | warm, on-character, reusable |

**Total: ~$1–2.** I'll deliver the clips + a clear ✅/❌ on each, side-by-side with our Higgsfield versions.

## 4. After the test
- **If T1 + T2 pass** → I build the **orchestration script** (`call → poll → download → ffmpeg`) for the recommended stack, and we run **Episode 1's remaining acts (4–6)** on it at ~$10–16 instead of ~$40+.
- **If T1 fails** (muzzle lip-sync weak) → fall back to **Hedra Character-3** (also animated) or keep our proven **Wan** path (available on fal.ai) for talking shots; everything else still migrates.
- Then: a **one-time character LoRA** on the locked Bentley/Pip renders for bulletproof cross-episode identity.

---
**Fastest path:** grab the **sync.so** + **fal.ai** keys (~$10 total), drop them in `.keys.env`, tell me — I run T1 + T2 today.
