# Body upload lifecycle handoff

Updated: October 20, 2026 · BrineSpace · Remaining large-station hitches

## Objective and acceptance

Find a body-sheet upload remedy preserving original art, sampling, animation,
complete visible drones and bounded memory. This pass establishes current
lifecycle attribution; no optimization is admitted and no runtime file changed.

## Accepted decisions and constraints

Keep prior carry storage and underwater mask retention. Do not repeat the rejected
larger-cache, prewarm, grace-window, cropped-page, allocation-reuse, indexed-renderer
or GPU-reconstruction approaches unchanged. Native tests use isolated profiles,
silent secondary-display windows and the frozen unsigned Windows candidate.

## Current state

Evidence and private scripts: `D:/bs-body-upload-20261020`.
`drone-diagnostic.gd` adds bounded metadata-only lifecycle events to the frozen
candidate's matching animation source. It retains no extra texture references
and changes no residency policy. `compare.py` mounts that overlay alongside
accepted carry storage and mask retention; runtime/member hashes are recorded.
`analyze.py` produces `analysis.json`.

The initial `diagnostic` run is invalid: transplanting the checkout animation
script omitted tablet APIs required by the frozen release. Its parse errors are
preserved and its results excluded. `lifecycle-v2` uses matching frozen source,
completes with valid=true and no captured script errors. Do not copy that whole
frozen script into the older checkout to install a future fix.

## Verification and findings

Actual debug=false Compatibility, RTX 4070 Ti, 1920×1080, mixed-large fixture;
1,080 measured idle/lighting frames across 1×/2×/4×. Fixed comparison clocks enabled.
This is an instrumented diagnostic, not an A/B performance result.

- Measured frame 476: two North/South mining body uploads, 275.625 MiB total,
  56.070 ms in texture creation; frame 134.584 ms, simulation step 2.299 ms.
- Preceding frame 475: wheel/effect uploads take 50.304 ms, frame 107.418 ms.
- Frame 625: North/South collection body/cargo burst takes 42.626 ms,
  frame 88.711 ms.

These are aligned CPU API intervals, not GPU execution measurements or an additive
whole-frame breakdown. The instrumented run does not establish a regression from
earlier, faster measurements.

Lifecycle trace includes startup/warmup as well as measured frames: 774 events,
175 cache-image calls, 163 requests, 185 upload-time evictions, 25 post-draw
evictions and 50 weak restorations. Total texture-creation time is 1,167.271 ms;
the preceding cache preparation/retirement interval totals only 15.170 ms.
Of 106 repeated uploads, all have a preceding recorded eviction; none returns
in the eviction frame. Gaps are 2 frames minimum and 46.5 median.

| Recurring sheet | Uploads | Submitted MiB | Creation ms |
|---|---:|---:|---:|
| steer-right-west | 12 | 551.25 | 107.48 |
| wheel-layer-west | 9 | 413.44 | 90.59 |
| wheel-layer-south | 8 | 367.50 | 74.09 |
| steer-right-east | 8 | 367.50 | 62.05 |
| steer-left-south | 7 | 321.56 | 60.08 |

The diagnostic helper's Dictionary.merge preserves its default `bytes` field;
the analyzer therefore recovers each incoming payload from the corresponding
cache-start record. Standard sampled upload events supply the burst payloads.
Payload totals are decoded submission accounting, not physical bus traffic.

The immediate-retirement/same-frame-reload hypothesis is not supported as the
main bottleneck. Large first-use bursts and recurring state/heading sheets are
distinct costs. Enlarging retention would repeat a rejected approach; moving the
same full-sheet work between frames requires a visual-readiness policy decision.

All 2,971 owner files hash-identical; signed ZIP size/mtime unchanged. Temporary
runtime EXE/PCK copies cleaned. Original art, production code and delivery unchanged.

## Next action

Owner explicitly chose **keep exact animation timing**. Previous-pose holds and
delayed body publication to spread uploads are ruled out, including private trials
of that tradeoff. No implementation was started.

Any next upload experiment must preserve original-coordinate sampling, complete
visible drones, readiness and animation clocks within the existing memory gates.
The trace provides attribution, not a demonstrated remedy satisfying those constraints.
