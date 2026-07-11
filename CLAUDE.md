# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repository is

Banyan City is an open framework for growing **story trees** — branching, AI-rendered micro-drama series curated by one human author's extracted taste. **The repo is the product**: story content, governance, reaction data, and money ledgers all live as versioned files here. The website (banyan.city / GitHub Pages) is a disposable rendering surface; git is the canonical layer.

This is not a typical software project. Most of the repo is Markdown/YAML data plus a small, deliberately boring Python pipeline (stdlib + `pyyaml` + `markdown`, no framework, no database, no client JS).

Read `PROMISE.md` first — it is canonical and everything else follows from it. `GUIDELINES.md` (the seven rules), `VOCABULARY.md` (tree/node/leaf/sap/watering…), and `PRD.md` (full design, the §-references used everywhere) are the other load-bearing docs.

## Commands

```sh
pip install pyyaml markdown          # the only dependencies

python3 pipeline/lint_genome.py      # the test suite — structural rules of the framework
python3 pipeline/build_site.py       # static site → _site/
```

Run both before pushing; CI runs both on every push (`.github/workflows/lint.yml`, `pages.yml`). There is no other test runner, linter, or build system.

Other pipeline entry points:

```sh
python3 pipeline/render_t1.py sapling <node-id|--all>   # compile T0 script → T1 storyboard leaf ($0, deterministic)
python3 pipeline/harvest_sap.py                          # pull issue reactions → sap/summary.yaml (needs GITHUB_TOKEN; runs daily in CI)
python3 pipeline/author_agent.py select <genome> <node> --dry-run   # apply taste file to competing leaves (needs ANTHROPIC_API_KEY)
python3 pipeline/author_agent.py blindset <file> --dry-run          # taste-fidelity scoring against taste/blindsets/
python3 pipeline/extract_taste.py --tree <id> --author <you>        # taste-extraction interview (--answers for non-interactive)
```

## Architecture

**Canonical data (`genomes/<tree>/`)** — one directory per story universe; forking a tree = copying its genome:

- `tree.yaml` — tree config: format, lifecycle parameters, watering split
- `lineage.yaml` — the branch graph. Every node declares `parent:` (the only obligation of a branch), `trunk: true/false` (the author-curated path), `status:` (`hot | hardened | dormant`), and its `leaves:` list. `render_t1.py` registers new leaves here via regex, preserving comments.
- `edl.md` — the edit decision log: every authorial act (trunk calls, grafts, deferrals) recorded publicly, citing taste-rule IDs
- `nodes/<id>-<slug>/` — one story beat: `node.md` (the script; doubles as the T0 text leaf), `leaves/*.yaml` (one metadata file per render, plus `.html` for T1 storyboards), `sap/` (reaction data harvested from GitHub issues)

**Taste (`taste/`)** — `sapling.founder.v0.2.md` holds the author's numbered decision rules R1–R6. These are the constitution: selections cite rule IDs, and the human amends the *file* (a public diff), never individual decisions. `blindsets/` holds the validation harness data.

**Pipeline (`pipeline/`)** — reads whatever genomes exist; a fork changes content, not scripts. `lint_genome.py` encodes the framework's structural rules as checks; `build_site.py` generates the site from lineage.

**Ledgers (`ledger/`)** — `expenses.csv` (operator spends) and `watering.csv` (citizen funding, Phase 3). Every dollar is public.

**Governance docs (root)** — `DECISIONS.md` (open/resolved decisions D1–D7), `STEWARDSHIP.md` (the founder delegated day-to-day authorship to the author-agent, operating under the founder's taste file), `OPERATOR.md` (work-order handoff channel between the steward-agent and an operator with browser/payment access).

## Hard rules the linter enforces

- Node IDs unique; every node's `parent:` declared in `lineage.yaml`; valid statuses
- Every `node.md` contains `## State change` (R1) and `## Hook` (R5) sections
- Every leaf yaml publishes complete provenance: `prompt`, `model`, `seed`, `cost_usd` (use `none`/`0.00` for human-written or deterministic renders — never omit)
- Ledger CSVs well-formed

## Conventions that are not in the linter but are binding

- **Nothing is ever deleted** (R6, Guideline 7). Story content, branches, and decisions are deferred, superseded, or marked dormant — never removed. Don't rewrite `DECISIONS.md` or `edl.md` entries; append resolutions/supersessions.
- **Authorial acts cite taste-rule IDs** (STEWARDSHIP.md §1) — in `edl.md` entries and in commit messages for trunk/graft/selection decisions. An act that can't cite a rule becomes a wince note proposing a taste-file amendment instead.
- **$0 by default**: nothing in CI may spend money. Paid render tiers run only with a contributor's own API key.
- **Forks must inherit working tooling**: no hardcoded repo names or URLs in pipeline code — derive from `GITHUB_REPOSITORY` (see `build_site.py` / `harvest_sap.py` for the pattern).
- **Data lands in the repo, not a database.** Reaction data, screening ratings, ledgers — all versioned files.
- **This repo is public; no secrets ever.** Tokens live in GitHub repo secrets (referenced by name only, e.g. `VERCEL_TOKEN`, `MIRROR_GIT_URL`). Money and account actions are human-only (STEWARDSHIP.md §4) and flow through `OPERATOR.md` work orders + `ledger/expenses.csv`.
- **Decisions reserved for citizens** (Guideline 6 amendments, D6 rename, D7 entity) are not the agent's to make.
- Steward-authored content is labeled in leaf metadata (`author:`/`model:` fields state who made it).

## Adding a branch (the most common content change)

1. Create `genomes/sapling/nodes/<id><letter>-<slug>/` with `node.md` (must include `## State change` and `## Hook`), `leaves/<id>-t0-a.yaml` (copy an existing one; text is a render), and an empty-ish `sap/`
2. Add the node to `lineage.yaml` with `parent:` declared — that line is the whole ceremony
3. Optionally `python3 pipeline/render_t1.py sapling <id>` to add the T1 storyboard leaf
4. `python3 pipeline/lint_genome.py` must pass

Sibling IDs use letter suffixes (`002a`, `002b`, `002c`); a sole continuation may be unlettered (`001`, `004`). Reaction channels: one GitHub issue per node, recorded canonically in the node's `sap/reactions.yaml`.
