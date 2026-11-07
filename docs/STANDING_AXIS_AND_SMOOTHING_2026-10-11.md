# Project handoff

Updated: October 11, 2026 · Project: BrineSpace · Task: smoothing/standing overhead

## Objective and acceptance

Find repeated smoothing work, preserving collision/route policy and visual quality.
Admit only measured equivalent work. Small geometry kernel improvement installed;
whole-game frame gates remain open.

## Accepted decisions and constraints

Muted secondary display, isolated profiles/input, owner fingerprints, reused actual
debug=false runtime with small overlays. No art/runtime copies/screenshots, quality
changes or navigation deferral. Private query timers call originals exactly once.

## Current state

Changed `scripts/bill_npc.gd` `can_stand`: finite local coordinates use direct
up/right/down/left comparisons at the original strict thresholds, replacing four
unit-vector construction/dot iterations. Nonfinite local values keep original loop.
Remaining geometry/blocker/legacy/corridor behavior unchanged; no cache introduced.
Changed `tests/test_navigation_segment_parity.gd`: independent original standing
implementation plus six shape classes, sixteen door masks, blockers, exact edges,
negative and large-coordinate differential. Paired UIDs unchanged.

Evidence under `D:/bs-release-crew-cache-20261009/benchmark-input-isolation/`:
`detour-smoothing-attribution`, `standing-axis-trial`, `standing-axis-attribution`,
`standing-axis-workloads`. Scoped runners in `output/renderdoc-tools-2026-10-08/`.

## Verification

Smoothing-only detailed probe matches twelve full states/cameras and 54 UI
snapshots. Largest Margot event: 1667 standing queries/1344 unique points; only
~19% repeats. Peer copying 88 calls/~0.021 ms, crew-clear ~0.129 ms. Most cost lies
in segment geometry. Query wrappers inflate timings; overlapping fields must not
be added or treated as FPS acceptance. Do not prioritize an unproven standing or
peer-list cache based solely on call count.

115,200 original/candidate standing comparisons exact. Three alternating CPU
pairs, 163,840 queries each lane, equal 153,160 successful queries each:
154.333→130.615, 154.312→130.291, 154.342→131.229 ms (~15.3% improvement).
This headless query kernel is not a gameplay/render benchmark.

Coarse candidate replay matches twelve complete phase states/cameras and 54 UI
snapshots; local smoothing gains small/mixed. Three ordinary native current-station
pairs without private method timers, 6480 frames, idle/pan/selection/zoom-selection
at 1x/2x/4x: 36 full paired phase states/cameras and 162 UI snapshots exact.

| Metric | Installed control | Axis candidate now installed |
|---|---:|---:|
| Mean frame ms | 11.445 | 11.406 |
| p95 ms | 18.977 | 18.847 |
| p99 ms | 27.830 | 28.112 |
| Maximum ms | 46.199 | 44.504 |
| Frames >50 / >100 ms | 0 / 0 | 0 / 0 |
| Texture peak MiB | 1945.262 | 1945.262 |

Whole mean -0.34%, mixed pairs: effectively neutral. Fifteen passage frames have
11 better, mean crew 5.644→5.567 (-1.36%, small/mixed). Construction frame 27
mean 19.355→19.430; no construction/FPS improvement claim. Admit as equivalent,
measurably faster primitive checks, not a broad performance remedy.

Installed maintained segment/standing test: 153,824 comparisons, zero failures.
Maintained detour test: 41,442 comparisons plus original filter/swimmer coverage,
zero failures. Logs clean. Installed bytes equal measured candidate; UIDs unchanged.
All owner guards 2938 unchanged; native jobs terminal/runtime override restored.
No new rendered pixel certification claimed for pure equivalent collision checks.

Evidence 28.48 MiB plus 22.64 MiB scratch; C 123.25 / D 69.31 GiB free.
No cleanup-policy bypass attempted.

## Next action

Shift to larger animated room-content drawing costs. `RoomContents.advance_live`
queues every visible live/nonfrozen slot each frame. Some effects need continuous
time; others may have discrete output. Count/category/time these slots and observe
actual output changes before introducing retention. Preserve original pixels,
timing, material/flood behavior and default motion settings. Do not repeat rejected
triangle/cache/wall-cap trials. Reported/large scope for axis change, full frame/
memory/loading/endurance, bugs/visuals and PC/Mac certification remain open.
