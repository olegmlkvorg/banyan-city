# The Loop — repeatable quality cycle (founder's dad, 2026-07-23)

The season shipped rough because episodes were made *once*. The loop makes
quality compound instead: every cycle upgrades the **pipeline**, and any
episode rendered afterward — remake or new — inherits every fix ever made.
The episode being remade is just the loop's test bench.

## The cycle

1. **DIAGNOSE** — review the benchmark episode cold, like a scrolling
   viewer: what loses attention, ranked by damage. Evidence required
   (frames, timestamps), not vibes. Founder winces and platform numbers
   (ledger/reach.csv) join the list as they exist.
2. **FIX** — top 1–3 defects only, and only as *pipeline/prompt-system*
   changes (style bible, character blocks, shot grammar, renderer code).
   A fix that only helps one video is a hand-touch, not a fix.
3. **RE-RENDER** — the same benchmark episode, next version number, on the
   $0 path (Kaggle floor / free quota if any). Founder-reserved spend rules
   unchanged.
4. **SCREEN** — founder watches old vs new side by side. Keep or revert.
   If clearly better: post it; platform metrics become the external score.
5. **LOG** — `pipeline/loop/cycle-NNN.md`: defects found → fixes applied →
   what the founder felt → what the numbers did. Then go to 1.

## Rules

- **Benchmark: episode 001** (the front door — every viewer judges the
  show by it) until a cycle's diagnosis says another episode teaches more.
- One cycle = small and finished beats big and half-done. Never fix more
  than 3 things per cycle; you can't tell what worked.
- Old versions are never deleted (R6) — v1/v2 stay as leaves; the site
  shows the latest.
- Diagnosis is model-run; **taste verdicts stay the founder's** (R4):
  the loop proposes, the screening decides.
- Every re-render publishes provenance like any leaf (§7.2).

## Cycle log

| Cycle | Diagnosed | Top defects | Fixes | Verdict |
|---|---|---|---|---|
| 001 | 2026-07-23 | silent 2.5s open; −22 LUFS + dead-air holes; wall-of-text captions (15 confirmed, `loop/cycle-001.md`) | 3 chosen, all render_t3 assembly — v3 re-cuts at $0 | pending founder screening |
