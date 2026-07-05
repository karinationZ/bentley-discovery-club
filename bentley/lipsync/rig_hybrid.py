"""THE HYBRID lip-sync pipeline (owner-approved 2026-07-02): one command, a VO line -> a photoreal,
on-model, temporally-coherent, SINGLE-SPEAKER talking Bentley clip that matches the Kling footage.

  rig (on-model keyframe)  ->  nano-banana-edit (photoreal)  ->  Kling-Avatar (sync to our audio)

Why this and not the pure rig: the pure Blender rig is deterministic+$0 but can't match Kling's
photorealism; per-frame AI restyle FLICKERS. Restyling ONE rig keyframe then letting Avatar generate
one coherent synced clip gives photoreal + stable + correct-speaker. ~44cr (~$0.22)/line.

  python -m bentley.lipsync.rig_hybrid --audio episodes/ep3/vo/B_strong.mp3 \
      --out scratch/rig_build/HYBRID_B_strong_FINAL.mp4 [--keyframe key.png] [--pose "6 4 -8 3"]
"""
import argparse
import subprocess
import tempfile
from pathlib import Path

from bentley.shared.hosting import kie_host
from bentley.shared.kie_client import run, download

ROOT = Path(__file__).resolve().parents[2]
BLENDER = "/Applications/Blender.app/Contents/MacOS/Blender"
KEYFRAME_SCRIPT = ROOT / "scratch/rig_build/render_keyframe.py"
DESERT_RIG = ROOT / "scratch/rig_build/bentley_rig_desert.blend"
# LOCKED photoreal Bentley identity — every shot's restyle is anchored to this so all shots match.
MASTER = ROOT / "scratch/rig_build/Bentley_PHOTOREAL_MASTER.png"

RESTYLE_PROMPT = (
    "Make this cartoon dog a photorealistic CGI Boxer puppy, high-end animated-film quality. "
    "KEEP THE EXACT SAME pose, head angle, framing and mouth position. Add realistic short fur with fine "
    "individual hairs, a wet glossy black nose, soft subsurface skin. "
    "EYES: large, deep DARK-BROWN almost-black eyes with a single bright catchlight and a soulful, warm, intelligent "
    "gaze looking directly into the camera lens — expressive and full of feeling, like she is looking into your soul. "
    "Preserve exactly: red-fawn coat, black face mask, grey chin, floppy folded-down ears, white chest blaze, "
    "teal collar with round gold paw-print tag, and the golden-hour desert background with shallow depth of field. "
    "Photorealistic, cinematic, sharp fur detail. No human features, no human teeth."
)
ANCHOR_PREFIX = ("Match the dog's EXACT identity — face shape, proportions, fur color and markings, and especially "
                 "the dark near-black soulful eyes — to the SECOND reference image. ")
AVATAR_PROMPT = (
    "A red-fawn Boxer puppy with a black face mask speaks warmly and gently to a small friend. "
    "Soft happy expression, natural subtle mouth movements, tongue visible but NO human teeth. "
    "Keep her exact appearance, floppy folded ears, teal collar and round gold paw-print tag, "
    "and the golden-hour desert background. Calm cinematic close-up, minimal head movement."
)


def audio_dur(p):
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries",
                 "format=duration", "-of", "csv=p=0", str(p)]))


def hybrid(audio, out, rig=DESERT_RIG, keyframe=None, pose=(0, 0, 0, 0), anchor=MASTER, workdir=None):
    audio, out = Path(audio), Path(out)
    wd = Path(workdir or tempfile.mkdtemp(prefix="hybrid_"))
    wd.mkdir(parents=True, exist_ok=True)

    # 1) on-model keyframe from the rig (deterministic, single-character)
    if keyframe is None:
        keyframe = wd / "key.png"
        subprocess.run([BLENDER, "-b", str(rig), "-P", str(KEYFRAME_SCRIPT), "--",
                        str(keyframe), *[str(x) for x in pose]], check=True)
    keyframe = Path(keyframe)

    # 2) restyle that ONE frame to photoreal, ANCHORED to the locked master so every shot matches
    photoreal = wd / "key_photoreal.png"
    imgs = [kie_host(str(keyframe))]
    prompt = RESTYLE_PROMPT
    if anchor and Path(anchor).exists():
        imgs.append(kie_host(str(anchor)))
        prompt = ANCHOR_PREFIX + RESTYLE_PROMPT
    r1 = run("google/nano-banana-edit", {"prompt": prompt, "image_urls": imgs})
    download(r1["urls"][0], str(photoreal))
    print(f"restyle: {r1['credits']}cr  (anchored={bool(anchor and Path(anchor).exists())})")

    # 3) Kling-Avatar syncs the photoreal keyframe to our locked-voice audio (one coherent clip)
    raw = wd / "avatar_raw.mp4"
    r2 = run("kling/ai-avatar-standard",
             {"image_url": kie_host(str(photoreal)), "audio_url": kie_host(str(audio)), "prompt": AVATAR_PROMPT},
             timeout=900, poll=10)
    download(r2["urls"][0], str(raw))
    print(f"avatar: {r2['credits']}cr")

    # 4) trim Avatar's silent tail to the audio length + remux the pristine original audio
    dur = round(audio_dur(audio) + 0.05, 2)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(raw), "-i", str(audio),
                    "-map", "0:v", "-map", "1:a", "-t", str(dur), "-c:v", "libx264", "-crf", "18",
                    "-pix_fmt", "yuv420p", "-c:a", "aac", str(out)], check=True)
    total = (r1["credits"] or 0) + (r2["credits"] or 0)
    print(f"-> {out}  ({dur}s, ~{total}cr, photoreal+synced+single-speaker)")
    return out, total


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--audio", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--rig", default=str(DESERT_RIG))
    ap.add_argument("--keyframe", help="use a pre-rendered/posed keyframe instead of the neutral render")
    ap.add_argument("--pose", help='"jaw nod yaw roll" degrees for the rig keyframe', default="0 0 0 0")
    a = ap.parse_args()
    pose = [float(x) for x in a.pose.split()]
    hybrid(a.audio, a.out, rig=a.rig, keyframe=a.keyframe, pose=pose)


if __name__ == "__main__":
    main()
