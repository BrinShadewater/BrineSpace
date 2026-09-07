# Current-controller controlled traversal

The room fixture now has an explicit `--controlled-tour` mode. Default
needs-driven simulation and its existing all-rooms visitation assertion remain
unchanged; their recorded finite-horizon failures are not relabelled passes.

The controlled mode schedules destinations only inside the isolated test. Every
leg uses the production NPC graph, route smoothing, main update function,
movement, clearance and arrival implementation. It does not assign foot positions
after initial NPC creation, change speed, alter needs priorities, disable room
collision, or change gameplay resources to ease a route.

Evidence:

- `output/batch-two/controlled-tour-v1.log`: native PASS, all 30 arrivals and
  visited rooms, 84 reciprocal boundary transitions, 6,367 movement samples.
- `output/batch-two/windows-validation-v7/verification.json`: standalone Windows
  controlled tour PASS with identical counts, plus 20 source hashes and 40 raw
  PNG decodes. Run from an external temporary directory; binary/PCK hashes saved.
- Each step checks foot/segment clearance, reciprocal-door crossing and maximum
  distance for the controller's current 46-world-unit/second speed. Trace records
  source controller hash, initial/target feet and every sampled position per leg.
- Independent read-only trace check confirms 30 continuous legs, complete targets,
  6,367 samples and maximum step 4.600457 (within the 4.601 tolerance).
- `controlled-tour-negative-v1.log` disables the first target graph node in the
  fixture only, fails the route-exists assertion and exits 1. The negative case
  has its own log/capture directory; successful tour/export logs have no errors.
- The final exported arrival screenshot was inspected: room art, UI, environment
  and actor are present. At 20.4% station zoom it is not a close-up seam or sprite
  occlusion review. Thirty arrival captures exist; not all were visually reviewed.

Reproduce with `tools/export_room_validation.ps1`, a new output directory,
`-AdditionalManifest @('res://rooms/underwater/batch-two/export-manifest.json')`
and `-ControlledTour`. Omitting that switch retains the original behavioral test.
The export wrapper checks mode, arrival count and actual visited count separately.
Four bridge tests verify source hashes and unchanged copied assertion bodies.

Scope: one connected 30-room arrangement (20 batch rooms plus 10 trunk rooms),
scheduled destinations and actual production movement. This does not establish
all-pair/all-rotation navigation, natural needs-driven destination coverage,
interactive controls, long-run balance or release approval. The older geometric
path sweeps describe their earlier controller snapshot and remain separately scoped.
