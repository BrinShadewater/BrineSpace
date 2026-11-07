# Indexed drone storage: real-map verification

Updated: October 10, 2026 · Project: BrineSpace · Task: PC/Mac performance readiness

## Objective and acceptance

Compare current normal source with the private 21-source lossless indexed drone
provider on the reported 12-room save, the frozen owner save (10 rooms, with a
pending room completing), and the corrected deterministic 40-room stress fixture.
Preserve selected pixels and gameplay, reduce retained texture storage and uploads,
and demonstrate gains with matched native workloads before admitting the provider.

## Accepted decisions and constraints

The provider stays private. This pass changes no production gameplay or art. All
native runs use the actual Windows `debug=false` executable with small current-source
PCK overlays, RTX 4070 Ti, 1080p, muted audio, the secondary display, disabled physical
input, and isolated profiles. These are owner-hardware measurements, not GTX 1650,
M1, Mac, cold-loading, endurance or final packaged-release certification.
Current construction prewarming and Solar working-copy fixes are preserved in both
lanes. No downscaling, dropped frames, default-quality reduction or engine upgrade.

## Visual verification

72/72 station-art image pairs match every RGBA pixel: 24 per map across idle, pan,
zoom and lighting at 1x/2x/4x, including adjacent pan/zoom samples. Capture records
have identical state, camera, animation clock and room-light levels.

Earlier capture passes exposed fixture issues, not grounds for waiving pixels:
lighting fades used native elapsed time while gameplay used fixed time; zoom waited
on different asset preparation; portrait meters refreshed on their own interval;
discovery notifications obscured rooms; pending drone decoding could leave a frozen
reference image incomplete; deferred background drawing could remain stale.
The final visual fixtures use the simulation light clock, synchronous camera
placement, refreshed portraits, completed pending decoding and repeated redraws
without advancing gameplay. Current/large captures also hide the hand and transient
discovery notification and drain pending background work. Reported captures hide the
hand. These checks establish station-art equivalence in that scope; they do not
certify asynchronous zoom pacing, the whole UI, linear-filter fallback, every flooded
material or animation speed at 30/60/120 FPS. Screenshot readbacks are excluded from
performance acceptance.

Evidence: `indexed21-loaded-pixels` (reported: 24/24) and
`indexed21-station-only-pixels` (current and large: 24/24 each), under
`D:/bs-release-crew-cache-20261009/benchmark-input-isolation/`.
Earlier mismatches and diagnostic detail images remain available in the preceding
whole-station/fixed-clock/loaded capture directories.

## Matched performance results

18 serial runs: three alternating pairs per map, 19,440 measured frames total.
Each lane/map has 3,240 uncapped samples. Workloads use ordinary rendering, real
asynchronous preparation, no screenshot capture inside measured phases, and the
existing bounded trace collection. Results are pooled across actions and speeds.

| Map | Mean ms, normal -> indexed | p95 ms | p99 ms | Frames >50 ms | Frames >100 ms | Peak texture MiB |
| --- | --- | --- | --- | --- | --- | --- |
| Reported 12 | 14.331 -> 14.416 | 21.198 -> 21.433 | 25.177 -> 25.043 | 0 -> 0 | 0 -> 0 | 1558.872 -> 1528.343 |
| Frozen current | 13.866 -> 13.983 | 20.992 -> 21.627 | 34.828 -> 29.612 | 9 -> 3 | 0 -> 0 | 1940.831 -> 1911.626 |
| Expanded 40 | 30.589 -> 30.659 | 52.302 -> 50.846 | 67.975 -> 67.808 | 200 -> 179 | 6 -> 1 | 3028.007 -> 2629.355 |

Average frame time worsens by 0.60%, 0.85% and 0.23% respectively. Pair-level
results are mixed: no consistent average-performance win. Large-scene memory falls
398.652 MiB (13.17%); current/reported savings are about 29/31 MiB. The large
candidate still contains a 109.421 ms frame, versus a normal maximum of 107.048 ms.
Performance release gates remain failed.

### Upload and renderer attribution

Within the measured large workload, fresh upload events fall 584 -> 471, decoded
storage submitted for texture creation falls 22,476.375 -> 15,141.815 MiB (32.63%),
and measured texture-creation CPU time falls 3,301.648 -> 2,286.562 ms (30.74%).
These are complete sampled event records, not measured GPU transfer or residency.
Current-map uploads fall 240 -> 207 and decoded submissions 7,315.765 -> 5,663.958 MiB.
Reported-map uploads are negligible and equal (six events, 0.194 MiB).

Large renderer averages are nearly unchanged: CPU 7.403 -> 7.374 ms, GPU
4.899 -> 4.869 ms, draw calls 2770.600 -> 2760.421. These separately measured,
potentially overlapping timings must not be added to infer total frame cost.
Reduced uploads and memory have not translated into a reliable average-frame gain.

## Verification and remaining discrepancies

All 108 phase pairs have identical final cameras. Reported/current state pairs are
exact. Six large-map state comparisons fail strict equality, all exclusively at
`crew/playback/branforth/phase` in 1x zoom and subsequent lighting: maximum delta
2.7284840165e-8 seconds in `walk-north`, repeated in all three pairs. Other captured
fields are exact. The strict comparator exits nonzero; no epsilon allowance was
added. `crew_sprite_player.gd` accumulates gait phase from sampled position distances,
and grid playback obtains Branforth's position through zoom-scaled coordinates.
Different asynchronous zoom histories are a plausible cause; this remains an
unverified explanation requiring a focused probe, not a closed regression.

All 108 candidate backend scans complete: provider enabled, 21 sources, no original
texture duplication for indexed sources and no observed filter/material fallback.
All run logs finish without engine errors or missing PNGs. All 2,938 owner files
remain unchanged in every recorded profile guard. Processes have exited, runtime
configuration is restored, and all 76 measured source/resource identities remain
unchanged. Detailed results and the intentional strict-state failure are in
`indexed21-current-normal-real-maps/comparison.json` and `validation.json`.

## Storage and changed files

The five evidence directories total 1,070.93 MiB (about 1.05 GiB), including failed
capture evidence, compact overlay packs and isolated profiles. Existing runtime
packages are reused. Free space after the pass: C 124.77 GiB / D 72.75 GiB; the
existing 20 GiB free-space floor is enforced before preparation and runs. No broad
cleanup or release copies were created.

Private runners/comparators live in `output/renderdoc-tools-2026-10-08/`, with names
`run-indexed21-*` and `compare-indexed21-*`. Production changes in this milestone are
this handoff and `docs/CURRENT_STATUS.md` only. Earlier accepted production fixes
remain in place. No export, commit, upload or release certification was performed.

## Next action

1. Probe the small gait-phase discrepancy using world position, rendered position,
   sampled clock and per-frame playback phase during zoom. Preserve the strict gate.
2. Separate indexed rendering overhead from storage savings with a matched ordinary
   RGBA control using the same draw groups. Profile group/material preparation before
   changing it; verify any measured remedy with exact pixels and matched real maps.
3. Complete loader, explicit filter/material fallback and session-lifetime checks,
   then transition/endurance coverage before considering normal-source integration.
   Do not encode more sources solely to chase average FPS: current evidence shows
   reduced uploads without an average-frame win.
4. Continue room/layer CPU hotspot work and the remaining Windows/Mac release plan.
   Hardware targets, loading gates, two-hour native soak, ten scene transitions,
   packaged bug closure and Mac certification remain open.
