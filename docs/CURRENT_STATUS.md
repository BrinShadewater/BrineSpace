# BrineSpace current status

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
    not a game softlock. Its `final.loop` was deleted by a probe (restore points
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
