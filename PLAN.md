# Steward night-shift plan (2026-07-13 → 14)

**Protocol:** on every wakeup, open this file, do the FIRST unchecked block,
check it off with a one-line result, commit+push main, re-arm the next wakeup.
Founder asleep, but explicitly authorized overnight work this session. Still:
$0 spend, no accounts, no governance changes, all story labeled with
provenance, taste rules cited (STEWARDSHIP.md).

## Shipped tonight
- Deploys fixed (PEP 668, default branch → main, pages env); all CI green.
- render_t3.py — episode assembler (clips→episode, overlays, captions, slates,
  title/end cards); caption boundary flash fixed.
- /trials/ page + intake.py; scores.yaml.
- **First real footage:** founder's 3 Veo/Google-Flow shots (A/B/C) filed,
  objective-scored (weighted 4.5), live on banyan.city/trials.
- First real T3 episode of node 001 assembled (Veo beats 1/2/4 + 2 slates +
  cards, 90.5s, $0) → preview at ~/Desktop/banyan-001-veo-preview.mp4.
- 004a "Ticket One" node published (T0/T1/T2); render_t2 chromium path portable.

## Remaining
- [ ] **Clip watch (recurring).** Each wakeup: check pipeline/t3-trials/outputs/
      for new drops (founder may run Dreamina/Hailuo). Process any with
      `python3 pipeline/t3-trials/intake.py <file> <platform> <shot>`, pre-score
      objective axes, rebuild, push. Direct `cp <fullpath>` works even though
      Downloads listing is TCC-blocked.
- [ ] **Morning report + tidy.** At morning (past ~07:00 Dubai) or when the
      founder returns: concise report of what shipped + the decisions waiting on
      them (below). Then delete this file.

## Decisions waiting on the founder (do NOT self-resolve)
1. Publish the 001 Veo episode as node 001's official T3 leaf? (trunk root,
   watermarked, 2 beats still slate — steward's read: not yet.)
2. Fill the taste-axis scores (motion/look/consistency) on /trials/ (R4 — author only).
3. Run the same 3 prompts on a 2nd/3rd platform to make the bake-off real
   (Veo set a high bar at 5/5/5 adherence).
