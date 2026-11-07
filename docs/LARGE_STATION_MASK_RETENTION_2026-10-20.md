# Large-station mask retention handoff

Updated: October 20, 2026 · Project: BrineSpace · Task: remaining frame cost and hitches

## Objective and acceptance

Reduce measured large-station work while preserving rendering and gameplay.
Retained a small underwater visibility mask optimization; the overall frame-pacing
gate remains open. No repeatable FPS or hitch improvement is claimed.

## Accepted decisions and constraints

Keep existing artwork and renderer. No rover body cropping, larger cache/grace
repeat, or broad refactor. Tests use isolated profiles, muted native windows on
the secondary display, and the frozen unsigned Windows candidate. Delivery is
unchanged; this is a source change, not a new exported build.

## Current state

- `scripts/underwater_visibility.gd` snapshots the mask's actual terrain, survey
  and corridor-light inputs. Unchanged masks skip rebuilding and uploading.
  In-place terrain edits, same-count moves, power changes, suspension, low-power
  flicker and reset invalidate immediately. Dynamic light uniforms, silt and
  visual clocks still run on every draw; the texture retains its identity.
- `tests/test_underwater_mask_retention.gd` and its paired UID cover CPU mask
  bytes, native texture pixels, invalidation, skipped uploads and texture release.
  `tests/index.json` registers it in the crew group with an explicit native lane.
- `tools/release_benchmark.gd` and `tools/run_release_benchmark.py` add opt-in
  `--deterministic-clocks`: fixed-step survey cadence and discovery tween,
  seeded fixture pilot and per-phase saved-state capture. Production timing is
  unchanged. This addresses the comparison limitation in the preceding report.

Evidence and private drivers: `D:/bs-frame-cost-next-20261020`.
The reference helper retains original mask behavior with matching instrumentation.
Both variants include the previously accepted carry-cargo storage overlay.
Runtime identity and overlay member hashes are recorded per run.

## Verification

Native regression: original helper fails 24 redundant-upload checks; retained
implementation passes all 97 checks across 24 states, including exact native
mask pixel comparisons. An initial parse-error attempt is not counted as red.
Native lane classification and scoped diff whitespace checks pass.

Two unchanged fixture runs have identical state/camera snapshots in all six
phases, with mean frame times 27.551 and 27.629 ms. Two reversed-order mask
comparisons then match full saved state (excluding timestamp) and start/end
camera in all 12 paired phases. Each run measures 1,080 frames at 1920×1080:
idle and lighting at 1×, 2× and 4×.

| Measurement | Reference 1 | Candidate 1 | Candidate 2 | Reference 2 |
|---|---:|---:|---:|---:|
| Mask uploads | 1,080 | 26 | 26 | 1,080 |
| Fog CPU mean, ms | 0.481 | 0.345 | 0.365 | 0.415 |
| Frame mean, ms | 31.055 | 26.152 | 27.308 | 26.788 |
| Frame p95, ms | 44.942 | 36.729 | 39.242 | 38.040 |
| Frame maximum, ms | 101.836 | 88.199 | 88.337 | 90.742 |
| Frames over 50 ms | 39 | 12 | 21 | 18 |

Uploads fall 97.6%; fog CPU falls 0.050–0.136 ms in both pairs. Overall frame
results are mixed, and no phase passes the existing pacing gate. Texture memory
ends at 1,968.448 MiB in all four runs. A minimized candidate attempt is excluded
under `invalid-minimized-mask1`; the successful retry and second pair are valid.
The second pair launches directly on screen 2. Final candidate screenshot was
visually inspected; exact pixel acceptance here is for the mask test, not a
whole-scene screenshot comparison.

All 2,971 owner files hash-identical; signed ZIP size/mtime unchanged.
Hash-verified temporary EXE/PCK copies were removed by the maintained runner.
C and D retain 23.26 and 26.09 GiB free respectively. Original delivery preserved.

## Next action

Large-station ordinary frames remain roughly 26–27 ms and sampled hitches reach
88 ms. The prior body-sheet upload stalls remain unresolved; this small mask
change does not address their allocation/upload cost. Use the now state-matched
fixture to investigate the next live-render or body-upload hypothesis, preserving
art and avoiding previously rejected renderer/cache trials. Longer gameplay and
endurance acceptance must follow any larger change; these short comparisons do
not replace that coverage.
