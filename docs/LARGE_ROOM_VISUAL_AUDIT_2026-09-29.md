# Four large rooms: visual bible audit

Updated: 2026-09-29 · Project: BrineSpace · Task: large room art review

## Objective and acceptance

Check the four installed large rooms, their eight new painted source PNGs, structural walls and doors, floor treatments, and baked cards for pixel density, art style, scale, perspective, and color against `BRINESPACE_VISUAL_AESTHETIC_BIBLE.md`. This is an agent visual review, not owner acceptance or a release playtest.

## Accepted decisions and constraints

Hydroponics Farm is green, Storage Depot and Tidal Power Plant are yellow, and Moonbay is cyan. These are muted department identities over practical station materials. The four rooms have fixed large installations, north-only risers, top-down east/west/south walls, current painted station door skins, and a dry Moonbay at rest. Preserve the 92-unit station ports and Moonbay's 192-unit inner gates. The existing accepted `station-props-v2` pieces are reused furnishings, not new source art.

## Current state

Reviewed commit `4797302f` on `codex/large-rooms`. The four 512-pixel selected cards, the 16 Walls-on and 16 Walls-off rotation contact sheets, four native station captures, and Moonbay idle/flooding/launching captures are under `assets/large-room-cards/`, `output/large-room-review/`, and `output/moonbay-review/`. Compared them with the bible's accepted September 26 prop board and the actual new PNGs in `rooms/large-rooms/art/`.

| Check | Result | Evidence and limit |
|---|---|---|
| Pixel density | Pass at current display sizes | The grow beds display at about 347×408 world units from 1157×1359 pixels (3.33 source px/unit); gantry and turbine at 408×408 from 1254×1254 (3.07); mini-sub at about 336×160 from 1816×866 (5.41). Wall-bank cache resizing gives exactly 5.0 px/unit in their displayed 62-unit riser band. The existing floor textures downscale from 1254 to 185 units per repeat; they are quiet at their 0.36–0.43 opacity. The sub has finer source density, but no visible mismatch or jagged edges at card/gameplay size. These numbers describe sampling, not a pixel-art grid requirement: the bible calls for detailed hand-painted sprites. |
| Focal art and scale | Pass with a texture caveat | The four centerpieces have overhead views, shallow hardware depth, clear functional silhouettes, matte metal, and believable fixed scale relative to the room and crew. Storage's gantry and Tidal's turbine contain much more fine wear than the nearby support props; at card scale this reads as dense texture, but does not hide the function. Do not add more surface noise. |
| Shared construction | Partial | The north cap, short returns, top-down perimeter, and painted station doors now belong to the same hull family in all rotations. Tidal's ocean-facing intake/opening remains a flat dark-cyan rectangle with five dots; it is a visual outlier beside painted risers, door skins, and turbine. It is drawn by `_draw_ocean_face` when `bay_gate` is false. Moonbay's chamber side rails, tie bars, and some inner-gate trim are broad flat aqua/gray code shapes alongside a painted sub and door leaves. The intended enclosure is readable, but the material treatment is less finished than the rest. |
| Perspective and rotation | Pass, with the same construction caveat | The riser is on screen north only; other perimeter walls are top-down. The fixed banks move to clear north segments. Centerpieces, support props, and bay enclosure rotate together. No source asset becomes a tall frontal elevation or an isometric object. The flat ocean opening and Moonbay rail shapes weaken depth rather than changing the camera angle. |
| Color and hierarchy | Partial | Storage's extra desaturation achieves dull ochre rather than a bright yellow wash. Moonbay's cyan is localized mostly to machinery, lines and lamps; Tidal's turbine remains charcoal and steel with ochre details. Hydroponics's full 740-unit deck has a green base (`#263b36`) under its low-opacity floor, so the entire room reads as a green field beside neutral single rooms. The bible calls for muted *local* department color rather than full-image wash. Tidal's `#113b4b` ocean face is also a comparatively strong blue patch, especially on the north rotation. No change to interface/category colors is implied. |
| States and openings | Pass in inspected frames | Moonbay is dry while idle, fills only its chamber during flooding, and reveals the sub leaving through the ocean side at launch. The outer Moonbay hatch uses the current painted ocean asset. Closed and fully open station-door rotation captures show the large-room seam only once. Mission collision, a full long-run playtest, and owner visual acceptance are outside this art review. |

### Focused art corrections

1. **Tidal Power Plant ocean face — high priority:** replace the five-dot blue block with a painted intake/grille or pressure-hull fitting that matches the existing door/hull finish. It is an ocean-facing facility, not a crew-sized station door; retain its 192-unit opening and all rotations. Review both Walls-on and Walls-off, especially north and side orientations.
2. **Moonbay chamber construction — medium priority:** give the flat side rails, tie bars and gate trim the same matte painted depth and controlled edge treatment as the accepted hull and door assets. Keep the separate inner station and ocean gates and the dry/flooding state behavior.
3. **Hydroponics deck — medium priority:** bring the base toward neutral gray-green, leaving the plant beds and wall manifold as the clear green identity. Compare the native station view beside ordinary rooms and the 512-pixel card before selecting a shade.
4. **Source edge quality — low priority:** at source zoom the generated PNGs have partially transparent antialiasing and a few colored edge specks, most noticeable near the gantry/wall-bank yellow edges. No fringe was clearly visible in the reviewed native cards. If these assets are reused at a larger size, inspect against light and dark backdrops and clean only demonstrably visible fringe; preserve the original sources and hashes.

## Verification

Read the current bible, accepted prop board, source PNGs and renderer code; inspected the existing native image evidence at original or high detail and measured source/display dimensions with Pillow. No asset or gameplay code changed in this audit, so no test rerun was needed. Earlier focused tests apply to commit `4797302f` as recorded in `LARGE_ROOMS_HANDOFF_2026-09-28.md`; they do not grant visual acceptance.

## Next action

Repair the Tidal ocean face first, then make the focused Moonbay and Hydroponics material changes above. Re-render the four relevant rotations and native station comparisons after each changed surface, then rebake selected cards and run the focused art test. Owner review remains the final visual acceptance gate.
