# Marsh west/south carrying

Updated: September 22, 2026. Project: BrineSpace. Task: continue animation work.

## Objective and acceptance

Complete adjacent carrying turns with retained case and exact carry-loop joins.
All eight adjacent clips are integrated. Owner motion acceptance and ordinary
station transport review remain open.

## Accepted decisions and constraints

No Higgsfield. Built-in image generation authored independent west/south views.
Return reverses pose order; no mirroring. Preserve existing rooms and gameplay.

## Current state

Source/prompt: `character/marsh-carry-turns-v1/sources/west-south-01.*`.
Pair builder uses explicit centers and .24 source scale; canonical rebuild includes
the extended pair list. Runtime: `character/marsh-v2/supplemental/carry-turn-west-south/`.
Two400ms clips, ten184x184 frames, pivot92,172, standingHeight148, dry metadata.
Endpoints preserve existing carry frame zero exactly. Catalog/hash contract updated.
Earlier runtime PNGs and clearance are unchanged. No export or publication.
Review GIF/contact: `character/marsh-carry-turns-v1/review/west-south-01/`.
Preview endpoint holds are longer than runtime.

## Verification

- All forty carry-turn frames reproduce exactly; endpoints, binary alpha and reversal pass.
- Native player:120 samples, both new clips and exact frame-zero handoffs, zero failures.
  Agent inspected contact and native front-facing capture for scale/case position.
- Handoff:56 actor/body/equipment cases, zero failures, including pause/restore.
- Complete packs:20,367 checks, zero failures. Existing fixture source-loading
  warnings do not establish export compatibility.
- Validator:180 body states/890 references, no errors or border touches;
  211 original source frames and one original manifest unchanged.
- Evidence: `output/marsh-west-south-carry-2026-09-22/`. Clearance unchanged;
  no redundant route run. Normal transport and subjective motion acceptance pending.

## Next action

Four opposite-facing carry turns, then twelve swimming-with-cargo turns. Fresh
stable builds, ordinary station visual review and Apple Silicon testing remain open.
