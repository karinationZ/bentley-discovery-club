---
title: EP2 Restart From Scratch Plan
date: 2026-06-23
tags:
  - bentley/episode-2
  - production/restart
  - pipeline/kling-3
aliases:
  - Episode 2 Restart Plan
  - EP2 Character-Driven Rebuild
---

# EP2 Restart From Scratch Plan

## Decision

Stop patching the current cut.

`scratch/ep2/final_delivery/EP2_v10_FINAL.mp4` has strong individual visuals, but the foundation is still wrong: it feels like beautiful clips stitched together. The next Episode 2 pass should be treated as a fresh character-driven rebuild, not a v10 polish pass.

The new target is:

- Fun
- Curious
- Playful
- Cute
- Adventurous
- Educational

Bentley must feel excited and expressive, not sad. Indi must feel clever, funny, friendly, slightly mysterious, and expressive. The episode should feel like two friends exploring and learning together.

## What Works In v10

Review targets:

- `1:12` window: `scratch/ep2/restart_review/scene_1m12_window.mp4`
- `2:54` window: `scratch/ep2/restart_review/scene_2m54_window.mp4`
- Contact sheets:
  - `scratch/ep2/restart_review/scene_1m12_contact.png`
  - `scratch/ep2/restart_review/scene_2m54_contact.png`

Why these moments work:

- Bentley and Indi are in the same frame.
- The characters face each other, so the viewer understands the relationship.
- The scale relationship is readable: Bentley is the big curious puppy, Indi is small but active.
- The scene has personality: Bentley watches, Indi performs, then they react.
- The audience can attach to both characters because the story happens between them.
- The background supports the moment without replacing it.

This becomes the template for the rebuild.

## What Does Not Work

The current cut fails when it follows this pattern:

`scene -> cut -> unrelated scene -> cut -> narration -> cut -> static insert`

Those sections create confusion:

- Why are we suddenly here?
- Who is talking?
- Why is this character sad?
- How does this fact connect to the story?
- Why did we leave the relationship scene?

The rebuild should use this pattern instead:

`character interaction -> reaction -> discovery -> conversation -> reaction`

The educational facts should arise from the characters playing, exploring, and solving a problem together.

## New Story Shape

The episode should be a two-character adventure, not a narrated science reel.

### Sequence 1: Meet The Mystery

Bentley finds a "rock" with an eyeball. Indi reveals herself as clever and playful, not only scared.

Story goal: hook the audience with surprise and cuteness.

Tone: funny, curious, warm.

Key interaction:

- Bentley wants to boop the rock.
- Indi opens one eye.
- Bentley is thrilled, not gloomy.
- Indi teases: she is not a rock, she is the hide-and-seek champion.

### Sequence 2: The Hide-And-Seek Game

Indi turns the science into a game. She shows Bentley how she changes color and texture. Bentley tries to find her.

Story goal: teach camouflage through play.

Tone: playful and magical.

Required visuals:

- Two-shot setup where Bentley watches Indi.
- Indi changes from purple to rock color.
- Indi changes texture from smooth to bumpy.
- Bentley reacts with delight and confusion.
- No static macro-only science shot unless it is part of their game.

### Sequence 3: Why Hiding Matters

The eel danger is introduced through Indi's point of view, not as a random cutaway.

Story goal: explain why Indi hides without making the episode sad.

Tone: adventurous with soft suspense.

Key interaction:

- Bentley asks why Indi is so good at hiding.
- Indi says hiding keeps little octopuses safe.
- A shadow or ripple interrupts them.
- Indi reacts first, then Bentley notices.
- The eel threat appears in the same geography as the characters.

### Sequence 4: Stop, Look, Listen

Bentley learns that helping does not mean grabbing or chasing. It means staying with Indi and listening.

Story goal: Bentley's lesson lands through action.

Tone: tender but not slow or gloomy.

Key interaction:

- Indi gets nervous or stuck.
- Bentley starts to rush in.
- Indi warns her not to yank.
- Bentley stops herself.
- Bentley says the catchphrase with energy and focus, not sadness.

### Sequence 5: The Escape Artist

Indi uses her boneless body to solve the problem while Bentley coaches and reacts.

Story goal: the science saves the day.

Tone: exciting, clever, triumphant.

Required visuals:

- Indi stuck in a clearly readable gap.
- Bentley close by, reacting and encouraging.
- Indi softens/squeezes/pours through a coin-sized opening.
- Bentley celebrates.
- No slow-motion lag or reused loop.

### Sequence 6: Friendship Button And Ant Tease

The three-hearts/blue-blood fact becomes a warm character moment, not a cheap graphic overlay.

Story goal: land the friendship, then open the next adventure.

Tone: cute, cozy, curious.

Key interaction:

- Indi and Bentley sit together.
- Indi touches Bentley's paw/tag.
- Narrator or dialogue explains the fact briefly.
- Indi gives Bentley the shell clue.
- They look inland together.
- Ants appear as the next mystery.

## New Format: Scene Pods

Do not build a long chain of isolated 4-5 second shots. Build conversation pods.

Each pod is 20-35 seconds and stays in one geography. A pod can use several clips, but they should feel like one scene:

- Establishing two-shot
- Bentley reaction
- Indi reaction
- Shared action
- Insert only when motivated
- Return to two-shot

Cuts inside a pod are allowed, but they must be conversation cuts, not location jumps.

## Shot Rules

Every character scene must satisfy these rules:

- Both characters are present unless the beat truly needs isolation.
- If one character speaks, the other reacts.
- If narrator speaks, the picture still shows character action.
- No dialogue over a static character.
- No shot over 5 seconds without visible acting or a motivated internal cut.
- No black-frame transitions.
- No repeated animation loops unless it is an intentional joke.
- No sad default Bentley face for curiosity beats.
- No sad/slow music bed under playful scenes.

## Mouth And Performance Policy

The new direction asks for proper mouth animation, but the old AI-avatar path is risky for Bentley and Indi because it can create human teeth and human smiles.

Use this hierarchy:

1. **Best:** Kling 3.0 two-character performance shots with subtle mouth movement, body acting, eye movement, and clear reactions; overlay ElevenLabs VO.
2. **Acceptable:** VO-over performance where the mouth movement is approximate but the acting is lively and the speaker is visually clear.
3. **Use carefully:** Kling-Avatar only for short, low-risk lines after full-duration QA proves no human teeth, no human smile, and correct speaker ownership.
4. **Reject:** static character plate with VO, wide human-style smile, tooth-like white mouth shapes, frozen octopus during speech.

Indi's mouth should stay tiny and toothless. Indi can "speak" through eyes, arm gestures, body posture, and small mouth movement. Do not force a humanoid mouth.

Bentley can show dog joy through soft eyes, head tilt, bouncing paws, tail/body wiggle, tongue/pant if clean, and bright posture. Avoid sad brows as the default expression.

## Music Direction

Replace the sad/slow emotional bed with a playful adventure palette.

Default music:

- Light marimba, pizzicato strings, ukulele, glockenspiel, soft hand percussion, buoyant ocean textures.
- Medium-bright tempo, around 95-120 BPM for chase/exploration.
- Curious shimmer for mystery.
- Short suspense stings for eel moments.
- Warm, brief emotional lift only after the rescue.

Avoid:

- Long emotional piano under playful exploration.
- Slow melancholy pads as the default.
- Music that makes Bentley feel lonely or defeated.

## Model And Tool Direction

Forward model rule: use **Kling 3.0** for new motion.

Recommended stack:

- Keyframes: KIE `gpt-image-2-image-to-image` for Bentley identity-critical stills; Nano-Banana Pro or FLUX Kontext for constrained Indi/color/texture edits when they preserve the master.
- Motion: KIE `kling-3.0/video` with `kling_elements`.
- Audio: ElevenLabs for dialogue and narration.
- Edit/mix: ffmpeg assembly, but driven by a real cue sheet/EDL, not concat-script improvisation.
- VFX: ffmpeg/Pillow/After Effects-style overlays for water ripples, ink wipes, tag glow, subtle skin texture shimmer, and final grade.

Kling 2.6 stays retired.

## Production Workflow

### Gate 1: Rewrite The Episode As A Character Scene

Before rendering, write a new short script where Bentley and Indi carry the episode together.

Requirements:

- 6 scene pods, not 35 disconnected beats.
- Narrator supports, but does not carry, the story.
- Each educational fact is introduced because one character does or asks something.
- Bentley's emotional mode is curious/excited/playful by default.
- Indi is funny and clever by default, with mystery and caution underneath.

### Gate 2: Audio-Only Readthrough

Make an audio-only radio edit before picture.

Pass criteria:

- The story is clear with no visuals.
- It feels fun and energetic.
- No line appears out of nowhere.
- Speaker ownership is obvious.
- Music supports play/adventure, not sadness.

### Gate 3: Two-Character Animatic

Build a rough animatic using stills, placeholders, and best v10 windows.

Pass criteria:

- The viewer understands where both characters are.
- The episode works muted.
- No random eel or science inserts.
- Every cut answers the previous shot.

### Gate 4: Generate Only Scene-Pod Assets

Generate shots as pod coverage, not individual disconnected clips.

For each pod, generate:

- One shared two-shot.
- One Bentley reaction.
- One Indi reaction/performance.
- One action insert.
- One return-to-two-shot or resolution shot.

Every generated shot must pass:

- Bentley on-model.
- Indi on-model.
- No human teeth/smiles.
- Both characters lively.
- No static hold.

### Gate 5: Edit With Interaction Rhythm

The edit should feel like:

`talk -> react -> discover -> react -> try -> celebrate`

Not:

`shot -> fact -> shot -> silence -> fact`

Transition language:

- Hard cuts for comedy and action.
- Eye-line cuts for conversation.
- Ink/water wipes for octopus vanish/appearance.
- Match cuts for discovery.
- Short dissolves only for emotional settling.
- No black dips inside the episode.

### Gate 6: Final QA

Run these checks on the final export:

- Watch with sound.
- Watch muted.
- Listen audio-only.
- Check every transition sheet.
- Check mouth/identity risk sheet.
- Check duplicate-source/pHash/SSIM pass.
- Run `blackdetect`.
- Run `freezedetect`.
- Confirm no subtitles or generated text except title/next/outro cards.

If the muted pass feels like random clips, the episode is not done.

If the audio-only pass feels confusing, the episode is not done.

If Bentley feels sad for most of the episode, the episode is not done.

## What To Salvage

Salvage ideas, not the current structure.

Likely salvage:

- The two-character interaction style from 1:12 and 2:54.
- Strong Bentley identity from Kling 3.0.
- Tidepool visual style and color grade.
- Indi/Bentley scale relationship.
- Ant ending concept.
- Shell clue concept.
- Core science facts.

Do not automatically salvage:

- The existing EDL.
- Sad music bed.
- Static science shots.
- One-off eel cutaways.
- Long narration over unrelated visuals.
- Reused single-character talking heads.

## Immediate Next Step

Write `EPISODE2_SCRIPT_v3_CHARACTER_DRIVEN.md` from scratch.

It should be short, scene-based, and dialogue-led:

- Pod 1: "The rock winked."
- Pod 2: "Hide-and-seek champion."
- Pod 3: "Why hiding matters."
- Pod 4: "Stop. Look. Listen."
- Pod 5: "Escape artist."
- Pod 6: "Three hearts and the next clue."

Only after that script works should we create the new cue sheet and generation list.

