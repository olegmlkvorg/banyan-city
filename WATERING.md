# Watering — how value flows back to the tree

Watering is citizens funding **specific renders**, not vague content (Guideline 2).
Every watered render publishes its prompt, model, seed, and cost; every dollar or
GPU-hour lands in [`ledger/watering.csv`](ledger/watering.csv) with its published
split. This document is the front door for Phase 3; nothing here accepts money yet.

## The two kinds of water

**Money.** Phase 3 opens with an individual Ko-fi/Patreon (pre-incorporation),
mapped manually into the ledger. Citizens water a *specific* line item — e.g.
"Node 002b, 8 candidates, ~$14" — and the resulting renders publish their full
provenance. **Blocked on [D5](DECISIONS.md):** the split (author share /
generation costs / city commons) must be resolved and published before the first
dollar is accepted.

**Compute.** The pipeline is designed so citizens can run renders with their own
API keys and submit the results — compute as watering:

- `pipeline/render_t1.py` already runs at $0 for anyone (`python3 pipeline/render_t1.py sapling <node-id>`).
- `pipeline/author_agent.py` runs against the contributor's own `ANTHROPIC_API_KEY`.
- T2/T3 renderers (Phase 2+) will take the same shape: bring your own key, the
  render's provenance (prompt, model, seed, cost) is committed, and the
  contribution is recorded in the ledger with `type: compute`.

A compute contribution is watering the branch exactly as money is: it appears in
the ledger, it orders sibling branches, and it keeps a branch from going dormant.

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
