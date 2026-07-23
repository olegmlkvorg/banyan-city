#!/usr/bin/env python3
"""Directed VO synthesis — the voice track with performance direction.

Promoted from the one-off scratchpad make-vo scripts after loop cycle 002
opened (founder winces 2026-07-23: captions drift off the voice; delivery
is metronome-flat). Same kokoro-82M local synthesis ($0), three upgrades:

  trim       kokoro pads every line with engine silence; head/tail are
             trimmed so every pause below is authored, not an artifact
             (cycle-001 defect 14: constant ~0.9s gaps everywhere)
  direction  deterministic delivery from script structure: gaps follow
             dramatic intent — a standalone 'Beat.' stage direction
             breathes ~1.2s, rapid short exchanges snap at ~0.18s,
             trailing ellipses/dashes hang shorter than sentence ends —
             and per-line speed eases with punctuation shape
  chunks     each caption chunk (pipeline/captions.py) is synthesized solo
             to MEASURE its spoken length, then mapped into the line's
             real speech window and written to the manifest as
             lines[].chunks — render_t3 burns captions on the voice, not
             on a word-count guess

kokoro has no true emotion control: this fixes rhythm, not acting. The
acting upgrade (emotional TTS on a free GPU) is tracked in the loop.

Writes NN-vo.mp3 + NN-vo.json into the node's clips dir; existing takes
are archived to clips/vo-archive/ first (R6: nothing deleted). Runs under
the TTS venv (kokoro-onnx, soundfile, numpy):

    <tts-venv>/bin/python3 pipeline/synth_vo.py <ffmpeg> <genome> <slug> […]
"""

import json
import subprocess
import sys
from pathlib import Path

import numpy as np
import soundfile as sf

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO / "pipeline"))
from captions import caption_chunks  # noqa: E402
from render_t1 import extract_script, parse_frames, strip_inline_md  # noqa: E402
from render_t2 import clean_speech, load_voices, speaker_key, voice_for  # noqa: E402

GAP_DEFAULT, GAP_TRAIL, GAP_SNAP, GAP_BEAT = 0.50, 0.35, 0.18, 1.2
SNAP_WORDS = 4          # both lines this short → rapid exchange
TRIM_THRESH = 0.003     # amplitude floor for head/tail engine silence
TRIM_PAD_S = 0.04


def trim_silence(x: np.ndarray, sr: int) -> np.ndarray:
    idx = np.where(np.abs(x) > TRIM_THRESH)[0]
    if not len(idx):
        return x
    a = max(0, int(idx[0]) - int(TRIM_PAD_S * sr))
    b = min(len(x), int(idx[-1]) + int(TRIM_PAD_S * sr))
    return x[a:b]


def pacing(base: float, who: str, text: str) -> float:
    """Per-line speed from delivery hints and punctuation shape."""
    spd = base
    if any(w in who.lower() for w in ("quiet", "whisper", "small")):
        spd = max(0.92, spd - 0.10)
    if text.rstrip().endswith(("?", "!")) or "??" in text:
        spd += 0.07
    if text.strip().startswith(("…", "...")):
        spd -= 0.04
    if len(text.split()) <= 3:
        spd -= 0.03  # short lines land, they don't rush
    return spd


def gap_before(prev_text: str | None, cur_text: str, beat_pause: bool) -> float:
    """The pause a line takes before speaking, from script intent."""
    if prev_text is None:
        return 0.0
    if beat_pause:
        return GAP_BEAT
    if (len(prev_text.split()) <= SNAP_WORDS
            and len(cur_text.split()) <= SNAP_WORDS):
        return GAP_SNAP
    if prev_text.rstrip().endswith(("…", "...", "—", ",")):
        return GAP_TRAIL
    return GAP_DEFAULT


def is_beat_pause(action_text: str) -> bool:
    """A standalone 'Beat.' / 'A beat.' stage direction is a scripted
    breath (cycle-001 defect 14: the render dropped it entirely)."""
    return bool(action_text) and action_text.strip().rstrip(".").lower() in ("beat", "a beat")


def measured_chunks(k, text: str, voice: str, spd: float,
                    start: float, end: float) -> list:
    """Caption chunks timed by their own measured synthesis, scaled into
    the line's real speech window [start, end]."""
    chunks = caption_chunks(strip_inline_md(text))
    if len(chunks) == 1:
        return [{"text": chunks[0], "start": round(start, 3), "end": round(end, 3)}]
    durs = []
    for c in chunks:
        speak = clean_speech(c) or c
        samples, sr = k.create(speak, voice=voice, speed=spd, lang="en-us")
        durs.append(len(trim_silence(np.asarray(samples), sr)) / sr)
    total = sum(durs) or 1.0
    spans, t = [], start
    for c, d in zip(chunks, durs):
        dt = (end - start) * d / total
        spans.append({"text": c, "start": round(t, 3), "end": round(t + dt, 3)})
        t += dt
    return spans


def archive(clips_dir: Path, beat_num: int) -> None:
    arch = clips_dir / "vo-archive"
    for ext in ("mp3", "json"):
        old = clips_dir / f"{beat_num:02d}-vo.{ext}"
        if not old.exists():
            continue
        arch.mkdir(exist_ok=True)
        dest, n = arch / old.name, 2
        while dest.exists():
            dest = arch / f"{old.stem}.v{n}.{ext}"
            n += 1
        old.rename(dest)


def main() -> int:
    if len(sys.argv) < 4:
        raise SystemExit(__doc__)
    ff, genome = sys.argv[1], sys.argv[2]
    from kokoro_onnx import Kokoro
    m = Path.home() / ".cache" / "banyan-tts"
    k = Kokoro(str(m / "kokoro-v1.0.onnx"), str(m / "voices-v1.0.bin"))
    genome_dir = REPO / "genomes" / genome
    vcfg = load_voices(genome_dir)

    for slug in sys.argv[3:]:
        node_dir = genome_dir / "nodes" / slug
        frames = parse_frames(extract_script((node_dir / "node.md").read_text()))
        clips_dir = node_dir / "clips"
        clips_dir.mkdir(exist_ok=True)
        for beat_num, f in enumerate(frames, start=1):
            # walk items in order: lines speak; a 'Beat.' action between
            # lines becomes the next line's breath
            entries, pending_beat = [], False
            for it in f["items"]:
                if it[0] == "action":
                    pending_beat = pending_beat or is_beat_pause(strip_inline_md(it[1]))
                elif it[0] == "line":
                    text = strip_inline_md(it[2])
                    if clean_speech(text):
                        entries.append((it[1], text, pending_beat))
                        pending_beat = False
            if not entries:
                continue

            sr, pieces, manifest, cursor, prev_text = 24000, [], [], 0.0, None
            for raw_who, text, beat_pause in entries:
                who = speaker_key(raw_who) or "VO"
                voice, base = voice_for(who, vcfg)
                spd = pacing(base, raw_who, text)
                samples, sr = k.create(clean_speech(text), voice=voice,
                                       speed=spd, lang="en-us")
                samples = trim_silence(np.asarray(samples), sr)
                gap = gap_before(prev_text, text, beat_pause)
                if gap:
                    pieces.append(np.zeros(int(gap * sr), dtype=samples.dtype))
                    cursor += gap
                start = cursor
                cursor += len(samples) / sr
                manifest.append({
                    "who": who, "text": text,
                    "start": round(start, 3), "end": round(cursor, 3),
                    "chunks": measured_chunks(k, text, voice, spd, start, cursor),
                })
                pieces.append(samples)
                prev_text = text
            # short settle so the last word never clips at the beat edge
            pieces.append(np.zeros(int(0.30 * sr), dtype=pieces[-1].dtype))
            cursor += 0.30

            archive(clips_dir, beat_num)
            audio = np.concatenate(pieces)
            wav = clips_dir / "tmp.wav"
            sf.write(str(wav), audio, sr)
            mp3 = clips_dir / f"{beat_num:02d}-vo.mp3"
            subprocess.run([ff, "-y", "-loglevel", "error", "-i", str(wav),
                            "-c:a", "libmp3lame", "-q:a", "4", str(mp3)], check=True)
            wav.unlink()
            (clips_dir / f"{beat_num:02d}-vo.json").write_text(json.dumps(
                {"cast": "voices.yaml", "directed": "synth_vo v1",
                 "lines": manifest, "total_s": round(cursor, 3)}, indent=1))
            print(f"{slug} beat {beat_num:02d}: {len(entries)} lines, {cursor:.1f}s")
    print("VO_DONE")
    return 0


if __name__ == "__main__":
    sys.exit(main())
