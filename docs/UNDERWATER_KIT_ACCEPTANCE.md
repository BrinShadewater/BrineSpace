# Underwater corridor-kit implementation audit

Scope: the accepted follow-up to the narrow corridor test: correct the downward
collar, add character to straight/corner hulls, verify four rotations, animated
crossings, sealed ends and power-off presentation, and carry learned rules into
the bible/pipeline. Station/card integration and nursery operating effects are
also implemented. This closes that implementation pass, not the entire game's
underwater migration or every proposed room in the bible.

| Requirement | Current evidence |
|---|---|
| Narrow straight and elbow fit standard rooms | Shared corridor_geometry.gd; 384 cell, 96 lane, 128 hull, 72 socket; station v6 path test |
| Downward and side connections fit hull | corridor_parts in department_door.gd; latest native v8 four-rotation midpoint sheet inspected |
| More hull character | Generated surface samples, service pipes, white lamps, flush hatch, native reinforcing bands and grates; cards v3 and station v6 inspected |
| Details stay inside hull/clear of doors | test_corridor_detail_bounds.gd passes 388 fitting-corner samples |
| Complete door cycles and crossings | Native v8: 328 poses, four rotations, both directions; 9,216 incremental route steps; closed/sealed gates and pause checks |
| Unused connections sealed; power-off shown | v8 sealed and offline captures plus production station v6 incompatible/offline captures |
| Actual station/cards consume kit | main.gd and grid_canvas.gd use cards v3 and shared renderer; v6 verifies 1,616 production walker samples and full-thumbnail fit |
| Functioning machinery without false lighting state | nursery irrigation v4: rack-local motion, pause, real economy adequate inputs/biomass shortage/power shortage, four rotations |
| Existing gameplay preserved | Four final-effects regression logs pass without engine errors; costs and discovery rules unchanged |
| Workflow learns from results | Bible section 23, repository lessons, package/effect reports updated; installed lessons points to current project lessons; stale section reference corrected |
| Evidence matches current detail | Final native v8 rerun uses shared geometry, latest fittings and nursery effect; no engine errors |

Visual checks distinguish accepted construction from subjective final art approval.
The owner has not yet approved this latest finish; the current images are ready
for that review. The surface sampling method is documented and original/rejected
generation files remain preserved. Nothing has been published or pushed.

Additional package evidence: a checkout-independent station PCK passed with raw
room art plus imported UI icon dependencies (station-package-v2). That captured
the preceding art revision and proves its loading approach, not the latest build
or a standalone release. No release preset/template was available. Release export
remains a future distribution gate, not a completed deliverable.

Large rooms, flooded/draining rooms, wreck clearance, terrain, free-roaming crew,
the full room catalogue and orbital UI migration remain separate future work.
They are not silently implemented or certified by these corridor checks.
