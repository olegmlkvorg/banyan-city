# Node 004 — shot list (per-beat generation prompts)

The whole episode as a shot list — one generation prompt per script beat, for
end-to-end rendering and assembly by `pipeline/render_t3.py`. Same rules as
node 001's list: base footage only (no burned-in text, no spoken dialogue —
post adds caption overlays, the wireframe overlay flash, and VO), 9:16
vertical, ~10s per shot, one take.

**Character continuity (paste into any beat that shows them — anime model
sheet, `../../style.md`):** the scavenger is a small, round goblin — enormous
expressive ears that act like a second face, huge eyes, one broken tusk,
patchwork cloak in faded greens and browns. The farmer is a broad, squarish
silhouette in a straw hat — three lines draw his whole face, permanently
unimpressed posture — carrying a clay jug. The sapling is a tiny (~50cm)
mascot-simple tree — thin curved trunk, two oversized expressive leaves, never
a face; beside it a crooked lean-to and a small three-stone cairn.

**Naming for assembly:** save each clip as `NN-slug.mp4` in a clips dir, then:
`python3 pipeline/render_t3.py sapling 004 --clips <dir> --out episode.mp4`
Missing beats render as slates; partial lists still assemble.

Status legend: ✅ generated · ⬜ needs footage

---

## Beat 01 — RECAP / THE LOWERED FIG (0:00–0:08) ⬜ needs footage

Script beat: the raised fig from 003b… lowered in embarrassment. Pure
deflation gag.

```
Hand-drawn 2D anime style, low detail, dusk: amber-into-indigo watercolor-wash sky, silhouettes reading before faces. A small round goblin — enormous expressive ears, huge eyes, one broken tusk, patchwork cloak in faded greens and browns — stands beside a tiny mascot-simple sapling (thin curved trunk, two oversized leaves) and a crooked lean-to, holding a single fig raised high overhead in a grand ceremonial pose, chest puffed, mouth open. A long beat. His face falls; he slowly lowers the fig and his shoulders slump, ceremony collapsing into embarrassment. Deadpan comedy, static camera. Flat cel-shaded colors, bold clean linework, minimal shading (single shadow tone), simplified shapes, soft watercolor-wash background with large empty areas, gentle pastel-leaning palette, expressive minimal faces. No photorealism, no 3D render look, no heavy texture. 9:16 vertical, no text.
```

## Beat 02 — THE NAMING (0:08–0:40) ⬜ needs footage

Script beat: name-audition pacing montage, rejection by stillness, the defeated
flop into the shade — and both leaves tilting at once on "it's just shade."

```
Hand-drawn 2D anime style, low detail, midday: high flat greens, pale blue-white sky, minimal shadow. A small round goblin in a patchwork cloak — enormous expressive ears, huge eyes, one broken tusk — paces back and forth in front of a tiny (~50cm) mascot-simple sapling with a thin curved trunk and two oversized expressive leaves (never a face), gesturing grandly like a founder pitching investors, glancing at the tree after each pitch — and the tree stays perfectly still each time, which visibly wounds him. Finally he flops down against the little trunk in its tiny patch of shade, defeated, muttering. Above him, both oversized leaves suddenly tilt at once, emphatic and deliberate. He goes very still and looks up. Comedic rhythm. Flat cel-shaded colors, bold clean linework, minimal shading (single shadow tone), simplified shapes, soft watercolor-wash background with large empty areas, gentle pastel-leaning palette, expressive minimal faces. No photorealism, no 3D render look, no heavy texture. 9:16 vertical, no text.
```

## Beat 03 — THE SECOND CITIZEN (0:40–1:08) ⬜ needs footage

Script beat: boots; the failed hide; the farmer following the damp line
upstream; the jug and half-loaf set at the trunk like tribute; "Tell no one."
Post adds the one-frame wireframe flash at the end of this beat.

```
Hand-drawn 2D anime style, low detail, late afternoon: warm gold wash edging toward dusk amber, long soft shadows. A broad squarish farmer in a straw hat — whole face drawn in three lines, permanently unimpressed posture — walks slowly along a dark damp line in the grass, tracing it upstream to a tiny mascot-simple sapling with a crooked lean-to, where a small round goblin with enormous ears is very visibly failing to hide behind the thin curved trunk. A long wary stare between them. Then the farmer sets down a clay jug and half a loaf of bread at the base of the little tree, next to a small three-stone cairn — an offering, not charity — and gives the tree a single gruff nod, refusing eye contact. Flat cel-shaded colors, bold clean linework, minimal shading (single shadow tone), simplified shapes, soft watercolor-wash background with large empty areas, gentle pastel-leaning palette, expressive minimal faces. No photorealism, no 3D render look, no heavy texture. 9:16 vertical, no text.
```

## Beat 04 — THE HOOK (1:08–1:25) ⬜ needs footage

Script beat: the farmer's parting warning over his shoulder; he walks into the
dusk; the scavenger looks at the tree; the leaves are very still.

```
Hand-drawn 2D anime style, low detail, dusk: amber into indigo watercolor wash, silhouettes reading before faces, long flat shadows. A broad squarish farmer in a straw hat, an empty sack over his shoulder, pauses at the edge of a small clearing, half-turned back toward a tiny mascot-simple sapling, a crooked lean-to, and a small round goblin holding a fig — delivering a warning over his shoulder. Then he walks away down the darkening field. The goblin turns slowly to look at the little tree; its two oversized leaves hang perfectly, ominously still against the last light. Quiet dread under warmth, slow push-in on the sapling. Flat cel-shaded colors, bold clean linework, minimal shading (single shadow tone), simplified shapes, soft watercolor-wash background with large empty areas, gentle pastel-leaning palette, expressive minimal faces. No photorealism, no 3D render look, no heavy texture. 9:16 vertical, no text.
```

---

## Progress

0 of 4 beats generated. Generating footage is a paid action wherever it runs —
a founder call per the spend rules (STEWARDSHIP.md §4, `pipeline/budget.yaml`).
Platform choice tracks [D8](../../../../DECISIONS.md). Provenance for any
generated beat goes in a sibling `NN-slug.meta.yaml` (platform, model, prompt,
cost) so `render_t3.py` records per-beat sources in the T3 leaf.
