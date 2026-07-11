# Contributing

There are four ways to contribute to a tree, in ascending order of commitment.
None requires permission.

## React (10 seconds)

Every node has a reaction issue — 👍/❤️/😄 or a comment. That's sap
(Guideline 4): open data, harvested daily into the node's `sap/summary.yaml`,
and it genuinely orders sibling branches.

## Screen (2 minutes)

Rate any leaf with the [🔍 Screen a leaf](../../issues/new?template=screening.yml)
form — continuity, character, vibe, and optionally the *wince*: the specific
moment that landed or broke. Screening narrows; the taste file decides.
Ratings land in the node's `sap/screening.yaml`.

## Branch (an evening)

Continue any node differently. **No git knowledge needed:** use the
[🌿 Submit a branch](../../issues/new?template=branch-submission.yml) form —
paste your story, name your parent node, and the steward files it as a real
branch credited to you on the next tending pass.

If you're comfortable with git, the full walkthrough is in the
[README](README.md#how-to-branch-a-story); the contract for a branch PR is:

- [ ] node directory under `genomes/<tree>/nodes/<id>-<slug>/` with `node.md`,
      `leaves/`, `sap/`
- [ ] `node.md` contains `## State change` (R1) and `## Hook` (R5) sections —
      the linter enforces this
- [ ] a leaf metadata yaml for the T0 leaf (copy any existing one; text is a render)
- [ ] your node added to `lineage.yaml` with `parent:` declared — the only
      real obligation (Guideline 1)
- [ ] `python3 pipeline/lint_genome.py` passes

Branches may contradict, subvert, or outgrow their parent. Nobody will police
direction — only lineage. A branch that isn't merged here can live in your fork;
it is no less real there.

## Build (ongoing)

The pipeline is small, deliberately boring Python (see `pipeline/README.md`).
Ground rules:

- $0 by default: nothing in CI may spend money; paid render tiers run only with
  a contributor's own API key (compute-as-watering, see [WATERING.md](WATERING.md))
- Everything auditable: renders publish prompt/model/seed/cost; decisions cite
  taste-rule IDs; data lands in the repo, not a database
- A fork must inherit working tooling: no hardcoded repo names or URLs — derive
  from `GITHUB_REPOSITORY` (see `build_site.py` / `harvest_sap.py` for the pattern)
- Run `python3 pipeline/lint_genome.py` and `python3 pipeline/build_site.py`
  before pushing; CI runs both

## What doesn't happen here

- Votes to override the author — disagreement is watering a rival branch
  (Guideline 3)
- Deleting story content — candidates are deferred, never killed (R6)
- Takedowns of forks — a fork is how the forest spreads (Guideline 5)
