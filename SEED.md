# Planting a seed — how to fork the city

Guideline 5 says: take everything, rename it, go. This is the concrete checklist.
A **seed** is a new tree started from this framework, in your niche, under your
name, with your taste.

## 1. Take everything

Fork or copy this repository. All the tooling (`pipeline/`), workflows
(`.github/workflows/`), and founding structure come with you. The code is MIT;
the framework texts are CC BY 4.0 — attribution means saying where you branched
from, once, wherever you credit things.

## 2. Drop the name

The only thing a fork must leave behind is "Banyan City" (Guideline 5). Rename
the repo, rewrite the README hero in your own words. The site generator picks up
your fork's name and URLs automatically from the repository it runs in — no code
edits needed.

## 3. Extract your taste

One tree, one tending author, your rules. Run the extraction interview:

```sh
python3 pipeline/extract_taste.py --tree <your-tree-id> --author <you>
```

It records your raw answers (`taste/interviews/…`) and emits a draft taste file.
Prune the draft into 4–8 numbered rules you'd defend against your own future
self. Then close the loop: build a blind set from candidates you've blind-scored
(`taste/blindsets/README.md`) and run

```sh
python3 pipeline/author_agent.py blindset taste/blindsets/<your-set>.yaml
```

until agreement ≥ 90%. Soul as a test suite.

## 4. Write your genome

Replace (or keep, with attribution) `genomes/sapling/` with your own:

```
genomes/<your-tree-id>/
├── tree.yaml          # point taste_file at your pruned taste file
├── lineage.yaml       # one root node to start
└── nodes/<slug>/
    ├── node.md        # must contain "## State change" (R1) and "## Hook" (R5) sections
    ├── leaves/<id>.yaml
    └── sap/
```

`python3 pipeline/lint_genome.py` tells you when the structure is honest.
`python3 pipeline/render_t1.py <tree-id> --all` gives every node a free
storyboard leaf.

## 5. Open the doors

- Create one reaction issue per node; record it in `sap/reactions.yaml`
  (`channel: github_issue`, `issue: N`, `url: …`) — the daily sap harvest and the
  site pick it up from there
- Enable GitHub Pages (Settings → Pages → Source: GitHub Actions); the `pages`
  workflow deploys your tree on every push
- Optionally set a `MIRROR_GIT_URL` secret to auto-mirror your canonical layer
  to an independent host (see `.github/workflows/mirror.yml`)

## 6. Grow

You owe the city you left nothing — not notice, not linkage, not similarity.
Your guidelines may diverge; only the right to branch and fork must survive in
whatever you write, because that right is the root, and it may never be cut.
