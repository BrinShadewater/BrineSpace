# Marsh west/north carrying turns

Updated: September 22, 2026. Project: BrineSpace. Task: continue animation work.

## Objective and acceptance

Add west/north carrying and its reverse with retained front-held cargo and exact
carry-loop endpoints. Technically integrated; owner motion acceptance and normal
station transport review remain open.

## Accepted decisions and constraints

No Higgsfield. Independent built-in image generation, no mirroring. Reverse pose
order is derived. Existing rooms, gameplay, equipment and exports preserved.

## Current state

Source/prompt: `character/marsh-carry-turns-v1/sources/west-north-01.*`.
Pair-aware `tools/build_marsh_carry_turns.py` and canonical rebuild include both
carry pairs. West source scale is .265 (the .25 trial was too short); measured
centers and a common boot baseline preserve registration. East recipe is unchanged.

Runtime: `character/marsh-v2/supplemental/carry-turn-west-north/`, two400ms clips,
ten frames,184x184 canvas, pivot92,172, standingHeight148, explicit dry metadata.
Catalog and source contract updated. No earlier runtime PNG or clearance changed.
Review GIF/contact: `character/marsh-carry-turns-v1/review/west-north-01/`.
Preview endpoint holds are longer than runtime. No new export or publication.

## Verification

- Twenty frames across both carry pairs reproduce exactly, with original endpoints,
  binary alpha and reverse ordering checked.
- Native player:120 rendered samples, both clips and exact frame-zero handoffs,
  zero failures. Agent inspected registered contact and native capture for body
  scale and cargo placement; this is not normal transport or owner acceptance.
- Maintained handoff:52 cases, zero failures, including pause/restore and gait clock.
- Complete packs:20,251 checks, zero failures. Existing fixture source-loading
  warnings do not establish release compatibility.
- Validator:176 body states/870 references; no errors/border touches;
  211 original source frames and one source manifest unchanged.
- Evidence: `output/marsh-west-carry-turns-2026-09-22/`. No redundant route run
  for unchanged clearance.

## Next action

South-facing carry pairs, then opposite-facing carrying turns. Eight dry-carry
and twelve swimming-with-cargo turns remain. Normal-play visual review, fresh
stable builds and Apple Silicon testing remain pending.
