## Veld master helmet registration v2 - September 30, 2026

Corrected 2-3px helmet/collar drift using selected master gasket bottoms
104/107/108/107 (N/E/S/W), interpolated through turns. Native components retain
scale/grade; body pixels outside x96:169, y65:109 unchanged. Rear carry uses the
physical crown, 7px above bare crown, replacing its warm-colour landmark.

Changed registration.py, fit_north_east.py, fit_family.py, fit_carry_north.py,
quarter/half frames, carry-north-helmet-manifest.json, grid_canvas.gd literal
overrides and ACTIVE_ASSETS.json. Previous revision: revisions/registration-v1.
Review: character/veld-unified-turn-helmet-v1/index.html and cargo handoff audit.

148 family fit checks, 333 packaging checks, 18 rear carry checks and 688 actual
installed-loader native checks pass. Scratch APPDATA; real profile unchanged
for v2. Earlier v1 architect-test deltas remain recorded. All quarter angles and
rear carry visually reviewed; owner visual acceptance remains open.

Remaining: inherited crew-life/water identity and motion. Water inventory shows
old gold/orange helmet construction. Helmet weld is controller-invalid; dry
idle/walk turns are not required. Swim/swim-carry turns are required. Accepted
planted cargo endpoints remain; completion resets to carry frame zero.
Full-set goal remains active.

# Project handoff - Veld master helmet repair

Updated: 2026-09-30. Project: BrineSpace. Goal: full Veld set and master consistency.

## Objective and acceptance
Restore one accepted helmet design through cargo turns. Previous half-turn
changed port, visor, face and collar at frame7. Shared runtime helmets define
scale/grade; original high-resolution helmet art defines construction.
Owner visual acceptance pending; broad full-set goal remains active.

## Accepted decisions and constraints
Matte graphite, silver trim, clear glass, white lamp; bun inside shell. Preserve
accepted bodies, equipment handedness, timing and pivot. Exact accepted cardinal
components. Independently authored opposite views; no mirrored body poses.
No commit/push/export. Original sources retained for rollback/comparison.

## Current state
Installed eight helmet quarter directions and four paired half-turns via final
literal grid_canvas.gd overrides and ACTIVE_ASSETS.json. Bare half-turns use
veld-carry-half-turns-consistent-v1. New quarter/half helmet manifests, fitted
frames, provenance, exact prompts and builders are here. Interactive index.html
synchronizes before/after and frame scrubbing. Browser frame7 capture retained.
Used north-east-source-v5, east-south-source-v1, north-west-source-v2 and
south-west-source-v1. Earlier large atlases/v4 rejected for angle/glow/hardware
drift; north-west-v1 rejected for right-facing intermediates. High-density master
sources resolved construction drift. Detached neighboring cell pixels removed
in extraction. Grade raw intermediates once; do not regrade fitted outputs.

## Verification
148 exact-body/clipping/join checks and333 contract/pixel/cardinal/GIF checks pass.
660 candidate native checks;659 installed normal-loader checks with candidate
loads removed. Includes all12 equipment turn states, exact pixels/metadata and
turn-to-carry handoffs. Scratch APPDATA. Candidate profile unchanged; installed
interval five architect-test files changed, attribution unresolved, untouched.
Reviewed all24 head angles, native image and synchronized frame7 beside masters.
Tests do not establish owner visual acceptance; angular pacing remains reviewable.

Static library inventory:173 bare/167 helmet states,2932 referenced frames, no
missing/non-RGBA files. Catalog/literal override model, not full runtime or motion
certification. Pre-repair inventory frozen in consistency-audit-v2. Many inherited
catalog states still need contemporary master and complete-motion review.
Pipeline/bible/maintained and installed skill now record source-density,
directional-reference, extraction and cumulative GIF timing lessons.

## Next action
Check idle/carry/turn handoffs and continue inherited ordinary turns, crew-life
and water states against masters at station scale. Trace controller-required
coverage separately from catalog presence; bare-only weld may be role-specific.
Do not complete the full-set goal on these12 repaired equipment turn states.

Browser registration-v2 reviewed at north-south frame7 (385ms); masters and synchronized before/after visibly loaded. Capture: browser-family-registration-v2.png.

Master recheck September30: owner-visible smooth-shell-v2 URL resolves to the historical half-turn preview. Confirmed its frame7 port/visor/collar construction differs from the directional masters; current grid_canvas final overrides select the unified quarter/half manifests. Re-ran333 packaging/master/pixel checks:0failures. Opened synchronized north-south frame7 comparison beside accepted masters; fresh capture browser-master-recheck-v3.png. No asset/runtime changes made in this recheck; owner motion review remains open.

Master recheck October 1: historical smooth-shell-v2 preview retains the known frame7 shell/port/visor/collar switch and links to the installed replacement. Final grid_canvas overrides select unified quarter/half manifests. Fresh333 packaging/master/pixel/GIF checks:0failures; no source/frame/runtime edits. Browser north-south frame7/385ms compared beside directional masters; full-page capture browser-master-recheck-oct1.png. Owner motion acceptance remains open. Existing native evidence retains its dated scope; no new Godot run for this read-only recheck.
Preview correction October 1: owner reported mid-turn helmet change at historical smooth-shell-v2 URL. Visually rechecked master board and synchronized north-south frame7 comparison; old shell/port/visor/collar switch confirmed. Existing installed replacement passes333 contract/pixel/master/GIF checks,0 failures. Updated half-turn index.html to display installed replacement GIFs (16 links verified), retaining historical-preview.html and all previous frames. No artwork/runtime edits or new native test. Master comparison opening queued in Codex; owner motion review remains pending. This narrow preview repair does not complete the full-set goal.

Current master audit: all12 north-south poses compared in north-south-master-audit-current.png. Historical frame7 construction switch remains visible; current master-derived shell retains directional hardware. Re-ran333 package/master checks,0failures. Existing browser tab11 verified paused at frame7/385ms beside masters. No source artwork or runtime changed; owner motion acceptance remains pending.
