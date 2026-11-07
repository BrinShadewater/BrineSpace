# Quarantine Cell registered pass

The isolated empty berth, dedicated filtration, observation console and protective
gear cabinet now use registered source polygons in station, placement preview,
draft and inspector. The native 512 card uses the same embedded renderer.
The shared hull owns east/west sockets; its straight-mask rotation is offset
from the equipment rotation so south-facing props stay consistent with the batch.
Unused doors remain sealed. The source image is unchanged.

Filtration gauge and observation display have local operating cues. Berth and
gear remain still; no patient, occupancy or treatment simulation is claimed.
Costs, category, progression and saves remain unchanged.

## Evidence

`tests/playtest_quarantine_cell.gd` passes at 1280x720, 1600x900 and 2560x1440:
four rotations, full visual containment, non-overlap, per-host active/inactive/
pause pixels, east/west topology, disconnected seals and 728 center-to-port
samples. Sampled effects remain outside both reserved aisles. The native card
and rotated 2560 station/draft/inspector frame were inspected. Evidence is in
`output/production-ten/quarantine-native-*` and matching logs.

Synergy, discovery progression, polish gameplay and run balance pass. Quarantine
stderr has no ERROR/SCRIPT ERROR entries. Card has LFS attributes and new scripts
have paired UIDs. Inherited raw-image export warnings remain.

## Remaining acceptance

Neighbor and production-actor crossings, incompatible pixel seams, economy-driven
power transitions, mature mixed-station zoom, checkout-independent packaging and
owner visual review remain. Source-floor patches inside pipe loops require close
review. This completes initial registration of all ten requested rooms, not
full batch acceptance.
