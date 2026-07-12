#!/usr/bin/env python3
"""T2 renderer — animatic leaves (stills + VO + assembly), PRD §7.4.

Compiles a node's T1 storyboard into a real, playable 9:16 video:

  stills     each storyboard frame screenshotted via headless Chromium
             (Playwright) — $0, deterministic, no image API required.
             Optionally replaced later by generated art (bring your own key).
  voice      optional TTS narration per frame via OPENAI_API_KEY
             (--tts openai); without a key the animatic is silent with
             on-frame text carrying the script (still watchable, still $0).
  assembly   ffmpeg (bundled via imageio-ffmpeg) concatenates frames with
             durations estimated from text length into <node>-t2-a.mp4.

Every render publishes full provenance (§7.2): providers, models, per-part
costs. Compute-as-watering: citizens run this with their own keys and submit
the leaf (WATERING.md).

Usage:
    python3 pipeline/render_t2.py <genome> <node-id> [--tts openai] [--dry-run]
"""

import argparse
import json
import math
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parent.parent
WIDTH, HEIGHT = 720, 1280  # 9:16
MIN_SEC, MAX_SEC = 3.0, 12.0
READ_CPS = 15.0  # chars/sec reading speed → per-frame duration


def ffmpeg_exe() -> str:
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except ImportError:
        return "ffmpeg"


def frame_durations(t1_html: str) -> list:
    """Estimate seconds per frame from visible text length."""
    frames = re.findall(r'<div class="frame">(.*?)</div>\s*(?=<div class="frame">|<footer)', t1_html, re.S)
    durations = []
    for f in frames:
        text = re.sub(r"<[^>]+>", " ", f)
        sec = min(MAX_SEC, max(MIN_SEC, len(text.strip()) / READ_CPS))
        durations.append(round(sec, 1))
    return durations


def shoot_stills(t1_file: Path, count: int, outdir: Path) -> list:
    """Screenshot each storyboard frame at 9:16 via headless Chromium.

    Node resolves modules from the script's own directory, so the script is
    written next to a node_modules containing playwright (T2_NPM_DIR env, or
    any dir where `npm install playwright` was run)."""
    npm_dir = Path(os.environ.get("T2_NPM_DIR", outdir))
    script = npm_dir / "t2-shoot.js"
    script.write_text(f"""
const {{ chromium }} = require('playwright');
(async () => {{
  const b = await chromium.launch({{ executablePath: '/opt/pw-browsers/chromium' }});
  const p = await b.newPage({{ viewport: {{ width: {WIDTH}, height: {HEIGHT} }}, deviceScaleFactor: 1 }});
  await p.goto('file://{t1_file.resolve()}');
  await p.addStyleTag({{ content: `
    main {{ max-width: none; padding: 0; }}
    h1, .sub, footer {{ display: none; }}
    .frame {{ width: {WIDTH}px; height: {HEIGHT}px; margin: 0; border-radius: 0;
             border: none; justify-content: center; padding: 3rem 2.2rem; }}
    .frame * {{ font-size: 1.35em; }}
  ` }});
  const frames = await p.$$('.frame');
  for (let i = 0; i < frames.length; i++) {{
    await frames[i].scrollIntoViewIfNeeded();
    await frames[i].screenshot({{ path: `{outdir}/frame-${{String(i).padStart(3,'0')}}.png` }});
  }}
  await b.close();
  console.log(`shot ${{frames.length}} stills`);
}})();
""")
    subprocess.run(["node", str(script)], check=True)
    script.unlink(missing_ok=True)
    return sorted(outdir.glob("frame-*.png"))


def tts_openai(text: str, out: Path) -> float:
    """Narrate one frame via OpenAI TTS. Returns cost estimate (USD)."""
    import urllib.request
    key = os.environ["OPENAI_API_KEY"]
    req = urllib.request.Request(
        "https://api.openai.com/v1/audio/speech",
        data=json.dumps({"model": "gpt-4o-mini-tts", "voice": "onyx", "input": text[:2000]}).encode(),
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req) as r:
        out.write_bytes(r.read())
    return round(len(text) / 1_000_000 * 12.0, 5)  # $12/1M chars, published estimate


def assemble(stills: list, durations: list, audio: list, out: Path) -> None:
    """Concat stills (and optional per-frame audio) into an mp4."""
    ff = ffmpeg_exe()
    with tempfile.TemporaryDirectory() as td:
        concat = Path(td) / "concat.txt"
        lines = []
        for img, dur in zip(stills, durations):
            lines.append(f"file '{img.resolve()}'\nduration {dur}")
        lines.append(f"file '{stills[-1].resolve()}'")  # ffmpeg concat quirk: repeat last
        concat.write_text("\n".join(lines))
        cmd = [ff, "-y", "-f", "concat", "-safe", "0", "-i", str(concat)]
        if audio:
            alist = Path(td) / "audio.txt"
            alist.write_text("\n".join(f"file '{a.resolve()}'" for a in audio))
            cmd += ["-f", "concat", "-safe", "0", "-i", str(alist), "-c:a", "aac", "-shortest"]
        cmd += ["-vf", f"scale={WIDTH}:{HEIGHT},format=yuv420p", "-r", "24",
                "-c:v", "libx264", "-preset", "veryfast", "-crf", "28", str(out)]
        subprocess.run(cmd, check=True, capture_output=True)


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("genome")
    p.add_argument("node")
    p.add_argument("--tts", choices=["none", "openai"], default="none")
    p.add_argument("--dry-run", action="store_true")
    args = p.parse_args()

    genome_dir = REPO / "genomes" / args.genome
    lineage_text = (genome_dir / "lineage.yaml").read_text()
    lineage = yaml.safe_load(lineage_text)
    node = next(n for n in lineage["nodes"] if n["id"] == args.node)
    node_dir = genome_dir / "nodes" / node["slug"]
    t1_file = node_dir / "leaves" / f"{node['id']}-t1-a.html"
    if not t1_file.exists():
        raise SystemExit(f"no T1 leaf for {node['id']} — run render_t1.py first (T2 builds on T1)")

    t1_html = t1_file.read_text()
    durations = frame_durations(t1_html)
    total = round(sum(durations), 1)
    leaf_id = f"{node['id']}-t2-a"

    if args.dry_run:
        print(f"would render {leaf_id}: {len(durations)} frames, ~{total}s, "
              f"tts={args.tts}, est. cost ${'0.00' if args.tts == 'none' else '~0.02'}")
        return 0

    workdir = Path(tempfile.mkdtemp(prefix="t2-"))
    stills = shoot_stills(t1_file, len(durations), workdir)
    if len(stills) != len(durations):
        durations = (durations + [MIN_SEC] * len(stills))[: len(stills)]

    audio, cost = [], 0.0
    if args.tts == "openai":
        frames_text = re.findall(r'<div class="frame">(.*?)<div class="num">', t1_html, re.S)
        for i, ft in enumerate(frames_text[: len(stills)]):
            text = re.sub(r"<[^>]+>", " ", ft).strip()
            a = workdir / f"vo-{i:03d}.mp3"
            cost += tts_openai(text, a)
            audio.append(a)

    out = node_dir / "leaves" / f"{leaf_id}.mp4"
    assemble(stills, durations, audio, out)
    size_kb = out.stat().st_size // 1024

    (node_dir / "leaves" / f"{leaf_id}.yaml").write_text(f"""# Leaf metadata — every render publishes its full provenance (§7.2)
leaf: {leaf_id}
node: "{node['id']}"
tier: T2
form: animatic-mp4
content: {leaf_id}.mp4
author: pipeline/render_t2.py (deterministic assembly of the T1 leaf)
model: {"gpt-4o-mini-tts (voice) + chromium stills" if args.tts == "openai" else "none — chromium stills, silent (captions carry the script)"}
prompt: none            # deterministic — the T1 leaf is the source
seed: none
cost_usd: {cost:.2f}
status: live
platform_urls: []
""")
    if leaf_id not in (node.get("leaves") or []):
        new_text = re.sub(
            rf"(- id: \"{re.escape(node['id'])}\"\n(?:.*\n)*?    leaves: \[)([^\]]*)",
            rf"\g<1>\g<2>, {leaf_id}", lineage_text, count=1)
        (genome_dir / "lineage.yaml").write_text(new_text)

    print(f"✓ rendered {leaf_id}: {len(stills)} frames, ~{total}s, {size_kb}KB, cost ${cost:.2f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
