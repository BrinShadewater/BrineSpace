# Project handoff — current renderer / lossless drone storage

Updated: October 10, 2026 · BrineSpace · PC/Mac performance readiness

## Objective and acceptance
Reduce concurrent drone storage and transition stalls while preserving original atlas
coordinates, pixels, effective filtering, clocks, layering, gameplay and owner data.
Full release gates remain open. Previous turn progressed through peak attribution and
installed bounded report diagnostics; this turn makes measured private candidate progress.

## Accepted decisions and constraints
Muted secondary landscape display, isolated/resolved APPDATA, debug=false Windows
runtime on RTX 4070 Ti at1080p, 20GiB refusal threshold. Reuse existing source/encoded
assets and small overlays; no complete export copies, runtime/art installation or itch action.

## Current state
Adapted the already verified twenty-source indexed provider to CURRENT Grid; preserve
all accepted room, floor, terrain, monitor and crew changes. Reuse hashed trial resources
in D:/bs-release-crew-cache-20261009/indexed-drone-hotspots. Twenty original PNG hashes
match frozen encoding inputs, all53 reused resource identities verified, animation sample
function byte-for-byte identical. Current private Grid and added bounded collection
preparation are in benchmark-input-isolation/indexed-current-maps-trial.
First candidate adapter placed class_name after helper methods; could not preload Grid.
Moved declaration to the top, successful V2. A direct headless parse probe timed out at
30seconds and was terminated by subprocess; no FPS/engine-crash conclusion from that.

Indexed-only preliminary: mean27.609->28.253ms, peak3027.507->2370.132MiB. Reduced
storage but slower average. Combined indexed+collection preparation preliminary:
mean27.769ms, peak2629.426MiB, max72.251ms. Predict at most4 pending jobs across
backends; at most1 early upload/frame; one simulation second before collection;
current engine memory plus allocation checked against3GiB. These checks alone are not
proof against future required allocations: actual per-frame peak remains the gate.
Keep prepared paths recent until transition. No pixels/frames skipped or quality changes.

## Verification
Three alternating pairs per saved12 and deterministic expanded40 station, 810 measured
frames/run, 9,720total. Workloads idle, continuous pan, interior lighting at1x/2x/4x.
**No zoom action in these runs.** Reference=current accepted RGBA source; candidate=
current renderer with twenty-source indexed provider plus bounded early collection.

| Map/lane | Mean ms | p95 ms | p99 ms | Max ms | >50/>100 | Peak MiB |
|---|---:|---:|---:|---:|---:|---:|
| Saved12 reference | 15.141 | 21.059 | 23.424 | 28.101 | 0/0 | 1558.411 |
| Saved12 candidate | 15.277 | 21.617 | 24.369 | 36.132 | 0/0 | 1527.882 |
| Expanded40 reference | 27.793 | 43.904 | 52.915 | 135.260 | 38/3 | 3027.507 |
| Expanded40 candidate | 28.112 | 45.088 | 53.433 | 76.401 | 43/0 | 2629.426 |

Saved peak saves30.529MiB, average0.90%slower; large saves398.081MiB (13.15%),
average1.15%slower. All six candidate pair means worse; worst stalls reduced but
p95/p99 and >50count fail. NOT production admission or overall FPS improvement.
Large candidates each8prediction requests/uploads, zero budget skips; saved candidates
no prediction work. All27candidatephase snapshots/map show20sources/factory active,
no selected original duplicates, no fallback draws, complete group scan. All54 gameplay
snapshots match outside one historically variable cached Branforth playback observation
(largepair3 final4xlighting: last_time/last_position/phase/motion.started);53full exact.

Indexed-only timing suggests content callback cost lower by418us and exterior callback
by260us, but work moves into ordered child slots. Delayed viewport GPU5.496->5.790ms,
CPU7.177->7.244ms; not synchronous cause attribution and not additive with callback costs.
Need actual per-group preparation/cleanup/slot timing before an overhead remedy.

Final candidate capture inspected: UI and art visible, but much of the station sits near
bottom edge at saved zoom0.06148 and a discovery toast is present. This is NOT full-scene
visual acceptance. Matched legacy-camera comparison remains valid, but representative
station coverage is unproven. Current fixture captures each action's scroll origin from
previous action and does not restore it; pan can accumulate across speeds. Verify initial
framing and visible-room bounds, then normalize independent workloads and include explicit
zoom before using these results as any release certification. Do not edit owner camera save.

All jobs terminal/config restored. Four guards:2,938 owner files unchanged. Evidence+
scratch208.56MiB, no full PCK copies; C126.91/D78.40GiB free. Relevant artifacts:
benchmark-input-isolation/indexed-current-prewarm-maps/{comparison,snapshot-mismatches,
storage-summary}.json; per-run JSON/log/PNG and hashed pack inputs retained.

## Next action
First repair/validate benchmark framing and action isolation with bounded visibility
checks and explicit zoom. Then instrument current candidate group cleanup/preparation/
slot callbacks, reduce measured overhead and rerun representative map pairs. Keep current
candidate private until pixel/full-scene motion/filtering/flood/fallback, session lifecycle,
source binding and performance checks support admission. Mac native/signing/notarization,
release freeze, endurance, original bug coverage and all original PC/Mac gates remain open.
