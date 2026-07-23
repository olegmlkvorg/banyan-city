# Loop cycle 001 — diagnosis of episode 001 (2026-07-23)

Method: six model reviewers, one dimension each (hook, visual consistency,
motion, audio, captions, pacing/payoff), on frames extracted from the live
leaf `001-t3-b.mp4` + eps 004/007a for cross-episode comparison. Every
claim adversarially re-verified against the video/code by a second agent;
only survivors listed as confirmed. Workflow `wf_4b4a7935-ebc`
(~1.5M tokens, $0 marginal). 15 confirmed · 1 refuted · 13 pending
(verify agents hit the session limit; to re-verify next cycle).

## Confirmed defects (ranked)

| # | Sev | Dim | Defect |
|---|---|---|---|
| 1 | 5 | hook | First 2.5s of EVERY episode = silent, near-black, static title card — the whole scroll-decision window. Cause: `render_t3.py:462` prepends a 2.5s card with `audio=None`. Reads as a video that failed to load. |
| 2 | 5 | audio | Same window is digital-zero silent (astats Peak −inf, 0–2.6s). The script's designed sonic hook ("the sound of one mechanical keyboard") never renders. |
| 3 | 5 | pacing | Premise (reincarnated as a tree) first visible ~13s in; seconds 0–3 show zero story, first bright signature image at 12.5s. |
| 4 | 4 | hook | First live shot (2.5–8s) is a back-of-head, near-static wide; first face at ~8s. Beat-1 prompts never lock camera/face; fitter plays clips head-first. |
| 5 | 4 | hook | Hook window is dark: mean luma 22% for 0–8s vs 57% at 12–16s. On a bright feed, 8 dark seconds = swipe. |
| 6 | 4 | audio | Episode masters −22.3 LUFS vs ~−14 platform norm — plays ~half as loud as adjacent feed videos. T3 has NO loudnorm (T2 already does; omission is T3-specific, all 7 episodes −19..−22 LUFS). |
| 7 | 4 | audio | No ambience/music bed anywhere: 3.1s digital-zero hole at 9.5–12.6s (right in the retention window) + 4.4s silent tail. Script specifies sound there. |
| 8 | 4 | captions | Wall-of-text captions: whole VO lines burn in as 4–6-line, 24–35-word paragraph blocks (render_t3 rasterizes a full line as one PNG, unlimited wrap). |
| 9 | 4 | captions | Caption glyphs ~2.2% of frame height, regular-weight mono, 59%-alpha box — roughly ⅔ the size of platform-native captions; weak for sound-off viewing. |
| 10 | 4 | pacing | Inventory punchline spoiled: all capability overlays render at once ~38s, 9s before the VO reveal "…That's the whole API." The episode's central R5 mechanic deflated. |
| 11 | 4 | pacing | Caption walls freeze pacing: 6-line blocks held ~8s over near-static shots (worst 22.5–32s, inter-frame delta ~0.2 vs 1.4–2.6 baseline). |
| 12 | 3 | hook | First caption ("retry loop" dev-jargon, 3 lines) held unchanged 5.5s across the 3–8s retention stretch. |
| 13 | 3 | audio | Scripted sound design structurally discarded — VO is the only sound; SFX cues have no pipeline path; native clip audio dropped at mux. |
| 14 | 3 | audio | Metronomic VO pacing: six inter-line gaps all 0.88–0.98s regardless of dramatic intent; standalone "Beat." dropped entirely. TTS autopilot tell. |
| 15 | 3 | pacing | GROW beat has no growth — reuses the SENSE underground clip; 14s single-scene stretch mid-video; scripted timelapse never got a shot prompt. |

## Refuted (1)

- "Ending fizzles / no cliffhanger visual" — REFUTED: at 67.3–68.7s a
  creature's shadow sweeps and engulfs the frame, timed to the VO. The
  reviewer under-sampled. End card is 3.0s, not 4s.

## Pending verification (session limit; carry to next cycle)

Visual consistency: goblin is a different creature in nearly every shot;
art style re-rolls every clip; protagonist morphology drifts; recurring
humans drift across episodes; attribute bleed between characters.
Motion: first shot holds near-still; beat 3 ~10s motionless; climax
replays its whole clip; loop restarts are hard jump-cuts.
Captions: captions sit inside platform UI safe-area; 720x1280+CRF23
veryfast masters soft after platform re-encode.
(These match the founder's own winces — treated as plausible; the
character-consistency fix is already the standing regrow-era priority.)

## Cycle-1 fix selection (max 3, per loop.md)

All three are `render_t3.py` assembly changes — **episode 001 v3 re-cuts
from existing clips at $0. No new footage, no quota, no Kaggle.**

1. **Kill the silent open** (defects 1, 2, 3, 12 partially): no leading
   card segment; footage + audio start at t=0; series wordmark + title
   (+ "Previously:") composited as a small overlay on the first ~2.5s of
   live footage. End card stays.
2. **Sound floor** (6, 7): two-pass loudnorm to I=−14/TP=−1/LRA=11 on the
   final mux + continuous low-level ambience bed (port T2's wind bed)
   under the whole episode, fading over the end card. No frame ever
   digitally silent.
3. **Caption system v3** (8, 9, 11, 12): chunk VO lines to ≤2 rendered
   lines (~8 words) timed proportionally within the line's manifest
   window; ~46px bold; box alpha ~200.

Deferred to later cycles: hook-beat shot grammar + in-point selection (4,
5), overlay-sync-to-VO (10), SFX lane (13), gap-by-intent VO pacing (14),
beat/clip coverage lint (15), character bible + keyframe pipeline
(pending cluster).

## Fixes applied (2026-07-23, same day)

All three landed in `render_t3.py` (+7 chunker/span tests in
`test_pipeline.py`); ep 001 v3 bench-rendered from existing clips at $0:
`~/Desktop/banyan-001-v3-LOOP1.mp4`. Measured against the diagnosis:

| Defect | v2 (001-t3-b) | v3 |
|---|---|---|
| silent black open | 2.5s card, story at 2.7s | footage + VO at t=0, title as 2.8s overlay |
| digital-zero holes | 0–2.6s, 9.5–12.6s, 68–71.7s | **none** (silencedetect −45dB: zero events) |
| loudness | −22.3 LUFS | **−14.4 LUFS** (two-pass loudnorm + wind bed) |
| captions | 4–6-line walls, 28px regular | ≤2-line chunks, 46px bold, VO-proportional timing |

## Verdict

Pending founder screening of v3 vs v2 (loop.md step 4). If kept: re-assemble
eps 2–7 with the same renderer (pure re-cut, $0) before their drop nights.
