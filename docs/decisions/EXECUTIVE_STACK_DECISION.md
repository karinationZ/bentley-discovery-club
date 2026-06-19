# Executive decision: move Bentley's Discovery Club to an API stack (2026)
> Research brief, 2026-06-17. Replaces Higgsfield's subscription/credit model with a pay-as-you-go API pipeline. Bottom line: **same/better quality, ~3–5× cheaper per episode, no credit ceiling.**

## TL;DR — the recommendation
Switch to a **code + API pipeline**. The cheapest-but-good stack, all reachable by API key:

| Stage | Tool | API rate (2026) | Why |
|---|---|---|---|
| **Consistent images** | **Nano Banana 2** (or Seedream 4) | ~$0.045/img (Seedream $0.018) | multi-reference char consistency; we already use it |
| **Living-motion video** | **Kling via KIE.ai or fal.ai** | KIE Kling **$0.025–0.05/s**; fal Kling 2.5 Turbo $0.07/s | cheapest credible video; living water + camera control |
| **Lip-sync (animal faces!)** | ~~sync.so~~ **TESTED 2026-06-17 → FAILED on animals** (it re-syncs *human* lips; barely moved the dog/crab mouth). Use a **generate-talking** model instead: **Wan 2.5** (fal, proven on our opening movement) or **Hedra Character-3** | Wan $0.05/s; Hedra ~$0.05/s | re-sync tools (sync.so/latentsync) need human lips; cartoon animals need a model that *generates* the talking performance |
| **Voices** | **ElevenLabs** | Creator **$11/mo** (~100 min) | premium TTS + **voice cloning** to lock Theodore/Bentley/Pip across episodes |
| **Assemble + finish** | **ffmpeg** (+ optional upscale endpoint) | free | carries over unchanged |

**Operationally:** you can get **image + video + lip-sync under ONE aggregator key** (fal.ai or KIE.ai) **+ ElevenLabs for voice** = just **2 API keys** to manage.

## Per-episode cost (3–4 min, ~28 shots, ~10 lip-synced)
| Item | Math | Cost |
|---|---|---|
| Images (~35 keyframes) | 35 × ~$0.03 | ~$1 |
| Video (~28 shots × 6s = 168s) | KIE Kling Std $0.025/s → Pro $0.05/s → fal $0.07/s | **$4–12** |
| Lip-sync (~10 shots × 5s = 50s) | 50 × sync.so $0.05/s | ~$2.50 |
| Voice | ElevenLabs Creator covers ~15+ episodes/mo | ~$0.70 (or $11/mo flat) |
| Finish | ffmpeg local | free |
| **TOTAL compute / episode** | | **≈ $8–16** |

**Versus Higgsfield:** $56/mo that couldn't finish *one* premium episode (a premium ep burned ~650 cr). The API stack: **~$10–16/episode, pay only for what you use, no ceiling.** Weekly (4 eps/mo) ≈ **$40–65/mo of compute + $11 voice** — and you actually get four finished episodes.

## Three options (pick your price/quality point)
- **A — Rock-bottom (~$6–9/ep):** Seedream 4 images + **KIE.ai Kling Standard ($0.025/s)** + sync.so lipsync-2 + ElevenLabs Starter $5. Max savings; reseller-reliability risk; test lip-sync first.
- **B — RECOMMENDED, best-quality-still-cheap (~$12–18/ep):** Nano Banana 2 images + **fal.ai Kling 2.5 Turbo** (or KIE Kling Pro) + **sync.so lipsync-2-pro** (or Hedra Character-3) on hero talking shots + **ElevenLabs Creator $11** (voice cloning) + ffmpeg. Reliable, premium, animal-lip-sync handled.
- **C — Premium (~$25–40/ep):** Nano Banana Pro + **Veo 3.1** (fal, $0.20–0.40/s) for hero shots + Kling for the rest + **Hedra Character-3** lip-sync + ElevenLabs Pro. Best look; still a fraction of a real studio.

## Migration path (most of our work carries over)
- ✅ **Carries over unchanged:** the staged *image → animate → lip-sync → assemble* workflow; **all ffmpeg** assembly/grade/mux/upscale; the locked character DESIGNS (re-used as reference images); the scripts, VO lines, Performance Bible, and the 10 hard rules. The opening movement we just made is the quality target.
- 🔄 **Changes:** Higgsfield MCP calls → direct REST calls (KIE/fal for image+video, sync.so for lip-sync, ElevenLabs for voice). Consistency: Higgsfield "Elements" → pass **reference image(s)** to Kling image-to-video + Nano-Banana multi-reference. Lip-sync: the Wan-upload trick → **sync.so API** (cleaner, animated-native).
- ⚙️ **New (one-time):** get the 2 API keys; I build a small **orchestration script** (call → poll → download → ffmpeg). Optional: train a **character LoRA** on the locked Bentley/Pip renders for rock-solid cross-episode identity.

## Risks — read before switching
1. **Animal-face lip-sync is the #1 unknown.** sync.so *claims* animated support, but a dog **muzzle** (not a frontal humanoid face) must be **tested** before committing. Fallbacks: Hedra Character-3 (also animated), or keep our proven **Wan** path (available on fal.ai). → **Smoke-test this first** (one Bentley close-up).
2. **Cross-episode consistency:** reference-image conditioning is good, not perfect. The gold standard is a **one-time LoRA/character train** on our locked renders, then reuse. Budget a small one-time setup.
3. **Reseller reliability:** KIE.ai is cheapest but a reseller (rate-limit/uptime risk). **fal.ai** is more production-reliable (faster cold start ~0.5s); **Replicate** is best for big batch jobs. Suggested: **fal.ai primary + KIE.ai for cost-sensitive bulk.**
4. **No UI:** it's a code pipeline now (I run it via your keys) — more setup, but far cheaper, scriptable, ceiling-free.

## Recommended next step (cheap, decisive)
**Smoke-test option B's two risky pieces for a few dollars** before any migration: (1) one **Bentley talking close-up through sync.so** (does animal-face lip-sync hold?) and (2) one **Kling shot via fal.ai/KIE** from our locked keyframe (consistency + living water). If both pass, I build the orchestration script and we run Episode 1's remaining acts on the new stack at ~$10–16 instead of ~$40+.

---
### Sources (2026)
- Video API pricing: [KIE.ai Kling](https://kie.ai/kling/v2-1) · [KIE.ai Kling 3.0](https://kie.ai/kling-3-0) · [fal.ai video](https://fal.ai/learn/tools/ai-video-generators) · [AI video API pricing Apr 2026 (buildmvpfast)](https://www.buildmvpfast.com/api-costs/ai-video) · [DevTk AI video pricing 2026](https://devtk.ai/en/blog/ai-video-generation-pricing-2026/) · [PiAPI vs official Kling](https://piapi.ai/blogs/how-piapi-s-kling-api-is-better-than-the-official-kling-api-cost-speed-and-additional-features) · [EvoLink Kling/Seedream](https://evolink.ai/blog/seedream-pricing-guide-2026)
- Images: [Nano Banana 2 pricing](https://www.glbgpt.com/hub/how-much-does-nano-banana-2-cost-full-pricing-api-and-subscription-guide/) · [Cheapest image APIs 2026 (Atlas)](https://www.atlascloud.ai/blog/guides/cheapest-ai-image-generation-api-2026)
- Lip-sync: [sync.so pricing](https://sync.so/pricing) · [sync.so models](https://sync.so/docs/models/lipsync) · [Hedra API guide](https://magichour.ai/blog/guide-to-hedra-ai) · [Hedra pricing](https://www.hedra.com/pricing) · [Kling 2.6 native audio](https://getimg.ai/blog/all-you-need-to-know-about-kling-2-6-native-audio-review)
- Voice: [ElevenLabs pricing 2026 (BIGVU)](https://bigvu.tv/blog/elevenlabs-pricing-2026-plans-credits-commercial-rights-api-costs/) · [ElevenLabs pricing (TextToLab)](https://texttolab.com/blog/elevenlabs-pricing)
- Aggregator reliability: [fal vs Replicate vs KIE (apidog)](https://apidog.com/blog/best-ai-inference-platform-guide-2026/) · [fal vs Replicate (TeamDay)](https://www.teamday.ai/blog/fal-ai-vs-replicate-comparison)
