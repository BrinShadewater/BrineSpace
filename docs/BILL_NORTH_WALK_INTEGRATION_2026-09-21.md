# Bill canonical north walk integration

Updated September 21, 2026. BrineSpace. Broad goal remains unfinished.

## Objective and decisions
Give Bill clearer alternating rear-view contact/passing poses while retaining
canonical identity and connected limbs. Preserve speed, stride, timing, other
states and owner rooms. No new generation in this integration; the preceding
north source study used two built-in calls. No Higgsfield or publication.

## Current state
Canonical rebuild selects tools/build_bill_north_walk.py. Sources and frozen
recipe: character/major-bill-v3/sources/north-walk-canonical-2026-09-21/.
The original head, backpack, upper body, arms and helmet pixels are preserved
under recorded per-pose vertical translations. One connected pelvis-and-both-legs
region is transferred from the earlier motion draft and mapped to the original
palette. Knees, shins and boots are never moved independently. The first waist
registration study inherited the old head-bob sequence and exaggerated one pose;
selected v2 registers the canonical upper body to the new pose progression.

The full generated body and detail edit remain rejected for identity; only the
recorded lower-body region is selected. Raw prompts, sources and reproducible
motion normalization remain in the preceding source-study folder. Original
canonical frames, normalized motion inputs and output hashes are frozen. Recipe
status records its staging point; integration.json records later selection.

Exactly12north bare/helmet PNGs changed;4448other inventoried runtime art,
metadata/import files remain unchanged. No controller, clearance, manifest stride,
900ms cycle,184canvas,148standing height or92/172pivot changes.

## Verification
Evidence: output/bill-north-walk-integration-2026-09-21/.
- Full canonical rebuild passes and reproduces all12reviewed candidate images.
- Six surface tests pass, including translated canonical-pixel preservation,
  exact output hashes, binary alpha and every replacement pixel connecting through
  the waist to the torso. Bare/helmet lower regions are identical.
- Full library:2214frames,zero errors/border touches;780original frames and113
  original manifests unchanged. Actual consumer:11773checks,zero failures.
- Installed production-player render:27samples,bare/helmet,source/game scales,
  moving ground reference,zero missing textures. Native image inspected.
- Installed paid station:exit0,480captures,261unpaused north walks,actual getter
  verified with no candidate table/metadata overrides. Costs/failures enabled.
  Controlled opening/manual30Hz stepping is not ordinary full-expedition acceptance.
  Native station context inspected.
- Compact four-direction GIF composes source-scale crops from the latest installed
  native captures for each direction. It is a comparison, not a turning sequence.
- Pipeline reference synchronized; visual bible and CURRENT_STATUS updated.

## Limits and next action
This repairs pose differentiation and identity continuity; anatomical world-space
foot locking is not established. Comparing selected Veld/Branforth sources showed
similarly sparse six-frame north loops and comparable stride values. Do not impose
zero sliding as a new completion standard or change walking speed to satisfy an
image-bound heuristic. Owner visual judgment and ordinary expedition review remain
open. Review idle/walk/work transitions across the repaired set, then refresh the
Windows/Mac packages, which predate all four recent walk integrations. Continue
room polish, measured performance work and Apple Silicon testing preparation.
