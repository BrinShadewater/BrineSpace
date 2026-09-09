# Room Layout Studio

Open **Room Layout Studio** from the title screen or press **F8** during play.
The expedition pauses until the studio closes. Choose a room and orientation;
local layouts apply to every instance of that room and orientation.

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

## Floors and doors

Choose **Floor finish** and click a preset to replace the whole room's floor.
All fourteen registered floor sources are available, plus **Room default** to
restore the authored floor. There are no paint brushes, individual tile swaps,
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
