# Single-body preparation trial

Updated: October 20, 2026 · BrineSpace · Body-sheet upload hitches

## Objective and acceptance

Reduce body-upload bursts with exact animation timing and current artwork.
**No production optimization admitted.** A private preparation trial separates
uploads, but does not demonstrate a repeatable reduction in whole-station hitches.
No pose hold, delayed publication, crop, resampling or clock change was introduced.

## Accepted decisions and constraints

Owner explicitly retained exact animation timing. Preserve full original textures,
ordinary sampling and complete poses. Existing rejected larger-cache, collection
prewarm, cropped-page, allocation-reuse and indexed-renderer trials remain rejected.
This trial differs by limiting preparation to one body and, finally, one source path,
using the newer carry-storage/mask baseline and explicit memory headroom.

## Current state

Private evidence/scripts: `D:/bs-body-slot-20261020`.
`drone-trial.gd` and `grid-trial.gd` are overlays on the matching frozen Windows
candidate source, not replacement files for this checkout. `compare.py`, `pair.py`,
`repeat.py` and `analyze.py` retain the runs and identities. Ordinary source, original
art and delivery were not changed by this pass. Existing checkout changes remain.

Final trial prepares only the whole `mine-north.png` body, at most one extra
137.813 MiB decoded sheet (about 183.75 MiB in the calibrated engine counter).
It requests within 0.75 simulation seconds of arrival, keeps one temporary strong
reference, and uses a 128 MiB reserve beyond the slot under the 3,072 MiB gate.
This is a workload-tested bound, not a universal driver-VRAM guarantee.
Visible draws continue selecting their normal current frame without waiting for
the forecast. Standard loading remains available if prediction does not finish.

Important finding: mining harvest presentation faces the deposit's exposed work
side, not necessarily the travel/arrival heading. The final forecast calls the
same `UnderwaterVisibility.work_side` calculation in the grid's rendering caller.
Predicting from `DroneAnimation.sample` on the traveling record alone is insufficient.

## Verification and decision

Native debug=false Compatibility, RTX 4070 Ti, 1920×1080; each completed run measures
1,080 idle/lighting frames across 1×/2×/4×, with fixed fixture clocks and isolated saves.

Attempts retained separately:

- `candidate1`: generated-script indentation failure; stopped its verified owned
  process, excluded. Corrected script passes isolated parse checking.
- `candidate2`: one-slot/512 MiB reserve pilot; prepared East and left the target
  North/South burst intact.
- `candidate3` / `reference2`: arrival-route forecast; all six state/camera pairs
  match, but still leaves that burst intact. The presentation work-face override
  was not yet represented.
- `north1`: North-only/128 MiB reserve, still using arrival heading; zero forecast
  requests/uploads. Not evidence of a preparation benefit.
- `north2`: correct work-face forecast. North uploads earlier (25.010 ms API /
  59.980 ms frame); South alone at transition (23.511 ms / 62.130 ms).
  An automatic diagnostic capture adds one event-history entry, so five phase
  states differ from `reference3`. This pair is excluded from matched performance
  conclusions; its structural upload evidence remains useful. Do not silently
  strip the log difference: report writing also adds work.
- `reference4` / `north3`: clean final matched pair, six full saved states and
  camera pairs equal, no automatic captures. Results below.

| Final matched pair | Reference | North preparation |
|---|---:|---:|
| Mean frame, ms | 24.821 | 24.801 |
| p95, ms | 35.268 | 34.560 |
| p99, ms | 45.982 | 46.050 |
| Maximum, ms | 66.287 | 69.369 |
| Frames over 50 ms | 4 | 4 |
| Frames over 100 ms | 0 | 0 |
| Sampled peak texture, MiB | 2,760.853 | 2,760.853 |
| Sampled upload API total, ms | 591.285 | 601.832 |

Final candidate requests twice and prepares one North body. Its prepared frame
costs 47.466 ms (22.739 ms upload); South costs 49.107 ms (15.779 ms upload).
In this clean reference, worker completion naturally splits South and North into
separate 49.024/49.052 ms frames already. Matching gameplay state does not make
asynchronous asset readiness identical. Thus this pair cannot establish removal
of a simultaneous-body stall, and its unchanged hitch count does not justify
production complexity. No 60 FPS phase passes.

Do not pool earlier pilots, the report-affected pair and the clean pair into an
optimization claim. API intervals are CPU wall time, not completed GPU work.
No new native visual/lifetime acceptance suite was run after the performance
result failed to justify admission. In particular, the prototype's strong slot
would need explicit `SessionArtCache` release integration before any future
installation; the root-exit hook alone is insufficient for menu/session changes.

All 2,971 owner files hash-identical; signed ZIP size/mtime unchanged.
Temporary EXE/PCK copies removed; original delivery retained. Final free space:
C 23.16 GiB, D 26.01 GiB. Guard: `final-guard.json`.

## Next action

Keep this prototype private. Do not repeat the same prewarming variants unchanged.
A future body-upload experiment needs both controlled readiness attribution and
natural station validation: fixed gameplay state alone does not force the same
worker-completion/upload grouping. The final clean runs' largest aligned bursts
are wheel/effect layers, while other observed long frames have no sampled drone
uploads. Exact timing and original artwork remain mandatory; the body hitch
problem is not declared fixed.
