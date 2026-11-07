# Project handoff

Updated: October 5, 2026 · BrineSpace · Corridor and door memory

## Objective and acceptance

Trace remaining title-resident artwork, remove proven unused corridor uploads and
release unused transit images after the last gameplay/Studio owner exits. Keep
selected pixels, filtering, door styles, progress and owner layouts unchanged.

## Accepted decisions and constraints

Bounded census finds 12.01 MiB decoded corridor walls, 4.50 MiB legacy deck,
1.08 MiB lighting and 35.99 MiB department-door images retained at title. Wall-kit,
wall-dressing and measured airlock/prop caches are empty in this checkpoint;
no speculative cleanup there. Tiled corridors never draw the legacy deck.
Clear only derived transit images after the last registered owner exits; retain
door objects, catalog data and settings. No active-state eviction or art changes.

## Current state

`rooms/underwater/corridor_surfaces.gd` skips the unused legacy deck upload in
tile mode. `scripts/session_art_cache.gd` now clears corridor wall/detail/tunnel/
deck images, each retained department-door object's texture dictionary and lamp
images on final-owner exit. Reference switches: `--reference-corridor-deck` and
`--reference-transit-material-lifetime`. Earlier cleanup stays enabled in both arms.
New native `tests/test_transit_material_cache.gd`, paired UID and test-index entry.
Evidence/runners/logs: `output/wall-corridor-lifetime-2026-10-05/`.

## Verification

Godot 4.7.2 native Compatibility / RTX 4070 Ti; isolated guarded user directory.
618 focused checks pass, including 144 exact pixel comparisons: straight/corner/
tee corridors, four rotations, two scales, half-pixel origin, tile/legacy floors,
nearest/linear filtering; doors at four travel positions, detail/glazing/lamp art,
overlapping owners, weak image release and exact reloads. Door identity and
progress remain intact. All 2,936 owner non-log files unchanged.

The census traverses 123 values without truncation and deduplicates ImageTexture
instances. It reads named static roots and explicit door-object image dictionaries;
it is not a complete GPU inventory. Native drawing checks cover affected paths,
not full-room motion acceptance.

Three alternating native matched pairs use the same checkpoint at 1600×900,
two Title Continue → gameplay → menu save → title cycles each, and first-entry
Studio open/close. Earlier cleanup stays enabled in both arms. Raw engine texture
accounting in MiB:

| State | Reference | Candidate |
|---|---:|---:|
| Initial title | 47.00 | 47.00 |
| First gameplay after Studio | 3,404.22 | 3,398.22 |
| Settled title after exit | 262.05 | 190.65 |
| Following gameplay | 3,431.95 | 3,417.95 |

All three pairs agree: 6.00 MiB first-entry, 71.40 MiB settled-title and 14.00 MiB
repeat-entry reductions. These engine counters are not certified driver residency.
First-profile loading-stage median 16.146→16.879 s; repeated Continue
5.446→4.918 s. Samples overlap and first-entry direction worsens; no loading-speed
improvement claimed. OS caches uncontrolled; first-profile is not certified cold
and stage sums do not certify packaged loading. All 2,936 owner files unchanged.
Common short-fixture shutdown ObjectDB warning remains unassigned.

Final ten-transition native run passes with zero failures, engine errors or
shutdown warnings. Settled title 190.65→191.01 MiB (0.188% growth); comparable
later gameplay 3,417.95→3,418.27 MiB (0.009%). Each old gameplay scene/player
releases; obsolete ownership/lookups empty at title. All 2,936 owner files
unchanged. The earlier intermittent RefCounted shutdown warning is not reproduced
here; its cause is still unassigned. Runtime/test source hashes unchanged across
measurement. Fixtures manually step 120 updates per entry; no FPS, driver-residency,
two-hour soak, normal-clock rendering or packaged/platform certification claimed.

## Next action

Retain the changes within this measured scope. Keep active memory, loading,
stutter, two-hour soak and packaged
Windows/Mac/target-hardware gates open. Next inspect unused historical corridor
sources: grid/Studio call `load_sources()` but `draw_hull()` never reads its passed
textures and detail methods are empty. Measure before removing caller uploads;
do not change source during this comparison. Frozen release inputs unchanged.
