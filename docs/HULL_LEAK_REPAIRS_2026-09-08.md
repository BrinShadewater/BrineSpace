# Hull leak variations and physical repairs

Updated: September 8, 2026 · Project: BrineSpace

## Objective and acceptance

Owner requested varied leaks with different rates and physical crew blowtorch
repairs costing Metal. Implementation and targeted native checks complete; owner
visual/pacing acceptance pending.

## Accepted decisions and constraints

Three provisional profiles: hairline 20% severity / 0.8% room depth per second /
2 Metal / 6 seconds work; split seam 50% / 2% per second / 3 Metal / 10 seconds;
rupture 100% / 4% per second / 5 Metal / 16 seconds. Existing continuous severity
values remain compatible; bands <=35%, <=70%, >70% select art/cost/time.
Containment incidents now cycle these severities; repeat damage can worsen leaks.

Order through the room inspector. Metal is allocated once when queued. The leak
continues during travel and work, stopping on completion. Existing water remains.
Blocked jobs wait for reachable crew; deaths retain partial paid work. Normal
15/60-second air limits apply, including while repairing submerged damage.

## Current state

- New `scripts/hull_repair.gd` + UID: orders, navigation to nearby work points,
  paid work, ownership/reassignment, completion, save validation.
- `scripts/bill_npc.gd`: prioritized repair task, arrival handling and validated
  welding goal. Dry unhelmeted crew use authored weld frames; equipped/submerged
  crew use existing repair/underwater poses with a separate torch effect.
- `scripts/main.gd`, `scripts/local_incidents.gd`, `scripts/room_flooding.gd`:
  replace instantaneous hull repair with orders; inspector names/rates/cost/time,
  progress; persist and validate job data inside existing room saves.
- `scripts/flood_visuals.gd`: three crack silhouettes, severity-scaled jets,
  submerged torch/sparks. Existing authored dry torch is not drawn twice.
- `scripts/grid_canvas.gd`: repair progress excluded from structural caching.
- `tests/test_hull_repair.gd` + UID, updated flooding/rendering tests.
- Native captures: `output/hull-leak-variants.png`, `output/hull-repair-torch.png`,
  `output/hull-repair-underwater.png`.

## Verification

Flooding unit test passes. New integration/native test verifies metal allocation,
duplicate refusal, actual navigation, dry welding, pause, disk Save/Continue,
death interruption, resumed progress without second charge, stopped inflow with
remaining water, three rates, insufficient funds, corrupt progress and helmeted
critical-water work consuming oxygen. Rendering cache test passes. Existing crew
construction test passes (0 failures); its existing two-resource shutdown warning
remains. Scoped whitespace check passes. Logs: `output/hull-repair-*.log`.

## Next action

Owner review of the three profiles and torch appearance. Rates/costs are provisional.
Approaches obey existing room geometry: crowded or inaccessible work sites wait
rather than teleporting crew. No full-station performance or export claim.
