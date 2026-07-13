# Steward night-shift plan (2026-07-13 → 14)

**Protocol:** on every wakeup, open this file, do the FIRST unchecked block,
check it off with a one-line result, commit+push main, re-arm the next wakeup.
The plan lives in git, not in memory. Founder is asleep: $0 spend, no accounts,
no governance changes, all story content labeled with provenance, taste rules
cited (STEWARDSHIP.md).

Previous night plan (07-11→12): blocks 1–3 shipped that night; blocks 4–5
(housekeeping + report) completed 2026-07-13 — CI green, deploys fixed
(PEP 668, default branch → main, pages env), main synced, report delivered.

- [ ] **Block 1 — Trial intake.** Check `pipeline/t3-trials/outputs/` for
      clips the founder dropped before sleeping. For each: write
      `<shot>.meta.yaml` (platform, model, prompt, watermark, credits, $0),
      normalize filenames, commit. If none yet, skip without waiting.
- [ ] **Block 2 — render_t3.py scaffold (the post pipeline).** Assembly stage
      that takes per-beat clips + the T1 storyboard and composites the
      episode: terminal-text overlays (drawtext/subtitles), beat timing from
      node.md, concat to 60–90s 9:16 mp4. Prove it end-to-end using the T2
      stills (or any trial clips present) as stand-in footage — the point is
      that whichever platform wins, its clips slot in unchanged.
- [ ] **Block 3 — scores.yaml + trials page.** Scoring template per rubric;
      build_site.py renders a public /trials/ comparison page (per-platform,
      per-shot, embedded clips where present). Steward pre-scores objective
      axes (adherence, 9:16 nativeness, friction); taste axes left blank for
      the founder.
- [ ] **Block 4 — Grow the tree (T0+T1).** One new branch node under a
      sibling that currently has no continuation (mind R1/R5; cite taste
      rules; provenance: model-written, steward-committed). Lint, issue,
      lineage.yaml, T1 storyboard, deploy.
- [ ] **Block 5 — Housekeeping + morning report.** CI green, harvest landed,
      submissions queue empty, deploys Ready. Then: concise morning report in
      chat — what shipped, trial-intake status, what needs the founder (the
      remaining sign-ups / taste scoring). Delete this file.
