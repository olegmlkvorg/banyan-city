# Node 002b — shot list (per-beat generation prompts)

The **whole episode** as a shot list — one generation prompt per script beat,
so node 002b (the trunk's second node) can be rendered end-to-end and
assembled by `pipeline/render_t3.py`. Same rules as node 001's list: base
footage only (no burned-in text, no spoken dialogue — post adds caption
overlays and VO), 9:16 vertical, ~10s per shot, one take.

**Character continuity (paste into any beat that shows him):** the scavenger
is a small goblin — big ears, patchwork cloak, one broken tusk, nervous
cat-like eyes. The sapling is ~40cm tall with a single leaf (plus, this
episode only, one small fig). Keeping these clauses verbatim across beats and
platforms is the cheap half of character consistency; the taste axes
(motion/look) judge the rest.

**Naming for assembly:** save each clip as `NN-slug.mp4` in a clips dir, then:
`python3 pipeline/render_t3.py sapling 002b --clips <dir> --out episode.mp4`
render_t3 fits each clip to its beat's script duration; any missing beat
renders as a slate, so partial shot lists still assemble.

**Voice (optional):** drop `NN-vo.mp3` beside a clip and it's muxed on that
beat; silent stays watchable (captions carry VO and dialogue).

Status legend: ✅ generated · ⬜ needs footage

---

## Beat 01 — RECAP / ARRIVAL (0:00–0:05) ⬜ needs footage

Script beat: the footsteps from 001 arrive — small, fast, panicked. Something
dives into frame. Footage needs urgency entering a calm frame.

```
Vertical 9:16 cinematic shot, enormous empty green field in soft morning light, a tiny 40cm sapling with a single leaf alone at center frame, static camera. Suddenly a small goblin creature — big ears, patchwork cloak, one broken tusk — sprints into frame from the side at full panicked speed, skids in the grass, and dives behind the tiny sapling. Dust and grass kicked up. Photoreal fantasy, muted naturalistic color grade, shallow depth of field, no text.
```

## Beat 02 — THE FUGITIVE (0:05–0:20) ⬜ needs footage

Script beat: the goblin hides behind a trunk that covers one-sixth of him while
two mismatched patrol guards jog past and argue. Comedy of scale; the guards'
dialogue is carried by captions — footage needs the visual gag and the search.

```
Vertical 9:16 cinematic shot, morning field. A small goblin with big ears and a patchwork cloak presses his back against the pencil-thin trunk of a 40cm sapling, sucking in his belly, absurdly failing to hide — the tiny tree covers almost none of him. In the background two patrol guards in mismatched, ill-fitting armor jog past, stop, and scan the field; one consults a clipboard made of tree bark. They gesture at each other in disagreement. Deadpan comedic staging, photoreal fantasy, muted color grade, static camera, no text.
```

## Beat 03 — THE LONELY MONOLOGUE (0:20–0:50) ⬜ needs footage

Script beat: danger passed; the scavenger sits in the sapling's tiny shade,
knees up around his ears, and talks to a plant because it's the only thing
that won't file a report. The episode's emotional center — footage needs
smallness, warmth, and practiced loneliness.

```
Vertical 9:16 intimate cinematic shot, midday. A small goblin with big ears, a patchwork cloak and one broken tusk sits curled in the tiny patch of shade under a 40cm sapling, knees pulled up to his ears to fit into it, with the practiced ease of someone used to small shelters. He talks quietly to the little tree, picking at the dirt, glancing around embarrassed. Vast empty field behind, soft warm light through the single leaf. Gentle, lonely, tender tone, photoreal fantasy, shallow depth of field, slow imperceptible push-in, no text.
```

## Beat 04 — THE ANSWER (0:50–1:10) ⬜ needs footage

Script beat: the sapling spends everything it owns — one fig, released from
the thinnest branch, bonking off the scavenger's head. Footage needs the
deliberateness of the drop (this is a *decision*, not wind).

```
Vertical 9:16 macro cinematic shot: high on the thinnest branch of a tiny 40cm sapling hangs one small ripe fig, trembling slightly, backlit by afternoon sun. The camera holds on the fig as the stem slowly, deliberately lets go — the fig drops out of frame. Cut within the same take to a low wide angle: the fig bounces softly off the head of a small goblin in a patchwork cloak who was walking away, and lands in the grass at his feet. He stops mid-step. Photoreal fantasy, warm light, shallow depth of field, no text.
```

## Beat 05 — THE HOOK (1:05–1:25) ⬜ needs footage

Script beat: "…Did you just *answer* me?" — the fig held up like evidence, the
empty field, and one leaf tilting in absolute stillness. The franchise's
signature gesture; the leaf tilt must read as intentional.

```
Vertical 9:16 cinematic shot, late afternoon, absolute stillness — no wind, grass frozen. A small goblin with big ears and one broken tusk stands facing a tiny 40cm sapling, holding a small fig up in both hands like evidence, wide-eyed. Slow push-in past him toward the sapling's single leaf. In the dead-still air, the one leaf slowly, deliberately tilts to one side — an unmistakable intentional gesture from a plant. Hold on the tilted leaf. Quiet awe, photoreal fantasy, warm low light, cinematic depth, no text.
```

---

## Progress

0 of 5 beats generated. Generating footage is a paid action wherever it runs
(platform credits or API) — a founder call per the spend rules
(STEWARDSHIP.md §4, `pipeline/budget.yaml`); this list exists so that call is
one command, not a writing session. Platform choice tracks
[D8](../../../../DECISIONS.md): whatever wins the trials renders these five.

Provenance for any generated beat goes in a sibling `NN-slug.meta.yaml`
(platform, model, prompt, cost) so `render_t3.py` records per-beat sources in
the T3 leaf. A full set here + node 001's remaining beats 03/05 = the trunk's
first two episodes fully filmed.
