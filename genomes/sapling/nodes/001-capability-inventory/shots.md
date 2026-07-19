# Node 001 — shot list (per-beat generation prompts)

The trials proved single shots; this is the **whole episode** as a shot list —
one generation prompt per script beat, so node 001 can be rendered end-to-end
and assembled by `pipeline/render_t3.py`. Same rules as the trials: base
footage only (no burned-in text, no dialogue — post adds terminal overlays and
VO), 9:16 vertical, ~10s per shot, one take.

**Naming for assembly:** save each clip as `NN-slug.mp4` in a clips dir, where
`NN` is the beat number below, then:
`python3 pipeline/render_t3.py sapling 001 --clips <dir> --out episode.mp4`
render_t3 fits each clip to its beat's script duration; any missing beat renders
as a slate, so partial shot lists still assemble.

**Voice (optional):** episodes are watchable silent (captions carry the VO), but
render_t3 also muxes per-beat audio in sync. Drop an `NN-vo.mp3` beside each
clip and it's placed on that beat automatically; or pass `--tts openai` to have
the VO lines narrated (paid — a founder/spend call). Cards stay silent. No audio
anywhere = the silent captioned animatic, unchanged.

Status legend: ✅ generated · ⬜ needs footage

---

## Beat 01 — COLD OPEN (0:00–0:12) ⬜ needs footage (v2 anime) — v1 photoreal clip archived (Veo/Flow trial shot A)

```
Vertical 9:16 shot, night interior, hand-drawn 2D anime style, low detail: flat cel-shaded colors, bold clean linework, minimal shading (single shadow tone), simplified shapes, soft watercolor-wash backgrounds with large empty areas, gentle pastel-leaning palette, expressive minimal faces. A cramped dark apartment washed in flat deep indigo, lit only by the cold teal glow of a computer monitor. A tired male engineer in his 30s — simple slumped silhouette, a few clean lines for an exhausted face — sits at a desk, typing fast on a mechanical keyboard, face underlit by flat monitor glow, 3 a.m. exhaustion. He suddenly inhales sharply, sways sideways and collapses out of frame; a ceramic mug falls and shatters on the floor. Static camera. No photorealism, no 3D render look, no heavy texture. No text.
```

## Beat 02 — WAKE (0:12–0:28) ⬜ needs footage (v2 anime) — v1 photoreal clip archived (Veo/Flow trial shot B)

```
Vertical 9:16 shot from ground level, two centimeters above the soil, hand-drawn 2D anime style, low detail: flat cel-shaded colors, bold clean linework, minimal shading (single shadow tone), simplified shapes, soft watercolor-wash backgrounds with large empty areas, gentle pastel-leaning palette. Looking up through a single small trembling oversized green leaf of a tiny mascot-simple sapling — thin curved trunk, one or two oversized expressive leaves, no face, no eyes; all its acting is leaf angle and timing. Beyond the leaf, an impossibly saturated too-blue flat watercolor-wash sky with a few drifting simplified clouds. The leaf twitches nervously, shaking the whole frame slightly, as wind moves flat-color grass around it. Enormous empty green field with large empty areas, warm morning light in peach and gold washes with long soft shadows, slight fisheye distortion. No photorealism, no 3D render look, no heavy texture. No text.
```

## Beat 03 — INCIDENT RESPONSE (0:28–0:40) ⬜ needs footage

Script beat: the panic stops. A held beat of stillness — the sapling, composed.
The tone flips from flailing to methodical. Post will type a `$ whoami` terminal
line over this; the footage just needs to be *calm and still* to contrast beat 02.

```
Vertical 9:16 shot, static and quiet, hand-drawn 2D anime style, low detail: flat cel-shaded colors, bold clean linework, minimal shading (single shadow tone), simplified shapes, soft watercolor-wash backgrounds with large empty areas, gentle pastel-leaning palette. A single tiny mascot-simple sapling — thin curved trunk, one or two oversized expressive leaves, no face, no eyes; expression is pose alone — standing alone in a vast empty field at dawn, seen from low and close. Dawn palette: warm peach and gold washes, long soft shadows. After the trembling of before, it is now completely still — no wind, held breath, the light soft and even. One small leaf, motionless. Wide empty watercolor horizon behind, mostly empty space. A held, meditative, almost surgical calm. Slow imperceptible push-in. No photorealism, no 3D render look, no heavy texture. No text.
```

## Beat 04 — THE INVENTORY (0:40–1:05) ⬜ needs footage (v2 anime) — v1 photoreal clip archived (Veo/Flow trial shot C)

```
Vertical 9:16 shot, hand-drawn 2D anime style, low detail: flat cel-shaded colors, bold clean linework, minimal shading (single shadow tone), simplified shapes, soft watercolor-wash backgrounds with large empty areas, gentle pastel-leaning palette. An underground cross-section view beneath a tiny mascot-simple sapling (thin curved trunk, one or two oversized leaves). Dark soil as a near-black flat wash rendered as a deep translucent map: glowing root filaments spreading downward as clean bioluminescent teal and green neon lines, veins of dark water as simple shimmering flat shapes, mineral particles as sparse glittering dots. In the far distance through the soil, rhythmic concentric rings of soft light pulse like sonar with each distant footstep, growing brighter — clean flat rings, no texture. Bioluminescent teal and green on near-black, slow camera push-in. No photorealism, no 3D render look, no heavy texture. No text.
```

## Beat 05 — REALIZATION / HOOK (1:05–1:25) ⬜ needs footage

Script beat: slow push-in on the tiny sapling, alone in an enormous field; the
realization that it cannot leave — and something is coming over the hill. This is
the episode's emotional close and its cliffhanger. Footage needs scale (tiny
subject, huge world) and a sense of approach.

```
Vertical 9:16 wide shot, hand-drawn 2D anime style, low detail: flat cel-shaded colors, bold clean linework, minimal shading (single shadow tone), simplified shapes, soft watercolor-wash backgrounds with large empty areas, gentle pastel-leaning palette. One tiny fragile mascot-simple sapling — thin curved trunk, one or two oversized expressive leaves, no face; expression is pose alone — alone at the center of an enormous empty field under a vast watercolor-wash sky, dwarfed by the landscape. Dusk hook palette: amber into indigo, silhouettes reading before any detail. Slow steady push-in toward the sapling. On the far horizon, over a low hill, faint dust rises and the grass bends in a line — something is approaching, unseen, from far away. Lonely, epic, quietly ominous, mostly empty frame. No photorealism, no 3D render look, no heavy texture. No text.
```

---

## Progress

0 of 5 beats exist in the v2 anime style — all five prompts above are
rewritten and ready to generate. The assembled v1 episode (Veo/Google Flow
photoreal trial clips for beats 01/02/04, slates for 03 and 05) and its
provenance remain archived evidence, not canon style — see `../../style.md`,
"Status of v1 footage". Generating all five beats in v2 completes the first
full episode of the trunk root node in the canonical style.

Provenance for any generated beat goes in a sibling `NN-slug.meta.yaml`
(platform, model, prompt, cost) so `render_t3.py` records per-beat sources in
the T3 leaf. A full, watermark-free set is the prerequisite for publishing
node 001's official T3 leaf (a founder decision).
