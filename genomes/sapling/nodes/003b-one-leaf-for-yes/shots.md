# Node 003b — shot list (per-beat generation prompts)

The whole episode as a shot list — one generation prompt per script beat, for
end-to-end rendering and assembly by `pipeline/render_t3.py`. Same rules as
node 001's list: base footage only (no burned-in text, no spoken dialogue —
post adds caption overlays and VO), 9:16 vertical, ~10s per shot, one take.

**Character continuity (paste into any beat that shows them):** the scavenger
is a small goblin — big ears, patchwork cloak, one broken tusk, nervous
cat-like eyes. The sapling is ~40cm tall with a single leaf; this episode it
gains a second visible leaf.

**Naming for assembly:** save each clip as `NN-slug.mp4` in a clips dir, then:
`python3 pipeline/render_t3.py sapling 003b --clips <dir> --out episode.mp4`
Missing beats render as slates; partial lists still assemble.

Status legend: ✅ generated · ⬜ needs footage

---

## Beat 01 — RECAP / THE FIG RETURNED (0:00–0:07) ⬜ needs footage

Script beat: the uneaten fig, carried back at dawn and set at the trunk like
evidence returned to a crime scene.

```
Vertical 9:16 cinematic macro shot, dawn light. Two small green-grey goblin hands carefully carry a single ripe fig, cradled like something precious, and set it down gently in the grass at the base of a tiny 40cm sapling. The camera tilts up from the fig to the small goblin — big ears, patchwork cloak, one broken tusk — sitting back on his heels, staring at the little tree with wary determination. Soft golden morning light, photoreal fantasy, shallow depth of field, no text.
```

## Beat 02 — THE PROTOCOL (0:07–0:40) ⬜ needs footage

Script beat: the coin-test. He sits cross-legged, businesslike; one leaf tilts
in dead-still air; the interrogation montage with a tally scratched in dirt.
The tilt must read deliberate — this beat establishes the series' core gesture.

```
Vertical 9:16 cinematic shot, morning, absolute stillness — no wind. A small goblin with big ears and a patchwork cloak sits cross-legged in front of a tiny 40cm sapling like a card player, watching it intently. On a single small branch, one leaf slowly, deliberately tilts to the side in the dead-still air, then returns. The goblin's ears go flat; he leans in and scratches a tally mark in the dirt with a stick. The exchange repeats — question, tilt, tally. Deadpan wonder, photoreal fantasy, muted naturalistic grade, static camera, no text.
```

## Beat 03 — THE ASK (0:40–1:05) ⬜ needs footage

Script beat: the energy drops; he asks to stay without looking up; the tree
spends tomorrow's budget — two leaves for yes. The emotional core of the
episode; footage needs smallness and the cost of the answer.

```
Vertical 9:16 intimate cinematic shot, late morning. A small goblin with big ears and one broken tusk sits by a tiny 40cm sapling, hunched, picking at the dirt, not looking at the tree — the posture of someone asking for something that matters too much. A slow beat of stillness. Then on the sapling, one leaf tilts — and a second leaf tilts with it, both together, unmistakably deliberate, and the tiny tree seems to sag slightly with the effort. The goblin looks up. Soft light, gentle and quiet tone, photoreal fantasy, shallow depth of field, slow push-in, no text.
```

## Beat 04 — THE HOOK / THE LEAN-TO (1:05–1:25) ⬜ needs footage

Script beat: warm timelapse of terrible construction; dusk survey of the
world's smallest city; the fig raised like a founding charter; cut on the
breath before the name.

```
Vertical 9:16 cinematic timelapse then real-time, warm afternoon into dusk. A small goblin in a patchwork cloak drags deadfall branches and leans them clumsily against a rock beside a tiny 40cm sapling, building a crooked little lean-to, working with his tongue out, visibly bad at it. The light shifts to dusk: he stands surveying the lean-to, a tiny stone cairn, and the sapling — the world's smallest settlement. Then he raises a single fig high overhead in one hand, like a flag, mouth open mid-proclamation. Warm, hopeful, comedic tone, photoreal fantasy, golden-hour grade, no text.
```

---

## Progress

0 of 4 beats generated. Generating footage is a paid action wherever it runs —
a founder call per the spend rules (STEWARDSHIP.md §4, `pipeline/budget.yaml`).
Platform choice tracks [D8](../../../../DECISIONS.md). Provenance for any
generated beat goes in a sibling `NN-slug.meta.yaml` (platform, model, prompt,
cost) so `render_t3.py` records per-beat sources in the T3 leaf.
