# Construction access preview — October 20, 2026

Owner-approved advisory: before payment, a legally placeable blueprint shows an amber **WARNING // NO SAFE CREW ROUTE** when no present, active, living, suitably equipped dry crew member has a safe construction approach. It uses the same `CrewConstruction.approach` door/work-point/navigation checks as paid construction. Crew currently inside fire must evacuate first. Busy, resting or hungry crew are not treated as geometrically unreachable.

The floating heading becomes **CHECK BUILD ACCESS** instead of **READY TO BUILD**. Copy suggests another reachable site or restored access and explicitly says placement still spends normal materials. Desalination adds: “Emergency Water must wait until a builder can reach and finish this unit.” A powered dedicated construction drone with an exterior route instead shows **DRONE ACCESS**, with an availability caveat; busy drones can finish their earlier work. Offline, station-switch-disabled or exterior-isolated drones do not hide the warning. Ordinary illegal placement continues to show its original rejection.

## Implementation

- `scripts/construction_preview.gd` and paired UID: read-only advisory queries with one bounded current-preview cache. Cell/rotation, crew presence/state/cell/navigation signature/fire map, station switches, powered bays and exterior blockers invalidate it. Unchanged state is retried after 250 ms to account for movement within a room. Queries may populate existing navigation caches and route-search telemetry; they do not assign goals, move actors, enqueue orders, spend resources or change RNG.
- `scripts/main.gd`: one helper instance and a small addition to the existing placement status/floating feedback. No new placement gate, automatic builder policy, save field, construction rule or cost.
- Two paired-UID tests and a `construction-preview` group in `tests/index.json`.

Normal Desalination remains **5 Metal, 2 Power → 2 Water per functioning cycle**. Companion repair remains 8 Metal. A current route is advisory, not a promise of immediate work, future access or operational supply: needs, other jobs, evacuation, hardware, intake and resource rules still apply. No new emergency automation, balance change, art change, export or publication.

## Verification

Final group commands: `python tools/run_tests.py --subsystem construction-preview --timeout 240` and the same with `--native`.

- Four headless tests pass: new preview (21 checks), existing crew construction, construction break checks and inspector refresh. One render-bound test is correctly routed to native.
- Native preview passes 25 checks, including the same functional coverage and visible/clamped floating feedback at 1600×900 and 1280×720. Captures visually reviewed: [normal](../output/construction-preview-20261020/warning-1600x900.png), [compact](../output/construction-preview-20261020/warning-1280x720.png).
- Real-route controls establish an accessible site, then fire isolation; warning appears before payment, clears after fire removal, follows compatible rotations, and does not replace incompatible-door rejection. A safe alternative beside Core remains usable; another living crew member across the fire can serve the isolated side, while dead crew cannot. Powered/busy, offline, switch-disabled and exterior-blocked construction drone alternatives are covered.
- Repeated unchanged preview causes no additional route searches during its cache interval. Resources, orders, actor foot/goal/path and RNG stay equal across repeated queries. Clicking the warned Desalination site still pays exactly five Metal and queues normal work; free-building/disabled-failure flags remain off.
- All five final logs contain no engine/script errors or warnings. Final receipts: `output/test-runs/20261020-001658-headless/` and `output/test-runs/20261020-001708-native/`.

Tests use supplied room topology and controlled fire states in scratch APPDATA, not a new fresh-opening pacing study. Prior adaptive fire cohorts remain separate evidence. This does not establish human legibility acceptance, general performance, endurance, Apple validation or release-package acceptance.

TDD history retained: initial route fixture had incorrect supplied corridor rotation; corrected fixture demonstrated both warning assertions failing before implementation. Functional checks then passed. Intermediate harness issues were cache expiry during native captures and deferred music startup during headless cleanup; both were corrected without changing game music. Final logs govern.

All **2,971 real player files** hash-equal; protected existing source/art/test inputs unchanged except the intended main/test-index edits and appended direction notes. Signed Windows ZIP size/mtime unchanged. Original dirty work retained. Evidence and preservation: `output/construction-preview-20261020/`.
