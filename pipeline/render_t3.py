#!/usr/bin/env python3
"""T3 renderer — full-video leaves assembled from generated clips, PRD §7.4.

The generation platform (Kling, Veo, Seedance, …) supplies raw per-beat
footage; everything the platform is bad at stays deterministic post:

  beats      parsed from node.md (same beat structure as the T1 storyboard);
             each beat's target duration comes from its `— 0:00–0:12` slug
             timing, falling back to a reading-speed estimate.
  clips      --clips <dir> holds one clip per beat, named by beat number
             (`01-*.mp4`, `02-*.mp4`, …). Each clip is fitted to 9:16
             (scale + center-crop), trimmed or last-frame-padded to the
             beat's duration. A beat with no clip renders as a $0 slate —
             the episode always assembles end-to-end, footage lands later.
  overlays   the script's terminal code-fences are burned in as green
             monospace panels; VO lines appear as timed bottom captions.
             Text is rasterized by Pillow and composited with ffmpeg's
             core `overlay` filter — no freetype/drawtext build needed.
  voice      optional --tts openai narration per beat (render_t2's engine).
  assembly   per-beat encodes concatenated losslessly into <node>-t3-<sfx>.mp4.

Provenance (§7.2): clip-side `<clip>.meta.yaml` files (platform, model,
prompt, cost) are aggregated into the leaf yaml. Without --out the leaf is
published into the genome and registered in lineage.yaml; with --out it is a
bench render (pipeline development, platform trials) and touches nothing.

Deps: pyyaml, pillow, ffmpeg on PATH (any build with libx264).

Usage:
    python3 pipeline/render_t3.py <genome> <node-id> --clips <dir> [--tts openai]
    python3 pipeline/render_t3.py sapling 001 --clips /tmp/trial --out /tmp/bench.mp4
"""

import argparse
import re
import subprocess
import sys
import tempfile
from pathlib import Path

import yaml
from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, str(Path(__file__).resolve().parent))
from render_t1 import extract_script, parse_frames, strip_inline_md  # noqa: E402

REPO = Path(__file__).resolve().parent.parent
WIDTH, HEIGHT = 720, 1280
FPS = 24
MIN_SEC, MAX_SEC = 3.0, 12.0
READ_CPS = 15.0
GREEN, INK, BG = (111, 206, 138, 255), (230, 239, 232, 255), (10, 15, 11, 255)
PANEL_BG, CAPTION_BG = (10, 15, 11, 200), (0, 0, 0, 150)

MONO_FONTS = [
    "/System/Library/Fonts/Menlo.ttc",                       # macOS
    "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",   # debian/ubuntu CI
    "/usr/share/fonts/dejavu/DejaVuSansMono.ttf",
]


def mono_font(size: int) -> ImageFont.FreeTypeFont:
    for f in MONO_FONTS:
        if Path(f).exists():
            return ImageFont.truetype(f, size)
    raise SystemExit("no monospace font found — extend MONO_FONTS")


def beat_duration(slug: str, items: list) -> float:
    """`COLD OPEN — 0:00–0:12` → 12.0; otherwise estimate from text."""
    m = re.search(r"(\d+):(\d+)\s*[–—-]\s*(\d+):(\d+)", slug)
    if m:
        a, b = int(m[1]) * 60 + int(m[2]), int(m[3]) * 60 + int(m[4])
        if b > a:
            return float(b - a)
    text = " ".join(str(p) for item in items for p in item[1:])
    return min(MAX_SEC, max(MIN_SEC, len(text) / READ_CPS))


def find_clip(clips_dir: Path, num: int) -> Path | None:
    if not clips_dir:
        return None
    hits = sorted(clips_dir.glob(f"{num:02d}-*.mp4")) or sorted(clips_dir.glob(f"{num:02d}.mp4"))
    return hits[0] if hits else None


def wrap(text: str, font: ImageFont.FreeTypeFont, max_w: int) -> list:
    out = []
    for raw in text.split("\n"):
        line = ""
        for word in raw.split(" "):
            cand = f"{line} {word}".strip()
            if font.getbbox(cand)[2] <= max_w or not line:
                line = cand
            else:
                out.append(line)
                line = word
        out.append(line)
    return out


def text_png(text: str, path: Path, size: int, fg: tuple, bg: tuple,
             max_w: int = WIDTH - 100, pad: int = 18) -> Path:
    """Rasterize a text block into a tight RGBA panel."""
    font = mono_font(size)
    lines = wrap(text, font, max_w - 2 * pad)
    lh = size + 8
    w = min(max_w, max(font.getbbox(l)[2] for l in lines) + 2 * pad)
    img = Image.new("RGBA", (w, lh * len(lines) + 2 * pad), bg)
    d = ImageDraw.Draw(img)
    for i, l in enumerate(lines):
        d.text((pad, pad + i * lh), l, font=font, fill=fg)
    img.save(path)
    return path


def slate_png(slug: str, path: Path) -> Path:
    img = Image.new("RGBA", (WIDTH, HEIGHT), BG)
    d = ImageDraw.Draw(img)
    font = mono_font(30)
    lines = wrap(slug.upper(), font, WIDTH - 120)
    lh = 42
    y = HEIGHT // 2 - lh * len(lines) // 2
    for i, l in enumerate(lines):
        w = font.getbbox(l)[2]
        d.text(((WIDTH - w) // 2, y + i * lh), l, font=font, fill=GREEN)
    small = mono_font(18)
    note = "[ footage pending ]"
    d.text(((WIDTH - small.getbbox(note)[2]) // 2, y + lh * len(lines) + 30),
           note, font=small, fill=(147, 166, 152, 255))
    img.save(path)
    return path


def render_beat(beat: dict, num: int, dur: float, clip: Path, workdir: Path) -> Path:
    """Encode one beat: fitted footage (or slate) + overlays + captions."""
    inputs, chains = [], []
    if clip:
        inputs += ["-i", str(clip)]
        chains.append(
            f"[0:v]scale={WIDTH}:{HEIGHT}:force_original_aspect_ratio=increase,"
            f"crop={WIDTH}:{HEIGHT},fps={FPS},"
            f"tpad=stop_mode=clone:stop_duration={dur},"
            f"trim=duration={dur},setpts=PTS-STARTPTS[base]")
    else:
        slate = slate_png(strip_inline_md(beat["slug"]), workdir / f"slate-{num:02d}.png")
        inputs += ["-loop", "1", "-t", str(dur), "-i", str(slate)]
        chains.append(f"[0:v]fps={FPS},trim=duration={dur},setpts=PTS-STARTPTS[base]")

    layers = []  # (png, x, y, enable-expr)
    y = 100
    for j, block in enumerate([i[1] for i in beat["items"] if i[0] == "overlay"]):
        png = text_png(block, workdir / f"ovl-{num:02d}-{j}.png", 24, GREEN, PANEL_BG)
        layers.append((png, "36", str(y), f"gte(t,{dur * 0.3:.2f})"))
        y += Image.open(png).height + 24

    lines = [i[2] for i in beat["items"] if i[0] == "line"]
    if lines:
        slice_s = dur / len(lines)
        for j, text in enumerate(lines):
            png = text_png(strip_inline_md(text), workdir / f"cap-{num:02d}-{j}.png",
                           28, INK, CAPTION_BG)
            layers.append((png, "(W-w)/2", "H-h-160",
                           f"between(t,{j * slice_s:.2f},{(j + 1) * slice_s:.2f})"))

    prev = "base"
    for k, (png, x, yy, enable) in enumerate(layers):
        inputs += ["-loop", "1", "-t", str(dur), "-i", str(png)]
        nxt = f"v{k}"
        chains.append(f"[{prev}][{k + 1}:v]overlay=x={x}:y={yy}"
                      f":enable='{enable}'[{nxt}]")
        prev = nxt
    chains.append(f"[{prev}]format=yuv420p[out]")

    out = workdir / f"beat-{num:02d}.mp4"
    cmd = (["ffmpeg", "-y"] + inputs +
           ["-filter_complex", ";".join(chains), "-map", "[out]",
            "-t", str(dur), "-r", str(FPS), "-an",
            "-c:v", "libx264", "-preset", "veryfast", "-crf", "23", str(out)])
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode:
        raise SystemExit(f"beat {num} ffmpeg failed:\n{r.stderr[-1500:]}")
    return out


def clip_provenance(clip: Path) -> dict:
    meta = clip.with_suffix(".meta.yaml") if clip else None
    if meta and meta.exists():
        return yaml.safe_load(meta.read_text()) or {}
    return {}


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("genome")
    p.add_argument("node")
    p.add_argument("--clips", type=Path, default=None, help="dir of per-beat clips (01-*.mp4 …)")
    p.add_argument("--tts", choices=["none", "openai"], default="none")
    p.add_argument("--out", type=Path, default=None,
                   help="bench render: write mp4 here, publish no leaf")
    p.add_argument("--suffix", default="a", help="leaf suffix (default a)")
    args = p.parse_args()

    genome_dir = REPO / "genomes" / args.genome
    lineage_text = (genome_dir / "lineage.yaml").read_text()
    lineage = yaml.safe_load(lineage_text)
    node = next(n for n in lineage["nodes"] if n["id"] == args.node)
    node_dir = genome_dir / "nodes" / node["slug"]

    beats = parse_frames(extract_script((node_dir / "node.md").read_text()))
    if not beats:
        raise SystemExit(f"{node['id']}: no beats in script")

    workdir = Path(tempfile.mkdtemp(prefix="t3-"))
    parts, sources, missing = [], [], 0
    for i, beat in enumerate(beats, 1):
        dur = beat_duration(beat["slug"], beat["items"])
        clip = find_clip(args.clips, i)
        if not clip:
            missing += 1
        parts.append(render_beat(beat, i, dur, clip, workdir))
        prov = clip_provenance(clip)
        sources.append({"beat": i, "slug": strip_inline_md(beat["slug"]),
                        "clip": clip.name if clip else "slate (no footage yet)",
                        "platform": prov.get("platform", "none"),
                        "model": prov.get("model", "none"),
                        "cost_usd": float(prov.get("cost_usd", 0) or 0)})

    tts_cost = 0.0
    if args.tts == "openai":  # narration groundwork; muxing lands with first voiced leaf
        from render_t2 import tts_openai
        for i, beat in enumerate(beats, 1):
            text = " ".join(strip_inline_md(it[2]) for it in beat["items"] if it[0] == "line")
            if text.strip():
                tts_cost += tts_openai(text, workdir / f"vo-{i:02d}.mp3")

    leaf_id = f"{node['id']}-t3-{args.suffix}"
    out = args.out or (node_dir / "leaves" / f"{leaf_id}.mp4")
    concat = workdir / "concat.txt"
    concat.write_text("\n".join(f"file '{p.resolve()}'" for p in parts))
    r = subprocess.run(["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(concat),
                        "-c", "copy", str(out)], capture_output=True, text=True)
    if r.returncode:
        raise SystemExit(f"concat failed:\n{r.stderr[-1500:]}")

    total = sum(beat_duration(b["slug"], b["items"]) for b in beats)
    cost = round(tts_cost + sum(s["cost_usd"] for s in sources), 2)
    print(f"✓ assembled {out.name}: {len(beats)} beats ({len(beats) - missing} footage, "
          f"{missing} slate), ~{total:.0f}s, cost ${cost:.2f}")

    if args.out:
        return 0  # bench render — no leaf, no lineage

    (node_dir / "leaves" / f"{leaf_id}.yaml").write_text(
        "# Leaf metadata — every render publishes its full provenance (§7.2)\n"
        + yaml.safe_dump({
            "leaf": leaf_id, "node": node["id"], "tier": "T3", "form": "full-video-mp4",
            "content": f"{leaf_id}.mp4",
            "author": "pipeline/render_t3.py (assembly; per-beat footage sources below)",
            "model": "per-beat — see sources", "prompt": "per-beat — see sources",
            "seed": "per-beat — see sources", "cost_usd": cost,
            "status": "live", "platform_urls": [], "sources": sources,
        }, sort_keys=False))
    if leaf_id not in (node.get("leaves") or []):
        (genome_dir / "lineage.yaml").write_text(re.sub(
            rf"(- id: \"{re.escape(node['id'])}\"\n(?:.*\n)*?    leaves: \[)([^\]]*)",
            rf"\g<1>\g<2>, {leaf_id}", lineage_text, count=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
