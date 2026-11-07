# Project handoff

Updated: September 27, 2026 · Task: three-crew walk consistency and integration

## Objective and acceptance
Owner authorized final four-direction consistency, idle/walk review, installation and in-game checks after accepting Bill rear v5. Final combined palette/cadence review remains for owner judgment.

## Accepted decisions and constraints
Preserve accepted poses, proportions and department colours. Dark graphite, silver hardware; Bill burgundy, Veld blue, Branforth muted yellow. Save free Genjutsu. No paid generation this pass; last confirmed balance56.

## Current state
`character/crew-runtime-walk-v2/` contains reproducible build, three standalone overrides,24 states/673 frames, source hashes, colour/bounds checks and review media. Latest Bill southv3/northv5 replace the older cast-stage rows; other rows derive from the darker accepted pass. Fixed per-clip neutral-body correction removes residual purple/warm fabric bias. Head pixels and alpha unchanged; pixel mean cannot brighten beyond integer rounding. Material masks are colour approximations, not perfect semantic segmentation.

Playback is1500ms per complete gait cycle. Multi-cycle clips use proportional duration and travel (69/384 cells per cycle) so extra cycles do not accelerate feet. Bill/Branforth use static matching-reference idle holds; Veld retains existing idle motion. No invented poses or frame interpolation. Fixed registration184x184, pivot92,172, standing148.

`scripts/grid_canvas.gd` loads whole explicit paths for all three overrides. Bill's helmet idle/walk branch now uses its independent equipment player, avoiding indexing the older helmet rows with new bare-frame counts. `character/ACTIVE_ASSETS.json` records overrides. Existing action/helmet artwork and Marsh remain unchanged; action-to-idle visual joins are outside this pass and may still differ from new masters.

## Verification
All three manifest validators: zero errors/warnings. No clipped frames; source hashes unchanged. Godot4.7.2: test_crew_walk_v2 passes1586 checks; test_veld_walk_integration passes415. Native production-loader review captures120 frames at source/station scales. Actual station-renderer fixture captures20 views and samples96 Bill helmet phases, zero failures. Representative final native and station captures visually reviewed. Tests use scratch APPDATA; real owner-profile hashes unchanged. New tests have paired .uid files and runtime test registered in tests/index.json.

Evidence: checks.json, test-results.json, validation JSONs, native.gif, station.png; detailed native captures under output/crew-walk-v2-native and output/crew-walk-v2-station. These are deterministic rendering fixtures, not a full autonomous expedition or exported-build test. No executable export, commit or push.

## Next action
Owner reviews `/character/crew-runtime-walk-v2/` for final combined palette/cadence and transitions. If accepted, prioritize frequently used work-action consistency next; inspect existing role actions before spending further credits. Preserve other concurrent grid/status edits.
