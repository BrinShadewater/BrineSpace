# Room content retention — September 6, 2026

Station furniture now retains Godot drawing commands between changes. Machinery,
monitor playback, water, crew and drone animation remain live. No rasterized room
textures, reduced animation rates or new art are involved.

## Rendering changes

- `room_content_canvas.gd` owns a small sequence of drawing nodes for each visible
  room. Prop bodies, overlays and crew retain the original depth-sorted order.
- Static furniture redraws when its registered geometry, renderer, rotation,
  operating state, relevant cryo/drone/airlock state, origin or scale changes.
  Animation clocks and crew movement do not invalidate unrelated static props.
- Six common renderers explicitly separate body drawing from animation: Life
  Support, Hydroponics, Med Bay, Research Lab, Reactor and Crew Hab. Machine
  housings and supported objects are retained; their effects draw over them.
- Other room types use their existing animated-prop classification. Unknown
  classifications stay live. BRINE workstation dressing remains live because it
  includes computer playback. Specialty animated machines remain on their full
  live path until explicitly split.
- Shared room-view state is saved/restored around node drawing. Room-specific
  actor, door and cryo state cannot leak into another instance of the same view.
- The content pass skips constructing shell queues that would be discarded.
- Conservative prop bounds, padded by 64 room units, skip off-screen draw callbacks
  and their animation preparation. Simulation continues normally. `--draw-all-props`
  disables this drawing cull for comparison.
- Viewport changes request redraw even while paused, including deferred camera
  centering after construction. Newly visible props therefore return immediately.
- Removed rooms free their content nodes. Remaining nodes are bounded by each
  room's largest render queue. Existing resource loading and save formats are unchanged.

The grid retains its floor/wall layers. Rear doors precede room content; front
doors, lighting, global actors, effects and previews follow it in a separate
foreground pass. Exact draw transforms are preserved rather than moving the
transform into scene nodes, avoiding subpixel rasterization differences.

## Measurements

Sequential native `tests/profile_station.gd` runs, 1600×900, VSync off, warmed
25-room station. Both modes include the preceding floor/wall and mesh caches.
The reference uses `--redraw-room-contents`; retained content is the default.

| Scenario | Reference | Retained | Frame-time reduction |
|---|---:|---:|---:|
| Expanded Fit | 30.96 ms | 26.53 ms | 14.3% |
| Expanded close | 20.94 ms | 17.03 ms | 18.6% |

These local samples correspond to roughly 38 FPS at Fit and 59 FPS close; they do
not establish sustained 60 FPS. The gain is additional to earlier passes, not a
comparison against their older checkout or hardware state. Rendering still submits
thousands of drawing calls, and animated BRINE content remains relatively costly.
The profiler now reports per-room-type content preparation/drawing times as well.

Evidence: `output/content-profile-{direct,retained}.*` and
`output/content-performance-comparison.json`. Both profiles pass culling parity.

## Verification

`tests/test_content_cache_parity.gd` plus
`tests/check_content_cache_parity.py` compare all four RGBA channels:

- Four rotations, Fit/close views, live rotation, power on/off and partial fades.
- Raised walls, placement/removal, drone door opening/closing, culling, pan and zoom.
- Powered animation at three times in every rotation, warming retained content
  before advancing the clock to catch incorrectly classified static animations.
- A busy fixture using actual NPC updates and the construction-drone state machine;
  it asserts crew movement, drone launch and completed construction, then compares
  four snapshots with the reference renderer.
- Static draw counters must remain unchanged while live counters advance.

These are dedicated free-build/disabled-failure rendering fixtures. Normal run
costs, failures, hidden discoveries and progression are unchanged.

Final result: all 33 image pairs are pixel-identical, including warmed animation
and busy-state captures, with no script errors. Native shared-menu, workspace,
placement-preview (148 cases), menu recovery and Architect selection suites pass.
Embedded geometry, NPC segment clearance/movement, Architect recovery, drone fleet
and production walker paths also pass. Existing raw-image loading warnings remain.
