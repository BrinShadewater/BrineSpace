# Project handoff

Updated: October 11, 2026 · BrineSpace · Task: final guarded validation, in progress

## Objective and acceptance

Admit the measured circle-geometry optimization only after final guarded pixels,
matched performance and a maintained native regression check. Full release gates
remain open. No production admission yet.

## Accepted decisions and constraints

Enable reusable geometry only on Windows. Other platforms keep original circle
submission until native math/raster parity is established. Fallback verification
on Windows does not certify Mac gameplay. Tests remain muted, secondary-display,
isolated and disk bounded. Frozen earlier evidence remains intact.

## Current state

`D:/bs-release-crew-cache-20261009/benchmark-input-isolation/synergy-geometry-guarded/`
contains final private candidate, fixture, passing visual log and proposed native
test against original draw commands. The proposed test exercises both guard
paths; not yet installed/registered. Production Grid/Main/Bill unchanged.

`synergy-geometry-final/` contains the ongoing final three-pair-per-map comparison.
Runner/analyzer: `output/renderdoc-tools-2026-10-08/run-synergy-geometry-final.py`
and `analyze-synergy-geometry-final.py`. Actual candidate source marker and
`geometry_enabled` verify the optimized path is active. Original reference and
candidate have the same additive timing counters.

## Verification

Final guarded visual oracle: 1,152 image-byte comparisons, zero failures; both
optimized and original-rendering fallback paths. Six effects, six sizes, four
times, two directions, two origins including station-sized coordinates. Native
debug=false executable. No screenshots written. Owner 2,938 files unchanged;
visual-verifier job terminal and override restored before gameplay suite began.

First final large-map pair: synergy CPU 657.028 → 514.626 us/sample, preserving
the prior local saving. This is preliminary; full matched-state/tail analysis
and all three pairs are pending. No FPS or release acceptance claimed.

Last observed live suite handle: unified exec session `10108`, native process
`584592`. It completed large pair1 both lanes and pair2 candidate, then started
the next lane. Re-poll that handle / inspect current processes before acting;
these IDs describe an observation, not proof of future liveness. Do not restart
because a wait expires or rely only on `completed.json`. The runner restores
runtime override and fingerprints owner data in `finally` when terminal.

Last free-space check C:134.62/D:68.39 GiB, above 20 GiB floor. Final-suite traces
have not been compressed while the runner is active; compress terminal generated
reports only, with exact content hashes. No runtime/source-tree copies added.

## Next action

Observe existing session to terminal, then run final analyzer. Inspect matched
states/actions, per-pair local savings, whole-frame tails and memory before
admission. If justified, install guarded Grid with existing UID preserved,
register proposed native oracle with a newly generated UID, and run it against
the actual installed source. Keep the full PC/Mac/stutter/loading/memory/endurance
and original bug scope active; this optimization alone does not close it.
