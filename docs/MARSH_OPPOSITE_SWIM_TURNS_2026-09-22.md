# Marsh opposite-facing swimming turns

Updated: September 22, 2026. Project: BrineSpace. Task: continue animation work.

## Objective and acceptance

Complete four opposite-facing swimming transitions with exact endpoint joins.
All twelve swimming turns are integrated and technically checked. Owner motion
acceptance and ordinary station play review remain open.

## Accepted decisions and constraints

Reuse independently authored adjacent poses without mirroring or new generation.
No Higgsfield, room/gameplay changes, export, commit or publication.

## Current state

- `tools/build_marsh_opposite_swim_turns.py` composes east/west through north
  and north/south through east. Return clips reverse the pose order. The identical
  shared middle frame is stored once with its combined120ms duration.
- Each of four clips is800ms with nine frames:60/90/100/90/120/90/100/90/60.
  Canvas184x208, pivot92,172, standingHeight148, water metadata. Endpoints are
  exact current swim frame zero with transparent padding only.
- Runtime folders: `character/marsh-v2/supplemental/swim-turn-east-west/` and
  `swim-turn-north-south/`. Canonical rebuild, catalog and hash contract updated.
- Review GIFs/contact sheets: matching pair folders under
  `character/marsh-swim-turns-v1/review/`. Preview endpoint holds are lengthened.
- No pre-existing runtime PNG or clearance changed. Sources remain the preserved
  adjacent sheets; these are derived sequences, not newly authored half-turn art.

## Verification

- Reproduction checks all76 turn frames, exact endpoints, binary alpha and reversal.
- Two native fixtures,120 rendered samples each: all four clips selected with
  correct destination-frame-zero handoff, zero failures. Agent inspected contact
  sheets and native midpoint captures. Comprehensive motion quality remains open.
- Maintained handoff:48 actor/body/equipment cases, zero failures, including
  pause/restore and proper clock continuation. Every Marsh swimming direction
  pair is now required rather than skipped when absent.
- Complete packs:20,135 checks, zero failures. Existing source-loading fixture
  warnings do not establish export compatibility.
- Validator:172 body states/850 references, zero errors/border touches;
  211 original source frames and one source manifest unchanged.
- Evidence: `output/marsh-opposite-swim-turns-2026-09-22/`. Clearance unchanged;
  previous route evidence remains relevant without a redundant run.

## Next action

Twelve dry-carry and twelve swimming-with-cargo turns remain. Review the completed
swimming matrix during normal station movement, especially interrupted turns and
the longer half-turns. Updated stable builds and Apple Silicon testing remain pending.
