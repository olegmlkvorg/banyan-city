# Node 006a — shot list (per-beat generation prompts)

The whole episode as a shot list — one generation prompt per script beat, for
end-to-end rendering and assembly by `pipeline/render_t3.py`. Same rules as
node 001's list: base footage only (no burned-in text, no spoken dialogue —
post adds caption overlays and VO), 9:16 vertical, ~10s per shot, one take.

**Character continuity (paste into any beat that shows them — anime model
sheet, `style.md`):** the magistrate is a sharp angular silhouette in dark,
travel-worn robes of office, a seal on a chain, a face drawn for one raised
eyebrow. The scavenger is a small, round goblin — enormous ears that act like
a second face, one broken tusk, huge expressive eyes, patchwork cloak in
faded greens and browns. The farmer is a broad, squarish silhouette in a
straw hat; three lines draw his whole face; permanently unimpressed posture.
The sapling is a tiny, mascot-simple ~50cm tree — thin curved trunk, one or
two oversized expressive leaves, never a face; its acting is entirely leaf
angle and timing. Beside it a crooked lean-to, a three-stone cairn, and —
as of this episode — two clay jugs side by side.

**Naming for assembly:** save each clip as `NN-slug.mp4` in a clips dir, then:
`python3 pipeline/render_t3.py sapling 006a --clips <dir> --out episode.mp4`
Missing beats render as slates; partial lists still assemble.

Status legend: ✅ generated · ⬜ needs footage

---

## Beat 01 — COLD OPEN / AUDIT PREP (0:00–0:10) ⬜ needs footage

Script beat: morning, and Shade is being *staged* — the scavenger re-stacks
the cairn's three stones by size, steps back, re-stacks them by color; the
farmer arrives and sets a second jug beside the first. Infrastructure.

```
Vertical 9:16 shot, morning. A tiny settlement being frantically tidied for inspection: a small round goblin — enormous ears that act like a second face, one broken tusk, huge expressive eyes, patchwork cloak in faded greens and browns — carefully re-stacks a three-stone cairn by size, steps back to squint at it, then re-stacks the same three stones by color. Beside him a mascot-simple 50cm sapling with a thin curved trunk and one or two oversized expressive leaves, a crooked lean-to behind it. A farmer with a broad squarish silhouette, straw hat, and three-line unimpressed face walks in and solemnly sets a second clay jug down beside the first, perfectly aligned. Fussy, nervous comedy of preparation; warm peach and gold morning washes, long soft shadows. Hand-drawn 2D anime style, low detail: flat cel-shaded colors, bold clean linework, minimal shading (single shadow tone), simplified shapes, soft watercolor-wash backgrounds with large empty areas, gentle pastel-leaning palette, expressive minimal faces. No photorealism, no 3D render look, no heavy texture. 9:16 vertical, no text.
```

## Beat 02 — THE ARRIVAL (0:10–0:30) ⬜ needs footage

Script beat: the magistrate is early — she comes up the road reading the
assessor's ledger as she walks, no pause at the clearing's edge, suddenly
simply *inside* the settlement mid-file. The scavenger dives behind the tree,
remembers he is official, and emerges at approximately attention. She closes
the ledger and looks at the tree for a long moment; one leaf tilts.

```
Vertical 9:16 shot, morning. Up a dirt road toward a tiny settlement walks the magistrate — a sharp angular silhouette in dark, travel-worn robes of office, a seal on a chain, a face drawn for one raised eyebrow — reading an open ledger as she walks, never looking up, never pausing, striding straight into the clearing mid-page-turn. A small round goblin (enormous ears, one broken tusk, huge expressive eyes, patchwork cloak in faded greens and browns) dives behind a mascot-simple 50cm sapling in pure reflex, then remembers himself, steps back out, and stands at wobbly approximate attention. She snaps the ledger shut and regards the little tree — thin curved trunk, oversized expressive leaves, never a face — in a long silent appraisal. One oversized leaf slowly, deliberately tilts. Her eyebrow rises one degree. Deadpan comedic authority; warm peach and gold morning washes, long soft shadows. Hand-drawn 2D anime style, low detail: flat cel-shaded colors, bold clean linework, minimal shading (single shadow tone), simplified shapes, soft watercolor-wash backgrounds with large empty areas, gentle pastel-leaning palette, expressive minimal faces. No photorealism, no 3D render look, no heavy texture. 9:16 vertical, no text.
```

## Beat 03 — THE HEARING (0:30–1:00) ⬜ needs footage

Script beat: she paces the clearing and the law breaks down in real time —
resident, property, livestock, tenancy all defeated in turn — until she stops,
takes in the jug-tribute, the cairn, the two humans arranged around the tree,
and the answer arrives: *shrine*. She fills the form and hands the scavenger a
sealed slip of paper; he holds it in both hands like it might evaporate. She
asks the tree's consent; one leaf tilts; she notes it.

```
Vertical 9:16 montage-style shot, late morning. The magistrate — a sharp angular silhouette in dark, travel-worn robes of office, a seal on a chain, a face drawn for one raised eyebrow — paces a tiny clearing in crisp lines, ticking categories off on her fingers, deadpan and rapid, while a small round goblin (enormous ears that act like a second face, one broken tusk, huge expressive eyes, patchwork cloak in faded greens and browns) trails her offering helpless interjections. She stops mid-stride. Her gaze travels slowly across the evidence: two clay jugs set like offerings at the roots of a mascot-simple 50cm sapling with oversized expressive leaves, a neat three-stone cairn, a farmer (broad squarish silhouette, straw hat, three-line face) and the goblin arranged around the little tree like a congregation. Realization lands. She writes briskly on a form, then hands the goblin a small slip of paper with a seal; he receives it in both cupped hands like it might evaporate, ears drooping with emotion. She turns and addresses the tree formally; one oversized leaf tilts; she makes a precise note. Escalating bureaucratic comedy arriving at reverence; high flat greens, pale blue-white sky, minimal shadow. Hand-drawn 2D anime style, low detail: flat cel-shaded colors, bold clean linework, minimal shading (single shadow tone), simplified shapes, soft watercolor-wash backgrounds with large empty areas, gentle pastel-leaning palette, expressive minimal faces. No photorealism, no 3D render look, no heavy texture. 9:16 vertical, no text.
```

## Beat 04 — THE CLAUSE (1:00–1:25) ⬜ needs footage

Script beat: she stamps the form, stops on the final line — faintly
entertained for the first time — delivers the provisional clause, and leaves,
pausing at the clearing's edge exactly where the assessor paused. She walks
off into the morning; the scavenger looks at his paper, the farmer looks at
the tree, the tree's leaves are very still.

```
Vertical 9:16 shot, late morning. The magistrate — a sharp angular silhouette in dark, travel-worn robes of office, a seal on a chain, a face drawn for one raised eyebrow — stamps a form with ceremonial finality, then stops on its last line and, for the first time, looks faintly entertained. She says something brief over her shoulder and walks out of the clearing; at its exact edge she pauses for one measured beat — the same spot on the road where a previous official once paused — then continues off down the dirt road into the morning light. Left behind: a small round goblin (enormous ears, one broken tusk, huge expressive eyes, patchwork cloak in faded greens and browns) staring down at a small sealed slip of paper in both hands; a farmer (broad squarish silhouette, straw hat, three-line face) turning to look at the tree; and a mascot-simple 50cm sapling — thin curved trunk, oversized expressive leaves, never a face — its leaves held very, very still. Slow push-in on the motionless little tree to end. Quiet weight after comedy; warm gold morning washes, long soft shadows. Hand-drawn 2D anime style, low detail: flat cel-shaded colors, bold clean linework, minimal shading (single shadow tone), simplified shapes, soft watercolor-wash backgrounds with large empty areas, gentle pastel-leaning palette, expressive minimal faces. No photorealism, no 3D render look, no heavy texture. 9:16 vertical, no text.
```

---

## Progress

0 of 4 beats generated. Generating footage is a paid action wherever it runs —
a founder call per the spend rules (STEWARDSHIP.md §4, `pipeline/budget.yaml`).
Platform choice tracks [D8](../../../../DECISIONS.md). Provenance for any
generated beat goes in a sibling `NN-slug.meta.yaml` (platform, model, prompt,
cost) so `render_t3.py` records per-beat sources in the T3 leaf.

006a is one of the R4 sibling pair off the trunk tip (005); the trunk call
between 006a and 006b is the founder's. This list makes the candidate
render-ready either way.
