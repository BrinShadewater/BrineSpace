# Marsh west/north swimming turns

Updated: September 22, 2026. Project: BrineSpace. Task: continue crew animation work.

## Objective and acceptance

Add west-to-north swimming and the reverse with consistent body scale and exact
destination-loop joins. Integrated and technically verified; owner visual
acceptance and ordinary station play review remain open.

## Accepted decisions and constraints

No Higgsfield. Built-in image generation authored the west views independently;
no mirroring of the east sheet. North-to-west reverses the selected pose order.
Existing rooms, equipment, gameplay, audio and release builds remain unchanged.

## Current state

- Source and exact prompt: `character/marsh-swim-turns-v1/sources/west-north-01.*`.
  The west endpoint is frozen beside the already-frozen north endpoint.
- `tools/build_marsh_swim_turns.py --pair west-north` reproduces the new pair;
  default east/north output retains identical runtime pixels. Canonical rebuild
  includes both pairs. No new generation is needed for a rebuild.
- Runtime: `character/marsh-v2/supplemental/swim-turn-west-north/`. Two clips,
  ten frames, 400 ms each (60/90/100/90/60), non-looping, water-pose metadata.
  Canvas 184x208, pivot 92,172, standing height 148; transparent padding only.
- Review: `character/marsh-swim-turns-v1/review/west-north-01/`, contact sheet
  and animated GIF. Preview endpoints are held longer for inspection.
- Supplemental source hashes and catalog updated. No pre-existing runtime PNG
  or clearance changed. No export, commit or publication made.

## Verification

- Python reproduction checks both pairs: all twenty runtime frames exactly match;
  binary alpha, existing endpoints and reverse order pass.
- Native fixture: 120 rendered samples, both new clips selected, two exact
  destination-frame-zero handoffs, zero failures. Agent inspected captured poses
  and the contact sheet for head scale, compact rear legs and registration.
  This does not establish owner approval or comprehensive motion quality.
- Maintained turn handoff test: 40 actor/body/equipment cases, zero failures,
  including pause/restore and the appropriate distance/time clock.
- Complete packs: 19,823 checks, zero failures. The test's source-image-loading
  warnings remain; this is not release-export verification.
- Validator: 164 body states / 794 references, zero errors or border touches;
  211 original source frames and one original manifest unchanged.
- Prior battery-route result remains relevant to unchanged clearance; no rerun
  solely for this addition. Evidence: `output/marsh-west-north-turns-2026-09-22/`.

## Next action

Add east/south and west/south pairs, then remaining opposite-facing swimming
turns. Eight directed swimming turns, twelve carrying turns and twelve swimming
with cargo turns remain. Review connected motion during ordinary station play
before considering the animation work visually accepted. Stable release updates
and native Apple Silicon testing are still pending.
