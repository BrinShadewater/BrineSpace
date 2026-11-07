# Project handoff

Updated: October 7, 2026 · Project: BrineSpace · Task: remaining Moonbay rendering attribution

## Objective and acceptance

Continue full PC/Mac performance readiness. Test whether remaining cached Moonbay water geometry is a worthwhile optimization target after accepted stroke batching. Diagnostic omissions must preserve simulation and resource endpoints; they are not accepted visual changes or obtainable savings.

## Accepted decisions and constraints

Do not implement further water aggregation on this evidence: all Moonbay water together represents only about 21 remaining calls in this workload. Preserve selected pixels, timing, effects and gameplay. Normal source unchanged. Earlier status-only turn supplied no new implementation evidence; this continuation revalidated current source and completed a concrete attribution experiment.

## Current state

Private current-source copies and isolated runner in `output/moon-components-2026-10-07/`. Only Moonbay drawing skips water, enclosure walls/corners, bay doors, or beacons in separate lanes. Full lane uses the same private copies without omission. Current normal Main/Grid/large canvas/base and Moonbay are copied; no earlier private memory provider is used. Private scene UID/class declaration removed to avoid duplicate registrations.

## Verification

Five native 1920×1080 uncapped lanes, each 60 measured idle frames at 1×/2×/4×: fifteen phases. All twelve omitted-phase full crew/drone/zoom/power/door/light comparisons equal control. All texture endpoints identical, no missing art, logged errors, warnings or leaked instances. Owner fingerprint: 2,936 files before/after, zero changes. Full and water captures inspected. Runner terminal.

At 1×, full 5,088 calls/render CPU 11.153 ms; water omitted 5,067/10.878 ms; walls 4,932/10.593 ms; doors 4,959/10.811 ms; beacons 4,986/10.550 ms. Call reductions remain approximately 21/156/129/102 at other speeds. CPU/GPU and whole-frame deltas vary; omission effects overlap and cannot be summed. Full p95 39.813/37.785/40.979 ms: frame gate fails. Idle-only chronology differs from earlier idle/pan workload; these numbers do not establish a gain over that workload.

Initial private parser mistake used `filter` directly on PackedStringArray. Exact failing PID stopped; log retained as `parse-before.log`; conversion to Array corrected. Failed run excluded. Corrected lanes all completed cleanly. No release executable, PCK, lifecycle or endurance certification in this experiment.

## Next action

Prioritize broader measured CPU preparation and animated environment costs. Current full control records live-room work 6.27 ms, environment line callback 1.26 ms, and door/light validation 1.64 ms at 1×; scopes overlap with other timings. Inspect invariant versus changing environment-line geometry and room state preparation before choosing a prototype; require actual native pixel/clock/culling checks and a matched workload gain. Continue private crew/drone provider admission, complete memory inventory, refreshed packages, original nine packaged reports, endurance and actual Windows/Mac certification. All original gates remain open.
