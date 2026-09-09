# Room Layout Studio workflow additions — September 8

## Corridor workflow closeout - September 8

Preserve owner overrides while updating defaults. Variant choice belongs in live
floor rendering/cache keys, not only cards. New corner selections alternate west/south
and east/south using completed plus queued corners; keep manual R and existing rooms.
Check concave returns in all rotations and both visibility settings. Check exposed,
connected and nonmatching-neighbor entries separately. Keep gallery notes exportable
and native evidence distinct from Studio/export acceptance. See the
[session closeout](CORRIDOR_ART_SESSION_CLOSEOUT_2026-09-08.md).

Historical feature record: later owner decisions supersede saved arrangements,
coordinate-driven editing and independent low-wall light placement below. See
ROOM_STUDIO_SIMPLIFICATION_2026-09-08.md, ROOM_STUDIO_USABILITY_2026-09-08.md and
RISER_LIGHTING_2026-09-08.md for this session's accepted changes. Use live code and
CURRENT_STATUS.md for subsequent sessions' changes.

All existing controls remain available. New authoring tools:

- Alignment guides snap edges and centers to the room perimeter, center, and other visible objects. Grid snapping remains independent. Hold Alt during a drag to bypass both.
- Hover outlines, Ctrl-click to cycle overlapping artwork, and Shift-drag empty space to box-select. Empty left-drag and middle-drag pan. Shift-click adds/removes selections.
- Group/Ungroup persists memberships per room orientation; selecting a member selects its group. Dragging, X/Y and arrow nudges move the selection. Locked and fixed objects do not move.
- Copy/Paste (Ctrl+C / Ctrl+V) transfers movable props and arrangements between rooms. Native artwork retains its source renderer via a catalog-validated descriptor, preserving registered cutouts. Fixed baked wall slices cannot be transferred. Floor panels and surface decorations retain their layer semantics; clicking floor decorations on the canvas selects their layer automatically.
- Bring forward / Send backward changes order within the Props, Floor decorations or Riser decorations layer. Structural layer boundaries are retained.
- Lights expose brightness, color and beam spread. The shared renderer consumes the same settings in the studio and game. Raised and low-wall lights keep their independent placement/settings.
- Named saved arrangements can be inserted repeatedly, including after reopening the editor. Names are unique; existing presets are not silently replaced.
- Room switching saves valid edits; invalid unfinished edits remain available for correction. Picker markers and an unsaved-orientation count show outstanding work. A separate recovery file is written every two seconds while idle and immediately for new workflow commands; reopening offers Restore edits or Discard recovery. Recovery does not publish edits into saved room layouts.

Ctrl+G groups; Ctrl+Shift+G ungroups. Text-entry fields retain their normal shortcuts. Existing Save, Save all rotations, Undo/Redo, Delete-to-tray, placement validation and Original preview behavior remain in place.

Presets and recovery sit beside the configured layout file as `.presets.json` and `.recovery.json`, written via temporary-file replacement. Layout metadata uses `group/`, `order/`, `lighting/` and `portable/` keys, with the existing version-one layout format. Source artwork and save data are not flattened into image snapshots.

## Verification

- `tests/test_layout_workflow.gd`: cross-room native copy, duplication, saved arrangement insertion, group movement/undo, ordering, guide snapping/Alt bypass, hover/overlap cycling, box selection, light settings, disk reload, multi-room recovery, fresh-editor recovery prompt, and main-scene rendering.
- `tests/test_room_layout_editor.gd`: existing editor regression suite, including all 43 catalog rooms, tray/placement, rotation, flips, group movement, Save All, light placement and pause restoration. Legacy drag checks disable the new optional alignment snapping; captures explicitly request a rendered frame.
- Native evidence: `output/layout-editor/workflow-test.log`, `workflow-regression.log`, `workflow-studio.png`, and `workflow-runtime.png`. Studio and game captures visually inspected.

Checks use isolated test layout, preset and recovery files. No owner layouts or packaged executable were changed.

## Packaged playtest follow-up

The later Windows debug build at `output/layout-studio-playtest-20260908/build-v2/BrineSpace.exe` packages these features. Keep its PCK beside it and open Room Layout Studio from the normal title screen. Exported workflow and normal startup checks passed with no engine errors, isolated test saves, and unchanged final package hashes. The exported studio screenshot was visually inspected. Evidence and hashes are in the parent directory (`checks.json`, `package.json`, `workflow-v2.log`, `startup-v2.log`). The initial build failed only its generated test-adapter indentation and is retained as failed evidence; build-v2 is the tested build. This supersedes the earlier no-package statement for this feature set.


## Latest local controls and performance (session closeout)
Free placement defaults on, with explicit saved preferences preserved. Entryway
areas and Clean preview are in the main toolbar. See LAYOUT_CONTROLS_2026-09-08.md.
Transparent tray previews, stable loading slots, outline selection and translation-only
drag updates are recorded in LAYOUT_EDITOR_POLISH_2026-09-08.md. Native workflow and
performance guards pass. Earlier packaged builds above predate these changes.
Use those dated scope statements rather than treating this whole document as a
single exported revision. See WATER_EDITOR_SESSION_CLOSEOUT_2026-09-08.md for resume notes.
