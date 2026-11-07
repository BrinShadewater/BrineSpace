# Crew underwater expansion

In production. Scope: Major Bill, Dr. Veld and Chief Engineer Branforth.

## Current equipment coverage

Bill's first six-pose helmet-donning source is saved as
`generated/bill-equip-helmet-east-candidate-01.png`. The action reads clearly,
but its camera is too front-facing for the east endpoint. It is a motion reference,
not a packaged or integrated transition. Veld/Branforth transitions remain missing.

Ground-death helmets have 18 revised frames in the shared review and renderer.
Corrected rotated-overlay offsets restore visible faces in intermediate poses.
Composition, phase-preservation and terminal-restore tests pass. Native samples
at 400/620/3000ms retain helmets and clear nearby props at fixture positions;
see `pilot/ground-helmet-station-evidence.json`. Fittings remain provisional.

Kneel/repair/stand additionally have 54 fitted frames across all three crew,
with per-pose head offsets and inspected face openings. All three actions now
load into the renderer and shared review. Packaged and renderer dry coverage:
40 clips / 240 frames. Automated per-pose equipment-clock checks pass; native
captures now cover the action chain. Three inspected kneel/repair/stand samples
show retained helmets and readable tools without nearby prop overlap. Continuous
motion and travel clearance remain unverified; see `pilot/dry-helmet-station-evidence.json`.

Dry helmet fittings now cover idle/walk in four directions for all three crew,
Bill's four run directions, and east-facing interaction for all three: 31 clips,
186 frames. They load in the renderer and shared review. Original manifests,
source hashes, registered composition and phase-preserving equipment toggles
pass automated checks. Contact sheets are inspected; native dry playback is
not yet accepted. The interaction poses retain their hands/tools below the rim.

Water fittings cover swim/tread in four directions and east-facing water death
for all three. All artwork remains provisional. Equipped ground death,
put-on/take-off, and actual locker/environment integration remain
 unfinished. Veld and Branforth have no authored base run cycles yet.

The notes below record development history; this coverage summary supersedes
older counts and claims that dry fittings are absent from the renderer or review.

Required animation families per character:

- Four-direction swimming and stationary water treading.
- Grounded death, underwater death, and persistent terminal poses.
- Diving helmet equipment variants registered to each supported pose.
- Put-on and take-off transitions at diving lockers near personnel airlocks.

Preserve existing dry animation sources and frame pixels. New swimming frames
use torso registration and a horizontal silhouette; do not normalize horizontal
poses to the existing 74-pixel standing height. Retain a 92-pixel canvas only if
the pilot fits at matching anatomical scale. Keep body/helmet anchor metadata
separate from collision position. Asymmetric equipment forbids mirroring.

Runtime contract: flooded interiors and exterior water select swim/tread states;
dry interiors select walking. Helmets are saved equipment, obtained at a locker
before exterior departure, retained during swimming and death, and removed after
safe return. Death stops decision-making and locomotion and holds its terminal
pose. No new mortality balance or resource consumption is implied by these clips.

Current engine has indoor crew navigation and aggregate crew-loss events, but no
flooded-room state, exterior crew navigation, or diving-locker interactions.
Integration requires explicit state/interaction hooks and fixtures; art alone
does not establish those gameplay conditions.

Pilot source: `generated/branforth-swim-east.png`, generated from Branforth's
canonical concept. Not yet packaged or integrated. Full coverage remains pending.


East-swim pilots are now generated and sliced for all three characters (18 frames).
Run `python character/crew-underwater-v1/build_pilot.py --character bill` (or
`veld` / `branforth`). Each character has its own contact sheet, GIF and provisional
contract under `pilot/<character>-swim-east/`. Bounding-center registration and
width-derived scale still need anatomical calibration before runtime integration.
`coverage.json` explicitly tracks the remaining directions, states and equipment.
The shared helmet sheet is a design reference only; its front visor is opaque and
side views arrived west then east, so it cannot yet be used directly as an overlay.
The first Branforth checkerboard source is retained as rejected evidence.

Refinement: east-swim pilots now use source-hashed shoulder anchors in
`registration.json`, with head-height-derived uniform scale and clipping checks.
All 18 frames rebuild. Bill west source is saved but needs pitch refinement before
packaging: phases 3/6 tilt the whole body more than the east-facing stroke.

Grounded-death pilots: `python character/crew-underwater-v1/build_death.py`
packages all three crew into 18 binary-alpha frames with a fixed row scale, shared
floor baseline, non-looping manifests and held terminal frames. Per-character
contacts and one-shot GIF previews are under `pilot/<character>-death-ground-east/`.
These clips are not yet wired into NPC life states or reviewed in live playback.

`tests/test_crew_death_pack.gd` passes for all three characters: additive manifest
loading preserves dry textures, clocks and stride; six timed death poses play;
terminal frames hold and restore from saved playback. NPC life-state integration
and native station rendering remain outstanding. Dry Branforth pack regression
also passes after the shared player change.

The shared NPC controller now exposes idempotent `die()`, stops needs/movement/
goal selection/navigation rebuilds, and validates optional dead save state.
`test_crew_death_pack.gd` verifies terminal controller behavior for all three crew.
No mortality trigger has been connected; death rendering and disk restoration
remain to verify before this can be called integrated.

Station playback now loads the death expansion for all three actors, including
Bill's legacy animation path. `tests/test_crew_death_save.gd` passes real disk
serialization mid-death, exact-frame restoration, terminal NPC state and older
checkpoint compatibility. Native death occlusion review and mortality triggers
are not yet verified/connected.


Native death fixture: `tests/playtest_crew_death.gd` passes at 1600x900 and captures
all three actors at 0, 220, 400, 600, 800, 1100 and 3000 ms. Agent inspection of
400/3000-ms room crops finds registered floor contact and readable, distinct
bodies with no nearby machinery intersection in this maintenance-room fixture.
Evidence: `pilot/native/death/`. This is sampled native review, not exhaustive
occlusion coverage. Grounded death is available to the station renderer/controller;
no population-loss event has been assigned to a named NPC.

Underwater-death pilots now package for all three crew with
`build_pilot.py --character <bill|veld|branforth> --state death-water`.
The 18 frames have binary alpha and no clipping. Their torso pivot is (61,44),
not the dry floor pivot (46,86); station consumers must honor this metadata.
`tests/test_crew_water_death_pack.gd` passes timing, terminal hold and playback
restore checks. Station environment selection/rendering remains pending.
# Pivot integration refinement

Shared animated review: [review.html](review.html). Rebuild with
`python character/crew-underwater-v1/build_review.py` after changing a pilot or the
coverage ledger. It currently reads 13 packaged clips, compares the three crew,
and exposes missing swim/tread directions. Pause and scrub for pose comparison;
restart a death clip to inspect its one-shot ending. This is an isolated-art review,
not a station or equipment integration test.

The sprite player now transfers each manifest pivot to texture metadata, and the
shared whole-room renderer plus all three legacy crew renderers consume it.
Existing dry frames retain (46,86); water pilots use the torso anchor (61,44).
The water pack test passes for all three characters, and the station death/save
regression passes with minimum crew separation 20.61. Logs are
`pilot/water-pivot-test.log` and `pilot/death-pivot-regression.log`.
This does not yet establish flooded-room behavior or visual water acceptance.

### East-facing tread expansion

Bill, Veld and Branforth now each have six east-facing tread poses (24 base clips total). Bill revision 01 is retained as a rejected camera-turn candidate; revision 02 keeps a consistent side profile. Sources, prompts, hashed shoulder registration, frames and review media are reproducible through `build_pilot.py --character <actor> --state tread --direction east`. The station pilot loader includes these clips. `test_crew_swim_packs.gd` verifies all six stationary phases, loop and shoulder pivot for each character. Visual smoothness, helmet fits and actual station playback for these three clips remain pending.

### Dry helmet fitting coverage and provenance

All three crew now have provisional helmet fittings for idle and walk in all four
cardinal directions: 24 clips, 144 frames. `fit_dry_helmet.py` preserves original
body frames, timing, loop flags and pivots. Front, east, west and rear use their
own overlay views; fitting offsets vary by character. East/west walk contact
sheets retain visible faces; the rear shell covers the head consistently across
six phases. These are isolated contact-sheet observations, not station acceptance.

`check_pilots.py` now verifies every dry fitting against the original manifest,
original frame hashes, overlay hash and exact registered composition. Preserve
this chain when adding actions: a successful rebuild alone does not establish
correct head tracking. Review each pose for visor alignment and limb occlusion.
Dry fittings are not yet loaded into gameplay or the shared water review page.
Run/actions, equipped ground death, equip/remove motion and locker integration
remain outstanding. Do not count idle/walk coverage as complete equipment support.

The shared `build_review.py` now includes the 24 dry idle/walk fittings and their
original unequipped sources alongside the 30 water/death base clips. Both sides
use the original timing and pivot; toggling the helmet preserves the shared clock.
Original frame URLs resolve relative to the review directory, including parent
paths, rather than assuming every asset lives inside the expansion pack. The live
review page loaded with all eight idle/walk options present. Full playback and
station acceptance remain separate checks. This supersedes the earlier note that
dry fittings were absent from the shared review; gameplay loading is still pending.

Dry idle/walk helmet fittings now load in `grid_canvas.gd` for all three crew.
Bill validates these against his original dry manifest in a separate player and
merges only equipment rows into his legacy renderer; water rows and original dry
playback remain intact. Veld and Branforth load fittings into their own players.
The expanded swim-pack test checks every dry phase and unchanged clocks across
helmet toggles (24 clips). It passed, as did the real-save regression.

The save fixture needed an explicit legacy three-crew setup: current gameplay
now gates actors behind architect pod recovery. Clearing `architect_run` only in
this fixture restores its intended legacy population. Do not bypass recovery in
normal gameplay to satisfy an animation test. The passing save regression measured
20.36 minimum foot separation. Native dry helmet playback is still unreviewed;
run/actions and equipped ground death remain uncovered, and lockers are unfinished.

Bill's four original run cycles now have provisional helmet fittings (24 frames),
loaded by the dry equipment helper and included in the shared review. All four
contact sheets were inspected: face aperture remains visible in front/side views
and rear shell alignment is consistent. Dry phase/toggle tests now cover these
four additional clips and pass. Native running playback remains unreviewed.
Veld and Branforth have no run states in their authoritative base manifests;
the fitter reports MISSING BASE ANIMATION and leaves their rows empty. Never
claim a wearable state exists because the same state exists on another character.
Current dry equipment count is 28 clips / 168 frames; this is still partial
coverage, with role actions, ground death and equip/remove transitions unfinished.
