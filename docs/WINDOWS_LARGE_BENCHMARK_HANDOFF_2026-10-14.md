# Project handoff

Updated: October 14, 2026 · Project: `C:/Users/Alex/Documents/Brine Space` · Task: current Windows candidate and large-station benchmark

## Objective and acceptance

Rebuild the Windows candidate with accepted card improvements and current source changes;
check the large-station benchmark. Owner also requested fixing black open-door apertures
in large-room risers. This task is complete; the resulting frame-rate gate fails.

## Accepted decisions and constraints

Owner accepted the card appearance and authorized helper agents. One read-only agent
reviewed the five card/door files and found no actionable regressions; it ran no Godot
process. Rendering checks stayed serial after the build. No publication, Mac build,
gameplay redesign or unrelated refactor. Loading and 12-room zoom exceptions stay accepted.
Marsh polish, object-count tracing and Clone Lab revival remain parked.

## Current state

Candidate `brinespace-2fe5a9922a7a63cf`: `C:/bs-release-20261014/windows/`.
HEAD `67e7db969` plus frozen working changes, including card improvements, Crew Hab text,
and today's changes inherited from Claude. Source SHA and EXE/PCK hashes are in
`build_info.json`, `identity.json`, and `SHA256SUMS`; delivery hashes unchanged after QA.
Existing October 13 candidate preserved.

New fix: `rooms/doors/painted_door.gd` accepts an optional raised-door backing color;
`rooms/large-rooms/common.gd` passes its floor color. It no longer covers large thresholds
with near-black as the leaves retract. Ordinary callers retain the previous default.
No art replacements, UID changes, commit or upload. Documentation updated in CURRENT_STATUS.

Initial freeze copied and verified 36,275 runtime inputs and 57,822 files including
build support. The two door scripts were replaced after verification with explicit old/new
hashes in `freeze.json`; `freeze-before-door-fix.json` preserves preceding provenance.
Maintained export rebuilt the dependency manifest from the frozen source.

## Verification

- Native open-door probe: four failures before, zero after; all four large-room styles,
  closed/half/open captures reviewed. `test_large_room_art`: zero failures;
  `test_door_polish`: pass including 100 aperture states.
- Release manifest: 10 Python tests pass; release assertion safety: 2 pass.
- Full clean import exits 0; the same four non-runtime corrupt review PNGs as prior builds
  produce twelve known import error lines. No new script error; final export log clean.
- Pack audit from an empty directory: 35,790 checked, 0 missing/changed/unexpected.
- Actual EXE normal title/New Game/dialogue/Continue/simulation/F8: zero failures,
  debug=false, exit 0. Reviewed `smoke-profile/.../release-game.png`.
- Three valid actual-release `mixed_large` runs, 1920x1080, RTX 4070 Ti, Compatibility,
  180 frames per action/speed, 40 rooms / 52 occupied cells / four multi-cell rooms,
  seven actions at 1x/2x/4x. **0/63 phases pass** p95<=16.7 ms / p99<=25 ms / max<=100 ms.

| Idle speed | Mean frame time across runs | Approx. FPS |
|---|---|---|
| 1x | 24.90-25.32 ms | 39.5-40.2 |
| 2x | 25.64-26.19 ms | 38.2-39.0 |
| 4x | 26.01-26.29 ms | 38.0-38.4 |

Zoom p95 39.41-44.38 ms; lighting 36.53-42.95 ms; pan 30.75-38.29 ms.
Worst frame 103.13 ms (pan). Texture peak 2744.00 MiB / 2.68 GiB, settled
1944.32-1946.08 MiB / about 1.90 GiB: within the existing 3 GiB large-station
texture-counter limit. No automatic reports, missing-art fallback or engine errors
in valid benchmark runs. These counters do not establish physical GPU residency.

Initial second benchmark attempt was invalidated by a minimized window, retained and
excluded. Two fresh retry passes supply the remaining valid results. Save action omitted
because of the existing Bill carry/checkpoint fixture limitation. No controlled old/new
performance comparison, save/relaunch certification, endurance soak or target-PC/Mac test.

Owner profile: initial freeze guard failed while the owner closed the active game;
recorded progress/checkpoint/session/report changes were retained, not restored.
All subsequent import/build/audit/smoke and both benchmark-batch fingerprints are unchanged
(2,948 files). Scratch profiles and resolved-path guards isolated runtime writes.

## Next action

Large-station rendering/frame pacing needs further work to meet the existing 60 FPS
target. Profile live-room drawing and renderer submission before choosing a contained
optimization; sampled counters are a lead, not proof of the complete bottleneck.
Native GTX 1650-class and M1 acceptance remain open. Publishing remains the owner's call.

Evidence: `C:/bs-release-20261014/large-station-results.json`, stage logs and owner checks,
`benchmark-large/` (first valid + invalid attempt), `benchmark-large-retry/` (two valid),
`freeze.json`; adapted stage drivers and door test logs in
`output/release-drivers-20261014/`. Door captures: `C:/bs-door-probe-20261014/`.
