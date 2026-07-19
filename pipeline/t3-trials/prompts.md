# Trial prompt pack — node 001, three shots

Same three prompts on every platform, verbatim, 9:16, ~10 s, one take.
No text overlays, no dialogue, no VO — post handles those (see README).
Chosen to probe three different failure modes: interior human acting (A),
the series' signature macro shot (B), stylized non-human abstraction (C).

Prompts are v2 (low-detail anime, per `genomes/sapling/style.md`) as of
2026-07-19; archived v1 outputs were generated under the v1 photoreal
prompts — each output's `meta.yaml` records the exact prompt used.

---

## Shot A — cold open (0:00–0:12): interior, human, night

Tests: human character acting, screen light, night interior — the *hardest*
to keep on-model.

```
Hand-drawn 2D anime style, low detail: flat cel-shaded colors, bold clean
linework, minimal shading (single shadow tone), simplified shapes, soft
watercolor-wash backgrounds with large empty areas, gentle pastel-leaning
palette, expressive minimal faces. No photorealism, no 3D render look, no
heavy texture. 9:16 vertical, no text. Scene: night interior, a cramped dark
apartment lit only by a computer monitor — deep indigo palette, flat and
quiet, the screen's cold pale glow as the single light tone. A tired male
engineer in his 30s, exhaustion drawn in a few simple lines, sits at a desk
typing fast on a mechanical keyboard, face underlit by the terminal glow,
3 a.m. He suddenly inhales sharply, sways sideways and collapses out of
frame; a ceramic mug falls and shatters on the floor. Static camera.
```

## Shot B — wake (0:12–0:28): the signature shot

Tests: macro nature, POV framing, the image the whole series hangs on.

```
Hand-drawn 2D anime style, low detail: flat cel-shaded colors, bold clean
linework, minimal shading (single shadow tone), simplified shapes, soft
watercolor-wash backgrounds with large empty areas, gentle pastel-leaning
palette, expressive minimal faces. No photorealism, no 3D render look, no
heavy texture. 9:16 vertical, no text. Scene: macro view from ground level,
two centimeters above the soil, looking up through a single small trembling
green leaf of the sapling — a tiny, almost mascot-simple tree with a thin
curved trunk and one or two oversized expressive leaves, never a face; its
acting is entirely leaf angle and timing. Beyond the leaf, a flat too-blue
sky with drifting simple clouds. The leaf twitches nervously, shaking the
whole frame slightly, as wind moves the grass around it. Enormous empty
green field in soft watercolor washes, warm peach-and-gold morning light
with long soft shadows, slight fisheye curve to the framing.
```

## Shot C — the inventory (0:40–1:05): underground sense-vision

Tests: stylization control — abstract but must stay legible, not mush.

```
Hand-drawn 2D anime style, low detail: flat cel-shaded colors, bold clean
linework, minimal shading (single shadow tone), simplified shapes, soft
watercolor-wash backgrounds with large empty areas, gentle pastel-leaning
palette, expressive minimal faces. No photorealism, no 3D render look, no
heavy texture. 9:16 vertical, no text. Scene: an underground cross-section
view beneath the tiny sapling. Dark soil as a deep translucent map on
near-black: glowing root filaments in bioluminescent teal and green
spreading downward as clean neon lines, veins of dark water shimmering,
mineral particles glinting as simple dots. In the far distance through the
soil, rhythmic concentric rings of soft light pulse like sonar with each
distant footstep, growing brighter. Slow camera push-in.
```

---

## Per-output metadata (`outputs/<platform>/<shot>.meta.yaml`)

```yaml
platform:            # e.g. kling
model:               # e.g. Kling 3.0 Standard
shot: A              # A | B | C
prompt: verbatim-from-this-file   # note any forced deviation
mode: t2v            # t2v | i2v (+ seed frame path if i2v)
seed:                # if the platform exposes one
duration_s:
resolution:
watermark: true
credits_spent:
cost_usd: 0.00
date:
notes:               # refusals, queue time, retries used
```
