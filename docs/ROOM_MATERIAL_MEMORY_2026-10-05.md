# Project handoff

Updated: October 5, 2026 · BrineSpace · Room material memory

## Objective and acceptance

Remove unused floor uploads and release room material images after their last
gameplay/Studio owner exits. Preserve selected pixels, filtering, layouts and
reload behavior. Compare identical native transition workloads.

## Accepted decisions and constraints

Tiled profile floors previously uploaded a legacy grain before returning through
the tile renderer; that grain contributes no pixels. Skip that unused upload,
while preserving the legacy renderer. Extend existing last-owner session cleanup
to painted shells, windows, risers, department walls, north-wall BRINE art and
floor grains. Keep catalog definitions, explicit settings and owner marks intact.
No active-state eviction, downscaling, art changes or save-schema changes.

## Current state

Changed `rooms/whole-room/room_floor.gd` and `scripts/session_art_cache.gd`.
Reference switches: `--reference-profile-grain` and
`--reference-room-material-lifetime`; prior session cleanup stays enabled in both
comparison arms. New native tests `test_profile_floor_loading.gd` and
`test_session_material_cache.gd`, paired UIDs, registered in `tests/index.json`.
Evidence, runners, source hashes and full logs:
`output/title-cache-inventory-2026-10-05/`.

## Verification

Godot 4.7.2 native Compatibility / RTX 4070 Ti at 1600×900. All runs guard the
resolved scratch user directory; layouts and a scratch checkpoint are copied in.
387 floor checks pass, including 96 exact pixel comparisons across three actual
full-wall room profiles, four rotations, tile/legacy rendering, two scales,
half-pixel origin and layout edits. 18 material checks pass with nearest/linear
filtering, overlapping owners, weak image release and exact reloaded pixels.
This establishes the changed drawing paths, not full moving-room acceptance.

Three alternating matched pairs each use two Title Continue → gameplay → menu
save → title cycles, including first-entry Studio open/close. Engine texture
accounting in MiB:

| State | Reference | Candidate |
|---|---:|---:|
| Initial title | 47.00 | 47.00 |
| First gameplay after Studio | 3,446.20 | 3,404.22 |
| Settled title after exit | 383.46 | 262.05 |
| Following gameplay | 3,473.92 | 3,431.95 |

All three pairs agree. Skipping unused uploads saves 41.98 MiB in active gameplay;
material cleanup reduces settled title accounting by 121.41 MiB. A bounded census
before changes attributes about 91.1 MiB of decoded image storage to these roots;
it is not a complete inventory. Raw engine figures are not driver residency.

First-profile loading-stage median: reference 16.339 s, candidate 16.042 s;
repeated Continue: 4.843→4.868 s. Samples overlap; no loading-speed improvement
claimed. OS caches uncontrolled, first-profile is not certified cold, and stage
sums do not certify packaged loading. Matched runs preserve all 2,936 owner
non-log files. Short fixtures retain the previously seen common ObjectDB shutdown
warning; its cause remains unassigned.

Final enabled-default ten-cycle run: zero failures or engine errors; obsolete
owners and old scene/crew-player objects release on each exit. Settled title
262.05→262.41 MiB (~0.137% growth); comparable later gameplay
3,431.95→3,432.26 MiB (~0.009%). All 2,936 owner files unchanged. One shutdown
warning reproduces; verbose output identifies only a zero-reference-count
`RefCounted`, without a script or allocation site. Cause unassigned, so clean
shutdown remains open. Native fixtures use 120 manually stepped updates per entry,
not a normal-clock FPS test, a two-hour soak or packaged acceptance.

## Next action

Retain both changes within this measured scope. Inventory remaining title-resident
image owners with bounded explicit roots,
starting with wall-dressing/riser kits and corridor art. Keep active full-roster
memory, first-profile loading, long stalls, the two-hour large-station soak and
packaged Windows/Mac/minimum-hardware gates open. Frozen release inputs unchanged.
