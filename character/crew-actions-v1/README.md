# Crew action expansion

Integrated September 8, 2026; owner visual review pending. All three architects
retain their existing base packs and department identity.

| Added coverage per architect | Directions | Use |
|---|---|---|
| Salvage / underwater work | E, S, W, N | Expedition work and submerged hull work where the silhouette fits |
| Swim start / stop | E, S, W, N | Tread-to-swim transitions |
| Swim turn | All 12 facing changes | Quarter turns and composed half turns |
| Torch draw / stow | E, S, W, N | First/last 0.52 seconds of the existing ten-second construction job |
| Carry, swim-carry, unload | E, S, W, N | Expedition cargo; workshop carrying/unloading |
| Interact, kneel, repair, stand | S, W, N | Completes the existing east-facing activity coverage |

111 authored rows / 666 registered RGBA frames produce 168 runtime clips, each
available bare and helmeted. Each frame is 128 × 128; dry foot pivot (64,112),
water shoulder pivot (64,64). Loop frames last 140 ms; transitions total 520 ms.
Half turns combine two quarter turns over 680 ms. Carry gait follows distance.
Construction and unload transitions use simulation time, including Continue.

New source sheets and exact prompts are in `source/`; canonical actor contact
references sit beside this README. `registration.json` preserves each source
hash, scale, head anchor and offset. No opposite body views are mirrored.

Derived sequences: stow reverses draw, stop reverses start, stand reverses kneel,
and reverse turns reverse their corresponding authored quarter turn. Runtime
transition endpoints use the existing fitted swim/tread images at their exact
pivots. Half turns concatenate quarter turns. Existing helmets are composed onto
the new poses; the accepted original swimming helmet fit is unchanged.

Rejected sources are preserved: `*-directional-work.png` has palette/facing
defects and is replaced by `*-directional-work-v2.png`. The last two rows of
`*-swim-turn.png` have incorrect northern joins; dedicated `*-swim-turn-north.png`
replaces them. Bill's fifth unload pose drops the case prematurely; packaging
holds the correctly grounded sixth pose instead. Source separation follows
alpha gaps, not fixed-width cells, to avoid clipping extended swimming limbs.

Rebuild without generation:

1. `python character/crew-actions-v1/build_pack.py`
2. Godot 4.6.1: `--path . --script tests/preview_crew_actions.gd`
3. `python character/crew-actions-v1/build_review.py`
4. `python character/crew-actions-v1/build_evidence.py`

The runtime loader is `scripts/crew_action_pack.gd`. Clearance metadata comes
from the actual native fitted textures, including their transition endpoints.
Conservative room clearance suppresses wide transitions where they cannot fit;
cargo retains its held-object cycle on facing changes.

Review: `output/crew-actions-review.html` offers all added clips with equipment
comparison, direction filters, pause and scale controls. Native contact renders,
an animated showcase, and expedition screenshots accompany it. Agent inspected
source/contact sequences and native station presentation; interactive browser
inspection was blocked by the local-file URL policy. Owner motion/fit acceptance
remains pending. This is not a claim of exhaustive temporal visual acceptance.
