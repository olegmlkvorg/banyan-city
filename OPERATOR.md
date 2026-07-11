# Operator work orders

This file is the handoff channel between the **steward** (the agent tending this
repo remotely — no browser, no accounts, no money) and the **operator** (an
agent or human on the founder's machine, with browser access and, when the
founder grants it, payment ability).

**Protocol:** the steward writes bounded work orders here. The operator
executes them, then edits this file — filling in the `RESULT` line and checking
the box — and commits with message `operator: <task-id> done`. The steward
verifies outcomes independently (DNS, HTTP, ledger) on its next tending pass.

## Rules for the operator (read first)

1. **Standing grant (founder, 2026-07-11, stated non-negotiable):** the
   operator has **full access on the founder's machine and the founder's
   payment card**. Work-order budget lines are the steward's cost *estimates*
   and scope signals, not caps — the operator may exceed them at its own
   judgment under this grant.
2. **Transparency is not waived:** every spend, whatever its size, gets
   recorded in `ledger/expenses.csv` (date, item, amount, task-id). This city
   publishes its costs — that's the framework's constitution, not a leash.
3. **Card and credentials never enter this repo or any commit.** This
   repository is PUBLIC: a card number, token, or password committed here is
   scraped by strangers within minutes. The card lives on the founder's
   machine and in payment forms only. Secrets that services need go in their
   own dashboards (e.g. GitHub repo secrets), referenced here by name only.
4. **This repo's story/governance files are not the operator's surface.**
   Operators touch this file, `ledger/expenses.csv`, and service dashboards —
   nothing else without a work order saying so.

---

## OPEN WORK ORDERS

### V4 — Add the VERCEL_TOKEN repository secret (enables auto-deploy from CI)
- [ ] Status: **open** — founder or operator, ~30 seconds
- **What:** GitHub repo → Settings → Secrets and variables → Actions → New
  repository secret. Name: `VERCEL_TOKEN`. Value: the Vercel token the founder
  issued to the steward (founder has it; steward holds it only in its ephemeral
  session). Then re-run the `vercel` workflow once (Actions → vercel → Run
  workflow) or push anything to `main`.
- **Why:** the steward's session proxy blocks writing GitHub secrets, and the
  steward's own copy of the token dies with its container. Until this is set,
  banyan.city updates only when the steward manually redeploys on a tending pass.
- **Budget:** $0.
- **Done when:** the `vercel` workflow runs green and banyan.city reflects a new push.
- RESULT:

### V5 — Record the banyan.city purchase price
- [ ] Status: **open**
- **What:** add a row to `ledger/expenses.csv` with the actual price the founder
  paid for banyan.city (registrar receipt) and commit.
- **Budget:** $0 (retroactive bookkeeping).
- RESULT:

### V3 — Report rails available for Phase 3 (no purchase)
- [ ] Status: **open** (anytime)
- **What:** check whether the founder's GitHub account is eligible for GitHub
  Sponsors, and note which of Ko-fi / Patreon the founder prefers to open when
  Phase 3 starts. **Do not create any account or accept any money** — this is
  reconnaissance only; opening a rail requires the founder's explicit go
  (STEWARDSHIP.md §4).
- **Budget:** $0.
- RESULT:

---

## COMPLETED WORK ORDERS

### V1 — Deploy the site to Vercel — **done 2026-07-11 by the steward**
- Founder issued a full-access Vercel token directly to the steward, making the
  browser path unnecessary. Project `banyan-city` created via CLI; prebuilt
  static deploys (local `vercel build` → `deploy --prebuilt --prod`).
- RESULT: production live; remote pip build intentionally bypassed (prebuilt flow).

### V2 — Attach banyan.city — **done 2026-07-11 by the steward**
- Domain was already on Vercel nameservers (bought by founder); apex attached to
  the project, `www` added with redirect to apex; certificates issued.
- RESULT: <https://banyan.city> serves the full site (8 nodes), valid TLS.
