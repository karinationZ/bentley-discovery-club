#!/usr/bin/env python3
"""EP3 v7 — re-run the 26 Avatar lip-sync CUs on the NEW desert-background keyframes (scratch/ep3/tk2/)
so they stop reading as one repeated green-studio shot. Routing spreads keyframes so adjacent dialogue
beats differ. Grades warm + overwrites scratch/ep3/talk_graded/<LABEL>.mp4. Also Kling the 3 new shots.
Run: python3 episodes/ep3/talk_rerun.py"""
import sys, time, subprocess, concurrent.futures
from pathlib import Path
ROOT = Path("/project"); sys.path.insert(0, str(ROOT))
from bentley.shared import kie_client
from bentley.shared.hosting import catbox_host
def c(p): return catbox_host(str(ROOT / p))
TK2 = ROOT / "scratch/ep3/tk2"; VO = ROOT / "episodes/ep3/vo"; OUT = ROOT / "scratch/ep3/talk_graded"
GRADE = "eq=brightness=0.04:saturation=1.04:contrast=1.03,unsharp=3:3:0.4:3:3:0.0,format=yuv420p"
BP = "Bentley the red-fawn Boxer puppy talks naturally in the warm scrub, natural dog mouth NO human teeth NO grin, soft eyes, on-model, lively head motion."
MP = "Marco the golden-amber boy ant talks in the warm scrub, big eyes antennae moving, toothless, golden-amber not yellow, on-model, lively."
# label -> (keyframe, prompt) ; keyframes spread so adjacent beats differ
LINES = {
 "B_hook1":("bt_happy1",BP),"B_findline":("bt_happy2",BP),"B_tooheavy":("bt_happy1",BP),"B_whatline":("bt_neutral",BP),
 "B_zoomit":("bt_happy2",BP),"B_oops":("bt_worried",BP),"B_realize":("bt_worried",BP),"B_smellit":("bt_neutral",BP),
 "B_crosseyed":("bt_happy1",BP),"B_dontgrab":("bt_happy2",BP),"B_strong":("bt_warm",BP),"B_youarecity":("bt_happy1",BP),
 "B_lesson":("bt_warm",BP),"B_promise":("bt_catch",BP),"B_deepdrop":("bt_worried",BP),
 "M_igotit":("mk_excited1",MP),"M_smellpath":("mk_neutral",MP),"M_waitno":("mk_worried",MP),"M_lost":("mk_worried",MP),
 "M_youstopped":("mk_excited2",MP),"M_checkyou":("mk_neutral",MP),"M_brave":("mk_neutral",MP),"M_together":("mk_excited1",MP),
 "M_noboss":("mk_worried",MP),"M_nobody":("mk_neutral",MP),"M_comesee":("mk_excited2",MP),
}
def avatar(item):
    label,(kf,prompt)=item
    kfp=TK2/kf/"kf.png"; vop=VO/f"{label}.mp3"
    if not kfp.exists() or not vop.exists(): return f"{label} MISSING kf={kfp.exists()} vo={vop.exists()}"
    img=c(str(kfp.relative_to(ROOT))); aud=c(str(vop.relative_to(ROOT)))
    for a in range(5):
        try:
            r=kie_client.run("kling/ai-avatar-standard",{"image_url":img,"audio_url":aud,"prompt":prompt},timeout=1200,poll=10)
            raw=str(OUT/f"{label}_raw.mp4"); kie_client.download(r["urls"][0],raw)
            subprocess.run(["ffmpeg","-y","-loglevel","error","-i",raw,"-vf",GRADE,"-c:a","copy",str(OUT/f"{label}.mp4")],check=True)
            return f"{label}: {r.get('credits')}cr"
        except Exception as e: time.sleep(12); err=str(e)[:50]
    return f"{label} FAIL {err}"

B=[c("assets/character_design/Bentley_MASTER_pixar.png"),c("assets/character_design/Bentley_MODEL_SHEET_turnaround.png")]
M=[c("assets/character_design/Marco_LOCKED.png"),c("assets/character_design/Marco_MODEL_SHEET.png")]
BE={"name":"bentley","description":"Bentley red-fawn Boxer puppy ALL paws red-fawn no white socks, black mask floppy ears teal collar gold tag","element_input_urls":B}
ME={"name":"marco","description":"golden-amber ant Marco antennae toothless","element_input_urls":M}
SHOTS=[
 ("ant_relay",[ME],"A line of golden-amber ants relay a glowing scent-signal antenna-to-antenna down the trail, the road lighting up as it passes; NO bread crumb, NO dog. Warm scrub. Continuous, no freeze. No text."),
 ("birdshadow",[BE,ME],"A large dark hawk bird-shadow sweeps across the sand; Bentley's head snaps up alert over tiny Marco; both alive. Bentley's paws stay ENTIRELY RED-FAWN, no white. Warm scrub, no humans. Continuous, no freeze. No text."),
 ("burrow2",[BE,ME],"Over Bentley's blurred shoulder onto tiny Marco standing on the burrow rim looking up; gentle rack focus, both alive. Warm low sun, no humans, no white paws. Continuous, no freeze. No text."),
]
def kling(item):
    name,elem,prompt=item
    payload={"prompt":prompt,"image_urls":[c(f"scratch/ep3/bridges/{name}/key.png")],"sound":False,"duration":"5","aspect_ratio":"16:9","mode":"std","multi_shots":False,"kling_elements":elem}
    for i in range(3):
        try:
            r=kie_client.run("kling-3.0/video",payload,timeout=1200,poll=10)
            kie_client.download(r["urls"][0],str(ROOT/f"scratch/ep3/bridges/{name}/shot.mp4")); return f"{name}: {r.get('credits')}cr"
        except Exception as e: time.sleep(10); err=str(e)[:50]
    return f"{name} FAIL {err}"

def main():
    jobs=[("A",i) for i in LINES.items()]+[("K",s) for s in SHOTS]
    def run(j):
        kind,item=j; return (avatar if kind=="A" else kling)(item)
    done=0
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:
        for m in ex.map(run,jobs): done+=1; print(f"  [{done}/{len(jobs)}] {m}",flush=True)

if __name__=="__main__":
    main()
