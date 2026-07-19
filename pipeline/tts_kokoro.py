#!/usr/bin/env python3
"""Kokoro TTS worker — local neural narration at $0 (the voice rung of §7.4).

Runs under a python environment with kokoro-onnx + soundfile installed and
model files in ~/.cache/banyan-tts/ (kokoro-v1.0.onnx, voices-v1.0.bin —
one-time free download from the kokoro-onnx GitHub releases). render_t2.py
invokes it via the T2_TTS_PYTHON env var so the render pipeline's own python
doesn't need onnxruntime.

Usage: tts_kokoro.py <job.json> <outdir>
  job.json: [{"i": <shot index>, "text": str, "voice": str, "speed": float}]
  writes:   <outdir>/vo-<i>.wav per job + <outdir>/durations.json
"""
import json
import sys
from pathlib import Path


def heal_espeak_data() -> None:
    """Some espeak-ng builds resolve phoneme data at the espeakng_loader
    package root instead of its espeak-ng-data/ subdir; symlink the data
    files up one level so both layouts work."""
    import espeakng_loader
    data = Path(espeakng_loader.get_data_path())
    pkg = data.parent
    if not (pkg / "phontab").exists():
        for f in data.iterdir():
            target = pkg / f.name
            if not target.exists():
                target.symlink_to(f)


def main() -> None:
    if len(sys.argv) != 3:
        raise SystemExit(__doc__)
    job_file, outdir = Path(sys.argv[1]), Path(sys.argv[2])
    heal_espeak_data()
    import soundfile as sf
    from kokoro_onnx import Kokoro

    models = Path.home() / ".cache" / "banyan-tts"
    kokoro = Kokoro(str(models / "kokoro-v1.0.onnx"), str(models / "voices-v1.0.bin"))
    jobs = json.loads(job_file.read_text())
    durations = {}
    for j in jobs:
        samples, sr = kokoro.create(j["text"], voice=j["voice"],
                                    speed=j.get("speed", 1.0), lang="en-us")
        sf.write(str(outdir / f"vo-{j['i']:03d}.wav"), samples, sr)
        durations[str(j["i"])] = round(len(samples) / sr, 3)
    (outdir / "durations.json").write_text(json.dumps(durations))
    print(f"synthesized {len(jobs)} segments")


if __name__ == "__main__":
    main()
