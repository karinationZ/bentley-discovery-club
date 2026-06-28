---
title: EP2 v3 Production Cue Sheet
date: 2026-06-24
tags:
  - bentley/episode-2
  - production/cue-sheet
  - script/v3
aliases:
  - EP2 v3 Cue Sheet
---

# EP2 v3 Production Cue Sheet

This is the production sheet for the Episode 2 restart. It is based on `EPISODE2_SCRIPT_v3_CHARACTER_DRIVEN.md`, not the v10/v2 salvage EDL.

## Production Lock

- Build conversation pods, not disconnected clips.
- Keep Bentley and Indi together whenever possible.
- Make facts happen through interaction, play, danger, rescue, and friendship.
- No static character shots.
- No black-frame transition dips.
- No reused animation loops.
- No human teeth on Bentley.
- No teeth on Indi.
- No human-style smiling.
- No slow sad piano main bed.
- New motion uses KIE `kling-3.0/video`.

## Runtime Lock

The full v3 script line pool measures about 579 words. That is too long unless read very fast. The production VO below is the locked recording cut.

Target:

- VO words: about 460-485 words.
- Runtime: 3:35-4:05 with action breaths.
- Pace: bright kids-show pace, not rushed.
- If a pod runs long, cut the lowest-priority joke before shortening the science point.

## Model And Tool Rules

### Keyframes

Use KIE image generation/editing for still keyframes:

- Preferred identity-critical stills: `gpt-image-2-image-to-image` through KIE, using the locked references.
- Existing stack alternative: Nano-Banana Pro / Gemini image for fresh keyframes when it preserves the locked look.
- Surgical edits only: FLUX.1 Kontext for ocelli, color patches, clean mouth fixes, or local plate repair.

Input references:

- Bentley: `assets/character_design/Bentley_MASTER_pixar.png`
- Bentley body: `assets/character_design/Bentley_MODEL_SHEET_turnaround.png`
- Indi: `assets/character_design/Indi_LOCKED.png`
- Indi mouth safety: `assets/character_design/Indi_openmouth.png`
- Tidepool plate: `assets/character_design/TidePool_plate.jpg`

### Motion

Use KIE `kling-3.0/video`.

Default payload shape:

```json
{
  "model": "kling-3.0/video",
  "input": {
    "image_urls": ["<single_keyframe_url>"],
    "sound": false,
    "duration": "<render_duration: 5 or 10>",
    "aspect_ratio": "16:9",
    "mode": "std",
    "multi_shots": false,
    "kling_elements": [
      {
        "name": "bentley",
        "description": "locked red-fawn Boxer puppy, black mask, grey chin, floppy folded ears down, teal collar, gold paw tag, white chest blaze, solid red-fawn paws, short docked tail stub, natural dog muzzle, mouth closed or tiny dark puppy-mouth opening only, no visible teeth, no gums, no grin, no human smile",
        "element_input_urls": ["<Bentley_MASTER_pixar>", "<Bentley_MODEL_SHEET_turnaround>"]
      },
      {
        "name": "indi",
        "description": "locked small purple California two-spot octopus, teal eyes, two teal ring spots, eight soft sucker-lined arms, no nose, no eyebrows, tiny toothless cephalopod mouth",
        "element_input_urls": ["<Indi_LOCKED>", "<Indi_openmouth>"]
      }
    ]
  }
}
```

For two-character shots, create one approved keyframe containing both characters, then pass that single keyframe into Kling 3.0 with both `kling_elements`.

Render duration rule: submit Kling 3.0 clips as 5s or 10s render units, then trim editorially to the `duration` in the shotlist. Any beat with planned visual duration over 5s should render as 10s. Do not ask Kling for arbitrary 6s or 7s clips unless KIE explicitly supports that duration.

Every motion prompt must include timed non-looping action beats and the safety phrase: continuous non-looping performance, no repeated gesture, no freeze-frame, no visible restart. For emotional beats, express emotion through Bentley's eyes, ears, head tilt, body bounce, tail-stub wiggle, and Indi's eyes, ring spots, arms, and body posture, not through a wide mouth.

### Dialogue And Mouth Motion

Primary approach:

- Generate Kling 3.0 performance clips with small, safe mouth movement, expressive eyes, head turns, body acting, and clear speaker ownership.
- Overlay ElevenLabs VO in ffmpeg.
- Do not default to Kling AI-Avatar for Bentley or Indi in this episode.

Fallbacks:

- Indi close dialogue: use `scratch/ep2/make_indi_lipsync.py` with the toothless mouth atlas if a direct mouth-sync close-up is required. This prevents teeth by construction.
- Bentley close dialogue: only use Kling AI-Avatar for very short low-risk lines after full-duration frame QA proves no human teeth, no human smile, and correct voice ownership.
- If any talking render opens too wide, reject it. Do not patch it into the final cut.

## Locked Production VO

Record this cut, not every optional line in the master script.

```text
P1_B01 | Bentley | Helloooo, little rock. You look like you need a boop.
P1_B02 | Bentley | You winked.
P1_I01 | Indi | Rocks are very good winkers.
P1_B03 | Bentley | You are not a rock.
P1_I02 | Indi | I am when I want to be.
P1_B04 | Bentley | I'm Bentley.
P1_I03 | Indi | I'm Indi, and I am impossible to find.
P1_B05 | Bentley | I found you.
P1_I04 | Indi | You found one eyeball. That barely counts.
P1_B06 | Bentley | There are rules?
P1_I05 | Indi | Rule one: no booping the champion.
P1_B07 | Bentley | Champion of what?
P1_I06 | Indi | Hide-and-seek.

P2_I01 | Indi | Watch closely, puppy detective.
P2_B01 | Bentley | I'm watching with my whole face.
P2_B02 | Bentley | Your skin did a costume change!
P2_I02 | Indi | Color and texture. Very fancy. Very useful.
P2_I03 | Indi | No Indi here. Only extremely normal rock.
P2_B03 | Bentley | This rock sounds smug.
P2_I04 | Indi | That is because this rock is winning.
P2_N01 | Narrator | An octopus can change color and texture in a blink.
P2_B04 | Bentley | I was looking at you, and then you became geology.
P2_B05 | Bentley | A clue!
P2_I05 | Indi | A trail, if you listen.
P2_B06 | Bentley | You are tiny trouble.
P2_I06 | Indi | Thank you.

P3_B01 | Bentley | So you hide because it is fun?
P3_I01 | Indi | Fun. Clever. Dramatic. Also because some neighbors have very big mouths.
P3_B02 | Bentley | Your spots just went flashlight.
P3_I02 | Indi | That means: do not be crunchy.
P3_B03 | Bentley | I'll chase it away!
P3_I03 | Indi | Please do not chase anything with that many teeth.
P3_B04 | Bentley | Right. No chasing teeth.
P3_N01 | Narrator | That is a moray eel. Not a villain, just a hungry neighbor. For a small octopus, hiding is smart.
P3_B05 | Bentley | So hide-and-seek is survival.
P3_I04 | Indi | And style.

P4_I01 | Indi | What is that shiny paw?
P4_B01 | Bentley | My Listening Tag. It glows when I stay still.
P4_I02 | Indi | Impressive.
P4_B02 | Bentley | Thank you.
P4_I03 | Indi | It tastes like sunshine and wet dog.
P4_B03 | Bentley | That is my personal brand.
P4_N01 | Narrator | Octopus arms taste and feel. Indi was reading Bentley.
P4_B04 | Bentley | Stop. Look. Listen.
P4_I04 | Indi | You really can stop.
P4_B05 | Bentley | Only for important things.
P4_I05 | Indi | Am I important?
P4_B06 | Bentley | Extremely.
P4_I06 | Indi | Then I shall become extremely Bentley.
P4_B07 | Bentley | You did me! You're a teeny-tiny tidepool Bentley!
P4_I07 | Indi | Do I look brave?
P4_B08 | Bentley | You look like trouble wearing my outfit.

P5_I01 | Indi | Big mouth. Back again.
P5_B01 | Bentley | No chasing teeth.
P5_I02 | Indi | Too tight!
P5_I03 | Indi | No yanking. I am soft parts!
P5_B02 | Bentley | Right. Soft parts. No yanking.
P5_B03 | Bentley | Champion, what does a champion do?
P5_I04 | Indi | Hide?
P5_B04 | Bentley | And?
P5_I05 | Indi | Squeeze.
P5_B05 | Bentley | Squeeze like fancy soup.
P5_I06 | Indi | That is not science wording.
P5_B06 | Bentley | No bones. Slow breath. Soft body.
P5_B07 | Bentley | You did it! You fancy-souped!
P5_I07 | Indi | Escape artist.
P5_N01 | Narrator | If a gap is bigger than her tiny beak, an octopus can pour through.
P5_B08 | Bentley | I wanted to help by pulling.
P5_I08 | Indi | You helped by listening.

P6_B01 | Bentley | You changed color, tasted my tag, and turned into soup.
P6_I01 | Indi | I also have three hearts.
P6_B02 | Bentley | Three? My one heart already gets busy.
P6_I02 | Indi | Two help my gills. One sends blue blood everywhere.
P6_B03 | Bentley | Blue blood?
P6_I03 | Indi | Very fashionable.
P6_N01 | Narrator | Three hearts. Blue blood. Built for hiding, squeezing, and surprising puppies.
P6_B04 | Bentley | I'm glad I found your eyeball.
P6_I04 | Indi | I am glad you stopped chasing it.
P6_B05 | Bentley | Another clue?
P6_I05 | Indi | The next mystery is not in the water.
P6_B06 | Bentley | That crumb has legs.
P6_I06 | Indi | Lots of them.
P6_B07 | Bentley | Where are they going?
P6_I07 | Indi | Underground.
P6_B08 | Bentley | Do underground crumbs need boops?
P6_I08 | Indi | Only after we listen.
P6_B09 | Bentley | Stop. Look. Listen.
P6_N02 | Narrator | And just like that, the tidepool handed Bentley one more secret.
```

## Shot Pods

Each pod should be generated and QA'd as a mini-scene before final assembly.

| Shot ID | Dur | Coverage | VO | Prompt intent |
| --- | ---: | --- | --- | --- |
| p01_s01_boop | 5s | Bentley approaches speckled rock | P1_B01 | Bright tidepool. Bentley trots in curious and playful, paw lifted for a boop. Mouth closed, expressive eyes. |
| p01_s02_eye | 4s | Rock eye reveal | P1_B02 | The "rock" opens one large octopus eye. Bentley freezes in delighted surprise. |
| p01_s03_winkers | 6.3s | Indi reveals | P1_I01-P1_I02 | Indi peeks out and jokes with Bentley. Keep tiny toothless cephalopod mouth; expression through eyes and arms. |
| p01_s04_names | 5.2s | Friend names | P1_B04-P1_I03 | Bentley and Indi introduce themselves in a clean two-shot. |
| p01_s05_found_rules | 6.3s | Bentley found her | P1_B05-P1_B06 | Indi teases Bentley; Bentley asks about the rules. |
| p01_s06_no_boop | 6.3s | Champion reveal | P1_I05-P1_I06 | Indi declares no booping the champion; Bentley learns the game is hide-and-seek. |
| p02_s01_watch | 5s | Game setup two-shot | P2_I01-P2_B01 | Indi gestures like a tiny show-off; Bentley watches with whole-body excitement. |
| p02_s02_costume | 6.8s | Color and texture reaction | P2_B02-P2_I02 | Indi changes purple to rock color and smooth to bumpy while Bentley reacts in-frame. |
| p02_s03_camo_fact | 5s | Camouflage fact | P2_N01 | Narrator fact plays over living transformation and Bentley searching. |
| p02_s04_hidden | 3.8s | Hidden Indi speaks | P2_I03 | Indi is hidden but speaker ownership is clear through one visible eye blink or ring-spot glow. |
| p02_s05_smug | 4.9s | Bentley searches wrong spot | P2_B03-P2_I04 | Bentley sniffs and circles; hidden Indi gives herself away with a tiny arm twitch. |
| p02_s06_geology | 3.9s | Bentley reacts | P2_B04 | Bentley reacts to Indi becoming geology. |
| p02_s07_shell_trail | 7s | Shell clue and pop-out | P2_B05-P2_I06 | Shell taps Bentley paw as a real trail clue toward the crevice; Indi appears on the other side. |
| p03_s01_fun_mouths | 9.5s | Explore toward crevice | P3_B01-P3_I01 | Same geography, both walking together; curiosity stays light. |
| p03_s02_flashlight | 5s | Indi eyespots flare | P3_B02-P3_I02 | Dark ripple crosses water; Indi ring spots brighten, Bentley notices. |
| p03_s03_no_chasing | 7.3s | Eel in same world | P3_B03-P3_B04 | Eel silhouette glides through nearby gap. Bentley starts protective, then stops when warned. |
| p03_s04_moray_fact | 9s | Moray fact | P3_N01 | Narrator names the moray eel over Indi camouflaging and Bentley holding still. |
| p03_s05_relief | 4.3s | Danger passes | P3_B05-P3_I04 | Indi relaxes back to purple; Bentley understands hiding as survival. |
| p04_s01_shiny_paw | 6s | Indi notices tag | P4_I01-P4_B01 | Indi notices the tag; Bentley explains it while remaining upbeat. |
| p04_s02_tag_taste | 7.8s | Indi tastes Bentley tag | P4_I02-P4_B03 | Indi sucker touches Bentley tag; tag glows softly. Both visible. |
| p04_s03_touch_fact | 5.8s | Taste-by-touch fact | P4_N01 | Narrator fact plays over a living paw/tag touch, not a static macro. |
| p04_s04_stop | 4s | Stop Look Listen | P4_B04 | Bentley sits still but happy, not sad. The tag pulses. |
| p04_s05_important | 7.3s | Indi sees Bentley stop | P4_I04-P4_B06 | Indi realizes Bentley can stop for important things. |
| p04_s06_extremely_bentley | 7.4s | Indi turns red-fawn | P4_I06-P4_B07 | Only Indi's skin color changes; keep octopus silhouette, teal eyes, two ring spots, eight arms, and toothless mouth. |
| p04_s07_brave_outfit | 4.5s | Color-copy button | P4_I07-P4_B08 | Bentley reacts with joy through eyes, ears, and body bounce, not a wide smile. |
| p05_s01_shadow_return | 5s | Eel returns | P5_I01-P5_B01 | Same crevice geography; shadow returns. Bentley chooses not to chase. |
| p05_s02_wedged | 7.8s | Indi stuck | P5_I02-P5_B02 | Indi wedges halfway through tiny gap. No still hold; arms move, eyes blink. |
| p05_s03_champion | 6.2s | Bentley coaches | P5_B03-P5_I05 | Bentley lowers to eye level and reminds Indi she is the champion. |
| p05_s04_fancy_soup | 9.7s | Bentley gives science cue | P5_B05-P5_B06 | Bentley gives the no-bones cue before the squeeze. Keep both in frame. |
| p05_s05_escape | 4s | Escape artist button | P5_B07-P5_I07 | Indi finishes squeezing through and reforms, proud. |
| p05_s06_beak_fact | 5.8s | Beak fact | P5_N01 | Narrator fact plays over the clear squeeze-through action. |
| p05_s07_safe_twoshot | 4.7s | Relief and thesis | P5_B08-P5_I08 | Bentley and Indi reunited, soft relief, tag glow. |
| p06_s01_recap | 7.4s | Bentley recaps Indi powers | P6_B01-P6_I01 | Cozy two-shot; both characters alive and close. |
| p06_s02_hearts | 7.2s | Three hearts setup | P6_B02-P6_I02 | Indi explains three hearts through a playful living two-shot. |
| p06_s03_blueblood | 10s | Blue blood fact | P6_B03-P6_N01 | Use subtle bioluminescent internal glow or water reflections, not flat floating hearts. |
| p06_s04_friendship | 4.4s | Glad I found your eyeball | P6_B04-P6_I04 | Fresh warm close two-shot staging reference only; no reused footage or loops. |
| p06_s05_shell_handoff | 4.5s | Next clue | P6_B05-P6_I05 | Indi gives Bentley shell and points inland. |
| p06_s06_ants | 6s | Ant trail reveal | P6_B06-P6_I07 | Match cut from shell line to ants carrying crumb. Bentley and Indi remain motivated observers. |
| p06_s07_boops | 5.1s | Underground boops | P6_B08-P6_I08 | Bentley asks about boops; Indi reminds her to listen first. |
| p06_s08_catchphrase | 3.2s | Catchphrase | P6_B09 | Bentley repeats the catchphrase in a living character shot. |
| p06_s09_next_card | 5s | Next-time card | P6_N02 | Deterministic editorial card: NEXT TIME: THE ANT CITY BENEATH OUR FEET. Do not generate card text in Kling. |

## Transition Plan

- Pod 1 to Pod 2: eye reveal becomes hide-and-seek challenge. No scene jump.
- Pod 2 to Pod 3: shell clue and walking exploration lead to the crevice.
- Pod 3 to Pod 4: after danger passes, Bentley slows down and Indi notices the tag.
- Pod 4 to Pod 5: playful color-copy is interrupted by the returning eel shadow.
- Pod 5 to Pod 6: rescue relief naturally becomes friendship and science payoff.
- Pod 6 to Episode 3: shell handoff points inland; ants reveal follows the character gaze.

## Music Direction

Generate a bright family of cues:

- Main bed: pizzicato strings, marimba, ukulele, glockenspiel, soft hand percussion, gentle tidepool ambience.
- Hide-and-seek: bouncy plucks and tiny percussion.
- Eel: brief suspense stings only, then return to play.
- Rescue: rhythmic pulse, not sad piano.
- Ending: warm playful lift.

## QA Gate

Every shot must pass before assembly:

- Bentley identity: black mask, grey chin, floppy ears, teal collar, gold tag, solid red-fawn paws, short docked tail.
- Indi identity: purple body, teal eyes, two teal ring spots, no nose, no brows, eight arms, toothless mouth. During camouflage/color-copy shots, only skin color/texture may change; silhouette, teal eyes, ring spots, arms, and toothless mouth stay locked.
- Mouth safety: no teeth, no gums, no human smile, no wide mouth grin.
- Acting: visible blink, breath, body shift, reaction, or motivated camera move.
- Scene logic: each shot answers the previous shot.
- Loop check: no visible restart, repeated gesture, or recycled sub-range.
- VO ownership: the visible speaker or motivated listener must be clear.
- Transition check: no black frames between pods.

Worst frame fails. Re-render or replace the shot before final assembly.
