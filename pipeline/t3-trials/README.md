# T3 platform trials — free-tier bake-off

**Goal:** pick the video model(s) for the first paid T3 leaves (PRD §7.4) by
rendering the *same three shots* from node 001 on every candidate platform,
spending $0 (free tiers only), and scoring the results against a fixed rubric.
Everything here is public per §7.2 — prompts, models, outputs, scores.

**Scope decision:** trials test **base footage only** — no burned-in text, no
audio. Terminal overlays and VO are composited deterministically in post by the
existing T2 pipeline (`render_t2.py` lineage), so the generation model is judged
purely on photography: image quality, motion, prompt adherence, 9:16 framing.
This keeps free tiers viable (no native-audio credits needed) and keeps the
per-shot prompt identical across platforms.

## Candidates (free tiers as of 2026-07-13)

| # | Platform / model | Free tier | Watermark | Notes |
|---|---|---|---|---|
| 1 | **Kling 3.0** (kling.ai) | 66 credits / 24 h **website only** | yes (free) | most generous daily reset; cheapest paid fallback (~$0.84/10 s). Verified 2026-07-13: the official agent CLI (`@klingai/cli-global`, OAuth'd) has a **separate agent credit pool with no free allowance** — every CLI submit returns "Insufficient credits" at $0 balance, even v2.5. Free-tier trials must go through the website UI; the CLI becomes useful once paid credits exist. |
| 2 | **Hailuo 2.3** (hailuoai.video) | 200 credits first-time, then ~3–5 gens/day | yes (free) | strong motion reputation |
| 3 | **Seedance 2.0** via Dreamina (dreamina.capcut.com) | daily credits, ~2–3 videos/day | reported watermark-free on some tiers — verify | CapCut variant has stricter filters; prefer Dreamina |
| 4 | **Veo 3.1** via Google Flow (labs.google/flow) | 100 credits once + 50/day (~2 videos/day) | yes (free) | best prompt adherence per current comparisons; also 10/mo via Google Vids |
| 5 | **Pika 2.5** (pika.art) | 80 credits / month | yes | effects-oriented; cheap test of stylized shots |
| 6 | **Luma Dream Machine 2.5** | 30 credits / month | yes | low allowance — run only Shot B |
| 7 | **PixVerse** | daily free credits | yes | wildcard; fast iterations |

Excluded: **Sora** — OpenAI announced discontinuation (app Apr 2026, API Sep 2026).
Dead end for a platform we'd depend on.

Sources: [buildmvpfast ranking](https://www.buildmvpfast.com/articles/best-llms-2026-guide/video-generation-ai),
[kingy.ai comparison](https://kingy.ai/ai/best-ai-video-generator-2026/),
[Veo free access](https://incrypted.com/en/how-create-video-googles-veo-31/),
[Seedance free guide](https://www.gamsgo.com/blog/seedance-ai-free),
[Dreamina Seedance](https://dreamina.capcut.com/tools/seedance-2-0).
Free-tier numbers drift weekly — verify on signup, correct this table in the
same commit that records the trial.

## Protocol

1. **Accounts:** the founder creates/logs into each platform (steward does not
   hold accounts — STEWARDSHIP.md). Free tier only; no card attached even when
   a card exists (this phase is $0 by design).
2. **Shots:** render the three shots in [`prompts.md`](prompts.md) — verbatim
   prompts, 9:16, ~10 s, one take each. If the platform needs an image-to-video
   seed frame, note it; a shared seed frame beats prompt-only for consistency.
3. **No retries on taste:** one regenerate allowed per shot for outright
   technical failure (garbage output), none for "didn't like it" — we are
   measuring the platform's default competence, not our patience.
4. **Archive:** save every output as
   `pipeline/t3-trials/outputs/<platform>/<shot>.mp4` + a `meta.yaml` per file
   (platform, model+version, prompt used, credits consumed, resolution,
   watermark y/n, date). Outputs are trial artifacts, **not leaves** — nothing
   enters `genomes/` until a model is chosen and a real T3 leaf is rendered.
5. **Score:** fill `scores.yaml` per the rubric below. Scoring is public data.

## Rubric (1–5 each)

| Axis | What 5 looks like |
|---|---|
| **Prompt adherence** | shot contains what the prompt asked, composition included |
| **Motion quality** | physics plausible; no morphing, no AI-shimmer on the leaf/roots |
| **Look** | could sit in a real micro-drama; lighting and lens feel intentional |
| **9:16 nativeness** | composed *for* vertical, not cropped from landscape |
| **Consistency potential** | could shots 2–3 pass as the same world/character? |
| **Friction** | free-tier UX: queue times, refusals, resolution caps, watermark severity |

Weighting: adherence and consistency-potential count double — a branching
series lives or dies on shot-to-shot coherence across many nodes.

## Exit criterion

One platform (or a two-platform split: hero shots vs. cheap coverage) chosen
for the first real T3 leaf of node 001, with its per-episode cost estimated
from actual credits consumed. That choice + evidence goes into DECISIONS.md
and unblocks Phase 3 pricing.
