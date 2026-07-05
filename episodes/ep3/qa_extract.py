#!/usr/bin/env python3
"""QA prep: for each assembled beat, build a contact sheet (3 frames) + a manifest entry pairing the
PICTURE with the exact VO line(s) spoken over it and the intended beat note. Lets QA agents check
VO-to-picture match, on-model canon, and loops/freezes per beat. Run after assemble_v2.py.
Out: episodes/ep3/_qa/<id>.png (sheets) + episodes/ep3/_qa/manifest.json"""
import json, subprocess, re, os
from pathlib import Path
ROOT = Path("/project")
SEG = ROOT / "episodes/ep3/_segs"
QA = ROOT / "episodes/ep3/_qa"; QA.mkdir(parents=True, exist_ok=True)
SHOTS = json.load(open(ROOT / "episodes/ep3/shotlists/ep3_assembly.json"))["shots"]

# label -> spoken text, from the script VO block
TXT = {}
for ln in (ROOT / "episodes/ep3/EP3_SCRIPT.md").read_text().splitlines():
    m = re.match(r"\s*((?:B_|M_|N_)[a-z]+)\s*\|\s*[BMN]\s*\|\s*(.+)", ln)
    if m:
        TXT[m.group(1)] = re.sub(r"\[[^\]]+\]", "", m.group(2)).strip()


def dur(p):
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)]).decode())


def main():
    man = []
    for s in SHOTS:
        seg = SEG / f"{s['id']}.mp4"
        if not seg.exists():
            continue
        d = dur(seg)
        fr = []
        for j, frac in enumerate((0.1, 0.3, 0.5, 0.7, 0.9)):
            o = QA / f"_{s['id']}_{j}.png"
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{d*frac:.2f}", "-i", str(seg),
                            "-frames:v", "1", "-vf", "scale=300:169", str(o)], check=True)
            fr.append(str(o))
        sheet = QA / f"{s['id']}.png"
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *sum([["-i", f] for f in fr], []),
                        "-filter_complex", "[0][1][2][3][4]hstack=5", str(sheet)], check=True)
        labels = re.findall(r"(?:B_|M_|N_)[a-z]+", s.get("vo", ""))
        vo_text = " / ".join(f"[{l}] {TXT.get(l, '?')}" for l in labels) or "(no VO — visual beat)"
        seq = s.get("seq")
        if seq:
            srcs = [(Path(p["src"]).parent.name + "/" + Path(p["src"]).name if p["src"] not in ("TITLE", "CARD") else p["src"]) +
                    (" [LIPSYNC-CUTIN]" if p.get("lipsync") else "") for p in seq]
        else:
            srcs = [Path(x).parent.name + "/" + Path(x).name if x not in ("TITLE", "CARD") else x for x in s.get("srcs", [])]
        man.append({"id": s["id"], "voice": s.get("voice"), "note": s.get("note"),
                    "srcs": srcs, "vo": vo_text, "dur": round(d, 2), "sheet": str(sheet)})
    (QA / "manifest.json").write_text(json.dumps(man, indent=2))
    print(f"-> {QA}/manifest.json  ({len(man)} beats, sheets in {QA})")


if __name__ == "__main__":
    main()
