# Department riser wall pass

Updated: September 8, 2026 · BrineSpace · Riser art and default visibility

## Objective and acceptance

Add more riser wall designs that suit different rooms, and enable risers by default. Native visual review is complete; owner acceptance is pending in the [47-room gallery](../output/riser-departments-v1/index.html).

## Accepted decisions and constraints

The owner's latest default-on direction supersedes the retired forced-low preference. Keep editable wall mount identities, saved owner layouts, raised-wall geometry, connection culling and door apertures. New finishes remain matte and restrained. Eight new families complement the dedicated BRINE and airlock walls:

| Family | Design |
| --- | --- |
| Biology | Cream/sage panels, irrigation services and moisture instrumentation |
| Clinical | Pale medical panels, aqua service channels and gas controls |
| Habitat | Warm cream, wood and fabric recesses, soft inset lamps |
| Engineering | Graphite construction, orange accents and heavy service ducts |
| Research | Icy grey panels, teal instruments and sealed sample equipment |
| Communications | Slate blue, burgundy data channels and recessed electronics |
| Logistics | Olive/ochre hatches and recessed storage rails |
| Containment | Sage/burgundy panels, reinforced gaskets and observation details |

## Current state

`assets/riser-departments-v1` preserves eight original generated sources, exact prompts, source hashes, UV registrations and 53 native cards. `rooms/whole-room/riser_catalog.gd` maps all 47 room types. `north_wall.gd` draws registered department faces/caps beneath existing editable mounts; `corridor_dressing.gd` uses the logistics face while retaining chamfers, narrow returns and neighbor culling. BRINE and airlock retain their bespoke artwork. Both card consumers now use the refreshed 47 primary cards and six corridor variants.

The source illustrations include quiet lower cabinet areas. Runtime samples the upper service band at the room face's 6.4:1 aspect; short corridor spans use proportional center crops. Original raster pixels are unmodified. Native captures establish composition; source sheets alone do not establish game appearance.

`title_settings.gd` initializes raised walls on and persists `display/riser_walls_enabled`. The old `raised_walls` value was previously forced off; migration intentionally ignores that retired value. An explicit subsequent off choice persists through the new key. `settings_panel.gd` exposes the toggle and defaults reset. `room_layout_editor.gd` opens with risers visible and previews the appropriate door finish. No tool wrote the owner's layout file; fixtures use isolated stores. Other active project work is retained.

## Verification

- Settings: fresh default, legacy migration, explicit off persistence and reset all pass.
- Department fixture: 47 explicit unique assignments, eight bounded aspect-correct faces, 32 native rotation previews and nine corridor captures pass.
- Studio: initial riser visibility, rotation/autosave, R/F, asset variants, Listening Post movement and door leaf animation pass.
- Native station: default visibility without a fixture override, stepped adjacency, cache invalidation and visual toggle pass. Station capture visually inspected.
- Card consistency: all 47 identities agree across primary/grid/variant mappings and PNG decoding.
- Eight source SHA-256 values verified; new PNGs match the Git LFS filter. Gallery serves HTTP 200. Existing raw-image export warnings remain; this pass does not claim exported-build validation.

Logs and native evidence: `output/riser-departments-v1`. Rebuild registration with `tools/register_riser_departments.py`; bake furnished cards with `tools/bake_current_architecture_cards.gd -- --compact --output=res://assets/riser-departments-v1/cards`, corridor/rotation captures with `tests/test_riser_departments.gd`, and gallery/card mappings with `tools/finalize_riser_departments.py`.

## Next action

Owner reviews the gallery and exports notes. Apply specific material or layout corrections from that review; do not treat the source or native checks as owner approval.
