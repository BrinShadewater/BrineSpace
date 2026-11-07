# Crew walking consistency review

## Objective and acceptance
Owner accepted Branforth rear v2 and authorized shared scale, colour, timing and idle-transition review before integration. All Bill/Branforth walks are visually accepted; staged idle holds and cadence proposal are new review material.

## Accepted decisions and constraints
Preserve all accepted walk pixels and dark suit limits. No generation spending. Veld runtime stays untouched. No synthetic breathing, interpolation or per-frame geometry normalization.

## Current state
`character/crew-walk-stage-v1/` holds two staged manifests referencing accepted walk files, eight darkening-only master idle holds, all-12-clip comparisons, direct idle/walk transition review, colour/size measurements and source hashes. `matched-cadence-review.gif` is an alternative timing-only preview at 1500ms per full stride; proposal JSON is not applied to manifests or runtime.

## Verification
Two staged manifests pass with zero errors/warnings. All 12 clips are 184-square with intended standing height148; measured walking heights span141–152px. No clipped frames. 510 accepted Bill/Branforth PNG hashes captured and unchanged through build. Static contact review shows broadly consistent scale and dark suit tone; Veld front/rear neutral samples remain slightly cooler. Source cadence varies: Bill south1194ms versus east1667ms per cycle; Branforth south1056ms versus east1916ms. Other candidate directions and Veld use1500ms. Comparison GIFs preserve full frames and either original timing or explicitly proposed timing. Direct arbitrary-phase idle/walk joins expose discontinuities; static inspection does not establish temporal smoothness or runtime acceptance.

## Next action
Review original versus matched cadence and direct idle joins in motion. Use current Veld cadence as candidate baseline, then calibrate movement-distance stride and choose appropriate stop phase during integration; avoid confusing multi-cycle clip duration with one stride. No accepted timing or runtime artwork changed. Remaining balance last verified76, zero spent here.
