#!/usr/bin/env python3
"""Trial-clip intake — normalize a dropped render into the trials archive.

Takes any video file the founder downloaded from a platform, copies it to
outputs/<platform>/<shot>.mp4, probes it (duration, resolution) via ffprobe,
and writes the provenance meta.yaml with the verbatim prompt from prompts.md.
The /trials/ page picks it up on the next site build.

Usage:
    python3 pipeline/t3-trials/intake.py <file> <platform> <shot A|B|C> \
        --model "Kling 3.0" [--credits 35] [--no-watermark] [--mode i2v] [--notes "..."]
"""

import argparse
import re
import shutil
import subprocess
from datetime import date
from pathlib import Path

HERE = Path(__file__).resolve().parent


def probe(f: Path) -> dict:
    try:
        out = subprocess.run(
            ["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
             "stream=width,height:format=duration", "-of", "csv=p=0", str(f)],
            capture_output=True, text=True, check=True).stdout.split()
        w, h = out[0].split(",")[:2]
        return {"resolution": f"{w}x{h}", "duration_s": round(float(out[-1]), 1)}
    except Exception:
        return {"resolution": "unknown", "duration_s": None}


def shot_prompt(shot: str) -> str:
    text = (HERE / "prompts.md").read_text()
    m = re.search(rf"^## Shot {shot} .*?```\n(.*?)```", text, re.M | re.S)
    return " ".join(m.group(1).split()) if m else "see prompts.md"


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("file", type=Path)
    p.add_argument("platform")
    p.add_argument("shot", choices=["A", "B", "C"])
    p.add_argument("--model", required=True)
    p.add_argument("--credits", default="")
    p.add_argument("--mode", default="t2v", choices=["t2v", "i2v"])
    p.add_argument("--no-watermark", action="store_true")
    p.add_argument("--notes", default="")
    args = p.parse_args()

    dest_dir = HERE / "outputs" / args.platform.lower()
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / f"{args.shot}.mp4"
    shutil.copy(args.file, dest)
    info = probe(dest)

    (dest_dir / f"{args.shot}.meta.yaml").write_text(f"""# Trial output — provenance (§7.2)
platform: {args.platform.lower()}
model: {args.model}
shot: {args.shot}
prompt: {shot_prompt(args.shot)}
mode: {args.mode}
seed: none exposed
duration_s: {info['duration_s']}
resolution: {info['resolution']}
watermark: {str(not args.no_watermark).lower()}
credits_spent: {args.credits or 'unknown'}
cost_usd: 0.00
date: {date.today().isoformat()}
notes: {args.notes}
""")
    print(f"✓ {dest.relative_to(HERE.parent.parent)} ({info['resolution']}, {info['duration_s']}s) + meta.yaml")
    print("  next: python3 pipeline/build_site.py && git add -A && commit — the /trials/ page updates itself")


if __name__ == "__main__":
    main()
