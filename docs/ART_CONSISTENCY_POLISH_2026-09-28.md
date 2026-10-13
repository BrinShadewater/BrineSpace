# Project handoff: art consistency polish

Updated September 28, 2026. Scope: current assets created in this conversation.

## Objective and acceptance
Review style, consistency, apparent pixel density, color and scale; polish concrete
outliers. 63 selected sources: the earlier 44 architectural/machinery images plus
19 hallway props. Superseded sources and unrelated concurrent crew work excluded.
Owner visual acceptance remains pending at /consistency-polish/.

## Accepted decisions and constraints
Preserve matte painted industrial materials, muted but distinct colors, the
requested tall plant silhouettes and alternate crate perspectives. Preserve the
locked launcher. Source oversampling is not itself a density defect: compare
visible detail at equal world scale. No global blur, palette flattening or resizing.

## Current state
Two new, non-destructive sources in assets/hallway-props-v1: asparagus-fern-pot-polished.png
and rubber-plant-pot-polished.png. Fern leaflets are broader and less busy; rubber
leaves, soil and pot have simpler painted surfaces instead of photographic grain.
Existing IDs and world widths preserved. Originals and exact prompts retained.
Six plant registrations now use pot contact instead of a foliage-sized blocker:
sage leaf, fern trough, succulent, rubber plant, asparagus fern and dwarf palm.
rooms/station-props-v2/props.json and pack manifest updated; owner layouts unchanged.
Normal gallery refreshed and /consistency-polish/ adds native comparisons.

## Review findings
- Crates, barrels and machinery share quiet paint, dark protective edges and readable
  top surfaces. Their distinct colors and front-face depth variants are intentional.
- Tall snake/cane plants have more visible vertical growth as requested. They are
  visually different from low overhead plants; preserved rather than flattened.
- Fern was a bright, fine-detail outlier. Revised broad leaf clusters reduce visual
  noise; hue remains olive, rather than forcing every plant to the same green.
- Rubber plant was more photographic than its peers. Revised material treatment
  better matches the painted set, with original plain-leaf identity preserved.
- Nineteen props use approximately 16-35 source pixels per world unit; the high
  resolution masters remain unmodified. Native display size governs visible density.
- Earlier wall/floor repairs remain intact. Shared panel and glass sampling, muted
  floor revisions and matte outlet are retained. Department colors remain distinct.
- Alpha surrounds the props; no conspicuous exterior halo in native review. This is
  visual evidence, not a claim of exhaustive alpha-fringe proof at every zoom.

## Verification
All 44 earlier source hashes match audit/repair records; four launcher lock hashes
match. All 19 source-region, polygon and normalized-footprint checks pass. Fresh
native Godot run passes 228 placements across straight/corner/tee and four rotations,
using production collision/segment checks with 10-unit crew clearance. Scratch
APPDATA used; complete real owner-profile fingerprints unchanged.
Reviewed all 19 source/native comparisons, 28 riser wall strips, 12 hallway finishes,
four floors and the outlet rotation board. Earlier architectural captures were reused
with matching source hashes; no fresh launcher motion, live crew overlap or release
validation is claimed. Fixture previews show individual placements, not arbitrary
combinations of all props in a furnished room.
Evidence: assets/hallway-props-v1/polish-review/audit-before.json, audit-after.json,
manifest-before.json, generation.json, footprint-fixes.json and native comparisons.

## Next action
Owner review of /consistency-polish/. No required implementation work remains in
this pass; no commit, export or changes to unrelated crew work.

## Owner follow-up: outlet alignment
Owner accepted the polish with outlet placement/opacity corrections. Updated
scripts/survey_probe_art.gd: north raised outlet centered at x=-4, solid steel
backing under the sleeve, other directional launcher art inset 24 units and clipped
to the inner wall boundary. Docked probe pose follows the inset and blends back
to its unchanged ocean route. Exterior side joints crop at the hull boundary.
Four fresh native views pass and were visually reviewed; real profile unchanged.
All four locked north launcher hashes still match. Updated outlet comparison in
both consistency galleries. No fresh full motion acceptance or release test.

Further owner correction: directional collars inset a total of 36 units (12 more),
with an inner solid sleeve to the wall and explicit exterior cap occlusion at
200 units east/west and 196 south. Four new native views pass and were reviewed;
owner profile unchanged. North alignment and locked mechanics retained.

## Side collar burial and south overhead correction
Owner clarified that east/west collars must be embedded within the wall, rather
than standing farther inside the room. Reduced their inward offset to 18 units,
so the outer collar is clipped beneath the cap. Replaced south launcher drawing
with a generated overhead sleeve/rail companion, preserving the old source.
Destination (-22,85,64,112), cropped at inner cap edge y=184; no front-facing
circular opening remains. North lock unchanged. Four fresh native views pass
and south/east/west were visually reviewed; owner profile unchanged. No fresh
animation acceptance claimed. Registration and prompt stored with outlet assets.

## South circular collar correction
Owner requested a circular top-down collar on the inner south wall. Replaced
the rectangular sleeve candidate with south-launcher-round-collar.png. Uniform
64/1028 scale preserves circular geometry; destination (-21.2,96,64,95.25292),
clipped at y=184 so the cap covers the outer rim. Source/prompt/hash retained.
South native view inspected; four orientation checks pass, owner profile unchanged.
East/west/north art and placement retained. Review ?v=south-round-collar.

## South edge-only correction
Owner clarified the south collar is vertical and only its top edge is visible
from overhead, not a flat circular hatch. South drawing now excludes the circular
opening, extends the rail bed to the wall and samples a shallow metal rim at
y=177..184 beneath the cap. Right fittings retained. Four native checks pass,
south view inspected, real profile unchanged. Supersedes circular view acceptance.

## Rounded inner collar refinement
South collar now samples the rounded crown of the exterior tube source, displayed
as a shallow 46-by-12 band at (-23,172), ending at the inner cap edge y=184.
This retains the tube material and rounded shoulders without showing its opening.
South native view inspected; four orientation checks pass, owner profile unchanged.
Review ?v=rounded-inner-collar. Other directions retained.

## Owner acceptance
September 28: owner accepted the rounded inner collar revision and current outlet
arrangement ("Okay great, that looks good."). Connection snapshot recorded in
assets/probe-outlet-stub-v3/accepted-connection.json. No further collar work pending.
