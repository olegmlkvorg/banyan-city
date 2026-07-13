# Open Decisions

The city's unresolved questions, logged in the open. Decisions are made per
**Guideline 6** (open proposal, visible support), except where the Promise
reserves them to the tending author's taste — exercised since 2026-07-11 by the
delegated steward under the founder's taste file (see [STEWARDSHIP.md](STEWARDSHIP.md)).
A closed decision is never edited away — it gets a resolution entry and stays
here as history. Any resolution below is amendable the same way it was made.

**Status legend:** `open` · `leaning` · `resolved (date, by, how)`

---

## D1 — Content license

**Question:** CC BY 4.0 vs CC0 + cultural credit norm for all story content.
**Status:** **resolved** (2026-07-11, steward) — **CC BY 4.0**, as applied in
`LICENSE-CONTENT.md`. Attribution = "declare your parent" maps 1:1 onto
Guideline 1, giving lineage a legal floor at zero enforcement cost. CC0+norms
remains a valid amendment proposal for citizens who find even that floor too heavy.

## D2 — Code license

**Question:** MIT vs AGPL for all pipeline/tooling code.
**Status:** **resolved** (2026-07-11, steward) — **MIT**, as applied in
`LICENSE-CODE.md`. Guideline 5 says take everything and go, no strings; AGPL's
strings, however well-meant, contradict the founding text.

## D3 — Screening vote weight

**Question:** one-citizen-one-vote vs watering-weighted vs hybrid, for the screening (narrowing) stage.
**Status:** **resolved** (2026-07-11, steward) — **one-citizen-one-vote**.
Screening only *narrows* (§2); the taste file decides; watering already has its
own lever (ordering branches, Guideline 2). Weighting the narrowing stage by
money would double-count wealth and add nothing the ledger doesn't already do.
Revisit if screening volume ever makes manipulation a real cost.

## D4 — Lifecycle defaults for *Sapling*

**Question:** hot duration and hardening threshold values in `genomes/sapling/tree.yaml`.
**Status:** **resolved** (2026-07-11, steward) — set in `tree.yaml`:
`hot_duration_days: 45`; hardening threshold: a leading leaf holds **≥60% of the
node's sap for 14 consecutive days with ≥25 total reactions**; `dormancy_season_days: 90`.
Values chosen to be slow enough that early, tiny audiences can't accidentally
harden a node, and concrete enough to be machine-checkable once sap volume exists.
First-contact with reality expected to amend them.

## D5 — Watering split defaults

**Question:** default percentages for author share / generation costs / city commons.
**Status:** **resolved** (2026-07-11, steward) — **costs first, then 70/30**:
each watered render reimburses its *actual published generation cost* first;
the remainder splits **70% author / 30% city commons**. Published per-row in
the ledger as `split_applied: costs-first-70-30-v1`. Rationale: citizens water
*renders*, so the render must be made whole before anyone profits; the commons
share funds infrastructure citizens can inspect. Set in `tree.yaml`; amendable
per Guideline 6; must be re-confirmed by the founder before the first real
funds land (money rails are human — STEWARDSHIP.md §4).

## D6 — Genome rename

**Question:** does *Sapling* keep its working title?
**Status:** open — **reserved for citizens.** Naming threads live in the
reaction issues (see #6, where the story is asking itself the same question).

## D7 — Stewarding entity

**Question:** when (if ever) do citizens form a foundation/co-op to defend the name and fund the commons?
**Status:** explicitly deferred to citizens per the Promise. Neither founder
nor steward will create one.

## D8 — First T3 render platform

**Question:** which video model renders the first paid T3 leaves (PRD §7.4)?
**Status:** **leaning — Veo 3.1 (Google Flow), pending a real comparison and the founder's taste read.**
Evidence so far (all public, [banyan.city/trials](https://banyan.city/trials)):

- **Veo 3.1 / Google Flow** rendered all three node-001 trial shots (A cold-open,
  B leaf-POV, C underground) at native 9:16, 10s. Steward objective read: 5/5
  prompt adherence on all three, 5/5 vertical framing. Friction 3/5 — free tier
  is ~2 gens/day, 720p cap, and a sparkle watermark.
- No other platform tested yet, so this is a bar, not a winner. A choice needs
  at least one rival run of the same three shots (Kling, Dreamina/Seedance, or
  Hailuo) — otherwise "best" is untested.

**Two things this decision waits on, both founder-reserved:**
1. **Taste axes** (motion / look / consistency) are unscored — R4 reserves them
   to the author; the objective 4.5 is only half the rubric.
2. **Spend.** The free tier is watermarked and rate-limited; a production leaf
   likely needs paid credits — a money decision (STEWARDSHIP §4, human rails).

**Steward recommendation:** run the same three prompts on one or two rivals
(cost: the founder's time on their sites — steward holds no accounts), let the
founder score taste, then resolve here. If no rival clears Veo on taste, Veo
wins by default. Amendable per Guideline 6.

## D9 — When is a node's T3 video leaf publishable?

**Question:** what must be true before an assembled T3 episode becomes a node's
official `live` leaf (not just a Desktop/bench preview)?
**Status:** open — **draft criteria below, for the founder to ratify or amend.**
Prompted by the first real case: the node-001 Veo episode assembles end-to-end
but (a) carries the Flow watermark and (b) has 2 of 5 beats as placeholder
slates. Steward read: **not yet** — publish criteria, proposed:

1. **Footage complete or intentionally slated** — every beat has real footage,
   or a slate is a deliberate stylistic choice noted in the leaf metadata (not
   just "not generated yet").
2. **Watermark policy** — either watermark-free, or the founder explicitly
   accepts the platform mark as the price of the free tier for this leaf.
3. **Provenance complete** (§7.2) — per-beat platform/model/prompt/cost recorded
   in the leaf yaml (render_t3 already aggregates this).
4. **Taste-blessed** — the author has seen the assembled episode and approved it
   as the node's representative video (R4; trunk-root nodes especially).
5. **Lint + CI green**, leaf registered in `lineage.yaml`.

Publishing is a `render`, within steward authority once criteria are met — but
criterion 4 keeps the trunk's first video a founder call. Amendable per Guideline 6.
