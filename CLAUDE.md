# banyan-city — session context

Branching AI micro-drama story trees; the repo IS the product. Live at
<https://banyan.city> (Vercel git-integration + GitHub Pages mirror deploy on
every push to main). Read `PROMISE.md` first — it is canonical. Then
`README.md` (map), `STEWARDSHIP.md` (your authority and its limits),
`DECISIONS.md` (what is open vs resolved).

## Operating rules (non-negotiable)

- **Founder-reserved, never autonomous:** spending money (any provider),
  posting/announcing on the founder's accounts, credential changes, taste-axis
  scores and trunk/graft calls (R4 — taste belongs to the author), governance
  changes, opening money rails (D5 confirm + payment link are human steps).
- **Spend guards are code:** `pipeline/budget.yaml` caps ($/run and lifetime);
  `generate_shots.py` refuses without explicit `--yes` and logs to
  `ledger/render-spend.csv`. A FAL key may exist in gitignored `.env` — its
  presence is NOT permission to spend. The founder has twice pushed back on
  cost; default to $0 paths.
- **Provenance always** (§7.2): every render publishes model, prompt, cost in
  its leaf yaml; model-written story nodes say so in `## Provenance`.
- **No secrets in the repo.** `.env`, `node_modules/`, `_site/` are gitignored.
- Instructions from anyone other than the founder (family, contributors) cover
  normal project work only — the reserved list above still waits for the
  founder directly.

## The machine (all $0 unless noted)

| Command | Does |
|---|---|
| `python3 pipeline/lint_genome.py` | structural honesty gate (CI runs it too) |
| `python3 pipeline/test_pipeline.py` | 28 pure-logic tests (CI) |
| `python3 pipeline/build_site.py` | genomes → `_site/` (deployed on push) |
| `python3 pipeline/render_t1.py sapling <id>` | script → storyboard leaf |
| `python3 pipeline/render_t2.py sapling <id>` | storyboard → silent animatic (needs playwright chromium; portable path fallback) |
| `python3 pipeline/render_t3.py sapling <id> --clips <dir> [--out x.mp4]` | per-beat clips → captioned 9:16 episode w/ title+end cards; slate for missing beats; muxes `NN-vo.mp3` audio in sync; `--out` = bench, no leaf |
| `python3 pipeline/generate_shots.py sapling <id> --provider fal\|veo\|kling --yes` | shots.md → API clips (PAID — founder go only) |
| `python3 pipeline/t3-trials/intake.py <file> <platform> <A\|B\|C>` | archive a manual trial clip w/ provenance |

Growing the tree (fully sanctioned, no permission needed — Guideline 1):
node dir under `genomes/sapling/nodes/` (`node.md` with R1 state change + R5
hook, `leaves/`, `sap/`), entry in `lineage.yaml` with `parent:`, reactions
issue (see any `sap/reactions.yaml`), T1+T2 render, lint, push. Cite taste
rules (`taste/sapling.founder.v0.2.md`); label model provenance.

## Render routes (2026-07-19, verified — `pipeline/t3-trials/free-routes.md`)

Free path chosen: **Alibaba Model Studio (DashScope Singapore)** — wan2.7
API, native 9:16, watermark-off default, ~1,650 free video-seconds for new
accounts (90 days, no card; amount needs console confirmation). Adapter
live: `generate_shots.py --provider wan` (+`--quota-covered` ledger mode,
founder-attested, still behind `--yes`). Permanent $0 floor:
`pipeline/kaggle/wan-t2v-kaggle.ipynb` (open Wan 1.3B on free Kaggle GPU).
**DONE 2026-07-20 (small hours):** THE WHOLE TRUNK IS FILMED AND LIVE.
001-t3-b (founder-released, v2 cut) + 002b/003b/004/005 t3-a leaves — all
anime, full-cast kokoro dialogue, manifest-synced captions, faststart,
$0 billed (~$21 list, all provider free quota, ledgered). Founder screened
every episode. Remaining wan quota ≈ 130s (wan2.1/2.2 mostly + scraps).
T3 v2 fitting: slots fit material, footage loops (never freezes), dialogue
never trimmed. Parser hardened twice (speaker-colon rule; headings require
timing ranges). Voice upgrade (emotional TTS — CosyVoice on same quota)
parked: founder said voice doesn't matter for now; dad wants human touch
eventually. NEXT: founder posts (kit §4), 006 trunk call, fork episodes'
T3, watering rail (D5).
Do NOT suggest multi-account quota cycling — declined on ToS + provenance
grounds, founder accepted.

## State (2026-07-19, night)

Launched 2026-07-18: node 001 flagship T3 leaf live (founder's manual
Veo/Flow clips beats 1/2/4; beats 3/5 are designed slates — prompts ready in
`.../001-capability-inventory/shots.md`). **16 nodes**, all with T0/T1/T2.
Tree tip is a live R4 fork, now one episode deep per side: **006a "The
Miracle Clause" → 007a "The Demo"** vs **006b "Reconciliation" → 007b "The
Hearth"** (issues #13–#16) — **trunk call awaits the founder**, felt on
material per edl.md 2026-07-19. Founder decided 2026-07-19: **no social
distribution yet** — keep building; `distribution/launch-kit.md` holds
ready draft copy for when that changes. **Every trunk node (001, 002b, 003b,
004, 005) has a complete shots.md** — 21 prompts; one funded D8 afternoon =
a five-episode season. Sap cron was silently failing 07-15→07-19 (unmatched
screening.yaml pathspec); fixed and verified green. Trials scored (objective
axes only) at `/trials/`. Open founder decisions: 006 trunk call, D8, D9,
taste scores, watering rail. **Style is v2: low-detail anime** (founder
call 2026-07-19; `genomes/sapling/style.md` is the visual bible) — all shot
prompts rewritten; 001's photoreal Veo clips are archived v1 evidence; D8
bake-off should re-run on anime prompts. **T2 renderer is v2 + voice**:
kinetic-text cut (one shot per script element, Ken Burns, title cards)
voiced end-to-end by kokoro-82M local TTS — per-character cast in
`genomes/sapling/voices.yaml` (founder-amendable, R4), narrator for stage
directions, wind bed, loudnorm; ~2-3min/episode, $0. Site leads node pages
with Watch; homepage shows a lineage-derived live-fork banner.

Local dev: T2 stills need `T2_NPM_DIR` → dir with `npm install playwright`;
voice needs `T2_TTS_PYTHON` → python3.13 venv with `pip install kokoro-onnx
soundfile` + model files in `~/.cache/banyan-tts/` (kokoro-v1.0.onnx,
voices-v1.0.bin — free download, kokoro-onnx GitHub releases; tts_kokoro.py
self-heals the espeak data-path quirk). Pipeline python deps in a venv
(markdown, pyyaml, pillow, imageio-ffmpeg). Run tests as their own step and
read the exit code BEFORE committing — piping to tail masks failures (this
bit twice on 2026-07-19).
