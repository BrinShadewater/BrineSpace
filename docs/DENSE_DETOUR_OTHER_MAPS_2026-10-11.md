# Project handoff

Updated: October 11, 2026 · Project: BrineSpace · Task: reach-fill cross-map validation

## Objective and acceptance

Validate installed dense reachability on reported/large maps and distinguish local
CPU gain from whole-run performance. Preserve full gameplay/camera/UI state.
Full PC/Mac release requirements remain incomplete.

## Accepted decisions and constraints

Muted secondary display, isolated profiles/input, owner fingerprints; existing
debug=false runtime plus small overlays. No asset/runtime copies, screenshots,
renderer/quality changes or new production edits. Reference restores only the old
reach fill. Regular benchmark diagnostics enabled in both lanes; private method
timers disabled. Same deterministic survey/notification fixture clocks.

## Current state

Runners/comparator in `output/renderdoc-tools-2026-10-08/`:
`run-detour-dense-other-maps.py`, `compare-detour-dense-other-maps.py`,
`run-detour-large-call-census.py`. Evidence under
`D:/bs-release-crew-cache-20261009/benchmark-input-isolation/`:
`detour-dense-other-maps`, `detour-large-call-census`.
Production keeps the already verified dense fill; no new code changes.

## Verification

Twelve native runs, three alternating pairs per map, idle/pan/selection/zoom-selection
at 1x/2x/4x, 90 measured frames per phase: 12,960 frames.
All 72 complete paired phase states/cameras and 324 UI snapshots exact.

| Metric | Original fill | Installed dense fill |
|---|---:|---:|
| Reported mean ms | 12.123 | 12.125 |
| Reported p95 / p99 ms | 17.673 / 27.268 | 17.508 / 26.604 |
| Large mean ms | 24.401 | 24.841 |
| Large p95 / p99 ms | 35.563 / 48.464 | 35.966 / 49.858 |
| Large max ms | 85.294 | 88.159 |
| Large >50 / >100 ms | 27 / 0 | 32 / 0 |

Reported mean neutral; large +1.80%, all three pair means slower. Do not present
this as a whole-game improvement or passed frame gate. Texture peaks unchanged,
1559.506 MiB / 3028.686 MiB. Large sampled creation events 583→586, not proof of
bus traffic or a cause for the entire timing difference.

One counter-only large replay, no method timers, matches the installed control's
12 full phase states/cameras and 54 UI snapshots. Reach fill runs six times in
five logical 2x frames: idle 50/51/75, pan 10/11, Branforth/Margot. Call census
identifies these events after the whole-run comparison; it is not a preselected
whole-frame performance gate. Comparing those same frames in all three prior
pairs gives 15/15 lower crew CPU measurements: mean 11.540→10.347 ms (-10.34%).
This supports retaining the targeted CPU improvement alongside the earlier current
station's 15/15 events; it does not erase the slower large whole-run measurements.

All-frame large means: crew 1.631→1.644 ms, simulation step 2.299→2.321,
drawing callbacks 10.093→10.267, renderer CPU 6.302→6.416 and GPU 4.791→4.924.
Timings overlap; do not add them or attribute the shift to one cause without
stronger evidence. Rendering/upload tails remain unresolved.

Loading source follow-up: `RunSave._finish_restore` calls `Companions.restore`,
which invokes `restore_snapshot` without staged mode. Thus the optional companion
staged-rebuild call pattern does not establish a current Continue defect. No
speculative loading fix made. Adapter main source differs from current only by
two paused toast tweens, manually stepped by the shared fixture.

No engine errors/missing art. Owner guards both 2938 unchanged, source identities
unchanged; native jobs terminal/runtime override restored. Evidence 41.97 MiB plus
36.70 MiB scratch; C 123.00 / D 69.36 GiB free. No cleanup-policy bypass attempted.

## Next action

Attribute repeated `can_stand`, segment, peer-list and proximity checks inside
route smoothing, with exact ordered-route checks before proposing a scoped cache.
Preserve dynamic fire/door/facing policy and graph rebuilding. Continue separate
render/upload investigation; do not repeat rejected cache/triangle/wall-cap trials.
Loading/endurance, broader bugs/visuals, target hardware and actual PC/Mac release
certification remain open. Indexed lossless provider remains private.
