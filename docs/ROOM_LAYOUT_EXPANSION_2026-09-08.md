# Layout Studio expansion

Implemented the owner's seven requested editing improvements:

- Independent duplicate IDs for repeated library assets, authored props and surface decorations; saved source references reconstruct native duplicates.
- Shift-click canvas multi-selection, grouped drag, flip and return-to-tray; X/Y moves the selected group by a common delta.
- All 43 RoomDatabase identities in editor-catalog.json, preserving existing asset/save keys for the original 15. Corridor previews reuse their native polygons, with saved prop additions drawn in gameplay. Corridor structural floor/wall artwork remains fixed and unsupported editing layers are disabled.
- Save all rotations validates the room's edited orientations then writes them together through one temporary-file replacement. Failed validation does not partially save orientations.
- Exact X/Y numeric controls.
- Persistent lock and visibility flags, with hidden objects still accessible in the object list.
- Original preview uses the authored defaults without discarding the current draft. Editing is guarded while comparison is active.

The sidebar scrolls to keep controls reachable. Fixed baked wall slices remain non-movable and are excluded from duplication; their source image cannot safely be treated as an independent object. Owner layout files were not modified during tests.

Verification: output/layout-editor/expansion-verified.log covers the previous regression suite plus all 43 room loads, duplicate instances, grouped coordinates/flip and native drag, lock/hide, before/after, Save All and duplicated riser persistence. output/layout-editor/catalog-runtime.log verifies saved additions in a corridor and Current Turbine using the main scene. expanded-studio.png was visually inspected at 1280×900. Syntax/diff checks passed. No executable rebuilt, committed or published.
