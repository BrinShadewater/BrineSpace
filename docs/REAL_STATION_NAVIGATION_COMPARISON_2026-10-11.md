# Project handoff

Updated: October 11, 2026 · Project: BrineSpace · Task: verify navigation lookup retention on real stations

## Objective and acceptance

Verify the small retained point-map optimization on the reported station and the
owner's current station, with matched actions and exact state. Full PC/Mac release
gates remain open. A large-fixture benefit alone does not establish broad acceptance.

## Accepted decisions and constraints

Muted secondary-display debug=false executable, isolated profiles, owner folder
fingerprints. Three alternating pairs per station; lighting, connected placement
and successful demolition at 1x/2x/4x. No screenshots or full runtime copies.
Keep exact full state, cameras, action success, gameplay and visual behavior.

## Current state

**Withdrawn the retained point-map optimization.** Replaced only the measured
candidate bill_npc.gd bytes with its frozen reference after verifying candidate
identity and the small diff. Restored SHA256:
62ca5765aa3e433aa1ff2b9083ddf1610cac33f6dac2d6146b47f370f4ade0dd.
Earlier grid zoom scheduling remains byte-identical to its accepted candidate:
e4bdb79b4413bfdd21f4b0c3c9af51a8c8835cb158e8254d8cbb98d33fe966cf.
No broad source reset. Maintained tests/test_navigation_prefix.gd retains useful
ordered lookup and staged rebuild coverage; paired UID unchanged.

Initial cross-map batch did not achieve exact parity: four phase differences were
mining-bay warning timing/order, with all other state paths and cameras identical.
drone_idle_alert.gd throttles that read-only warning with wall-clock time. V2 uses
visual simulation seconds for that clock in a test-only overlay in both lanes,
guarded at runtime. Production warning behavior unchanged; full equality required,
no fields ignored. Initial v2 overlay type error was corrected with explicit float;
the errored run was excluded. Initial results are not accepted as parity evidence.

## Verification

V2: twelve native runs, 19440 frames, 54 exact full phase states/cameras and 90
paired successful action events. Runtime source guards verify reference/candidate
and deterministic warning clock. Logs clean, safe-image failures empty, actual
display rendering enabled. Tested RTX 4070 Ti at 1080p, not target GTX1650 or M1.
Fixture input is disabled and simulation is stepped at 1/60; this is workload
acceptance, not physical mouse/keyboard, normal title/Continue or cold/warm loading
certification. Free building/failure disabling remain fixture-only.

| Metric (ms unless stated) | Reported before | Trial | Current before | Trial |
|---|---:|---:|---:|---:|
| Mean |12.646|12.588|12.512|12.601|
| p95 |18.323|18.441|18.509|18.411|
| p99 |21.007|21.457|30.288|29.829|
| Maximum |55.736|54.279|49.196|50.223|
| >50 frames |7|8|0|1|
| >100 frames |0|0|0|0|
| 18 structural-event crew mean |13.444|14.072|14.006|14.630|
| Texture peak MiB |1559.522|1559.522|1940.818|1940.818|

Reported whole mean improves 0.45%, with only two of three pairs better. Current
whole mean worsens 0.71%, all three pairs worse. Structural-event crew mean worsens
4.67% reported and 4.45% current. Earlier large-fixture improvements do not transfer
consistently. Withdraw this trial, preserving the accepted zoom optimization.
Both maps fail p95 release gate; current also fails p99. Memory remains unchanged.

All 15 reported >50 frames across both lanes occur at demolition frame30, with zero
sampled drone uploads. Largest reference frame55.736ms includes action17.510ms,
step12.437ms (crew12.055), grid draw15.392ms. The single current trial >50 frame
is placement frame30:50.223ms, step23.414ms (crew23.011), grid18.204ms, zero sampled
uploads. These are measured rebuild/redraw stalls; absence of uploads applies only
to these frames, not the entire game.

Staged navigation: both frozen lanes passed 110 checks, 127892 point records and
984 routes in the debug=false executable/headless. Tests observe actual yields,
bound partial points lookup, require no staged prefix retention, and compare final
ordered graphs/maps/routes with fresh assembly. Restored source exactly matches
the reference already tested and rendered in all six v2 reference runs.

Owner fingerprint2938 files before/after, zero changes. All processes terminal,
runtime override restored. Initial twelve traces compressed37935658→14389248
bytes; v2 twelve traces37898403→14360576 bytes. Every content SHA verified before
and after. No owner/runtime compression or deletion. Free C134.86/D68.84GiB.

Evidence: D:/bs-release-crew-cache-20261009/benchmark-input-isolation/
retained-point-map-other-maps-v2/comparison.json, reports, source identities and
owner.json. Initial mismatches in retained-point-map-other-maps/parity-differences.json.
Staged evidence in retained-point-map-staged. Runners/analyzers in
output/renderdoc-tools-2026-10-08/*retained-point-map-other-maps-v2.py.

## Next action

Attribute James goal preparation/sorting using the restored source and runtime
guards. The prepared goal-target-sort diagnostic was based on the withdrawn trial:
regenerate it before running. Measure candidate gathering, station claims,
target sorting and routes without changing RNG draws/order or crew decisions.
Structural drawing and recurring image uploads remain separate targets. Keep full
endurance, bugs/UI, save transitions, packaged Windows/M1 and signing gates open.
