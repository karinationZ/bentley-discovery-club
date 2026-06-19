#!/usr/bin/env python3
"""EP1 v2 FINAL (v4 — SYNC FIX) sound mix. Dialogue rides the PICTURE's embedded lip-synced audio
([0:a]); narration/cry/sfx/music/ambient are layered over it. Narration sits ONLY over motion shots
and is DYNAMICALLY CAPPED (read from timeline2.json) to end >=0.2s before the next talk shot — so no
two voices ever overlap. Cry answers Bentley. Music re-pinned to shot anchors. loudnorm -14, mux."""
import os, json, subprocess
from bentley.shared.ffio import dur
from bentley.shared.paths import episode_assets
from bentley.episode_builder.timeline import make_next_talk_start, place_sequential
ROOT = str(episode_assets("hybrid_ep1"))
V2 = f"{ROOT}/v2"; AUD, SFX, MUS, WORK = f"{V2}/audio", f"{V2}/sfx", f"{V2}/music", f"{V2}/work"
TLJSON = json.load(open(f"{WORK}/timeline2.json"))
TL = {s["id"]: s for s in TLJSON}
def st(i): return TL[i]["start"]
# dur() imported from bentley.shared.ffio
PIC = f"{WORK}/EP1_v2_picture.mp4"; picdur = dur(PIC)
# next_talk_start + sequential voice placement now live in bentley.episode_builder.timeline

# NARRATION / O.S. — (file, anchor_id, offset, gain). Placed over MOTION shots; auto-capped to next talk −0.2s.
NARR = [
 (f"{AUD}/THEO_INTRO1.mp3","I1_establish",0.4,2),(f"{AUD}/THEO_INTRO2.mp3","I2_hero",0.3,2),
 (f"{AUD}/THEO_FACT1.mp3","a1_04_reveal",0.6,2),
 (f"{AUD}/PIPOS_wave1.mp3","a3_02a_wave",0.4,3),   # Pip panic over the LIVE wave (seg1); seg2 is embedded in a3_02b
 (f"{AUD}/BENTOS_chain.mp3","a4_01_crowd",0.3,2),(f"{AUD}/THEO_FACT4.mp3","BR2_lineshuffle",0.3,2),
 (f"{AUD}/THEO_N16.mp3","a4_03_cascade",0.3,2),
 (f"{AUD}/BENTOS_octo.mp3","a6_01_octopus",0.6,2),(f"{AUD}/THEO_outro.mp3","END_card",0.5,2),
]
CRY = (f"{AUD}/PIPOS_help1.mp3", "a1_02_hear", -1.5, 1, 1.0)  # cry HEARD before Bentley reacts
SX = [
 (f"{SFX}/gull.mp3","I1_establish",1.5,-16),(f"{SFX}/sparkle.mp3","I1_establish",2.6,-10),
 (f"{SFX}/chime.mp3","I1_establish",4.0,-10),(f"{SFX}/paws.mp3","BR3_explore",1.0,-13),
 (f"{SFX}/wave_rise.mp3","a3_02a_wave",0.3,-9),(f"{SFX}/wave_crash.mp3","a3_02a_wave",2.2,-7),(f"{SFX}/wave_crash.mp3","a3_03_recoil",0.3,-7),
 (f"{SFX}/shake.mp3","N3_bridge",0.4,-11),(f"{SFX}/skitter.mp3","a4_01_crowd",1.0,-13),
 (f"{SFX}/skitter.mp3","BR2_lineshuffle",1.5,-13),(f"{SFX}/clicks.mp3","a4_03_cascade",0.6,-9),
 (f"{SFX}/clicks.mp3","BR1_crableave",1.0,-10),(f"{SFX}/sparkle.mp3","a4_04_whoaa",0.2,-9),
 (f"{SFX}/chime.mp3","a5_01_piphome",1.0,-13),(f"{SFX}/octo_curl.mp3","a6_01_octopus",1.2,-11),
 (f"{SFX}/wave_crash.mp3","a6_01_octopus",6.4,-7),(f"{SFX}/sparkle.mp3","a6_01_octopus",6.8,-9),  # octopus SPLASH + magic
]
# MUSIC — anchored to shot ids (robust to timeline). (file, anchor_id, gain, fadein, fadeout)
MU = [
 (f"{MUS}/calm_mystery.mp3","I1_establish",-11,1.5,3),(f"{MUS}/theme_wonder.mp3","a1_02_hear",-12,2,3),
 (f"{MUS}/suspense.mp3","a3_01_fix",-11,1.5,3),   # dropped theme_wonder re-anchor @N1 -> continuous bed across a1_06->N1 seam (issue #2)
 (f"{MUS}/suspense.mp3","a3_03_recoil",-11,1.0,3),
 (f"{MUS}/emotional_piano.mp3","N4_lonely",-10,2,4),(f"{MUS}/triumph.mp3","a4_01_crowd",-11,1.5,3),
 (f"{MUS}/theme_wonder.mp3","a5_01_piphome",-12,2,3),(f"{MUS}/triumph.mp3","a5_04_tag",-10,1.5,4),
]
AMB = f"{SFX}/amb_ocean.mp3"

inputs, filt, labels, idx = [], [], ["adia"], 1
filt.append("[0:a]aresample=48000,volume=1dB[adia]")  # dialogue rides the picture
def add(path, delay, gain, cap=None, fades=None, stream_loop=0):
    global idx
    if stream_loop: inputs.extend(["-stream_loop", str(stream_loop)])
    inputs.extend(["-i", path]); ms = max(0, int(round(delay*1000)))
    chain = "aresample=48000"
    if cap: chain += f",atrim=0:{cap:.3f},asetpts=PTS-STARTPTS"
    if fades:
        fi, fo, d = fades; chain += f",afade=in:st=0:d={fi},afade=out:st={max(0,d-fo):.2f}:d={fo}"
    chain += f",adelay={ms}:all=1,volume={gain}dB"
    lab = f"a{idx}"; filt.append(f"[{idx}:a]{chain}[{lab}]"); labels.append(lab); idx += 1

# Chronological SEQUENTIAL placement of narration + cry: each voice starts >=0.25s after the
# previous voice ends (no narration-narration overlap) AND is capped to end >=0.2s before the next
# dialogue shot (no narration-dialogue overlap). One voice at a time, guaranteed.
events = [(st(anc) + off, path, g, None) for path, anc, off, g in NARR]
events.append((st(CRY[1]) + CRY[2], CRY[0], CRY[3], CRY[4]))   # cry, with its 1.0s hard cap
events.sort(key=lambda e: e[0])
nts = make_next_talk_start(TLJSON, picdur)
sched = [(desired, dur(path), hardcap) for desired, path, g, hardcap in events]
for i, start, cap, avail, placed in place_sequential(sched, nts):
    path, g = events[i][1], events[i][2]
    if placed:
        add(path, start, g, cap=cap)
    else:
        print(f"  SKIP {os.path.basename(path)} (window {avail:.2f}s @ {start:.1f}s)", flush=True)
for path, anc, off, g in SX:
    start = st(anc) + off
    if start < picdur - 0.3: add(path, start, g)
for path, anc, g, fi, fo in MU: add(path, st(anc), g, fades=(fi, fo, dur(path)))
add(AMB, 0.0, -17, stream_loop=14)

mixn = len(labels)
filt.append("".join(f"[{l}]" for l in labels) + f"amix=inputs={mixn}:normalize=0:duration=longest[mx]")
filt.append("[mx]alimiter=limit=0.95,loudnorm=I=-14:TP=-1.5:LRA=11[aout]")
fc = ";".join(filt)
OUT = f"{WORK}/EP1_v2_premix.mp4"
cmd = ["ffmpeg","-y","-loglevel","error","-stats","-i",PIC] + inputs + \
      ["-filter_complex", fc, "-map","0:v","-map","[aout]",
       "-c:v","copy","-c:a","aac","-b:a","192k","-ar","48000","-ac","2","-t",f"{picdur:.3f}", OUT]
print(f"mixing {mixn} elements (1 dialogue bus + {mixn-1} layers) -> premix ({picdur:.1f}s) ...", flush=True)
subprocess.run(cmd, check=True)
print(f"PREMIX -> {OUT}  {dur(OUT):.2f}s", flush=True)
