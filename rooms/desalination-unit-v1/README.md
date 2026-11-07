# Desalination Unit

Owner-approved early water source, October 19, 2026: common Life Support,
**5 Metal**, **2 Power → 2 Water/cycle**, one cell. North intake and
**west/east/south doors** rotate together. Pumps, clear ocean intake and station Power are required.
Normal paid construction, suspension, storage and failure rules apply.

## Current room design

The owner's follow-up requested recolouring the yellow prop and giving the room
more character. All five machines now share a muted matte blue-green painted finish, with neutral
steel vessel bodies, charcoal parts and functional display colours retained. Spare filter cartridges, a
recessed drain, flush service channel, corner paint and a small FILTERS stencil
make the room read as a maintained water plant. Machinery remains upright; the
four authored rotations reposition the service bank to keep all three door routes clear.
Floor details follow the effective machinery positions, including Studio moves.
These are static surfaces, not new gameplay hazards or machine animations.

`view.gd` remains a leaf of the shared expansion renderer, using a custom
window-free water-plant riser over the clinical family, muted Life Support floor
and ordinary lighting. Gameplay did not change in these art passes. The original
yellow and green source artwork remains available to other rooms.

The riser has protected intake/outlet manifolds, analogue pressure gauges, filter
housings and a small droplet emblem. Neutral cladding keeps the blue-green fittings
readable. The quiet 92-unit central reserve accommodates the separate 72-unit
doorway. Existing 384×60 face geometry, cap and shared-neighbour visibility remain
unchanged; these are static fittings with no new simulated status or animation.
Studio's **Room default** selects this wall automatically.

A muted grey-green **INTAKE** floor decal points toward the sealed, non-door wall.
It rotates with the same quarter-turn as the intake and doors; the label stays upright.
It identifies which outside cell must remain open ocean, not a simulated water-flow
direction or operating-status light. The stencil adds no collision or gameplay rule.
The 22-size lettering is compressed to 80% height on the floor plane, replacing the
earlier tiny 10-size label. Thin applied ink, narrow stencil bridges and restrained
edge nicks reveal the actual deck beneath; there is no offset shadow. Canonical
vector cutouts are cached once. Font and floor rendering remain shared and unchanged.

Continuous bevelled hull caps, mitred corners and port frames use the production
painted-shell cap drawing with the custom atlas. The raised crown includes a full
header above rotated north doorways. This is a room-only cap layer; the custom wall
face, shared renderer code and three-door collision geometry remain intact.

## Artwork and provenance

| Role | Library ID | Raster |
| --- | --- | --- |
| Filter vessels | `library/sp-desalination-vessels-1` | `assets/desalination-unit-v1/filter-vessels-teal-v1.png` |
| Intake pump | `library/sp-desalination-pump-1` | `assets/desalination-unit-v1/intake-pump-teal-v1.png` |
| Quality console | `library/sp-desalination-console-1` | `assets/desalination-unit-v1/quality-console-teal-v1.png` |
| Teal membrane skid | `library/sp-desalination-membrane-1` | `assets/desalination-unit-v1/membrane-skid-teal-v1.png` |
| Service cartridges | `library/sp-desalination-cartridges-1` | `assets/desalination-unit-v1/service-cartridges-teal-v1.png` |

The built-in image generator produced separate painted siblings. Original source
rasters remain intact for Water Reclamation and Tidal Condenser. The first membrane
edit is recorded in `assets/desalination-unit-v1/provenance.json`; the subsequent
four matching edits, exact prompts, raw images, normalization and hashes are in
`assets/desalination-unit-v1/matching-props.provenance.json`. These are generated
repaints, not pixel-identical hue substitutions.

Godot exports each sibling into the original source canvas: vessels 317×325,
pump 276×288, console 331×232 and cartridges 294×281. The subsequent equipment-scale
review matches the console to Water Reclamation's effective authored size:
**81.73 world units wide**, down from 112.54. The membrane skid is **130.5** wide,
down from 140.3, compensating for the repaint's tighter visible bounds. Vessels
107.78, pump 93.84 and the smaller 76-unit service cartridge bank are retained.
Bottom-center ground anchors stay fixed in all four authored rotations; normalized
collision metadata and raster art remain unchanged. Raw images and game PNGs use Git LFS. The card is
baked from the current room renderer. No custom animation was added.

The riser atlas is `assets/desalination-unit-v1/riser-water-plant-v1.png`:
1024×178, with an independently sampled 1024×18 cap and 1024×160 face. Its raw
master, exact prompt, crop/resize recipe, alpha probes and hashes are recorded in
`assets/desalination-unit-v1/riser.provenance.json`. Raw and game PNGs use Git LFS;
the original clinical artwork remains intact.

## Validation and continuation

Further testing covers three additional fresh seeds through cycle70, one natural
Galley ignition, and five controlled severe-fire cases from an actual early paid
checkpoint. Desalination sustains routine tested use and replenishes suppression,
but simultaneous severe fires can exhaust early reserves. A burning plant correctly
stops cycle production. Current tuning is retained; these are limited balance
samples, separate from visual/package acceptance. [Fire-Water results](../../docs/DESALINATION_FIRE_WATER_BALANCE_2026-10-19.md).

The owner accepted the current equipment scale. A subsequent matched fresh-profile
seed4404 paid opening through cycle20 left **22 Water** with the unit active,
versus **zero** with the same paid unit suspended. It prevented six observed Galley
Water outages. Both survived without blackouts; no fire demand was exercised and
no balance values changed. [Fresh-run pacing and limitations](../../docs/DESALINATION_FRESH_RUN_BALANCE_2026-10-19.md).

The actual native station, Studio, card and four-orientation renderer were
reviewed. The latest scale revision passes **906 native checks**, including normal paid architect construction,
Water production, suspension/resume, staged Save/Continue, four crew-graph routes
and all Studio rotations, plus room-default riser resolution, source rectangles,
window-free registration and the central door reserve. Crew can enter through all
12 rotated entrances and travel between each pair of connected neighbours. A
connected north-neighbour capture verifies the shared wall is hidden correctly.
**51 gameplay checks pass**, including placement through each door, rejected
intake-side connection and retained economy. Scoped layout lint covers all four
orientations with zero findings. Only this room's four authored layout records
changed for the new circulation; owner layout data was not edited.
Eight additional rendered cap probes cover the side band and central doorway
lintel at crown height in all rotations. They reject the former missing-cap state.
Four additional rendered arrow probes use the game's actual ocean-exterior cells
to check that the arrow points toward the intake in every rotation; the no-arrow
negative control fails all four.

The equipment-scale review compares five effective prop pairs and three furnished
rooms at the same zoom beside the production 65.28-unit crew ruler. Console and
skid visible widths now match their existing counterparts; vessels and pump were
already consistent. The compact cartridge bank remains a service accessory rather
than another full purification machine. [Scale comparison and evidence](../../docs/DESALINATION_EQUIPMENT_SCALE_2026-10-19.md).

[Gameplay addition](../../docs/DESALINATION_UNIT_2026-10-19.md) retains the initial
implementation evidence. [First art revision](../../docs/DESALINATION_ART_POLISH_2026-10-19.md) and
[matching-prop revision](../../docs/DESALINATION_MATCHING_PROPS_2026-10-19.md)
retain their scoped evidence. [Custom riser](../../docs/DESALINATION_RISER_2026-10-19.md)
retains the custom-wall evidence. [Three-door revision](../../docs/DESALINATION_THREE_DOORS_2026-10-19.md)
records the current images and checks. This is local source work; owner visual and
pacing acceptance and new-release package validation remain separate.

[Top-cap correction](../../docs/DESALINATION_CAPS_FIX_2026-10-19.md) records the
latest card, native views and resumed isolated playtest.
[Intake arrow](../../docs/DESALINATION_INTAKE_ARROW_2026-10-19.md) records the current
direction marker's initial integration. [Floor-decal refinement](../../docs/DESALINATION_INTAKE_DECAL_2026-10-19.md)
records the current larger lettering, finish and updated rotations.
