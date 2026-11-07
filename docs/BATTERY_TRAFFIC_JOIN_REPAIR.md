# Battery Array traffic graph-entry repair

The failed Biodome canopy package recorded Bill waiting near Battery Array
`(25,20)`. `tools/probe_battery_traffic.gd` reconstructs two adjacent Battery
Arrays using their real registered geometry, Bill's recorded foot
`(9614.982421875,7872)`, stationary Veld at
`(9635.5791015625,7878.26123046875)`, and destination `(9792,7872)`.
It does not reproduce the third actor, complete station or earlier trajectory.

## Reproduced mechanism

The controller's nearest clear graph join `(9616,7872)` is only 1.018 units away,
but has no route after the existing 32-unit padded peer-node exclusion. The
next safe join `(9616,7856)` is 16.032 units away and has a 12-node clear route.
The previous implementation stopped after the first entry failed, even though
the actor could safely reach another entry. This is distinct from the earlier
Lounge defect where the entry segment itself passed through a colleague.

Baseline controller hash:
`1F1E3C1923AEB6CADCB8FF03DD99F11723BD7BF4BC87700F83E2A8FAB082350A`.
`output/battery-traffic-probe-v1.log` records both entry alternatives and the
actual movement result. Without the peer Bill arrives; with the peer he does not.
The same snapshot with `--require-progress` exits 1 in `battery-traffic-red-v1`.
No parser error or collision assertion accounts for that failure.

## Narrow implementation

`detour_around_crew()` now tries safe joins nearest-first until one yields a
complete route. `crew_detour_from()` retains the existing padded node exclusion,
restoration and static/crew-clear smoothing for each attempt. It never installs
a partial route. Collision, door widths, furniture, speed, crew clearance and
traffic retry/cancellation timings remain unchanged. No artwork or saves changed.

Repaired controller hash:
`46757B6F6E6AEA6C370477CCACA46B792A176DA396406B8DA3ED3A595158F62B`.
`battery-traffic-green-v1` exits 0: both snapshot cases arrive with zero
violations. The test-only traced controller checks consumed movement legs and
their total length, rather than mistaking an endpoint chord for the traveled path.

Fresh headless regressions all exit 0 without engine/script errors:

- Bill: 140 room/rotation navigation checks.
- Crew polish: minimum observed separation 20.36.
- Branforth three-crew checks: minimum observed separation 20.36.
- Movement trace regression.
- Prior Lounge stationary-peer progress probe.

Logs use `output/battery-join-<test-name>-v1.*`. Godot generated the new probe's
paired UID during import. These checks do not establish universal crowd liveness,
full-speed visual quality, or the failed package's original three-crew history.

## Fresh Windows mixed tour

`output/batch-two/battery-join-package-v1/verification.json` records a clean
import, furnishing-host preflight, export and runtime. The external-directory
run reaches all 30 scheduled rooms, crosses 84 reciprocal door connections and
passes 6,418 swept movement/speed samples at delta 0.1. Child 0, no engine/script
errors. Twenty source hashes, 40 raw PNGs, 29 component assets and 19 composition
profiles load successfully, including the Biodome canopy v6 art.

PCK SHA-256:
`B051F87A8374EC6E56B30BAEC11975C778EA0F8457B4EA8223A8B5015C8DD755`.
EXE SHA-256:
`8515CD8041A906BDF82A3C9926125E20F642A1062CB2A45A962F3A43DFFA41ED`.
The six export-bridge consistency tests also pass against the current sources.

This scheduled-destination run exercises native rendering and production movement,
not autonomous choice or all 35 catalog identities. Its peer decisions do not
constitute an exact replay of the failed tour. The deterministic snapshot supplies
the red/green causal evidence; broader crowd liveness and continuous visual motion
review remain separate. The previous failed package is retained unchanged.
