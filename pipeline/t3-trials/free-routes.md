# Free ($0) video-generation routes — verified 2026-07-19

Researched for the v2 anime style (`../../genomes/sapling/style.md`) by a
4-lens web research pass + adversarial verification of each candidate's
current terms (workflow run `wf_1f0df994-177`; every claim below carries a
2026-dated source in that run's journal). Landscape shifts monthly — re-verify
before relying on numbers here after ~August 2026.

## Usable at $0 for published leaves (no visible watermark, publishable terms)

| Route | Free volume | Output | Watermark | Notes |
|---|---|---|---|---|
| **Qwen Studio** (chat.qwen.ai — Wan 2.7 under the hood) | soft-capped, ~6-7/session, no card | ~5s · ~720p · 9:16 picker | **none visible** (invisible provenance only) | Wan family = community-consensus best open model for flat 2D anime. ToS forbids *stripping* provenance marks — we never do. Platform output-rights wording thin; weights-family is Apache-2.0. |
| **HF ZeroGPU Space** `Lightricks/ltx-video-distilled` | ~4-5 clips/day (5 min GPU/day on free account) | up to 8.5s · 576×1024 native 9:16 | none | LTX is the weakest at anime of the viable set — test before committing. LTX community license: fine for us (<$10M). Wan ZeroGPU spaces are 832×480 landscape-locked — wrong aspect. |
| **Kaggle free GPU** (30 GPU-h/week) running open weights | effectively unbounded for our volume | Wan 2.1 1.3B: 480×832 portrait 5s; anime LoRAs possible | none — self-hosted | Most control; reproducible-by-citizens (compute-as-watering). Also the only free CUDA path that might run **AniSora** (Bilibili's anime-specialist, Apache-2.0, 12GB-VRAM V3.1 variant) — worth one experiment. |
| **Google Flow free** — Veo 3.1 **Lite** | **5 clips/day** (official: 50 credits/day, Lite=10) | 4-10s · ~720p · 9:16 | **visible** "Made with Veo" on free | Trials/taste-tests only — the visible watermark keeps free Flow output out of canon leaves (D9). Confirmed on Google's own support page. |

## Verified dead ends or blocked

- **Kling / Vidu / PixVerse / Luma free tiers** — all watermarked AND
  free-plan ToS restricts output to personal, non-commercial use. Vidu and
  PixVerse are the *best anime stylists* of the consumer apps, which makes
  this genuinely a shame — but publishing their free output on banyan.city
  would breach their stated terms. Blocked on license, not quality.
- **Gemini API / AI Studio free Veo** — none exists (video is paid-tier
  only). **Grok** — free video tier removed 2026-03. **Runway** — 125
  one-time credits, a trial not a tier. **fal.ai / Replicate / Together /
  Fireworks** — no dependable free video allowance.
- **Local on the founder's M1 Pro 32GB** — real but slow: Wan 2.1 1.3B
  measured ~1.5-2h per 5s clip; FastWan 2.2 5B has official MPS support
  (M-series, "32GB preferable") but no M1 Pro timing published. Overnight
  batches only; Kaggle dominates it on speed at the same $0.
- **Near-future watch items**: Wan 2.7 open weights (reportedly on
  ModelScope 2026-06; the model anime rankings call best-in-class for
  exactly our style), LTX-2.3 ZeroGPU space (9:16-native, 75s GPU per gen).

## API routes to the Wan models (verified 2026-07-19, follow-up pass)

Qwen Studio itself exposes **no API** — but the Wan models behind it do:

- **Alibaba Cloud Model Studio (DashScope, Singapore region)** — the
  official API. `wan2.7-t2v` / `wan2.7-i2v`: native **1080×1920 (9:16)**,
  **2–15s** clips, synced audio, and **watermark OFF by default** (an
  explicit `watermark` param, default false — official API reference).
  Pricing ≈ $0.10/s (third-party corroborated; official table is
  JS-rendered — confirm in console). **New-user free quota: 90 days,
  Singapore region only, no credit card to activate** — reportedly
  **~1,650 seconds of video** (≈330 five-second clips ≈ the whole season
  ~10× over; amount is third-party-corroborated, confirm on the console's
  Free Quota page before planning). Publishing terms in the intl service
  agreement not yet reviewed — flag before canon use.
- **ModelScope API-Inference** — genuinely $0 ongoing (~2,000 calls/day)
  and Wan video is advertised as included, but requires Alibaba
  real-name-verified account binding, limits are dynamic/opaque, and
  video-specific caps + watermark policy are unverified. Worth an empirical
  probe only if Model Studio's quota disappoints.
- Paid API hosts for the same models, for reference: Together AI $0.10/s
  (official wan2.7 partner), SiliconFlow $0.29/clip, fal.ai (see D8 table).
  No recurring free video tier on any of them.

**Consequence:** free + automated is possible — `generate_shots.py` can
drive the whole season through Model Studio's free quota once the founder
activates the account (no card) and drops the key in `.env`. Activation is
a founder action: it opens a rail that can convert to pay-as-you-go, so it
stays under the spend rules even at $0.

## Practical shape for our 24-prompt season

Two 5s generations per ~10s beat (or write beats to 5-8s), assembled by
`render_t3.py` which fits/pads clips per beat. A 3-route anime trial (Qwen
vs Flow-Lite vs Kaggle-Wan on trial shots A/B/C) costs $0 and gives D8 real
same-style evidence; the paid fal.ai bake-off remains the fast alternative.
Generation on hosted webapps is a founder action (their accounts); the
steward prepares prompts (done — every trunk node has `shots.md`) and can
author the Kaggle notebook end-to-end.
