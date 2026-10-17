# Project handoff

Updated: 2026-09-29 · Project: BrineSpace · Task: Veld east scanner interaction

## Objective and acceptance
Resolve the demonstrated first-interior body/head/material swap against accepted
idle. Owner accepted continuous-sleeve-v3; six bare and six equipped poses installed.

## Accepted decisions and constraints
Preserve existing scanner motion and timing. Canonical brown hair, warm skin,
science blue badge and neutral suit; subdued approved helmet. No new generation.

## Acceptance and installation — 2026-09-29

Owner accepted continuous-sleeve-v3 and asked to move on. Paired body/equipment
overrides installed in grid_canvas.gd and ACTIVE_ASSETS.json. Existing east action
test updated to assert selected interaction pixels. Native sprite fixture48 checks,
zero failures; source/gameplay capture inspected. Scratch APPDATA asserted;2730
real profile files unchanged. Unrelated drone_dust.gd compile errors occurred in
startup autoloads; clean overall startup is not claimed. First fixture timed out;
second completed with capture. Subsequent headless east-action regression90 checks/0 failures, no compilation
errors, zero profile changes. No release export. Next: east crouch/rise candidate.

## Continuous-sleeve correction — continuous-sleeve-v3

Owner still reported different-looking detached arm and awkward cuts in v2.
Close-up showed a smooth mismatched forearm and straight crop seam. Built-in
imagegen repaired the four moving sleeves as continuous shoulder/elbow/forearm
poses. Source, exact prompt and input saved locally; register_arm_source.py
registers source from its original resolution. build.py transfers only explicit
arm polygons, applies one clip neutral curve and restores accepted science badge
within its footprint. Whole generated figures are not substituted. Head/body,
exact idle endpoints and timing remain. Shoulder anatomy now follows corrected
source; v2's fixed-shoulder assertion is superseded. Prior builder/contact/GIFs
retained. All12 PNG/GIF checks pass and arm detail/contact reviewed. Corrected
playback remains staged for owner review; runtime and saves untouched.

## Shoulder/arm follow-up — arm-attachment-v2

Owner liked canonical-v1 except shoulder/arm anatomy. Broad old upper-arm pixels
were replacing the accepted shoulder. Now selected shoulder/blue patch and upper
sleeve remain; only elbow/forearm/glove/scanner are transferred. Idle far glove
cleared during motion. Prior builder/contact and versioned GIFs preserved. Sleeve
curve frozen in neutral-curve-canonical-v1.json, preventing mask edits changing
grading. Shoulder ROI rows54–71/x82–98 is asserted exact to selected idle across
all12 PNGs; prior decoded GIF/head/body/endpoints/timing checks pass. Contact sheet
reviewed. Candidate remains uninstalled pending corrected playback review.

## Current state
build.py and paired manifests use selected idle bodies and isolated retained
scanner arms. A single source-clip neutral sleeve curve applies throughout;
accepted badge mapped only through its footprint. Tiny occluded side torso uses
the same preserved source/mask as approved fitting. Existing runtime unchanged.
Sources hashed in checks.json; all processing reproducible locally.

## Verification
Exact idle endpoints and fixed upper head/lower body in PNGs. All12 decoded GIF
frames checked for stationary palette and clean exterior. Contact sheet inspected.
Browser playback at full and82/54/27px sizes provided for review. No native
acceptance or release evidence claimed for this staged candidate.

## Next action
Owner playback review, then actual loader/native check before installation.
Kneel/repair/stand and retained special-state inconsistencies remain separate.
