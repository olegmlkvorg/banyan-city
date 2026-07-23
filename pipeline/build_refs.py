#!/usr/bin/env python3
"""Reference voices for Chatterbox cloning — identity continuity across
the engine swap. Each voice in the genome's voices.yaml cast (plus the
narrator and default pool) gets ~10s of kokoro speech saved to
~/.cache/banyan-tts/cb-refs/<voice>.wav; synth_vo --engine chatterbox
clones from these, so the tree still sounds like the tree (R4: the cast
is the founder's; this preserves it rather than recasting).

Runs under the kokoro TTS venv:
    <tts-venv>/bin/python3 pipeline/build_refs.py <genome>
"""

import sys
from pathlib import Path

import soundfile as sf
import yaml

REPO = Path(__file__).resolve().parent.parent
CACHE = Path.home() / ".cache" / "banyan-tts"

# neutral storyteller passage: long enough to carry timbre and cadence,
# no strong emotion for the clone to latch onto
REF_TEXT = ("The town was quiet that evening. Someone had left a lantern "
            "burning by the gate, and the light moved a little in the wind. "
            "Nobody knew yet what the morning would bring, but the fields "
            "were watered, the ledger was balanced, and for one long moment "
            "everything simply held still.")


def main() -> int:
    if len(sys.argv) != 2:
        raise SystemExit(__doc__)
    from kokoro_onnx import Kokoro
    k = Kokoro(str(CACHE / "kokoro-v1.0.onnx"), str(CACHE / "voices-v1.0.bin"))
    vcfg = yaml.safe_load((REPO / "genomes" / sys.argv[1] / "voices.yaml").read_text())

    voices = {vcfg.get("narrator", "af_sarah")}
    voices.update(vcfg.get("default_pool") or [])
    for entry in (vcfg.get("cast") or {}).values():
        voices.add(entry["voice"])

    out = CACHE / "cb-refs"
    out.mkdir(parents=True, exist_ok=True)
    for v in sorted(voices):
        samples, sr = k.create(REF_TEXT, voice=v, speed=1.0, lang="en-us")
        sf.write(str(out / f"{v}.wav"), samples, sr)
        print(f"ref {v}: {len(samples) / sr:.1f}s")
    print(f"✓ {len(voices)} reference voices in {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
