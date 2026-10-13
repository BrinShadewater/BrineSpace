# Project handoff

Updated: October 6, 2026 · BrineSpace · Station memory/pacing and cycle eligibility

## Objective and acceptance

Measure the isolated Veld backend in larger native workloads; address a reproduced
cycle stall without changing emergency Metal rules, animation quality or saves.
Release certification remains separate.

## Accepted decisions and constraints

Normal runtime keeps its current GPU-backed animation storage. The private Veld
backend remains experimental: lower texture accounting is not a total-RAM or FPS
win. No art changes, downscaling, atlas conversion, renderer upgrade, default
quality changes, export or upload. Owner layouts/archives remain intact.

## Current state

Evidence: `output/private-veld-workloads-2026-10-05/` (work began before midnight).
Copied benchmark/Main/scene adapters use the prior isolated Veld bank. The reported
12-room checkpoint is preserved as-is and has no active Veld. The 40-room fixture
starts fresh with selected Veld and standard core recovery, then uses the maintained
fixture's deterministic placement/resource reserves. It has one active Veld, five
drones and 40 powered rooms; it is not the older reported-save-based 40-room fixture
or a full busy-crew release workload.

Normal source change: `scripts/metal_trickle.gd` checks affordable Metal and the
three-cycle award interval before expensive harvest-route queries. Those queries
are observational and do not populate route caches or change drone state. Eligible
low-Metal cycles still check income and award exactly as before. No economy rule
changes. `tests/test_metal_trickle.gd` adds real-route query-budget/outcome coverage
and verifies the explicit scratch user directory before gameplay writes.

## Verification

Godot 4.7.2 native Compatibility / RTX 4070 Ti / 1920×1080 / `debug=true`.
Three alternating reference/private pairs per scene: idle, pan, zoom and lighting
at 1×/2×/4×, 60 frames per phase after 180 warm-up frames. All 72 paired phase
end states match for crew, camera, production and drone phases. No missing runtime
art or engine errors. Active-Veld runs route 902 draws / 134 poses with four slots
and three retained spill images. Slot/overflow policy is unchanged.

| Whole-station measure | Reported 12 rooms | Selected-Veld 40 rooms |
|---|---:|---:|
| Ending engine textures, reference → private (MiB) | 3,583.40 → 3,096.34 | 4,076.31 → 3,590.28 |
| Median paired texture reduction (MiB) | 487.06 | 486.03 |
| Median paired OS peak working-set increase (MiB) | 364.92 | 296.50 |
| Median paired sampled private-commit change (MiB) | −12.94 | −103.13 |
| Median of run phase-mean averages, reference → private (ms) | 20.287 → 20.537 | 36.566 → 37.250 |

External process sampling every 25 ms includes loading and gameplay. Working set,
commit and texture counters are different measures; do not add them or infer M1
unified memory. OS/driver cache state is uncontrolled. Sixty samples per phase
make p99 equal the maximum here; these short runs do not certify release tails.
Both texture budgets and the 60 FPS target fail. Each large run has frames over
100 ms; full placement/demolition/UI/save, 1440p, longer soak, minimum hardware,
packaged Windows and Mac remain open.

Focused copied-cycle timers found ~37 ms in emergency Metal routing despite ample
Metal, ~19 ms in discovery and ~12 ms in interface refresh. The new regression
test failed on three unnecessary-query cases before the guard and passes after;
existing emergency recovery/real-cycle checks also pass. Drone fleet and route
cache suites pass. Green logs have no errors/warnings. Test lanes are headless;
the matched timing workloads are native. All launches use scratch APPDATA and
all 2,936 owner non-log files remain unchanged.

Three additional alternating before/after guard pairs preserve every phase's
crew/camera/drone/production state, texture allocation and Veld presentation
counters. Before behavior is reloaded from a physical copy verified against HEAD
inside each isolated process; normal source stays fixed. Results:

- Emergency Metal stage at the last measured cycle: median 37,788 → 3 µs.
- Last cycle's summed instrumented stages: median 67.212 → 31.126 ms.
- Matched 4× cycle frame: 106.136/101.300/101.932 →
  68.195/68.644/68.334 ms; median 101.932 → 68.334 ms.
- Other stalls remain: after-run maxima 116.474/92.191/101.235 ms. This fixes
  recurring eligibility waste, not every stall or the frame-time release gate.

`matched-summary.json`, `metal-matched-summary.json`, source hashes and full logs
retain comparisons. A separate epoch probe confirms that the sampled end counter
is one ahead of the simulation/draw epoch. Uploads of 45.94–137.81 MiB atlases
align with multiple >50 ms frames; in that probe the 137.81 MiB South mining
body/effects uploads take ~19/21 ms and coincide with 71/80 ms frames. A previous
run took 37 ms on the body upload and produced a 116 ms frame. Timing varies;
uploads contribute, but do not explain every remaining stall. The current drone
cache can evict entries older than two frames under its soft budget while canvas
pins keep images alive; re-entry can upload the same path again. No cache-policy
change has been made. Final workload screenshots inspected; discovery toast and
fixture reserves limit their visual-acceptance scope.

## Next action

Trace drone LRU eviction against retained canvas pins and test session-scoped weak
reuse of surviving immutable atlas textures before broader storage changes. Keep
the soft active-set policy and avoid a permanent cache that holds every visited
asset. Then measure first-use upload remedies with exact pixels/filtering, retained
canvases, water/effects and action deadlines. Separately profile discovery persistence
and interface refresh (~31 ms combined on the heavy cycle). The Veld CPU bank needs
an explicit hardware/RAM tradeoff decision and further coverage before admission;
no default enablement or Mac memory claim is accepted.
