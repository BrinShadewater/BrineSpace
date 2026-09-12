# BrineSpace current status

## Higgsfield pilot — September 12, 2026

[Pilot verdict](HIGGSFIELD_PILOT_2026-09-12.md): eight generations, 28 credits, no source-tree writes and no registrations. **GPT Image 2.5 beats Nano Banana Pro on this project's art contract** — Nano Banana Pro produced flat front elevations twice, including with an accepted asset as reference, while GPT Image 2.5 matched the shallow overhead geometry, detail density and material discipline, and returned native transparent alpha. What made it work: passing an accepted asset as an image reference, naming the geometry explicitly ("not a flat elevation"), and self-referencing for controlled revisions — which lifted the engineering bank from 101 to 120 units tall at 324 wide, against 123 for the accepted bench. Outstanding gaps: alpha is always soft and needs a binary threshold, invented iconography slips through, interior depth is shallower than the authored art, and available aspect ratios do not match authored side regions. A side-wall finding became its own [proposal](MIRRORED_SIDE_WALLS_PROPOSAL_2026-09-12.md): author one side and mirror it, since separately authored sides drift (accepted strips are 303x974 and 279x979). Owner acceptance not given; nothing adopted.

## Rebuilt release live on itch — September 12, 2026

`builds/BrineSpace-2026-09-12-main/` exported from a clean tree at `68c6cc4e` and uploaded as version `2026-09-12-main` (build `1970435`), replacing the September 11 slim build on the same `windows` channel so the existing download updates. Same 1.24 GiB package; butler sent a 794 KiB patch. Validation before upload: pack audit `checked=7780 missing=0 changed=0`, release smoke fixture `0 failures; debug=false` with no resource-loading errors, and a PCK scan confirming the owner-reference photo is not packed (its filename appears only inside a provenance JSON). Note for future rebuilds: the Windows export templates under `output/production-ten/export-tools/` had to be re-extracted from the verified `.tpz` bundle — the presets depend on files inside `output/`, which cleanup passes target.

## Workflow hardening and shared placement envelope — September 11, 2026

[Workflow handoff](WORKFLOW_HARDENING_2026-09-11.md): Track 4 completed — Codex skill copies resynced with an end-of-line-tolerant `check_source_sync.py`, character bindings extended 4 → 16 with an `installed-portraits.json` cross-check, a new art-free layout-key guard (`tests/test_layout_keys.py`) in CI, and a `push_warning` replacing the silent out-of-envelope prop reset. Studio and the live game now share one placement envelope (`RoomLayoutStore.envelope_for()` / `door_lane()`), with the live values as the truth: across 47 rooms × 4 rotations 30 placements change status, 29 of them Studio relaxing to match the game, and only constrained layouts are affected (0 of 188 authored, 1 owner layout). Three long-failing native tests were traced to owner decisions rather than regressions — dressing and common decorations stay in Studio, free placement is the Studio default, wall decorations are paused — and one real flake (`test_run_save`, a fixed wait after the Continue scene swap) was fixed and re-verified under load. Headless 112 PASS / 0 FAIL; native layout lane 7 PASS. Source and tests only; no executable rebuilt. A follow-up claim that the `battery_array/1` cells section is reset in game was withdrawn on September 12: that placement is owner-authored in free placement, where the guard does not run, and a probe confirms it survives untouched.

## Release size cut — September 11, 2026

Shipped pack 5.81 GB → 1.19 GB with no tracked file removed: raster import roles (normal / keep / skip, see [release workflow](RELEASE_WORKFLOW.md)) stop `.ctex` duplicates and unshipped sources from packing, and two manifest-crawler fixes (`swim_helmet_fit.gd` tree literal, `addons/` prefix test) drop ~1.3 GB of QA captures that were shipping to players. Manifest 11,273 → 8,108 files; empty-directory pack audit `missing=0 changed=0 remapped=8`; release smoke (title → New Game → Continue → Resume → F8) 0 failures on warm runs — the first cold launch after export raced the fixture's fixed frame counts on the two post-Continue timing checks, a fixture-hardening note rather than a game fault. Build: `builds/BrineSpace-2026-09-11-slim/`. Local `.import` sidecars rewritten (gitignored); `.godot/imported` still holds ~30k stale `.ctex` safe to clear.

## Performance pass phases 1+2 — September 11, 2026

[Performance handoff](PERFORMANCE_PASS_2026-09-11.md): phase 1 (retained environment passes, layout-store memoization, door/surface key memos, idempotent hardware panel, flooded quick wins) plus phase 2 (sorted prop-queue caching with pre-expanded stable entries; cheap identity+serial DrawSlot keys replacing per-slot deep dictionary compares). Measured on the same build via opt-out flags: **100-room fit 74.8→61.4 ms (−17.9%)**, 50-room fit −21%, save hitch −43%. All native parity gates pass — content-cache parity's 33 capture pairs verified pixel-identical with a comparator (the GD test alone does not compare pixels) — plus the new environment parity harness and the headless battery (176 preferred orientations, 47 cards, companion water). Five parity fixtures' 7-second thaws corrected to the 10-second pod duration. Dense fit still misses the 60 fps budget; the remaining headroom (render_into internals, painting, GPU) and the owner-decision options (mipmaps, atlasing) are recorded in the handoff, as is a pre-existing sub-perceptual fit-zoom capture variance in two old pixel comparators, reproduced on the unmodified code path. Source only; no executable rebuilt, no commit.

## Bug-fix session — September 10, 2026

[Bug-fix handoff](BUGFIX_SESSION_2026-09-10.md): companion water-mode hysteresis (personality starvation fix) with powerdown-exit wake, flood alerts no longer re-announce on Continue, flood-retreat re-validates its refuge mid-route, correct journal pet-refusal reasons, crew rest restored at crew hab/lounge rotation 2, rotated-door navigation walls corrected in the shared embedded-view path, MetaState fixture isolation (test_marsh_unlock now green), Josh swim-clearance guard, settings-panel crash guard, and test_bill_npc modernized to the post-thaw spawn model. Thirteen affected tests pass, including 176-orientation preferred layouts and 47 card bindings. Source only; owner behavior review pending; no executable rebuilt, no commit.

## Starting-screen facial likeness - September 9, 2026

[Title likeness handoff](TITLE_LIKENESS_2026-09-09.md): BRINE's starting-screen face revised toward the owner's supplied cover reference, preserving the body, stage and floating silhouette. Native 1600/960 layout, float and Reduced Motion checks passed; agent visual review complete. Source only; executable and itch.io build retain the prior title until the next release.

## Butler upload workflow saved - September 9, 2026

Future owner-requested Windows uploads should use the [saved Butler procedure](ITCH_UPLOAD_WORKFLOW.md). Reuse brinshadewater/brinespace:windows. First verified version: 2026-09-09-face-icon, build 1963891. Page remained Restricted; no new gameplay validation implied.

## BRINE face executable icon - September 9, 2026

[Icon handoff](APP_ICON_2026-09-09.md): current BRINE portrait assigned to the project and Windows executable. Embedded icons reviewed at native sizes; release title launch passes. Updated playable folder: builds/BrineSpace-2026-09-09-face-icon/. Gameplay unchanged from the polished build.

## Combined polish and release - September 9, 2026

[Combined handoff](FINAL_POLISH_RELEASE_2026-09-09.md): completed local art, animations and reliability work integrated; sprite failure handling, clip duration calculation and title/badge loading polished. Focused source/native checks and actual release New Game/Resume/F8 pass; 10,978 packaged assets checked with zero missing/changed. Source pushed to GitHub. Playable build: builds/BrineSpace-2026-09-09-polished/. See the handoff for package identity and remaining performance/pacing limits.

## UI, character and build session closed - September 9

[Closeout](SESSION_CLOSEOUT_UI_CHARACTERS_2026-09-09.md): accepted portrait/sidebar decisions added to the bible; character/room skill lessons and installed copies updated; [release workflow](RELEASE_WORKFLOW.md) now distinguishes editor/PCK evidence from actual release gameplay. This session has no remaining active work. Later optimized-release, animation, portrait and room entries below retain their own scope and acceptance. No new build or source-art cleanup during closeout.

## Art session closed - September 9, 2026

[Closeout](ART_SESSION_CLOSEOUT_2026-09-09.md): selected room/title assets and current dependency integration checked, runtime manifest refreshed to 11,273 files, assets and supporting work staged with verified LFS pointers. Bible and maintained/installed room-pipeline lessons updated. Current 47 card bindings pass and newer riser/animation selections are preserved. Source session closed; generated build metadata stays local, and no executable, commit or push was made by this closeout.

## Reliability session closed — September 9, 2026

[Closeout](SESSION_CLOSEOUT_RELIABILITY_2026-09-09.md) consolidates the merged teegly
fixes, local reliability/performance work and maintained pipeline lessons. The
optimized executable uses frozen bindings; newer companion water, animation and
room-art source milestones below are not jointly accepted in that build. Follow
[release delivery](RELEASE_ASSET_CONTRACT.md) for the next combined build.

## September 9 character session closed

[Character closeout](CHARACTER_SESSION_CLOSEOUT_2026-09-09.md): all completed portrait and animation selections are bound to the source game. The active registry audits nine packs (355 clips / 1,488 frame references including retained states) and eight portraits with zero errors. Visual bible, character skill/installed mirror and asset pipeline guide updated with observed lessons. Recent native water, dry action, repair and save checks remain passing. Session complete; no executable rebuild or commit/push.


## September 9 companion water behavior

[Companion water](COMPANION_WATER_2026-09-09.md): Margot swims from 20% room flooding, River floats from 25%, and Josh shuts down at 50% until water recedes. Four-direction water motion, surface rendering, route restrictions, pause and checkpoint handling are installed. Native flooded-room rescue/routing/save tests and dry-action/repair regressions pass. [Animation gallery](../character/companion-water-v1/review.html). Source only; no executable rebuilt.

## Riser session closed — September 9, 2026

Six new walls remain assigned to reactor, cryo chamber, data archive, storage bay, crew lounge and research lab, now with coordinated door finishes. Separate wall decorations are suppressed in gameplay and Studio, including the airlock; source fittings and saved placements are retained. Seven cards refreshed. [Final review](../assets/riser-session-closeout/review.html) and [handoff](RISER_SESSION_CLOSEOUT_2026-09-09.md). Native 28-rotation captures and focused wall/door checks passed; source checkout only, no executable rebuilt.


## September 9 reliability, smaller release and rendering

[Implementation and acceptance](RELIABILITY_PERFORMANCE_2026-09-09.md): safe image fallbacks, exact release IDs and live diagnostic snapshots; 30% smaller data pack; 98-room frame time improves 30.5% fitted and 60.1% close. Native geometry/pixel parity, failure/report checks, 10,300 packed assets and actual release New Game/F8 pass. Build: `builds/BrineSpace-2026-09-09-optimized/`; stable animation bindings used while concurrent animation work continues.

## Room risers V3 — September 9, 2026

Added six window-free risers for reactor, cryo chamber, data archive, storage bay, crew lounge and research lab; catalog overrides and refreshed card bindings installed. Owner direction: future windows are separate wall props. Keep mounting panels and the central door reserve clear. [Review gallery](../assets/room-risers-v3/review.html) includes toggleable guides; [placement notes](../assets/room-risers-v3/WINDOW_PLACEMENT.md) record source/world bounds. Native checks and 24 captures passed; 47 card identities passed. Future prop fit/occlusion needs validation when props are added. No executable rebuilt. See ROOM_RISERS_V3_2026-09-09.md.


## September 9 character animation expansion

[Animation expansion](ANIMATION_EXPANSION_2026-09-09.md): Marsh now has dedicated sitting/reading/resting/cargo and distinct swim/tread poses; Margot has directional sit/groom/nap plus stretch/yawn; River and Josh have start/stop/turn transitions, startup and standby. Installed v5 packs preserve prior sources. Asset, checkpoint/pause, real-station companion and repair tests pass; native captures reviewed. [Animated gallery](../character/animation-expansion-v5/review.html). Source checkout only; no executable rebuilt.

## September 9 room-specific riser walls

[Room risers](ROOM_RISERS_2026-09-09.md): six installed wall strips for medical, hydroponics, maintenance, galley, command and observation with baked fittings, static windows and reserved central entries. All 24 native rotations reviewed; adjacency, Studio and card-binding checks pass. Six cards refreshed. Source only; no executable rebuild.

## September 9 floor variants V5

[Six further finishes](FLOOR_VARIANTS_V5_2026-09-09.md) for reactor, cryo, robotics, refinery, command and observation add 96 tile slots to Studio. Sources and six furnished captures reviewed; native texture/rotation and selection/undo/redo checks pass. Two rejected robotics candidates preserved separately. Existing defaults retained; no executable rebuilt.

## September 9 common prop and floor-wire removal

[Room declutter](ROOM_DECLUTTER_2026-09-09.md): live rooms suppress common props/accessories, floor wiring/conduit and decorative overlays; the layout editor retains the assets and saved placements. Specialist equipment positions and sizes are preserved. Native 47-room/four-rotation checks pass; 44 furnished cards refreshed and all 47 card bindings pass. [Gallery](room-declutter-2026-09-09/review.html). Source checkout only; no executable rebuild.

## September 9 Josh tread and blowtorch pass

[Josh torch](JOSH_TORCH_2026-09-09.md): installed neutral charcoal tracked base across Josh movement/actions, plus four-direction torch deploy/weld/stow. Josh assists nearby paid crew hull repairs at +25% progress only while actively welding; costs and job ownership remain with crew. Focused repair, real-station routing/checkpoint/interruption and native sprite tests pass. Review gallery saved; no executable rebuild.

## September 9 Teegly release fix and bug reports

[PR integration](TEEGLY_PR_INTEGRATION_2026-09-09.md): integrates release-safe image loading and F8/unclean-session diagnostic bundles, with newer-loader coverage, pause support, safer report writes and a CI assertion guard. Fixed local Windows release is in `builds/BrineSpace-2026-09-09-fixed/`; detailed verification and limits are recorded in the handoff.

## September 9 expanded floor variety

[Floor variety](FLOOR_VARIETY_2026-09-09.md): six more selectable finishes for medical, hydroponics, cargo, data, galley and lounge; 96 additional tile slots. Sources and six furnished native captures reviewed; texture/rotation and selection/undo/redo checks pass. Existing room defaults retained. No executable rebuild.

## September 9 room materials and headphone scale

[Room art consistency](ROOM_ART_CONSISTENCY_2026-09-09.md): 16 selected matte source repaints across six room families, smaller radio headsets, and refreshed cards. Owner layouts and the restored BRINE room remain intact. All 47 rooms reviewed in four native rotations; final layout, source, dressing and card checks pass. [Before/after gallery](room-art-consistency-2026-09-09/review.html). Source checkout only; final headset correction awaits owner feedback.

## September 9 additional floor tiles

[Floor additions](FLOOR_TILE_ADDITIONS_2026-09-09.md): three new 4x4 atlases available in Studio's Floor finish selector. Native furnished review, texture/rotation and selection/undo/redo checks pass. Existing defaults retained; per-room adoption remains open. Source only; no executable rebuild.

## September 9 companion white-cutout repair

[Companion extraction repair](COMPANION_EXTRACTION_FIX_2026-09-09.md): River/Josh/Margot now load companion-cleanup-v3. Preserves interior white panels, removes connected exterior backgrounds, and area-downsamples original sources to reduce speckling. All six manifests, extraction regression and native sprite board pass; full personality run is not green amid concurrent room compile/render errors. Before/after gallery saved; no executable rebuild.

## September 9 sprite scale and animation polish

[Sprite polish](SPRITE_POLISH_2026-09-09.md): installed revised adult-proportion Marsh sprites and dedicated idle, consistent 64-color companion packs, and River/Josh action entry/exit clips. Native sprite and companion personality checks pass. Marsh broader test has peer-count failures reproduced with old art; secondary pose sharing remains. Review gallery and native captures saved; continuous browser review was blocked. Source checkout only, no executable rebuild.

## September 9 latest portraits installed

[Portrait installation](PORTRAITS_INSTALLED_2026-09-09.md): all eight latest portraits now load in the game, including the final suit/lighting pass, distinct station backgrounds, Margot realism V3 and BRINE V14. Native selection/comms reviewed at two sizes; bubble test passes. Room-dressing assertions noted separately. Source checkout only; existing executable not rebuilt.

## September 9 title and terrain fixes

[Fixes and before/after review](ART_FIXES_2026-09-09.md): revised title uses BRINE V13 likeness/rendering with matte slate/ivory surroundings and retained float, monitors and Reduced Motion. Eleven habitat patches now use continuous source fields rather than mirrored repeats. Native title, habitat and focused visual regressions pass. Source only; no executable rebuilt.

## September 9 art consistency audit

[Audit and review board](ART_CONSISTENCY_2026-09-09.md): 47 room families / 188 native orientations reviewed; distinct department palettes and owner layouts retained. Owner-selected pixel-textured V2 portraits installed for all seven architects/companions, with proportional Continue portraits. Native UI checks pass at two sizes. Title illustration style and some mirrored habitat ground repeats remain documented follow-ups. Source only; no executable rebuilt.

## September 9 portrait individuality review

[Portrait review](PORTRAIT_INDIVIDUALITY_2026-09-09.md): seven V3 portraits revise underlying anatomy and materials after owner feedback that V1/V2 looked generic. Margot uses her original photo reference. Version comparison saved; runtime portraits unchanged. Owner likeness and final pixel-texture review remain open.


## September 9 camera shimmer correction

[Camera handoff](CAMERA_SHIMMER_2026-09-09.md): align the entire rendered world to physical screen pixels to reduce nearest-neighbor shimmer during panning at fractional window scales. Logical camera/input coordinates and sharp filtering are preserved. Native 64-case sampling regression and navigation checks pass; source only, owner motion review pending.

## September 9 companion personality

[Personality handoff](COMPANION_PERSONALITY_2026-09-09.md): Margot's sit/groom/nap/pet actions, River's head scans/equipment inspection/quiet chirps, and Josh's head gestures/tread pivots/repair watching. Journal > Crew offers Pet Margot and companion Locate links. Action clocks, cooldowns and pending approaches persist through Continue. Native action and companion regression checks pass; owner animation/pacing review remains open. Local source only, no executable rebuilt.

## September 9 playable Windows build

Windows x64 release is available in builds/BrineSpace-2026-09-09. Quick regression, package startup/assets and release launch checks pass. Includes an export dependency correction and startup zoom-slider signal fix. [Build handoff](WINDOWS_BUILD_2026-09-09.md).

## September 9 character portraits and recap discoveries

Companion selector portraits now match architect portrait dimensions. End-of-loop discoveries include newly unlocked architects and companions, preserved across Continue. [Handoff and checks](CHARACTER_DISCOVERIES_2026-09-09.md).

## September 9 Margot companion

[Margot integration](MARGOT_INTEGRATION_2026-09-09.md): selected frog-hat portrait V2, four-direction cat idle/walk, pet cryopod rescue beside two failed human pods, optional future selection and Save/Continue. Older robot-only loops remain intact. Focused native/headless and affected regression checks pass. Owner gait/pacing review pending; local source only, no executable rebuild.

## September 9 game maintenance pass

[Maintenance handoff](MAINTENANCE_2026-09-09.md): fixed delayed camera centering overriding Fit Station, startup/resize view drift, guide-visible sidebar overflow, and flood warnings consumed during pause. Removed redundant layout lookups during prop drawing with identical flip pixels. Inspector still expands to 520 design pixels when the guide closes. Broad regression and native visual checks are recorded in the handoff; no overall FPS claim or executable rebuild. Existing authored layouts preserved.

## September 9 BRINE layout restored

Owner requested BRINE return to its pre-simplification arrangement. Restored its four authored quarters, original personal BRINE entry and matching card, including the lower workstations, servers and observation pedestal. Other rooms and their saved overrides are unchanged. BRINE is an explicit exception to the 3�4-asset direction. Four native editor/runtime comparisons and card consistency pass; capture reviewed. Evidence: `output/brine-layout-restore/`; no executable rebuilt.

## September 9 uncluttered large-asset correction

[Layout correction](LARGE_ASSET_LAYOUTS_2026-09-09.md) supersedes the denser pass below: 3�4 major assets per furnished room, with already simpler rooms left sparse. Removed 139 prop instances across 97 orientations; 188 native editor/runtime comparisons match. Updated saved removals with original-file backup, verified 176 native kept-prop lists, and refreshed 44 cards. Local changes only; no executable rebuilt.

## September 9 Marsh battery tradeoff

[Android survival and recharge](MARSH_BATTERY_2026-09-09.md): Marsh needs no helmet or Oxygen, including underwater expeditions. Initial battery lasts five minutes; he returns to his original pod at 35%, recharges at 5%/s for 1 Power per 25%, and resumes work. Battery and prepaid charge survive Save/Continue. Native docking, zero-Oxygen expeditions, recall, core/derelict return, human survival and construction checks pass. Owner balance review pending; local source only.

## September 9 preferred room layouts

[Layout handoff](PREFERRED_LAYOUTS_2026-09-09.md): adopted the owner�s 49 saved orientations unchanged and extended larger equipment/selective clutter removal to the remaining furnished layouts. All 188 Studio entries covered; 176 furnished orientations pass door-route checks. Gameplay now matches free-placement saves, BRINE corner notches have matching collision, and 44 room cards are refreshed. Native editor/runtime parity, live core/recovery-pod routes, Studio workflow and card checks pass. Personal saves unchanged; owner visual review pending, no executable rebuilt.

## September 9 River and Josh companions

[Companion integration](COMPANIONS_HANDOFF_2026-09-09.md) adds small green River
and larger blue-lavender Josh with owner-requested treads. Paid derelict recovery,
container opening, powered restart, a separate roster, optional pre-loop selection
and Save/Continue are installed. Both have four-direction idle/rolling packs.
Focused headless/native and affected regression checks pass; [visual review](../character/companions/review.html)
is ready. Owner motion/pacing review and Margot remain pending. Local source only;
no executable rebuilt. Prototype behavior and log limits are recorded in the handoff.

## September 9 Marsh charging chamber

[Charging chamber implementation](MARSH_CHARGING_2026-09-09.md) supersedes Marsh's cryo route in new loops. Reconnect his dedicated derelict and restore power: white fluid pumps through attached tubes for 12 seconds, then Marsh wakes and permanently unlocks. Charge persists through power loss, suspension and Save/Continue. Distinct occupied/empty cradle art and native fluid motion/freeze checks pass, alongside Marsh recovery and legacy/selection regressions. Owner visual review pending; existing loops preserve their original occupants. Local source only.

## September 9 Marsh unlockable architect

[Marsh integration](MARSH_UNLOCK_2026-09-09.md) adds the approved blond android as a fourth recoverable architect in new loops. Recovery permanently unlocks selection; starting cache is +4 Data/+4 Metal. Independent actor, portrait, pod art, sprites, helmet frames, construction and saves are installed. Four-crew recovery/persistence, legacy recovery, picker and four-direction paid-construction checks pass. Old loops retain existing occupants; no executable rebuilt. First-pack animation sharing and owner review limits are recorded in the handoff.

## September 9 building decisions and discoveries

[Decision pass](BUILD_DECISIONS_2026-09-09.md): inspector priorities, visible placement explanations, adaptive construction/supply guidance and three hidden synergies. Discovery suite is clean and native UI assertions pass; screenshot reviewed. Native logs also report missing assets from concurrent Marsh integration, so global native acceptance remains pending. Local source only.

## September 9 maintenance session closed

[Maintenance closeout](MAINTENANCE_SESSION_CLOSEOUT_2026-09-09.md) records export cleanup and the brief north-placement investigation. Owner reported placement working again; no gameplay/layout fix was made. The follow-up portrait/asset integration request was canceled before implementation. Other art and gameplay sessions remain independent.

## September 9 Marsh android concept

Latest revision: [V3](../character/marsh-portrait-v3/README.md) adds owner-requested blond hair, visible steel temple plate and an off-white suit, preserving the human-looking male identity. Saved for owner review; no gameplay integration.

Owner correction: Marsh is male and more humanoid. [V2](../character/marsh-portrait-v2/README.md) now uses human skin, ears, neck and dark hair, with subtle android details. Supersedes V1's visibly mechanical design; owner review pending.

Created [Marsh's portrait concept](../character/marsh-portrait-v1/README.md) in the current crew style: ivory synthetic face, graphite shell, amber eyes and sage shoulder panels. Source, prompt and manifest saved. Owner review and role definition pending; no gameplay integration.

## September 9 matching crew portraits

[Crew portrait handoff](CREW_PORTRAITS_2026-09-09.md) records new Bill, Veld and Branforth close-ups matching BRINE V13, replacing the old concept crops in the shared portrait loader. Comms use the larger portrait size for all speakers. Native all-speaker and picker checks pass at both sizes, with small-size visual review; owner acceptance pending.

## September 9 sidebar readability

[Sidebar handoff](SIDEBAR_READABILITY_2026-09-09.md): Construction/Flood buttons hidden, hardware and time controls compacted, inspector reading area enlarged with clearer font and contrast. Final native navigation and hardware checks pass; screenshot reviewed. Local source only.

## September 9 BRINE reference restart

Owner liked V13. Animated bubbles are now 62.5% smaller, dimmer and thinner at their request. Native comms and bubble mask/clock checks pass; small-size capture reviewed, owner bubble review pending. See portrait handoff for evidence.

Latest follow-up: V13 darkens the face slightly while preserving V12's soft shadows. Installed and native-checked at both sizes; captures saved with V13. Owner review pending.

Follow-up: V12 softens facial shadows and caustic contrast at owner request, retaining V11 identity and framing. Installed and native-checked at both sizes; captures saved with V12. Owner visual review pending.

Owner requested a fresh portrait from a supplied photo reference. [V11 handoff](BRINE_REFERENCE_RESTART_2026-09-09.md) records the new tied-back hair, reference-based face and close composition, installed in the enlarged comms portrait area. Native checks at both sizes and revised bubble masking pass; owner visual acceptance pending. This supersedes V9 selection below.

## September 9 menu, portrait and comms polish

[Polish handoff](MENU_PORTRAIT_POLISH_2026-09-09.md): Continue uses the approved selection portrait, comms is wider, and the in-game menu has five main choices with clearer labels. Four native fixtures pass; menu, dialogue and title preview captures reviewed. Local source only.

## September 9 HUD sizing

[HUD sizing handoff](HUD_SIZE_POLISH_2026-09-09.md): top-right icons enlarged from 44 to 60 design units; time/cycle controls use a compact shared pause/speed row and tighter margins. Native navigation checks pass; both HUD sizes and cycle panel visually reviewed. Local source only.

## September 9 dialogue pause

[Dialogue pause handoff](DIALOGUE_PAUSE_2026-09-09.md): visible conversations pause station time until explicit close, preserving any previous manual pause. Removed timed dialogue dismissal. Native pause/menu/queue checks and headless context/archive checks pass. Local source updated; no new export.

## September 9 larger BRINE comms portrait

BRINE's V9 portrait now fills the comms panel's interior height at 150x150, 56% wider than before, retaining the closer crop. Native comms checks pass at both resolutions; small-screen capture visually reviewed. [Portrait handoff](BRINE_PORTRAIT_STYLE_2026-09-08.md) records captures and pending owner review.

## September 8 readable awakening intro

[Intro handoff](INTRO_CONTINUE_2026-09-08.md): the complete transmission renders before station setup and stays until explicit Continue. Gameplay pauses while reading. Native new/restore, GUI and keyboard acknowledgement, reduced-motion and archive checks pass; screenshots reviewed. Local source updated; no new package.

## September 8 BRINE portrait style pass

[Portrait handoff](BRINE_PORTRAIT_STYLE_2026-09-08.md) records the owner's preference for the previous portrait after V10. V9 is restored with 25% closer runtime framing for readable features; source pixels are unchanged. Bubble masking follows the crop. Native comms at both sizes and crop-aware bubble checks pass; owner review of framing and packaged validation remain pending. Earlier sources retained.

## September 8 second game-wide maintenance round

[Second-pass handoff](GAME_MAINTENANCE_PASS2_2026-09-08.md) records the final-drainage
inspector fix, invalid-checkpoint control rejection, stale-error cleanup, shared source
atlases and reduced renderer/layout work. Twenty-one targeted fixtures pass; all 33
native retained/direct pixel comparisons match. Native shutdown checks are clean;
an Ogg warning remains in the headless economy fixture. The paid two-generator salvage
comparison now buys generation earlier, without changing game costs. Dense frame time
is essentially unchanged at 25.205 ms dry / 34.312 ms flooded. Work is local and
uncommitted; a new package and owner normal-play acceptance remain pending.

## September 8 game-wide maintenance round

[Maintenance handoff](GAME_MAINTENANCE_2026-09-08.md) records checkpoint isolation
fixes, cached door lookups, lighter inspector/badge updates, corrected guide copy and
updated construction fixtures. Twenty-six targeted current-source checks return zero,
with intermittent shutdown warnings in two fixtures documented separately. Native
49-room median frame time improves from 33.943 to 25.221 ms dry and 44.885 to 34.120 ms
flooded; dense views still exceed the 60 fps budget. Native HUD, lighting and wet-door
checks pass. Costs, failures and hidden discovery remain intact. Local work is
uncommitted; new package and owner normal-play acceptance remain pending.

## September 8 obsolete compiled export cleanup

Owner requested disk cleanup. Removed 67 superseded `.pck`/`.exe` files (66.775 GiB): environment-export-v1 through v22, airlock-low-package-v1 through v3, mat-repair-package-20260906-v1/v2, drone-fleet-v2/v3, station-package-v1, and earlier tiled-floor/game-polish/layout-performance/layout-studio playtest binaries. Historical references below to those runnable binaries are now archival; their source snapshots, manifests, captures and test evidence remain.

Retained `output/tiled-floor-complete-20260908/build/` and `output/audio-playtest-20260908/build/` (EXE/PCK checksums matched their recorded manifests), plus the latest export in each numbered series and the integrated-acceptance package. These retained binaries are dated snapshots, not rebuilds of subsequent source changes. Source art, Git data and game saves were not pruned.

## September 8 fitted service art session closeout

[Session handoff](FITTED_SERVICE_SESSION_CLOSEOUT_2026-09-08.md) consolidates this art session, host-fit findings and restart point.29 scoped export records match current files. Skill lessons and visual bible updated; this session is paused at owner request. Other sessions remain separate; work is local and uncommitted.

## September 8 navigation UI session paused

[Session handoff](NAVIGATION_UI_SESSION_CLOSEOUT_2026-09-08.md) records the final
four-button HUD row, selected clean badges, cream Codex, skill/bible updates and
verification limits. Local work saved; owner review and optional alpha exports remain.


## September 8 room material session closeout

[Material session handoff](ART_MATERIAL_SESSION_CLOSEOUT_2026-09-08.md) consolidates Tidal-reference repaints, shared accessories, Bio/Xeno follow-ups and the cryo machinery replacement. Latest Xeno front/side views pass native rotation, card and draft checks with visual review. Full asset matching and owner acceptance remain incomplete. Session paused at the owner's request; reconcile newer architecture work below before resuming. No executable rebuild or commit from this session.

## September 8 crew animation session closeout

[Crew animation closeout](CREW_ANIMATION_SESSION_CLOSEOUT_2026-09-08.md) records completed coverage, runtime checks and pending owner visual review. Character skill, asset-pipeline/workflow reference and visual bible updated with facing, cropping, furniture-depth and checkpoint lessons. Other sessions remain separate; this closeout performs no commit or deployment.

## September 8 wall-asset session paused

[Session handoff](WALL_ASSET_SESSION_CLOSEOUT_2026-09-08.md) consolidates wall families, companion props, material/alpha workflow and seed placement evidence. Production stopped at owner request for now. Remaining directions, crew/service validation and runtime installation are explicitly recorded; other sessions are managed separately.


## September 8 room/corridor art session closeout

[Session closeout](CORRIDOR_ART_SESSION_CLOSEOUT_2026-09-08.md) records corridor/riser direction, live variants, source locations, tests and review limits. The room skill, asset-production notes, layout workflow and visual bible include the reusable lessons. Work remains local and uncommitted. Other sessions are independent; resume from current status and latest owner notes.

## September 8 Studio / BRINE session closed

Owner closed the session with V8 selected. [Closeout](STUDIO_BRINE_SESSION_CLOSEOUT_2026-09-08.md)
records Studio, lighting, portrait direction, source provenance and tested scope.
Portrait pipeline guidance and visual bible updated; no remaining work in this task.

## September 8 water and editor session closeout

[Session handoff](WATER_EDITOR_SESSION_CLOSEOUT_2026-09-08.md) consolidates this session's water/editor changes, validation, remaining performance limits and pending owner review. Room skill, thumbnail production notes, editor workflow and visual bible updated. Work remains local and uncommitted; other sessions are managed separately.

## September 8 opposite-facing corner defaults

New corner selections alternate west/south and east/south defaults, based on placed corners plus queued corner orders. Manual rotation and existing saved rooms remain intact. Automatic hand selection and explicit card selection share the rule. Focused tests pass queued/completed parity and preservation. [Both directions in all three finishes](../output/corner-defaults-v1/index.html). Native art is reused from the validated rotation captures.

## September 8 crew life animations

[All eight crew-life categories](CREW_LIFE_EXPANSION_2026-09-08.md) are integrated for Bill, Veld and Branforth: sitting, meals, sleep, oxygen distress/recovery, pickup, reading/inspection, carrying turns and additional death directions. 258 new runtime clips include fitted helmet counterparts. Native pack, 72 furniture/rotation/actor cases and affected expedition, flooding, swimming, construction and repair checks pass. [Moving review](../output/crew-life-review.html) and [showcase](../output/crew-life-preview.gif); owner visual acceptance pending.

## September 8 layout editor performance and tray polish

[Editor polish](LAYOUT_EDITOR_POLISH_2026-09-08.md) removes raw source-sheet thumbnail backgrounds and solid selection fills, stabilizes tray rows during loading, and uses a finite thumbnail queue. Translation-only drag updates reduce populated-fixture CPU update time from 0.933 to 0.058 ms; total render-inclusive time remains about 6.06 ms. Transparent-preview and fast/full pixel/geometry checks pass. [Tray review](../output/layout-editor/polished-tray.png). Owner acceptance pending.

## September 8 corridor doors and water review

[Corridor floor/door pass](CORRIDOR_DOORS_WATER_2026-09-08.md) adds restrained floor variation and gray metal doors at all default corridor, corner and T entries. Shared connected doors use the same finish. Nine live wet-door variants pass closure and pause checks; all 36 rotated water masks match their footprints, and water physics reports zero failures. [Dry and flooded review](../output/corridor-polish-v3/index.html). Owner acceptance pending.

## September 8 corridor junction and floor polish

[Corridor polish](CORRIDOR_POLISH_2026-09-08.md) removes the 35-unit overextension of inner T/elbow wall returns and gives all nine shape/variant combinations distinct floor arrangements. Transit tread/grating, utility service runs and observation grating retain solid borders and compatible entrance lanes. Native rotations, floor mapping/coverage, routing and card checks pass. [Review and notes](../output/corridor-polish-v2/index.html). Owner acceptance pending.

## September 8 aligned hallway floor runs

The industrial floor now follows the path: solid perimeter strips, matching central grating/pipe lanes, and grated manifold covers at elbows and T branches. Symmetric lane selection keeps flipped corridor sockets compatible. Explicit tile/finish edits are preserved. Native rotations, footprint/UV/finish tests and refreshed cards pass. [Aligned floor review](../output/hallway-floor-aligned-v1/index.html); owner acceptance pending.

## September 8 industrial hallway floor revision

Owner rejected the first floor as too large and plain. The new [industrial deck](HALLWAY_FLOOR_TILES_2026-09-08.md) uses 64 smaller grating, steel-panel and recessed-pipe modules at 24 units wide, half the prior panel width. It is the corridor/corner/T default; the prior quiet finish remains selectable. Native views, footprint/UV/finish checks and refreshed cards pass. [Updated review](../output/hallway-floor-tiles-v2/index.html). Owner acceptance pending.

## September 8 hallway floor tiles

[Hallway tile pass](HALLWAY_FLOOR_TILES_2026-09-08.md) adds a 16-panel matte grey-green atlas as the corridor, corner and T-junction default. Tiles use the existing 48-unit grid and clipped footprints; explicit saved finishes remain. Native previews, full mesh coverage at 12 shape/rotation combinations, current finish selector and 47-card consistency pass. [Floor review and notes](../output/hallway-floor-tiles-v1/index.html). Owner visual acceptance pending.

## September 8 corridor cleanup and north-entry doors

Owner follow-up removes corridor/corner/T floor drains, service pipes, cables, hatches and legacy mounted props. Observation windows are vertically centered within the riser; exposed north-facing port faces use a closed door without windows. Connected faces still cull. [Updated review](../output/corridor-wall-variants-v1/index.html) includes all nine variants and rotations. Native port mapping, raised/low and card checks pass; owner review pending. Scope is the corridor set under review, not furnished-room machinery.

## September 8 unique corridor and corner walls

[Dedicated routing architecture](CORRIDOR_WALL_VARIANTS_2026-09-08.md) adds six original transit, utility and observation designs: separate straight and turning-bay sources, nine combinations across corridors, corners and T-junctions. Low hulls, raised faces and nine cards now use the new art through existing variant selection. Native rotation/raised-low, fitting bounds, connection masks, taper coverage and card consistency checks pass. [Variant gallery and notes](../output/corridor-wall-variants-v1/index.html). Owner visual acceptance pending.

## September 8 layout editor controls

[Editor controls](LAYOUT_CONTROLS_2026-09-08.md) enable free placement by default (explicit saved settings remain), add left-drag camera panning on empty canvas and retain Shift-drag marquee selection. Canvas clicks find floor decorations without manually changing modes. Entryway areas and Clean preview are accessible in the main toolbar. Native workflow, movement/undo, camera, save/reload and recovery checks pass; clean room preview inspected.

## September 8 department riser walls and default visibility

[Department riser pass](RISER_DEPARTMENT_PASS_2026-09-08.md) adds eight distinct matte wall families, retaining the dedicated BRINE and airlock designs. All 47 room types are assigned; corridor faces and 47 primary cards plus six corridor variants are refreshed. Risers now default on in the game and Layout Studio. A new saved preference migrates the retired forced-low setting while remembering subsequent explicit changes. Native station/default/adjacency/cache, settings, studio controls and card checks pass. [Before/after gallery with notes](../output/riser-departments-v1/index.html). Owner visual acceptance pending.

## September 8 dense-station rendering polish

[Rendering polish](DENSE_STATION_POLISH_2026-09-08.md) tightens off-screen room culling and shares door aperture calculations within each render frame, while physics reads live state. In the same 49-room fixture, flooded median frame time falls from 64.418 to 44.584 ms (about 31%); dry falls from 48.215 to 33.372 ms. Culling comparisons are pixel-identical at two tested zoom levels. Rendering cache and native wet-door/pause checks pass. Active repair wording is clearer. Dense views still exceed the 60 fps frame budget; owner review during normal play remains pending.

## September 8 crew action expansion

[All five animation priorities](CREW_ACTION_EXPANSION_2026-09-08.md) are generated,
packaged and integrated for Bill, Veld and Branforth: underwater work, swimming
transitions, torch draw/stow, cargo carry/unload and directional interactions.
168 added runtime clips include helmet variants; unloading checkpoints before
one-time cargo credit. Native pack, expedition, hull repair, construction,
swimming and room-activity checks pass. [Moving review](../output/crew-actions-review.html)
and [showcase](../output/crew-actions-preview.gif); owner visual acceptance pending.

## September 8 detailed doors and flooded closing

[Door art polish](DOOR_ART_POLISH_2026-09-08.md) integrates detailed skins across shared front/side, raised, BRINE default and airlock doors, with five finishes. Flooded closing adds aperture-limited wash/foam, pressure ripples and amber indicators; sealed doors show no crossing flow. Native production/pause, aperture, water physics, airlock and BRINE route checks pass; 44 cards refreshed and all 47 card identities validate. [Animated review and notes](../output/door-polish-v1/index.html). Owner visual acceptance pending.

## September 8 flood safety, controls and scale checks

[Safety and scaling pass](FLOOD_SAFETY_AND_SCALE_2026-09-08.md) adds conservative
repair air budgets, physical low-air retreat/refill, cancel/refund and crew
assignment, plus a station flood alert with room location and threshold hysteresis.
Standard rupture tuned to 3.2%/s and 14s work, still 5 Metal; old severe damage and
paid jobs remain compatible. Native safety/save and expedition tests pass; a
64-room open network conserves water. Water physics in a 49-room fixture fell
from 1.425 to 0.301 ms, but dense-overview rendering remains slow (~65 ms/frame).
[Controls preview](../output/hull-safety-controls.png). Owner review pending.

## September 8 submerged BRINE portrait

[V8](../character/brine-comms-v8/README.md) adds buoyant hair and refracted
underwater light so BRINE reads as suspended in water. Bubble occlusion updated
for the wider hair. Native comms and mask checks pass; owner review pending.

## September 8 BRINE glass background

[V7](../character/brine-comms-v7/README.md) replaces generic background light
bands with curved glass and cropped ivory framing matching the actual tube.
Smile and smaller bubbles preserved; native comms checks pass. Owner review pending.

## September 8 BRINE default entry doors

All four BRINE sockets now display closed pressure doors by default, including unconnected entries. North uses the themed riser door when raised walls are enabled; low north and the other three use ceramic/aquamarine leaves. Connected/open wall spans retain the existing animated door handling. Collision and connection rules are unchanged. Native card refreshed; see `assets/brine-default-doors-v1/README.md` for verification.

## September 8 hull leak variations and crew repairs

[Physical hull repairs](HULL_LEAK_REPAIRS_2026-09-08.md) replace instant hull sealing.
Hairline, seam and rupture profiles flood at 0.8/2/4% per second; repairs allocate
2/3/5 Metal and take 6/10/16 seconds at the worksite. Crew navigate and weld;
submerged work consumes oxygen. Partial paid work survives death and Continue.
Native repair/save, physics, render-cache and existing construction checks pass.
[Leak comparison](../output/hull-leak-variants.png); owner visual/pacing review pending.

## September 8 crew water contact

Owner accepted softer water and hull leaks. [Crew wake refinement](CREW_WATER_WAKE_2026-09-08.md)
replaces blue circles with faint, separated trailing strokes aligned to the crew.
Native stages/Save-Continue pass; [preview](../output/crew-wake-polish.png), owner review pending.

## September 8 softer water and hull leak

[Visual refinement](WATER_SOFT_LEAK_2026-09-08.md) removes the net-like water
highlights in favor of broad drifting light. Hull leaks now have fractured metal,
curved streams, droplets and impact ripples. Native stage/save check passes;
[before/after preview](../output/water-soft-leak-comparison.png), owner review pending.

## September 8 water physics and shadow polish

[Second polish pass](WATER_POLISH_2026-09-08.md) fixes near-empty pump and saturated
leak transfer, skips equal-depth water checks, adds aperture-driven doorway
currents, softens submerged crew shadows and reduces deep-water glare.
Physics/material-reuse, native Save/Continue and three-crew transit checks pass.
Three-room median frame time is 10.98 ms versus 10.50 ms before this pass; no
full-station speedup claimed. [Native stage comparison](../output/flood-heights-polish.png).
Owner visual acceptance pending.

## September 8 BRINE machinery, wall and starting thaw

[Room renewal](BRINE_ROOM_RENEWAL_2026-09-08.md) adds a distinct northeast machinery bank to the BRINE tray, ceramic/aquamarine riser and matching door panels, a fitted tube label and removal of the protruding floor decoration. Starting cryopod now retains the selected architect for ten simulation seconds; pause and Continue preserve progress. Recovery/save and default-room routes pass; native art reviewed. NE bank is available for placement, with an isolated fitted preview replacing the old workstation. Owner visual acceptance pending.

## September 8 water depth and performance

Water now visibly submerges crew and equipment as it rises, with animated floor
caustics, surface wakes and a front cutaway waterline. Two repeated room rebuilds
were removed: the three-room native fixture improved from 206.6 ms to 10.5 ms
median frame time. Targeted gameplay, rendering, live-layout and native checks
pass; owner visual acceptance pending. See [handoff](FLOOD_VISUAL_DEPTH_2026-09-08.md)
and [four-height comparison](../output/flood-heights-v2.png), plus the
[60-fps transit replay](../output/flooded-transit-v2.mp4).

## September 8 swimming helmet fit

Side-view follow-up now uses 36 measured per-pose face anchors and scalp occlusion
to prevent the bare head protruding through the shell. Close-up native review and
playback checks pass; moving preview updated to pose4 for owner review.

Swimming helmets now compose at a smaller, closer fit across all three architects
and four directions. Per-pose layering and timing retained. Native 72-pose loader
comparison and swim playback checks pass; owner visual/motion review pending.
See [handoff](SWIMMING_HELMET_FIT_2026-09-08.md).

## September 8 BRINE corner asset

Owner equipment revision: [v2 console](../assets/brine-corner-service-v2/README.md) adds dense monitors, diagnostic controls and circulation equipment to both arms using the supplied reference. The same tray entry now uses v2; 128-unit width and flush NW fit retained. Native tray/clearance and alpha checks pass; personal layouts unchanged. [Updated preview](../output/brine-corner-equipment-2026-09-08/room.png). Owner visual acceptance pending.

[Northwest corner service console](../assets/brine-corner-service-v1/README.md) starts the corner-fitted furniture series. A pearl-white/aquamarine L-shaped bank fits both walls while preserving BRINE's central chamber. Available in BRINE Core's Room Default tray at 128 world units wide; [native fitted preview](../output/brine-corner-service-2026-09-08/room.png), static prop/door clearance and alpha export pass. Personal layouts unchanged; one authored NW orientation, owner visual review pending.

## September 8 room style polish

[Before/after review](../output/room-style-polish-2026-09-08/index.html) polishes twelve recent south-facing banks against approved Tidal material quality and department references. Registered placement frames and personal layouts preserved. Riser doors now have recessed textured panels, seals and threshold details. Twelve comparisons beside Bill, ten default south placements, door animation and the 47-room gallery reviewed; card/source/alpha checks pass. Owner style acceptance pending. See [handoff](ROOM_STYLE_POLISH_2026-09-08.md).

## September 8 Studio owner-note corrections

[Illustrated review](../output/studio-owner-notes-2026-09-08/index.html) updates all 47 room previews and preserves the owner's three edited-room layouts. Studio adds centered Rotate Room / Next Room / Save, valid-edit autosave across rotations, R variant cycling, F flip and default-tray vertical views. Listening Post slices move; north riser door animates and replaces the low north edge. Mining/Refinery materials and three cutouts repaired; twelve authored south views added, ten used by current south-wall defaults. Forty-four cards refreshed. Native editor/targeted checks, 47-card consistency and 162 source hashes pass; owner visual acceptance pending. See [handoff](STUDIO_OWNER_NOTES_2026-09-08.md).

## September 8 room flooding and survival

Follow-up: [35-second native transit replay](../output/flooded-transit.mp4) shows
all three crew swimming through real doorways and changing movement as water
spreads between compartments. Headless/native routes and video decode pass.

[Implementation and checks](ROOM_FLOODING_2026-09-08.md) add gradual hull leaks,
open-door water transfer, powered pump drainage and low/wading/swimming/critical
stages. Crew have 15-second breath, 60-second helmet tanks, real locker refills,
oxygen/exposure deaths and a provisional 90-second starvation period. Water and
survival clocks persist through Continue. Focused logic, expedition/refill and
disk-save checks pass; native stages reviewed. Owner pacing/visual acceptance is
pending. This supersedes the earlier instantaneous food-shortage casualty behavior.

## September 8 BRINE expression

[V6](../character/brine-comms-v6/README.md) gives BRINE a faint composed smile
to address the sad expression. Crew style, tube framing and smaller bubbles
preserved. Native comms checks pass; owner review pending.

## September 8 BRINE crew-style portrait

[V5](../character/brine-comms-v5/README.md) brings BRINE closer to Bill/Veld's
angular, matte pixel rendering and reduces bubble size by about a third.
Spacious tube framing preserved. Native comms checks pass; owner review pending.

## September 8 full room art catalog

[Owner review catalog](../output/room-catalog-2026-09-08/index.html) covers all 47 room types with 167 native stills and 75 recent standalone prop records. All 44 furnished-room cards refreshed from live renderers; primary/grid/variant consistency and native portrait checks pass. 150 wall-source hashes match. New standalone libraries still need fitted room installation, including known seed/communications overlap fixes. See [handoff](ROOM_ART_CATALOG_2026-09-08.md); owner notes and installation work remain pending.

## September 8 navigation badges

Owner follow-up groups Archive, Diagnostics, Journal and Menu into one top-right row and removes the top resonance/cycle displays. Compact badge labels and two-size native review complete.

[Clean colored badges](NAVIGATION_BADGES_2026-09-08.md) now appear on the HUD, title tiles and pause Codex entry. Runtime silhouette clipping excludes source checkerboards. Native Journal/Diagnostics checks pass;1600/960 HUD and title captures visually reviewed. Owner review pending.

## September 8 maintenance parts-cleaning bank

[North cleaning bank](../assets/parts-cleaning-wall-v1/README.md) adds dry basin, supplies and ribbed parts mat at320 by78.70 units. V2 corrects washer and quiets fittings; muted bottle shoulder facets remain. Native material/alpha review and clean log pass. Standalone art only; room fit, other directions and cleaning behavior remain outstanding.


## September 8 short communications section host study

The [100-unit section](../assets/communications-south-section-v1/README.md) adds finished ends and fits the tested Radio Lab south gap without visual furniture or door overlap. Native art and static host capture reviewed. Host helper gains --section mode; no room data changed. Mounting, occupied access and owner acceptance remain pending.

## September 8 seed carrier supported group

[Group review](../output/seed-packet-carrier-v1/group-scale.png) places the24-unit carrier on the right worktop while retaining the28-unit propagation tray on the left. Native and2x review shows support and a clear central sorting tray. Static group pass; hand clearance, lifting and runtime attachment remain unverified.


## September 8 seed packet carrier

[Small carrier](../assets/seed-packet-carrier-v1/README.md) adds three supported packets at24 by19.50 units. Native material/alpha review and clean export log pass; enclosed handle aperture is registered and sampled transparent. Handle pose, worktop placement and carrying animation remain unverified.


## September 8 communications host fit rejected

The [Radio Lab study](COMMUNICATIONS_HOST_STUDY_2026-09-08.md) retains current furniture while comparing all four full banks. North overlaps the installed signal wall; south intersects the electronics bench; both side banks cross doors and furniture. Native capture reviewed, no room data changed. Next: shorter service sections or a distinct host layout.

## September 8 gallery placement evidence

The material review gallery now displays contextual host, relocation and supported-group reviews with separate verdicts, findings and evidence links. Rejected original layouts remain visible alongside later static proposals; changed hashed study evidence gets a stale warning. Five gallery tests pass;72 records generated with no stale export hashes. Browser rendering was not checked in this change.


## September 8 seed section relocation proposal

[Relocation study](../output/seed-sections-relocation-study.png) retains all six Hydroponics furniture items and clears measured seed-section overlaps. Crops move68 units right; nutrients and harvest stand96 right. West door stays clear with other walls closed. Native visual review and clean log pass. No runtime installation; crew access and service connections remain unverified.


## September 8 foundation seabed contact

Foundation feet now have broader contact shadows and overlapping sediment to
connect them visually to the ocean floor. Opening-room native preview reviewed;
owner acceptance pending. See [handoff](FOUNDATION_CONTACT_2026-09-08.md).

## September 8 split seed bank host review

[Paired host study](../output/seed-sections-host-study.png) confirms a96-unit section gap clears the72-unit west doorway with12-unit axial margins. Sorting still overlaps crops; storage overlaps nutrients and harvest stand. No room data changed. These assets need a distinct preparation layout or measured furniture relocation before installation.


## September 8 handheld signal meter

The [16-unit meter](../assets/handheld-signal-meter-v1/README.md) adds a supported communications companion. V2 quiets pointer and casing details; native material/alpha and static mat-group review pass. Source-space support and actual dimensions recorded. Pickup, live signals and room placement remain unimplemented.

## September 8 short seed storage section

[West storage section](../assets/seed-storage-west-section-v1/README.md) adds four tins and cassette with right-facing catches. V2 quiets shiny lid rims. Native material/alpha review passes. Actual67.84 by136 is deeper than sorting55.24; paired room fit remains pending.


## September 8 short seed sorting section

[West sorting section](../assets/seed-sorting-west-section-v1/README.md) adds a finished-end136-unit module. V2 quiets seed shading and widens the narrow first pass; actual depth55.24 exceeds the45-unit brief and awaits host assessment. Native material/alpha review passes. Storage companion and furniture-fit solution remain outstanding.


## September 8 communications four-direction coverage

The [east bank](../assets/communications-service-east-wall-v1/README.md) completes four standalone directions at66.54x320 with left-facing access. Native material/alpha and clean-log review pass. [Family handoff](COMMUNICATIONS_SERVICE_FAMILY_2026-09-08.md) records dimensions and pending host/clearance review. No runtime changes.

## September 8 west communications counter

The [west bank](../assets/communications-service-west-wall-v1/README.md) adds right-facing access. V3 reduces visual depth from95.17 to65.07 at320-unit length, retaining three leads and spare connectors. Native review passes; north/south/west indexed. East and runtime placement pending.

## September 8 seed bank host fit rejected

[Host study](../output/seed-bank-host-study.png) overlays the slim west bank on current Hydroponics with furniture retained. It intersects crops, nutrients and harvest stand; an open west wall also blocks the central door. No room data changed. Next art work: shorter sections with central access or a distinct preparation-room host. Native standalone art remains valid; this placement does not.


## September 8 seed bank four-direction art family

[East seed bank](../assets/botanical-seed-east-wall-v1/README.md) completes four standalone directions at46.76 by320 with left-facing access. V2 restores four tins lost in V1. Native scale/material/alpha review and clean export log pass; four-view provenance audit passes. Casebook and bible record dimension and inventory drift. Runtime placement remains unverified.


## September 8 portrait room-card preview

Room cards now use 224 × 320 portrait proportions with larger artwork and
width-relative rarity badges. The hand tray is taller to accommodate them.
Native 1600 × 900 preview shows three cards without clipped names or costs:
`output/portrait-room-cards.png`. Owner review pending; see
[handoff](PORTRAIT_ROOM_CARDS_2026-09-08.md).

## September 8 south communications counter

The [south bank](../assets/communications-service-south-wall-v1/README.md) adds north-facing fixtures and cabinet access. V3 quiets the rear rail and screen after orientation repair. Native320-unit review passes; north/south indexed with cabinet differences recorded. Side variants and runtime placement pending.

## September 8 slim west seed bank

[West botanical seed bank](../assets/botanical-seed-west-wall-v1/README.md) adds a 45.36 × 320 matte side-wall variant with right-facing access. V1 rejected for excess depth; V2 has three packets and narrower construction. Native visual review and clean export log pass. Family now north/south/west; east and runtime installation remain outstanding.


## September 8 radial lighting and riser cutaways

Hidden risers now hide their light fixture housings in-game and in Room Layout
Studio; neighboring rooms and the wall hardware toggle also suppress unsupported
mounts. Interior and exterior illumination now use soft radial falloff. Native
cutaway, Studio, power-toggle and renderer checks pass; owner visual review pending.
See [lighting handoff](RADIAL_LIGHT_CUTAWAY_2026-09-08.md).

## September 8 communications service counter

The [communications bank](../assets/communications-service-wall-v1/README.md) adds patch leads, a compact tester/handset and clear repair mat. V2 quiets bright hardware. Native320-unit material/alpha and clean-log review pass; waveform and cables are static art, with placement and owner acceptance pending.

## September 8 spacious BRINE tube

[V4 portrait](../character/brine-comms-v4/README.md) fills the comms frame with
the wider tube interior, with outer supports beyond the crop. BRINE's scale and
animated bubbles are preserved. Native comms checks pass; owner review pending.
Bubbles subsequently enlarged and brightened, with staggered starting positions
so they are visible immediately. Native small-portrait review and comms checks pass.

## September 8 south botanical seed bank

The [south bank](../assets/botanical-seed-south-wall-v1/README.md) adds north-facing
drawers and container latches. Native320-unit material/alpha review passes; white
source background preserves pale edges. North/south indexed with added right
drawers recorded. Side views and room placement remain pending.

## September 8 textile counter four-direction coverage

The [south bank](../assets/textile-repair-south-wall-v1/README.md) completes four standalone textile directions after correcting the sewing throat toward the operator. Native material/alpha and clean-log review pass. [Family handoff](TEXTILE_REPAIR_FAMILY_2026-09-08.md) records independent dimensions, the basket companion and pending runtime placement.

## September 8 BRINE portrait correction

[V3](../character/brine-comms-v3/README.md) removes the bottom tube rim and adds
sparse animated bubbles masked behind BRINE. Native comms and foreground checks
pass; corrected artwork and prompt retained alongside earlier versions.

## September 8 seed-bank supported grouping

The [propagation-tray group](../assets/covered-propagation-tray-v1/README.md) places
the28-unit tray on the bank without overhang or sorting-tray overlap. Native/2x
static support review and hash checks pass. Hand clearance, lift animation and
runtime attachment remain unverified; original raster assets unchanged.

## September 8 east textile counter

The [east bank](../assets/textile-repair-east-wall-v1/README.md) adds left-facing access at320-unit length and67.65 visual depth. Native material/alpha and clean-log review pass. North/west/east indexed with independent dimensions; south and runtime placement pending.

## September 8 covered propagation tray

The [28-unit tray](../assets/covered-propagation-tray-v1/README.md) adds a closed
opaque companion for Hydroponics. V2 removes shiny bevels; native material/alpha
review passes. Backed vents stay opaque. Contents, support placement and owner
acceptance remain unverified; both sources and prompts retained.

## September 8 west textile counter

The [west bank](../assets/textile-repair-west-wall-v1/README.md) adds right-facing access at320-unit length and74.28 depth. V3 corrects orientation, tin latch and accessory scale. Native material/alpha and clean-log review pass; north/west indexed, south/east and runtime placement pending.

## September 8 botanical seed-storage wall

The [seed bank](../assets/botanical-seed-wall-v1/README.md) adds packets, sorting
tray and opaque tins for Hydroponics. Native320-unit material/alpha review passes.
V2 replaces a dark checkerboard that conflicted with pale cabinet edges; rejected
geometry retained. Static candidate, pending placement and owner review.

## September 8 BRINE tube comms portrait

The [tube portrait](../character/brine-comms-v2/README.md) puts BRINE inside her
canonical pale-collared glass chamber, preserving her established face and suit.
Installed in Comms; the original portrait is retained. Native reveal/replay and
1600/960 containment checks pass, with both sizes visually reviewed. Owner visual
acceptance remains pending.

## September 8 reusable alpha probe validation

The [pixel validator](ASSET_ALPHA_PROBES_2026-09-08.md) makes named opening/interior checks executable and hash-bound. Nine tests and the textile basket five-point check pass. Material workflow updated and installed reference synchronized. Selected pixels only; no new silhouette or runtime acceptance.

## September 8 textile repair basket

The [28-unit basket](../assets/textile-repair-basket-v1/README.md) adds a loaded fabric companion. Native/shared-scale review passes after black-background and rim repair, followed by registration spike cleanup. Named alpha probes include coordinates and export hash for reproducibility. Static art only; room placement and owner acceptance pending.

## September 8 directional registration guard

The [audit update](DIRECTIONAL_REGISTRATION_GUARD_2026-09-08.md) rejects changed
reviewed outlines and swapped registration paths. Sixteen tests and both four-view
chart/tool families pass. Legacy registration coverage is explicit; no new visual
or placement acceptance. Material workflow updated.

## September 8 textile repair counter

The [textile workbench](../assets/textile-repair-wall-v1/README.md) adds a compact sewing machine, clear cutting space and fabric storage. V2 corrects oversized equipment and bright hardware. Native320-unit material/alpha and clean-log review pass; static north-wall candidate with placement and owner acceptance pending.

## September 8 chart-counter four-view coverage

The [east counter](../assets/observation-chart-east-wall-v1/README.md) completes
four standalone chart-bank directions. Native320-unit material/alpha review and
four-view metadata audit pass. Sleeve construction and depth differences remain
explicit; room placement and owner acceptance pending.

## September 8 listening counter four-direction coverage

The [south bank](../assets/crew-listening-south-wall-v1/README.md) completes four standalone listening-counter directions. Native320-unit light/dark review and clean Godot log pass. Directional depths differ; room placement and owner acceptance remain pending. See [handoff](CREW_LISTENING_FAMILY_2026-09-08.md).

## September 8 west chart-counter candidate

The [west counter](../assets/observation-chart-west-wall-v1/README.md) adds east
access at320-unit length and74.01 depth. Native material/alpha review passes;
three-view family metadata checks pass. East art and room placement remain pending;
side-view storage differences are recorded.

## September 8 crew listening east candidate

The [east counter](../assets/crew-listening-east-wall-v1/README.md) adds left-facing controls and access at full320-unit length. Native light/dark material and alpha review pass. North/west/east are indexed; south and runtime placement remain pending.

## September 8 south chart-counter candidate

The [south counter](../assets/observation-chart-south-wall-v1/README.md) adds inward
north drawer access and a plain rear panel. Native320-unit material/alpha review
passes. North/south indexed with depth/construction differences; side views and
room placement remain pending.

## September 8 Observation chart folio

The [22-unit closed folio](../assets/observation-chart-folio-v1/README.md) adds a
matte canvas companion to the chart counter. Native alpha/material and supported
tabletop group review pass. Static art, pending runtime placement and owner review;
source, exact prompt and evidence preserved.

## September 8 riser-mounted fixtures and exterior beams

The [lighting follow-up](RISER_LIGHTING_2026-09-08.md) removes low north-strip
dressing and makes the riser the single light mount. Fixtures stay visible and
stationary when the riser is hidden; legacy low-light offsets/settings remain
readable. Brighter exterior cones point away from exposed edges, clearing the
riser crown and foundation. Native studio/station captures, migration, editor
regressions and hardware controls pass. Owner visual acceptance remains pending.

## September 8 Observation chart counter

The [chart bank](../assets/observation-chart-wall-v1/README.md) adds matte wood map
drawers, plotting surface and rolled-chart storage. Native320-unit material/alpha
review passes after base-fringe cleanup. Static standing counter; room placement
and owner acceptance pending. Source, prompt and revised bounds recorded.

## September 8 crew listening west candidate

The [west listening counter](../assets/crew-listening-west-wall-v1/README.md) adds right-facing player access and smaller headphones in backed docks. Native320-unit review passes;92-unit visual depth recorded separately from north. Family index tracks north/west with south/east absent. No runtime changes.

## September 8 wall-host evidence clarification

The [host review](WALL_HOST_EVIDENCE_2026-09-08.md) separates16-unit strip depth
from the owner-directed60-unit raised face. Notice-rail dependency hashes still
match; its schematic fit remains valid only for the strip. Workflow and asset
notes clarified, installed skill synchronized. No new mounting acceptance.

## September 8 audit report protection

The [family audit](DIRECTIONAL_FAMILY_AUDIT_2026-09-08.md) now protects linked files and unrelated JSON, writes atomically, and records failures instead of leaving an earlier tool-owned pass. Thirteen tests pass; water-assay and galley have valid protected-format reports. No art or runtime changed.

## September 8 mechanical tool four-view coverage

The [east bank](../assets/mechanical-tool-east-wall-v1/README.md) completes four
standalone directions. Native320-unit material/alpha review passes; all four
metadata records audit successfully. East75.21 and west70.47 depths remain explicit.
Room placement and owner acceptance are still pending.

## September 8 unrolled exercise mat

The [olive mat](../assets/crew-exercise-mat-v1/README.md) adds a28x57.11-unit floor candidate beside the exercise cabinet. V2 corrects the overly elongated source; native/shared-scale and alpha review pass. Unrolled static state only, with occupied clearance and placement pending.

## September 8 mechanical tool west candidate

The [west bank](../assets/mechanical-tool-west-wall-v1/README.md) adds east-facing
access. V2 narrows depth from102.13 to70.47 at320-unit length. Native material and
alpha review pass after rear-edge cleanup. Three directions indexed; east and
room placement remain pending. Sources and exact repair prompts retained.

## September 8 riser height and square-wall refresh

[Risers are 25% taller](RISER_WALL_REFRESH_2026-09-08.md) (48 to60 units), with
matching caps, returns, mounts and lighting. Eight rooms now use textured square
perimeters and corner caps. All44 furnished rooms were reviewed in four rotations;
44 cards refreshed. Native wall/adjacency checks pass. The broader Airlock test
reported five helmet-state failures, recorded separately for investigation.

## September 8 Room Studio usability follow-up

The [usability pass](ROOM_STUDIO_USABILITY_2026-09-08.md) fixes pointer-centered
previews, restored-default clearance and stable corner resizing. The tray now
has focused common categories, five more reusable props (45 total), and clean
registered-cutout thumbnails. Native title entry, normal-rule drag/drop and return,
save/reload, existing editor behavior and thumbnail shutdown pass. Category and
window-size captures were visually reviewed; owner hands-on acceptance remains.

## September 8 crew exercise storage wall

The [exercise cabinet](../assets/crew-exercise-wall-v1/README.md) adds modest weights, bands, mats and fabric storage. V2 reduces rubber-edge glints; native320-unit and alpha review pass. Static low storage candidate, with retrieval and occupied exercise clearance unverified. Placement and owner review pending.

## September 8 mechanical tool family metadata

The [family audit](MECHANICAL_TOOL_FAMILY_AUDIT_2026-09-08.md) verifies both source
dimensions and hashes and converts the index to the reusable directional schema.
Both indexed views pass metadata checks; east/west remain missing. South repair
history and final evidence now have hashes. Raster and visual verdicts unchanged.

## September 8 mechanical tool south counterpart

The [south bank](../assets/mechanical-tool-south-wall-v1/README.md) adds north-facing
access. V2 repairs pouch/drawer facing; V3 removes tool shine through dark sleeves
and plain spanners. Native320-unit and alpha review pass. North/south family indexed
with construction differences; side views and room placement remain pending.

## September 8 reusable directional audit

The [family metadata audit](DIRECTIONAL_FAMILY_AUDIT_2026-09-08.md) checks coverage, declared facing, hashes, review evidence and scale. Eight tests pass; water-assay and galley pass all four indexed views. Metadata validation does not establish visual or runtime acceptance. Production guide updated with the reusable command.

## September 8 playable character construction

The [construction handoff](CHARACTER_CONSTRUCTION_IMPLEMENTATION_2026-09-08.md)
replaces opening emergency-drone builds with an architect welding from an existing
room. Twelve directional loops and work-driven room assembly are integrated;
paid costs, ten seconds of manual work, interruption/save progress and later
dedicated drone builders remain. Twelve native actor/direction cases, save and
fleet regressions, sprite checks and the paid-opening fixture pass. Native review
also corrected full-wall cached drawing at completion. Owner pacing/animation
acceptance and a new packaged build remain separate.

## September 8 mechanic kneeling-pad companion

The [28-unit pad](../assets/mechanic-kneeling-pad-v1/README.md) adds a matte fabric
companion to the tool wall. True-alpha export and native/shared-scale review pass.
Pouch is closed; no kneeling behavior or placement is installed. Occupied posture
and clearance remain pending. Existing material/group workflow reused.

## September 8 crew listening wall candidate

The [listening counter](../assets/crew-listening-wall-v1/README.md) adds cassette trays, a player and two backed headphone docks. V2 replaces unintended book-like storage; native320-unit and alpha review pass. Standing counter candidate, no playback or seated-use behavior. Placement and owner review pending.

## September 8 mechanical tool wall candidate

The [tool bank](../assets/mechanical-tool-wall-v1/README.md) adds olive drawers,
recessed tools and a clear repair mat. V2 reduces shiny hardware; native320-unit
material/alpha review passes. Standalone, pending placement and owner review.
The [handoff](MECHANICAL_TOOL_WALL_2026-09-08.md) records a new graphical review
wrapper that rejects error logs even when a PASS marker appears; four tests pass.

## September 8 water-assay directional candidates

The [four-view handoff](WATER_ASSAY_DIRECTIONAL_CANDIDATES_2026-09-08.md) records north/south/west/east art. East native review passes; all source/export hashes match. Visible depth differences remain explicit. Standalone directional coverage complete; owner acceptance and runtime placement remain pending.

## September 8 water-assay west candidate

The [west bank](../assets/water-assay-west-wall-v1/README.md) adds a328-unit vertical view with right-facing access. V2 restores filtration tray and corrects analyzer orientation. Native material/alpha review passes; family now records north, south and west. East view and runtime placement remain pending.

## September 8 water-assay south candidate

The [south bench](../assets/water-assay-south-wall-v1/README.md) puts backing south and access north. V2 corrects individual analyzer/case facing; native328-unit review passes. North/south family index records exports and missing side views. Standalone, awaiting placement and owner review.

## September 8 reading-wall knee-recess variant

The [desk variant](../assets/lounge-reading-recess-v1/README.md) removes the
central lower panel/plinth while retaining side supports and matte reading art.
Native320-unit material/scale and alpha review pass. The opening measures85.36
units at the recorded sample; original wall preserved. Occupied seating and
runtime placement remain unverified; gallery refreshed.

## September 8 simplified Room Layout Studio

The [studio simplification](ROOM_STUDIO_SIMPLIFICATION_2026-09-08.md) adds WASD
camera movement, fourteen whole-room floor presets, visible doors, 50% new tray
placements and bottom-right drag resizing. A bordered thumbnail tray includes
Room Default and forty common props; objects drag out and back in. Coordinates
and saved arrangements leave the visible UI; secondary controls sit under Options.
Three graphical fixtures pass, including native drag preview/drop and 1600/960
visual review. Existing saved sizes remain; owner usability acceptance is pending.

## September 8 Lounge shared-scale arrangement

The [reading group](../assets/lounge-reading-stool-v1/README.md) pairs the26-unit
stool and320-unit wall in a native/2x diagnostic. Visual proportion, palette and
export/hash checks pass. The solid cabinet front has no knee recess, so occupied
reading posture and reach remain unverified; this is a static grouping proposal.

## September 8 cargo dolly state-pair review

The [state-pair handoff](CARGO_DOLLY_STATE_REVIEW_2026-09-08.md) verifies both exports at one crop and36-unit width. Native/2x static review passes; binary silhouettes overlap99.1%, with small recorded bounds drift. Runtime transitions and collision remain unverified. Existing casebook entry updated with this evidence.

## September 8 drone component wall candidate

The [drone service bank](../assets/drone-component-wall-v1/README.md) adds gripper
jaws, empty assembly cradle, actuator and diagnostics. V2 corrects inherited
battery-pack shapes. Native320-unit matte/scale and alpha review pass; gallery
refreshed. Standalone, pending placement and owner review. Reference-subject
transfer failure recorded in the casebook.

## September 8 archive trolley candidate

The [loaded archive trolley](../assets/archive-trolley-v1/README.md) adds a32-unit companion to the restoration bench. Native material/alpha and shared-scale group review pass. Loaded state and handle exclusions recorded; no hauling behavior or room placement added. Existing group and alpha workflow reused without adding duplicate skill rules.

## September 8 archive restoration wall candidate

The [restoration bench](../assets/archive-restoration-wall-v1/README.md) adds continuous cartridge intake, reading, sorting and preservation tasks. V2 reduces inherited bright trim; native328-unit and alpha review pass. Standalone, pending placement and owner review. Reference-transfer lesson recorded in the casebook.

## September 8 filter-service comparison completed

The [filter bank](../assets/filter-service-wall-v1/README.md) now has a clean native
comparison beside the furnished Life Support room at320 units. Visual scale
review passes; export hash is unchanged. The earlier renderer failure remains in
the history, and the gallery reflects the completed agent review. Placement and
owner acceptance remain pending; no floor code was changed in this art task.

## September 8 filter-service wall candidate

The [filter bank](../assets/filter-service-wall-v1/README.md) adds Life Support
filter shelves, inspection tray and test equipment. V2 corrects silver brackets
and paper highlights; isolated native material/alpha review passes. Full room
comparison remains pending after an undeclared `pads` error in the floor renderer.
The failed log is retained; no floor code changed. Gallery records partial scale
review and standalone status rather than a full visual pass.

## September 8 maintenance bench arrangement

The [case support proposal](../assets/seal-maintenance-case-v1/README.md) places the26-unit case on the pressure-seal mat with its full handle inside measured support bounds. Native group visual and export/hash checks pass; tools remain clear. Runtime attachment and occupied clearance remain pending. The faucet trial moved intact into the material casebook, preserving the concise daily guide.

## September 8 water-assay wall candidate

The [water-assay bench](../assets/water-assay-wall-v1/README.md) adds three unequal science task zones and clear preparation space. V3 replaces a persistently shiny faucet with a flat-sided spout. Native328-unit and alpha review pass; standalone, pending owner review and placement. Repair lesson recorded in the room skill.

## September 8 material workflow consolidation

The [workflow handoff](MATERIAL_WORKFLOW_CONSOLIDATION_2026-09-08.md) separates
the119-line daily guide from the preserved304-line casebook. Original text
preservation is hash-verified; maintained/installed skills match. All production
gates remain, with detailed future trials routed to case notes or asset records.
No asset or runtime changes in this maintenance step; art production remains active.

## September 8 Battery service wall candidate

The [battery bank](../assets/battery-service-wall-v1/README.md) adds pack cradles,
an inspection surface, cable trays and enclosed diagnostics. Native320-unit
matte/scale and alpha review pass; gallery refreshed. Four unequal task areas
vary the composition. Standalone, pending placement and owner review.

## September 8 maintenance case candidate

The [sealed maintenance case](../assets/seal-maintenance-case-v1/README.md) adds a26-unit engineering prop. V2 removes glow and excessive edge wear; native and handle-alpha review pass. Closed static candidate, not installed. Material-repair lesson recorded in the room pipeline.

## September 8 notice rail measured-size follow-up

The [rail handoff](../assets/crew-notice-rail-v1/README.md) now records a
131.74×14 alternative for the inherited16-unit wall strip. Native schematic
size/readability review passes with unchanged source/export. Fine marks become
decorative. Mounting-plane orientation, depth ordering and doors remain unverified;
no wall geometry or runtime art changed.

## September 8 group-preview validation

The [group diagnostic](PROP_GROUP_REVIEW_2026-09-08.md) rejects clipped crops/arrangements, invalid coordinates, stale hashes and export overwrites. Eight graphical checks pass; valid console/stool capture visually reviewed. This establishes static preview integrity, not room placement or collision.

## September 8 pressure-seal maintenance wall candidate

The [pressure-seal bank](../assets/pressure-seal-wall-v1/README.md) adds gasket storage, assembly space, enclosed testing and lubricant supply. V2 reduces bright tool and gauge hardware; native328-unit and alpha review pass. Standalone, pending placement and owner review. Edit-output transparency lessons recorded in the room skill.

## September 8 Crew notice rail candidate

The [notice rail](../assets/crew-notice-rail-v1/README.md) adds a shallow clock,
paper/postcard strip and personal-effects ledge. Native240-unit matte/scale and
alpha review pass; gallery refreshed. Host fit and owner review remain pending:
the25.50-unit visual height must not be used to justify raising the low hull.

## September 8 operator stool and group diagnostic

The [operator stool](../assets/operator-stool-v1/README.md) adds a modest22-unit companion to the analog control bank. Alpha and native visual review pass; a reusable Godot group board checks shared scale and export hashes. Static arrangement only, with occupied clearance and runtime placement pending.

## September 8 Lounge reading stool candidate

The [small reading stool](../assets/lounge-reading-stool-v1/README.md) complements
the wooden wall bank with matte fabric seating. Native26-unit scale/material and
between-leg alpha review pass; standardized gallery refreshed. Standalone,
pending placement and owner review. Seating approach/interaction remains separate.

## September 8 analog control wall candidate

The [analog control bank](../assets/analog-control-wall-v1/README.md) adds five connected olive console bays inspired by the owner references. Transparent export and native 328-unit visual diagnostic pass agent review. Standalone asset; room placement and owner acceptance remain pending.


## September 8 Ore sampling wall candidate

The [sampling bank](../assets/ore-sampling-wall-v1/README.md) adds mineral trays,
weighing/preparation equipment, an enclosed analyzer and sealed samples. V2
reduces silver edging and stone sparkle. Native320-unit matte/scale and alpha
review pass; standardized gallery refreshed. Standalone, pending placement and
owner review. Mineral-material guidance added to the skill and bible.

## September 8 gallery coverage refinement

The [material gallery](MATERIAL_REVIEW_GALLERY_2026-09-08.md) now includes22
standardized records, including multi-asset `*-review.json` files. All export
hashes and110 local links match. Three discovery/findings tests pass; duplicates
are rejected and written review findings are shown. Browser rendering remains
unverified. This is a candidate subset, not total room-art coverage.

## September 8 empty cargo dolly candidate

The [empty dolly](../assets/cargo-dolly-empty-v1/README.md) complements the loaded
prop. Native36-unit and alpha review pass. A state index records both exports,
small bounds drift and a proposed shared region; runtime transitions remain
unverified. Both are standalone candidates awaiting placement and owner review.

## September 8 Lounge reading and games wall candidate

The [reading bank](../assets/lounge-reading-wall-v1/README.md) adds books, games,
a reading surface and compact radio. V2 reduces bright wood-edge lines and grain.
Native320-unit matte/scale and alpha review pass. Standalone, awaiting placement
and owner review; warm-wood material lessons added to the skill and bible.

## September 8 loaded cargo dolly candidate

The [cargo dolly](../assets/cargo-dolly-v1/README.md) adds a small strapped-parcel
platform matching the packing area. Native36-unit and alpha review pass, including
handle opening and retained parcel checks. Loaded state is explicit; no hauling
or empty variant is installed. Gallery rebuilt with matching export hashes.

## September 8 Cryo recovery wall candidate

The [Cryo support bank](../assets/cryo-recovery-wall-v1/README.md) adds blankets,
recovery clothing, a preparation counter, monitoring dock and enclosed thermal
service cabinet. V2 repairs outer-edge flecks and bright trim. Native320-unit
material/scale and alpha review pass. Standalone; placement and owner review remain.

## September 8 cargo packing wall candidate

The [cargo wall](../assets/cargo-packing-wall-v1/README.md) adds weighing, packing,
labeling and open dispatch trays. Native328-unit and alpha review pass; records
describe the actual open-tray configuration. The gallery now has 16 standardized
candidates with matching hashes. This wall is uninstalled and awaits owner review.

## September 8 Quarantine preparation wall candidate

The [Quarantine bank](../assets/quarantine-preparation-wall-v1/README.md) adds
garment storage, a basin, transfer cassette, returns hatch and filtration cabinet.
Native320-unit matte/scale and alpha review pass; source-specific dark-background
cleanup retains the basin and garment. Standalone, pending placement and owner
review. Pipeline guidance extends the existing measured-threshold lesson.

## September 8 local material review gallery

The [review gallery workflow](MATERIAL_REVIEW_GALLERY_2026-09-08.md) gathers 14
standardized candidates with facing, scale and native-evidence links. All export
hashes and local links pass. Browser policy blocked the local-file preview, so
page rendering/filter interaction remains unverified. This is a record subset,
not total art coverage; ongoing asset production remains active.

## September 8 Storage Bay dispatch wall and dolly

The [dispatch set](../assets/storage-dispatch-wall-v1/README.md) adds a packing/
weighing wall at320 units and small cargo dolly at38. Native material/scale and
alpha review pass, including the dolly grab slot. V2 corrects shiny case corners
and bumper; rejected source retained. Both are standalone, pending placement and
owner review. Skill/bible guidance now preserves usable packing work surfaces.

## September 8 emergency response wall candidate

The [emergency wall](../assets/emergency-response-wall-v1/README.md) adds rescue
supplies, a folded stretcher, masks, trauma kit and incident terminal. V3 removes
persistent visor reflections; native 328-unit and alpha review pass. Earlier
revisions remain recorded. Standalone, with placement and owner review pending.

## September 8 acoustic service wall candidate

The [acoustic service bank](../assets/acoustic-service-wall-v1/README.md) adds
hydrophone preparation, recording storage, calibration and cable trays for the
Listening Post. Native 320-unit matte/scale and true-alpha review pass. It remains
standalone, with placement and owner review pending. The record initializer was
used for provenance; the art guidance now records complementary service tasks.

## September 8 specimen carrier candidate

The [specimen carrier](../assets/specimen-carrier-v1/README.md) adds a small sealed
laboratory case. Native 28-unit and alpha review pass, including transparent handle
and retained inspection-window checks. The new initializer captured provenance
before visual findings were added. Standalone; placement and owner review remain.

## September 8 reusable asset review initializer

The [record initializer](ASSET_RECORD_INITIALIZER_2026-09-08.md) replaces repeated
provenance setup with one command. It records hashes and native scale, rejects
stale sources and overwrites, and leaves visual/owner acceptance unset. Five
focused tests and real east-galley metadata/overwrite checks pass. The room skill
now documents its use for subsequent assets.

## September 8 medical supply wall and cart candidates

The [clinical supply set](../assets/medical-supply-wall-v1/README.md) adds a 320-unit
wall bank and 36-unit cart. Native matte-material/scale and alpha review pass.
Cart V2 reduces glossy rim/packet highlights; the wall required a bounded rear-edge
registration repair. Skill/bible lessons updated. Both remain standalone; placement
and owner acceptance are pending, with ongoing art production still active.

## September 8 salvage workbench wall candidate

The [salvage workbench](../assets/salvage-workbench-wall-v1/README.md) adds parts
sorting, mechanical repair, a vise and electrical testing artwork. True-alpha
export and native 328-unit review pass. The projecting vise needs actual operator
clearance review during placement; the asset remains static and uninstalled.

## September 8 cultivation service wall candidate

The [cultivation service wall](../assets/cultivation-service-wall-v1/README.md)
adds seed storage, potting, propagation preparation, mixing and irrigation artwork.
True-alpha export and native328-unit review pass. The review template separates
depicted functional bays from runtime behavior; this remains uninstalled static
art awaiting owner review.

## September 8 Crew linen wall and hamper candidates

The [linen utility set](../assets/crew-linen-wall-v1/README.md) adds a warm fitted
wall and a small 34-unit hamper. Transparent exports and native material/scale
review pass. Hamper V2 removes shiny frame highlights; darker checkerboards and
the handle opening required source-specific cleanup. Skill/bible lessons recorded.
Both remain standalone candidates, with placement and owner review pending.

## September 8 crew utility wall candidate

The [crew utility wall](../assets/crew-utility-wall-v1/README.md) adds clothing
storage, washing, drying, folding and linen supplies. V2 corrects upright drawer
facades into low overhead surfaces. Transparent export and native328-unit review
pass; it remains standalone and awaiting owner review. The skill records the
projection correction for future storage briefs.

## September 8 engineering repair trolley candidate

The [repair trolley](../assets/repair-trolley-v1/README.md) adds a small diagnostic,
tool and cable cart. V2 reduces silver tool rims and surface speckling. Native
38-unit review passes; its enclosed handle gap is verified in geometry and export
alpha. Standalone candidate, not installed or owner accepted. The skill records
individual tool finishes and enclosed-aperture checks.

## September 8 Airlock low side-wall candidates

The [Airlock side-bank handoff](../assets/airlock-side-wall-v1/README.md) adds west/
east low preparation banks with inward access. Both have transparent exports and
native 320-unit length review; they are companion designs with packed-suit drawers,
not exact side views of the hanging-suit wall. A stacked-elevation failure is kept.
The review tool now segments tall material details, with a passing horizontal
export regression. Skill/bible lessons updated; room placement remains open.

## September 8 station hardware sidebar

The [eight-control hardware panel](STATION_HARDWARE_2026-09-08.md) is integrated:
power, Comms, wall/foundation visibility, sprinklers, internal door locks,
interior/exterior lights and Pumps. Owner decision: Pumps gates existing water
production while preserving manual suspension; sprinklers are visual only.
Controls and feedback, save compatibility, compact Comms and power checks pass.
Native 1600/960 review is complete; owner playtest remains.

## September 8 four-direction galley candidates

The [south galley](../assets/galley-south-wall-v1/README.md) completes standalone
north/south/east/west artwork. The [family index](../assets/galley-wall-v1/family.json)
maps facing, backing, exports and reviews; linked hashes and alpha channels pass.
South native review passes after backing and tap corrections. All four remain
uninstalled candidates awaiting owner review; ongoing production remains active.

## September 8 equipment and deposit audio

[Three cues](EQUIPMENT_DEPLETION_AUDIO_2026-09-08.md) confirm helmet sealing,
helmet removal and newly depleted nearby deposits. Completed-state observation,
cooldowns and silent restore priming prevent repeated feedback. Focused audio
tests and native mixer capture pass. WAVs are in `output/audio-equipment/`;
previous Windows packages are unchanged.

## September 8 east-facing galley candidate

The [east galley](../assets/galley-east-wall-v1/README.md) adds the opposite-facing
vertical view, with controls and taps toward the left. Full328-unit native review
and alpha export pass; placement and owner review remain. The neutral-registration
helper now records its actual thresholds without changing silhouette geometry.

## September 8 Reactor and Loom wall candidates

Two [wall banks](../assets/reactor-loom-wall-v1/README.md) add Reactor cooling/
shutdown cabinets and a Gravity Loom calibration bench. True-alpha exports and
native 320-unit scale reviews pass. Reactor V2 corrects reflective pipe/handle
detail; Loom uses varied supported working heights and muted ceramic parts.
The skill and bible record those lessons. Both remain standalone candidates;
room integration and the ongoing wall-asset production goal remain open.

## September 8 west-facing galley candidate

The [west galley](../assets/galley-west-wall-v1/README.md) adds newly drawn vertical
art with right-facing controls and fittings. Two directional failures are retained;
V3 passes standalone 328-unit height and alpha review. The review tool now uses
taller native panels for side banks. Owner acceptance and room placement remain.

## September 8 underwater, work and hazard audio

[Twelve new sounds](EXPANDED_AUDIO_2026-09-08.md) cover swimming/suits/bubbles,
active mining/salvage, galley/medical/lab/cultivation details and distinct
oxygen/power/hull warnings. Local activity and warning cooldowns stay bounded;
continuous ambience remains at nine layers. Focused integration, native spatial
checks and mixer capture pass. WAVs are in `output/audio-expanded/`; previous
Windows packages remain unchanged.

## September 8 galley wall and meal trolley candidates

The [galley asset handoff](../assets/galley-wall-v1/README.md) adds a warm fitted
food-service wall and separate small meal trolley. Both have transparent exports,
source/reference records and native scale reviews; neither is installed or owner
accepted yet. The review tool now fits portrait enlarged details while preserving
true display scale in native previews, verified with both new assets.

## September 8 power-room wall assets

Two [standalone wall banks](../assets/power-wall-v1/README.md) add Current Turbine
intake/controls/cable storage and Heat Recovery exchanger/manifold/pump storage.
Transparent exports and native material/scale boards pass. Heat's repeated coil
shine required a plate-fin revision; the pipeline records the lesson. These are
candidate assets, not installed room layouts or changes to live machines.

## September 8 laboratory wall candidate

The [laboratory wall](../assets/laboratory-wall-v1/README.md) adds a continuous
science bench with sample storage, analysis, specimen examination, preparation,
wash and sterilization bays. V2 reduces chamber reflections; source provenance,
true-alpha export and native 328-unit scale review are recorded. Standalone and
awaiting owner review. The workflow now explicitly rechecks alpha after edits,
because this material correction returned an opaque checkerboard.

## September 8 airlock and return sound

[Five cues](AIRLOCK_RETURN_AUDIO_2026-09-08.md) cover pressure adjustment, seal
release, chamber ready, recall acceptance and safe empty-handed return. Full-cycle
gameplay and silent checkpoint-restore checks pass. WAVs and native mix captures
are under `output/audio-airlock/`; an intermittent capture shutdown warning and
clean diagnostic repeat are documented. Earlier Windows packages are unchanged.

## September 8 fitted operations wall candidate

The [operations wall asset](../assets/operations-wall-v1/README.md) translates the
owner references into a continuous matte gray-olive instrument bank. Transparent
export and native 328-unit scale review pass; owner review remains. This is a
standalone asset, not installed room art or a change to existing layouts.


## September 8 fitted room reference direction

The owner supplied six [interior references](ROOM_REFERENCE_DIRECTION_2026-09-08.md)
and prefers wall-length installations for room character. Subsequent art should
use varied functional bays, tactile retro-industrial controls and restrained warm/cool
lighting, retaining matte materials, modest scale, inward faces and top-down geometry.
This is art direction; no bulk room restyle or gameplay change was performed.


## September 8 recovery and crew audio

[Three new cues](AUDIO_RECOVERY_2026-09-08.md) confirm stable hazard recovery,
successful crew dispatch and actual cryo emergence. Crew Foley no longer overlaps
another crew cue's tail. Focused audio, dispatch and recovery assertions pass;
native mixer capture is clean. A transient fixture shutdown warning and its clean
diagnostic rerun are recorded in the handoff. Prior Windows packages are unchanged.

## September 8 Airlock wall asset and matte-style workflow

The [Airlock wall-bank handoff](../assets/airlock-wall-v1/README.md) adds a standalone
suit, fitting-bench and breathing-air bank. V1 was rejected for reflective tanks
and helmet glass; targeted V2 is exported with true alpha and reviewed at room
scale. It is not installed; side-facing views or a split layout must respect the
pressure chamber and fitting station before integration.

Owner direction now explicitly requires matte materials and modest prop scale.
The room skill and visual bible include separate material/scale review gates,
a review template, a reusable native export/scale-board tool, and milestone-based
feedback into the maintained workflow. Changed skill files are synced to the
installed snapshot. This revision does not restyle other rooms or change gameplay.

## September 8 industrial UI switch assets

The [switch asset handoff](UI_SWITCH_ASSETS_2026-09-08.md) records four industrial
switch families with off/on/disabled states and 12 Godot atlas resources. These
are dark-backed menu assets ready for selection and integration; live menus are
unchanged. Transparent cutouts and dedicated hover/focus art are not included.

## September 8 sound variation pass

The [variation pass](AUDIO_VARIATION_2026-09-08.md) adds subtle pitch/level variation
to crew and selected mechanical cues, shared crew burst limiting and pitch-aware
tail cleanup. Focused tests and a native repeated-cue mix capture pass. Source
playback is updated; previous Windows packages and base WAVs are unchanged.

## September 8 missing audio cues created

[Ten new original sounds](MISSING_AUDIO_CREATED_2026-09-08.md) cover construction,
drone launch, expedition outcomes, nearby crew Foley, Cold Store and Salvage Workshop.
Real triggers, cooldowns, distance gating and nine bounded ambience layers are
integrated. Audio, paid-construction and native spatial checks pass; WAV previews
and mixer evidence are in `output/audio-missing-cues/`. Earlier packages are unchanged.

## September 8 Holographic Core wall artwork

The [Holographic Core handoff](HOLO_WALL_2026-09-08.md) adds optical processors
and projection-control wall banks in all four orientations. Main projector and
calibrator retained; native visual/placement, eight floor anchors and production
crew routes pass. The card is refreshed. Gameplay and existing packages are unchanged.


## September 8 audio coverage and third pass

The [audio inventory](AUDIO_COVERAGE_2026-09-08.md) records current coverage and
remaining construction, expedition and crew Foley gaps. Incoming comms and manual
Save now have restrained feedback; queued messages do not chatter. Mechanical
variants start at a random sample. Focused integration and native mixer checks
pass. This source pass is separate from earlier frozen Windows builds.

## September 8 Data Archive wall artwork

The [Data Archive handoff](ARCHIVE_WALL_2026-09-08.md) adds eight directional
wall sections with inward controls and flush backing rails. Native four-orientation
review, eight floor anchors and production crew routes pass. The existing room
keeps its library/terminal and gameplay behavior. Holographic Core is a next-art
candidate, not started. The [earlier fourteen-room rollout](WALL_ROOM_ROLLOUT_ACCEPTANCE_2026-09-08.md)
is complete in the checkout; packages retain their recorded snapshot scopes.


## September 8 Cold Store

Owner requested smaller, less shiny props. Matte V2 now uses charcoal panels,
subdued ochre and simpler pixel detail; live width is reduced by 25.8%. Native
card/room and clearance checks pass. See the Cold Store handoff for revision evidence.

The [Cold Store handoff](COLD_STORE_2026-09-08.md) adds a through-room with
refrigeration, ingredient weighing and stock-check visits. It adds 40 Food and
20 Biomass capacity, consumes 1 Power/cycle, and retains capacity during outages.
Connected Galley operation offers a hidden discovery. Paid connected construction,
crew routes, storage/discovery and native visual checks pass. The roster now has
47 identities. No standalone package was rebuilt for this addition.

## September 8 second audio mix pass

The [second mix pass](AUDIO_MIX_PASS_TWO_2026-09-08.md) preserves short UI cue
attacks, gently ducks ambience under priority sounds, and isolates music shuffle
randomness. Focused audio tests and a native stereo capture pass with no clipping
or dropped capture frames. These are source changes; previous Windows packages
remain frozen. Listening acceptance and a future package update remain separate.

## September 8 compact comms popup

The owner requested a smaller rectangular popup with only Next and X. This
supersedes the expanded conversation controls and floating inbox. Dialogue now
uses a 520x170 logical panel with a smaller portrait and disappears five seconds
after text completes; queued dialogue advances in order. A dedicated COMMS button
in the side panel reopens it. Native timer, queue, control-count and 1600/960
viewport checks pass. See [comms handoff](CREW_COMMS_HANDOFF_2026-09-08.md).

## September 8 audio Windows playtest

The [audio build handoff](AUDIO_PLAYTEST_BUILD_2026-09-08.md) records a fresh
Windows package at `output/audio-playtest-20260908/build/`. All six native package
checks pass, including positional sound, settings and normal gameplay save/quit.
Audio now drains before normal closing. Exported settings received visual review;
headphone/speaker listening remains with the owner. Earlier packages are unchanged.
This snapshot includes then-current room/editor work but does not establish full
acceptance of those concurrent changes; its manifest records the included files.

## September 8 tiled-floor Windows playtest

The verified package is `output/tiled-floor-playtest-20260908/build/BrineSpace.exe`.
Keep its PCK alongside it. Open Room Layout Studio → Research Lab or Corridor →
Floor tiles. Five exported checks pass, including floor editing/pixel comparison,
connected station/collision, editor workflow, menu/save recovery and music restart.
Packaging caught and fixed shared music playlist ownership. Quarantine uses its
previous complete production view in this snapshot; later checkout work remains
separate. See the [pilot report](TILED_FLOOR_PILOT_2026-09-08.md) for exact scope.

## September 8 Galley

The [Galley handoff](GALLEY_2026-09-08.md) adds a warm Crew room with a pantry,
stove/sink bank and serving counter. Cooking converts 1 stored Biomass, 1 Water
and 1 Power into 4 Food. Hungry crew take meal breaks; connected Hydroponics
offers a hidden discovery. Paid construction, economy, crew and native art checks
pass. The roster now has 46 identities. Standalone packages remain unchanged.

## September 8 Salvage Workshop

The [workshop handoff](SALVAGE_WORKSHOP_2026-09-08.md) adds a paid Engineering
room with workbench, parts shelves, repair press and crew tote deliveries.
It converts 3 stored Metal and 2 Power into 1 Rare Mineral per functioning cycle.
A connected salvage bay offers a hidden discovery using the existing three-cycle
stabilization rule. Native art, economy, paid construction and crew checks pass.
The room roster now contains 45 identities. No standalone package was rebuilt.

## September 8 tiled floor pilot

The [tiled floor pilot](TILED_FLOOR_PILOT_2026-09-08.md) adds cached floor meshes
and paint/fill/rectangle/variation tools to Research Lab and straight Corridor.
Default pixels and corridor clipping are verified; native editor, save/reload,
undo, connected-pair and collision checks pass. The edited-floor submission
microbenchmark improves by about 69%; no whole-game speedup is established.
Review it in the current checkout or the tiled-floor Windows package above.

## September 8 positional station sound

The [positional audio pass](POSITIONAL_AUDIO_2026-09-08.md) adds camera-relative
local sounds, saved Effects/Ambience controls, bounded room-character layers,
short music rests and small missing cues. Global warnings and the existing
polished assets remain. The handoff records source/native checks and listening
limits. Earlier frozen Windows packages are unchanged.

## September 8 game performance and regression pass

The [performance/polish report](GAME_PERFORMANCE_POLISH_2026-09-08.md) records
6.5–8.4% lower measured frame times in 50/100-room fixtures, saved-layout visual
refresh, native prop restoration on reset, and crew collision cache fixes.
19 final source fixtures and five exported gameplay/editor workflows pass.
The frozen Windows package is `output/game-polish-playtest-20260908/build/`.
Startup loads, with a remaining forced-shutdown audio resource warning; large
station overviews and first-frame rebuilds still need further optimization.
Concurrent edits after the source snapshot are outside its acceptance.

## September 8 Observation Room

The [Observation Room handoff](OBSERVATION_ROOM_2026-09-08.md) adds a paid Crew
blueprint with a giant north porthole, two side bookshelves and owner-requested
square corners. This version has a fixed south entrance and no resource output.
Native card/clearance checks, paid construction, Save/Continue and a crew return
route pass; three window sizes were captured. The live roster now has 44 identities.
The darker room now includes the wooden desk, rear-facing chair and lamp/open book.
All three crew alternate seated reading and window visits, with interruption and
snapshot restore checks. See [reading handoff](OBSERVATION_READING_2026-09-08.md).
No standalone package was rebuilt; owner visual review remains separate.

## September 8 music and sound polish

The [audio polish pass](AUDIO_POLISH_2026-09-08.md) matches music/loop loudness,
installs 15 shorter event edits, crossfades music, lowers it briefly for priority
cues and reduces repeated warnings. Source audio and station-system checks passed;
the handoff records mixer-capture evidence and listening limits. The existing
Windows playtest package predates these edits and remains unchanged.

## September 8 targeted Windows playtest package

The frozen local Windows debug package at
`C:/Users/Alex/Documents/Codex/2026-09-07/can/outputs/BrineSpace-Windows-Playtest`
passed six targeted native acceptance cases: title/architect selection, loading
and Continue, station systems/crew salvage/replay, save restoration, paid mining,
and paid salvage. Its README and evidence identify the exact snapshot and checks.
PCK SHA-256: `ab749328e96ad28bbe000b4a5070bd9a7aa41970dcce0496834201545b40a288`.
Final normal-entry startup also exited without engine errors. Headless paid checks
passed gameplay assertions but reported Ogg resources alive at shutdown; native
repeats were clean after explicit fixture music cleanup. Broader shutdown
reliability, subjective pacing and the owner-supplied audio mix still need review.
This is bounded acceptance of that package, not the older 21-case suite or later
checkout edits. No balance changes or online publication were performed.

## September 8 Suno audio integration

The [Suno audio handoff](SUNO_AUDIO_2026-09-08.md) records the owner's 27 supplied
exports: four Moonlit music tracks, station/ocean/airlock/drone loops and event
effects. A persistent playlist and saved music-volume control are integrated.
Original WAVs remain in Downloads. Focused source validation is separate from
in-game listening and packaged-build acceptance; the mix still needs owner review.

Guidance reconciled September 7, 2026 (Vancouver). Update this page at meaningful
owner decisions or acceptance milestones; keep detailed evidence in dated reports.

## Accepted direction

Restore a silent underwater station through satisfying placement and interdependent
systems. The underwater visual bible supersedes the old orbital setting.
Normal play uses paid construction, resource failures, hidden discoveries and three
functioning stabilization cycles. Starting doctrines, timed directives and scenario
victory are retired; Conclude Expedition ends the open loop. Do not restore them
from old balance notes. Preserve deliberately provisional systems unless the requested
change calls for revisiting them.

## Latest recorded integrated acceptance

The [September 7 build/playtest report](INTEGRATED_BUILD_PLAYTEST_2026-09-07.md)
records 21 automated acceptance runs on one frozen Windows debug package, repeated
whole-crew traces and a normal title-launch smoke check. It completes the combined
build and bounded packaged-test step that was still open in the
[September 6 handoff](BRINESPACE_HANDOFF_2026-09-06.md).

That result belongs to the package and source baseline identified in the report.
The checkout contains later/uncommitted work; the report is not blanket acceptance
of the current tree. Check the relevant diff before reusing its evidence. No new
build, gameplay test, release or publication was performed for this documentation update.

## Remaining work and next action

1. Play a short normal paid expedition from the recorded build. Focus on opening
   power/charging feedback, recovery choices and human pacing. Controlled tests found
   substantial one-generator charging waits; they do not establish a universal
   generator requirement or authorize an automatic balance change.
2. Review the new crew salvage expedition's pacing and sound mix in normal play.
   The September 8 systems pass connects chamber transit, exterior salvage and safe
   return; targeted packaged checks now pass, while human pacing review remains.
3. Complete continuous animation/art review, including provisional swim/helmet
   transitions. Headless checks and manifests do not establish visual approval.
4. Resolve larger-station performance (including 101-room scenarios), broader
   gamepad/display/hardware coverage and release-size optimization as relevant work
   is scheduled. These remain separate from the bounded debug-package acceptance.

The next useful step from the recorded acceptance is the human opening-power playtest.
A later owner request can change that priority; this page does not authorize unrelated
work or a new asset-generation batch.


## September 8 storage cleanup

The [storage handoff](STORAGE_CLEANUP_2026-09-08.md) records owner-authorized removal
of 215 temporary/rejected/older EXE/PCK files, totaling 157.26 GiB. Artwork, source,
Git, review evidence and current accepted builds were preserved. Historical
batch-two/room-rollout/production-ten binaries named in the removal log are no
longer locally replayable; their recorded test results remain historical evidence.
Export-tool automatic temp cleanup remains unimplemented. This was storage and
documentation maintenance, not new gameplay or visual acceptance.
