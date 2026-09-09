# Room declutter handoff

Updated: 2026-09-09 · Project: BrineSpace

## Objective and acceptance

Owner requested removal of electrical wire/conduit floor decorations and all common props/art from rooms, retaining them in the layout editor.

## Accepted decisions and constraints

Runtime excludes library common props (including copies and variants), dressing-profile furniture and supported accessories, raised-wall accessory overlays, floor-profile details and automatic floor patches/service runs/bridge covers. Specialist room equipment and artwork embedded in its source remain intact. Assets, common catalog, editor prop definitions and personal layout files are retained. Studio remains able to display/edit common content, but live rooms suppress it under this current preference.

## Current state

Runtime filtering occurs in `scripts/room_layout_store.gd` after library/copy/variant placement, removing common props from the same list used for rendering and obstacles. The existing editor preview bypass retains the full authoring list. `rooms/whole-room/room_dressing.gd`, `north_wall.gd`, `decoration_props.gd`, `room_services.gd` and `rooms/floor-profiles-v1/details.gd` suppress the associated automatic artwork. Decorative floor kits remain available as source/catalog assets; automatic floor patches and service runs are disabled globally.

44 furnished room cards were rebaked to `assets/room-declutter-v1/cards/`; `scripts/room_card_art.gd` and `scripts/grid_canvas.gd` now use them. Three corridor cards retain their existing images. Original cards are preserved and previous bindings recorded in the new pack.

## Verification

- Native Godot capture and assertions: 47 rooms × four rotations = 188 views; zero runtime common props and zero specialist equipment rectangle differences against the editor. The saved owner layout copy retains 81 common prop instances across rotations in the editor. Isolated user data; no personal layout writes.
- Native capture completed with exit zero and no errors (`output/room-material-consistency/render-1788992508571014000.log`). Existing raw-image export warnings were present; no export acceptance is claimed.
- Visual review of all 47 default room orientations plus representative alternate orientations confirms open floors and retained main equipment. [Gallery and full geometry report](room-declutter-2026-09-09/review.html).
- Native card bake: 44 rooms, exit zero, no errors. Card consistency regression passes all 47 catalog identities and primary/grid/variant bindings.
- Full capture evidence: `output/room-declutter/`; durable report and contact sheets: `docs/room-declutter-2026-09-09/`.

## Next action

Owner review of the cleaner layouts. No executable rebuild, export, commit or push performed. Later concurrent source changes are outside this captured revision.
