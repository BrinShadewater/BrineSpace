# Project handoff

Updated: September 26, 2026 · BrineSpace · Furnished room prototype integration

## Objective and acceptance
Continue from the installed prop collection: furnish the new rooms and connect aquarium
and survey-probe motion to gameplay. Native gallery: http://127.0.0.1:8780/new-room-props-2026-09-26/furnished.html .
Agent visual/technical review completed; owner visual acceptance and balance review remain.

## Accepted decisions and constraints
Preserve original art, 188 authored layouts, 323 original catalog records, owner saves
and Studio marks. Current painted industrial bible, .34 world units per export pixel.
Cinema seats face the screen; botanical dome is central. No new source art generated.
No answer arrived to the optional room-economy question: implemented explicitly
provisional costs and resource outputs, without changing existing balance or starting
unlocks. New blueprints use the existing Archived Data shop.

## Current state
28 additional room definitions, 112 layouts, 28 baked cards; 75 room types total.
Definitions/views/layout candidates: rooms/new-room-expansion/. Live layouts/catalog:
rooms/full-wall-v1/. Cards: assets/new-room-cards/. Existing owner layouts override defaults.
Shared shell and lazy view registration preserve existing rendering. 38 new GDScripts
have paired UIDs. New prop metadata includes default-room associations and tank windows.

Aquarium: scripts/aquarium_life.gd draws the approved three swimmers, six plants, two coral
clusters and habitat inside both tanks. Exact 48-second cyclic motion; game pause freezes
the clock. Life continues during power outages. Existing tank paintings remain untouched.

Survey: scripts/survey_probe.gd and survey_probe_art.gd use the current eight-heading
32-second mission pack. Each room quarter has a fitted launcher opposite the entrance.
The warning light rotates before launch; blue active/red held/yellow charging or unpowered
status follows runtime state. Empty launcher stays visible. Hull clips the passing body.
Existing exploration sources reveal terrain/resources; no resources are conjured by scans.
Per-room survey_clock is saved in existing placed-room snapshots and validated on load.
Pause, lost allocation/power, suspension and obstruction hold the mission. Old checkpoints
without the new fields remain valid. The local circuit repeats and has no global routing.

Changed integration hooks: room_database, grid_canvas, main, underwater_visibility,
room_asset_library, room_content_canvas, room_card_art and run_save. No main refactor.
New tools: build_new_room_layouts.py, bake_new_room_cards.gd, prepare_new_room_uids.gd,
review_new_room_gameplay.gd, build_new_room_gallery.py. Tests: test_new_room_expansion.gd;
the Studio count assertion now follows the database. tests/index.json has a scoped group.

## Verification
- 112 native views; 17,920 walking samples; zero failures or visual overlaps.
- All 28 default views visually inspected with production Bill; cinema, dome and all four
  launcher orientations separately reviewed after fitting adjustments.
- 38,512 runtime assertions: continuous paths, loop seams, real survey memory, pause,
  power/suspension, obstacles appearing before/during launch, resume and checkpoint restore.
- Native live renderer: 36 probe phase/direction captures and five aquarium phases, clean
  engine log. Captures establish sampled states; continuous source preview and path checks
  establish timing, not a full native motion-video acceptance.
- Studio regression passes for 75 entries; 300 authored layout keys pass. Gallery loads
  all 112 views and 36 mission captures, filters work, no browser errors.
- Original 188 layout values, 323 prop records, owner room_layouts.json and all four mark
  files unchanged. New PNGs resolve to Git LFS attributes. No export/release claimed.
- Headless runtime test passes but engine shutdown reports four Ogg playback objects/two
  audio resources held. Verbose output names station-music tracks, not new room resources.
  Native capture/Studio runs exit cleanly. Do not mislabel this as a gameplay assertion failure.

Evidence: assets/new-room-props-2026-09-26/{furnished-review,gameplay-review,integration.json};
focused logs in rooms/new-room-expansion/. before-integration/ preserves pre-turn files.

## Next action
Owner reviews furnished.html and the provisional room economics before a balance pass.
Room-specific interactions/recipes beyond the stated generic resource outputs are not
implemented. Survey bays need a clear exterior route; they wait instead of finding a
different route. Directional launcher paintings are not articulated hatch machinery.
Ocean-life files remain reusable assets, not outdoor spawns. New room prototypes have
not been packaged into a playable release. Preserve other concurrent work in this checkout.
