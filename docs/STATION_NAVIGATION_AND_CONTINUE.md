# Station navigation and Continue

Implemented September 6, 2026.

- **Find Room / Ctrl+F** opens the journal's installed-room list with search focused.
  Search combines name, ID, category, coordinates, observed interruption and next-cycle
  interruption text. Every word must match. It never searches unbuilt or hidden rooms.
  Enter locates the first sorted match; result links select and center the inspector.
  Escape clears a focused search before closing the journal. History and room queries
  remain independent when switching tabs.
- Station Health and Rooms provide inspection links, relevant supply-review links and
  a Resume action for suspended rooms. Resume uses the existing operation handler;
  stale links cannot suspend a room again. Malformed coordinate links are ignored.
- An optional versioned workspace field accompanies loop checkpoints: normalized camera
  center, journal tab, separate searches, event filter, resource selection, per-tab
  scrolls, inspector scroll and sidebar scroll. Existing saved room selection remains
  in the gameplay snapshot. Pause-menu round trips restore presentation state too.
  Saves without this extension retain the prior pixel-scroll fallback. Invalid optional
  values fall back safely without invalidating the gameplay checkpoint.
- Continue displays a schematic of installed rooms, architect portrait/name, cycle,
  room count, timestamp and critical oxygen/food/power reserve warnings. Low-reserve
  estimates explicitly use the last recorded rate, not a promised future forecast.
  No new confirmation step is required to Continue.

## Validation

Native `test_station_navigation.gd` passes search/hidden-room boundaries, Ctrl+F,
Escape/Enter, independent queries, malformed links, Resume and stale Resume, checkpoint
and menu camera restoration, restoration at a different window size, old saves,
malformed optional fields and Continue preview warnings/layout at 1280×720 and 1600×900.
Screenshots: `output/continue-preview-1280.png` and `output/continue-preview-1600.png`.

Existing native save, UI workspace, shared-menu, menu-recovery and staged restoration tests also pass. Staged
restoration still yields while rebuilding crew navigation and returns a paused station.
Logs: `output/navigation-save.log`, `output/navigation-feature-final.log`,
`output/navigation-workspace.log`, `output/navigation-staged.log`,
`output/navigation-menu.log`, `output/navigation-recovery.log`.

## Cold Fit experiment

Added opt-in cumulative draw-stage timings to the existing large-station profiler.
Unlike the per-draw dictionary, these retain all measured stages up to the first frame
after a transition. They do not change the normal renderer or capture GPU work.

The local 101-room cold Fit transition measured **200.626 ms**, with the zoom command
itself taking **0.136 ms**. Instrumented floor drawing accounted for **44.592 ms**,
live-room drawing **30.643 ms**, door/light validation **15.928 ms**, walls **10.703 ms**,
and the two door passes **16.206 ms** together. These partial script timings do not
explain the entire native frame or isolate GPU submission costs.

A bounded experiment reusing floor-plate geometry measured 229.921 ms overall and
47.201 ms in floors. Other stage costs and draw counts also varied, so this is not a
controlled proof of regression, but there was no evidence to keep the extra cache.
The experiment was removed. **No Fit speedup is claimed in this pass.** Follow-up
should address floor command generation/submission while preserving exact seams and
transforms. Logs: `output/navigation-fit-profile.log` and `output/navigation-fit-plates.log`.
