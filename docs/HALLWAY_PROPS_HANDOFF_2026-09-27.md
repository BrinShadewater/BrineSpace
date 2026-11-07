# Project handoff

## Superseding closeout - September 28, 2026

All 19 non-drone props are Common library entries, grouped by searchable family labels. See [current closeout](COMMON_PROPS_SESSION_CLOSEOUT_2026-09-28.md); historical pending selections below are superseded by the current manifest and polished sources.


Updated: 2026-09-27 · Project: BrineSpace · Task: small-medium hallway props

## Objective and acceptance
Three walk-around props matching the accepted muted industrial hallway art.
Owner visual acceptance remains pending at http://127.0.0.1:8812/hallway-props/.

## Accepted decisions and constraints
Overhead perspective, subdued metals, native scale calibrated against the existing
52-unit cart. New props are 44/46/40 units wide. No automatic layout changes.

## Current state
Generated originals and exact prompts in assets/hallway-props-v1, registered as
sp-hall-breathing-cabinet, sp-hall-maintenance-caddy and sp-hall-pressure-pedestal
in rooms/station-props-v2/props.json. Registration crops transparent margins;
source pixels remain unchanged. Explicit footprints/collision boxes support walking.
These are decorative props, without oxygen or inventory gameplay.

## Verification
tests/test_hallway_props.gd and paired UID; corridor run_review.py --props uses
scratch APPDATA. All 36 placements pass native navigation using production collision
and segment checks, across three shapes and four rotations, with 10-unit clearance.
Native comparison visually inspected. Real saves/layouts unchanged; last_session.json
changed while concurrent Godot sessions were active, so a wholly unchanged owner
profile cannot be claimed. No owner file was restored or modified by this work.
Raw image hashes, bounds, prompts and evidence recorded in the pack manifest.

## Next action
Owner review of /hallway-props/. Available in Studio; no release/export performed.

## Crate-stack extension
Added stacked-sage-crates and stacked-slate-cases, 46 and 50 units wide, with more
overhead lid-dominant artwork. Originals, prompts and hashes retained in the pack.
Registered both in station-props-v2; existing layouts untouched. Native fixture now
passes 60 placements (24 new), including collision and all exit routes. Both native
straight-hall previews visually inspected. Only concurrent last_session.json changed
in the real profile during isolated validation; saves/layouts unchanged. Gallery
/hallway-props/?v=crates#crates is ready for owner review. Cleanup experiment did not
improve the second source and was not selected; original alpha renders cleanly at
native scale. No release or commit.

## Barrel extension
Added sealed-sage-barrel and paired-slate-barrels (34/49 world-unit widths) to the
station library, preserving source pixels and exact generation prompts. The single
and pair use lid-dominant overhead views and subdued matte metals. Conservative
solid footprints registered; existing layouts unchanged. Native fixture passes
84 placements, including 24 new barrel cases, across three shapes and four rotations
with 10 units of crew clearance. Both straight-hall native previews inspected.
Latest isolated run left the entire owner profile unchanged. Review gallery
/hallway-props/?v=barrels#barrels ready; owner acceptance pending. No export/commit.

## Perspective variant
Owner requested a changed perspective for stacked crates. Added stacked-crates-depth,
a 48-unit two-crate prop with slightly more visible front walls, keeping older
overhead sources intact. Prompt, original and hash recorded. Registry and native
fixture extended; 96 cases pass including 12 new placements, owner profile unchanged.
Native corridor view reviewed. Gallery /hallway-props/?v=depth#crate-depth; owner
visual acceptance pending. Existing layouts unchanged.

## Shape and color extension
Added long-slate-case, hex-clay-crate and olive-capsule-crate at 48/39/38 units,
with muted slate-blue, clay-brown and olive finishes. Originals/prompts/hashes
retained; Studio registrations include solid footprints. Existing layouts unchanged.
132 native placement cases pass including 36 new cases, real owner profile unchanged.
Three-up native comparison visually reviewed; source transparency renders cleanly
at native scale. Review /hallway-props/?v=shapes#shapes, owner acceptance pending.

## Potted plant extension
Added sage-leaf-planter (35 units) and fern-trough-planter (48 units), with matte
muted foliage/pots and an overhead camera. Exact prompts, originals and hashes
retained in the pack. Station registry and fixture extended; conservative collision
footprints include foliage envelope. 156 native placements pass including 24 new
plant cases, real owner profile unchanged. Both native hallway views inspected.
Existing layouts unchanged. Review /hallway-props/?v=plants#plants; owner visual
acceptance pending. No oxygen production or other gameplay behavior added.

## Small tall plants - September 28
Added snake-plant-pot and cane-plant-pot at 30/32-unit widths. Matte foliage,
small pots and taller silhouettes; source originals/prompts/hashes retained.
Collision and depth anchors follow pot contact, not full leaf height. Native
previews reviewed, 24 new placement cases pass (180 total), owner profile unchanged.
Existing layouts preserved. Review /hallway-props/?v=tall-plants#tall-plants,
owner acceptance pending.

## Four plant types - September 28
Added succulent-bowl, rubber-plant-pot, asparagus-fern-pot and dwarf-palm-pot
at 30/34/38/40-unit widths. Matte muted foliage; overhead perspective. Rubber
plant first candidate resembled the sage reference too closely and was replaced
with plain rounded dark leaves; both prompts recorded. Originals/hashes retained.
48 new placement cases pass (228 total), owner profile unchanged. Native four-up
comparison reviewed. Existing layouts unchanged. Review
/hallway-props/?v=four-plants#four-plants; owner acceptance pending.
