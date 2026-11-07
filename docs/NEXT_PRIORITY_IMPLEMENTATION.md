# Next-priority implementation — 2026-09-06

## Started and verified

### Power feedback and opening pacing

- Power/Reserves now leads with docked-drone refill demand, stored Power,
  charge-starved drones and offline bays. Station Health links charge starvation
  directly to Power details. Power Routing also includes the current refill need.
- Bay/site inspectors distinguish paused, offline, charging, reserve starvation,
  travel and blocked routes. Selected bay readings refresh twice per second.
- Charge credit already purchased is subtracted before counting additional Power.
  Traveling drones and offline bays are not counted as immediate charging demand.
  Demand is explicitly separate from the per-cycle room forecast.
- Full-frame paid opening comparison, Bill starting, controlled available cards,
  normal costs/failures, 300 seconds after setup:

| Opening | Metal delivered | Waiting for Power | Final Power | Survived |
|---|---:|---:|---:|---|
| One generator | 8 | 242 seconds | 0 | Yes |
| Two generators | 34 | 0 seconds | 11 | Yes |

Both include an awake Architect, mining, hydroponics and life support. The second
case pays for a generator at (19,19). Setup duration differs because construction
and charging are paid. These are controlled fixtures, not proof that all openings
or Architect choices are balanced. No production rates were changed.

Evidence: `tests/test_priority_foundations.gd`, `tests/test_power_demand_ui.gd`,
`tests/playtest_paid_opening.gd`; logs/images under `output/priority-foundations*`,
`output/power-demand-ui*`, `output/paid-opening-comparison*`.

### Recoverable progression records

- Meta saves retain the existing unversioned JSON format and primary path.
- New records are flushed to `.tmp`, then replace the primary after protecting
  its valid previous contents as `.bak`.
- Damaged/missing primary records fall back to an intact backup. Corrupt primary
  data never overwrites a valid backup during a subsequent save.
- Write failures report an actionable error. Save Game retries progression as
  well as the loop checkpoint; Save-and-exit remains open if progression fails.
- An Architect choice is not confirmed when it cannot be saved. Unlocks earned in
  the active process remain available for a Save Game retry. Title reports backup
  recovery, gameplay reports failures, and the pause menu retains the error.
- Tests cover corrupt primary, missing primary, recovery followed by another save,
  failed replacement, selection rollback and actionable error text.

Shared-menu, menu-recovery, workspace, placement-preview and Architect-selection
native regression groups passed with no script errors after these integrations.

## Remaining priorities

Station search, actionable diagnostic links, saved workspace restoration and the
Continue schematic are implemented in the [navigation and Continue pass](STATION_NAVIGATION_AND_CONTINUE.md).
Its cold Fit experiment identified substantial floor drawing cost but did not establish
a safe speedup; the experimental cache was removed.

- Rendering first pass completed: cached prop meshes and embedded wall-edge setup,
  pixel-identical across four rotations and close-up. Controlled frame-time gains
  are 3.1% at Fit and 7.1% close. See [render cache pass](ROOM_RENDER_CACHE_PASS.md).
  The follow-up retained floor/wall pass is implemented: current controlled
  samples reduce frame time by 39.7% at Fit and 38.9% close, with 17 pixel-identical
  state comparisons. The [content retention pass](ROOM_CONTENT_RETENTION.md)
  adds static furniture retention, six machine body/animation splits and prop
  culling: another 14.3% Fit / 18.6% close frame-time reduction in local samples.
  The [BRINE/batching and large-station pass](BRINE_BATCH_AND_LARGE_STATION_PASS.md)
  retains chamber parts, reduces GPU submissions by about 14%, and defers dormant
  crew navigation on restore. 101-room Fit remains slow; cold zoom and active-crew
  navigation rebuilds remain priorities, with measured limits in that report.
  The [zoom and restore follow-up](ZOOM_AND_RESTORE_PASS.md) caches door geometry,
  preserves prop bounds across zoom, centers Fit directly and removes redundant
  same-room navigation samples. Fit pauses improve 13.4% and restore 22.4% in
  local comparisons; 101-room Fit remains effectively unchanged.
  The [retained door/light and staged Continue pass](RETAINED_LIGHTS_AND_STAGED_RESTORE.md)
  subsequently improves 101-room Fit by 18.5% in its paired local benchmark,
  reuses wall assembly across zoom and yields navigation restoration behind a
  loading overlay. The cold Fit pause and initial scene/art loading remain limits.
- Architects: prototype role-specific placement incentives and compare decisions;
  avoid adding blanket output multipliers without gameplay evidence.
- Replayability: seeded site layouts need reachability/buildability validation and
  reproducible save seeds before replacing the fixed authored layout.
- Release: a separate runtime-only packaging pass should exclude source sheets,
  generation studies and unused exports, retaining runtime raw-image loading.

These remain future implementation work; this first batch does not claim them done.
