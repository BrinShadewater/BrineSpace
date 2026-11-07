# Project handoff

Updated: October 7, 2026 · Project: BrineSpace · Task: static large-base command retention during zoom

## Objective and acceptance

Avoid replaying hydroponics-farm/storage-depot base drawing commands when only screen translation/zoom changes. Preserve selected pixels, line widths, clipping, filtering, door/water states and layering. Full original PC/Mac performance/release scope remains active; private trial is not normal source admission.

## Accepted decisions and constraints

Draw the same authored768×768 base commands around local zero; update the existing StaticBase CanvasItem position/scale to the actual screen rect. Keep room snapshot, reduced-motion and layout revision invalidation. Nonsquare/invalid bounds retain the original screen-space drawing fallback. Moonbay/Tidal/live props remain on their current paths. No raster atlas, image downscaling, quality reduction or renderer upgrade.

## Current state

Private artifacts under `output/large-local-retention-2026-10-07/`: standalone probe/results/owner, fresh `control/` and `candidate/` Main/Grid/large scripts/scenes, common benchmark, reports/logs/images/comparison and owner record. Candidate changes only StaticBase.submit bounds/key and CanvasItem transform; its key excludes changing screen rect for valid square rooms. Source generation removes duplicate Grid class_name/scene UID only in diagnostics. Normal source/art/UIDs unchanged.

Runners: `output/compressed-crew-2026-10-06/test-large-local-retention.py`, `compare-large-local-retention.py`. Full fixed selected renderer code used; owner layouts copied only to isolated profiles.

## Verification

- Native Godot4.7.2 Compatibility/RTX4070Ti:640/640 byte-identical raster pairs. Farm/depot ×4rotations ×2wall heights ×2water levels(0/.55) ×2nearest/linear filters ×5scales(.25/.5/.73/1/1.37) ×2fractional origins; includes closed/partial/open ports and nonwhite tint/alpha. This compares actual full base drawings under equivalent local/screen transforms; it does not yet test a single retained canvas across a continuous transform/invalidation sequence or Mac DPI.
- One actual current-source native1920×1080 matched40-room pair, idle/pan/zoom at1/2/4×,60frames per phase:9 full crew snapshots/drone dictionaries/door and light entries/zoom/power/drone phases equal; every texture endpoint equal. Clean engine logs, no missing art, warnings or leaked-instance diagnostics. No omitted renderer components/private crew storage.
- Total recorded retained-base redraws500→178. Zoom base callback means1.388→1.230ms at1×,2.467→2.010ms at2×,2.719→2.280ms at4×. This avoids work in target path; one pair does not establish repeatability or overall FPS improvement.
- Zoom p9551.292→49.397 /77.496→78.076 /66.359→59.210ms; idle/pan mixed. Frame gates remain failed; native texture endpoints~3.63–4.35GiB still exceed budget. No blanket correction of engine counter or driver VRAM inference.
- Final saved1920×1080 gameplay captures byte-identical; candidate inspected, art/UI present. A synergy toast obscures part of the station, so this final still is not full layer/motion or original bug/UI acceptance. `capture-comparison.json` records exactness and scope.
- Owner2,936 non-log files unchanged for both standalone and gameplay runs. No normal source changes or export. All test processes terminal.

## Next action

Test actual retained StaticBase across sequential fractional transforms and room/layout/door/water/settings invalidation, including nonsquare fallback. Reverse run order and repeat matched gameplay pairs before admission; resolve possible idle/frame regression concerns rather than treating fewer redraws as enough to certify60FPS. If accepted, install only this narrow helper change with relevant permanent native coverage/paired UID, then refresh packaged measurement. Continue exact-provider loading/ownership, remaining frame/memory/loading gates, original bugs/UI/motion, two-hour soak, target PC and native Mac certification. No publication authorized.
