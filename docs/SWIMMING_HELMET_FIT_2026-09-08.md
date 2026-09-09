# Project handoff

Updated: 2026-09-08 · Project: BrineSpace · Task: swimming helmet fit

## Objective and acceptance

Owner reports oversized, poorly fitted helmets while swimming. Fit the existing
equipment more closely to the head and review the actual loaded swimming poses.

## Accepted decisions and constraints

Preserve body artwork, asymmetric views, registered pivots, stroke timing, dry and
treading equipment. No new generated art. Owner visual acceptance remains pending.

## Current state

Latest per-pose correction supersedes the shared side offset below:
`character/crew-underwater-v1/swim-head-fit.json` records 36 measured face-edge
anchors, head bounds, source hashes and the retained 16-degree forward tilt.
The compositor aligns the visor to each pose and suppresses exposed scalp pixels
above/outside the shell, retaining the face opening and lower neck/shoulder pixels.
Initial broad masking cut into the suit and was narrowed before delivery. Bare
sources remain untouched. All 36 source hashes match; native loader comparison
passes and swim playback reports 0 failures. Reviewed enlarged bare/equipped
east/west sheets (`output/head-detail-east.png`, `output/head-detail-west.png`).
Animated comparison refreshed to pose4 with a close-up toggle. Browser automation
timed out, so owner motion review remains pending; native frame review is complete.

Latest owner adjustment: side helmets move one source pixel toward the face and
tilt 16 degrees forward (previously 12). Native loader comparison passes; refreshed
east/west pose sheets visually reviewed. Moving preview cache version is forward3.

Owner follow-up: the first smaller east/west fit remained too upright and clipped
the head. Side views now tilt 12 degrees forward about the neck seal, retain 75%
height but use 82% width, and sit one pixel higher. The previous horizontal shift
is removed. All 36 side poses re-exported through the native loader and visually
reviewed; all-direction loader comparison passes and playback regression reports
0 failures. Animated review URLs refreshed to avoid stale cached frames. Owner
motion acceptance of this follow-up remains pending.

`scripts/swim_helmet_fit.gd` (+ UID) composes existing helmet overlays at load time:
75% side-view size, 85% overhead size, centered with two-pixel facing adjustments
for side views. Recorded per-pose positions and foreground arm regions are retained.
`scripts/crew_sprite_player.gd` applies this only when loading swimming equipment.
All 12 live swim clips covered, including Veld's legacy north clip. Original baked
frames stay intact; old disk contact sheets therefore show the previous fit.

## Verification

`tests/preview_swim_helmet_fit.gd` (+ UID) verifies corrected frames match the actual
grid loader for all 72 poses and exports before/after native contact sheets. All four
direction sheets visually reviewed. Native run exits 0; `test_crew_swim_packs.gd`
reports 0 failures. Godot import exits 0. Existing conservative navigation envelopes
are retained. These checks do not establish a fresh full expedition acceptance.

`output/swimming-helmet-review.html` provides animated original/revised pairs using
manifest timings and native exported frames. Owner motion review remains pending.

## Next action

Owner review of fit in the moving comparison. No commit or push made.
