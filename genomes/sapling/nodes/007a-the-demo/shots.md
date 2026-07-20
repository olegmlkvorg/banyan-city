# Node 007a — shot list (per-beat generation prompts)

The whole episode as a shot list — one generation prompt per script beat, for
end-to-end rendering and assembly by `pipeline/render_t3.py`. Same rules as
node 001's list: base footage only (no burned-in text, no spoken dialogue —
post adds caption overlays and VO), 9:16 vertical, ~10s per shot, one take.

**Character continuity (paste into any beat that shows them — anime model
sheet, `style.md`):** the scavenger is a small, round goblin — enormous ears
that act like a second face, one broken tusk, huge expressive eyes, patchwork
cloak in faded greens and browns. The farmer is a broad, squarish silhouette
in a straw hat; three lines draw his whole face; permanently unimpressed
posture; clay jug. The magistrate is a sharp angular silhouette in dark,
travel-worn robes of office, a seal on a chain, a face drawn for one raised
eyebrow. The sapling is a tiny, mascot-simple ~50cm tree — thin curved trunk,
as of this episode a small fan of slender branches, oversized expressive
leaves, never a face; its acting is entirely leaf angle and timing. The
pilgrim (new this node) is a road-worn stranger in a dusty, simple travel
cloak, hood lowered, drawn as a plain kneeling silhouette with a minimal
quiet face; she carries nothing to count. Beside the tree a crooked lean-to,
a three-stone cairn, and two clay jugs side by side.

**Naming for assembly:** save each clip as `NN-slug.mp4` in a clips dir, then:
`python3 pipeline/render_t3.py sapling 007a --clips <dir> --out episode.mp4`
Missing beats render as slates; partial lists still assemble.

Status legend: ✅ generated · ⬜ needs footage

---

## Beat 01 — COLD OPEN / THE MIRACLE BACKLOG (0:00–0:10) ⬜ needs footage

Script beat: night — a plank propped against the lean-to, covered in charcoal
scrawl (the miracle backlog); the scavenger presents it to the tree and the
farmer like a general briefing troops. (The backlog's readable lines are a
post caption overlay — the plank itself carries only illegible scrawl.)

```
Vertical 9:16 shot, night. A wooden plank propped against a crooked lean-to, covered in neat rows of charcoal scribble-strokes and tally marks — deliberately illegible scrawl, not readable writing. A small round goblin — enormous ears that act like a second face, one broken tusk, huge expressive eyes, patchwork cloak in faded greens and browns — stands beside the plank like a general briefing troops, chest out, self-serious, tapping row after row with a pointer stick. His audience of two: a tiny mascot-simple 50cm sapling — thin curved trunk, a small fan of slender branches, oversized expressive leaves angled attentively toward the plank, never a face — and a farmer with a broad squarish silhouette, straw hat, and three-line unimpressed face, arms crossed, a clay jug at his feet. Deadpan war-room comedy in miniature. Deep indigo night palette, figures edged in silver rim light, flat and quiet. Hand-drawn 2D anime style, low detail: flat cel-shaded colors, bold clean linework, minimal shading (single shadow tone), simplified shapes, soft watercolor-wash backgrounds with large empty areas, gentle pastel-leaning palette, expressive minimal faces. No photorealism, no 3D render look, no heavy texture. 9:16 vertical, no text.
```

## Beat 02 — THE REHEARSALS (0:10–0:30) ⬜ needs footage

Script beat: deadpan montage — the scavenger conducts with a stick; a ripple
wave travels up the branches and stalls halfway at branch three, take after
take; the farmer watches from a stump, arms crossed, jug at his feet.

```
Vertical 9:16 montage-style shot, midday. A small round goblin — enormous ears that act like a second face, one broken tusk, huge expressive eyes, patchwork cloak in faded greens and browns — stands before a tiny mascot-simple 50cm sapling — never a face, its acting entirely leaf angle and timing — conducting it with a stick like an orchestra. On his downbeat the tree's oversized expressive leaves ripple in sequence — a wave traveling up its small fan of slender branches — and stall halfway, one middle branch missing its cue; the goblin sags, resets, raises the stick, and the same wave stalls at the same branch again. Repeated takes, exasperation escalating entirely through the goblin's ears and shoulders. On a stump behind them a farmer — broad squarish silhouette, straw hat, three-line unimpressed face — watches with arms crossed, a clay jug at his feet. Deadpan rehearsal-montage comedy; high flat greens, pale blue-white sky, minimal shadow. Hand-drawn 2D anime style, low detail: flat cel-shaded colors, bold clean linework, minimal shading (single shadow tone), simplified shapes, soft watercolor-wash backgrounds with large empty areas, gentle pastel-leaning palette, expressive minimal faces. No photorealism, no 3D render look, no heavy texture. 9:16 vertical, no text.
```

## Beat 03 — THE DEMO (0:30–0:55) ⬜ needs footage

Script beat: full moon — the magistrate arrives, unfolds a small travelling
chair and sits; the scavenger raises the stick, and the wind picks up: the
whole field ripples, every tree on the horizon does the choreography, the
rehearsed wave indistinguishable from weather. He flails — conducting bigger,
gesturing at the moon as if he ordered it; her expression does not change;
the farmer covers his eyes.

```
Vertical 9:16 shot, full-moon night. Under a huge flat full moon, the magistrate — a sharp angular silhouette in dark, travel-worn robes of office, a seal on a chain, a face drawn for one raised eyebrow — unfolds a small travelling chair at a clearing's edge and sits, perfectly composed. Facing a tiny mascot-simple 50cm sapling with a small fan of slender branches — never a face, its acting entirely leaf angle and timing — a small round goblin (enormous ears that act like a second face, one broken tusk, huge expressive eyes, patchwork cloak in faded greens and browns) raises a conductor's stick, visibly sweating. As the sapling's oversized leaves gather to move, the wind rises: the entire field of flat-color grass ripples in waves, and a distant treeline on the horizon performs the same choreography — the one rehearsed wave indistinguishable from weather. The goblin flails, conducting bigger and bigger, at one point gesturing grandly up at the moon as if he ordered it. The magistrate's face does not move. Behind them a farmer (broad squarish silhouette, straw hat, three-line face) covers his eyes with one hand. Deadpan catastrophe; deep indigo night palette with silver rim light on every figure, flat and quiet under the moon. Hand-drawn 2D anime style, low detail: flat cel-shaded colors, bold clean linework, minimal shading (single shadow tone), simplified shapes, soft watercolor-wash backgrounds with large empty areas, gentle pastel-leaning palette, expressive minimal faces. No photorealism, no 3D render look, no heavy texture. 9:16 vertical, no text.
```

## Beat 04 — THE TRUE THING (0:55–1:15) ⬜ needs footage

Script beat: the wind dies; the scavenger's arms drop and he stops performing
— small, honest, one hand to his chest. And the tree, having hoarded two
weeks of growth, lets go: every branch blooms and fruits at once, dozens of
figs swelling in real time, silver in the full moon, its leaves drooping as
it spends everything. The magistrate rises, stands over the little tree, and
catches the fig it drops to her — deliberate, bonk-height.

```
Vertical 9:16 shot, full-moon night, dead-still air. The wind has died. A small round goblin — enormous ears drooping, one broken tusk, huge expressive eyes, patchwork cloak in faded greens and browns — lowers his conductor's stick, arms falling to his sides, and speaks quietly with one hand touching his chest, all performance gone. Behind him the tiny mascot-simple 50cm sapling — thin curved trunk, a small fan of slender branches, never a face — lets go: every branch blooms and fruits at once, dozens of simple flat-color figs swelling in real time out of season, silver in the full moonlight, while the tree's oversized expressive leaves visibly droop lower and lower as it spends — the cost of the wonder drawn on the tree itself. The magistrate — a sharp angular silhouette in dark, travel-worn robes of office, a seal on a chain, a face drawn for one raised eyebrow — rises from her small travelling chair and comes to stand over the fruiting tree; one fig pops loose in a gentle, deliberate arc and she catches it in one hand, holding it up a long moment in the silver light. Comedy giving way to reverence; deep indigo night palette, silver rim light, flat and quiet. Hand-drawn 2D anime style, low detail: flat cel-shaded colors, bold clean linework, minimal shading (single shadow tone), simplified shapes, soft watercolor-wash backgrounds with large empty areas, gentle pastel-leaning palette, expressive minimal faces. No photorealism, no 3D render look, no heavy texture. 9:16 vertical, no text.
```

## Beat 05 — THE HOOK (1:15–1:25) ⬜ needs footage

Script beat: dawn — the clearing littered with figs like dropped coins; at
the exact edge where every arrival has ever stopped, a stranger kneels, hood
down, travel-worn — not counting, not assessing, praying. The farmer picks up
his jug and doesn't answer; long hold on the kneeling figure.

```
Vertical 9:16 shot, dawn. A tiny settlement clearing littered with dozens of simple flat-color figs scattered in the grass like dropped coins around a mascot-simple 50cm sapling — never a face, its acting entirely leaf angle and timing — with drooping oversized leaves, a crooked lean-to, a three-stone cairn, and two clay jugs side by side. At the clearing's exact edge, where the dirt road meets the grass, a road-worn stranger kneels — dusty simple travel cloak, hood lowered, a plain kneeling silhouette with a minimal quiet face, hands folded — not counting, not assessing: praying. In the middle distance a small round goblin (enormous ears that act like a second face, one broken tusk, huge expressive eyes, patchwork cloak in faded greens and browns) and a farmer (broad squarish silhouette, straw hat, three-line unimpressed face) stand very still, staring; the farmer bends, picks up his clay jug, and turns away without a word. The shot holds long on the kneeling figure, the empty road stretching behind her to the horizon. Warm peach and gold dawn washes, long soft shadows, quiet and vast. Hand-drawn 2D anime style, low detail: flat cel-shaded colors, bold clean linework, minimal shading (single shadow tone), simplified shapes, soft watercolor-wash backgrounds with large empty areas, gentle pastel-leaning palette, expressive minimal faces. No photorealism, no 3D render look, no heavy texture. 9:16 vertical, no text.
```

---

## Progress

0 of 5 beats generated. Generating footage is a paid action wherever it runs —
a founder call per the spend rules (STEWARDSHIP.md §4, `pipeline/budget.yaml`).
Platform choice tracks [D8](../../../../DECISIONS.md). Provenance for any
generated beat goes in a sibling `NN-slug.meta.yaml` (platform, model, prompt,
cost) so `render_t3.py` records per-beat sources in the T3 leaf.

007a deepens the 006a side of the R4 sibling pair; with this list the whole
006a line (005 → 006a → 007a) is render-ready end to end, so the founder's
trunk call between the 006 siblings can be felt on finished footage.
