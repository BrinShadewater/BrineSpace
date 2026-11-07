# iPad Cold Store texture storage — October 19, 2026

Installed Validation2 **brinespace-7bb44e16b7f164d3**, bundle
`com.shadewater.brinespace.nativeoptimization20261017`, physical iPad13,18/A14/4GB/iPadOS27.2.
Checkout `/Users/Shared/BrineSpace-native-validation-20261017`, branch
`codex/ipad-memory-placement-2026-10-17`, HEAD81b2f9a4a36eb0e3162d86ccfb4e9ef735836122 plus accepted dirty work.
Starting installed build e8afae3a95947e78 remains complete in sibling `grid-loading-pass`.
Evidence and signed app: `/Users/Shared/BrineSpace-ipad-optimization-20261019/texture-residency-pass`. No commit/push/public delivery; frozen Mac/Windows builds untouched.

## Change and attribution

Cold Store eagerly uploaded two retired fridge/rack sheets during tablet setup despite
current station artwork not drawing them. About12MiB of source pixels were unused.
Tablet setup now follows existing RoomAssetLibrary.defer_legacy_art policy. An explicit
raw fallback loads only the requested original sheet before accessing its bounds.
Overhead rendering, geometry, desktop and editor-preview eager behavior remain unchanged.
Whole-path constants also replace the old folder-prefix dependency, dropping six unused
rasters from the maintained export; PCK is8,607,190bytes smaller. Source artwork was not edited.

A temporary creation census used weak texture references to identify upload owners.
All142 temporarily instrumented source files were restored byte-exact; no census
helper ships. Its source-pixel totals are not total GPU residency. The selected fix
has direct native and physical-device counter measurements below.

## Verification

New test failed on eager baseline with3expected assertions, then passed. It verifies
all four rotations, exact overhead/raw fallback pixels and original bounds, single-sheet
demand loading, unchanged geometry, desktop/editor behavior and available sources.
Native related legacy-room and overlay tests passed. Scoped independent static review
found no actionable issue. Fourteen actual-PCK fixtures passed: Cold Store, legacy rooms,
crew cache writes/workers/session/source keys, title, cards/regions, raw texture regions,
shared floors, HullUI175checks, RunSave and tablet controls. Asset/source audits,
Release build, strict signing and export/app PCK equality passed. Test registration is
native/tablet-memory. Native runs isolated profiles and guarded the real Mac profile.

Frozen native owner-station pixels were identical. Godot's texture counter changed
815.677→799.682MiB (about16MiB).

Source SHA-256 `7bb44e16b7f164d3a6f0d752a13ba7daf4cfa567dbfcb248c1d3fe8b9e87ae18`.
PCK SHA-256 `dddcc7ed3286416fbf620860f639c4b2ca1768e4563c1ae8afb6d84bdd2af42e`.
Executable SHA-256 `471f8d099f2be21ace6e6487f67ac9f945368a2f7e3dbba437851fe09f520a18`.
Export configuration restored exactly; CR-at-EOL-aware whitespace check passed.

## Physical observations

Normal paused cycle64/seven-room checkpoint, water0, no free-building/stress marker.
One ordered fresh-process load each, with existing crew disk cache retained:

| Measurement | Old e8af | New 7bb4 |
|---|---:|---:|
| Station texture counter peak | 827.962MiB | 811.967MiB |
| Station setup | 4015ms | 4002ms |
| Process sampled peak footprint | 1,870,941,512B | 1,847,479,624B |

New repeated setup3212ms. Physical texture counter decreased by the same15.995MiB
as native, while first setup stayed about4seconds. Whole-process samples cover different
durations and uncontrolled OS/cache conditions; no general23MB RAM-saving claim or
consistent latency gain follows from this single pair. First title-return frame236.864ms
versus old266.768ms; manual report still contained3.636s setup and2.636s after-render
intervals. These intervals are not GPU-time attribution. Loading/title pauses remain open;
automatic capture skips paused stalls, so zero automatic stall reports is not clearance.

Actual card selection/return dismissed placement controls; pinch saved a changed zoom;
rotation button saved rotation1; Codex touch scroll and Home/activate returned paused.
Gameplay fields and exact timer matched through touch checks. Two-finger pan/tap were
not automated. After original restoration, controlled Cancel→Save/title/Continue/Save
matched complete state/workspace and exact timer; only normal save metadata changed.
Final originals were restored again: all five files SHA-exact even after normal launch.
Left cycle64/seven rooms paused4x, menu closed; final launch/hash/screenshot records are
in final-owner-restoration.json and final-original-station.png. No spontaneous crash
or game error observed. A baseline CoreDevice10004 launch/PID error was retained;
process inspection found the intended app live, and one retry activated it successfully.
Test helper now retries that specific launch error once while preserving failed metadata.
Intentional stops generated recovery notices; no unrelated app was stopped.

Helper8545 remains running with its two-hour limit. Not release-cleared. Continue
first-use grid/render attribution and sustained whole-process memory measurements.
