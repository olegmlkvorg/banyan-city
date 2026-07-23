"""Caption chunking shared by render_t3 (burn-in) and synth_vo (timing).

Whole VO lines burned in as 4-6-line paragraph blocks read as homework on a
phone (loop cycle 001, defects 8/11/12): captions are short phrase units.
Lives in its own module so the TTS venv can import it without pillow."""

import re

CAPTION_MAX_WORDS = 7


def caption_chunks(text: str, max_words: int = CAPTION_MAX_WORDS) -> list:
    """Split a line into caption units: on sentence ends, then clause marks,
    then a hard word cap, so each unit rasterizes to <=2 lines at caption
    size. Never loses or reorders a word."""
    units = []
    for sent in re.split(r"(?<=[.!?…])\s+", text.strip()):
        if not sent.split():
            continue
        buf = []
        # a mid-line em dash ends its clause but stays VISIBLE (it carries
        # tone): \x00 marks the split point after it
        for clause in re.split(r"(?<=[,;:])\s+|\x00",
                               re.sub(r"\s+—\s+", " —\x00", sent)):
            for word in clause.split():
                buf.append(word)
                if len(buf) == max_words:
                    units.append(" ".join(buf))
                    buf = []
            # a clause end past half the cap is a natural caption break
            if len(buf) > max_words // 2:
                units.append(" ".join(buf))
                buf = []
        if buf:
            units.append(" ".join(buf))
        # fold a 1-2 word orphan into its predecessor
        if (len(units) >= 2 and len(units[-1].split()) <= 2
                and len(units[-2].split()) + len(units[-1].split()) <= max_words + 2):
            orphan = units.pop()
            units[-1] += " " + orphan
    return units or [text.strip()]


def chunk_spans(text: str, w0: float, w1: float) -> list:
    """Chunk a (display-ready) line and time each unit inside the window
    [w0, w1], proportional to word count: (chunk, start, end) triples.
    A word-count ESTIMATE — synth_vo writes measured timings into the VO
    manifest, which render_t3 prefers whenever present."""
    chunks = caption_chunks(text)
    total = sum(len(c.split()) for c in chunks) or 1
    spans, t = [], w0
    for c in chunks:
        dt = (w1 - w0) * len(c.split()) / total
        spans.append((c, t, t + dt))
        t += dt
    return spans
