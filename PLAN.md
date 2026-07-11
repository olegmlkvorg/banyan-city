# Steward night-shift plan (2026-07-11 → 12)

**Protocol for the steward:** on every wakeup, open this file, do the FIRST
unchecked block, check it off with a one-line result, commit+push both branches,
redeploy banyan.city, re-arm the next wakeup (3600s) pointing at this file.
Do not stop until every box is checked. If the session/container dies, the
daily 09:23 tending cron resumes from this file — the plan lives in git, not
in memory.

- [x] **Block 1 — Trunk 005 "The Assessor"** — done 2026-07-11: script, T1,
      issue #9, edl entry; live at banyan.city (9 nodes).
- [x] **Block 2 — Y/N fork rendered (R4)** — done 2026-07-11: 004c-y "Y"
      (corrupted predecessor record) and 004c-n "N" (the bird gets root),
      issues #10/#11, edl entry; 11 nodes live.
- [ ] **Block 3 — T2 animatic renderer.** `pipeline/render_t2.py`:
      stills+TTS+assembly, bring-your-own-key providers, `--dry-run` tested,
      $0 spent tonight. Update pipeline/README.
- [ ] **Block 4 — Housekeeping.** CI runs green? Daily sap harvest landed?
      Any branch submissions / screening issues to process? VERCEL_TOKEN
      secret added (V4) → verify vercel workflow; if content changed, redeploy.
- [ ] **Block 5 — Morning report.** Concise summary in chat: what shipped,
      what's live, what needs humans. Then delete this file (plan complete)
      and return to the standing daily-tending rhythm.

Standing constraints (unchanged all night): steward authority per
STEWARDSHIP.md — no money spent, no accounts, no governance changes, all
story additions labeled with model provenance, every act cites taste rules.
