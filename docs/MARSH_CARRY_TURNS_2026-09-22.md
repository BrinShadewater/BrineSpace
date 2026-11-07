# Marsh first carrying turns

Updated: September 22, 2026. Project: BrineSpace. Task: continue animation work.

## Objective and acceptance

Add east/north carrying turns with retained cargo, consistent scale and exact
carry-loop joins. Integrated and technically verified. Owner motion acceptance
and normal station cargo transport review remain open.

## Accepted decisions and constraints

No Higgsfield. Built-in image generation produced three independent poses; reverse
motion reverses order without mirroring. Cargo remains in front of the torso and
becomes occluded in rear view. Preserve existing rooms, gameplay and exports.

## Current state

- Frozen source and prompt: `character/marsh-carry-turns-v1/sources/east-north-01.*`.
- `tools/build_marsh_carry_turns.py` reproduces ten frames and is included in the
  canonical rebuild. Scale .25, measured horizontal centers, common boot baseline.
- Runtime: `character/marsh-v2/supplemental/carry-turn-east-north/`. Two400ms
  non-looping dry clips, five frames each. Canvas184x184, pivot92,172,
  standingHeight148; exact existing carry frame-zero endpoints.
- Catalog/hash contract updated. No earlier runtime PNG or clearance changed.
- Review GIF/contact: `character/marsh-carry-turns-v1/review/east-north-01/`.
  Preview endpoint holds are longer than runtime. No new release export.

## Verification

- Ten frames reproduce exactly; original endpoint joins, binary alpha and reversal pass.
- Native player:120 samples, both clips and destination-frame-zero joins, zero failures.
  Agent inspected contact and native capture for body scale and cargo occlusion.
  This is controlled playback, not normal transport or owner motion acceptance.
- Maintained handoff test:50 cases, zero failures, including pause/restore and
  resumed carry gait. Both new Marsh carry clips are required.
- Complete packs:20,193 checks, zero failures. Existing fixture source-loading
  warnings do not establish release compatibility.
- Validator:174 body states/860 references; no errors/border touches;
  211 original source frames and one source manifest unchanged.
- Evidence: `output/marsh-carry-turns-2026-09-22/`. Unchanged clearance needs no
  redundant route run.

## Next action

Ten dry-carry and twelve swimming-with-cargo turns remain. Continue the other
adjacent cargo views, check normal transport/interruption, then update stable
builds and complete Apple Silicon testing.
