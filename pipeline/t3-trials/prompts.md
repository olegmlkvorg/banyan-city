# Trial prompt pack — node 001, three shots

Same three prompts on every platform, verbatim, 9:16, ~10 s, one take.
No text overlays, no dialogue, no VO — post handles those (see README).
Chosen to probe three different failure modes: interior human realism (A),
the series' signature macro shot (B), stylized non-human abstraction (C).

---

## Shot A — cold open (0:00–0:12): interior, human, night

Tests: human realism, screen light, night interior — the *hardest* to fake.

```
Vertical 9:16 cinematic shot, night interior. A cramped dark apartment lit
only by a computer monitor. A tired male engineer in his 30s sits at a desk,
typing fast on a mechanical keyboard, face underlit by cold terminal glow,
3 a.m. exhaustion. He suddenly inhales sharply, sways sideways and collapses
out of frame; a ceramic mug falls and shatters on the floor. Static camera,
shallow depth of field, muted color grade, realistic photography, no text.
```

## Shot B — wake (0:12–0:28): the signature shot

Tests: macro nature, POV framing, the image the whole series hangs on.

```
Vertical 9:16 macro shot from ground level, two centimeters above the soil,
looking up through a single small trembling green leaf of a tiny sapling.
Beyond the leaf, an impossibly saturated too-blue sky with drifting clouds.
The leaf twitches nervously, shaking the whole frame slightly, as wind moves
grass around it. Enormous empty green field, morning light, dreamlike but
photoreal, slight fisheye distortion, no text.
```

## Shot C — the inventory (0:40–1:05): underground sense-vision

Tests: stylization control — abstract but must stay legible, not mush.

```
Vertical 9:16 stylized shot: an underground cross-section view beneath a tiny
sapling. Dark soil rendered as a deep translucent map: glowing root filaments
spreading downward, veins of dark water shimmering, mineral particles
glittering. In the far distance through the soil, rhythmic concentric rings of
soft light pulse like sonar with each distant footstep, growing brighter.
Bioluminescent color palette on near-black, slow camera push-in, no text.
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
