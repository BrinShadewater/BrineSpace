# Mining rover animation handoff

Updated: September 26, 2026 · Project: Brine Space

## Objective and acceptance
Continue from the accepted Construction polish with the Mining drone. Owner
specified a rover that drives along the ocean floor, matching the established
art style, size, perspective and pixel density. New rover animation art awaits
owner visual review; this is not a gameplay integration milestone.

## Accepted decisions and constraints
Preserve approved-v10 four-wheel identity, articulated suspension, central
processing bay, muted cyan/gray steel and overhead camera. Eight travel headings,
four cardinal mining actions, separate blue/red/yellow pulsing top lamp. No
mirrored views, floating movement or propellers. Construction remains intact.

## Current state
`assets/mining-rover-v1-2026-09-26/` contains source/provenance, reproducible Python
builders, manifest, 44 clips, separated effects, review media and HTML preview.
Frame contract: 448×448, pivot (224,224), 30fps, proposed 0.34 world units/library pixel.
South silhouette 246 px / 83.64 world units. Diagonal registration was reduced after
the first comparison showed oversized tyres; dimensions are visually matched,
not an exact 3D reconstruction. Compact deployable front drill added.

Preview: http://127.0.0.1:8768/. Existing Construction review stays on 8767.
New isolated fixture: `tools/capture_mining_rover_scale.gd` plus paired UID.

## Verification
Native production Mining Drone Bay/Bill scale capture completed at 69.12 / 83.64 / 96
world widths. Owner save fingerprints unchanged. Direction contact sheet reviewed
on dark/light backgrounds at reduced scale. Browser checks cover the cardinal
mining sequence, reverse, steering, pause and lamp state controls.
Final validation passed all 44 clips / 3,120 body frames and matching effects:
frame/atlas parity, clipping, travel alpha, mining endpoints and source hashes.
Evidence: `review/final-validation.json`. All eight driving headings loaded in
the browser without warnings/errors; held-key movement was not visually verified.

## Next action
Owner requested another tyre-animation pass. Revision 2 now selects 32 revised
travel clips from `tyres-v2/`, preserving the originals. Motion separates small
tread studs from fixed tyre lighting, adds curved rolling projection, tightens
steering cutouts and links preview travel speed to each wheel cycle. Rebuild with
`build_tyres_v2.py` after the original builders; validation is in
`validate_tyres_v2.py` and `tyres-v2/motion-validation.json`.
Revision 2 checks passed 32 clips / 1,920 changed frames: continuous loop seams,
exact reverse playback and connected steering silhouettes in every frame. All
eight steering headings loaded in the browser with no warnings/errors. Original
idle/mining entries and effect paths compare unchanged against the saved manifest.

Continued preview polish: `motion.mjs` and `preview.mjs` retain wheel phase across
headings, ease acceleration/braking, stop before mining, and hold tread phase at
idle. Ground movement uses the same integrated distance as wheel motion; manual
movement pans the ground at viewport limits. `node test_motion.mjs` passed phase,
reverse, braking, stop hold, mining interlock and frame-rate independence checks.
Browser observed braking/reverse and braking/mining transitions. Continuous
held-key driving remains unverified. Exported artwork and gameplay are unchanged.
Mining cancellation now retracts before departure, including a matched extension
when cancelled during deployment. Both cases pass the motion controller checks.

Owner reviews the revised tread motion, diagonal consistency and the
proposed native scale. Any subsequent integration must separately establish
seabed pathing, collision clearance, work targets, rewards and launch/recovery.
Do not treat this art preview as an accepted runtime footprint.

## Completion milestone
Owner requested finishing the whole Mining rover set. Added intake/unload, loaded
travel, blocked-tool recovery, startup/shutdown, charging and disabled states.
The final contract has 112 clips and a complete work-cycle preview. See
`assets/mining-rover-v1-2026-09-26/completion/CLOSEOUT.md` for scope and evidence.
Animation production is complete for review; next action is owner visual review
and a separately scoped live-game integration. Earlier counts above record the
progression of this task, not missing work.

## Art audit milestone
September 26: completed the requested artstyle, consistency, density and animation
review. See `assets/mining-rover-v1-2026-09-26/review/ART_AUDIT.md` and its reproducible
metrics. Coverage/export checks remain passing; visual sign-off remains pending.
Open findings: brighter/glossier diagonals, larger diagonal tyre studs, and a
rolling-to-static tread texture mismatch at work transitions. Native scale remains
plausible, but nominal chassis width is not full alpha bounds or gameplay clearance.
Added audit report, metrics script/JSON and browser evidence; no source artwork or
gameplay changes. Next step is a targeted material/detail and wheel-join polish pass,
then affected-family validation and visual comparison. No owner save access.

## Audit repairs and next drone
Owner authorized repairing the audit findings and moving to the next drone.
Selected diagonal v5 source corrects materials/stud density and retains one front
drill per heading. `build_directions.py` now selects it for all four diagonals.
`build_tyres_v2.py` uses phase-zero-preserving cylindrical projection and exports
60 shared wheel layers per heading. `preview.mjs`, `motion.mjs` and their tests
preserve the stopped wheel phase across all work/power actions. Original sources
remain. Detailed evidence and exact prompts: `review/POLISH_CLOSEOUT.md` and
`review/POLISH_PROMPTS.md` in the rover pack. Full 112-clip export validation,
tyre validation, 480 wheel-layer phases and controller joins pass; browser full
cycle completed without errors. No gameplay integration. Next consumer must use
the shared wheel layer to preserve arbitrary incoming phase.

Started the Salvage south-facing pilot on port 8771; five clips / 420 frames,
native room comparison and owner-save isolation passed. Continue from
`docs/SALVAGE_DRONE_HANDOFF_2026-09-26.md`. Construction/Mining previews remain.
