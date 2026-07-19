# Node 005 — shot list (per-beat generation prompts)

The whole episode as a shot list — one generation prompt per script beat, for
end-to-end rendering and assembly by `pipeline/render_t3.py`. Same rules as
node 001's list: base footage only (no burned-in text, no spoken dialogue —
post adds caption overlays and VO), 9:16 vertical, ~10s per shot, one take.

**Character continuity (paste into any beat that shows them):** the assessor
is a thin precise man in dust-grey robes with a heavy ledger chained to his
belt and a quill worn to a stub. The scavenger is a small goblin — big ears,
patchwork cloak, one broken tusk. The farmer is a weathered middle-aged man
in plain work clothes. The sapling is ~50cm with a handful of leaves; beside
it a crooked lean-to, a three-stone cairn, and a clay jug.

**Naming for assembly:** save each clip as `NN-slug.mp4` in a clips dir, then:
`python3 pipeline/render_t3.py sapling 005 --clips <dir> --out episode.mp4`
Missing beats render as slates; partial lists still assemble.

Status legend: ✅ generated · ⬜ needs footage

---

## Beat 01 — COLD OPEN / THE METRONOME (0:00–0:10) ⬜ needs footage

Script beat: dawn over Shade, wide and peaceful — and the assessor entering
down the exact center of the road, counting under his breath before a word.

```
Vertical 9:16 wide cinematic shot, dawn. A tiny settlement in an enormous field: a 50cm sapling, a crooked lean-to, a three-stone cairn, a clay jug, all golden in first light. Down a dirt road toward it walks a thin, precise man in dust-grey robes, a heavy ledger chained to his belt — walking the exact center of the road with metronome regularity, unhurried and inevitable. He stops at the clearing's edge, lips moving as he counts under his breath. Photoreal fantasy, soft dawn grade, static camera, quietly comedic menace, no text.
```

## Beat 02 — THE ASSESSMENT (0:10–0:45) ⬜ needs footage

Script beat: rapid-fire deadpan fieldwork — knotted string measuring the
lean-to, the cairn counted stone by stone, the string held against the trunk;
the scavenger orbiting in rising panic, the farmer stonewalling.

```
Vertical 9:16 cinematic montage-style shot, morning. A thin man in dust-grey robes with a chained ledger methodically surveys a tiny settlement: he measures a crooked lean-to with a knotted string, counts a three-stone cairn one stone at a time with his finger, and holds the string up against the pencil-thin trunk of a 50cm sapling. A small goblin with big ears and a patchwork cloak orbits him in rising panic, gesturing; a weathered farmer stands with arms crossed, giving nothing. The assessor writes in the ledger without ever changing expression. Deadpan bureaucratic comedy, photoreal fantasy, bright morning light, no text.
```

## Beat 03 — THE FORM FAILS (0:45–1:05) ⬜ needs footage

Script beat: the settlement schema visibly defeats him — the damp field line,
the mended channel, and the two-second montage revealing he's been watching
leaves move in still air all along.

```
Vertical 9:16 cinematic shot, late morning. A thin man in dust-grey robes stands with quill frozen above his ledger, staring at a dark damp irrigation line running through green grass toward a tiny sapling — a channel that should not have mended itself. His eyes move slowly from the wet field line, to the weathered farmer's blank face, to the little tree. Close on the assessor's eyes narrowing: quick flash cuts of the sapling's leaves tilting in dead-still air, seen from his point of view at different moments of the day. He has been counting everything. Photoreal fantasy, tense quiet, muted grade, no text.
```

## Beat 04 — THE QUESTION (1:05–1:25) ⬜ needs footage

Script beat: he addresses the tree with exhausted professionalism —
"Occupation?" — one leaf tilts; he writes one line we never see, chains the
ledger, and leaves, pausing precisely where he entered. Long hold on the tree.

```
Vertical 9:16 cinematic shot, midday. A thin precise man in dust-grey robes walks up to a 50cm sapling, adjusts his robes, and addresses the little tree directly and formally, ledger open. A small goblin and a weathered farmer watch, frozen, holding their breath in the background. On the sapling, one leaf slowly, deliberately tilts. The man nods as if that were an answer, writes a single line in the ledger, closes it, and chains it shut to his belt. He walks away down the road; the shot holds long on the tiny tree alone in the frame. Photoreal fantasy, dry comedic gravity, bright flat light, slow push-in at the end, no text.
```

---

## Progress

0 of 4 beats generated. Generating footage is a paid action wherever it runs —
a founder call per the spend rules (STEWARDSHIP.md §4, `pipeline/budget.yaml`).
Platform choice tracks [D8](../../../../DECISIONS.md). Provenance for any
generated beat goes in a sibling `NN-slug.meta.yaml` (platform, model, prompt,
cost) so `render_t3.py` records per-beat sources in the T3 leaf.

With this file, every trunk node (001, 002b, 003b, 004, 005) has a complete
shot list: **21 prompts ≈ one funded afternoon from a five-episode season.**
