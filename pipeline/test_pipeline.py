#!/usr/bin/env python3
"""Fast, dependency-light tests for the render pipeline's parsing logic.

No ffmpeg, no chromium, no network — pure functions only, so this runs in CI
next to lint_genome.py. Catches the silent-corruption regressions: a broken
beat-timing regex or clip-naming rule would mis-time or drop episode footage
without any error. Run: python3 pipeline/test_pipeline.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import render_t3 as t3
from render_t1 import extract_script, parse_frames

REPO = Path(__file__).resolve().parent.parent
FAILURES = []


def check(name, cond):
    print(("  ok  " if cond else "FAIL  ") + name)
    if not cond:
        FAILURES.append(name)


def test_beat_duration_from_timecode():
    # `SLUG — 0:00–0:12` → 12.0s exactly (en-dash separator)
    check("timecode 0:00–0:12 → 12.0", t3.beat_duration("COLD OPEN — 0:00–0:12", []) == 12.0)
    check("timecode 1:05–1:25 → 20.0", t3.beat_duration("HOOK — 1:05–1:25", []) == 20.0)
    check("hyphen separator 0:28-0:40 → 12.0", t3.beat_duration("X — 0:28-0:40", []) == 12.0)


def test_beat_duration_fallback():
    # no timecode → reading-speed estimate, clamped to [MIN, MAX]
    d_empty = t3.beat_duration("NO TIME", [])
    check("empty beat clamps to MIN_SEC", d_empty == t3.MIN_SEC)
    long_items = [("line", "", "x" * 500)]
    check("long beat clamps to MAX_SEC", t3.beat_duration("NO TIME", long_items) == t3.MAX_SEC)


def test_find_clip_naming(tmp: Path):
    (tmp / "01-cold-open.mp4").write_bytes(b"x")
    (tmp / "04.mp4").write_bytes(b"x")
    check("finds NN-slug.mp4", t3.find_clip(tmp, 1) is not None)
    check("finds bare NN.mp4", t3.find_clip(tmp, 4) is not None)
    check("missing beat → None", t3.find_clip(tmp, 2) is None)
    check("no clips dir → None", t3.find_clip(None, 1) is None)


def test_wrap_never_drops_words():
    font = t3.mono_font(24)
    text = "SENSE roots air vibration and several more words here to force wrapping"
    wrapped = t3.wrap(text, font, 200)
    joined = " ".join(wrapped).split()
    check("wrap preserves all words", joined == text.split())


def test_node_001_beats_parse():
    md = (REPO / "genomes/sapling/nodes/001-capability-inventory/node.md").read_text()
    beats = parse_frames(extract_script(md))
    check("node 001 parses 5 beats", len(beats) == 5)
    total = sum(t3.beat_duration(b["slug"], b["items"]) for b in beats)
    check("node 001 total ≈ 85s script time", total == 85.0)
    # every beat has a nonempty slug
    check("all beats have slugs", all(b["slug"].strip() for b in beats))


def main():
    import tempfile
    test_beat_duration_from_timecode()
    test_beat_duration_fallback()
    with tempfile.TemporaryDirectory() as td:
        test_find_clip_naming(Path(td))
    test_wrap_never_drops_words()
    test_node_001_beats_parse()
    print()
    if FAILURES:
        print(f"✗ {len(FAILURES)} failure(s): {', '.join(FAILURES)}")
        return 1
    print("✓ all pipeline tests passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
