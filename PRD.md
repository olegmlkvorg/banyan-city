# Banyan City — Product Requirements Document

**Version:** 0.1 (living document — amend via commits, never via silent edits)
**Status:** Founding draft. This repo is the product. Everything evolves in git.

---

## 1. One-line summary

An open framework for growing **story trees**: AI-rendered, vertically-shot micro-drama series that branch instead of running linear, curated by one human author's extracted taste, screened and funded by the community watching them, with every decision, dollar, and render publicly auditable in git.

## 2. What this is

- A **framework first, product second.** Banyan City is the first *instance* of the framework. The framework itself is designed to be forked into other niches under other names. A fork is success, not infringement.
- A **story tree, not a series.** Episodes branch. Multiple continuations of the same moment coexist as siblings. Nothing is ever rejected — only deferred, dormant, or watered.
- A **living render.** Each story node can have multiple competing rendered versions (leaves) that mutate over time based on audience reaction data (sap), then harden into a canonical render.
- A **community-funded pipeline.** Citizens fund specific renders ("watering"), not vague content. Every cost is published. Payment is the strongest feedback signal.
- A **human-souled machine.** The author's taste is extracted into an explicit, versioned taste file. An AI author-agent applies it in a loop, committing selections to trunk. The human amends the *rules*, never individual commits.

## 3. What this is NOT

- Not a ReelShort clone (no paywall-per-cliffhanger; funding is patronage of branches)
- Not a walled IP play (no offensive trademarks, no takedowns of forks; see §5 Licensing)
- Not a choose-your-own-adventure app (branches are public, shared, and canonical — not private playthroughs)
- Not audience-run (crowd filters, author's taste file decides; disagreement is expressed by watering rival branches, not votes to override)
- Not dependent on any single platform (canonical layer lives in git; video platforms are disposable rendering surfaces)

## 4. Founding documents (verbatim, canonical)

### 4.1 The Founding Promise

> Banyan City is one tree grown from an open framework. No one owns the tree — not its stories, its branches, or its name. Anyone may branch any story, and anyone may branch the city itself: take these guidelines, plant them under a new name, in a new niche, and grow your own. A fork is not theft here; it is how the forest spreads.
>
> What exists at the start is only this: a framework, a set of guidelines, and one human author tending the first tree. The author's role is taste, not power — they choose what the root canon keeps, but they cannot fence what grows beyond it. Value flows back through citizens who choose to water the branches they love; nothing is locked behind a wall, and nothing is enforced by law where it can be sustained by care.
>
> If the citizens ever decide the city needs protection, structure, or stewardship, they must build and fund it themselves, openly, and it must remain answerable to them. And this promise itself is a living document: any part of it may be changed by the citizens for the better — except the right to branch, which is the root and may never be cut.

### 4.2 The Guidelines of the Grove

1. **Branching.** Any released episode may be branched by anyone. A branch declares its parent — that's the only obligation. Credit the root, then grow freely. Branches may contradict, subvert, or outgrow their parent; the tree doesn't police direction, only lineage.
2. **Watering.** Citizens fund branches directly. Water flows to the branch, not the platform: the split is published (author's share, generation costs, city commons). A branch that goes unwatered for a stated season goes dormant — never deleted, just resting. Anyone may revive it.
3. **Root canon.** Each tree has one tending author. They decide what the root canon absorbs from the branches — grafting popular branches in, or refusing them. Their taste is the product; their refusals are as canonical as their choices. If citizens disagree, they don't vote the author down — they water a rival branch. Exit, not override.
4. **The reaction loop.** Reactions, comments, and watering patterns are open data, visible to all — because they belong to the citizens who produced them, and because closed data recreates the power we're avoiding.
5. **Forking the city.** Take everything — guidelines, structure, vocabulary — rename it, and go. A fork must only drop the name of the city it left. No permission, no notice, no shame.
6. **Amendment.** Citizens may change any guideline through open proposal and visible support, except the right to branch and fork (Guideline 5), which is permanent.
7. **The leaf lifecycle.** Young nodes run *hot*: multiple leaves compete, mutate, and collect sap. A node *hardens* when a winning leaf becomes the stable canonical render new viewers receive. Retired leaves are archived as *rings* — inspectable forever. Hardened nodes may *reopen* for a molt when render technology meaningfully improves. Lifecycle parameters (hot duration, hardening threshold) are set per-tree in `tree.yaml` and amendable per Guideline 6.

## 5. Licensing & ownership stance

- **No trademark registration by the founder.** Prior public use is established by this repo's dated history. If citizens ever want the name defended, they fund and form a stewarding entity themselves (foundation/co-op) per the Promise.
- **Story content license:** recommend **CC BY 4.0** (attribution = "declare your parent," matching Guideline 1). More radical option on the table: CC0 + cultural credit norm. → Open Decision D1.
- **Code license:** recommend **MIT** (maximally forkable). → Open Decision D2.
- The founder initially "owns" only authorship of the framework text — which is itself openly licensed and amendable.

## 6. Vocabulary (canonical glossary)

| Term | Meaning |
|---|---|
| **Tree** | One story universe (e.g., *Sapling*). |
| **Genome** | The complete heritable data of a tree: all nodes, lineage graph, taste file, tree config. Forking a tree = copying its genome. |
| **Node** | One canonical story beat/episode unit in the genome. Slow-changing. Must contain a state change (R1). |
| **Trunk** | The author-curated canonical path through the nodes. |
| **Branch** | A sibling node continuing the same parent differently. Never deleted. |
| **Leaf** | One rendered version of a node (text, storyboard, or video tier). Multiple leaves per node compete while hot. |
| **Molting** | Replacing a weak leaf with a mutated sibling render. |
| **Hardening** | A node's winning leaf becoming the stable canonical render. |
| **Ring** | An archived leaf generation. The story's geology. |
| **Sap** | Reaction data (views, completion, reactions, comments, watering) flowing from leaves back to the tree. Open data. |
| **Watering** | Funding a specific branch/render. Also: contributing compute. |
| **Citizen** | A community member. Not "audience" — the climate the tree grows in. |
| **Grafting** | Merging a branch (or its elements) into the trunk or another branch. |
| **Seed** | A new tree started from the framework. |
| **Dormant** | An unwatered branch at rest. Revivable by anyone. |
| **Taste file** | The author's extracted, versioned decision rules. The 1% human soul, as an executable document. |
| **Author-agent** | The AI loop that applies the taste file to candidates and commits to trunk. |

## 7. Architecture

### 7.1 Two-layer storage

**Layer 1 — Canonical (decentralized, permanent, ours):**
- Git repository = source of truth: framework docs, genomes, taste files, lineage graphs, edit decision lists, sap summaries, watering ledger.
- Hosted on GitHub for reach; auto-mirrored to at least one independent host (Codeberg/GitLab). Optional: pin releases to IPFS/Arweave.
- A fork of the city is literally `git fork`.

**Layer 2 — Rendering surfaces (centralized, deliberately rented, disposable):**
- Video leaves published to YouTube Shorts / TikTok / Instagram Reels.
- Their compliance stacks (CSAM detection, copyright screening, regional law, moderation) are leveraged as the harmful-content filter and free distribution.
- If a platform removes a video, only a *copy* died; the node persists in Layer 1 and can re-render/re-upload anywhere.

### 7.2 The pipeline (per node)

1. **Generation** (the money burn). Script segment + parameters → N candidate clips at a known API cost. Every render publishes: prompt, model, seed, cost. Citizens water *specific renders* ("Node 002b, 8 candidates, ~$14"). Later: citizens contribute compute/API keys directly — compute as watering.
2. **Screening** (multiplayer). Candidates enter a public review queue. Citizens rate continuity, character consistency, vibe. Crowd **narrows**; it does not decide. Screening data doubles as pre-release sap.
3. **Selection** (the author-agent). The agent applies the taste file to the shortlist and **commits to trunk**, each commit citing the rule ID(s) that drove it (e.g., "selected leaf-3: R3 laughter-as-resolution; rejected leaf-1: violates R2"). Refusals get a one-sentence reason. The edit decision list is published.
4. **Assembly.** Selected clips + voice + music → episode leaf. Published to Layer 2; metadata and EDL committed to Layer 1.
5. **The loop.** Human author reviews the commit log periodically. If a commit feels wrong, the fix is **amending the taste file**, never overriding the commit. Every wince → interrogate → rule diff (public).

### 7.3 Taste extraction subsystem

- Taste cannot be written down directly; it is **derived from reactions**: structured interviews + forced choices between real rendered candidates (text tier is a valid render — cheapest tier).
- Loop: elicit → compile candidate rules → validate on unseen candidates (author blind-scores the same set) → divergence = bug list → amend → repeat.
- **Definition of "feels right":** taste file predicts the author's blind choices on unseen material ≥ 90% (tunable). Soul as a test suite.
- The taste file is versioned; its diff history is public. Onboarding a new author for a new tree = running the extraction interview. This interview is the framework's front door.

### 7.4 Render tiers (cost ladder)

| Tier | Form | Cost | Use |
|---|---|---|---|
| T0 | Text script / beats | ~free | Feeling candidates, taste extraction, branching decisions |
| T1 | Storyboard (stills + captions) | cheap | Pre-visualization, screening |
| T2 | Animatic (stills + VO + music) | low | Publishable early leaves |
| T3 | Full AI video (60–90s, 9:16 vertical) | priced per render | Hardened / hot leaves on platforms |

R4 (felt, not reasoned) requires the ladder: decisions climb tiers only when cheaper tiers can't resolve the choice.

## 8. Taste file — v0.2 (author: founder; tree: Sapling)

- **R1 — Economy of attention.** Every scene must change something: world state, a relationship, or what someone knows. Deletable without consequence = already deleted. *(Only stated absolute.)*
- **R2 — No evil.** Antagonism comes from conditioning, incentives, misunderstanding — never innate malice. "Just bad" characters are bugs.
- **R3 — Laughter as resolution.** The preferred way around conflict is exposing how ridiculous the situation is until both sides see it. Comedy is the mechanism, not the relief. Domination-victories are last resort.
- **R4 — Felt, not reasoned.** Narrative decisions are made by comparing rendered candidates (any tier), never abstract debate. Author inability to choose = instruction to render all options.
- **R5 — Cliffhangers, yes.** Episodes end on hooks; per R1 the hook must be a real state change; per R4 which hook wins is decided on material.
- **R6 — Rejection is only deferral.** Live candidates are never killed; they become sibling branches ordered by watering. The author's cut decides sequence and trunk, never existence. Wince test (R4) applies to moments *within* candidates, not whole candidates.

## 9. First genome: *Sapling* (working title; citizens may rename)

**Premise.** An engineer dies debugging production at 3 a.m. and reincarnates in another world as a **banyan sapling**. He cannot move, fight, or flee — only sense, grow, and make the space around him worth staying in. A worldbuilding/kingdom-building story in the *Tensei Slime* lineage — and a mirror of the platform itself: the city inside the story and the city around it grow together.

**Format.** Vertical 9:16, 60–90s episodes, cliffhanger per R5.

**Node 001 — Trunk: "Capability Inventory"**
Death at the keyboard → wakes as a sprout → panic → engineer-brain runs inventory of verbs: *sense* (roots, air, vibration) and *grow* (slow, directional). Hook: the inventory itself — the audience realizes with him that this protagonist can never walk away from anything.

**Node 002 — three sibling branches (all alive per R6):**
- **002a — "The Broken Channel."** Roots detect water flowing wrong: a cracked irrigation channel drowning one field, starving another. A farmer curses the gods for drought. The sapling grows a root toward the crack. Hook: the system *responds* to him.
- **002b — "The First Citizen."** A goblin-ish scavenger hides in his shade from a patrol (crime: ate an apple; charge: tax evasion). Lonely, the scavenger talks to the plant. The sapling drops his only fruit on his head. Hook: "…Did you just *answer* me?"
- **002c — "ADMIN(?)."** Systematic experimentation yields nothing — until sunset, when the world briefly renders wireframes: debug overlay on every plant, rock, creature. Over his own trunk, a half-corrupted label: **ADMIN(?)**.

**Grafting is anticipated:** the scavenger can wander into the irrigation branch; the overlay can explain the channel's response. Reconvergence is a designed payoff.

## 10. Repository structure (Phase 0 deliverable)

```
banyan-city/
├── README.md                  # what this is, how to branch, how to fork
├── PROMISE.md                 # §4.1 verbatim
├── GUIDELINES.md              # §4.2 verbatim
├── VOCABULARY.md              # §6
├── PRD.md                     # this document
├── LICENSE-CONTENT.md         # D1 (proposed CC BY 4.0)
├── LICENSE-CODE.md            # D2 (proposed MIT)
├── DECISIONS.md               # open decisions log (§13)
├── taste/
│   └── sapling.founder.v0.2.md    # §8; versioned by filename + git history
├── genomes/
│   └── sapling/
│       ├── tree.yaml          # title, author, lifecycle params, watering split
│       ├── lineage.yaml       # node graph: id, parent(s), status(hot/hardened/dormant)
│       └── nodes/
│           ├── 001-capability-inventory/
│           │   ├── node.md    # beats, state change, hook (T0 leaf)
│           │   ├── leaves/    # per-leaf metadata: tier, prompt, model, seed, cost, platform URLs
│           │   └── sap/       # reaction summaries (open data)
│           ├── 002a-broken-channel/
│           ├── 002b-first-citizen/
│           └── 002c-admin-wireframe/
├── ledger/
│   └── watering.csv           # date, node, amount/compute, split applied
└── pipeline/                  # tooling (Phase 2+)
```

## 11. Build phases (for Claude Code)

**Phase 0 — The repo is the product (now, $0).**
Scaffold the structure above; write all founding docs; commit T0 leaves (full scripts) for nodes 001, 002a–c; taste file v0.2; empty ledger. *Acceptance:* a stranger can read the repo and (a) understand the framework, (b) fork it, (c) branch node 002.
**Phase 1 — The tree becomes visible.**
Static site (GitHub Pages) rendering `lineage.yaml` as an explorable tree; nodes show their leaves and sap. Reactions via GitHub Discussions/Issues mapped to nodes. *Acceptance:* a non-git citizen can read the story and react.
**Phase 2 — The render pipeline.**
Scripts to generate T1/T2 leaves (image + TTS + assembly); public render queue with published prompt/seed/cost per candidate; simple screening UI (rate candidates). *Acceptance:* one node goes hot with ≥3 competing leaves screened by ≥5 citizens.
**Phase 3 — Watering.**
Start with Ko-fi/Patreon (individual, pre-incorporation) mapped manually into `ledger/watering.csv` with published split. Compute-as-watering: documented path for citizens to run renders with their own keys. *Acceptance:* first externally watered render ships; ledger balances publicly.
**Phase 4 — The author-agent.**
Agent applies taste file to screened shortlists, opens PRs to trunk with rule-cited reasons; human merges = review of the log; wince → taste-file PR, never commit override. Validation harness: agreement % on blind sets. *Acceptance:* agent ≥90% agreement on a 20-candidate blind set.
**Phase 5 — Platform leaves.**
T3 video leaves published to Shorts/TikTok/Reels; sap ingestion from platform APIs where possible; hardening of node 001.

## 12. Metrics

- **Taste fidelity:** agent-vs-author blind agreement % (per taste-file version)
- **Sap volume:** reactions per leaf; completion proxies where available
- **Watering:** funds/compute per node; % of renders externally funded
- **Tree vitality:** live branches, grafts performed, forks of the city (forks are a success metric)
- **Transparency integrity:** % of renders with complete published metadata; ledger reconciliation

## 13. Open decisions (DECISIONS.md seeds)

- **D1:** Content license — CC BY 4.0 vs CC0+norms
- **D2:** Code license — MIT vs AGPL
- **D3:** Screening vote weight — one-citizen-one-vote vs watering-weighted vs hybrid (unresolved; founder leaning undecided)
- **D4:** Lifecycle defaults — hot duration, hardening threshold for *Sapling*
- **D5:** Watering split defaults — author / generation costs / city commons percentages
- **D6:** Genome rename — does *Sapling* keep its working title?
- **D7:** When (if ever) citizens form a stewarding entity — explicitly deferred to citizens per the Promise

## 14. Risks (named honestly)

- **Character/scene consistency across leaves** — the hard technical problem of AI video; mitigated by render tiers and molting when models improve
- **Platform AI-content policy shifts** — mitigated by Layer 1/Layer 2 split; leaves are disposable
- **Taste-articulation gap** — the residue that won't compress into rules; mitigated by the permanent human review loop (the 1% never fully migrates)
- **Payments centralization** — Stripe/Patreon are unavoidable bureaucrats early; mitigated by compute-as-watering and ledger transparency
- **Name squatting** — accepted risk per founder's stance; prior-use history in git is the only defense until citizens decide otherwise
- **Cold start** — communities rarely *start* things; the founder's taste and the first genome must carry until citizens arrive

## 15. North star

A stranger finds the repo, reads the Promise, watches node 001, waters branch 002b with $3, sees exactly which render their $3 bought, watches it beat its siblings, and tells someone: *"I live there."*
