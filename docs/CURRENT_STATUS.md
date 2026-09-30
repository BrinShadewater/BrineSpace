# BrineSpace current status

September 29 owner large-room corrections: fixed south-facing centerpieces, capped/aligned risers and corners, thicker low doors without backing blocks, rebuilt Moonbay pressure chamber/rear grated airlock and working helmet locker, and enclosed Tidal grating/feed pipe with fill-then-spin operation. All focused checks pass, 16 native station rotations reviewed and four cards rebaked. Real profile fingerprint unchanged. See [revision handoff](LARGE_ROOM_REVISIONS_2026-09-29.md). Restart the game/editor to load; owner hands-on acceptance remains open.


September 29 large rooms installed in main: the four 2×2 rooms are available in the main project's Layout Editor and normal-run rare-card pool, including paid construction, rotated ports, saved prop overlays and Moonbay missions. Existing character/UI working edits were merged and preserved. All ten focused checks pass on the combined main checkout; its 16 native station captures have no errors or warnings. See [main integration handoff](LARGE_ROOM_MAIN_INTEGRATION_2026-09-29.md). Restart an already-running game to load the integration. Owner hands-on acceptance remains open.

September 29 large-room native review continuation: repaired invalid local UI imports and captured all 16 large-room rotations cleanly in the station (exit 0, no errors or warnings). The review tool attaches neighbors to the rotated ports and fixes the camera after deferred recentering. Reviewed muted color, north risers, side walls, scale, upright supports and door alignment at gameplay size; no further production-art correction was indicated. See [polish handoff](LARGE_ROOM_POLISH_2026-09-29.md). Owner visual and hands-on acceptance remain open.

September 29 large-room art polish: a fresh visual-bible pass of the four assembled rooms and nine painted PNGs found one rotation inconsistency. The accepted station-prop workstations now move with each large room but retain their upright top-down facing; the large centerpiece still rotates. Their crew blockers and Studio fixed bounds use the same transformed positions. All 16 raised-wall and 16 low-wall rotations were reviewed after the change. The four selected 0° cards are pixel-identical to the prior cards; no source PNG or palette changed. Focused art, Studio and integration tests pass, and scratch Godot runs left the real profile fingerprint unchanged. See [polish handoff](LARGE_ROOM_POLISH_2026-09-29.md). Owner visual acceptance remains open.

September 29 large-room Studio integration: Hydroponics Farm, Storage Depot, Moonbay and Tidal Power Plant now appear in the Layout Studio as 2×2 previews in all rotations. Their painted shell and large equipment remain fixed; station props placed in the Studio save per rotation and render in live rooms with crew navigation blockers. The large-room view has its own door/ocean clearance guides and constrained-placement checks. The focused native Studio check and existing large-room integration and Studio regression checks pass; four native Studio captures were reviewed. Character, floor, wall, light and effect authoring controls are unavailable for these large rooms; owner hands-on and visual acceptance remain open. See [Studio handoff](LARGE_ROOM_STUDIO_HANDOFF_2026-09-29.md).

## Large rooms design — September 28, 2026

September 29 reserved-space paid-run continuation: with fresh unlocks, seed 9021 and no granted resources or cards, the automated builder reserved a legal 2×2 footprint at run start. Hydroponics Farm appeared and was ordered at cycle 19, then finished at cycle 21. In the Moonbay introduction, a Salvage Workshop bought from the actual hand supplied the missing Rare Mineral; Moonbay was ordered at cycle 48 and finished at cycle 51. Bill completed a distant Survey from cycle 55 to 64 in 189.2 simulated seconds, including boarding and travel. This establishes one normal-economy path for both rooms, not general ease or final mission pacing. See [paid-run playtest](LARGE_ROOM_PAID_RUN_PLAYTEST_2026-09-29.md). No runtime costs changed; owner visual and hands-on balance acceptance remain open.

September 29 paid-run pacing probe: corrected the automated balance harness so it does not draft twice, can select a specific first-four large-room introduction, and retains a seen rare card while cycling other cards. In seed 4404, Farm and Moonbay each appeared at cycle 23 after eleven paid orders; neither became affordable in the measured run. With deliberate saving, Farm remained 3 Metal short at cycle 60. In seed 9021, Farm appeared at cycle 29, was affordable at cycle 39, but no connected clear 2×2 footprint was found through cycle 50. These are bounded automated-policy findings, not a human balance verdict; no gameplay prices or mission rates changed. See [paid-run playtest](LARGE_ROOM_PAID_RUN_PLAYTEST_2026-09-29.md). Owner visual acceptance and a human paid-run balance review remain open.

September 29 floor-mark cleanup: the solid-color dots, bars, corner brackets, and loose blocks in all four large rooms were decorative code-drawn accents, not reserved prop slots or gameplay indicators. They have been removed. Existing department floor textures, fixed equipment, painted bay rails, structural hull, and actual mission water remain. Four selected cards were rebaked; all 16 Walls-on and 16 Walls-off rotations, native station views and Moonbay launch were reviewed. Art and Moonbay mission tests pass 2/2 under scratch `APPDATA`; real save-folder fingerprints match before and after.

September 29 visual-bible audit: all eight new painted source assets and the four assembled rooms were checked at source, card, rotation and native station scale. Pixel density, focal scale and perspective are sound at current display sizes. The [focused audit](LARGE_ROOM_VISUAL_AUDIT_2026-09-29.md) records three visible material/color corrections: Tidal's flat ocean-face block, Moonbay's schematic bay rails/trim, and Hydroponics's broad green deck wash. No art changed in that review; owner visual acceptance remains open.

September 29 visual corrections: Tidal now has a painted slatted ocean intake instead of the blue block, Moonbay's bay rails and gate trim use painted hull material, and Hydroponics has a neutral gray-green deck. The new intake is normalized to the wall-art pixel density and fitted separately to north riser and low-wall views. Three selected cards were rebaked; 16 Walls-on and 16 Walls-off rotations, four native station views, and Moonbay mission states were reviewed. Five focused tests passed, followed by a targeted art pass after the final intake crop. Owner visual acceptance remains open.

September 29 interior pass: fixed supporting work areas now surround each centerpiece: crop service, cargo handling, sub maintenance and boarding, and turbine service. Accepted station props retain their native muted colors and block crew navigation at their floor footprints. All four doors remain connected in every rotation. The four cards were rebaked; native station and Moonbay mission captures were reviewed. Owner visual acceptance remains open.

September 29 floor pass: the flat placeholder grid has been replaced with muted department material in all four large rooms, plus flush drains, load-bay marks, Moonbay anti-slip/boarding marks, and turbine service grates. Moonbay remains dry until its existing mission phase floods the launch chamber. The 16 raised-wall and 16 Walls-off rotations, four native station rooms, and eight Moonbay mission phases were reviewed; five focused tests pass. The selected cards were rebaked. Owner visual acceptance remains open.

September 29 door and riser correction: the north riser now has a broad top cap and short side-wall returns at both ends. Large-room station ports use the current painted department door skins instead of the temporary diagram openings; connected door leaves follow the crew door frame. Moonbay's two existing inner pressure gates remain, and its outer ocean opening now shows the current ocean-hatch artwork, closed at rest and open during launch. All 32 Walls-on/off rotation views, four station captures and eight Moonbay mission views were reviewed. Owner visual acceptance remains open.

Further door review found that the layered-door pass could paint a second door at a connection shared with a large room. The large-room view now owns that seam. Sixteen fully open door rotation frames, fresh station captures, the paid Moonbay walkthrough, and five focused tests pass; the gate artwork and route geometry are unchanged.

Owner accepted four 2×2 rare rooms with fixed large props: Hydroponics Farm (green), Storage Depot (yellow), Moonbay (cyan), and Tidal Power Plant (yellow). The [written design](superpowers/specs/2026-09-28-large-rooms-design.md) governs behavior. Implementation is on `codex/large-rooms`: all four room views, higher costs, aligned footprint doors, ocean-facing checks, and one later rare card per run are in place. The first four new runs introduce Farm, Depot, Moonbay, and Plant in order; later runs choose randomly. Moonbay offers crew-assigned Survey, Recover and Deep Access mini-sub missions, a dry interlocked launch chamber, at-sea movement, hazard return, repair, and Save/Continue. Painted fixed grow beds, cargo gantry, mini-sub and tidal turbine now have screen-north risers, top-down walls on the other sides, and fixed wall-bank art. Moonbay has an enclosed dry sub bay with two larger stateful pressure doors; the in-room sub fits through them. Pixel density, scale, perspective and style were checked against the visual bible; a later pass muted the new room sprites and physical accents while preserving category UI colors; Storage Depot received a further dull-ochre reduction in [the wall audit](LARGE_ROOM_WALL_AUDIT_2026-09-28.md). Cards were rebaked; native station, mission, all four rotation and Walls-off views were inspected. Owner visual acceptance is pending. The paid native walkthrough and focused/regression tests pass. See [large rooms handoff](LARGE_ROOMS_HANDOFF_2026-09-28.md) for results, visual evidence, and remaining tuning.

Updated September 26, 2026 — station props v2 is merged into `main`. **Read
[station props v2](STATION_PROPS_V2_2026-09-25.md) first**: the
room art, departments, Studio tray, cards and tests changed, and parts of the
September 24 notes below (bought props, protected-room rules, bunk profiles) are
superseded by it. The owner's saved Studio layouts now define every room.

Start with [the detailed Claude handoff](CLAUDE_HANDOFF_2026-09-24.md) and
[asset pipeline/workflow](ASSET_PIPELINE_AND_WORKFLOW.md). The previous full status
is preserved unchanged in [dated history](CURRENT_STATUS_HISTORY_2026-09-24.md).
Historical test counts and TODOs apply only to their recorded revision. The broad
polish/stability goal remains unfinished; session closure is not game acceptance.

## Current checkout and direction

Use this local checkout: `C:/Users/Alex/Documents/Brine Space`. At closeout intake,
branch `main`, HEAD `f380c42c046de276b0efe26364e7596ca2410ec7`, with 3,058 local
status entries. No commit, push, publication or new export was made for closeout.
A fresh clone will not reproduce the dirty files, ignored vendor originals or
owner user-data layouts. The handoff explains the transfer requirements.

Normal gameplay retains paid construction, resource failures, hidden discoveries,
three-cycle stabilization, Archived Data purchases and Conclude Expedition.
Doctrines, deadlines and scenario victory remain retired. No broad main.gd refactor.
Local deterministic pixel editing is authorized; no Higgsfield without a fresh
explicit request. Preserve source art, script UIDs, owner saves and test packages.

The latest style discussion, **Explore Graveyard Keeper 2 Style**, asks about that
reference's graphics/camera/art. Its recent message bodies were unavailable from
the task reader. Recover the discussion before treating a proposed camera change
as accepted. The installed top-down/inward-facing and bought-prop contracts remain
the documented baseline, with owner motion and whole-game appearance review open.

## Performance, Studio tools and cleanup — September 27-28, 2026

Engineering session alongside the art sessions. Lag reports traced: machinery heat repainted every floor and wall each cycle (9f8e4081); the owner's walkway tileset pieces blocked crew routes, so crew now step past `library/tileset-` pieces and Marsh waits 2 s before re-searching a blocked pod route (27045d08); swimmers pass over hallway furniture once a corridor floods (7c4b06ee). Core-only startup texture memory fell from 5,984 to 3,538 MB: room views build on first use and prewarm from the hand and station (bb60bef6), card images are shared and companion packs load on first use (3e3e7340). Crew animations (~2.3 GB) wait for the crew session.

Studio: preview buttons for airlock cycles, drone launch/return, probe launch, fire and flood (4b276b94); Walls / Wall Art / Doors tray categories with a per-room `door/style` honoured live (3afe524a); one door per doorway; survey launcher is fixed artwork (5a2d908a); Cmd shortcuts on Mac; deleting a copy leaves no orphan keys. Gameplay: Parts Passage pilot committed without Logistics Spine stacking (41458eba); Cryo Chamber is shown as Cryo Lab (id unchanged). Owner approved the survey probe launcher and the five gray-metal airlock recolors.

Cleanup: 49 old builds and unreferenced pre-Sept-26 `output/` evidence (~248 GB) removed by the owner after staging; local LFS cache pruned 23 → 6.6 GB after uploading 364 local-only objects; 535 MB of unused Marsh review candidates removed (a8686d6c); desktop art moved to `Desktop/Projects/Gaming/Brine Space Art` (28c788d3); Review Candidates, retired Sept 24 tiles and the new-room concept folder discarded. Open: crew animation lazy-load, the remaining crew soak gap (5.8 vs 3.4 ms mean) and Mac pinch zoom wait for the crew session; the empty Salvage Drone Bay report never reproduced.

## Owner-finished rooms: protect every rotation

*Superseded September 25:* all 43 redesigned rooms were re-dressed with station
props and hand-laid by the owner in the Studio; their saved layouts are the owner's
work to protect. The list below applies to the pre-v2 art only.

Research Lab, Mycelium Nursery, Med Bay, Pressure Control, Crew Lounge, Mining Drone
Bay, Ore Refinery, Cryo Chamber, Listening Post, Xeno Lab, Maintenance Bay, Crew Hab,
Bio Lab, Clone Lab, Isolation Vault, Current Turbine, Biomass Digester, Heat Recovery,
Airlock, Construction Drone Bay, BRINE Core, Solar Array, Reactor, Battery Array,
Salvage Drone Bay, Gravity Loom and Tidal Condenser — **27 rooms**.

The final eight are the September 24 owner completion update. Do not reapply the
September 23 cleanup to them. Other rooms retain their first rotation; deliberately
cleared secondary rotations remain owner authoring space. Completion is owner
reported, not a new visual/navigation pass. Names, categories, favourites, retired
marks and user layouts are owner data. Back up affected keys before writes.

## Latest implemented work

- Routing and crew spikes (Sept 26), measured on the saved seed-73 47-room station
  (`expedition-73-progressed-known-recipe-final/latest.loop`; its `final.loop` is gone):
  - Swim smoothing retries keeping the search's facings, so a shortcut can no longer
    strand a graph-valid escape. The Sept 23 doorway report now escapes in ~25 ms
    (was: no escape, 153–262 ms per retry, 740 ms worst update).
  - Every crew spike was a goal choice. Smoothing shortcuts reach two rooms; the swim
    A* uses a heap (identical costs on 40 real pairs); a failed swim search skips
    proven-unreachable targets within one choice. 30 cycles: worst 389 → 143 ms,
    slow frames 11 → 5, mean 5.3 → 3.6 ms.
  - Corridor swim clearance skips sampling when the body is inside a proven floor
    rectangle: cold failing swim search 820 → 481 ms, all 23,444 link answers unchanged.
  - Swim-to-walk routing (owner approved): crew swim or walk per room, so a swimmer's
    route now plans dry rooms with the walking check (`swim_cells`, published by
    `room_flooding.advance`; no map = old swim-everywhere planning). Branforth, stuck
    in the flooded reactor because the crew hab's furniture blocks a swim outline, now
    reaches a bunk in 17 s. 30 cycles: worst frame 143 -> 115 ms, mean 3.4 ms.
  - Crew stand-offs (fresh seed-101 review run): two crew meeting in a doorway tried a
    detour from every start in the room, each a failed search (269 starts, 500 ms,
    repeated per step-aside spot: 1 s frames). One fill from the target now predicts
    reachable starts (0 mismatches vs the real search at 26 stand-offs); detour
    smoothing got the two-room reach. Stand-off frames 1,018 -> 53-79 ms.
  - The seed-101 review run (alive at cycle 173, Veld rescued) froze from cycle 29:
    mining exhausted, and the test player waited forever for metal. Test-player limit,
    at first; the rerun (test player now rerolls unaffordable cards) reached metal 0 and
    showed a **real zero-metal softlock**: once surveyed deposits are gone there is no metal
    source (orbit rewards exist in `orbit_manager.gd` but nothing calls `orbit.advance`).
    Fixed per owner choice: BRINE Core reclaims +1 Metal every 3 cycles while Metal < 2 and no
    bay can harvest (`scripts/metal_trickle.gd`), and any leaf room can be scrapped from the
    inspector for half its Metal (`scripts/room_scrap.gd`; not the core, wards, crew habs,
    occupied rooms or rooms others need to reach the core). Rerun: metal recovers to 2 and
    corridors keep extending.
  - Room completion hitch: every crew member rebuilt navigation and re-chose its goal in one
    frame (141-176 ms on the 47-room station). The main crew loop now rebuilds one crew member
    per frame (`defer_navigation_rebuild`); peak 33-64 ms.
  - `test_marsh_expedition_presentation` failed about 1 run in 3: its route clearing erased
    unidentified ("recovery") wards when the random site put one on the route, so the saved
    site was invalid and the checkpoint read fell back to its backup. It now keeps them;
    the failing seeds 1, 6 and 11 pass and 8/8 random runs pass.
    The first run's `final.loop` was deleted by a probe (restore points
    autosave at the source file); events, profile and screenshots remain.
  - Bunk: the seated frame sits on the mattress edge. Colour-matching the bunk art and
    smoothing crew sprites were tried and reverted (props v2 doc, Open).
- `test_owner_report_regressions` passed only with the owner's saved Studio layouts:
  its flooded-escape fixture started on a corner node. It now starts where the swimmer
  fits and passes with default and owner layouts. (`test_room_catalog_cards` failed once
  in a busy isolated run and passed 3/3 after; not layout-dependent.)

- Merged from `main` (Sept 25): the September 20 art-path restore, doorway
  unblocking, Isolation Vault fix, zoom limits and CI — see
  [Codex handoff Sept 20](CODEX_HANDOFF_2026-09-20.md).
- [Full-Power report](DRONE_FULL_POWER_REPORT_2026-09-24.md): seed 3862060672,
  cycle 457 had fully charged mining drones and exhausted discovered mining stock.
  Nearby surveyed piles required salvage. Inspector work/battery status now comes
  before charging totals; empty surveys correctly report depletion without wrecks.
- [Stored-Power charging](DRONE_STORED_POWER_2026-09-23.md) uses stored Power
  independently of cycle allocation, retains reserve 3 and prepaid charge, and
  respects suspension/global pause/Power-off. Focused and native checks passed.
- [Studio fixes](STUDIO_OWNER_DECORATION_FIXES_2026-09-23.md) preserve authoring,
  front/back ordering, late details and deletions; repair floor/riser/locker details;
  and defer navigation while dragging. 44 cards were refreshed. Long-session hitch
  acceptance remains open. [Deletion persistence](STUDIO_DELETION_PERSISTENCE_2026-09-23.md)
  separately covers source layouts across 188 room/rotation combinations.
- [Owner-report repairs](OWNER_BUG_REPORT_FIXES_2026-09-23.md) fix flooded doorway
  escape, repair access/air budgeting/retries and unjoinable remote meals. Native
  Reactor repair and Continue pass. [Follow-up](EXPEDITION_FIX_FOLLOWUP_2026-09-23.md)
  reduces duplicate swimmer escape searches, but warm routing still takes ~125 ms.
- [Procedural sites](PROCEDURAL_SITES_2026-09-23.md) are installed for new loops;
  legacy maps persist. Survey first sightings follow Veld → Branforth → Marsh;
  repeat encounters use a saved seeded shuffle. Three paid native openings and
  1,000 deterministic seeds pass. Long all-recovery runs are checkpoint chains,
  not uninterrupted play. [Scenery and pacing review](PROCEDURAL_SITES_OWNER_REVIEW.md)
  remains open, including provisional low-rock/timber choices.

## Character and asset state

Bill's four repaired walks, work identity, standing endpoints, fitted smaller helmet
and locker identity are installed. Branforth's selected south/north/west repair
chains and locker identity are installed. Do not redo older rejected candidates.
Veld's reviewed art remains unchanged. Marsh has maintenance actions, all swimming
starts/stops and all twelve turns in each of swimming, dry carry and loaded swim,
plus connected loaded pickups/loops and saved drainage rising poses. The real
controller pickup/turn integration defects were fixed. Missing-turn notes in older
handoffs are superseded. Full source/rebuild/native evidence is indexed in the
[previous status](CURRENT_STATUS_HISTORY_2026-09-24.md).

Bought-bunk profiles cover the reviewed unmirrored bed for all four cast; other bed
sizes/orientations are not accepted by that evidence. Life Support console contact
and interruption behavior are covered. Drone tool/chassis shear and hatch joins
have recorded repairs; keep deliberate hull occlusion. Coverage, pixel equality
and sampled playback do not establish natural motion or owner approval.

Use large/medium bought props to compose logical work areas. Preserve physical
supports, operator space and actual doorway access. Avoid accessory scatter,
blanket upscaling and shrinking furniture to manufacture clearance. Live decoration
filtering, Studio free placement and paused wall decorations are intentional.
Card-review binding gaps are not automatically bad rooms; reconcile current hashes
and later owner decoration before another art pass.

## Existing packages

Latest recorded test build: **brinespace-6600876d650b0d68**.

- Windows: `builds/BrineSpace-stability-2026-09-23/BrineSpace.exe` with its PCK.
- Mac: `builds/BrineSpace-mac-stability-2026-09-23/BrineSpace.zip`.

[Build evidence](STABILITY_TEST_BUILDS_2026-09-23.md) records exact 15,619-asset
PCK audits and actual Windows New Game/Continue/Fit/F8 and crew/pod/hatch checks.
These packages include dialogue/pod/hatch fixes but predate procedural sites and
later source fixes. No new build was made for documentation closeout.
Mac is Universal2, ad-hoc, not notarized; native Apple Silicon testing remains open.

Newer Mac-only candidate (Sept 25): **brinespace-ffebeef84bf5f143** in
`builds/BrineSpace-mac-props-v2-2026-09-25/`, built with `tools/export_macos.py` from
commit 9c179ce34 (station props v2, shaped screens, airlock shelf, four-crew bunk entry,
Mac comfort fixes). Universal 2 structure and exact PCK audit pass (15,693 assets, zero
discrepancies; log in `output/mac-release-2026-09-25/`). No matching Windows build or
actual-release gameplay check was made for it. Its Windows twin (same build ID) is
`builds/BrineSpace-props-v2-2026-09-25/`: exact PCK audit passes (15,693 assets) and the
actual-release smoke passes New Game, dialogue Continue, simulation, disk Continue, Fit, F8,
bunk-entry and station-prop decoding (`output/win-release-2026-09-25/`). The September 23
expedition checkpoint could not be continued: it had been advanced to a zero-food state.

## Next work and acceptance gaps

1. Recover the latest style discussion before choosing a camera/art conversion.
2. *Done Sept 26* (see Latest implemented work): smoothing rejection fixed, goal-choice
   spikes cut, swim-to-walk routing added. Open: the ~115 ms spike right after a load.
3. Review a normal paid source expedition through exploration, rescue, crew work,
   disk Continue and conclusion. Keep fixture and checkpoint-chain evidence distinct.
4. Obtain owner feedback on motion, scenery, room coherence and music, and native
   Mac hardware evidence. No new isolated test can substitute for these.
5. Preserve staged Research q2/Pressure Control/Listening Post findings for review;
   reconcile later owner layouts before acting. Dialogue note 17 still needs the
   offending real-session line; F8 has diagnostic trace support.
6. Address individually reproduced coarse props or long-session Studio hitches.
   Do not restart completed inspector, fan-card, helmet or turn work from old lists.

## Workflow

Follow the repository's two pipeline skills and [workflow guide](ASSET_PIPELINE_AND_WORKFLOW.md).
The [bible](BRINESPACE_VISUAL_AESTHETIC_BIBLE.md) owns art direction and
[release workflow](RELEASE_WORKFLOW.md) owns packaging. Read relevant development
notes before gameplay changes. Search scripts/rooms/tests/tools/docs/assets with
bounded paths; avoid recursive output/ scans. Preserve frozen saves and use disposable
copies for Continue/conclusion. Wait for observable startup, inspect error logs,
and run only appropriate validation. Update this summary at the next real milestone.
