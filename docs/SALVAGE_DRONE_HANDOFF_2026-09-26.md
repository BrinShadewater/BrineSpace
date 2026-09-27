# Salvage drone directional animation handoff

Updated: September 26, 2026 · BrineSpace · Drone animation continuation

## Objective and acceptance
Owner authorized completing the next drone after Mining polish. Salvage now has
92 preview clips. New directional art awaits owner review; gameplay integration
is a separate remaining step.

## Accepted decisions and constraints
Use accepted v10 Salvage identity: heavier swimming hull, retrieval claw, matte
gray steel, muted cyan and separate blue/red/yellow top light. Shared fleet scale
is .34; south width 120.36 world units. Other headings use circular viewport
feature calibration and uniform resizing. Preserve Construction 8767 and Mining
8768. Independently authored heading views, no whole-body rotation substitutes.

## Current state
Pack: assets/salvage-drone-v1-2026-09-26/. Preview: http://127.0.0.1:8771/.
Ten eight-way travel/power states and three four-cardinal work states, 6,240 body
and cargo frame references each. 480 separable rotor phases retain continuous
spin across transitions. Work brakes before starting, departures queue until
completion, cargo survives direction changes, release deposits once.

Changed/added: build_full.py, validate_full.py, review_rigs.py, motion.mjs,
test_motion.mjs, preview.mjs, index.html, manifest, directional source images,
poses, full frames/atlases, review boards and provenance. Original pilot artifacts
remain historical; build_pilot.py would reset the manifest and must not be used
for the full set. Current build/validation commands are in the pack README.

## Verification
All 92 clips passed exhaustive export validation: review/full-validation.json.
All 6,240 body/cargo references match their atlases, silhouettes stay connected,
bounds and cargo joins pass, and 480 rotor phases pass silhouette/loop checks.
Controller checks passed: review/motion-checks.log. Browser recovery completed and
loaded southwest/power-off states were reviewed with no console warnings/errors.
Evidence: review/full-browser-recovery.png and review/full-browser-loaded.png.
Open and closed eight-heading boards reviewed, including wrist-mask corrections.
Native south room/Bill scale evidence and matching isolated owner-save fingerprints
from the pilot remain applicable because its registered base size is unchanged.
No gameplay tests or owner save writes were needed for this preview expansion.

## Next action
Owner follow-up corrected east/west rear turbines that faced toward the camera.
Selected `sources/east-west-v3.png` runs their axes horizontally along travel;
old rear-face rotor masks removed because the new forward faces are occluded.
All 26 changed clips and 120 rotor phases pass targeted validation; other six
headings retain their previous definitions. Browser east idle/west swimming
reviewed without console errors. See `review/TURBINE_CORRECTION.md` for exact
prompt, source, changed scope and evidence. This supersedes v2 side-view art.

September 26 polish follow-up: source identity, all eight headings and native
light/dark density reviewed. Fixed shutdown's exported spin reversal, preserved
phase-zero pixels, made controller power ramps frame-rate independent, and set
stop lamp red. Full 92-clip validation and expanded controller tests pass.
`review/POLISH_CLOSEOUT.md`, `polish-density.json` and the synchronized
`review/motion-audit.html` record the current revision. Source art and world scale
are unchanged; prior full-set export evidence is superseded by the polished run.

Owner visual review at enlarged and native size, particularly side-view proportions
and diagonal perspective. Painted headings are approximate projections, not an
exact shared 3D model. Then consider Godot animation/controller integration and
native movement/clearance testing with isolated APPDATA. No integration is claimed.
