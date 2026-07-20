# Watering — how value flows back to the tree

Watering is citizens funding **specific renders**, not vague content (Guideline 2).
Every watered render publishes its prompt, model, seed, and cost; every dollar or
GPU-hour lands in [`ledger/watering.csv`](ledger/watering.csv) with its published
split. This document is the front door for Phase 3; nothing here accepts money yet.

## The two kinds of water

**Money.** Phase 3 opens with an individual Ko-fi/Patreon (pre-incorporation),
mapped manually into the ledger. Citizens water a *specific* line item — e.g.
"Node 002b, 8 candidates, ~$14" — and the resulting renders publish their full
provenance. **The split is resolved** ([D5](DECISIONS.md)): each watered render
reimburses its published generation cost first; the remainder splits **70%
author / 30% city commons** (`costs-first-70-30-v1`). One human step remains
before funds can flow: the founder confirms the split and opens the payment
rail (STEWARDSHIP.md §4).

**Compute.** The pipeline is designed so citizens can run renders with their own
API keys and submit the results — compute as watering:

- `pipeline/render_t1.py` already runs at $0 for anyone (`python3 pipeline/render_t1.py sapling <node-id>`).
- `pipeline/author_agent.py` runs against the contributor's own `ANTHROPIC_API_KEY`.
- T2/T3 renderers (Phase 2+) will take the same shape: bring your own key, the
  render's provenance (prompt, model, seed, cost) is committed, and the
  contribution is recorded in the ledger with `type: compute`.

A compute contribution is watering the branch exactly as money is: it appears in
the ledger, it orders sibling branches, and it keeps a branch from going dormant.
The end-to-end walkthrough — pick an episode, re-render it better (free Kaggle
GPU, your own key, or any tool), submit the leaf — is [REGROW.md](REGROW.md).

## The ledger

One row per watering event:

```csv
date,node,leaf,citizen,type,amount_usd,compute_desc,split_applied,notes
```

- `type` is `funds` or `compute`
- `citizen` is a handle (or `anonymous`) — never more than the citizen chooses to publish
- `split_applied` names the split version in force at the time (per D5, once resolved)
- The ledger must reconcile publicly (PRD §12 — transparency integrity)

## What watering is not

- Not a paywall: nothing is locked behind it (the Promise)
- Not a vote: watering orders sibling branches and keeps them awake; the taste
  file still decides the trunk (Guideline 3)
- Not a subscription to the platform: water flows to the *branch*

## Opening the rail — founder runbook (10 minutes, one time)

1. Create the payment link you own (Ko-fi/Stripe/GitHub Sponsors — your pick,
   your account).
2. In `genomes/sapling/tree.yaml` → `watering_rail:` set `payment_link:` to
   that URL and `confirmed_by_founder: true` (this IS the D5 re-confirmation).
3. Push. The site's per-node "Water this branch" buttons go live on deploy.

Incoming contributions are mapped by hand into `ledger/watering.csv` (one row
per drop, split `costs-first-70-30-v1`) — steward drafts rows, founder
verifies against the payment account. Until then, compute-watering is already
open to everyone.
