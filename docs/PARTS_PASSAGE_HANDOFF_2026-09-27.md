# Project handoff

Updated: September 27, 2026 · Project: BrineSpace · Task: corridor incentive pilot

## Objective and acceptance
Give straight, corner and T corridors a useful placement relationship. Owner authorized
one short-range discovery connecting Storage Bay to Salvage Workshop through a passage,
with placement feedback and no bonus for extending the passage chain.

## Accepted decisions and constraints
- Parts Passage pays +1 Metal per functioning Storage Bay / Salvage Workshop pair through
  exactly one straight, corner or T corridor, with matching rotated doors at both ends.
- All three rooms must function. A tee can serve two different workshops; link identity
  remains the endpoint pair, so another route cannot stack the same pair's reward.
- Existing discovery rules apply: hidden until operation, three consecutive functioning
  cycles stabilize it, doubled bonus thereafter, standard Archived Data reward.
- Unknown placement feedback hints at an unrecovered connection without naming the recipe
  or reward. Learned previews report the pair count and current bonus, including doubling.
- Existing direct-corridor recipes, building costs, workshop inputs, failure conditions
  and saves remain governed by their existing rules. This is one pilot, not a broad rebalance.

## Current state
- `scripts/synergy_manager.gd`: recipe, one-passage matching, shared passage-only preview
  evaluation and passage relevance for learned card/inspector entries.
- `scripts/discovery_manager.gd`: functioning links require every participating cell.
- `scripts/main.gd`: placement feedback, learned passage card and inspector support.
- `scripts/grid_canvas.gd`: learned link effects follow the passage instead of drawing
  directly between endpoints. Preserved the pre-existing Veld animation change.
- `tests/test_parts_passage.gd` and paired UID; registered in `tests/index.json`.
- Review captures/logs and save fingerprints: `output/parts-passage/`.

## Verification
Three scoped suites passed: Parts Passage, synergy manager, discovery progression
(`output/test-runs/20260927-211453-headless`). Coverage includes all 12 shape/rotation
combinations, mismatched doors, direct adjacency and long-chain rejection, tee branching,
endpoint deduplication, functioning gates, discovery/stabilization, hidden/learned
previews and actual economy accounting. Workshop inputs must exist before bonus payment.
Native Godot 4.7.2 fixture also passed; reviewed readable placement feedback and built
tee capture. All runs used scratch APPDATA. Real profile fingerprint: 2,676 files;
an interim comparison was identical, while the final comparison shows only Godot log
rotation during concurrent activity. Save/progress/layout files remain identical.
Scoped diff whitespace check passed.

## No stacking with Logistics Spine (owner, Sept 27)
A balance probe found a straight passage also triggered Logistics Spine (storage opening
onto a corridor), paying +2 Metal and up to +4 stabilized, which made the workshop free or
profitable. `SynergyManager.within_passage_link` now skips an adjacent pair that sits inside
a passage link, in both evaluation and the placement preview. The passage pays +1 Metal
(+2 stabilized) as designed; storage beside a plain corridor keeps Logistics Spine.

## Next action
Owner normal-play review: judge whether the Metal saving makes reserving passage space
worthwhile. Balance and enjoyment are not established by the automated fixtures.
No release export performed.
