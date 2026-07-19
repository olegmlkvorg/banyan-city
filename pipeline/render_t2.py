#!/usr/bin/env python3
"""T2 renderer v2 — kinetic-text animatic leaves (shots + motion + assembly), PRD §7.4.

Compiles a node's script into a real, playable 9:16 animatic — one SHOT per
script element (beat title cards, action lines, dialogue, system overlays)
instead of one slide per beat. Each shot is held for reading rhythm and given
a slow Ken Burns drift, hard-cut like a vertical micro-drama, not a deck.

  shots      each script element becomes a typographic 720x1280 card,
             screenshotted via headless Chromium (Playwright) — $0,
             deterministic, no image API required.
  motion     ffmpeg zoompan gives every shot a slow push-in or pull-out;
             beat title cards fade in and out.
  voice      optional TTS narration per shot via OPENAI_API_KEY
             (--tts openai); silent by default — the type carries the script.
  assembly   per-shot clips concatenated into <node>-t2-a.mp4 at 24fps.

T2 still builds on T1: the T1 storyboard leaf must exist, and the script
parse is shared with render_t1 (same beats, same elements — the storyboard
is the contact sheet, the animatic is the cut). Every render publishes full
provenance (§7.2). Compute-as-watering: citizens run this with their own
keys and submit the leaf (WATERING.md).

Usage:
    python3 pipeline/render_t2.py <genome> <node-id> [--tts openai] [--dry-run]
"""

import argparse
import html
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
from render_t1 import extract_script, parse_frames, strip_inline_md  # noqa: E402

REPO = Path(__file__).resolve().parent.parent
WIDTH, HEIGHT = 720, 1280  # 9:16
FPS = 24
ZOOM_SPAN = 0.055  # total Ken Burns travel per shot (5.5%)

SHOT_CSS = """
:root { --bg:#0e1410; --screen:#0a0f0b; --ink:#e6efe8; --muted:#93a698;
  --leaf:#6fce8a; --leaf-soft:#bfe0ca; --amber:#e8b464; --line:#263529; }
* { box-sizing: border-box; }
body { margin:0; background:#000; }
.shot { width:720px; height:1280px; position:relative; overflow:hidden;
  background:
    radial-gradient(130% 90% at 50% -10%, rgba(111,206,138,0.05) 0%, transparent 55%),
    radial-gradient(160% 110% at 50% 115%, rgba(0,0,0,0.75) 0%, transparent 60%),
    var(--screen);
  color:var(--ink); font:15px/1.5 Georgia, serif;
  display:flex; flex-direction:column; align-items:center; justify-content:center;
  text-align:center; padding:6rem 3.4rem; }
.shot .num { position:absolute; bottom:1.5rem; left:0; right:0; text-align:center;
  font:700 0.68rem/1 ui-monospace, Menlo, monospace; color:#1d2a20;
  letter-spacing:0.15em; }
.title .text { font:700 1.55rem/1.5 ui-monospace, Menlo, monospace;
  color:var(--amber); text-transform:uppercase; letter-spacing:0.22em;
  padding:1.6rem 0; border-top:1px solid var(--line); border-bottom:1px solid var(--line); }
.title .node { font:700 0.75rem/1 ui-monospace, Menlo, monospace;
  color:var(--muted); letter-spacing:0.3em; text-transform:uppercase; margin-bottom:2.2rem; }
.action .text { font-style:italic; color:var(--muted); font-size:1.9rem; line-height:1.45; }
.line .who, .vo .who { font:700 0.85rem/1 ui-monospace, Menlo, monospace;
  color:var(--leaf); text-transform:uppercase; letter-spacing:0.28em; margin-bottom:1.6rem; }
.line .text { font-size:2.15rem; line-height:1.38; color:var(--ink); }
.vo .text { font-size:2.05rem; line-height:1.4; font-style:italic; color:var(--leaf-soft); }
.overlay .text { font:1.08rem/1.65 ui-monospace, Menlo, monospace; color:var(--leaf);
  background:rgba(111,206,138,0.06); border:1px solid var(--line); border-radius:14px;
  padding:1.6rem 1.9rem; white-space:pre; text-align:left; max-width:100%; overflow:hidden; }
.small .text { font-size:1.72rem; }
.tiny .text { font-size:1.45rem; }
.overlay.small .text { font-size:0.92rem; }
.overlay.tiny .text { font-size:0.8rem; }
"""


def ffmpeg_exe() -> str:
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except ImportError:
        return "ffmpeg"


def clamp(lo: float, v: float, hi: float) -> float:
    return max(lo, min(hi, v))


def build_shots(frames: list, node_label: str) -> list:
    """One shot per script element; beat headings become title cards.

    Consecutive speakerless quote lines are continuations of the previous
    spoken line (the script format wraps long speeches) and are merged so a
    sentence never splits across cuts."""
    shots = []
    for f in frames:
        slug = strip_inline_md(f["slug"])
        display = re.sub(r"\s*[—–-]\s*\d+:\d+.*$", "", slug).strip() or slug
        shots.append({"type": "title", "who": node_label, "text": display,
                      "dur": clamp(1.3, 1.0 + len(display) / 26.0, 2.0)})
        for item in f["items"]:
            if item[0] == "action":
                text = strip_inline_md(item[1]).strip()
                if not text:
                    continue
                shots.append({"type": "action", "who": "", "text": text,
                              "dur": clamp(1.1, len(text) / 21.0, 3.5)})
            elif item[0] == "line":
                who, text = item[1].strip(), strip_inline_md(item[2]).strip()
                if not text:
                    continue
                if not who and shots and shots[-1]["type"] in ("line", "vo"):
                    prev = shots[-1]
                    prev["text"] += " " + text
                    prev["dur"] = clamp(1.4, len(prev["text"]) / 18.0, 6.0)
                    continue
                kind = "vo" if who.upper().startswith("VO") else ("line" if who else "action")
                shots.append({"type": kind, "who": who, "text": text,
                              "dur": clamp(1.4, len(text) / 18.0, 5.0)})
            elif item[0] == "overlay":
                text = item[1].rstrip()
                if not text.strip():
                    continue
                n_lines = len(text.splitlines())
                shots.append({"type": "overlay", "who": "", "text": text,
                              "dur": clamp(1.6, 0.55 * n_lines + len(text) / 70.0, 4.0)})
    return shots


def size_class(shot: dict) -> str:
    n = len(shot["text"])
    if shot["type"] == "overlay":
        cols = max((len(l) for l in shot["text"].splitlines()), default=0)
        return " tiny" if cols > 52 else (" small" if cols > 40 else "")
    return " tiny" if n > 300 else (" small" if n > 190 else "")


def shots_html(shots: list, node_label: str) -> str:
    divs = []
    for i, s in enumerate(shots):
        who = f'<div class="who">{html.escape(s["who"])}</div>' if s["who"] and s["type"] in ("line", "vo") else ""
        node = f'<div class="node">{html.escape(s["who"])}</div>' if s["type"] == "title" else ""
        divs.append(
            f'<div class="shot {s["type"]}{size_class(s)}">{node}{who}'
            f'<div class="text">{html.escape(s["text"])}</div>'
            f'<div class="num">{html.escape(node_label)} · {i + 1}/{len(shots)}</div></div>'
        )
    return (f'<!doctype html><html><head><meta charset="utf-8">'
            f'<style>{SHOT_CSS}</style></head><body>{"".join(divs)}</body></html>')


def shoot_stills(page_file: Path, count: int, outdir: Path) -> list:
    """Screenshot each .shot card at 9:16 via headless Chromium.

    Node resolves modules from the script's own directory, so the script is
    written next to a node_modules containing playwright (T2_NPM_DIR env, or
    any dir where `npm install playwright` was run)."""
    npm_dir = Path(os.environ.get("T2_NPM_DIR", outdir))
    script = npm_dir / "t2-shoot.js"
    # CI ships a pinned chromium at a fixed path; locally (and anywhere that
    # ran `npx playwright install`) let playwright resolve its own binary.
    ci_chromium = "/opt/pw-browsers/chromium"
    launch_opts = (f"{{ executablePath: '{ci_chromium}' }}"
                   if os.path.exists(ci_chromium) else "{}")
    script.write_text(f"""
const {{ chromium }} = require('playwright');
(async () => {{
  const b = await chromium.launch({launch_opts});
  const p = await b.newPage({{ viewport: {{ width: {WIDTH}, height: {HEIGHT} }}, deviceScaleFactor: 1 }});
  await p.goto('file://{page_file.resolve()}');
  const shots = await p.$$('.shot');
  for (let i = 0; i < shots.length; i++) {{
    await shots[i].scrollIntoViewIfNeeded();
    await shots[i].screenshot({{ path: `{outdir}/shot-${{String(i).padStart(3,'0')}}.png` }});
  }}
  await b.close();
  console.log(`shot ${{shots.length}} stills`);
}})();
""")
    subprocess.run(["node", str(script)], check=True)
    script.unlink(missing_ok=True)
    return sorted(outdir.glob("shot-*.png"))


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


def kenburns_clip(ff: str, img: Path, dur: float, idx: int, is_title: bool, outdir: Path) -> Path:
    """One still → one motion clip: slow push-in (even shots) or pull-out
    (odd shots); title cards also fade in/out. Upscaled 3x before zoompan so
    the subpixel drift stays smooth."""
    frames = max(int(round(dur * FPS)), 12)
    if idx % 2 == 0:
        z = f"1+{ZOOM_SPAN}*on/{frames}"
    else:
        z = f"1+{ZOOM_SPAN}*(1-on/{frames})"
    vf = (f"scale={WIDTH * 3}:{HEIGHT * 3}:flags=lanczos,"
          f"zoompan=z='{z}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'"
          f":d={frames}:s={WIDTH}x{HEIGHT}:fps={FPS}")
    if is_title:
        vf += f",fade=t=in:st=0:d=0.25,fade=t=out:st={max(dur - 0.3, 0.3):.2f}:d=0.3"
    vf += ",format=yuv420p"
    clip = outdir / f"clip-{idx:03d}.mp4"
    subprocess.run([ff, "-y", "-i", str(img), "-vf", vf, "-frames:v", str(frames),
                    "-c:v", "libx264", "-preset", "veryfast", "-crf", "26", str(clip)],
                   check=True, capture_output=True)
    return clip


def assemble(ff: str, clips: list, out: Path) -> None:
    with tempfile.TemporaryDirectory() as td:
        concat = Path(td) / "concat.txt"
        concat.write_text("\n".join(f"file '{c.resolve()}'" for c in clips))
        subprocess.run([ff, "-y", "-f", "concat", "-safe", "0", "-i", str(concat),
                        "-c:v", "libx264", "-preset", "veryfast", "-crf", "26",
                        "-pix_fmt", "yuv420p", "-r", str(FPS), str(out)],
                       check=True, capture_output=True)


def mux_voice(ff: str, video: Path, shots: list, workdir: Path) -> float:
    """--tts openai: narrate spoken shots, pad each to its shot duration,
    concat into one track, mux. Returns cost (USD)."""
    cost, segs = 0.0, []
    for i, s in enumerate(shots):
        seg = workdir / f"aud-{i:03d}.m4a"
        if s["type"] in ("line", "vo", "action"):
            mp3 = workdir / f"vo-{i:03d}.mp3"
            cost += tts_openai(s["text"], mp3)
            subprocess.run([ff, "-y", "-i", str(mp3), "-af", "apad", "-t", f"{s['dur']:.2f}",
                            "-c:a", "aac", str(seg)], check=True, capture_output=True)
        else:
            subprocess.run([ff, "-y", "-f", "lavfi", "-i", "anullsrc=r=24000:cl=mono",
                            "-t", f"{s['dur']:.2f}", "-c:a", "aac", str(seg)],
                           check=True, capture_output=True)
        segs.append(seg)
    alist = workdir / "audio.txt"
    alist.write_text("\n".join(f"file '{a.resolve()}'" for a in segs))
    voiced = workdir / "voiced.mp4"
    subprocess.run([ff, "-y", "-i", str(video), "-f", "concat", "-safe", "0", "-i", str(alist),
                    "-c:v", "copy", "-c:a", "aac", "-shortest", str(voiced)],
                   check=True, capture_output=True)
    voiced.replace(video)
    return cost


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

    md = (node_dir / "node.md").read_text()
    node_label = f"{node['id']} · {node['title']}"
    shots = build_shots(parse_frames(extract_script(md)), node_label)
    if not shots:
        raise SystemExit(f"{node['id']}: no shots derived from script")
    total = round(sum(s["dur"] for s in shots), 1)
    leaf_id = f"{node['id']}-t2-a"

    if args.dry_run:
        print(f"would render {leaf_id}: {len(shots)} shots, ~{total}s, "
              f"tts={args.tts}, est. cost ${'0.00' if args.tts == 'none' else '~0.03'}")
        return 0

    workdir = Path(tempfile.mkdtemp(prefix="t2-"))
    page = workdir / "shots.html"
    page.write_text(shots_html(shots, node_label))
    stills = shoot_stills(page, len(shots), workdir)
    if len(stills) != len(shots):
        raise SystemExit(f"{leaf_id}: {len(stills)} stills for {len(shots)} shots")

    ff = ffmpeg_exe()
    clips = [kenburns_clip(ff, img, s["dur"], i, s["type"] == "title", workdir)
             for i, (img, s) in enumerate(zip(stills, shots))]
    out = node_dir / "leaves" / f"{leaf_id}.mp4"
    assemble(ff, clips, out)

    cost = 0.0
    if args.tts == "openai":
        cost = mux_voice(ff, out, shots, workdir)
    size_kb = out.stat().st_size // 1024

    (node_dir / "leaves" / f"{leaf_id}.yaml").write_text(f"""# Leaf metadata — every render publishes its full provenance (§7.2)
leaf: {leaf_id}
node: "{node['id']}"
tier: T2
form: animatic-mp4
content: {leaf_id}.mp4
author: pipeline/render_t2.py v2 (deterministic kinetic-text cut of the T0/T1 script)
model: {"gpt-4o-mini-tts (voice) + chromium shot cards" if args.tts == "openai" else "none — chromium shot cards, silent (type carries the script)"}
prompt: none            # deterministic — the script is the source
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

    print(f"✓ rendered {leaf_id}: {len(shots)} shots, ~{total}s, {size_kb}KB, cost ${cost:.2f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
