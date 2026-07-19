# Node 005 — shot list (per-beat generation prompts)

The whole episode as a shot list — one generation prompt per script beat, for
end-to-end rendering and assembly by `pipeline/render_t3.py`. Same rules as
node 001's list: base footage only (no burned-in text, no spoken dialogue —
post adds caption overlays and VO), 9:16 vertical, ~10s per shot, one take.

**Character continuity (paste into any beat that shows them — anime model
sheet, `style.md`):** the assessor is a thin vertical line of a man in
dust-grey robes, drawn with ruler-straight edges, a heavy ledger chained to
his belt and a quill worn to a stub; he moves like a metronome. The scavenger
is a small, round goblin — enormous ears that act like a second face, one
broken tusk, huge expressive eyes, patchwork cloak in faded greens and
browns. The farmer is a broad, squarish silhouette in a straw hat; three
lines draw his whole face; permanently unimpressed posture. The sapling is a
tiny, mascot-simple ~50cm tree — thin curved trunk, one or two oversized
expressive leaves, never a face; beside it a crooked lean-to, a three-stone
cairn, and a clay jug.

**Naming for assembly:** save each clip as `NN-slug.mp4` in a clips dir, then:
`python3 pipeline/render_t3.py sapling 005 --clips <dir> --out episode.mp4`
Missing beats render as slates; partial lists still assemble.

Status legend: ✅ generated · ⬜ needs footage

---

## Beat 01 — COLD OPEN / THE METRONOME (0:00–0:10) ⬜ needs footage

Script beat: dawn over Shade, wide and peaceful — and the assessor entering
down the exact center of the road, counting under his breath before a word.

```
Vertical 9:16 wide shot, dawn. A tiny settlement in an enormous empty field: a mascot-simple 50cm sapling — thin curved trunk, one or two oversized expressive leaves — a crooked lean-to, a three-stone cairn, a clay jug, all in warm peach and gold dawn washes with long soft shadows. Down a dirt road toward it walks the assessor, a thin vertical line of a man in dust-grey robes drawn with ruler-straight edges, a heavy ledger chained to his belt — walking the exact center of the road with metronome regularity, unhurried and inevitable. He stops at the clearing's edge, lips moving as he counts under his breath. Static camera, quietly comedic menace. Hand-drawn 2D anime style, low detail: flat cel-shaded colors, bold clean linework, minimal shading (single shadow tone), simplified shapes, soft watercolor-wash backgrounds with large empty areas, gentle pastel-leaning palette, expressive minimal faces. No photorealism, no 3D render look, no heavy texture. 9:16 vertical, no text.
```

## Beat 02 — THE ASSESSMENT (0:10–0:45) ⬜ needs footage

Script beat: rapid-fire deadpan fieldwork — knotted string measuring the
lean-to, the cairn counted stone by stone, the string held against the trunk;
the scavenger orbiting in rising panic, the farmer stonewalling.

```
Vertical 9:16 montage-style shot, morning. The assessor — a thin vertical line of a man in dust-grey robes drawn with ruler-straight edges, a chained ledger and a quill worn to a stub — methodically surveys a tiny settlement: he measures a crooked lean-to with a knotted string, counts a three-stone cairn one stone at a time with his finger, and holds the string up against the thin curved trunk of a mascot-simple 50cm sapling. A small round goblin — enormous ears that act like a second face, one broken tusk, huge expressive eyes, patchwork cloak in faded greens and browns — orbits him in rising panic, gesturing; a farmer with a broad squarish silhouette, straw hat, and three-line unimpressed face stands with arms crossed, giving nothing. The assessor writes in the ledger without ever changing expression. Deadpan bureaucratic comedy; warm peach and gold morning washes, long soft shadows. Hand-drawn 2D anime style, low detail: flat cel-shaded colors, bold clean linework, minimal shading (single shadow tone), simplified shapes, soft watercolor-wash backgrounds with large empty areas, gentle pastel-leaning palette, expressive minimal faces. No photorealism, no 3D render look, no heavy texture. 9:16 vertical, no text.
```

## Beat 03 — THE FORM FAILS (0:45–1:05) ⬜ needs footage

Script beat: the settlement schema visibly defeats him — the damp field line,
the mended channel, and the two-second montage revealing he's been watching
leaves move in still air all along.

```
Vertical 9:16 shot, late morning. The assessor — a thin vertical line of a man in dust-grey robes drawn with ruler-straight edges — stands with his quill stub frozen above the ledger, staring at a dark damp irrigation line running through flat green grass toward a tiny mascot-simple sapling — a channel that should not have mended itself. His minimal, expressive eyes move slowly from the wet field line, to the farmer's blank three-line face under a straw hat, to the little tree. Close on the assessor's eyes narrowing: quick flash cuts of the sapling's oversized leaves tilting in dead-still air, seen from his point of view at different moments of the day. He has been counting everything. Tense quiet; high flat greens under a pale blue-white sky, minimal shadow. Hand-drawn 2D anime style, low detail: flat cel-shaded colors, bold clean linework, minimal shading (single shadow tone), simplified shapes, soft watercolor-wash backgrounds with large empty areas, gentle pastel-leaning palette, expressive minimal faces. No photorealism, no 3D render look, no heavy texture. 9:16 vertical, no text.
```

## Beat 04 — THE QUESTION (1:05–1:25) ⬜ needs footage

Script beat: he addresses the tree with exhausted professionalism —
"Occupation?" — one leaf tilts; he writes one line we never see, chains the
ledger, and leaves, pausing precisely where he entered. Long hold on the tree.

```
Vertical 9:16 shot, midday. The assessor — a thin vertical line of a man in dust-grey robes drawn with ruler-straight edges — walks up to a mascot-simple 50cm sapling with a thin curved trunk and oversized expressive leaves, adjusts his robes, and addresses the little tree directly and formally, ledger open. A small round goblin (enormous ears, one broken tusk, patchwork cloak in faded greens and browns) and a farmer (broad squarish silhouette, straw hat, three-line face) watch, frozen, holding their breath in the background. On the sapling, one oversized leaf slowly, deliberately tilts — all its acting is leaf angle and timing, never a face. The man nods as if that were an answer, writes a single line in the ledger, closes it, and chains it shut to his belt. He walks away down the road; the shot holds long on the tiny tree alone in the frame, slow push-in at the end. Dry comedic gravity; high flat greens, pale blue-white sky, minimal shadow. Hand-drawn 2D anime style, low detail: flat cel-shaded colors, bold clean linework, minimal shading (single shadow tone), simplified shapes, soft watercolor-wash backgrounds with large empty areas, gentle pastel-leaning palette, expressive minimal faces. No photorealism, no 3D render look, no heavy texture. 9:16 vertical, no text.
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
