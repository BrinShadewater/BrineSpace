# Performance pass, phase 1 — September 11, 2026

Track 2 of the audited plan: parity-preserving frame-time work on the dense-view
GDScript draw path. Source checkout only; no executable rebuild, no commit.
Every change ships an opt-out flag so old/new can be A/B'd on one build.

## Measured result (tests/profile_large_station.gd, same machine, same run pair)

| scenario | before (flags) | after | change |
|---|---|---|---|
| 50-room fit | 46.84 ms | 37.11 ms | **-20.8%** |
| 50-room close | 9.87 ms | 9.14 ms | -7.4% |
| 100-room fit | 74.81 ms | 62.17 ms | **-16.9%** |
| 100-room close | 20.04 ms | 17.52 ms | -12.6% |
| menu-open hitch | 40.0 ms | 34.2 ms | -15% |
| save hitch | 22.9 ms | 13.1 ms | -43% |

tests/profile_flood_station.gd (49 rooms): dry 20.69→19.66 ms, flooded
29.68→28.73 ms. Evidence: output/game-pass/track2-baseline/ and
track2-optimized/. Dense fit views still exceed the 60 fps budget; the
remaining CPU sits in live_rooms (~10 ms) and content prepare/draw (~7.6 ms) —
phase 2 items (e)/(f) below.

## Changes (all parity-gated)

1. **Retained environment passes** (`grid_canvas.gd`; opt-out
   `--redraw-environment`): stars, haze rects and foundations move onto retained
   child passes (`Env.STATIC_BELOW` / `STATIC_FOUNDATIONS`) with cheap
   invalidation keys (visible cell range; visible rooms + exposure + exterior
   wreck subjects + hardware.walls). Animated haze lines, foundation shimmer,
   rocks/wrecks/cryo/harvest/drones and the admin grid stay live
   (`LIVE_LINES` / `LIVE_ABOVE`), in the original compositing order. The
   environment stage fell 13.6→0.6 ms at 100-fit. Retained environment engages
   only alongside retained surfaces: direct-painted floors land on the parent
   canvas, which composites below child passes (the surface-parity comparator
   caught exactly that during development).
2. **Layout store memoization** (`room_layout_store.gd`; opt-out
   `--uncached-layout-store`): `shared_positions()` caches the merged
   authored+user layout per asset/quarter, invalidated by the store revision and
   by wholesale `data` reassignment (identity check — capture tools and fixtures
   assign `data` directly). `apply()`'s early-out becomes
   hash(asset, quarter, revision) plus a per-prop `_layout_stamp`, so a rebuild
   that replaced the prop dictionaries still reapplies. `positions()` keeps its
   owned-copy contract for everyone else. One nested in-place edit in
   `tools/review_brine_corner.gd` now bumps the revision.
3. **Per-frame memos in the door/surface state keys** (`grid_canvas.gd`):
   `_drone_door_frame` memoised per rendered frame; crew feet gathered once per
   frame for `_nearest_crew_foot`; `_surface_state` snapshots only visible rooms
   (plus the placed-room count — off-screen mutations repaint nothing until the
   room scrolls in, which changes the key anyway; opt-out
   `--surface-key-all-rooms`).
4. **Idempotent hardware panel refresh** (`hardware_panel.gd`): the per-frame
   poll now skips theme-override and text writes when control state is unchanged.
5. **Flooded quick wins** (`flood_visuals.gd`): door-current drawing skipped for
   rooms whose pair context and wash history are dry (matching the function's own
   early-out+erase semantics), and the per-prop `clock` shader uniform uploads
   only when it changed (it never does while paused).

## Verification

- **New parity harness**: `tests/test_environment_cache_parity.gd` (native) +
  `tests/check_environment_cache_parity.py` — 7 mutation capture pairs
  (place/remove room, walls off/on, pan, zoom, baseline) byte-identical;
  invalidation counters asserted; retained passes stable across 12 animated
  frames. The fixture freezes the hardware panel (its WALLS knob eases between
  captures otherwise).
- Existing native gates all PASS: content-cache parity (first verified run of
  this gate), surface-cache parity, render-cache parity, retained-lights parity,
  brine-batch parity, hitch parity, flood rendering.
- Headless regressions PASS: layout free placement, live layout refresh,
  preferred room layouts (176 orientations), crew life rooms (72 cases),
  room catalog cards, side wall variants, crew room activity.
- Fixture repairs found along the way: five parity fixtures thawed the core
  architect for 7.0 s against the 10.0 s `Architects.DURATION`, so their crew
  never woke (fatal for retained-lights, which asserts movement) — all bumped to
  10.0. The exit-code-2 native-only tests got explicit native lanes in
  tests/index.json.

## Known limit (pre-existing, not from this pass)

`tests/check_surface_cache_parity.py` and `check_render_cache_parity.py` report
sub-perceptual differences at fit-zoom captures (q0–q3/pan/zoom: ~44k pixels at
channel delta ≤3, ~46 pixels up to ~225) on this machine (RTX 4070 Ti, GL
compatibility). Reproduced identically with every Track-2 flag opted out, i.e.
on the pre-pass code path; mutation-state captures are byte-identical. Likely
antialiased-polyline rasterization variance between captures at dense zoom.
Recorded here so a future red run is not misattributed.

## Phase 2 (same session): prop-queue caching + cheap DrawSlot keys

6. **Sorted prop-queue caching** (`nursery_whole_view.gd`; opt-out
   `--uncached-prop-queue`): on the retained-content path, the per-room queue of
   prop entries is no longer rebuilt and re-sorted every frame. The sorted
   arrangement (equal-depth order frozen as the captured sort output) is cached
   and validated per frame by prop-dictionary identity plus `sort_y`; the few
   live actor/crew entries are inserted by depth. Split passes
   (base/effects/prop_pass) are pre-expanded into the cache, so the content
   canvas receives the same Dictionary objects every frame.
7. **Cheap DrawSlot keys** (`room_content_canvas.gd`; opt-out
   `--uncached-slot-keys`): prop-kind slots compare by entry identity plus a
   flat static-value array (view id, layout `apply_serial`, quarter/operating/
   drone/hatch/recovery/pod/cycle fields) instead of deep-walking the prop
   dictionary (registration outlines included) and deep-copying it twice.
   `room_layout_store.apply_serial` increments whenever apply() actually
   mutates props, signalling every layout-driven change. Actor/crew slots keep
   the deep path (they change every frame regardless). Expansion logic is now
   one shared `expanded_prop_entries()` helper. (Caching expansion entries
   inside the prop dictionaries was rejected: it would create reference cycles
   that `duplicate(true)` in the geometry path recurses on.)

Isolated phase-2 measurement (flags off vs on, same build): 100-fit
63.07→61.40 ms; `live_rooms` 10.49→8.96 ms; `content_prepare` 3.47→2.34 ms.
Combined with phase 1 against the session baseline: **100-fit 74.81→61.40 ms
(−17.9%)**. Evidence: output/game-pass/phase2-off/ and phase2-on/.

Phase-2 verification: content-cache parity PASS natively and all **33 capture
pairs pixel-identical** (checked with a comparator — the GD test alone does not
compare pixels), plus surface/brine-batch/hitch/retained-lights/environment
parity PASS, and the headless battery (free placement, live refresh, 176
preferred orientations, 47 cards, checkpoint isolation, companion water) PASS.

Known tie-order caveat: a live actor/crew entry whose depth exactly equals a
prop's `sort_y` float now sorts after the equal-depth props deterministically,
where the previous unstable sort made no ordering promise. Exact float
equality with a continuously-moving crew y has measure zero; the parity
captures (including motion and busy-crew states) are pixel-identical.

## Remaining headroom

At 100-fit (61.4 ms) the budget miss now sits in `render_into` internals
(`live_rooms` ~9 ms), `content_draw` (~4.3 ms of actual painting),
`detail_room_setup` (~4.6 ms of per-frame configure/geometry adaptation), and
GPU/driver time. Further wins likely need owner-decision items (mipmapped
minification, texture atlasing) or per-room transform caching — outside this
pass's parity-preserving scope.

Owner-visible behavior is unchanged by design; owner acceptance of normal-play
feel remains pending as with any rendering pass.
