# Retained doors/lights, zoom data and staged Continue

## Delivered behavior

Door and light drawing commands now have ordered retained passes: floors, walls,
rear doors, room contents, front doors, lighting, foreground effects. Door keys
include the discrete animation frame, variant, corridor shape, exterior service
opening, light level and per-piece crew depth classification. Crew movement only
invalidates the door passes when it changes which side of a piece is drawn.
Lighting keys include visible room identity/position, zoom and exact fade level.
Power fades and door motion remain live. The current granularity is whole passes,
not individual doors: one changed door redraws both door passes.

Wall assembly queues retain room-space data across scales. Their owned deep keys
include layout, edges and props; the original complete depth-sort order is retained.
Each view caps its cache at 32 entries and falls back to fresh assembly beyond that.
Rooms containing actors and full previews keep their original assembly path.
The original native draw transforms remain in use. A trial moving prop scaling to
node transforms changed edge pixels and was removed.

Continue now restores active navigation in approximately 4 ms work slices, yielding
between geometry rooms and local-link batches. A root-owned loading overlay remains
active while the gameplay subtree is hidden and disabled, including timers/input.
The station is revealed only after route validation and deferred layout/scroll
corrections, and remains paused. Reduced motion disables the indeterminate bar;
menu text scaling and the existing mono font are used.

Saves are refused during restoration, so a partial station cannot overwrite a
checkpoint. Reentrant restores are rejected. Closing the window during restoration
quits without saving the partial state. Rejected checkpoints release the overlay
and leave gameplay intact. Normal `RunSave.restore()` remains synchronous for
existing callers; `restore_staged()` is the separate Continue entry point. Shared
validation/application, crew restoration and finalization keep the two paths aligned.

## Local native measurements

Godot 4.6.1 Compatibility, RTX 4070 Ti, 1600×900, VSync disabled.
Control: `--redraw-doors-lights --rebuild-shell-queues`; optimized: defaults.
Both use the same pass decomposition; the control skips retention-key preparation
and redraws the three new passes every frame. Existing earlier caches remain on.
Logs: `output/retention-baseline.log`, `output/retention-optimized.log`.
Structured results: `output/retention-comparison.json`.

| View | Control mean ms | Retained mean ms | Reduction |
|---|---:|---:|---:|
| 50-room Fit | 37.92 | 34.10 | 10.1% |
| 50-room close | 16.77 | 13.99 | 16.6% |
| 101-room Fit | 73.59 | 59.95 | 18.5% |
| 101-room close | 19.44 | 17.48 | 10.1% |

The 100-room fixture becomes 101 rooms as construction completes. It uses active
crew/drone simulation. GPU draw calls are unchanged (about 11,687 at large Fit).
At large Fit, viewport CPU rendering measured 25.97 → 24.00 ms and GPU rendering
22.12 → 20.43 ms. CPU/GPU timelines overlap; do not add them as serial frame costs.
The main gain is avoiding repeated drawing preparation. This remains about 17 FPS
in the largest view, not a solved 60 FPS target.

Cold Fit affected frame: 216.70 → 211.98 ms (2.2%, small enough to treat cautiously).
Normal-view transition: 55.01 → 45.41 ms (17.5%). These are single transitions,
not repeated-trial percentiles. Full drawing commands still rebuild at a new scale;
wall data reuse does not eliminate the cold Fit hitch. Concurrent desktop activity
and ongoing room integrations limit the precision of these local comparisons.

The dedicated restore fixture measured synchronous restoration at 308.50 ms and
staged completion at 511.14 ms, with 76 loading frames and a longest observed
frame interval of 45.71 ms. Total loading is longer because it yields; the benefit
is responsiveness. It verifies fresh navigation graphs and the real pending-
checkpoint Continue path. This measurement excludes initial scene/art loading;
that earlier startup phase can still block.

## Validation

- 33 native RGBA pairs are pixel-identical against the full direct renderer:
  four rotations, close view, power/fades, doors, raised walls, construction,
  removal, pan/cull/zoom, 12 motion samples and four busy crew/drone samples.
  Fixture contains 42 rooms and 37 views. Stable door/light counters stay unchanged
  while the animation clock advances and live room content continues drawing.
- Six room views retain their wall assembly across three zoom transitions.
- Staged and synchronous restoration produce equal crew snapshots, graph point
  counts and resources. Tests cover repeated yielding, hidden/disabled gameplay,
  blocked saves, invalid input without mutation, paused completion, reduced motion
  and the real Continue entry point consuming its pending checkpoint.
- Shared menu, UI workspace, menu recovery, architect recovery, navigation clearance
  and movement trace regressions pass. Save-suite verification includes current
  one-specialist-per-deck behavior; that rule was introduced by another task.
- Loading overlay and native close view inspected. Existing raw-image warnings
  remain. No export, commit or deployment was performed.

Key tests: `test_retained_lights_parity.gd`, `check_retained_lights_parity.py`,
`test_zoom_shell_reuse.gd`, `test_staged_restore.gd`, `test_run_save.gd`.
Reference switches remain available for controlled comparisons.
