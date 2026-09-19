# Room Layout Studio

Open **Room Layout Studio** from the title screen or press **F9** during play.
The expedition pauses until the studio closes. Choose a room and orientation;
local layouts apply to every instance of that room and orientation.

**Show character** on the toolbar stands a crew member in the room at gameplay size,
for judging scale. The side panel's **Scale:** picker chooses Bill, Marsh, Branforth or
Veld, and the menu beside it offers Standing, Walking and Place. The choice is a preview
preference and never enters a layout. Settle prop size once against a crew member before
decorating: library props share one scale, so one decision covers all of them. View options
(Options panel open, snap, alignment guides, entryway areas, clean preview, riser wall,
foundation, lights, animation, zoom and the character) carry over between rooms and
rotations and are saved beside the layouts in `user://room_layouts.json.studio.cfg`.
Free placement is part of each layout, not a view option.

## Direct editing

- **WASD** moves the camera. Middle-drag also pans; the mouse wheel zooms.
- Drag artwork from the **Asset Tray** into the room. Its drag preview follows
  the pointer at placement scale. New placements start at **50%**.
- Click a placed object to select it. Drag it to move, or drag its **bottom-right
  corner** to resize proportionally. Size % remains available for exact sizing.
- Drag an object back over the tray and release to remove it. Delete and
  **Return selected to tray** do the same thing. Undo restores it.
- Arrow keys nudge selected artwork; Shift nudges twelve units. Shift-click
  selects multiple objects; Ctrl-click cycles overlapping objects.
- R / Shift+R changes room orientation. Ctrl+S saves; Ctrl+Z / Ctrl+Y undo/redo.
  Keyboard shortcuts are suppressed while typing in a field.

The tray categories are **Room Default**, **Common props**, **Wall installations**,
and **All assets**. Room Default shows the selected room's native prop artwork,
including pieces already placed. Dragging an already placed movable default adds
a copy. Fixed baked wall artwork stays attached to its hull.

Common props includes forty-five reusable fittings and furniture pieces. Focused
filters separate Seating, Storage & carts, Small props, and Wall fittings without
adding another row of controls. The latest additions are a reading stool, meal
trolley, book trolley, linen hamper and sealed carry case. Search filters the
current category. Thumbnails use registered cutouts, including older props whose
source artwork has a solid background.

### The tileset library

About 10,900 bought props in 42 sets load from `rooms/tileset-library/props.json`.
Two dropdowns narrow them and combine: the first adds a **kind** filter per category
(Storage, Seating & tables, Screens & computers, Lab & science, Medical, Plants &
growing, Power & reactor, Industrial & workshop, Water & marine, Ship interior and
more), the second picks a **set** (Galley, Hydroponics, Infirmary, Undercity…). Search
matches the label, the set and any name you gave a prop. The tray lists 280 entries at
a time; the **◀ ▶ pager** under it reaches the rest and shows the range (`281–560 of
926`). Previews render one per frame, and a progress bar under the tray title counts
them in. **In this room** lists only what is already placed here, for reusing the same
chair or console. Resting the pointer on an entry shows it enlarged, straight from the
sheet, beside the tray.

**Group look-alikes** shows one tile for each family of near-identical props (the same
rack with different guns, the same monitor with a different screen), marked `×N`. About
a fifth of the library folds away. Nothing is hidden for good: select the tile and press
**Variants (N)** to list the family, **◀ Back** to return. Stars, marks and In this room
always list every prop.

Where a set has been given **titles**, the tray shows what a prop is ("Centrifuge,
benchtop") instead of its library label ("Lab 121"); search matches both, the tooltip
keeps the label, and a name you give with Rename still wins.

**New props at %** (side panel) is the size a prop starts at when dragged in. Library
props share one scale, so set it once against a crew member and every placement
follows; placed props keep their own size. It is remembered between sessions.

With a library prop selected in the tray:

- **☆ Star** adds it to **★ Favourites**, the first tileset filter.
- **Mark for removal** takes it out of the tray and lists it under **Marked for
  removal**. Nothing is deleted until an agent sweeps the list. Right-click does the same.
- **Move to category…** refiles it. Picking its original category clears the move.
- **Rename** gives it a name of your own, used in the tray, the sidebar and search.
  Clear the field to go back. A prop is a region of a shared sheet, so no file is renamed.
- **Split in two** is for two objects boxed as one. It cuts at the emptiest line through
  the middle and refuses when there is none. The entry keeps its identity as the first
  part, so placed copies still resolve; the second part joins the tray.

Ctrl-click or Shift-click selects several entries; Star and Mark for removal then act
on the whole batch. Your stars, marks, names and moves are saved beside the registry in
`favourites.json`, `retired.json`, `names.json` and `categories.json`. They are yours:
agents read them and act on them, and never reset them.

## Floors and doors

Choose **Floor finish** and click a preset to replace the whole room's floor.
The registered floor sources are available, plus the finishes listed in
`rooms/tileset-library/floors.json` (deck plates, panels and tiles cut from the bought
packs), plus **Room default** to restore the authored floor. A finish is drawn over the
authored floor: **Finish strength** under the list sets how strongly, from 20% to 100%
(42% unless you change it). It is per room, saves with the layout, shares undo, and
survives trying another finish. Adding a finish is
data only: a 192px image of one tile repeated 4×4, and a caption in `floors.json`.
There are no paint brushes, individual tile swaps,
variation seeds or rectangle-fill tools in this UI. Changes share normal undo,
redo and Save, and appear in runtime rooms as well as the preview.

Doors render at the selected room's actual ports even when clearance guides are
off. The low north-wall strip has no decorative overlays. Wall dressing belongs
to the riser; lights have one riser-mounted position and stay visible when the
riser is hidden. The workspace framing leaves room for those fixtures in either
view. Older low-light offsets are translated to the riser when loaded, while
explicit raised layouts and light settings are retained. **Options** contains snapping, alignment and door-clearance guides, free
placement, lighting/animation previews, riser/foundation visibility, view fitting,
original comparison, Reset and Save all rotations. Coordinates, the duplicate
object list and saved-arrangement controls are removed from the visible UI.

Existing arrangements retain their saved object sizes. Only new tray placements
start at 50%. Bounds, overlap and doorway checks still apply unless Free placement
is enabled. An invalid resize reverts; dragging a corner creates one undo step and holds the
opposite visual corner in place. Restoring a returned default also checks clearance.
Whole-wall assemblies resize as a unit; individual baked objects cannot be split.

## Persistence and review

**Copy to other rotations** (beside Save) uses the rotation you are looking at for the
other three. The room stays riser-north at every rotation and only the open door sides
move, so the composition is kept: a prop moves only where a door approach at that
rotation forces it, by the shortest way out. A rotation that still fails validation is
left as it was and named in the status line, for you to finish by hand. Look at each
rotation afterwards; validation permits a layout, your eye accepts it.

**Save** writes `user://room_layouts.json`, independently of expedition saves.
Per-orientation drafts, cross-room copy/paste, undo, recovery and adoption of local
layouts as project defaults remain supported. Previously saved arrangement files
are left on disk but the arrangement feature is no longer exposed.

Ask Codex to review the saved room/rotation and adopt it as a default. The existing
`tools/review_saved_room_layouts.gd` tool lists drafts; `-- --promote=ASSET/QUARTER`
validates and adopts one orientation into `rooms/full-wall-v1/default-layouts.json`.
Runtime editing does not rebake static cards.

## Validation

Run Godot 4.6.1 with `--path . --script res://tests/test_simple_room_studio.gd`
for native tray drag/preview, return drag, corner resizing, WASD/typing guard,
all floor finishes, persistence and 1600/960 captures. The broader
`tests/test_room_layout_editor.gd` and `tests/test_layout_workflow.gd` fixtures
cover runtime application, rotation, groups, lights, copy/paste and recovery.
All use isolated layout files under `output/layout-editor/`.

The follow-up `tests/test_room_studio_usability.gd` fixture enters through the
native title-screen button and checks actual pointer-aligned tray drops, reverse
drags, rejected default restoration, all five new props and focused filters with
Free placement disabled. `tests/test_layout_performance_guards.gd` checks tray
retention, recovery, bounded undo, and safe thumbnail shutdown.

`tests/test_tileset_library_tools.gd` covers the library controls: star and the
Favourites filter, move to category and back, batch marking, rename, Split on two
stacked chairs, all four crew in the picker, floor footprints including the mirrored
case, and every finish in `floors.json`. It redirects the registry and all four owner
files under `output/`. These three are native-lane tests: run them with
`python tools/run_tests.py --native --only <names, comma-separated>`.
