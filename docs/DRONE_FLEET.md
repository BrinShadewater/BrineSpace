# Drone fleet implementation

**Current follow-up:** [Finite harvesting and routes](FINITE_DRONE_HARVEST.md)
replaces the first pass's renewable sites and direct travel. Historical evidence
below describes the earlier snapshot unless explicitly updated.

First playable pass of the requested Mining, Salvage and Construction drone NPCs,
verified in Godot 4.6.1 on 2026-09-06. These are articulated 2D game assets.
The previous abstract rig remains the cryo restoration path; non-cryo clearance
now requires the matching Mining or Salvage bay and advances only while its drone
is working at the target. The existing single-clearance-job restriction and
18 seconds of actual cutting/drilling remain. Travel adds time.

Construction consumes the normal card cost when ordered, reserves the cell,
and only adds an operational room after the builder completes its work. The
Core carries an emergency construction drone to avoid a first-bay/power deadlock;
it takes 10 seconds of work. Dedicated Construction Drone Bays take 6 seconds,
cost 6 Metal and 1 Power to build, and consume 1 Power per cycle. They enter the
foundation deck. Free-build fixtures still place rooms immediately.

The fleet owns dock, launch, outbound, work, return and docking states. Each bay
owns one drone. Power loss freezes construction drones and prevents bay charging/launch; mining and salvage workers already outside use stored charge. Global pause freezes all
jobs. Work orders, cargo, position and animation clocks are checkpointed. Old
checkpoints without fleet data remain supported. Normal run failure/deadline
rules and discovery stabilization have not been disabled.

Mining and Salvage bay base output accrues each functioning cycle, is collected
at a local seabed work site, and enters storage when the drone docks. A clearance
assignment replaces harvesting. Wreck salvage retains its one-time completion
reward; basalt now yields 4 Metal. Clearance rewards travel as cargo and enter storage on docking. Local harvest grounds are a renewable
prototype, not a finite resource deposit system.

## Visual assets

`assets/drones/fleet-v1/atlas-matte-v1.png` is a generated six-object source:
three different drone bodies, empty cradle, fabrication bench and pressure hatch.
It uses the existing mining bay source only as a material/camera reference.
Two earlier transparency candidates painted checkerboards and were rejected.
The selected source has a magenta matte; `scripts/drone_art.gd` removes the key
at runtime, preserving the source bytes. It supplies thruster bubbles, drill
rotation cues, moving tool arms and welding sparks. Card PNGs are native Godot
captures of the room components. All raster paths are covered by Git LFS.

Generation source: Codex image tool, 2026-09-06. Selected raw output:
`exec-9d93e20a-9f59-4ba4-b537-0bd337677e16.png`.
Prompt: Replace the entire white/light gray checkerboard with completely flat
vivid solid MAGENTA #FF00FF. Preserve the six metal machines in their positions
and size, including steel details. Replace background holes between claws,
railings, legs and tools with the same matte. No shadows. 1536x1024.
Earlier atlas brief: three equal columns/two rows, mining ROV with central drill,
salvage ROV with two claws, orange construction ROV with assembly/welding arms;
empty cradle, fabrication bench and pressure hatch below. South-facing oblique
camera, maintained engineering steel, separate objects and no labels.

The additional stock rack is generated source `exec-a564b930-9fc8-4e24-8b2d-3ea4f03de900.png`,
1254 square. Exact selected edit/generation prompts, source dimensions and current
asset hashes are recorded in `assets/drones/fleet-v1/provenance.json`. Construction
uses `construction-bay-card-v3.png`; current Mining and Salvage card mappings use
their `*-bay-card-bounds-v4.png` assets. Earlier revisions remain preserved.

## Verification

| Requirement | Evidence |
|---|---|
| Three distinct models and animated jobs | Native `drone-work-tools-a.png` / `b.png`: drill motion, articulated claws, welding arms and sparks; each sprite changes, frozen clock renders identical pixels |
| Launch, travel, work, return, docking | `test_drone_fleet.gd`, `test_drone_lifecycle.gd`, native station sequence |
| Bay empty while away | Native docked/empty comparisons for all three bays in all four rotations |
| Correct hatch/cradle geometry | Native anchors checked against final rendered prop rectangles in all rotations |
| Mining and salvage clearance | Matching-bay requirement, arrival-gated work, pause, power loss and one-time completion in job/lifecycle and existing rock/wreck suites |
| Cargo credited on return | Mining and salvage cargo tests, including restored in-flight delivery exactly once |
| Paid room construction | Reserved cells, delayed operation, queued rotation, emergency Core builder, dedicated builder priority and checkpoint recovery |
| Construction room | Shared engineering hull; separate cradle, bench, hatch, stock rack; clear port-to-port route checked every four world units in all rotations |
| Normal rules retained | Existing synergy, discovery, polish gameplay, run balance, save, cryo, rock, wreck and scene polish suites pass |

Passing logs in `output/`: `drone-unit-final.log`, `drone-jobs-final.log`,
`drone-lifecycle-final.log`, `drone-route-final.log`, `drone-polish-final.log`,
`test_synergy_manager-drone.log`, `test_discovery_progression-drone.log`,
`test_polish_gameplay-drone.log`, `drone-run-balance-regression.log`,
`drone-save-regression.log`, `drone-cryo-final.log`, `test-wreck-drone.log`,
and `test_rock_clearance-drone.log`. Logs were checked for engine/assertion errors.
Native sequences were captured at 1280×720, 1600×900 and 2560×1440.

`output/drone-fleet-v4.pck` was run from an empty directory outside the checkout,
without a checkout resource fallback. `drone-package-v4-runtime.log` completed
the native fixture with no engine errors; its captures were visually inspected.
The sidecar records packaged file hashes. Shared workspace edits to `bill_npc.gd`,
`grid_canvas.gd` and `room_card_art.gd` continued after packaging; this evidence
certifies the package snapshot, not those later edits. Drone controller, artwork,
bay view and raster hashes match the checkout. This is an isolated PCK smoke test,
not a release export. Raw-export roots include `assets/drones`. Existing generic
Image.load export warnings remain for older room/environment loaders.

Earlier tiny station captures, incorrect rotated anchors, and incomplete package
candidates were rejected and corrected; their logs are historical failures, not
acceptance evidence. The final package also includes and passes the rotated
construction-bay circulation assertion.

## Prototype limits

Travel uses direct paths rather than obstacle routing. Local harvest sites are
renewable abstractions. Tool movement is procedural articulation of generated 2D
art, not a directional frame animation set or a 3D model library.

Construction and delayed cargo change pacing. The construction-aware policy in
`playtest_balance.gd` completed ten doctrine-pair runs with zero harness errors
and two wins (`output/drone-aware-pairs.json`). This small bot sample does not
establish balance or replace human playtesting. Normal costs, failures, deadlines
and three-cycle discovery stabilization remain intact; tuning them is separate
from this first NPC implementation.

## Extraction batteries (2026-09-06)

Mining and Salvage drones start with a charged 12-second extraction battery.
Active tools drain one second of charge per second; travel retains a separate
return reserve so workers can always reach home. At depletion they return,
recharge and resume the active clearance job without losing cuts. Construction
workers retain their previous power behavior in this pass.

Charging occurs only at a functioning bay. One stored station Power buys six
seconds of battery charge, transferred at three seconds of charge per second.
An empty battery therefore costs two Power and takes four seconds to refill.
Prepaid charge is retained, including through save/load. All bays share the
same available station reserve; charging cannot overdraw it. Bay operating
consumption remains separate. A drone waits at its bay when power is unavailable.

Basalt yields 4 Metal. Engineering/medical/habitation/hydroponics wrecks retain
12/8/6/10 Metal respectively. Both rock and wreck cargo arrive in storage at
docking, subject to storage capacity. Clearance frees the cell when work finishes.
The bay inspector reports battery percentage and recharge state.

Verification: test_drone_battery.gd covers depletion, return, interrupted-job
recovery, zero-power waiting, shared charging budget, save/load during charging,
invalid charge rejection, off-station battery use and one-time cargo. Existing
fleet, lifecycle, jobs, rock/wreck clearance and run-save suites pass. Their latest
logs use the -battery suffix under output; drone-battery-test.log contains the
focused suite. The earlier packaged visual evidence predates this behavior change.
