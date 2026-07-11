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

1. **Do only what a work order says.** No task here authorizes anything not
   written in it. If a step is impossible or costs more than its budget line,
   stop and write a `BLOCKED:` note instead of improvising.
2. **Money:** never exceed a task's stated budget. Founder: please use a
   **virtual card with a hard limit** for the operator, not a primary card,
   and review charges. Every spend gets recorded in `ledger/expenses.csv`
   (date, item, amount, task-id) — this city publishes its costs.
3. **Credentials stay on the laptop.** Never commit tokens, card numbers, or
   account passwords to this repo. Secrets go in the services' own dashboards
   (e.g. GitHub repo secrets), referenced here by name only.
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

### V2 — Purchase banyan.city and point it at the Vercel project
- [ ] Status: **open** (depends on V1)
- **What:** buy the domain `banyan.city` — simplest is directly inside Vercel
  (Project → Settings → Domains → Buy), otherwise a registrar the founder
  prefers (Porkbun/Namecheap/Cloudflare) + add the domain to the Vercel project
  and set the DNS records Vercel shows (A/ALIAS + CNAME for `www`).
- **Budget:** up to **$40 first year** (typical .city is ~$10–30/yr). If it's
  priced above budget (premium listing), STOP and write `BLOCKED:` with the price.
- **Done when:** `https://banyan.city` serves the site with a valid certificate.
- **Then:** record the purchase in `ledger/expenses.csv` and commit.
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
