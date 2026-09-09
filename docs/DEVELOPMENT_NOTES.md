The fourteen-room wall rollout is complete in the local checkout. Current acceptance: [full report](WALL_ROOM_ROLLOUT_ACCEPTANCE_2026-09-08.md). Earlier incremental statuses below are historical.

The [fourteen-room wall-art rollout](WALL_ROOM_ROLLOUT_2026-09-08.md) has all fourteen rooms integrated with individual native placement and crew checks; the full-set completion audit remains active. Its ledger tracks per-room source, runtime and verification stages.

The [September 8 additional full-wall batch](FULL_WALL_EXPANSION_2026-09-08.md) adds darker inward-facing installations for Tidal Condenser, Biodome and Thermal Power Control, including side views and required south-wall banks. Native placement, floor details and crew routes pass.

The [September 8 inward-facing side-wall revision](SIDE_WALL_INWARD_2026-09-08.md) supersedes the first six new vertical pairs with inward operator interfaces and slightly darker palettes. Native and crew-route checks pass.

The [September 8 side-wall completion](SIDE_WALL_COMPLETION_2026-09-08.md) adds the six missing east/west full-wall pairs, bringing all 15 installations to directional source coverage. Native default-layout and crew-route checks pass; personal-draft limits are recorded there.

The [September 8 placeholder floor cleanup](PLACEHOLDER_FLOOR_CLEANUP_2026-09-08.md) removes legacy route paint and procedural decorative overlays from live rooms and refreshes all 43 cards with the finished artwork. Native evidence and remaining detail-placement issues are recorded there.

The [September 8 BRINE renewal](BRINE_ROOM_RENEWAL_2026-09-08.md) keeps New Loop and Continue centered on BRINE, but supersedes the awake-start decision: the selected architect thaws in the core pod for ten simulation seconds. Continue preserves partial progress; already-awake saves remain awake.

The [September 8 depth pass](DEPTH_PASS_2026-09-08.md) adds connected subfloors, weathered bases, cast/contact shadows, subtle underwater atmosphere and eased camera input. Native evidence and scope limits are recorded there.

# BrineSpace Development Notes

The [September 7 power-room expansion](POWER_ROOM_EXPANSION_2026-09-07.md) adds
Current Turbine, Biomass Digester and Heat Recovery Room, with muted dedicated
machinery, functioning discovery and paid construction. New loops offer a second
affordable generator immediately after the opening hand. Conditional generation,
stored fuel, rotated intake blockage, native room states and disk Save/Continue
are covered by focused checks; packaged acceptance remains separate.

Start with [current status](CURRENT_STATUS.md) for accepted direction, remaining
work and the latest recorded acceptance. The [September 6 handoff](BRINESPACE_HANDOFF_2026-09-06.md)
is a historical checkpoint. The [September 7 integrated report](INTEGRATED_BUILD_PLAYTEST_2026-09-07.md)
records a frozen debug package and bounded tests; it does not validate later edits.

## Prototype North Star

BrineSpace should feel like restoring a silent underwater station: build a little, watch the systems find their rhythm, notice a strange connection, and decide whether to risk one more room. The interesting pressure should come from the station's interlocking needs, not from click speed. The underwater bible supersedes the orbital setting; existing reboot/run systems remain prototype implementation, not settled underwater fiction.

> **BRINE // DIAGNOSTIC**
>
> *"I have mapped thirty-seven ways to run out of oxygen. I recommend none of them."* ⚠️

## Implementation notes and supporting evidence

The [September 8 flooding pass](ROOM_FLOODING_2026-09-08.md) adds continuous room
water levels, open-door flow, powered drainage and physical crew survival. It
supersedes the earlier visual-only crew limits and instant food-shortage losses.
The room inspector and diving locker expose water stages, air and tank refills;
15-second breath and 60-second tanks are the owner's rules. Other rates remain
provisional pending normal-play review.

The [September 8 character construction pass](CHARACTER_CONSTRUCTION_IMPLEMENTATION_2026-09-08.md)
supersedes the opening emergency construction drone: an available architect walks
to an existing sealed connection and welds while the new room assembles. Costs,
saved work and dedicated drone builders remain. All three architects have four
torch directions; the first pass's ten-second work duration still needs owner
pacing review.

These notes summarize successive workstreams. Their linked reports retain their
own dates and test limits; use CURRENT_STATUS.md to determine active priorities.

Diving Airlock is a buildable starting blueprint with suit lockers, a fitting
shelf, compressor, bench and a separate central pressure chamber. Its inspector sends Bill, Veld
or Branforth to fit/return their diving helmet using existing authored animation.
One fitting station reserves through crew state; power interruption, pause and
Save/Continue are supported. The chamber closes its inner door, floods and
equalizes before opening outside; returning closes the outer hatch, drains and
restores station pressure before opening inside. One derived cycle state prevents
both doors opening together. Power loss/suspension hold the cycle; saved phases
preserve water, pressure and door movement. Crew remain in the dry preparation
area; chamber transit, exterior travel and full suit changing remain future
work. See [airlock integration](../rooms/underwater/airlock-v1/README.md).

Airlock art now separates pressure-hull windows and wall fittings from floor
equipment. Ocean glazing, protected controls, valve manifold, shielded lamps,
flush drains and steel chamber framing replace the generic wall treatment.
See [hull fitting production](../rooms/underwater/airlock-v4/README.md) for source
alpha/proportion findings, current consumers and native verification limits.

BRINE Core now uses a slimmer crew-style suspended figure behind layered water,
glass reflections and the chamber's front rim. Slow floating and an occasional
single bubble replace the busy bubble field. Perimeter computer workstations and
a server cabinet retain all four door approaches and startup-pod access. See
[BRINE chamber renewal](../rooms/underwater/brine-core/renewal-v2/README.md) for
source history, native motion/route evidence and verification limits.

The open-loop operations pass adds a construction queue, ranked Station Health
priorities and a learned-pattern stabilization watch. Opening drafts stage existing
power, extraction, food, oxygen and corridor cards; paid costs and discovery rules
remain intact. Off-screen room drawing is culled with a one-cell margin. See
[Station Operations](STATION_OPERATIONS.md) for tests and measured limits.

Starting doctrine selection, timed reconstruction directives and legacy orbital
POIs are retired for now at the owner's request. New Loop begins directly with
an unlocked-only neutral blueprint deck. Runs have no directive deadline or
scenario victory; Conclude Expedition banks the loop through the existing summary.
Paid construction, resource failures, discovery stabilization and physical wreck,
rock and cryo recovery remain active. Continue clears legacy scenario/event state
while retaining the station and draft. Historic mastery remains stored but grants
no starting bonus. Older doctrine/directive balance notes below are historical.

Finite surveyed mineral deposits and scrap piles now replace abstract harvest
grounds. Stock and partial extraction persist; depleted sites become buildable.
Drones prefer exterior routes and can use matching service ports when enclosed.
The four paid opening-station economy checks survived five simulated minutes
without charge-power waits. See [Finite drone harvesting](FINITE_DRONE_HARVEST.md)
for current mechanics, native evidence and the limits of this automated playtest.

The first drone fleet pass is integrated: Mining, Salvage and Construction drones
now have separate bodies/cradles, deployment states and job effects. Paid room
orders wait for construction, and matching drones perform non-cryo clearance.
Bay harvest and clearance output return as cargo; basalt yields 4 Metal.
Mining/Salvage batteries support 12 seconds of extraction, then return to charge
from stored station Power (1 Power per 6 seconds of charge). Cuts persist across
trips; global pause freezes work and charging. Core emergency construction prevents a
first-bay deadlock. Native rotation/animation checks, gameplay regressions and an
isolated package smoke pass. See [Drone Fleet](DRONE_FLEET.md) for evidence and
prototype limits; construction/cargo pacing still needs human playtesting.

Architect recovery now seeds two fixed wards containing the two architects other
than the selected starter, one per ward. Wards support one or two occupants.
A matching-door expansion and paid repair absorb the existing room into the station.
Powered thaw sequences add named crew once, respect available berths and supplies,
and retain progress through pause and Continue. Bill, Veld and Branforth have
identity-specific six-pose emergence clips and join their matching walking NPCs
and the Crew roster only upon completion. Bill is initially selectable; rescuing
the others permanently unlocks them for the title-screen architect selector.
A single BRINE Core pod wakes the selected architect at the start of each new loop.
Legacy checkpoints retain their old population behavior. New Loop, pause-menu restart
and summary reboot now open a shared Architect selection screen. Unrescued identities
remain unknown with a cryo recovery hint; recovered records show face, name, job and
starting supplies. Bill starts with +4 Food/+4 Oxygen, Veld +6 Data/+2 Biomass,
and Branforth +6 Metal/+1 Rare Mineral. These provisional perks apply only on a
fresh loop, never on rescue or Continue. Cancel leaves the saved selection untouched.
See [architect recovery](../rooms/architect-cryo-v1/README.md) and
[the original cryo recovery record](../rooms/derelict-cryo-v1/README.md).

The [sub-biome environment pack](../assets/environment/sub-biomes-v1/README.md)
adds sulfur vent sediment, sponge reef rubble, brine salt flats, kelp meadows,
cold coral gardens, manganese nodule fields and iron seeps, with two matching props per
habitat and soft ground transitions. These are fixed visual
regions beneath the station; hazards, resources and procedural site generation
remain separate design work.

The low-growth and service-wreckage packs add fine seagrass, encrusting algae,
mussel beds and four exterior debris identities in fixed authored groups.
They remain decorative beneath construction. Environment source ledgers now
verify hashes and explicit runtime selections for these packs and the seven
sub-biomes; see [the environment library](../assets/environment/index.html).

Major Bill now has collision-aware room wandering and a basic hunger, fatigue,
exploration, and equipment-check behavior loop. Connected doors remain his travel
routes; room interiors use registered prop footprints. This is a visual NPC
prototype, without resource costs or population effects. See
[Major Bill NPC](MAJOR_BILL_NPC.md) for behavior, limits, and verification.

Dr. Veld now accompanies Bill with independent needs and science-room preferences.
Her 72-frame pack includes four-direction walking/idling, scanner use and sample
inspection. Rooms render both crew members with prop depth, and connected doors
respond to either character. This remains a visual prototype without staffing,
resource or research rewards. See [Dr. Veld](../character/dr-veld-v1/README.md).

Crew polish adds local yielding/detours so Bill and Veld maintain foot clearance
while passing. Checkpoints now retain both NPCs' needs, routes, activities and
animation clocks; older checkpoints remain compatible. Head-on corridor and
save/Continue regression tests pass. See `tests/test_crew_polish.gd`.

Chief Engineer Branforth now joins Bill and Veld with Engineering room preferences,
independent needs, diagnostic readings and equipment-service animation. His 72-frame
pack uses the shared crew playback contract. Rendering, connected doors and saves
include all three crew, and avoidance checks both peers. Three-crew headless/native
and old-save regression checks pass. See
[Branforth's pack and evidence](../character/chief-engineer-branforth-v1/README.md).
This remains visual NPC behavior without resource costs or repair rewards.

Room art now follows [the visual aesthetic bible](BRINESPACE_VISUAL_AESTHETIC_BIBLE.md).
Its department-specific finishes supersede the universal ivory/slate pilot look.
Sections 12–22 establish the underwater design and distinguish proposals from
implemented systems. Section 23 preserves south-facing machinery and flush infill for unused
door sockets, with separate migration and consumer-verification work. Do not
equate earlier technical passes with aesthetic-bible acceptance.

The previous bible is archived under `docs/archive/`. Narrow underwater corridors
now have a shared geometry pilot and station/card integration. Their downward door
collar now uses a low cutaway, with an initial registered-surface art kit. V7 native
review covers animated crossings at production character scale. Station follow-up
checks actual walker paths and complete draft thumbnails; visual owner review
remains separate. See UNDERWATER_CORRIDOR_PILOT.md.

The real station fixture also passes from a checkout-independent PCK, including
raw room images and imported card-icon dependencies. For that earlier smoke scope, see STATION_PACKAGE_SMOKE.md. The later
[integrated debug-package report](INTEGRATED_BUILD_PLAYTEST_2026-09-07.md) supersedes
the old missing-export-configuration limitation; release acceptance remains open.

The Mycelium Nursery gameplay branch is now present in the working checkout:
one locked Bio blueprint and three additional discovery patterns use the existing
paid-build, functioning-cycle and stabilization rules. Its data/deck/discovery
tests and existing regression suites pass. The layered component now draws in
the station, placement preview and card/inspector consumers. Single-room native
acceptance and a checkout-independent room-package smoke test are complete.
See `NURSERY_GAMEPLAY_INTEGRATION.md` for the requirement/evidence audit and
accepted art tradeoffs. This does not complete the broader room expansion.

## Historical prototype records

The earlier doctrine/directive balance results, old priorities and mixed prototype
limits are preserved in [the historical record](archive/DEVELOPMENT_NOTES_LEGACY_DIRECTIVES.md).
They are not a current backlog. Use [current status](CURRENT_STATUS.md) for remaining
acceptance and next work; consult an older report only for its stated revision/scope.

## Working Agreements

- Keep room definitions data-driven in `scripts/room_database.gd`.
- Keep generated Godot imports, local backups, and audit exports out of version control.
- Commit art through Git LFS. Run `git lfs install` after cloning.
- Prefer small, tested gameplay changes over broad refactors while the prototype is taking shape.

## Next session

Follow [CURRENT_STATUS.md](CURRENT_STATUS.md), starting with the outstanding human
opening-power/pacing playtest unless a later owner request changes the priority.
Do not reintroduce retired doctrines or deadlines from historical balance notes.
