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

Status legend: ✅ generated · ⬜ needs footage

---

## Beat 01 — COLD OPEN (0:00–0:12) ✅ Veo/Flow (trial shot A)

```
Vertical 9:16 cinematic shot, night interior. A cramped dark apartment lit only by a computer monitor. A tired male engineer in his 30s sits at a desk, typing fast on a mechanical keyboard, face underlit by cold terminal glow, 3 a.m. exhaustion. He suddenly inhales sharply, sways sideways and collapses out of frame; a ceramic mug falls and shatters on the floor. Static camera, shallow depth of field, muted color grade, realistic photography, no text.
```

## Beat 02 — WAKE (0:12–0:28) ✅ Veo/Flow (trial shot B)

```
Vertical 9:16 macro shot from ground level, two centimeters above the soil, looking up through a single small trembling green leaf of a tiny sapling. Beyond the leaf, an impossibly saturated too-blue sky with drifting clouds. The leaf twitches nervously, shaking the whole frame slightly, as wind moves grass around it. Enormous empty green field, morning light, dreamlike but photoreal, slight fisheye distortion, no text.
```

## Beat 03 — INCIDENT RESPONSE (0:28–0:40) ⬜ needs footage

Script beat: the panic stops. A held beat of stillness — the sapling, composed.
The tone flips from flailing to methodical. Post will type a `$ whoami` terminal
line over this; the footage just needs to be *calm and still* to contrast beat 02.

```
Vertical 9:16 shot, static and quiet, of a single tiny sapling standing alone in a vast empty field at dawn, seen from low and close. After the trembling of before, it is now completely still — no wind, held breath, the light soft and even. One small leaf, motionless. Wide empty horizon behind. A held, meditative, almost surgical calm. Muted naturalistic color, shallow depth of field, photoreal, slow imperceptible push-in, no text.
```

## Beat 04 — THE INVENTORY (0:40–1:05) ✅ Veo/Flow (trial shot C)

```
Vertical 9:16 stylized shot: an underground cross-section view beneath a tiny sapling. Dark soil rendered as a deep translucent map: glowing root filaments spreading downward, veins of dark water shimmering, mineral particles glittering. In the far distance through the soil, rhythmic concentric rings of soft light pulse like sonar with each distant footstep, growing brighter. Bioluminescent color palette on near-black, slow camera push-in, no text.
```

## Beat 05 — REALIZATION / HOOK (1:05–1:25) ⬜ needs footage

Script beat: slow push-in on the tiny sapling, alone in an enormous field; the
realization that it cannot leave — and something is coming over the hill. This is
the episode's emotional close and its cliffhanger. Footage needs scale (tiny
subject, huge world) and a sense of approach.

```
Vertical 9:16 wide cinematic shot: one tiny fragile sapling alone at the center of an enormous empty field under a vast sky, dwarfed by the landscape, late golden-hour light. Slow steady push-in toward the sapling. On the far horizon, over a low hill, faint dust rises and the grass bends in a line — something is approaching, unseen, from far away. Lonely, epic, quietly ominous, photoreal, cinematic depth, no text.
```

---

## Progress

3 of 5 beats generated (Veo/Google Flow, trial run). Beats 03 and 05 remain —
generating them on the same platform completes the first full episode of the
trunk root node. Until then the assembled preview
(`~/Desktop/banyan-001-veo-preview.mp4`) carries slates for 03 and 05.

Provenance for any generated beat goes in a sibling `NN-slug.meta.yaml`
(platform, model, prompt, cost) so `render_t3.py` records per-beat sources in
the T3 leaf. A full, watermark-free set is the prerequisite for publishing
node 001's official T3 leaf (a founder decision).
