# Environment replacement handoff — September 29

## Objective
Replace all six remaining audited procedural environment groups with original
graphics matching the matte painted visual bible and native drawing density.

## Accepted decisions
Original art owns physical detail. Existing consumers own geometry, placement,
connectivity, tint, fog lighting, animation time, quality and reduced-motion gates.
Retain procedural fallbacks, source masters, immutable raster hashes and raw PNG loading.

## Current state
`assets/environment/procedural-replacements-v1/` contains ten painted masters,
ten calibrated derivatives, two exported neutral optical masks, prompts, bake,
ledger, README and isolated verifier. `scripts/environment_art.gd` and paired UID
provide explicit paths and cached loading. Consumers changed: `seabed_glow.gd`,
`station_hardware.gd`, `station_effects.gd`, `grid_canvas.gd`, `rock_view.gd`,
`wreck_view.gd`. Permanent runtime loader now includes all twelve bindings.
Native fixture and paired UID are `tests/preview_environment_replacements.gd`.
Other concurrent character/card changes in the workspace are outside this task.

## Verification
Source audit: 12 identities, 22 raster versions, zero unregistered candidates.
Runtime loader: 78 checks. Native fixture covers all 16 rock connectivity masks,
unchanged terrain data after drawing, repeat-frame equality, changing visual time,
hazard quality/reduced-motion branches, housing directions and a fogged station.
Captures: `output/procedural-replacements-v1/native-sheet-v1.png` and
`native-station-v1.png`. Profiles isolated through scratch APPDATA/LOCALAPPDATA;
passing native gates fingerprinted 2,769 real profile files unchanged.
Art fixture free-builds three solar arrays for illumination; no paid-run claim.

## Next action
Owner review in ordinary gameplay. Packaged gameplay is untested for this batch;
no release, commit or push performed. Future art additions should retain the
migrated historical source appendix when regenerating the inventory.
