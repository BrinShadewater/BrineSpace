# Numeric shadow-cache lookup: small installed CPU cleanup

Updated: October 11, 2026 · Project: BrineSpace · Task: PC/Mac performance readiness

## Objective and accepted scope

Reduce recurring floor/shadow preparation work without changing cached colours,
geometry, ordering or GPU resources. The previous material-retention trial was
progress: it ruled out a suspected overhead and identified larger grid callbacks.
This milestone installs a small equivalent lookup change, not a 60 FPS remedy.
The full performance/release objective remains active.

## Implementation and evidence

`rooms/whole-room/room_lighting.gd` replaces formatted HTML-colour/radius cache keys
with a `Vector2i` containing clamped RGBA8 and rounded radius. The first StyleBox
stored in each bucket still owns the original unquantized colour. Contact-band
radii are in the supported 0–10 range. Cache entries/resources and their lifetime
remain the same; no pixel, timing, art, scale, layering or quality change is intended.

Verified the native conversion against
[Godot ed1daf0bf colour implementation](https://raw.githubusercontent.com/godotengine/godot/ed1daf0bf/core/math/color.cpp):
HTML rounds and clamps channels; RGBA32 rounds them, so explicit clamping preserves
the same buckets. This is the commit reported by the local 4.7.2 runtime.

An isolated engine probe checks 10,005 inputs, including small alpha changes,
radius boundaries and out-of-range colour aliases. All cached StyleBox colours,
corner radii/detail, antialiasing and 112-entry counts match. Three 100,050-lookup
passes per lane: text 96,761/92,599/93,788 us; numeric 47,364/43,892/44,040 us.
About twice as fast locally; this is not an FPS claim.

## Matched game results

Six native debug=false Windows runs, three alternating 40-room pairs, 6,480 frames.
Normal source in both lanes except the helper. Current construction/Solar fixes
preserved; no indexed drone provider. RTX 4070 Ti, 1080p, muted secondary window,
isolated profile, physical input disabled. No captures inside measured phases.

| Metric | Text keys | Numeric keys |
| --- | --- | --- |
| Mean ms | 26.806 | 26.775 |
| p95 ms | 44.109 | 44.540 |
| p99 ms | 58.758 | 57.523 |
| Frames >50 ms | 75 | 79 |
| Frames >100 ms | 0 | 0 |
| Peak texture MiB | 3028.007 | 3028.007 |
| Shadow setup profile, mean us | 373.154 | 344.946 |

All 36 final state/camera comparisons exact. Mean changes only 0.116%, with mixed
pair-level results; no meaningful average FPS improvement. The shadow section is
about 7.6% cheaper in this sample, while broader frame-time gates remain failed.
The lookup change is accepted as a small allocation/CPU cleanup on the strength
of the equivalent-object probe, local timings, matched game evidence and native
regression coverage. Do not advertise it as a broad smoothness gain.

## Visual checks and open discrepancy

Initial scoped station-art capture: 23/24 pairs exact. One 2x zoom capture differed
by 8,879 pixels in a background wreck at [1240,149,1327,253]; saved state, camera,
clock and room-light levels were identical. A similar region differed in earlier
provider trials. Do not close that discrepancy merely because it later passes.

A focused rerun of that capture matches all pixels and captured layer transforms,
culling regions and retained keys. A complete-history traced rerun then matches
24/24 image pairs and all rendering-context fields. These use fixed light time,
synchronous camera placement, completed pending drone decoding, drained background
redraws, refreshed portraits and hidden hand/discovery overlays. They establish
that scope, not native asynchronous pacing, the full UI, every room or Mac support.
The intermittent background-wreck result remains awaiting reproducible diagnosis;
it was not attributed to or fixed by this equivalent-key change.

The first diagnostic attempt had a fixture indentation parse error. Only its known
isolated process was stopped, configuration/owner guards restored, and the script
corrected. The loader now exits when a script cannot instantiate. The successful
reruns are separate from that retained failed-fixture log.

## Installed verification and changed files

Installed implementation equals the measured candidate except for an explanatory
comment. Extended existing `tests/test_room_shadow_packet_cache.gd` with 17 alias,
first-colour, identity and rounding-boundary checks; preserve/restore its cache so
other tests retain their own state. Native installed test: 28 checks, zero failures,
including fade reuse, moved footprints, entry/byte limits and overlapping-owner
release. Existing script/UID pairs remain present; no UID changes requested.

Production files changed by this milestone: the lighting helper, the existing
cache test, this handoff and `docs/CURRENT_STATUS.md`. Preserve earlier unrelated
worktree changes. No release export, commit or upload.

Evidence under `D:/bs-release-crew-cache-20261009/benchmark-input-isolation/`:
`numeric-shadow-keys`, `numeric-shadow-keys-pixels`, `numeric-shadow-keys-wreck-trace`,
`numeric-shadow-keys-full-trace`. Exact private runners/comparators are in
`output/renderdoc-tools-2026-10-08/` with `numeric-shadow-keys` in their names.
All guards show 2,938 owner files unchanged. Processes exited; runtime configuration
restored. Evidence totals 224.36 MiB; C 124.62 / D 72.24 GiB free. Existing runtime
reused and 20 GiB free-space floor enforced.

Room-pipeline sync audit: 35 files checked, five differing references. Used maintained
project references for applicable production guidance; no skill overwrite. No new
art or furnishing pass was performed.

## Next action

Larger current trace targets: live-room drawing ~3.9 ms, content drawing ~2.8 ms and
door/light validation ~1.1 ms; scopes can overlap. Instrument the repeated room
setup and door/port work before editing, then test an invalidation-aware reuse change
against normal source and both real maps. Keep floor/light-pool/seam ordering.

Continue the intermittent background-wreck diagnosis when reproduced. Prior normal
versus indexed gait precision, indexed provider loader/fallback/lifetime, large-map
frame gates, actual Windows target hardware, endurance, packaged bug closure and Mac
release certification remain open.
