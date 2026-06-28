#!/usr/bin/env python3
"""Bootstrap a rigged 3D character from its master image via Tripo3D (paid cloud API).
Flow: image_to_model -> rig_model(QUADRUPED for Bentley / OCTOPOD for Indi) -> download .glb.
The rigged mesh is then opened in Blender, given a TOOTHLESS dog/cephalopod viseme pose set, and
lip-synced for free with Rhubarb (see lipsync.py) — $0/shot, no human teeth by construction.

Needs a Tripo3D API key: sign up at https://platform.tripo3d.ai -> API Keys -> create one, then add
to .env:  TRIPO_API_KEY=tsk_...
Run: set -a; source .env; set +a; python3 scratch/rig_poc/bootstrap_rig.py bentley
"""
import asyncio, os, sys
from pathlib import Path
from tripo3d import TripoClient, RigType

ROOT = Path("/project")
CHARS = {
    "bentley": dict(image=ROOT / "assets/character_design/Bentley_MASTER_pixar.png", rig=RigType.QUADRUPED),
    "indi":    dict(image=ROOT / "assets/character_design/Indi_LOCKED.png",          rig=RigType.OCTOPOD),
}


async def main(char):
    c = CHARS[char]
    out = ROOT / "scratch/rig_poc" / char
    out.mkdir(parents=True, exist_ok=True)
    key = os.environ.get("TRIPO_API_KEY")
    if not key:
        sys.exit("No TRIPO_API_KEY. Sign up at https://platform.tripo3d.ai, create an API key, add it to .env.")
    async with TripoClient(api_key=key) as client:
        print("Tripo balance:", await client.get_balance(), flush=True)
        print(f"[1/3] image -> 3D model  ({c['image'].name})", flush=True)
        mid = await client.image_to_model(
            image=str(c["image"]), texture=True, pbr=True,
            texture_quality="detailed", geometry_quality="detailed",
        )
        await client.wait_for_task(mid, verbose=True)
        print(f"[2/3] rig as {c['rig'].name}", flush=True)
        rid = await client.rig_model(original_model_task_id=mid, rig_type=c["rig"], out_format="glb")
        task = await client.wait_for_task(rid, verbose=True)
        print("[3/3] download", flush=True)
        files = await client.download_task_models(task, str(out))
        print("RIGGED MODEL ->", files, flush=True)
        print("Tripo balance after:", await client.get_balance(), flush=True)


if __name__ == "__main__":
    asyncio.run(main(sys.argv[1] if len(sys.argv) > 1 else "bentley"))
