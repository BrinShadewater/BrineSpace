# Project handoff

Updated: 2026-09-26 · Project: BrineSpace · Task: Common-prop density and style calibration

## Objective and acceptance
Owner requested consistent pixel density relative to larger props and the closest practical match to existing artwork. All 37 current candidates have size-calibrated exports. Visual sizes remain proposed until owner acceptance and room placement.

## Accepted decisions and constraints
Use the September 26 bible's painted sprites, not coarse pixel art. Smaller props need smaller raster budgets, not uniformly sized thumbnails. Preserve accepted seating geometry and neutral materials. Original masters, locked references, runtime registry and owner layouts remain unchanged.

## Current state
- game-size/: 37 transparent PNG exports from the current six packs, excluding rejected first-pass props and rejected literal-overhead seating.
- revised-masters/: four metal-seat material corrections generated through built-in image_gen. Smooth silver gradients replaced with painted gray steel. Exact prompts and source mapping retained in material-prompts.json and material-sources.json.
- build_exports.py: repeatable proportional premultiplied-alpha LANCZOS export, matching the accepted exporter's resampling. Visible bounds use alpha >=16 plus four source pixels of padding; original alpha inside that crop is preserved. Very faint exterior pixels had been making stool size calibration wrong. Eight pixels of final canvas padding added.
- manifest.json: every source/hash, crop, size budget, final size/hash and suggested display width. No runtime binding is implied.
- comparison-light.png / comparison-dark.png: compact comparison with unchanged accepted references at 1:1 library pixels. Full category sheets and world-scale-review.png cover all 37.

## Scale evidence
Locked native references include a 396x224 sofa, 360x201 cabinet/bookcase, 223x223 armchair-and-table and 264x249 scientific cabinet. Catalog display-width/native-width is about 0.336–0.340 for these. Proposed new exports use 0.34 world units per library pixel (~2.94 pixels/unit); the nearest-filtered world-unit preview follows grid_canvas.gd. Camera zoom still changes final screen pixels.

Visible budgets: seating 75–145 pixels per axis, small plants 55–140 (trough up to 200 wide), tall plants up to 230–250 high, larger furniture up to 310 wide. Each fits proportionally. These are reasoned starting sizes relative to the reference family, not measurements of owner placement. Variants share size budgets. The tabletop succulent is intentionally much smaller than a floor plant.

## Verification
37 exports rebuilt and checked: RGBA, transparent exterior, alpha peaks >=250, source hashes unchanged during export. Reviewed the full world-unit sheet, native category sheets and final light/dark compact comparisons. Painted foliage and upholstery read consistently at reduced scale; four metal surfaces corrected for closer material matching. Complete leaf tips, supports and silhouette edges retained. Large earlier preview cards were misleading for relative scale.

No game integration or room/crew fixture was changed. Exact seated-character fit, collision, floor footprints, actual zoom and live lighting remain installation checks; standalone sheets cannot certify them. Owner visual approval of revised metal finish and proposed sizes is pending.

## Next action
Use game-size exports and manifest display widths together when integrating; using a master at these dimensions would reintroduce excess density. Verify a room with existing furniture and crew before wider placement.
