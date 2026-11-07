# Project handoff

Updated: October 11, 2026 · Project: BrineSpace · Task: wall redraw pacing

## Objective and acceptance

Test bounded size-only wall-slot rebuilds during landed zoom. Require complete
rooms, unchanged structural updates, native pixels/zoom behavior and a matched
performance improvement. Candidate rejected; original release gates remain open.

## Accepted decisions and constraints

Private overlay only; preserve complete old commands at correct scale while slots
wait. New slots and non-size key changes bypass the cap. Reused debug=false runtime,
muted secondary display, isolated profiles, input disabled and owner fingerprints.
No art/runtime copies, screenshots, quality changes or production edits.

## Current state

Evidence under `D:/bs-release-crew-cache-20261009/benchmark-input-isolation/`:
`wall-slot-settling-trial`, `wall-slot-settling-native`. Corresponding runners/
comparator in `output/renderdoc-tools-2026-10-08/`. Candidate uses per-slot built
size, independent scaling, a twelve-slot size-only budget and explicit settling
backlog. Native fixture lowers budget to two to exercise deferral. Not installed.

## Verification

Three alternating native large-station pairs, idle/pan/selection/zoom-selection at
1x/2x/4x, 90 measured frames per phase: 6480 frames. All 36 complete paired phase
states/cameras and 162 UI snapshots exact.

| Metric | Installed control | Private candidate |
|---|---:|---:|
| Mean frame ms | 24.242 | 24.365 |
| p95 ms | 34.887 | 35.405 |
| p99 ms | 47.495 | 49.280 |
| Max ms | 93.472 | 77.253 |
| Frames >50 / >100 ms | 25 / 0 | 29 / 0 |
| Texture peak MiB | 3028.686 | 3028.686 |

Mean +0.51%, two pair means worse and one better. Lower maximum does not establish
better distribution or sustained performance. Do not adopt or repeat unchanged.

Native test PASS, zero failures/errors: deferral actually exercised, wall backlog
drains before settling ends, all visible settled slots have current size and unit
scale. Retained selection/settled zoom pixels match forced rebuild; zoom reveal
zero strongly differing sampled pixels out of 27,232; Fit glide passes in 30 frames.
These are exercised cases, not exhaustive interruption/animation certification.
Switching walls off with pending backlog remains untested and may need cleanup in
any future variant. No fix for an uninstalled rejected candidate required now.

Production source matches pinned trial identity and has no wall-slot backlog fields.
Both owner guards 2938 unchanged. Native jobs terminal and runtime override restored.
Evidence 21.11 MiB plus 18.11 MiB scratch; C 122.96 / D 69.50 GiB free. No cleanup
policy bypass attempted.

## Next action

Refresh the separate current-station non-rebuild companion passage spike with
narrow attribution of detour starts, reachability, padding and route attempts.
Do not assume the historical ~9 ms update still has identical timing after admitted
changes. Preserve route ordering and exact movement/playback state in any remedy.
Wall/texture stalls and full performance, memory/loading/endurance, visual/bug and
PC/Mac release gates remain open. Indexed provider stays private.
