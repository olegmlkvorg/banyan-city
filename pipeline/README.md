# Pipeline

All code here is MIT-licensed ([LICENSE-CODE.md](../LICENSE-CODE.md)). A fork changes content, not these scripts — they read whatever genomes exist.

## Here now

- **`lint_genome.py`** — the framework's structural rules as a test suite: unique node ids, parents declared (Guideline 1), valid statuses (Guideline 7), `## State change` (R1) and `## Hook` (R5) sections present in every T0 leaf, complete leaf provenance (§7.2), well-formed ledger. Runs in CI on every push (`.github/workflows/lint.yml`).
- **`build_site.py`** — Phase 1 static-site generator: renders every genome's `lineage.yaml` as an explorable tree with per-node pages (script, leaves audit table, sap/react links). No framework, no client JS, no external assets. Deployed to GitHub Pages on every push (`.github/workflows/pages.yml`).

Run locally:

```sh
pip install pyyaml markdown
python3 pipeline/lint_genome.py
python3 pipeline/build_site.py   # → _site/
```

- **`render_t1.py`** — Phase 2 first rung: compiles a node's T0 script into a 9:16 storyboard filmstrip leaf at $0, with full published provenance, and registers it in `lineage.yaml`. `python3 pipeline/render_t1.py sapling --all`
- **`harvest_sap.py`** — the reaction loop: pulls each node's issue reactions and screening-form ratings into `sap/summary.yaml` / `sap/screening.yaml`. Runs daily in CI (`.github/workflows/sap.yml`).
- **`author_agent.py`** — Phase 4: applies the taste file to a node's competing leaves (`select`) or scores agent-vs-author agreement on a blind set (`blindset`, the taste-fidelity harness — see [taste/blindsets/](../taste/blindsets/)). Cites rule IDs on every decision; deferrals per R6, never deletions; wince notes feed taste-file amendments. Needs `ANTHROPIC_API_KEY`; both modes support `--dry-run`.
- **`render_t2.py`** — Phase 2 second rung: compiles a node's T1 storyboard into a real 9:16 **video** — Chromium-screenshotted frames assembled by ffmpeg, with optional TTS narration (`--tts openai`, bring your own `OPENAI_API_KEY`). Silent mode is $0 and fully watchable (captions carry the script). Full provenance + cost in the leaf yaml. `python3 pipeline/render_t2.py sapling 001`
- **`extract_taste.py`** — the framework's front door (§7.3): the taste-extraction interview. Structured questions plus forced choices between rendered candidates; records the raw interview and emits a draft taste file to prune. `--answers file.yaml` for non-interactive runs; `--compile` optionally synthesizes candidate rules via the Claude API.

## Coming (see PRD §11)

- **Phase 2 rest** — paid render tiers (T2 animatic: image + TTS + assembly; T3 video) behind a published per-render budget, and the public render queue
- **Phase 4 rest** — the agent opening PRs to trunk automatically; CI wiring once a real (author-scored) blind set exists
