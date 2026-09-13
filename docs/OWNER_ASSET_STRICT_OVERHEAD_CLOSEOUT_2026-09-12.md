# Project handoff

Updated: September 12, 2026 · Project: BrineSpace · Task: owner asset fixes

## Objective and acceptance

Close the remaining actionable room-art items from
`ROOM_ART_HANDOFF_2026-09-12.md` while preserving the gameplay and character
animation sessions' scope. It records agent visual review, not owner acceptance or
a packaged release.

## Accepted decisions and constraints

Existing room placements and collision frames remain authoritative. The incomplete
owner sentence “The wall length mining drone bay” is not interpreted beyond the
global camera/style contract. Construction keeps its recognizable drone silhouette;
native review supported a material repair rather than a shape redesign.

## Current state

Five live families now derive north, east, south and west from the strongest
selected south overhead source through exact raster and registration quarter turns:

- Medical Treatment uses the blue-upholstery south bank. The large treatment bed,
  supplies and service controls keep one inventory and face inward on every wall.
- Mycelium Cultivation uses the populated south bank. Three cultivation groups and
  its turquoise reservoir remain readable without side elevations.
- Crew Lounge uses the preferred long south built-in. Four seats and both plant/end
  tables rotate as one low overhead installation.
- Mining Drone Service uses the matte graphite, blue and restrained yellow south
  bank. Its service robot, four lockers and tool board retain one style and inventory.
  This satisfies the global camera/style requirement without inventing a meaning for
  the owner's incomplete “The wall length mining drone bay” sentence.
- Research Analysis uses the preferred south bank. Two work chairs, analysis surface,
  sample controls and monitor keep one overhead composition through all walls.

The derived sources, original registration backups and hashes live in
`assets/owner-strict-overhead-v1`; `tools/build_owner_strict_overhead_families.py`
reproduces the 20 selected directions. Existing room placements and collision
frames remain authoritative. Selected q0 cards were refreshed for all five rooms.

### Alignment and retained repairs

Both BRINE corner installations move from y=-210 to y=-204 in all four room
quarters. Native before/after review shows the north arms seated lower against the
corner panels while keeping their scale, wall ownership and central chamber
clearance. `test_brine_room_v2` still passes four rotations, 16 door entries and
returns, and 3654 movement samples.

Current Quarantine q0-q3 captures were also reviewed. The corrected six-tube,
three-gauge/canister family faces inward and shows no white exterior cutout. Current
Anomaly q0-q3 captures confirm the repaired side banks are overhead/inward and the
task light remains absent. These already-selected repairs were retained.

Battery Array's last open camera issue is also closed: q0 uses shallow overhead
cell and distribution banks while q1-q3 retain their verified muted sources. See
`BATTERY_OWNER_NORTH_REPAIR_2026-09-12.md`.

Construction's shared fleet atlas remains byte-identical. Its source rectangle now
receives a runtime matte ochre/graphite transform, leaving Mining and Salvage pixels
untouched. Docked, travelling and articulated working views retain exact geometry.
Med Center q3 also moves its three independent stations against the closed north
wall, clearing the two side-door route that a final integrated layout run exposed.

## Verification

Native review:

- `output/owner-strict-overhead-audit-2026-09-12/native`
- `output/owner-strict-overhead-audit-2026-09-12/research-after`
- `output/owner-strict-overhead-audit-2026-09-12/remaining-audit`
- `output/brine-corner-alignment-2026-09-12/{before,after}`
- `output/owner-asset-completion-audit-2026-09-12/current-catalog` (47 room
  identities; 167 applicable native renders and four reviewed contact sheets)

The final targeted run is `output/test-runs/20260912-223410-headless`: 176 furnished
orientations, 20 side-wall variants and all 47 card identities pass. The BRINE room
run is `output/test-runs/20260912-220626-headless`. All 20 derived source hashes
match their registrations and their PNGs route through Git LFS. Python builders
compile, project and installed skill references match, documentation links resolve,
and `git diff --check` reports no whitespace errors.

The reconciled coverage ledger contains all 47 catalog IDs, no duplicates, all
four declared direction records, and 47 explicit current-catalog review gates with
evidence. Older per-direction stage text remains as provenance and may still say
“pending”; it does not override the later current-contract review field.

## Next action

The owner can review the current source-workspace captures and clarify the incomplete
Mining sentence if it names an additional issue beyond the completed global contract.
Cryopod motion and worn character helmets remain with the character-animation
session; power and turbine behavior remain with gameplay.
