# Settled room-selection repaint optimization

Updated: October 11, 2026 · Project: BrineSpace · Task: performance readiness

## Objective and acceptance

Reduce repeated room-selection stalls while preserving selected pixels, floor/wall
ordering and immediate interactive geometry during zoom settling. Keep the full
PC/Mac release plan and its failed frame gates open.

## Accepted decisions and constraints

Install this narrow change: the matched selection workload improves in all three
pairs, complete state matches and native pixel/interaction checks pass. No changes
to art, animation, simulation, effects quality or owner layouts. Preserve existing
zoom-settle selection repainting rather than deleting that dependency wholesale.

## Current state

Installed `scripts/grid_canvas.gd`: `_surface_state` retains its previous selection
key component at a settled size. Zoom preparation/reuse/settling still keys on actual
selection, so selecting an interactive room forces immediate geometry as before.
Other structural/layout/power dependencies remain unchanged.

Extended `tests/test_live_surface_retention.gd` with six checks: three settled
selection states cause no floor/wall repaint and each matches forced-rebuild pixels.
Existing immediate selection/zoom, live hatch/fire, chamber water, rotation and fit
glide checks remain. Paired UID preserved. Installed source matches accepted private
candidate text; hashes in `selection-surface-key-trial/installed-identity.json`.

## Verification

Actual Windows debug=false executable, RTX 4070 Ti, 1080p, deterministic 40 rooms;
selection through `_on_grid_clicked`, selection during zoom and lighting at 1x/2x/4x.
Six runs / three alternating pairs / 4860 measured frames / 324 verified selections.
Both lanes use fixture-only deterministic survey and notification clocks.

Combined mean 28.099→26.931 ms (-4.16%); all three pairs improve.
p95 58.145→44.436; p99 73.966→67.121; >50 ms 189→72; >100 ms 1→0.
Texture peak unchanged 3028.686 MiB. All 27 complete phase checkpoint/camera pairs
exact. This specialized workload is not an overall-game FPS or release certification.

| Workload | Mean ms, before → after | p95 ms, before → after | >50 ms, before → after |
|---|---|---|---|
| Settled selection | 26.489 → 23.710 | 58.664 → 35.812 | 81 → 3 |
| Selection during zoom | 28.330 → 27.497 | 64.183 → 57.653 | 81 → 47 |
| Lighting control | 29.477 → 29.585 | 46.041 → 46.427 | 27 → 22 |

Settled-selection floor/wall repaint counts 81→0 each; zoom-selection 81→63 each.
Lighting remains effectively neutral; no lighting gain claimed.

Actual release visual pair: 41/41 exact stabilized station crops, complete checkpoints,
camera and lighting contexts across every room selection plus clearing selection.
HUD processing hidden/frozen for these captures; lighting settled at a common final
state. This does not replace actual UI/motion acceptance. Native regression passes
after installation using the installed source and extended maintained test; immediate
zoom-settle repaint assertion unchanged, fit glide lands in 28 frames with one hold
and no simultaneous floor/wall glide repaint. Final logs have no engine errors.
First test launch was refused by the packaged profile guard because its command-line
user-dir marker was missing; added marker and subsequent runs pass with isolated data.

Evidence under `D:/bs-release-crew-cache-20261009/benchmark-input-isolation/`:
`selection-surface-workloads/{comparison.json,action-comparison.json,owner.json}`,
`selection-surface-pixels/{pixel-comparison.json,owner.json}`,
`selection-surface-key-trial/{native.log,installed-identity.json,owner.json}`.
Runners in `output/renderdoc-tools-2026-10-08/` use `selection-surface` names.

## Next action

Measure on the reported/current real-map selection workloads and check idle/pan
regression coverage before broader release claims. Existing accepted-candidate traces
show 81 click frames: mean handler work 7.253 ms, click frames 35.373 ms versus other
selection-phase frames 22.414 ms. Profile `_refresh_all` components to choose the next
UI optimization; do not guess which rebuild dominates or suppress necessary updates.
Continue larger render/upload hotspots and original bug/save/UI/endurance/platform
gates. Indexed provider remains private; no release upload authorized.

## Handoff and storage

Jobs terminal; runtime override restored. All owner guards: 2938 files, zero changes.
New evidence growth approximately 57.44 MiB (candidate directory was 0.26 MiB before
this turn; now 7.67 MiB, workloads 28.74 MiB, pixels 21.29 MiB). Existing executable,
art and base packs reused. C: 123.22 / D: 70.31 GiB free. Frame targets still fail.
