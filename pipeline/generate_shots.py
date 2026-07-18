#!/usr/bin/env python3
"""Shot generator — programmatic footage for a node's shot list, PRD §7.4.

Reads a node's `shots.md` (one generation prompt per beat), calls a video-gen
provider for every beat that doesn't have a clip yet, polls to completion,
downloads the result, and writes `NN-slug.mp4` + `NN-slug.meta.yaml` into a
clips dir — exactly the layout `render_t3.py --clips` assembles. This replaces
pasting prompts into platform websites: the manual path was for the free-tier
bake-off (see pipeline/t3-trials/); production renders are API-driven.

Providers (adapter per vendor; pick with --provider):
  kling   official agent CLI (`@klingai/cli-global`) — already OAuth'd on this
          machine; draws on paid agent credits (kling.ai membership-agent).
  veo     Google Gemini API (Veo) — needs GEMINI_API_KEY.
  fal     fal.ai aggregator (Kling/Seedance/Hailuo/…) — needs FAL_KEY;
          model chosen with --model.

Every clip's meta.yaml records platform, model, verbatim prompt, cost estimate,
and date (§7.2 — publish everything). Costs are estimates until the vendor bill
lands; the ledger reconciles.

Usage:
    python3 pipeline/generate_shots.py sapling 001 --provider kling --clips-dir /tmp/ep001
    python3 pipeline/generate_shots.py sapling 001 --provider veo --beats 03,05
    python3 pipeline/generate_shots.py sapling 001 --provider fal --model kling-video/v2.5-turbo/pro
"""

import argparse
import json
import os
import re
import subprocess
import sys
import time
import urllib.request
from datetime import date
from pathlib import Path

import yaml

REPO = Path(__file__).resolve().parent.parent
DEFAULT_DURATION = 10  # seconds per shot; beats are fitted by render_t3 anyway


# ---------------------------------------------------------------- shot list --

def parse_shots(shots_md: str) -> list:
    """`## Beat NN — TITLE ... ```prompt``` ` → [{num, slug, prompt, done}]"""
    shots = []
    for m in re.finditer(
            r"^## Beat (\d+) — ([^\n]*?)(✅[^\n]*|⬜[^\n]*)?$\n(.*?)```\n(.*?)```",
            shots_md, re.M | re.S):
        num, title, status = int(m.group(1)), m.group(2).strip(), (m.group(3) or "")
        slug = re.sub(r"[^a-z0-9]+", "-", title.split("(")[0].lower()).strip("-")
        shots.append({"num": num, "slug": slug or f"beat{num}",
                      "prompt": " ".join(m.group(5).split()),
                      "done": "✅" in status})
    return shots


# ---------------------------------------------------------------- providers --

def gen_kling(prompt: str, model: str, dur: int) -> tuple:
    """Official agent CLI (OAuth'd; paid agent credits). Returns (url, meta)."""
    model = model or "kling-video-v2_5"
    r = subprocess.run(
        ["kling", "text_to_video", "--model", model, "--duration", str(dur),
         "--aspect_ratio", "9:16", "--resolution", "720p", "--enable_audio", "false",
         "--poll", "600", prompt],
        capture_output=True, text=True, timeout=700)
    out = r.stdout + r.stderr
    if "Insufficient credits" in out:
        raise SystemExit("kling: agent credit balance is empty — top up at "
                         "https://kling.ai/h5-app/membership-agent (founder action)")
    urls = re.findall(r"https?://[^\s\"']+\.mp4[^\s\"']*", out)
    if not urls:
        raise RuntimeError(f"kling: no video URL in output:\n{out[-800:]}")
    return urls[-1], {"platform": "kling", "model": model, "cost_note": "agent credits; see kling.ai billing"}


def gen_veo(prompt: str, model: str, dur: int) -> tuple:
    """Google Gemini API — Veo long-running generation. Needs GEMINI_API_KEY.
    Veo natively supports 4/6/8s only (verified 2026-07: ai.google.dev/gemini-api/docs/veo);
    render_t3 clone-pads short clips to the beat length, so 8s is the right ask."""
    key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if not key:
        raise SystemExit("veo: set GEMINI_API_KEY (aistudio.google.com/apikey)")
    dur = max(4, min(8, dur if dur in (4, 6, 8) else 8))
    model = model or "veo-3.1-fast-generate-preview"  # $0.10/s 720p — the value tier
    base = "https://generativelanguage.googleapis.com/v1beta"
    req = urllib.request.Request(
        f"{base}/models/{model}:predictLongRunning",
        data=json.dumps({
            "instances": [{"prompt": prompt}],
            "parameters": {"aspectRatio": "9:16", "durationSeconds": dur},
        }).encode(),
        headers={"x-goog-api-key": key, "Content-Type": "application/json"})
    with urllib.request.urlopen(req) as r:
        op = json.load(r)["name"]
    for _ in range(120):  # poll up to ~10 min
        time.sleep(5)
        pr = urllib.request.Request(f"{base}/{op}", headers={"x-goog-api-key": key})
        with urllib.request.urlopen(pr) as r:
            st = json.load(r)
        if st.get("done"):
            if "error" in st:
                raise RuntimeError(f"veo: {st['error']}")
            vids = st["response"]["generateVideoResponse"]["generatedSamples"]
            return vids[0]["video"]["uri"] + f"&key={key}", {
                "platform": "google-veo-api", "model": model,
                "cost_note": "per-second API billing; see ai.google.dev/pricing"}
    raise RuntimeError("veo: generation timed out")


def gen_fal(prompt: str, model: str, dur: int) -> tuple:
    """fal.ai aggregator queue API. Needs FAL_KEY; --model picks the hosted model."""
    key = os.environ.get("FAL_KEY")
    if not key:
        raise SystemExit("fal: set FAL_KEY (fal.ai/dashboard/keys)")
    # verified fal endpoints + $/10s 720p 9:16 (2026-07-18, fal model pages):
    #   fal-ai/kling-video/v3/turbo/standard/text-to-video   $1.12 (native audio)
    #   fal-ai/minimax/hailuo-2.3/standard/text-to-video     $0.56
    #   bytedance/seedance-2.0/text-to-video                 $3.03 (w/audio)
    #   fal-ai/veo3.1/fast                                   $1.20 per 8s (no visible watermark)
    model = model or "fal-ai/kling-video/v3/turbo/standard/text-to-video"
    if not model.startswith("fal-ai/"):
        model = f"fal-ai/{model}"
    req = urllib.request.Request(
        f"https://queue.fal.run/{model}",
        data=json.dumps({"prompt": prompt, "aspect_ratio": "9:16",
                         "duration": str(dur)}).encode(),
        headers={"Authorization": f"Key {key}", "Content-Type": "application/json"})
    with urllib.request.urlopen(req) as r:
        sub = json.load(r)
    status_url, resp_url = sub["status_url"], sub["response_url"]
    for _ in range(120):
        time.sleep(5)
        sr = urllib.request.Request(status_url, headers={"Authorization": f"Key {key}"})
        with urllib.request.urlopen(sr) as r:
            st = json.load(r)
        if st["status"] == "COMPLETED":
            rr = urllib.request.Request(resp_url, headers={"Authorization": f"Key {key}"})
            with urllib.request.urlopen(rr) as r:
                res = json.load(r)
            url = (res.get("video") or {}).get("url") or res["videos"][0]["url"]
            return url, {"platform": "fal.ai", "model": model,
                         "cost_note": "per-run billing; see fal.ai model page"}
        if st["status"] in ("FAILED", "ERROR"):
            raise RuntimeError(f"fal: {st}")
    raise RuntimeError("fal: generation timed out")


PROVIDERS = {"kling": gen_kling, "veo": gen_veo, "fal": gen_fal}


# --------------------------------------------------------------------- main --

def download(url: str, dest: Path) -> None:
    with urllib.request.urlopen(url) as r, open(dest, "wb") as f:
        f.write(r.read())


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("genome")
    p.add_argument("node")
    p.add_argument("--provider", choices=sorted(PROVIDERS), required=True)
    p.add_argument("--model", default=None, help="provider-specific model override")
    p.add_argument("--beats", default=None, help="comma list, e.g. 03,05 (default: all beats without a clip)")
    p.add_argument("--clips-dir", type=Path, default=None,
                   help="where clips land (default: <node>/clips/)")
    p.add_argument("--duration", type=int, default=DEFAULT_DURATION)
    p.add_argument("--dry-run", action="store_true")
    args = p.parse_args()

    genome_dir = REPO / "genomes" / args.genome
    lineage = yaml.safe_load((genome_dir / "lineage.yaml").read_text())
    node = next(n for n in lineage["nodes"] if n["id"] == args.node)
    node_dir = genome_dir / "nodes" / node["slug"]
    shots_file = node_dir / "shots.md"
    if not shots_file.exists():
        raise SystemExit(f"{node['id']}: no shots.md — write the per-beat prompt list first")

    clips_dir = args.clips_dir or (node_dir / "clips")
    clips_dir.mkdir(parents=True, exist_ok=True)
    shots = parse_shots(shots_file.read_text())
    wanted = ({int(b) for b in args.beats.split(",")} if args.beats else None)

    todo = []
    for s in shots:
        if wanted is not None and s["num"] not in wanted:
            continue
        existing = list(clips_dir.glob(f"{s['num']:02d}-*.mp4"))
        if existing and wanted is None:
            continue  # already have footage; explicit --beats regenerates
        todo.append(s)
    if not todo:
        print("nothing to generate — every requested beat already has a clip")
        return 0

    print(f"{node['id']}: {len(todo)} shot(s) via {args.provider}"
          + (f" [{args.model}]" if args.model else ""))
    if args.dry_run:
        for s in todo:
            print(f"  would generate beat {s['num']:02d} ({s['slug']}): {s['prompt'][:70]}…")
        return 0

    gen = PROVIDERS[args.provider]
    for s in todo:
        print(f"  beat {s['num']:02d} ({s['slug']}) … ", end="", flush=True)
        url, meta = gen(s["prompt"], args.model, args.duration)
        dest = clips_dir / f"{s['num']:02d}-{s['slug']}.mp4"
        download(url, dest)
        dest.with_suffix(".meta.yaml").write_text(
            "# Shot provenance (§7.2)\n" + yaml.safe_dump({
                **meta, "shot_beat": s["num"], "prompt": s["prompt"],
                "duration_s": args.duration, "aspect": "9:16",
                "date": date.today().isoformat(),
            }, sort_keys=False, allow_unicode=True))
        print(f"✓ {dest.name} ({dest.stat().st_size // 1024}KB)")

    print(f"\nnext: python3 pipeline/render_t3.py {args.genome} {args.node} "
          f"--clips {clips_dir} --out /tmp/{args.node}-episode.mp4")
    return 0


if __name__ == "__main__":
    sys.exit(main())
