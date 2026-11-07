# Other crew locker review

Updated September 22, 2026. Broad goal remains active.

## Objective and constraints
Check the other human crew after Bill's locker repair. Preserve current character
and room art unless evidence supports a repair. No generation or owner-room edits.

## Current state and verification
Evidence: output/airlock-all-crew-2026-09-22/ and its adjacent dated logs.
Headless shared regression passes 1191 travel samples, equipment handoffs,
interlock phases, power interruption, pause and disk restores. Exact scope:
Bill q0-q3; Veld q0; Branforth q0. Not every actor in all four rotations.
Native focused runs each pass 223 travel samples and complete equip/remove
captures. Veld additionally checks actual selected frame pixels against source.
Both processes exit 0 without engine/script errors. Contact sheets and canonical
source/idle comparisons inspected. Dedicated controlled fixtures, not unforced
expeditions, other rotations or packaged acceptance.

Veld's observed poses retain her selected identity sufficiently to leave the
current art intact; owner motion acceptance remains separate. Branforth's interior
action frames have different head shape, suit detail and proportions than the
correct exact standing endpoints. Native movement/service succeeds, locating
the repair in source art rather than requiring a timing or navigation change.

The maintained test now logs explicit actor/quarter cases instead of its ambiguous
"all three architects, four rotations" wording. This reporting-only change follows
the recorded runs; it will be exercised by the next relevant repair regression.

## Next action
Trace Branforth's canonical pickup/don/remove sources, build a coherent replacement
using his current idle references, preserve event timing and standing endpoints,
and verify actual selected frames plus native shelf contact before installation.
Do not regenerate Veld or alter protected layouts as part of that repair.
