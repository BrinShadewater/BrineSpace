# Biodome polish review

Updated September 22, 2026. Broad goal remains active.

## Objective and constraints
Improve large/medium furnishing groups and bought/legacy art cohesion. Preserve
the ten owner reference rooms, library marks and original art. No Higgsfield.

## Current state and decision
Reviewed current cards for Biodome, Clone Lab, Construction Drone Bay, Gravity
Loom, Shield Generator, Salvage Drone Bay, Reactor and Life Support. These already
have reconciled furnishing; there is no basis to redo their entire layouts.
Biodome remains a useful composition/detail-density candidate: its rich fern bed
contrasts with small bought plants. Card montage is aspect-preserving and lives
at output/room-comparison-2026-09-22/candidates.png.

Staged q0 trial removes the second loose palm (cyb-210) and moves the round basin
beside the seating, from (114,-18) to (114,-72). Native review finds less accessory
scatter but a weaker, emptier right side. Do not install this removal-only trial.
Current saved/default layouts and cards remain unchanged.

## Evidence
Native funded fixture renders the staged room at two zoom levels and a room crop;
live.log exits 0 without reported errors. live/room-biodome.png was inspected
against the earlier same-framing installed Biodome crop. This is q0 composition
evidence only, not four-view navigation, owner acceptance or expedition gameplay.
The fixture uses isolated layout/profile paths and does not write owner layouts.

Reviewed four bought botanical sources at original pixel size, without enlarging
them: mb2-104 seedling shelf, mb-87 shrub trough, mb-47 flower trough, mb-48b
seedling trough. botanical-shortlist.json preserves source regions/registry data;
botanical-shortlist.png is a raw-region review board, not a processed runtime prop.

## Next action
Gather owner composition feedback and carry the accepted source revision into
the next test packages. Do not replace a density mismatch with indiscriminate
upscaling or add small props to fill empty floor.

## Medium-planter follow-up: installed
The next candidate retains the basin grouping and adds the bought mb-87 shrub
trough at (24,82), scale 0.95, in place of the removed loose second palm. The
source is unchanged and not enlarged. Live q0 review finds the medium display
balances the fern bed better than the rejected removal-only trial.

Four native views pass strict visual-overlap checks and 640 walking samples.
All four were visually inspected, including quarter-specific retained growing
and potting arrangements. Saved Biodome layouts matched defaults before promotion;
guarded installation changes exactly four Biodome keys in each file. Every other
layout key and all 12 tileset-library JSON files remain unchanged. Original files
and card are backed up in the evidence directory. Installation script/report:
install.py and installation.json.

Independent installed-default review again passes four views/640 samples. All four
installed RGBA framebuffers are byte-identical to the candidate. One room card
was baked, inspected and installed; its LFS filter remains set. The Biodome entry
in ORGANIC_ROOM_ROLLOUT.json now describes the current props and current card hash;
all other entries are preserved. No source raster or animation code changed.

Evidence: medium/room-biodome.png, four/, installed/, four.log, installed.log,
cards/biodome.png and card.log under output/room-comparison-2026-09-22. Existing
fern effects were not changed or newly certified. Owner visual acceptance and
updated playable exports remain open.
