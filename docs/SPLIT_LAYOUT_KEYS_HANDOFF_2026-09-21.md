# Project handoff

Updated: 2026-09-21 · Project: BrineSpace · Task: Restore saved split-room furniture

## Objective and acceptance
Honor the saved bought-art layouts before improving their composition. Broader
Bill, room polish and release work remains open.

## Accepted decisions and constraints
No owner layout or library mark edits. No Higgsfield. Artwork IDs remain stable.

## Current state
split_wall_prop.gd accepts a separate optional layout_asset_id (legacy default is
asset_id). Seven view constructors supply their editor-catalog key: Storage Bay,
Battery Array, Hydroponics, Life Support, Data Archive, Command Center, Holographic
Core. Both initial application and unchanged-geometry application use that key.
Previously they read art IDs such as storage-wall while Studio/defaults stored
room-storage_bay, so saved props and removals were ignored. Refreshed seven room
cards. Added tests/test_split_layout_keys.gd plus UID and room-art test index entry.
Maintained/installed room pipeline and visual bible updated with the diagnosis.

## Verification
output/storage-composition-2026-09-21/: before/fixed native Storage Bay shows legacy
versus saved bought props. Four Storage views/640 samples pass; six other rooms
24 views/3,840 samples pass. 70 repeated/rotated fixture setups pass canonical-key
selection and saved prop retention. Player layout bytes equal owner-before.json.
Cards log reports seven baked. Native live capture is tracked in live.log separately.
Preview geometry and agent review are not owner visual acceptance. Historical
station screenshots/benchmarks predate these restored layouts.

## Next action
Inspect final live Storage capture, then compose purposeful large/medium groups
using the now-correct furniture. Preserve named owner rooms. Bill gait remains open.

Native live Storage q0 capture completed at both zoom levels and was inspected.
It honors the saved sorting-island placement at lower left; q0 retains its legacy
banks by the current saved design, while q2/q3 use bought props. Do not describe
all four saved rotations as fully migrated or visually accepted.
