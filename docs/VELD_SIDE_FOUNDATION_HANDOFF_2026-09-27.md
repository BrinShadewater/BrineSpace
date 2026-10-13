# Side foundation handoff

Updated: 2026-09-27. Project: Brine Space.

## Objective and acceptance
Owner agreed side animations need a new drawing foundation rather than more
palette tweaks. Start Veld, review beside approved front, then motion and cast.

## Accepted decisions and constraints
Front A remains identity authority. Locked v4 equipment asymmetry remains.
Do not reuse drifted side sheets as design references or mirror opposite sides.
Existing runtime and 3D pilot work remain untouched.

## Current state
character/veld-side-foundation-v1 contains new east/west static standing masters,
raw built-in image_gen source, exact prompt, extraction script/hash evidence and
comparison.png beside the unchanged approved front. No palette processing applied.
This is a design review milestone, not a new animation pack.

## Verification
Actual RGBA inspected; alpha spans 0..254. Extraction found exactly two isolated
body components at alpha128; removed low-alpha surrounding residue. Views reviewed
at equal 148px standing height and approximately45px. Asymmetric gear retained.
No runtime or profile writes; no Godot tests needed for static study.
Owner art acceptance and room-context verification remain outstanding.

## Next action
Review face/proportions/silver/graphite against front. Refine master if needed,
then derive representative idle/walk/action before expanding the animation matrix.
Bill, Branforth and Marsh foundations follow the same process after Veld.
