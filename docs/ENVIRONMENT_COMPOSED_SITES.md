# Composed underwater locations

Three authored locations reuse the existing library through
`assets/environment/composed_sites.gd`. No new PNGs or runtime textures were added.

| Location | Center | Composition |
|---|---|---|
| Wreck field | 20.5, 18.5 | A broken service trail connects the existing engineering and medical wreck area: support, harness, cover, duct, tank and reel. Existing room and rock occupancy remain authoritative. |
| Current-swept shelf | 6.5, 12 | Ripple sand extends along an elongated 4 by 1.8-cell radius. Unequal rock pairs and sparse attached life frame an open central bed. |
| Overgrown station edge | 22.5, 22.5 | Growth collects against a fallen support and the hydroponics wreck edge; algae, mussels, broad lettuce and anemones form a small attached group. |

Random base scenery is excluded from these authored footprints. Other existing
habitat placements remain. All composition props use the existing texture caches
and draw below rooms and physical wrecks. Existing destruction, salvage and paid
rebuilding logic is unchanged; decorative props do not grant salvage rewards.

## Evidence

`output/composed-sites-v2.log` passes all source references, three locations at
1280, 1600 and 2560 widths, unchanged occupancy/resources/wreck state, and retained
engineering, medical and hydroponics wreck identities. Native captures were reviewed.
The earlier v1 captures remain available. Moving the pointer out of the grid in
v2 did not remove the existing room art; it must not be described as a proven hover
artifact. `tests/test_drone_fleet.gd` exits successfully.

`output/environment-export-v23/` passes the isolated Windows debug export with
93 exact PNGs, 22 renderer caches, 66 textures and eleven habitats, plus three
new named site captures. This is a first composition pass, not human gameplay
acceptance or a new clearance-mechanics validation.

[Scene comparison](../assets/environment/composed-sites.html)
