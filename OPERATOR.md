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

### V1 — Deploy the site to Vercel
- [ ] Status: **open**
- **What:** at <https://vercel.com/new>, import the GitHub repo
  `olegmlkvorg/banyan-city` (log in with the founder's GitHub). The repo already
  contains `vercel.json` — install/build/output are pre-configured
  (`python3 pipeline/build_site.py` → `_site/`). Production branch: `main`.
  Accept defaults otherwise; deploy.
- **Budget:** $0 (Vercel Hobby tier).
- **Done when:** the `*.vercel.app` URL serves the same site as
  <https://olegmlkvorg.github.io/banyan-city/> (8 nodes on the index).
- RESULT:

### V2 — Attach banyan.city to the Vercel project
- [ ] Status: **open** (depends on V1) — *domain already purchased by the founder*
- **What:** in the Vercel project → Settings → Domains, add `banyan.city` (and
  `www.banyan.city` redirecting to the apex). At the registrar where the founder
  bought it, set the DNS records Vercel displays (A/ALIAS for apex, CNAME for
  `www`). Wait for the certificate to issue.
- **Budget:** $0 (no purchase — domain is owned).
- **Done when:** `https://banyan.city` serves the site with a valid certificate.
- **Then:** record the founder's actual purchase price retroactively in
  `ledger/expenses.csv` (ask the founder or read the registrar receipt) and commit.
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

*(moved here by the operator, with results, newest first)*
