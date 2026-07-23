# Loop cycle 002 — the voice layer (2026-07-23)

Opened by two founder winces on the v3 screening (v3 itself KEPT):
**"the subtitles are offset from the voice"** and **"the voice is very
very emotionless."** Both trace to the VO layer, so this cycle promoted
the one-off scratchpad VO scripts into `pipeline/synth_vo.py`.

## Diagnosis (from code, not agents — causes were mechanical)

1. **Caption offset, two mechanisms:** (a) chunks were spread across
   [line start → NEXT line's start], i.e. across the silent inter-line
   gap, so every chunk after the first lagged the voice; (b) within the
   window, chunks were timed by word count — numbers, punctuation and
   kokoro's real pacing diverge from word-count proportions.
2. **Flat delivery, three mechanisms:** kokoro's head/tail engine silence
   made every gap ~0.9s regardless of intent (cycle-001 defect 14);
   scripted "Beat." breaths were dropped entirely; every line ran at its
   character's single base speed.

## Fixes

- `pipeline/captions.py` — chunker shared by renderer and synth (em dash
  kept visible at clause end; word order provably preserved — tests).
- `pipeline/synth_vo.py` (new, replaces scratchpad make-vo): trims engine
  silence so pauses are authored; gap-by-intent (standalone "Beat." →
  1.2s breath, rapid ≤4-word exchanges → 0.18s snap, trailing …/— →
  0.35s, sentence end → 0.5s); per-line speed eases with punctuation
  shape; and every caption chunk is synthesized SOLO to measure its
  spoken length, mapped into the line's real speech window, and written
  to the manifest as `lines[].chunks`.
- `render_t3.py` — prefers measured `chunks` from the manifest; fallback
  estimates now span the line's speech window [start, end], never the
  inter-line gap.
- Old VO takes archived per R6: `clips/vo-archive/`.

## Honest ceiling

kokoro-82M has no emotion control — this cycle fixes *rhythm* (breaths,
snap, pace), not *acting*. The acting fix is an emotional/instructable
TTS (CosyVoice2 / Chatterbox class) on a free GPU (Kaggle floor), which
is the standing next render-stack move.

## Bench

`~/Desktop/banyan-001-v4-LOOP2.mp4` — ep 001 re-cut with directed VO and
measured caption sync, $0. −14.4 LUFS, zero digital silence, all
pipeline tests green.

## Verdict

Pending founder screening of v4 vs v3. If kept: run `synth_vo` + re-cut
for eps 2–7 before their drop nights.
