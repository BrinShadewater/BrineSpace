# Top-down, inward-facing room direction

Owner decision after playing the game and Layout Studio, September 12, 2026.
This supersedes earlier front-elevation, tall north-wall and fixed-facing room-art guidance.

## Authoritative direction

All room equipment should use a coherent top-down view and face the room interior on every wall: north equipment operates from the south, east from the west, south from the north, and west from the east. This applies to north walls as well as side/south walls. A small amount of north perspective is acceptable only when the equipment remains low, readable and consistent through rotation. Do not preserve a tall elevation merely because it once passed a layout test.

Use low worktops, tray tops, lids and equipment footprints as the primary shapes. Keep functional access visible: handles, keyboard spacebars, case catches, cartridge releases, tool finger loops and handset access inward; hinges, hose connections and backing toward the wall. A vertical strip is not evidence of an overhead camera. Do not rotate an upright illustration into compliance.

Maintain room-specific materials and scale. Reduce bright orange to match the room's machinery; matte finish is independent of cleanliness. Avoid white rims, metallic sparkle, baked glow and white cutout artifacts. Cold Store moves toward blue; medical treatment beds should use matching blue rather than orange. Biomass equipment needs matching green. Wall finishes should harmonize with each room rather than impose a universal palette.

Observation is a strong style reference. Its porthole artwork should become part of the background wall/riser rather than movable equipment. This revises the older movable north-window/riser replacement solution. Architecture may retain its wall presentation; the new equipment camera is top-down.

## Owner-selected visual references

- Mycelium: the south side cultivation wall is the preferred style.
- Crew Lounge: the south built-in is stronger; extend that overhead treatment to north.
- Bio Lab: Side Bio Culture Wall South is the strongest wall piece.
- Clone Lab: Side Clone Growth Wall is strong; extend the top-down inward approach.
- Research Lab: Side Research Analysis Wall South is strongest.
- Listening Post: use the Side Deepwater Listening Walls style consistently; competing packs currently clash.
- Isolation Vault: use Side Emergency Isolation Wall South as the direction for every wall.
- Hydroponics, Observation, Ore Refinery and Quarantine are strong overall, with the specific corrections in the playtest queue still required.

These are owner preferences, not evidence that every variant already meets them. Recent native passes establish their tested source revision, not acceptance under this new global direction.

## Production and review workflow

1. Read the raw owner notes and handoff queue. Resolve the actual selected asset and room ID in current code; Studio and gameplay may expose different assets. Record provenance and current consumer paths.
2. Write a brief with room identity, department, condition, intended world size, exact functional inventory, inward edge, wall contact and doorway exclusions. Reference south/top-down exemplars by role. Avoid using an old elevation as the sole camera reference.
3. Generate/edit one coherent asset. Preserve originals and exact prompts. Review each component's direction and material, not just the overall cabinet. Count objects across the entire bank; prompts can accidentally repeat counts in every bay.
4. Register unchanged raster with actual alpha or neutral-exterior vector geometry. Verify alpha extrema, not just RGBA presence. Exclude confirmed exterior apertures; keep dark recesses and visible surfaces below handles. Fix white cutouts in the source/registration deliberately.
5. Fit art to the actual wall and crew scale. Outer-edge-aligned contain frames can preserve existing collision dimensions during a source change, but unchanged bounds alone are not a size acceptance criterion. Revisit an oversized footprint when the owner identifies scale problems. Preserve route access and check retained small equipment.
6. Use authored inward companions; mirror new sides only when the design allows it. Preserve separately authored accepted arrangements unless deliberately converting them. Ensure every consumer decodes the mirror flag and uses reflected source UVs; a JSON flag alone is insufficient.
7. Keep idle sources quiet. Operating screens use source-local anchors and room power state, including retained rendering. Preserve department colors. Reading lamps should stay steady; do not introduce flicker merely to satisfy a temporal-change check.
8. Review furnished native views in all relevant orientations, in gameplay and Studio. Add a standing/walking character scale option as requested; until implemented, use an appropriate native crew fixture and record that limitation. Test actual routes, not only silhouettes.
9. Check isolated effects in direct and retained renderers. Power/time comparisons are not pause proof. For pause/cache claims, use actual station power, pause and visibility transitions. A fixed-orientation room repeated four times is not four-direction coverage.
10. Refresh affected cards, inspect the native card, then update all current bindings. Default-quarter side changes can require a card refresh. Run relevant tests once; record exact scope/revision and unresolved findings. Keep export claims separate from editor/source checks.

## Scope of this handoff

No playtest issues below were implemented during consolidation. Source art improvements from this session are retained as useful work, but every room must be reassessed against this decision. See [handoff and complete work queue](ROOM_ART_HANDOFF_2026-09-12.md) and [verbatim owner notes](handoffs/2026-09-12-top-down/OWNER_PLAYTEST_NOTES.txt).
