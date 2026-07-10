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

## Coming (see PRD §11)

- **Phase 2** — T1/T2 render scripts (image + TTS + assembly), public render queue publishing prompt/seed/cost per candidate, simple screening UI
- **Phase 4** — the author-agent: applies the taste file to screened shortlists, opens PRs to trunk with rule-cited reasons, plus the blind-set validation harness
