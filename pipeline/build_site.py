#!/usr/bin/env python3
"""Static-site generator — Phase 1: the tree becomes visible.

Reads every genome under genomes/ and renders _site/:
    index.html                the city gate: lineage tree, explorable
    city.html                 Promise + Guidelines + Vocabulary
    <genome>/<slug>.html      one page per node: script, leaves, sap

Design constraints:
  - no build framework, no client JS required, no external assets
  - works for any genome that passes lint_genome.py (a fork changes
    content, not this script)
  - a non-git citizen can read the story and react (Phase 1 acceptance)
"""

import html
import os
import re
import shutil
from pathlib import Path

import markdown
import yaml

REPO = Path(__file__).resolve().parent.parent
OUT = REPO / "_site"
# Forkable: in CI GITHUB_REPOSITORY names the fork; locally fall back to origin
GH_REPO = os.environ.get("GITHUB_REPOSITORY", "olegmlkvorg/banyan-city")
REPO_URL = f"https://github.com/{GH_REPO}"
REPO_NAME = GH_REPO.split("/")[-1]
CANONICAL = "https://banyan.city"  # canonical host; Pages stays as free mirror
MD = markdown.Markdown(extensions=["tables", "fenced_code"])

CSS = """
:root {
  --bg: #0e1410; --panel: #151d17; --ink: #e6efe8; --muted: #93a698;
  --leaf: #6fce8a; --leaf-dim: #2e5c3d; --amber: #e8b464; --line: #263529;
  --code-bg: #0a0f0b;
}
@media (prefers-color-scheme: light) {
  :root {
    --bg: #f6f8f4; --panel: #ffffff; --ink: #1d2a20; --muted: #5b6f60;
    --leaf: #1e7a3f; --leaf-dim: #bcd9c5; --amber: #a06510; --line: #d8e2da;
    --code-bg: #eef2ec;
  }
}
* { box-sizing: border-box; }
body { margin: 0; background: var(--bg); color: var(--ink);
  font: 17px/1.65 Georgia, 'Times New Roman', serif; }
main { max-width: 720px; margin: 0 auto; padding: 2rem 1.25rem 5rem; }
a { color: var(--leaf); text-decoration: none; }
a:hover { text-decoration: underline; }
h1, h2, h3 { line-height: 1.25; font-weight: 600; }
h1 { font-size: 1.9rem; margin: 0.5rem 0; }
hr { border: 0; border-top: 1px solid var(--line); margin: 2rem 0; }
blockquote { margin: 1rem 0; padding: 0.1rem 1.1rem; border-left: 3px solid var(--leaf-dim);
  color: var(--muted); background: var(--panel); border-radius: 0 8px 8px 0; }
code, pre { font-family: ui-monospace, 'SF Mono', Menlo, Consolas, monospace; font-size: 0.85em; }
pre { background: var(--code-bg); border: 1px solid var(--line); border-radius: 8px;
  padding: 0.9rem 1.1rem; overflow-x: auto; color: var(--leaf); }
table { border-collapse: collapse; width: 100%; font-size: 0.92em; display: block; overflow-x: auto; }
th, td { border: 1px solid var(--line); padding: 0.45rem 0.7rem; text-align: left; }
th { background: var(--panel); }
.crumbs { font-size: 0.85rem; color: var(--muted); margin-bottom: 1.5rem;
  font-family: ui-monospace, Menlo, monospace; }
.chip { display: inline-block; font: 600 0.72rem/1 ui-monospace, Menlo, monospace;
  padding: 0.3rem 0.55rem; border-radius: 999px; border: 1px solid var(--line);
  color: var(--muted); vertical-align: middle; margin-right: 0.35rem; }
.chip.hot { color: var(--amber); border-color: var(--amber); }
.chip.trunk { color: var(--leaf); border-color: var(--leaf); }
.tree { list-style: none; padding-left: 0; margin: 1.5rem 0; }
.tree ul { list-style: none; padding-left: 1.4rem; border-left: 2px solid var(--leaf-dim); margin-left: 0.9rem; }
.tree li { margin: 0.8rem 0; }
.card { background: var(--panel); border: 1px solid var(--line); border-radius: 12px;
  padding: 0.9rem 1.1rem; }
.card .title { font-size: 1.1rem; font-weight: 600; }
.card .teaser { color: var(--muted); font-size: 0.92rem; margin: 0.35rem 0 0.5rem; }
.card .meta { font-size: 0.85rem; }
.hero { text-align: center; margin: 2.5rem 0 3rem; }
.hero .seal { font-size: 2.6rem; }
.hero p { color: var(--muted); max-width: 34em; margin: 0.8rem auto; }
.btn { display: inline-block; background: var(--leaf); color: var(--bg); font-weight: 700;
  padding: 0.6rem 1.2rem; border-radius: 10px; margin: 0.3rem; }
.btn:hover { text-decoration: none; opacity: 0.9; }
.btn.ghost { background: transparent; color: var(--leaf); border: 1px solid var(--leaf); }
footer { margin-top: 4rem; padding-top: 1.5rem; border-top: 1px solid var(--line);
  color: var(--muted); font-size: 0.85rem; text-align: center; }
.notice { background: var(--panel); border: 1px dashed var(--leaf-dim); border-radius: 12px;
  padding: 0.9rem 1.1rem; font-size: 0.92rem; color: var(--muted); }
"""


DEFAULT_DESC = ("Story trees that branch instead of running linear — AI-rendered "
                "micro-drama, curated by one human's taste, every decision auditable in git.")


def page(title: str, body: str, depth: int = 0, path: str = "", desc: str = "") -> str:
    root = "../" * depth
    desc = (desc or DEFAULT_DESC).strip()
    if len(desc) > 200:
        desc = desc[:197].rstrip() + "…"
    url = f"{CANONICAL}/{path}"
    og_image = f"{CANONICAL}/og.png"
    esc_t, esc_d = html.escape(title), html.escape(desc)
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="description" content="{esc_d}">
<link rel="canonical" href="{url}">
<link rel="alternate" type="application/rss+xml" title="new nodes" href="{CANONICAL}/feed.xml">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Banyan City">
<meta property="og:title" content="{esc_t}">
<meta property="og:description" content="{esc_d}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{og_image}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc_t}">
<meta name="twitter:description" content="{esc_d}">
<meta name="twitter:image" content="{og_image}">
<title>{esc_t}</title>
<style>{CSS}</style>
</head>
<body>
<main>
<nav class="crumbs"><a href="{root}index.html">🌳 {REPO_NAME}</a> · <a href="{root}city.html">the city</a> · <a href="{REPO_URL}">source</a></nav>
{body}
<footer>Everything here is auditable in <a href="{REPO_URL}">git</a>.
Branch anything. Fork everything. · <a href="{root}city.html">The Promise</a></footer>
</main>
</body>
</html>"""


def md_to_html(text: str) -> str:
    MD.reset()
    return MD.convert(text)


def strip_md(text: str) -> str:
    text = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", text)
    return re.sub(r"[*_`>#]", "", text).strip()


def extract_section(md_text: str, heading_prefix: str) -> str:
    """First paragraph under a '## <heading_prefix>…' heading."""
    m = re.search(rf"^## {re.escape(heading_prefix)}[^\n]*\n+(.+?)(?:\n\n|\n#)", md_text, re.M | re.S)
    return strip_md(m.group(1)) if m else ""


def load_genome(genome_dir: Path) -> dict:
    tree = yaml.safe_load((genome_dir / "tree.yaml").read_text())
    lineage = yaml.safe_load((genome_dir / "lineage.yaml").read_text())
    nodes = {}
    for n in lineage["nodes"]:
        node_dir = genome_dir / "nodes" / n["slug"]
        n["md"] = (node_dir / "node.md").read_text()
        n["teaser"] = extract_section(n["md"], "Hook")
        n["children"] = []
        n["leaf_meta"] = []
        for leaf_id in n.get("leaves") or []:
            f = node_dir / "leaves" / f"{leaf_id}.yaml"
            if f.exists():
                n["leaf_meta"].append(yaml.safe_load(f.read_text()))
        reactions = node_dir / "sap" / "reactions.yaml"
        n["reactions"] = yaml.safe_load(reactions.read_text()) if reactions.exists() else None
        summary = node_dir / "sap" / "summary.yaml"
        n["sap"] = yaml.safe_load(summary.read_text()) if summary.exists() else None
        screening = node_dir / "sap" / "screening.yaml"
        n["screening"] = yaml.safe_load(screening.read_text()) if screening.exists() else None
        nodes[n["id"]] = n
    for n in nodes.values():
        if n.get("parent"):
            nodes[n["parent"]]["children"].append(n)
    roots = [n for n in nodes.values() if not n.get("parent")]
    return {"tree": tree["tree"], "config": tree, "nodes": nodes, "roots": roots, "dir": genome_dir}


def chips(n: dict) -> str:
    out = f'<span class="chip">{html.escape(n["id"])}</span>'
    if n.get("trunk"):
        out += '<span class="chip trunk">trunk</span>'
    out += f'<span class="chip {html.escape(n["status"])}">{html.escape(n["status"])}</span>'
    return out


def node_card(genome_id: str, n: dict, depth: int) -> str:
    teaser = f'<div class="teaser">{html.escape((n["teaser"][:160] + "…") if len(n["teaser"]) > 160 else n["teaser"])}</div>' if n["teaser"] else ""
    react = f' · <a href="{html.escape(n["reactions"]["url"])}">💧 react</a>' if n.get("reactions") else ""
    kids = ""
    if n["children"]:
        kids = "<ul>" + "".join(node_card(genome_id, c, depth) for c in n["children"]) + "</ul>"
    return f"""<li><div class="card">
{chips(n)}
<div class="title"><a href="{genome_id}/{html.escape(n['slug'])}.html">{html.escape(n['title'])}</a></div>
{teaser}
<div class="meta">{len(n['leaf_meta'])} {'leaf' if len(n['leaf_meta']) == 1 else 'leaves'} · <a href="{genome_id}/{html.escape(n['slug'])}.html">read</a>{react}</div>
</div>{kids}</li>"""


def render_node_page(g: dict, n: dict) -> str:
    genome_id = g["tree"]["id"]
    body_html = md_to_html(n["md"])
    # rewrite sibling links (../<slug>/node.md) to site pages
    body_html = re.sub(r'href="\.\./([^/"]+)/node\.md"', r'href="\1.html"', body_html)

    def leaf_cell(l):
        content = str(l.get("content", ""))
        if content.endswith(".html"):
            return f'<a href="leaves/{html.escape(content)}"><code>{html.escape(str(l["leaf"]))}</code></a>'
        return f'<code>{html.escape(str(l["leaf"]))}</code>'

    def screen_cell(l):
        leaf_id = str(l["leaf"])
        means = ""
        sc = (n.get("screening") or {}).get("leaves", {}).get(leaf_id)
        if sc:
            avg = " ".join(f"{k[:4]} {v}" for k, v in sc["means"].items())
            means = f'<span class="chip">{html.escape(avg)} ({sc["ratings"]}×)</span> '
        url = f"{REPO_URL}/issues/new?template=screening.yml&title=screening%3A%20{leaf_id}&leaf={leaf_id}"
        return f'{means}<a href="{url}">rate</a>'

    leaves_rows = "".join(
        f"<tr><td>{leaf_cell(l)}</td><td>{html.escape(str(l['tier']))}</td>"
        f"<td>{html.escape(str(l['form']))}</td><td>${l['cost_usd']:.2f}</td>"
        f"<td>{html.escape(str(l['status']))}</td><td>{screen_cell(l)}</td></tr>"
        for l in n["leaf_meta"]
    )
    vids = [l for l in n["leaf_meta"]
            if str(l.get("content", "")).endswith(".mp4") and l.get("status") == "live"]
    vids.sort(key=lambda l: str(l.get("tier")), reverse=True)  # highest tier first
    players = "".join(
        f'<figure style="display:inline-block;margin:0.4rem 0.6rem 0.4rem 0">'
        f'<video controls playsinline preload="metadata" style="width:100%;max-width:360px;border-radius:12px;border:1px solid var(--line)" '
        f'src="leaves/{html.escape(str(l["content"]))}"></video>'
        f'<figcaption class="chip">{html.escape(str(l["tier"]))} · {html.escape(str(l["form"]))}</figcaption></figure>'
        for l in vids)
    player_html = f"<h2>Watch</h2>{players}" if players else ""
    leaves_html = f"""{player_html}<h2>Leaves (renders of this node)</h2>
<table><tr><th>leaf</th><th>tier</th><th>form</th><th>cost</th><th>status</th><th>screening</th></tr>{leaves_rows}</table>
<p class="notice">Every render publishes its prompt, model, seed, and cost — this table is the audit trail.
<strong>Screening:</strong> rate any leaf (continuity, character, vibe) — the crowd narrows the shortlist,
the taste file decides. Ratings are harvested into this node's <code>sap/screening.yaml</code>.
Higher-tier leaves (animatic, video) arrive with a published per-render budget.</p>"""

    react_html = ""
    if n.get("reactions"):
        vitals = ""
        if n.get("sap"):
            s = n["sap"]
            emoji = {"+1": "👍", "-1": "👎", "laugh": "😄", "confused": "😕", "heart": "❤️", "hooray": "🎉", "rocket": "🚀", "eyes": "👀"}
            counts = " ".join(f"{emoji[k]} {v}" for k, v in s["reactions"].items() if v) or "no reactions yet — be the first drop"
            vitals = f"""<p><span class="chip">{counts}</span> <span class="chip">💬 {s['comments']} comments</span>
<span class="chip">harvested {html.escape(str(s['harvested_at'])[:10])}</span></p>"""
        react_html = f"""<h2>Sap (your reactions)</h2>
{vitals}
<p><a class="btn" href="{html.escape(n['reactions']['url'])}">💧 React / comment on this node</a></p>
<p class="notice">Reactions are open data (Guideline 4): they order this branch against its siblings.
Harvested daily into this node's <code>sap/summary.yaml</code> by CI.
No account? Just tell someone about it — word of mouth is sap too.</p>"""

    kids = ""
    if n["children"]:
        links = " · ".join(f'<a href="{html.escape(c["slug"])}.html">{html.escape(c["id"])} — {html.escape(c["title"])}</a>' for c in n["children"])
        kids = f"<p><strong>Continues as:</strong> {links}</p>"
    parent_link = ""
    if n.get("parent"):
        p = g["nodes"][n["parent"]]
        parent_link = f'<p><strong>Parent:</strong> <a href="{html.escape(p["slug"])}.html">{html.escape(p["id"])} — {html.escape(p["title"])}</a></p>'

    body = f"""<p>{chips(n)}</p>
{body_html}
<hr>
{parent_link}{kids}
{leaves_html}
{react_html}
<h2>Branch this node</h2>
<p class="notice">Anyone may continue this moment differently. Declare <code>{html.escape(n['id'])}</code> as your parent —
that's the only obligation. <a href="{REPO_URL}#how-to-branch-a-story">How to branch →</a></p>"""
    return page(f"{n['id']} — {n['title']} · {g['tree']['title']}", body, depth=1,
                path=f"{g['tree']['id']}/{n['slug']}.html", desc=n.get("teaser") or "")


def render_index(genomes: list) -> str:
    sections = []
    for g in genomes:
        t = g["tree"]
        tree_html = "<ul class='tree'>" + "".join(node_card(t["id"], r, 0) for r in g["roots"]) + "</ul>"
        n_nodes = len(g["nodes"])
        n_leaves = sum(len(n["leaf_meta"]) for n in g["nodes"].values())
        sections.append(f"""<h2>🌱 {html.escape(t['title'])} <span class="chip">{n_nodes} nodes</span> <span class="chip">{n_leaves} leaves</span></h2>
<p class="notice">An engineer dies debugging production at 3 a.m. and reincarnates as a banyan sapling.
He can't move, fight, or flee — only sense, grow, and make the space around him worth staying in.
After node 001 the story <em>branches</em>: three continuations of the same moment, all alive, none rejected.
Read them; react; the sap decides what runs hot.</p>
{tree_html}""")

    body = f"""<div class="hero">
<div class="seal">🌳</div>
<h1>Banyan City</h1>
<p>Story trees that branch instead of running linear — AI-rendered micro-drama,
curated by one human's extracted taste, screened and funded by the citizens watching,
every decision auditable in git.</p>
<a class="btn" href="sapling/001-capability-inventory.html">▶ Watch node 001</a>
<a class="btn ghost" href="city.html">Read the Promise</a>
</div>
{''.join(sections)}
<hr>
<h2>The rules of this place, in one breath</h2>
<p>Anyone may <strong>branch</strong> any episode (declare your parent — the only obligation).
Citizens <strong>water</strong> the branches they love; unwatered branches sleep, never die.
One author's <strong>taste file</strong> decides the trunk; disagreement is watering a rival branch, not a vote.
All reactions and money are <strong>open data</strong>. And anyone may <strong>fork the whole city</strong> —
take everything, rename it, go. <a href="city.html">Full text →</a></p>
<p class="notice">🎬 <strong>Now growing:</strong> the tree is choosing its video model —
same three shots rendered on every candidate platform, scored in the open.
<a href="trials/index.html">The T3 platform trials →</a></p>"""
    return page("Banyan City — a story tree", body)


def render_city() -> str:
    parts = []
    for fname, title in [("PROMISE.md", None), ("GUIDELINES.md", None), ("VOCABULARY.md", None)]:
        parts.append(md_to_html((REPO / fname).read_text()))
        parts.append("<hr>")
    body = "".join(parts[:-1]) + f"""
<p class="notice">These texts are canonical and live in
<a href="{REPO_URL}">the repository</a> — amendable by citizens
per Guideline 6, except the right to branch and fork, which is permanent.
Open questions live in <a href="{REPO_URL}/blob/HEAD/DECISIONS.md">DECISIONS.md</a>.</p>"""
    return page("The City — Promise, Guidelines, Vocabulary", body, path="city.html")


AXES = ["adherence", "motion", "look", "nativeness", "consistency", "friction"]
WEIGHTED = {"adherence": 2, "consistency": 2}


def render_trials() -> str:
    """Public T3 platform-trials page: same three shots on every candidate,
    outputs + provenance + scores, all open data (§7.2)."""
    tdir = REPO / "pipeline" / "t3-trials"
    scores = (yaml.safe_load((tdir / "scores.yaml").read_text()) or {}).get("platforms") or {}

    outputs = {}
    outdir = tdir / "outputs"
    if outdir.exists():
        for pdir in sorted(p for p in outdir.iterdir() if p.is_dir()):
            clips = []
            for mp4 in sorted(pdir.glob("*.mp4")):
                meta_f = mp4.with_suffix(".meta.yaml")
                meta = yaml.safe_load(meta_f.read_text()) if meta_f.exists() else {}
                clips.append((mp4, meta or {}))
            if clips:
                outputs[pdir.name] = clips

    sections = []
    for plat in sorted(set(outputs) | set(scores)):
        rows, players = "", ""
        for mp4, meta in outputs.get(plat, []):
            players += (f'<figure style="display:inline-block;margin:0.5rem 0.6rem 0.5rem 0">'
                        f'<video controls playsinline preload="metadata" '
                        f'style="width:100%;max-width:300px;border-radius:12px;border:1px solid var(--line)" '
                        f'src="{html.escape(plat)}/{html.escape(mp4.name)}"></video>'
                        f'<figcaption class="chip">shot {html.escape(str(meta.get("shot", mp4.stem)))} · '
                        f'{html.escape(str(meta.get("model", "model?")))}</figcaption></figure>')
        shot_scores = (scores.get(plat) or {}).get("shots") or {}
        for shot, ax in sorted(shot_scores.items()):
            ax = ax or {}
            filled = [(a, ax[a]) for a in AXES if isinstance(ax.get(a), (int, float))]
            if filled:
                num = sum(v * WEIGHTED.get(a, 1) for a, v in filled)
                den = sum(WEIGHTED.get(a, 1) for a, _ in filled)
                total = f"{num / den:.1f}"
            else:
                total = "—"
            cells = "".join(f"<td>{ax.get(a) if ax.get(a) is not None else '·'}</td>" for a in AXES)
            note = html.escape(str(ax.get("notes", "") or ""))
            rows += f"<tr><td><strong>{html.escape(shot)}</strong></td>{cells}<td><strong>{total}</strong></td><td>{note}</td></tr>"
        table = (f"<table><tr><th>shot</th>{''.join(f'<th>{a}</th>' for a in AXES)}<th>weighted</th><th>notes</th></tr>"
                 f"{rows}</table>") if rows else '<p class="notice">Not scored yet.</p>'
        model = html.escape(str((scores.get(plat) or {}).get("model", "")))
        sections.append(f"<h2>{html.escape(plat)} <span class='chip'>{model}</span></h2>{players}{table}")

    if not sections:
        sections.append('<p class="notice">No trial outputs yet — the founder is out gathering free-tier '
                        'renders. The protocol, prompts, and rubric below are already fixed, so results '
                        'can\'t be quietly re-rolled until they flatter.</p>')

    intro = md_to_html((tdir / "README.md").read_text())
    prompts = md_to_html((tdir / "prompts.md").read_text())
    body = (f"{''.join(sections)}<hr><details><summary><strong>Protocol, candidates & rubric</strong></summary>"
            f"{intro}</details><details><summary><strong>The three prompts</strong></summary>{prompts}</details>")
    return page("T3 platform trials — same three shots, every model", body, depth=1,
                path="trials/index.html",
                desc="Choosing Banyan City's video model in the open: the same three shots "
                     "rendered on each candidate platform, scored on a fixed rubric.")


def render_feed(genomes: list) -> str:
    """RSS 2.0 of nodes, newest release first (dates from lineage `released`)."""
    items = []
    for g in genomes:
        gid = g["tree"]["id"]
        for n in g["nodes"].values():
            date = str(n.get("released", ""))
            url = f"{CANONICAL}/{gid}/{n['slug']}.html"
            desc = html.escape(n["teaser"] or n["title"])
            items.append((date, f"""  <item>
    <title>{html.escape(n['id'])} — {html.escape(n['title'])}</title>
    <link>{url}</link>
    <guid isPermaLink="true">{url}</guid>
    <pubDate>{date}T12:00:00Z</pubDate>
    <description>{desc}</description>
  </item>"""))
    items.sort(key=lambda t: t[0], reverse=True)
    body = "\n".join(i for _, i in items)
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
<channel>
  <title>Banyan City — new nodes</title>
  <link>{CANONICAL}/</link>
  <description>New story nodes on the tree: trunk and branches alike.</description>
{body}
</channel>
</rss>
"""


def main() -> None:
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir()
    genomes = [load_genome(p) for p in sorted((REPO / "genomes").iterdir()) if p.is_dir()]

    (OUT / "index.html").write_text(render_index(genomes))
    (OUT / "city.html").write_text(render_city())
    (OUT / "feed.xml").write_text(render_feed(genomes))
    (OUT / ".nojekyll").write_text("")
    og = REPO / "assets" / "og.png"          # social-share image referenced by page() meta
    if og.exists():
        shutil.copy(og, OUT / "og.png")
    (OUT / "trials").mkdir()
    (OUT / "trials" / "index.html").write_text(render_trials())
    trials_out = REPO / "pipeline" / "t3-trials" / "outputs"
    if trials_out.exists():
        for mp4 in trials_out.glob("*/*.mp4"):
            (OUT / "trials" / mp4.parent.name).mkdir(exist_ok=True)
            shutil.copy(mp4, OUT / "trials" / mp4.parent.name / mp4.name)
    for g in genomes:
        gdir = OUT / g["tree"]["id"]
        gdir.mkdir()
        for n in g["nodes"].values():
            (gdir / f"{n['slug']}.html").write_text(render_node_page(g, n))
            # publish renderable leaf artifacts (html storyboards, animatics…)
            for l in n["leaf_meta"]:
                content = str(l.get("content", ""))
                if content.endswith((".html", ".mp4")):
                    src = g["dir"] / "nodes" / n["slug"] / "leaves" / content
                    if src.exists():
                        (gdir / "leaves").mkdir(exist_ok=True)
                        shutil.copy(src, gdir / "leaves" / content)

    total = sum(len(g["nodes"]) for g in genomes)
    print(f"✓ built _site/ — {len(genomes)} genome(s), {total} node pages")


if __name__ == "__main__":
    main()
