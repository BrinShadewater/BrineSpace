# Marsh east/south carrying turns

Updated: September 22, 2026. Project: BrineSpace. Task: continue animation work.

## Objective and acceptance

Add east/south carrying and its reverse, keeping the case held at waist height
and joining current carry loops exactly. Integrated and technically checked;
owner motion acceptance and normal station transport review remain open.

## Accepted decisions and constraints

No Higgsfield. Independent built-in source generation; reverse pose order is
derived, not mirrored. Existing rooms, gameplay, equipment and exports preserved.

## Current state

- Source/prompt: `character/marsh-carry-turns-v1/sources/east-south-01.*`.
- Pair-aware builder uses measured centers and .23 scale for this larger source.
  Earlier recipes are unchanged; canonical rebuild consumes the extended pair list.
- Runtime: `character/marsh-v2/supplemental/carry-turn-east-south/`. Two400ms
  clips, ten frames,184x184, pivot92,172, standingHeight148, explicit dry metadata.
  Exact original carry frame-zero endpoints. Catalog/hash contract updated.
- Review GIF/contact: `character/marsh-carry-turns-v1/review/east-south-01/`.
  Preview endpoint holds are longer than runtime. No prior runtime PNG or clearance
  changed. No export, commit or publication.

## Verification

- Thirty frames across three carry pairs reproduce exactly; binary alpha,
  original endpoints and reverse ordering pass.
- Native player:120 rendered samples, both clips and exact frame-zero handoffs,
  zero failures. Agent inspected contact and native front-facing capture for
  registration/case position. Comprehensive motion acceptance remains open.
- Maintained handoff:54 cases, zero failures, including pause/restore and gait clock.
- Complete packs:20,309 checks, zero failures; existing fixture source-loading
  warnings do not establish release compatibility.
- Validator:178 body states/880 references, no errors/border touches;
  211 original source frames and one source manifest unchanged.
- Evidence: `output/marsh-south-carry-turns-2026-09-22/`. No repeated route test
  solely for unchanged clearance.

## Next action

West/south carrying, then the four opposite-facing carry turns. Six dry-carry
and twelve swimming-with-cargo turns remain. Normal-play visual review, fresh
stable builds and native Apple Silicon testing remain pending.
