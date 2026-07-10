# Taste file — Sapling — founder — v0.2

**Tree:** Sapling (working title, see D6)
**Author:** founder
**Version:** 0.2 — versioned by filename *and* git history; every amendment is a public diff
**Purpose:** the author's extracted decision rules. The author-agent (Phase 4) applies these rules to screened shortlists and cites rule IDs in every commit. The human amends *this file*, never individual commits.

---

## Rules

### R1 — Economy of attention
Every scene must change something: world state, a relationship, or what someone knows. Deletable without consequence = already deleted. *(Only stated absolute.)*

### R2 — No evil
Antagonism comes from conditioning, incentives, misunderstanding — never innate malice. "Just bad" characters are bugs.

### R3 — Laughter as resolution
The preferred way around conflict is exposing how ridiculous the situation is until both sides see it. Comedy is the mechanism, not the relief. Domination-victories are last resort.

### R4 — Felt, not reasoned
Narrative decisions are made by comparing rendered candidates (any tier), never abstract debate. Author inability to choose = instruction to render all options.

### R5 — Cliffhangers, yes
Episodes end on hooks; per R1 the hook must be a real state change; per R4 which hook wins is decided on material.

### R6 — Rejection is only deferral
Live candidates are never killed; they become sibling branches ordered by watering. The author's cut decides sequence and trunk, never existence. Wince test (R4) applies to moments *within* candidates, not whole candidates.

---

## How this file is used

- **Selection:** the author-agent cites rule IDs per decision, e.g. `selected leaf-3: R3 laughter-as-resolution; rejected leaf-1: violates R2`. Refusals get a one-sentence reason.
- **Validation:** this file "feels right" when it predicts the author's blind choices on unseen candidates ≥ 90% (tunable). Soul as a test suite.
- **Amendment:** every wince at a commit → interrogate the wince → rule diff, committed publicly as v0.3, v0.4, …
