# Station props v2 (September 24–25, 2026)

Built on branch `room-props-v2`, now merged into `main`. Owner direction: a clean
slate of room art. Every redesigned room is dressed only with props cut from the
owner's Codex room designs (`Desktop/BrineSpace Room Designs`), on the existing
floors, riser walls, doors, crew and drones.

## What changed

- **Props.** 322 station props, ids `sp-<room>-<n>` and `sp-<theme>-extra<k>-<n>`.
  Art: `assets/station-props-v2/`. Catalog: `rooms/station-props-v2/props.json`
  (category, default rooms, region, footprint, collision, role, floor piece).
- **Rooms.** 43 rooms show only station props. BRINE Core, corridor, corner and
  tee corridor keep their pre-v2 art (`Library.LEGACY_ART_ROOMS`). Built-in view
  props and full-wall banks are filtered out by `Library.keeps_in_room` /
  `strip_retired`, except live machinery.
- **Live machinery** stays as the game drives it: drone docks and drones
  (`*_hatch`, `*_rov`, placed on the painted pads), the airlock pressure chamber
  and outer hatch, and the two cryo pods (centred where the painted pod was).
  Replacement art for these is future work.
- **Rotation.** Props keep one facing. `build_catalog.py` turns positions with the
  room, keeps wall-contact props on their wall, clears doorway mouths, holds
  centrepieces and places painted props clear of live machinery. The owner has
  since hand-adjusted every room in the Studio (saved layouts are authoritative).
- **Collision.** Station props block their front 60% only (top-down art); floor
  pieces (hatches, pads, the lounge rug) block nothing, draw under crew, and get
  no contact shadow. The lounge set is split into rug + furniture.
- **Contact shadow** from each prop's silhouette (`CONTACT_SHADOW` in
  `scripts/room_asset_library.gd`); painted drop shadows were removed.
- **Crew behaviour** keys on catalog roles: `bunk`, `freezer`, `galley_counter`,
  `observation_sofa`, `lounge_seat`, `life_support_console`, `holo_projector`,
  `suit_locker`. Blocked fronts are worked from behind; the airlock locker keeps
  free floor to its west (crew face east). Bunk-entry choreography of the retired
  bought bunk is not carried over (owner decision): crew use the generic sleep pose.
- **Departments.** Seven: Operations (red), Engineering (yellow), Science (blue,
  includes medical), Life Support (green), Recreation (orange), Anomaly (purple),
  Robotics (cyan: BRINE Core, the three drone bays, Data Archive). Saves hold room
  ids, so no migration.
- **Studio tray.** Default, Common Props, Floors (finish picker), Walls (riser
  material per room, saved as `wall/riser`), then the seven departments. Pre-v2
  native art does not paste into redesigned rooms.
- **Raised north wall** reaches the deck with no seam bands (the banks that hid the
  gap are gone).
- **Cards.** 44 room cards rebaked from the owner's final layouts; synergy cards and
  the codex draw from them.
- **Retired art.** 240 tileset sheets (180 MB) moved to
  `Desktop/BrineSpace Retired Assets 2026-09-24/` with a checksummed manifest; list
  in `rooms/tileset-library/retired-sheets.json`. Loading skips them quietly.

## Pipeline

Tools in `tools/room_props_v2/` (the model cutter needs the venv
`C:/Users/Alex/.venvs/brine-cutout`; SAM weights `sam2.1_b.pt` download on first run):

1. `extract.py` finds each prop on the design sheets (boxes, `props.json`).
2. `build_catalog.py` writes the catalog, art copies and default layouts
   (categories, roles, floor pieces, live anchors/obstacles from `tags.json`).
3. `model_cut.py --install` replaces the art with BiRefNet + SAM 2.1 cutouts and
   applies per-prop repairs from `overrides.json` `_model_cut_fixes` (SAM clicks,
   solid rectangles, shadow peel, floor trim, rug split). It keeps each canvas, so
   saved layouts do not move; a cut that grows its canvas adjusts the catalog and
   default layouts.
4. Rebake cards: `godot --path . -s res://tools/bake_room_cards_v2.gd`.

Owner layouts (`%APPDATA%/Godot/app_userdata/BrineSpace/room_layouts.json`) are the
source of truth for placement; backups sit in the Desktop folder's `owner-data/`.

## Tests

CI checks (`test_layout_keys`, card binding, release) pass. Tests pinned to retired
props were refitted to station props (Studio tests run their native-prop checks in
BRINE Core) or retired with a reason in `tests/index.json`. The failures that predated this work are fixed (Sept 25): full run 162/162
headless and 73/73 native pass, 21 retired skips. Recurring cause: tests that
clear wrecks by hand need `set_meta("authored_site_fixture",true)` now that new
games use procedural sites.

## Open

- Step 8b (retire the remaining pre-v2 room art) was surveyed and skipped: every
  bank/common-asset sheet is also loaded by a room view, and each room's source
  sheet also supplies its wall and cap material. Revisit with the wall/machinery
  art pass.
- Crew suits read too blue beside the warm bunk (owner, Sept 26): Bill, Veld and
  Branforth. In-game pixels match the source art, so this is an art-direction pass for
  Codex, not a renderer tint. The bunk clips were also painted darker and crisper than
  each walk cycle; a colour match to the walk cycle was tried and reverted (it looked worse).
  Crew draw at about 37% of their painted size with nearest sampling (speckled). Mipmapped
  smoothing was built and compared in game; the owner kept nearest, since smoothing blurred
  faces. Crew art painted nearer its on-screen size is the likelier fix.
- Drone and live-machinery art: owner doing it in Codex (Sept 26). The Codex room
  designs paint each drone onto its pad, so flying drones need separate exports.
- Bunk climb-in: done Sept 25 for all four crew on `sp-crew_hab-3` (points are fractions
  of the art; front layer is the rail, ladder and end posts). The five bunk tests run again.
  The seated frame used to sit on the drawers, then jump up (the "dip"); since Sept 26 it
  sits on the lower mattress edge (`BUNK_SEAT_ROWS` in each crew script, from the art).
- Release: Mac and Windows twins `brinespace-ffebeef84bf5f143` (see CURRENT_STATUS). The
  continuation check needs a fresh frozen mid-game save; the Sept 23 one starves on load.
- Airlock spare-helmet shelf: done Sept 25. It sits on the locker's left panel, or
  at the foot of the left bay when a wall or furniture takes that side
  (`side_shelf_blocked` in `airlock_view.gd`); the airlock card was rebaked.

## Powered effects (Sept 25)

While a room is powered, station-prop monitors (`operating_screens`) show a faint
wash plus a display chosen by the glass's shape: radar sweep on large wide screens
(≥10,000 px², aspect 1.3–2.6), waveform on wide ones, level bars on square/tall ones
(`draw_station_screens` in `scripts/room_asset_library.gd`; older library art keeps
the single trace). The detector skips angled side monitors, so `tags.json`
`screens_add` lists their glass by hand; loosening the detector instead flagged
visors, solar cells and a mug. Catalog `effects` kinds: `specimen_glow`, `field`,
and `hologram` (Holo Core bench lens). The Holo Core projector's beam got a faint fill.
- Owner's Codex magenta re-export pass: [brief](CODEX_BRIEF_MAGENTA_PROPS.md).
