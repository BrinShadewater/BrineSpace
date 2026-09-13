# Room art and playtest handoff

Updated September 12, 2026 · Brine Space · source workspace, no new export or commit.

> **September 12 completion update:** the actionable asset queue below is now
> source-complete and agent-reviewed. A fresh current-source native catalog covers
> all 47 identities and 167 applicable renders (four quarters for rotatable rooms;
> one for fixed/corridor rooms). The remaining open items are gameplay (#1–2),
> character animation/art (#6 and #9), the owner's incomplete Mining sentence
> (#11), owner visual acceptance, and packaging. See
> [the strict-overhead closeout](OWNER_ASSET_STRICT_OVERHEAD_CLOSEOUT_2026-09-12.md)
> and [the current coverage audit](ROOM_ART_CURRENT_COVERAGE_AUDIT_2026-09-12.md).

## Objective and acceptance

Continue improving every room, including missing art, while maintaining the skills, workflow and visual bible. The owner has now played the game and Studio: move equipment to **entirely top-down, inward-facing art**, with only restrained north perspective where rotation remains coherent. Follow [the new direction](TOP_DOWN_ART_DIRECTION_2026-09-12.md) before older dated acceptance reports.

The current session is handing off, not declaring the broad goal complete. Do not resume generation merely as part of this closeout. The next session should work from the queue below and current source, with native visual acceptance distinct from technical passes.

## Accepted decisions and constraints

- Preserve department identity, matte materials, correct scale, inward interaction edges and doorway/crew clearance.
- Owner-selected south/top-down examples govern the conversion. Older north elevations, fixed playable orientations and library-only companions are not sufficient final solutions.
- Observation portholes belong to the background wall/riser, not movable wall furniture.
- Explicit removals are listed below. Map informal names to actual IDs before removing live/Studio references; preserve source provenance. Do not treat an unidentified item as permission to delete a similarly named functional room.
- Current source work has not been committed/exported by this task. Concurrent gameplay, crew, lighting and environment changes exist; preserve them. Never overwrite the checkout with an old snapshot.

## Complete owner playtest queue

Everything here is a reported problem/request, not a verified diagnosis or completed fix. The [verbatim notes](handoffs/2026-09-12-top-down/OWNER_PLAYTEST_NOTES.txt) preserve wording and incomplete entries.

### Gameplay, startup, Studio and navigation

| Area | Requested follow-up |
|---|---|
| Power | Investigate consistently low available power and reserve power apparently not discharging as a battery. Trace production, demand, charge/discharge and UI accounting before changing balance. |
| Current Turbine | Verify directional generation/bonus when rotated, specifically west clearance with the reported correct arrow orientation. Arrow-selected wall remains authoritative; art alignment does not prove generation. |
| Initial room selection | Start with no build room selected; require the player to click a room before placing it. |
| BRINE startup | Start dark; lights turn/flicker on in a startup sequence; pod powers on last and then starts. |
| Cryopod | Improve visibly weak animation; emit freezing-cold particles on opening and make the emerging character initially slightly blue. |
| BRINE corner fixtures | Move corner-wall art slightly farther down to align with corners. |
| Airlock | North placement must show an exterior door on the north wall. Exterior door always visible. Interior door can use ordinary interior-door treatment. Add an exterior diving hatch that opens/closes on departure and return. |
| Diving helmet | Replace the low-resolution/older-looking worn helmet asset. |
| Layout Studio | Add an option for a standing/walking character in the room to judge equipment scale. |
| Main menu | Move Continue Loop preview content right, away from the central area. |
| Cables | Remove leftover decorative power cables globally, including Data Archive. Preserve actual power simulation; identify their rendering owners. |

### Room-by-room art and content

| Room / asset | Owner direction and remaining work |
|---|---|
| Medical treatment wall (`med_bay` family) | All views top-down/inward. Side treatment wall is nice, but orange bed must become matching blue. |
| Mycelium Nursery | South side cultivation style preferred; use top-down across walls. |
| Crew Lounge | South built-in preferred, including for north-wall direction. |
| Drone service wall | Style differs from game/drone and colors differ from room contents. Redesign top-down/inward and match room. Resolve affected drone-bay consumers from current catalog. |
| Mining Drone Bay | Raw note ends at “The wall length mining drone bay”. Keep unresolved; do not invent a specific complaint. Apply the global art contract and ask for the missing detail when it matters. |
| Ore Refinery | Strong overall. Reduce orange to room palette and repair white cutouts on wall/art pieces. |
| Cryo Chamber | Room okay; all wall equipment top-down/inward. Slight north perspective allowed, but tall assets fail through rotation. |
| Listening Post | Competing asset packs clash. Standardize on Side Deepwater Listening Walls style, top-down/inward. |
| Xeno Lab | Xeno Containment Wall is attractive but jumbles in different layouts. Convert to top-down/inward and verify layouts. |
| Maintenance Bay | Maintenance Repair Wall needs top-down/inward redesign; reduce bright orange. |
| Crew Hab | Berth still does not work for owner; convert to only top-down/inward variants. Recent matte side repairs are not owner acceptance of the berth solution. |
| Bio Lab | Side Bio Culture Wall South strongest; use that approach for others. |
| Clone Lab | Side Clone Growth Wall strong; other views need top-down/inward conversion. |
| Isolation Vault | Remove the unclear “Full Insolation Wall” item after identifying exact asset. Keep the room and use Side Emergency Isolation Wall South direction for all walls. Investigate out-of-place battery assets; battery test bench needs matte finish. |
| Current Turbine | Top-down; owner finds views other than north okay except bright orange. Rework north, reduce orange, and separately investigate power/rotation. |
| Solar Array | Wall-length art orange is too bright; reduce brightness to match palette. |
| Biomass Digester | Full Wall Biomass Processing Wall strong; match its green. Investigate overly dark other objects and white cutout around service bench. |
| Construction Drone Bay | Assets too metallic and stylistically mismatched. Review whether construction drone itself also needs redesign; this was a question, not settled replacement scope. |
| Hydroponics | Remove harvest stand; room otherwise strong example. |
| Tidal Condenser | Strong assets; top-down/inward conversion and wall colors matching machinery. |
| Command Center | Add matching wall variant; ensure top-down/inward equipment. |
| Shield Generator | Remove weak hull cradle asset; reduce orange on other objects. |
| Observation | Strong direction, rotation fails. Convert movable equipment top-down/inward; integrate portholes into background wall/riser. |
| Salvage Workshop | Convert top-down/inward across layouts. |
| Galley | User wrote “Gallery”; kitchen/mess-hall context maps to Galley. Kitchen looks nice but does not work; top-down/inward conversion and large mess-hall tables. |
| Cold Store | Fridge/rack scale does not work despite good appearance. Top-down/inward, blue palette, add central coolers/fridges. Frosty blue particles are a later request. |
| Research Lab | Side Research Analysis Wall South strongest; follow it for all directions. |
| Quarantine Cell | Strong overall; correct specimen-wall facing and white cutouts. |
| Data Archive | Generally okay; remove random floor power cable. |
| Anomaly Lab | East/west containment wall needs top-down/inward. Remove anomaly task light. |
| Battery Array | Reduce overly bright orange on some assets. |

All 47 catalog identities remain in scope even if absent from this table. Absence from the notes is not blanket acceptance.

## Current state and evidence

The [source selection snapshot](handoffs/2026-09-12-top-down/SOURCE_SELECTION_SNAPSHOT.json) preserves the 47-room coverage ledger, current card path inventories and hashes of 219 registration JSONs at closeout. It is a source-selection snapshot, not a build or acceptance manifest. Current source wins if hashes change.

Recent selected work includes low overhead Battery, Data Archive, Storage, Med Office and Med Center side companions; matte/idle east and west Crew Hab berths; BRINE south idle service and earlier corner/riser state work; matte Cold Store, Galley and Salvage pieces; Turbine overhead side work; directional Airlock fixtures and many earlier room variants. Exact raw outputs/prompts/registrations are retained beside each asset pack. Earlier library companions and alternate host layouts remain distinct from selected live defaults.

Latest detailed records:

- [Med Center](MED_CENTER_OVERHEAD_HANDOFF_2026-09-12.md), [Med Office](MED_OFFICE_OVERHEAD_HANDOFF_2026-09-12.md), [Crew Hab](CREW_HAB_MATTE_HANDOFF_2026-09-12.md).
- [Storage](STORAGE_SIDE_HANDOFF_2026-09-12.md), [Data Archive](ARCHIVE_SIDE_HANDOFF_2026-09-12.md), [Battery](BATTERY_SIDE_HANDOFF_2026-09-12.md).
- [BRINE](BRINE_CORNER_SIDE_HANDOFF_2026-09-12.md), [Salvage](SALVAGE_SIDE_HANDOFF_2026-09-12.md), [Galley](GALLEY_KITCHEN_SIDE_HANDOFF_2026-09-12.md), [Cold Store](COLD_STORE_SIDE_HANDOFF_2026-09-12.md), [Turbine](TURBINE_SIDE_REVISION_2026-09-12.md), [Airlock](AIRLOCK_FACING_HANDOFF_2026-09-12.md).

Shared helpers now support source-local operating screens, optional display colors, optional reading-lamp polygons, and explicit side reflection in relevant library/full-wall/split consumers. Retained animation classification is still room-specific. Do not assume a new registration field automatically reaches every draw path.

## Verification and limits

Recent per-room passes covered 176 furnished layouts, the existing 20 side-variant regression cases, relevant card binding parity across 47 identities, and native comparisons. The 20-variant suite is not a complete visual test of every newly added source. Med Center's latest run is `20260912-154703-headless`; its eight screen cases cover two displays, two walls and direct/retained rendering. Other records identify their own revisions.

No test proves owner acceptance of the new global direction. Fixed-clock operating comparisons are not actual station pause proof. Four repeated fixed-room captures are not four unique orientations. Existing BRINE station-riser evidence is specific to that renderer/revision, not every new display. No release was built by these art passes, and the owner's playtest executable/revision is unspecified.

## Next action

1. Read current status, new direction, raw notes and this queue; preserve concurrent work. Establish which source/build reproduces the reported power/reserve and turbine issues, then diagnose those gameplay issues separately from art.
2. Make the Studio character-scale option available and remove unintended initial build selection so subsequent review is easier.
3. Use an owner-preferred south/top-down exemplar to complete a full north/east/south/west room conversion, including actual rotation/layout and crew-scale review. Do not merely accumulate more side-only candidates.
4. Apply the removal/color/cutout queue, architecture exceptions and new furnishing requests while extending the consistent camera to all rooms. Record remaining work in the existing ledger instead of declaring completion from file counts.

Unresolved wording: incomplete Mining Drone Bay sentence; exact “Full Insolation Wall” item; which global cable consumers are intended; whether the construction drone should also be redesigned. Preserve those unknowns for targeted follow-up, without delaying independent work.

## Closeout checks

Documentation-only consolidation: raw attachment preserved byte-for-byte (SHA256 `eb048369d04012264a1c479dd3ca543defeaa7cc005e4accbf103cf9cadee31d`), handoff/direction links resolve, 47 current-contract review gates present, new project/installed skill contract identical and linked from both entry points. No gameplay/art generation or runtime tests were added during closeout. The initial documentation verifier needed explicit UTF-8 under Windows; the corrected check passes.

The skill sync audit still reports pre-existing differences in layered-assets.md, material-and-scale-review.md and check_source_sync.py. Only this task's new contract and precedence banners were applied to both copies; unrelated concurrent guidance was preserved. New entry points are in SKILL.md, full-wall-installations.md, layered-assets.md, material-and-scale-review.md and handoff.md. CURRENT_STATUS.md, DEVELOPMENT_NOTES.md and the visual bible received byte-preserving precedence additions.
