#!/usr/bin/env python3
"""COMMITTED, versioned final grade for EP1 v2 — bright + vibrant + consistent.
Replaces the un-versioned one-off grades that kept regressing (the dark master got shipped twice).
S-curve lifts shadows + midtones (brings up dark faces) WITHOUT washing highlights, then vibrant
saturation + warm golden balance + gentle local-contrast de-haze. Premix -> delivered FINAL.
NOTE: a grade lifts front-lit shots fully; it cannot key BACKLIT Bentley faces (those need the
Tier-1 re-renders) — it only greys their shadow. That split is by design (see EPISODE1_FIX_PLAN.md)."""
import subprocess
PREMIX = "assets/pilot_shots/ep1/v2/work/EP1_v2_premix.mp4"
FINAL  = "assets/pilot_shots/ep1/Bentley_Ep1_v2_FINAL_1080p.mp4"
GRADE = (
 "curves=master='0/0.045 0.25/0.30 0.5/0.58 0.78/0.85 1/0.965',"            # lift shadows+mids, hold highlights -> bright, NOT washed
 "eq=saturation=1.22:contrast=1.05:brightness=0.0,"                          # vibrant, colorful
 "colorbalance=rs=.01:gs=0:bs=.01:rm=.04:gm=0:bm=-.03:rh=.02:gh=.01:bh=-.02," # warm golden, not an orange cast
 "unsharp=3:3:0.35:3:3:0.0,"                                                 # gentle local contrast / de-haze the milky BGs
 "format=yuv420p"
)
if __name__ == "__main__":
    subprocess.run(["ffmpeg","-y","-loglevel","error","-stats","-i",PREMIX,
      "-vf",GRADE,"-c:v","libx264","-preset","medium","-crf","18","-r","24",
      "-c:a","copy","-movflags","+faststart",FINAL], check=True)
    print("graded FINAL ->", FINAL)
