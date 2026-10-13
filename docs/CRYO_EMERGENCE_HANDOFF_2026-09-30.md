# Project handoff

Updated: September 30, 2026 · Project: BrineSpace · Task: Human cryopod emergence

## Objective and acceptance
Begin blue inside the chamber, gradually regain natural colour, then step out
using the characters' established identity, perspective, density and live scale.
Latest owner direction adds a slower exit, falling onto the floor and standing
back up. The final4.6s of the existing wake timer now covers that physical chain.
Owner found the revised motion good, with the remaining correction that live
crew must start exactly where they land. Landing v2 fixes that screen-space join.

## Accepted decisions and constraints
Use selected live bare south idle/walk frames, not newly generated character
poses. Preserve recovery rules and saved timing. Marsh retains separate charging.
Existing local changes from other character/environment sessions were preserved.

## Current state
Installed layered playback in `scripts/architect_cryo_art.gd`; display textures
and common release-node selection in `scripts/architects.gd`; ward navigation
warm-up in `scripts/cryo_recovery.gd`; removed post-release blue tint from
`scripts/cryo_release_effect.gd`. Empty closed source, registered insert and exact
prompt live in `character/cryo-layered-v1/`; deterministic builder is
`tools/build_cryo_layered.py`. Opening blends closed/open artwork; existing south
walk provides the step. No character pack, runtime registry or export changed.

## Verification
Final focused headless tests: cryo exit timing, architect recovery and cryo
recovery all PASS, including existing save/Continue and recovery constraints.
Native fixture `tests/playtest_cryo_layered.gd` checks actual selected frames,
paused pixel equality and matching release endpoints for all three core actors
and rotated wards. Native captures/motion previews in `output/cryo-layered-v1/`.
Source diff whitespace checks pass. Agent visual review is not owner acceptance.

All task Godot launches used scratch APPDATA, with scratch files confirmed.
Owner fingerprint: 2,775 initial compared records; 36 added/removed hash records across
nine changed non-log files plus rotated logs. Active godot.log was locked and
excluded. Changed files include other content/lighting/surface parity fixtures,
dialogue_trace.log and last_session.json; attribution remains unresolved amid
concurrent sessions. No profile restoration attempted. Evidence is in profile
before/after/delta files; do not claim the whole profile was unchanged.
Final progress-save, loop-checkpoint/sidecar and room-layout hash comparison has
zero deltas. Final native-motion.log passes; review GIF has 68 encoded frames
(69 source samples; identical adjacent capture merged by GIF encoding), plus
three-actor contact and exit-motion strips. Review assembler:
`python tools/build_cryo_review.py`. Closed housing exterior pixels and generated
source exterior alpha checked; existing source registration preserved.

## Next action
Owner review of the native motion previews; playable export validation remains
pending. No commit, push or release export was requested or performed.

## Slow exit, fall and recovery — September 30, 2026
Owner requested slower exit followed by a fall to the ground and standing up.
Installed three new master-referenced eight-pose sources in
`character/cryo-fall-recovery-v1/` with exact live-idle endpoints. Fixed source
scale/material grade and floor pivot; retained standing148/runtime65.28 scale.
Physical chain: opening0.55s, step1.4s (previous0.67s), fall0.7s, floor hold0.55s,
rise1.25s, idle0.15s. Existing wake/release/save/gameplay rules remain unchanged.
Legacy six-pose fallback retains its old1.2s timing. No normal crew action or
registry modified. Sources/prompts, builder and registration preserved.

Changed cryo art/display, timing/native fixtures and review assembler; added
`tools/build_cryo_fall_recovery.py` and `tests/test_cryo_fall_recovery.py`.
Packaging floor/scale/exact endpoints/joins checks and all three sprite manifest
validators PASS, no warnings. Architect/cryo recovery PASS; final timing PASS
after correcting an explicit test variable type. Native all-three pause, exact
release point, inactive grounded actor, grounded save/Continue, rotated ward
checks PASS. Native contact and complete fall/rise strip visually inspected.
Review GIF:86 source samples,50 encoded frames with identical holds merged.
Evidence in `output/cryo-fall-recovery-v1/`. Source whitespace check passes.

Scratch APPDATA/LOCALAPPDATA confirmed;2,789 owner profile records compared,
active godot.log excluded.25 hash delta records during concurrent activity;
attribution unresolved. Progress/checkpoint/layout hash comparison has zero deltas.
No profile restoration, commit, push or playable export performed. Owner review
of the revised motion is next; earlier visual acceptance does not cover new art.

## Landing position v2 — September 30, 2026
Owner approved the appearance with a position correction. The previous native
unit check mistakenly added the renderer lift twice: main's position helpers
subtract14.592 and grid adds it back, so the live sprite stood above the animated
landing despite the asserted actor-foot equation. Shared `landing_point` now
supplies both the animated endpoint and actual actor.foot. Candidate floor
clearance checks the true shifted landing point. Animated landing stays in the
accepted location; all source pixels, fall/recovery timings and Marsh remain.

Changed `scripts/architects.gd`, native handoff assertions and review output
recognition. Architect/cryo recovery PASS. Native screen-position/can-stand,
pause, grounded Continue, all-three core/rotated-ward checks PASS. One earlier
native run failed paused pixel equality at the grounded sample; diagnostic
rerun passed without production changes, so the intermittent fixture issue
remains unattributed. Failure-only state/capture diagnostics retained. Corrected
native before/after handoff visually inspected; latest evidence and preview:
`output/cryo-fall-landing-v2/`, passing log `native-probe.log`.
Scratch APPDATA/LOCALAPPDATA used; owner fingerprint evidence in that directory.
2,796 records compared (active log excluded),16 hash delta records across other
probe/hand-backdrop files and logs; attribution unresolved. Progress/checkpoint/
layout hashes unchanged. No owner files restored or modified by this task.
Owner review of the corrected join and playable export validation remain pending.

## Opening vapour follow-up — September 30, 2026
Owner requested an icy-blue puff when the chamber opens. Installed a finite
five-lobe burst from the lower opening seam, reusing the existing painted
`leak-puff` environment sprite with icy-blue tint. Saved wake progress controls
expansion and fade; Reduced Motion uses stationary lobes. Starts just after
opening begins and dissipates before release, keeping the face unobscured.
No source art, character registration or recovery rules changed.

Changed `scripts/architect_cryo_art.gd`, the display preference in
`scripts/architects.gd`, timing/native fixtures and review assembler's optional
output argument. Timing test PASS; native all-three core/rotated-ward handoff
and paused vapour pixel-equality checks PASS. Strip inspected at station scale;
new motion GIF and logs in `output/cryo-layered-vapour-v1/`. Source diff check
passes. Scratch APPDATA/LOCALAPPDATA confirmed; 2,777 owner files compared with
zero hash deltas, excluding active godot.log. Earlier concurrent-profile
uncertainty above is historical and remains unreconciled. Owner/release visual
acceptance remains pending.

## Polish v2 — September 30, 2026
Owner requested continued polishing. Added a restrained glass veil/reflection
over the occupant, staggered the five vapour lobes with slight upward curl and
increased their readability. Exit uses eased distance and samples a complete
selected south walk cycle by that distance; standing scale, pivot, endpoint,
saved wake timing and recovery rules stay fixed.

Changed cryo art/display and focused fixtures. Architect recovery PASS; timing
PASS after changing a new zero-boundary assertion to approximate float equality.
Native selected-frame/pause/core/rotated-ward checks PASS for all three humans.
Contact and complete exit strip inspected; new GIF/logs in
`output/cryo-layered-polish-v2/`. Source whitespace check passes.
Scratch APPDATA/LOCALAPPDATA confirmed. Compared 2,779 owner profile files,
excluding active godot.log: eight hash delta records during concurrent activity;
progress/checkpoint/layout files unchanged. Attribution remains unresolved;
no restoration attempted. Owner visual acceptance and release checks pending.

## Cryopod fog whoosh — September 30, 2026

The opening now releases nine denser icy-blue painted clouds with a fast outward
whoosh, a brief dense hold, and a slow fade over 4.35 seconds. Fog remains low
around the chamber through the fall and dissipates during recovery. Saved wake
time drives all motion; reduced motion uses fixed cloud positions. Character
art, scale, timings and landing handoff remain unchanged.

Changed `scripts/architect_cryo_art.gd`, focused timing assertions, and the native
fixture output destination. Timing PASS (zero failures); native selected identities,
pause, restore, core and rotated-ward handoffs PASS. Contact sheet visually reviewed;
86-sample three-character GIF: `output/cryo-fall-landing-fog-v3/thaw-and-exit.gif`.
Scratch APPDATA/LOCALAPPDATA used. Owner profile: 2802 files compared, 0 changed
paths during concurrent activity, 0 progress/checkpoint/layout changes; active
godot.log excluded. Attribution of concurrent changes unresolved; no restoration.
Owner visual acceptance remains pending. No export or commit.

## Cryopod translucent fog and delayed colour recovery — September 30, 2026

Owner requested translucent cloud at the base, blue character through the fall,
colour recovery starting on floor contact, and a few seconds of unfreezing first.
Interpreted "start blood" as "start blue" in context and stated this to owner.
Installed five pale low-opacity painted cloud lobes with slower drift near the
base. Frost clears from the closed glass during the existing 2.4-second displayed
pre-opening period. Characters stay cold blue until GROUND_START, regain colour
through recovery, and reach natural colour before the unchanged live handoff.
No changes to master artwork, scale, fall/recovery poses, costs or saved durations.

Changed scripts/architect_cryo_art.gd, tests/test_cryo_exit_timing.gd and native
fixture output destination. Timing PASS; native all-three selected identities,
pause/restore and core/rotated-ward handoffs PASS. Native contact visually reviewed;
86-sample motion preview is output/cryo-fall-landing-thaw-v4/thaw-and-exit.gif.
Scratch APPDATA/LOCALAPPDATA used; 2804 owner files compared, 1 changed paths,
0 progress/checkpoint/layout changes (active godot.log excluded). No restoration.
Owner visual review next; no commit or export.

## Cryopod lighter cold tint and closed-chamber mist — September 30, 2026

Owner requested slightly less blue characters and vapour inside the closed pod.
Cold tint changed from (0.30,0.64,1) to (0.44,0.72,1), retaining floor-contact colour
recovery. Three translucent painted mist lobes curl inside the chamber below the
glass layer, remain after the frost clears, and fade with door opening. Their
rectangles stay within the glass; saved wake drives movement and reduced motion
fixes it. Existing external base cloud, artwork, scale and handoff stay unchanged.
Changed scripts/architect_cryo_art.gd and focused timing/native fixtures.
Timing PASS; native all-three identities, pause/restore and core/rotated ward
handoffs PASS. Native contact visually reviewed; 86-sample preview at
output/cryo-fall-landing-mist-v5/thaw-and-exit.gif. Scratch profiles used;
2804 owner files fingerprinted, 1 changed paths, 0 progress/checkpoint/layout
changes (active godot.log excluded). Concurrent change attribution unresolved.
Owner visual review next; no commit or export.

## Cryopod density, perspective and grading polish — September 30, 2026

Owner requested another density/perspective/art-style/colour pass. Reviewed all
three authored recovery strips against their directional master inputs and
selected matte idle anchors. Existing fixed standing scale, floor registration,
linear crew sampling and exact idle endpoints retained; no pose resampling.
Effects were the demonstrated mismatch: cached linear-sampled painted mist now
matches crew sampling without changing housing. Flattened the external cloud
vertically by about 21 percent for floor perspective, reduced cyan saturation
in all mist/frost layers, and lowered closed frost opacity from .38 to .27 to
preserve graphite cloth, silver hardware and department detail readability.
No new image generation; master-derived poses retain their existing small-detail
simplifications. Changed cryo renderer, native output destination and pack README.

Timing PASS; recovery packaging contract PASS; native all-three identity,
pause/restore, core and rotated-ward landing handoffs PASS. Agent reviewed native
contact sheet and source strips; motion preview provided for owner review:
output/cryo-fall-landing-grade-v6/thaw-and-exit.gif (86 captured samples).
Scratch APPDATA/LOCALAPPDATA used; 2805 owner files compared, 2 changed paths,
0 progress/checkpoint/layout changes, excluding active godot.log. Concurrent
change attribution unresolved; no restoration. Owner acceptance remains pending;
no commit/export or gameplay changes.

## Cryopod sequence accepted for gameplay and derelict cryolabs — September 30, 2026

Owner approved adding the polished sequence to gameplay and found derelict
cryolabs. Confirmed installed shared routing: core uses Architects.pod_for_display;
unrepaired derelict and repaired cryolab both use ward_for_display and the same
layered cryo renderer. No separate old animation remains on these human routes.
Added explicit native assertions for found, unrepaired wards: survivors retain
selected crew textures, remain unrecovered and have the shared painted mist.
Artwork and gameplay rules unchanged; powered emergence remains gated by repair,
supplies and berths, with no premature crew entry.
Architect recovery and cryo recovery regression tests PASS. Native found-ward,
all-three identities, pause/restore and rotated-ward landing checks PASS.
Evidence: output/cryo-installed-v7/{regression,native}.log; visuals remain grade-v6.
Scratch APPDATA/LOCALAPPDATA used; 2808 owner files compared, 11 changed paths,
0 progress/checkpoint/layout changes, excluding active godot.log. Concurrent
change attribution unresolved. Pack README records owner acceptance. Source
integration complete; playable export not requested, no commit/export.
