Completed sampled doorway review: all forty crossing sequences and forty blocked centers inspected through native-pixel contact sheets. See crossing-review-sheets/review.json under output/production-ten for scope; standalone export remains outstanding.

Blocked-boundary follow-up: all forty incompatible adjacent-room cases reject traversal through 4,000 walker updates. Horizontal/vertical Command examples show flush shared walls; see PRODUCTION_TEN_BLOCKED_BOUNDARIES.md for remaining visual scope.

Mixed-station follow-up: all ten subjects in a fifteen-room connected layout pass at three viewports; the production walker visits every room through 303 valid transitions. See PRODUCTION_TEN_MIXED_STATION.md for exact scope and remaining visual/export gates.

Ingress-turn follow-up: fixed Command Center perimeter paths that crossed registered consoles. All 1,199,880 expanded production path samples now pass; see PRODUCTION_TEN_WALKER_PATHS.md. Forty seam captures exist, with full visual review still pending.

Walker-path follow-up: actual neighbor selection and 294,516 production path/foot samples pass across 6,400 pairings. See PRODUCTION_TEN_WALKER_PATHS.md for the initial-departure scope; turning paths and rendered sprite/seam checks remain.

Economy follow-up: forty real economy-driven supplied/depleted/suspended/restored state and frame pairs pass at 1600x900. See PRODUCTION_TEN_ECONOMY_STATES.md for exact scope; pixel seams, actors and standalone export remain separate.

Package follow-up: all ten room fixtures and the batch connection sweep pass from an external directory using the explicit PCK. See PRODUCTION_TEN_PACKAGE_SMOKE.md. Standalone export, pixel seams, production walkers and economy states remain unverified.

Batch geometry follow-up: all 6,400 room/rotation/side pairings match RoomDatabase sockets, with 294,516 compatible route samples passing. See PRODUCTION_TEN_CONNECTIONS.md; pixel seams, actors, economy and packaging remain separate outstanding gates.

Quarantine Cell follow-up: all ten requested rooms now have initial station/card integration. Batch neighbor, economy, mixed-station and packaging acceptance remains outstanding; see individual integration documents.

Command Center follow-up: initial source-v2 station/card integration verified at three viewports. Quarantine Cell remains source-only; see COMMAND_CENTER_INTEGRATION.md for evidence and remaining gates.

Crew Lounge follow-up: initial source-v2 registered station/card pass verified at three viewports. Two rooms remain source-only; see CREW_LOUNGE_INTEGRATION.md for evidence and remaining gates.

Salvage Drone Bay follow-up: initial registered station/card pass verified at three viewports. Three rooms remain source-only; see SALVAGE_DRONE_BAY_INTEGRATION.md for evidence and outstanding gates.

Mining Drone Bay follow-up: initial layered integration passes three viewport state/route checks; final card v2 reflects corrected aisle clearance. Four rooms remain source-only. See MINING_DRONE_BAY_INTEGRATION.md for evidence and outstanding gates.

# Production ten: source review

Refinery follow-up: initial station/card integration and three-size native
state/route/envelope checks are recorded in `ORE_REFINERY_INTEGRATION.md`.
Five batch identities still await registration; complete acceptance remains open.

Storage follow-up: initial registered station/card pass and three-size native
state/route evidence are recorded in `STORAGE_BAY_INTEGRATION.md`. Six batch
identities still await registration; full production acceptance remains open.

Maintenance follow-up: initial registered station/card pass and three-size native
state/route evidence are recorded in `MAINTENANCE_BAY_INTEGRATION.md`. Seven batch
identities still await registration; full production acceptance remains open.

Research follow-up: initial registered station/card pass and three-size native
state/route evidence are recorded in `RESEARCH_LAB_INTEGRATION.md`. Eight batch
identities still await registration; the full set is not accepted.

Follow-up: Battery Array now has initial station/card integration and three-size
native state/route evidence. See `BATTERY_ARRAY_INTEGRATION.md` for passed and
remaining gates. Source-stage findings below describe the initial batch audit.

September 6, 2026. All ten requested identities have individual built-in imagegen
sources in `rooms/production-ten/`. This is **generated**, not integrated status.
Original sources are immutable; Command and Lounge also have v2 corrections.
Exact prompts, reference roles, hashes, native dimensions, canonical port masks,
revision selection and known findings are in `rooms/production-ten/manifest.json`
and `correction-prompts.json`. All sources returned 1254 square, requested 1280.

## Evidence

`python tools/audit_room_source_batch.py rooms/production-ten/manifest.json output/production-ten/source-audit-v1`

The audit verified all ten identities and twelve source hashes and generated a
same-canvas-scale sheet. Each version's actual alpha counts are in audit.json.
Nine initial sources are RGB; Command v1 is RGBA. A checkerboard is painted into
Research and Refinery, not transparency. Dark backgrounds must not be removed
using a universal dark threshold. Existing cleanup tests pass (3 tests).
PNG LFS attributes were checked; nothing was staged, committed or published.

## Visual findings and required follow-up

- Battery: recognizable banks, insulated services, breaker and distribution unit.
  Register individual charge slots for operating indicators; static lenses remain
  non-emissive material. Do not invent stored-charge simulation from the picture.
- Research: specimen bench, analyzer, scanner, cabinet. Preserve scanner aperture
  as a genuine hole in its extraction mask rather than carrying floor pixels.
- Maintenance: repair tooling, tool bench, hull panel rack, diagnostic cart.
  Review the source's visible scratches against the maintained condition target.
- Storage: secured crates and shelves, cargo lift, smaller supply rack. Stored
  cargo stays still; only useful powered equipment should receive operating cues.
- Refinery: conveyors remain contained in their own machinery groups. Test full
  motion envelopes and all rotated north/south routes after registration.
- Mining: drilling ROV, servicing cradle, sealed deployment hatch, tether reel.
  Dark finish and weak cyan identification need native-size readability review.
- Salvage: gripping ROV, heavy winch, sorting bench and hatch are distinct from
  Mining. Preserve attached arms/hooks inside extraction and motion bounds.
- Lounge: v2 corrects the southeast chairs to south-facing. The L-sofa return and
  dining group still require deliberate prop registration and orientation review.
- Command: v1 has active screen content and open sockets. V2 removes screen traces
  but retains three open wall gaps. Only equipment is a candidate for adoption;
  shared engine geometry must replace the illustrated hull. Add sonar when running.
- Quarantine: empty isolated berth, dedicated filtration, observation console,
  protective equipment cabinet. Keep glass interior, berth and filtration distinct.

No source has yet passed complete silhouette extraction, collision registration,
four-rotation geometry, native lighting/operation/pause, cards or station review.
Existing game consumers remain untouched by this source batch. Full-set production
continues through those gates; source count is not completion count.
