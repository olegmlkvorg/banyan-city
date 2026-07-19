# Node 004 — shot list (per-beat generation prompts)

The whole episode as a shot list — one generation prompt per script beat, for
end-to-end rendering and assembly by `pipeline/render_t3.py`. Same rules as
node 001's list: base footage only (no burned-in text, no spoken dialogue —
post adds caption overlays, the wireframe overlay flash, and VO), 9:16
vertical, ~10s per shot, one take.

**Character continuity (paste into any beat that shows them):** the scavenger
is a small goblin — big ears, patchwork cloak, one broken tusk. The farmer is
a weathered middle-aged man in plain work clothes, gruff and unhurried,
carrying a clay jug. The sapling is ~50cm with a handful of leaves; beside it
a crooked lean-to and a small three-stone cairn.

**Naming for assembly:** save each clip as `NN-slug.mp4` in a clips dir, then:
`python3 pipeline/render_t3.py sapling 004 --clips <dir> --out episode.mp4`
Missing beats render as slates; partial lists still assemble.

Status legend: ✅ generated · ⬜ needs footage

---

## Beat 01 — RECAP / THE LOWERED FIG (0:00–0:08) ⬜ needs footage

Script beat: the raised fig from 003b… lowered in embarrassment. Pure
deflation gag.

```
Vertical 9:16 cinematic shot, dusk light. A small goblin — big ears, patchwork cloak, one broken tusk — stands beside a tiny sapling and a crooked lean-to, holding a single fig raised high overhead in a grand ceremonial pose, chest puffed, mouth open. A long beat. His face falls; he slowly lowers the fig and his shoulders slump, ceremony collapsing into embarrassment. Deadpan comedy, photoreal fantasy, warm golden-hour grade, static camera, no text.
```

## Beat 02 — THE NAMING (0:08–0:40) ⬜ needs footage

Script beat: name-audition pacing montage, rejection by stillness, the defeated
flop into the shade — and both leaves tilting at once on "it's just shade."

```
Vertical 9:16 cinematic shot, midday. A small goblin in a patchwork cloak paces back and forth in front of a tiny 50cm sapling, gesturing grandly like a founder pitching investors, glancing at the tree after each pitch — and the tree stays perfectly still each time, which visibly wounds him. Finally he flops down against the little trunk in its tiny patch of shade, defeated, muttering. Above him, two leaves suddenly tilt at once, emphatic and deliberate. He goes very still and looks up. Comedic rhythm, photoreal fantasy, bright natural light, no text.
```

## Beat 03 — THE SECOND CITIZEN (0:40–1:08) ⬜ needs footage

Script beat: boots; the failed hide; the farmer following the damp line
upstream; the jug and half-loaf set at the trunk like tribute; "Tell no one."
Post adds the one-frame wireframe flash at the end of this beat.

```
Vertical 9:16 cinematic shot, late afternoon. A weathered middle-aged farmer in plain work clothes walks slowly along a dark damp line in the grass, tracing it upstream to a tiny sapling with a crooked lean-to, where a small goblin with big ears is very visibly failing to hide behind the thin trunk. A long wary stare between them. Then the farmer sets down a clay jug and half a loaf of bread at the base of the little tree, next to a small stone cairn — an offering, not charity — and gives the tree a single gruff nod, refusing eye contact. Photoreal fantasy, warm low light, muted grade, no text.
```

## Beat 04 — THE HOOK (1:08–1:25) ⬜ needs footage

Script beat: the farmer's parting warning over his shoulder; he walks into the
dusk; the scavenger looks at the tree; the leaves are very still.

```
Vertical 9:16 cinematic shot, dusk. A weathered farmer with an empty sack over his shoulder pauses at the edge of a small clearing, half-turned back toward a tiny sapling, a crooked lean-to, and a small goblin holding a fig — delivering a warning over his shoulder. Then he walks away down the darkening field. The goblin turns slowly to look at the little tree; its leaves hang perfectly, ominously still against the last light. Quiet dread under warmth, photoreal fantasy, dusk grade with long shadows, slow push-in on the sapling, no text.
```

---

## Progress

0 of 4 beats generated. Generating footage is a paid action wherever it runs —
a founder call per the spend rules (STEWARDSHIP.md §4, `pipeline/budget.yaml`).
Platform choice tracks [D8](../../../../DECISIONS.md). Provenance for any
generated beat goes in a sibling `NN-slug.meta.yaml` (platform, model, prompt,
cost) so `render_t3.py` records per-beat sources in the T3 leaf.
