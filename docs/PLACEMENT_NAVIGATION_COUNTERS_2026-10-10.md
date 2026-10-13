# Project handoff

Updated: October 10, 2026 · Project: BrineSpace · Task: placement stall attribution

## Objective and acceptance
Reduce placement stalls and sustained large-station frame time without changing
movement, simulation timing, selected art or owner data. All release gates remain open.

## Accepted decisions and constraints
Use the original installed-cache debug=false physical package, isolated profile,
disabled physical viewport input and bounded observations. No NPC/gameplay edits,
quality reductions, shared mutable graph or deferred companion updates admitted.

## Current state
Private drivers in output/renderdoc-tools-2026-10-08:
run-placement-navigation-counters.py and analyze-placement-navigation-counters.py.
Evidence: D:/bs-release-crew-cache-20261009/benchmark-input-isolation/placement-navigation-counters/.
PCK e9d3f8460270b78b8eba5d29300349f1639ebd405965223e2b88f1be1ba6d297.
Added route counters, movement medium/direction and cache revision/count to the
previous private before/after actor snapshot. Counters and geometry revision are
static/shared: repeated actor fields do not establish per-actor search attribution.

## Verification
Native release session31799 terminal0: 540 placement samples, 1x/2x/4x,
1080p RTX4070Ti; clean engine log, missing-art dictionary empty, debug=false,
input disabled. Owner fingerprint 2,938 files unchanged. No target-hardware certification.
At frame30 each speed, Branforth/Margot/River all rebuild their independent graph.

| Speed | Whole frame ms | Crew ms | Branforth update ms | Global search delta |
|---|---:|---:|---:|---:|
| 1x | 114.600 | 40.881 | 13.821 | 2 |
| 2x | 147.056 | 62.049 | 34.777 | 24 |
| 4x | 147.404 | 73.452 | 45.420 | 56 |

Cache remains 34 entries and geometry revision2 across each action: no observed
layout-cache flush. Graph sizes rise 11,454 ->11,739 ->12,024 ->12,309 points;
each added room contributes285 points. Actors are dry. Route failure counter
delta0 does not prove every internal route attempt succeeded. Existing counter
increments only cover their actual source branches. Whole-frame and nested CPU
timings are not additive. Drone uploads are zero in the action's current frame;
the 2x sampled previous frame includes a ~46MiB upload, so not every interval is
an upload-free control. No matched optimization or gameplay behavior acceptance.

## Next action
Private instrumented follow-up completed, session99864 terminal0, 540 samples;
three captured phase-end states equal the uninstrumented counter control. Evidence:
placement-navigation-timing-v2/{timing-analysis,owner,diagnostic-none}.json beside
the counter results. Owner2,938 unchanged, debug=false/input guard/engine and
missing-art checks clean. Temporary runtime override restored byte-identically.
Drivers run-placement-navigation-timing.py / analyze-placement-navigation-timing.py.
Only frozen Bill base overridden with bounded per-instance timing counters.

| Speed | Whole frame ms | Combined rebuild ms | Branforth goal ms | Branforth route ms/calls |
|---|---:|---:|---:|---:|
| 1x | 112.741 | 37.349 | 0 | 0/0 |
| 2x | 145.884 | 39.849 | 20.358 | 4.719/23 |
| 4x | 147.844 | 39.682 | 31.765 | 4.326/55 |

Goal timing includes its route calls. Route wrappers cover route_between only,
not every navigation helper. These are attribution, not a matched speedup claim.
First attempt91562 exited1 despite completing phases: empty autoload override
caused startup errors. Failed artifacts retained in placement-navigation-timing;
v2 removes that empty entry. Both owner guards clean; no failed-run acceptance.

The measured extra cost is predominantly outside route_between, so a route-query
cache is not the next justified remedy. Attribute goal candidate enumeration,
target shuffle/sort, station/clearance validation and route smoothing before
selecting an exact-order scoped cache. Preserve RNG and decision ordering.
Independent synchronous graph rebuilds remain ~40ms and need separate treatment.
Renderer remains a separate sustained-frame-budget target; full release scope open.
