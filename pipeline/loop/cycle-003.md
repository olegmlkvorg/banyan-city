# Loop cycle 003 — the acting engine (2026-07-23)

Opened by the founder's verdict on cycle 002's v4: **"i dont see a
difference"** — and the directive **"take your time and figure out a way
to upgrade the voice."** Cycle 002 fixed rhythm; the ceiling was the
engine. kokoro-82M has no emotion control at all.

## Engine choice

Tested empirically on the founder's M1 Pro (32 GB): **Chatterbox 0.5B**
(Resemble AI, MIT) on Apple-Silicon MPS — ~3x realtime after warmup,
fully local, $0. Chosen for: explicit per-line emotion control
(exaggeration/cfg), zero-shot voice cloning, permissive license, and it
runs on hardware we own. (CosyVoice2/Orpheus-class models need a bigger
GPU; the Kaggle free-GPU route stays available as scale-out.)

## What was built

- `synth_vo.py` v2 — engine abstraction (kokoro | chatterbox), per-line
  **emotion direction** from script cues: parenthetical hints
  ('(quiet)', '(panicking)', '(without emotion)'), punctuation shape,
  caps emphasis → exaggeration/cfg. Deterministic per-line seeds so
  takes are reproducible (provenance).
- `build_refs.py` — per-voice reference wavs synthesized FROM the kokoro
  cast (~/.cache/banyan-tts/cb-refs/): the founder's casting (R4) is
  preserved across the engine swap, not recast.
- Setup notes: cb-venv python3.11, `chatterbox-tts` + `setuptools<81`
  (perth watermarker needs pkg_resources), torch.load mapped to cpu,
  `torch.mps.empty_cache()` after every take (long dialogue beats
  otherwise die by silent SIGKILL — found on 002b, the season's longest
  dialogue beat). Perth watermark kept — responsible-AI feature.

## Verdicts and rollout

- Founder heard the 3-way line test (kokoro / neutral / acted): engine
  adopted for the bench.
- Founder on ep-001 v5 full re-voice: **"it is improving for sure"** —
  KEPT, rolled to the season.
- All episodes re-voiced at $0: 003b–007a clean; caption-wall regression
  caught on 004's QA frames (chunker orphan-fold cascade — fixed,
  regression-tested, 004 re-taken); 002b in progress (SIGKILL fix).
- Drop staging moved to `~/Desktop/banyan-drops/` — an auto-organizer
  sweeps ~/Downloads and renames staged files.

## Carried forward

Emotion direction is still *rule-based* (punctuation + parentheticals).
The scripts under-specify performance; a future cycle could add explicit
per-line direction cues to the script grammar (an R4-adjacent question —
direction is taste).
