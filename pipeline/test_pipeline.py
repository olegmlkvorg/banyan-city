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

import render_t2 as t2
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


def test_find_audio_naming(tmp: Path):
    (tmp / "01-vo.mp3").write_bytes(b"x")
    (tmp / "03.wav").write_bytes(b"x")
    check("finds NN-*.mp3 audio", t3.find_audio(tmp, 1) is not None)
    check("finds bare NN.wav audio", t3.find_audio(tmp, 3) is not None)
    check("beat without audio → None", t3.find_audio(tmp, 2) is None)
    check("no clips dir → None audio", t3.find_audio(None, 1) is None)


def test_wrap_never_drops_words():
    font = t3.mono_font(24)
    text = "SENSE roots air vibration and several more words here to force wrapping"
    wrapped = t3.wrap(text, font, 200)
    joined = " ".join(wrapped).split()
    check("wrap preserves all words", joined == text.split())


def test_parse_frames_bold_emphasis_in_quote():
    # regression: a quote line opening with bold emphasis ('> **fires**. rest')
    # is a wrapped speech continuation — only a colon marks a new speaker
    md = ("**SCENE — 0:00–0:12**\n"
          "\n"
          "> **ROOT:** the line before\n"
          "> **fires**. rest of the sentence\n")
    items = parse_frames(md)[0]["items"]
    check("colon quote parses as speaker line", items[0] == ("line", "ROOT", "the line before"))
    check("bold-emphasis quote is speakerless", items[1][:2] == ("line", ""))
    check("bold-emphasis quote keeps its text", items[1][2] == "**fires**. rest of the sentence")


def test_parse_frames_bold_line_needs_timing():
    # regression: a full-bold line is a beat heading only WITH a timing range;
    # without one it is emphasis inside the scene → action item
    md = ("**SCENE — 0:00–0:12**\n"
          "\n"
          "**Both leaves tilt at once.**\n"
          "\n"
          "**NEXT BEAT — 0:12–0:20**\n")
    frames = parse_frames(md)
    check("bold line without timing is not a beat", len(frames) == 2)
    check("bold line without timing becomes action",
          frames[0]["items"] == [("action", "Both leaves tilt at once.")])
    check("bold line with timing is a beat", frames[1]["slug"] == "NEXT BEAT — 0:12–0:20")


def test_build_shots_merges_continuations():
    # regression: a wrapped speech (speakerless quote continuations, incl. one
    # opening with bold emphasis) stays one card — no mid-sentence cuts
    md = ("**SCENE — 0:00–0:12**\n"
          "\n"
          "> **ROOT:** The survey says the lot is empty. It\n"
          "> **lies**. Someone lives in every ring\n"
          "> of this trunk.\n")
    shots = t2.build_shots(parse_frames(md), "test-node")
    spoken = [s for s in shots if s["type"] in ("line", "vo")]
    check("wrapped speech is one card", len(spoken) == 1)
    check("merged card keeps its speaker", spoken[0]["who"] == "ROOT")
    check("merged card keeps the whole sentence",
          spoken[0]["text"] == "The survey says the lot is empty. It lies. "
                               "Someone lives in every ring of this trunk.")
    check("merged card re-times to the full text",
          spoken[0]["dur"] == t2.clamp(1.4, len(spoken[0]["text"]) / 18.0, 6.0))


def test_overlay_font_px():
    # regression: an 80-col terminal line must fit the ~578px card interior
    # (mono glyphs ≈ 0.62em); short lines cap at 17px, never balloon
    wide = "x" * 80
    px = t2.overlay_font_px(wide)
    check("80-col line fits the card", px <= 578 / (80 * 0.62))
    check("80-col line stays legible (>=9px)", px >= 9)
    check("widest line drives the size", t2.overlay_font_px("short\n" + wide) == px)
    check("short lines cap at 17px", t2.overlay_font_px("$ leaf status") == 17)


def test_speaker_key_strips_parentheticals():
    # regression: '(writing)' is a stage direction, not part of the cast key
    check("parenthetical stripped", t2.speaker_key("ASSESSOR (writing)") == "ASSESSOR")
    check("multi-word parenthetical stripped",
          t2.speaker_key("ASSESSOR (writing, without emotion)") == "ASSESSOR")
    check("plain speaker normalizes upper", t2.speaker_key(" root ") == "ROOT")


def test_clean_speech_drops_parentheticals():
    # regression: the voice must not read stage directions aloud
    check("stage parentheticals dropped",
          t2.clean_speech("(beat) I heard it. (softly) Everything.") == "I heard it. Everything.")
    check("plain speech untouched", t2.clean_speech("I heard it.") == "I heard it.")


def test_node_001_beats_parse():
    md = (REPO / "genomes/sapling/nodes/001-capability-inventory/node.md").read_text()
    beats = parse_frames(extract_script(md))
    check("node 001 parses 5 beats", len(beats) == 5)
    total = sum(t3.beat_duration(b["slug"], b["items"]) for b in beats)
    check("node 001 total ≈ 85s script time", total == 85.0)
    # every beat has a nonempty slug
    check("all beats have slugs", all(b["slug"].strip() for b in beats))


def test_shot_prompt_extraction():
    # intake pulls the verbatim prompt for a shot out of prompts.md; shot C's
    # prompt contains a colon ("stylized shot:") — the bug that broke the
    # hand-built meta YAML. Assert it round-trips through yaml cleanly.
    import yaml
    sys.path.insert(0, str(REPO / "pipeline" / "t3-trials"))
    import intake
    for shot in ("A", "B", "C"):
        prompt = intake.shot_prompt(shot)
        check(f"shot {shot} prompt nonempty", len(prompt) > 40)
        # emulate intake's serialization and confirm it parses back
        dumped = yaml.safe_dump({"prompt": prompt})
        check(f"shot {shot} prompt survives YAML", yaml.safe_load(dumped)["prompt"] == prompt)


def test_generate_shots_parsing():
    # the API driver must see every beat + verbatim prompt in shots.md;
    # a silent parse miss would skip a beat and ship an episode with a hole
    from generate_shots import parse_shots
    md = (REPO / "genomes/sapling/nodes/001-capability-inventory/shots.md").read_text()
    shots = parse_shots(md)
    check("shots.md parses 5 beats", len(shots) == 5)
    check("beat numbering 1..5", [s["num"] for s in shots] == [1, 2, 3, 4, 5])
    check("prompts nonempty + vertical", all("9:16" in s["prompt"] for s in shots))
    # style v2 (2026-07-19) reset all 001 beats to needs-footage: the v1
    # photoreal clips are archived evidence, not v2 footage — so no beat
    # parses as done until anime clips exist
    check("done-status parsed", [s["done"] for s in shots] == [False] * 5)


def test_budget_guard():
    # money-drain protection: pricing must resolve, unknown models must price
    # PESSIMISTICALLY, and the caps file must parse with sane values
    import generate_shots as gs
    check("veo fast rate", gs.price_per_sec("fal-ai/veo3.1/fast") == 0.15)
    check("kling turbo rate", gs.price_per_sec("fal-ai/kling-video/v3/turbo/standard/text-to-video") == 0.112)
    check("unknown model prices at max", gs.price_per_sec("brand-new-model-x") == gs.FALLBACK_PRICE)
    # wan family: specific versions price above the generic fal-wan entry, and
    # ordering in the table must let the specific fragments win
    check("wan2.7 rate", gs.price_per_sec("wan2.7-t2v") == 0.10)
    check("wan2.6 rate", gs.price_per_sec("wan2.6-t2v") == 0.15)
    check("generic wan rate", gs.price_per_sec("fal-ai/wan-25/text-to-video") == 0.05)
    check("wan provider registered", "wan" in gs.PROVIDERS)
    caps = gs.budget()
    check("caps parse + per-run <= lifetime",
          0 < caps["hard_cap_per_run_usd"] <= caps["hard_cap_total_usd"])


def test_all_leaf_content_exists():
    # every leaf's declared content file must exist on disk — the guarantee the
    # lint content-check enforces, verified here against the real genome so a
    # renamed/deleted artifact fails fast (dead site links otherwise)
    import yaml
    gdir = REPO / "genomes" / "sapling"
    lineage = yaml.safe_load((gdir / "lineage.yaml").read_text())
    ok = True
    for n in lineage["nodes"]:
        ndir = gdir / "nodes" / n["slug"]
        for leaf_id in n.get("leaves") or []:
            meta = yaml.safe_load((ndir / "leaves" / f"{leaf_id}.yaml").read_text())
            content = str(meta.get("content", ""))
            if content and content != "../node.md" and not (ndir / "leaves" / content).exists():
                print(f"      missing content: {n['id']}/{leaf_id} -> {content}")
                ok = False
    check("every leaf content file exists on disk", ok)


def test_trials_page_renders():
    # build_site.render_trials must not crash (populated or empty) and must
    # carry the core sections (regression guard for the /trials/ page)
    sys.path.insert(0, str(REPO / "pipeline"))
    import build_site
    html = build_site.render_trials()
    check("trials page renders", "T3 platform trials" in html)
    check("trials page has prompts section", "three prompts" in html)


def main():
    import tempfile
    test_beat_duration_from_timecode()
    test_beat_duration_fallback()
    with tempfile.TemporaryDirectory() as td:
        test_find_clip_naming(Path(td))
    with tempfile.TemporaryDirectory() as td:
        test_find_audio_naming(Path(td))
    test_wrap_never_drops_words()
    test_parse_frames_bold_emphasis_in_quote()
    test_parse_frames_bold_line_needs_timing()
    test_build_shots_merges_continuations()
    test_overlay_font_px()
    test_speaker_key_strips_parentheticals()
    test_clean_speech_drops_parentheticals()
    test_node_001_beats_parse()
    test_shot_prompt_extraction()
    test_generate_shots_parsing()
    test_budget_guard()
    test_all_leaf_content_exists()
    test_trials_page_renders()
    print()
    if FAILURES:
        print(f"✗ {len(FAILURES)} failure(s): {', '.join(FAILURES)}")
        return 1
    print("✓ all pipeline tests passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
