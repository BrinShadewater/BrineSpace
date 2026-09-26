# Fit button profiling correction

Updated September 22, 2026.

## Objective and constraints
Trace the actual player-facing Fit transition before optimizing it. Preserve
runtime zoom behavior, room visuals and owner layouts during diagnosis.

## Finding and tool change
The earlier 205.895 ms "zoom-fit" profile calls _fit_station_view() with its
default animated=false. The real toolbar button and F key pass true, enabling
camera interpolation and retained redraw preparation. That earlier measurement
is an instant-jump diagnostic, not a direct measurement of the shipped button.

tests/profile_large_station.gd now labels that path zoom-fit-instant and adds
zoom-fit-button. The latter invokes the real toolbar button's connected signal,
enables normal main processing with the station paused, and records per-frame
zoom/visible rooms/preparing/settling/target until three settled frames. It does
not force extra draws. Missing button or missing result makes the profile fail.
Other baseline scenarios retain their existing instrumentation.

## Verification and limits
First probe failed because the button is local to UI construction, not a main.gd
member. Its script-error log is preserved; its old zero-failure summary is not
accepted. Corrected probe locates ViewportTools and the button's stable metadata.

Corrected native run exits 0, zero fixture failures and no reported script errors.
Animated transition: 17 sampled frames /977.149 ms including final settle samples;
first/worst frame125.710 ms while preparing, frame9 122.957 ms while settling,
frame10 96.025 ms while settling. Final view has101 visible rooms (100 baseline
plus the construction interaction's addition); screenshot inspected.

Evidence: output/fit-view-trace-2026-09-22/native-r2.log and
output/game-pass/2026-09-22-fit-button-r2/large-render-profile.json,
fit-button-settled.png. This is a paused, instrumented large-station trace with
uncapped rendering, not ordinary gameplay FPS or a before/after runtime gain.
No runtime, source art, layout or package changed.

## Next action
Investigate whether initial and settling retained redraw groups can be split more
evenly across frames. Require matched visual parity and paired transition timing
before installing a change; do not hide layers to make a timing number smaller.

## Opt-in floor-preparation experiment
scripts/grid_canvas.gd now exposes --split-zoom-prepare-floors for review only;
default gameplay behavior is unchanged. It schedules the two retained floor
halves separately during preparation, as settling already does, without changing
layer drawing, ordering or content. Existing preparation bounds remain in force.

Candidate run completes with zero failures, 17 frames, worst109.848 ms and
976.723 ms through final settle samples. Final framebuffer RGBA bytes match the
earlier reference exactly (zero changed pixels). A repeat reference completes with
zero failures and worst162.927 ms, demonstrating appreciable timing variation.
The candidate peak is below both reference peaks, but this is preliminary evidence,
not a shipped optimization or an ordinary FPS claim. comparison.json records all
three runs under output/fit-view-trace-2026-09-22; native split.log and
reference-repeat.log preserve results. Candidate frames are under
output/game-pass/2026-09-22-fit-split.

Next: confirm candidate timing once more and inspect intermediate preparation,
movement and settling frames before enabling it by default. Current test packages
retain the original default scheduling and are not superseded by this experiment.

## Repeat timing verification
The second opt-in native run exits 0 with zero fixture failures and settles in
17 sampled frames. Peak/first frame109.910 ms, compared with109.848 ms in the
first candidate and125.710/162.927 ms in the two references. Total elapsed is
1017.130 ms including settled samples, versus976.723 ms in the first candidate
and952.695/977.149 ms in references. Thus peak reduction is repeatable in these
samples, but a shorter transition is not demonstrated. All four final captures
match in every RGBA pixel. Keep the flag disabled pending intermediate review.
Evidence: split-repeat.log and updated comparison.json in
output/fit-view-trace-2026-09-22; candidate repeat artifacts in
output/game-pass/2026-09-22-fit-split-repeat.

Separate native visual capture exits 0 with zero fixture failures. Inspected the
17-frame board spanning two preparation frames, seven moving frames, five settling
frames and three settled frames. Preparation retains the close room; the station
appears during movement and remains visible through settling. No obvious missing
floor half appears at board scale. This is not full-resolution per-layer parity.
Captures read back GPU images, so their timings are excluded from comparison.
Probe: output/fit-view-trace-2026-09-22/capture.gd; artifacts:
output/game-pass/2026-09-22-fit-split-capture/transition-00.png through -16.png;
board: output/fit-view-trace-2026-09-22/transition-board.jpg.
Next: matched reference transition capture/full-resolution comparison before any
default change. Candidate remains opt-in; releases are unchanged.

## Installed default and acceptance scope
Split floor preparation is now the local default; the temporary opt-in variable
and flag are removed. This supersedes the experiment's disabled-default notes
above. Only the preparation schedule changes. Existing release packages predate it.

The reference capture completes with zero failures (18 frames). Reviewed its board
against the17-frame candidate, plus full-size moving frames from both. Different
wall-clock camera deltas prevent claiming frame-by-frame pixel identity from those
captures. No obvious lost floor half or prop population is visible.

The maintained test_live_surface_retention.gd supplies controlled-step coverage:
opt-in candidate and final default both exit0 with PASS failures=0. Each reports
zero strongly differing sampled mid-zoom pixels of18642; exact settled/full-rebuild
checks pass, as do selection invalidation while settling and live floor/wall
retention. Fit glide takes30 controlled steps, holds3, never rebuilds floors and
walls together, and widens its cover once. This supports installing the lower-peak
schedule, not a faster total transition or general FPS improvement.
Logs: surface-retention-split.log and surface-retention-default.log under
output/fit-view-trace-2026-09-22. Visual reference: reference-transition-board.jpg;
full frames under output/game-pass/2026-09-22-fit-reference-capture.

Workflow lesson: profile the actual animated button/key path separately from
instant camera helpers. Keep GPU readback capture runs out of timing comparisons;
use controlled camera steps and forced-rebuild parity for reveal correctness.
Next work returns to animation/room polish; retain these timings as bounded evidence
and validate the changed renderer in the next planned release, not a new export
solely for this scheduling change.
