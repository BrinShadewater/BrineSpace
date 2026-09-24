# Bill overall helmet-size handoff

Updated: September 21, 2026. Project: BrineSpace.

## Objective and acceptance
Reduce Bill's helmet overall following the owner's clarification. Preserve body
proportions, connected motion and equipment registration. Owner visual acceptance
remains open; before/after comparison is ready for inline review.

## Accepted decisions and constraints
Normal shell height 56 -> 48px, approximately 14% smaller. Visible width is 41px
for north/front/west and 39px east. Preserve original registration canvases and
visor anchors, head/body art, metadata, speed and stride. Fits already 48px high
or smaller remain unchanged. No Higgsfield, generation, publication or commits.

## Current state
The canonical rebuild in tools/rebuild_bill_art.py first validates historical
recipes, then applies the selected capped equipment pass. North-walk and south
work endpoint helpers accept recomposed gear; side-walk helpers retain historical
checks by default and allow the explicitly selected new equipment pass. The
connected-walk review CLI uses the same selected fit.
Changed helpers: build_bill_north_walk.py, build_bill_south_style_actions.py,
build_bill_alternating_east_walk.py, build_bill_alternating_west_walk.py and
build_bill_connected_walk.py (all under tools/).
Exactly 178 helmet PNGs changed; 4282 other inventoried runtime files are unchanged,
including every bare-body frame and metadata file. Selected policy and 1080 gear
hashes: character/major-bill-v3/sources/helmet-size-2026-09-21/selected-fit.json.
Animation-contract skill reference updated and synchronized to the installed copy.

## Verification
Evidence: output/bill-helmet-size-2026-09-21/.
Canonical rebuild passes; six test_bill_walk_surface.py tests and two
 test_bill_work_helmet_scale.py tests pass. Full library validation: 2214 frames,
zero errors/border touches; 780 original frames and 113 original manifests unchanged.
Godot consumer: 11773 checks, zero failures.
Native scripted transitions: 171 samples across four directions and both gear
variants, zero missing textures. All 171 bare-render comparisons are exactly
identical. Native stills and motion reviewed; helmet-before-after.gif shows the
old/new installed rear and side walks. This is not an autonomous expedition test.

## Next action
Show the inline before/after preview. Refresh Windows and Mac packages with the
walk and helmet changes, then run exact PCK audits and actual Windows EXE smoke.
The previous Windows-only 5fc export is now outdated and unverified. Apple Silicon
native testing remains pending. North/west work suit/backpack bulk differences
remain a separate polish item. Broad project goal remains unfinished.
