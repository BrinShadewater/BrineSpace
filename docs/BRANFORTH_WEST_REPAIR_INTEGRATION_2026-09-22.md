# Branforth west repair handoff

Updated September 22, 2026. Project: Brine Space.

## Objective and acceptance

Replace the coarse west repair chain while retaining Branforth's mature profile,
slender proportions, foot contact and exact idle/action joins. Owner motion
acceptance and normal autonomous activity remain distinct from bounded rendering.

## Accepted decisions and constraints

No Higgsfield, room edits, publication or package replacement. Keep rejected
west-01 sources as evidence; they are not selected. Canonical face and helmet
pixels remain the identity reference. Existing action timings and metadata stay.

## Current state

Installed 36 PNGs: bare/helmet kneel-west, repair-west and stand-west, six frames
each. South and north installations remain unchanged. Branforth's three flagged
repair directions are now replaced; this does not certify every crew animation.

New preserved source and exact prompt:
`character/crew-repair-polish-v1/sources/branforth-west-chain-02.*`.
Frozen bare/helmet idle-west endpoints are alongside it. The new source was made
with the built-in OpenAI image tool using only the canonical idle reference.

`tools/prepare_branforth_west_repair_chain.py` extracts the unequal source rows,
removes disconnected alpha debris, downsamples at fixed 0.30 anatomical scale,
registers the forward boot at x124/y224 and composes canonical face/helmet pixels.
The source's top-row boots cross y512; equal grid slicing would amputate them.
Each selected transition has five distinct poses across six slots, including an
intentional final settling hold. The repair loop uses three authored work poses
in a forward/reverse sequence with an exact closing frame. Stand reverses kneel.
No synthetic claim of six unique in-betweens is made.

`tools/branforth_repair_revision.py` selects these explicit states in the crew
rebuild. `tests/test_branforth_repair_chain.py` now covers south, north and west.
Preview: `character/crew-repair-polish-v1/review/branforth-west-chain-02/chain.gif`.

## Verification

- Three Python regression tests pass: all 108 selected frames reproduce exactly,
  with binary alpha and exact idle/action joins across the three directions.
- Human crew validator: zero errors/border touches; 669 original frames and 108
  original source manifests unchanged.
- Complete crew packs: 19,475 checks, zero failures. Existing raw-image fixture
  warnings do not establish packaged release behavior.
- Native production animation player: 111 samples, both variants, no missing
  frames or errors; descent/work stills inspected.
- Actual station renderer: 222 controlled samples, 74 screenshots, both variants,
  exit zero and no logged errors. Inspected the helmeted pose beside the core pod.
  The greeting pauses normal play; the fixture advances visual time manually.
  This proves selected catalog rendering at station scale, not autonomous repair.
- Before/after audit: exactly 36 of 2,203 runtime PNG/JSON files changed; only
  selected west PNG paths. Other 2,167 unchanged; zero added.

Evidence: `output/branforth-west-chain-2026-09-22/` contains frozen baseline,
changed-path report, native/station captures, and validation/rebuild/pack logs.
Current test exports predate this work; no new export was made.

## Next action

Inspect Marsh's repair readability and transition gaps using the production player
and controller. Preserve his android/no-helmet contract and do not propagate new
welding art through unrelated legacy aliases. Then review the repaired crew in
ordinary play before preparing the next Windows/Mac test packages.
