# Bill and Airlock release handoff

Updated: September 12, 2026 · Project: BrineSpace

## Objective and acceptance
Review Bill's complete furnished-airlock journey, fix visible issues and deliver a verified playable build.

## Accepted decisions and constraints
Preserve detailed existing art, original animation timing and other ongoing work. Freeze selected runtime inputs for export. Existing builds and player data remain untouched; no publication requested.

## Current state
Deliverable: `builds/BrineSpace-bill-airlock-20260912/BrineSpace.exe` and adjacent PCK, README, NOTICE, build_info and checksums.
Build ID: brinespace-4aae058895cf7c27
Source fingerprint: 4aae058895cf7c276c519f89c901e50170591ed73a3e0f581a33a5dbd86fa8ff
Base commit: b2648fea378f3d8a5237e554ae2179e43ffb556c plus recorded working changes.

Fixed the chamber floor drawing over Bill: floor/water now render before sorted actors, with chamber-local water treatment. New native visibility regression and paired UID cover four rotations in dry/flooded states; registered in tests/index.json. The dependency collector now recognizes enabled `*res://` autoload entries, with regression coverage, so a minimal snapshot includes the bug reporter.

Snapshot: `output/bill-airlock-release-20260912/source`. Includes selected Bill/airlock art and current room/system bindings (including hull crack/patch and fire systems); later live checkout changes do not alter this build. No new art generation. Pipeline lesson updated and installed copy synchronized.

## Verification
- Native actual-controller Bill journey: 769 simulation samples, all 12 expedition phases, real locker equip and removal, safe return; zero failures. Every other sample recorded at 5 fps. Video and scrub review: `output/bill-airlock-release-20260912/journey-visible/`.
- Visually inspected locker contact, wet chamber occupancy, swimming/return and final helmet return at gameplay scale. Flooded silhouettes retain the existing water tint.
- Native visibility regression: eight occupied/empty render comparisons, zero failures.
- Headless airlock: three architects/four rotations/1,039 travel samples; station expedition systems pass. Evidence: `output/test-runs/20260912-034140-headless`.
- Four release dependency/assertion tests pass on snapshot.
- Maintained exporter passes. Empty-project audit checks 9,910 packed assets, zero missing/changed.
- Actual release EXE: New Game, simulation, F8 report and selected dense Bill/five furniture groups pass, zero failures, debug=false. Native release capture inspected.
- EXE/PCK identity in deliverable SHA256SUMS.txt. QA override disabled in separate QA directory; never present in deliverable.

Earlier native fixture attempts were rejected: first-layout registration canceled requests and old captures missed the room. Final focused fixture settles rendered layout before dispatch. First minimal export exposed missing autoload dependency; final build incorporates the collector fix. These failed attempts are not counted as acceptance.

## Next action
Owner playtest of this build. Full expedition balancing remains outside this smoke test. No commit, upload or publication performed.
