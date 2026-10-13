# West master-only regeneration

Updated: 2026-09-27. Project: Brine Space.

## Objective and acceptance
Owner requested fresh generation from approved master, noting size changes during
the mixed-source walk. Preserve accepted east and approved idle/master work.

## Accepted decisions and constraints
Only approved side master supplied to built-in image_gen. No old walk sources,
no per-frame scaling to conceal mismatch, no runtime promotion.

## Current state
character/veld-west-walk-master-v1 contains six-frame fresh west sheet, exact prompt,
uniform-scale extraction, manifest, master/motion GIF and contact sheet.
Source colour retained. No east writes. Prior attempts preserved.

## Verification
True alpha, six components, unclipped exports and manifest checks pass.
Inspected source and contact sheet. Head/collar20px-band width now31-32px, versus
28-32px in prior mixed v2; full height147-149px at common scale. This is a coarse
size proxy, not anatomy proof. Motion remains flawed: similar lead poses repeat,
near arm swing limited, far gear exposure varies. Not accepted or installed.

## Next action
Review fresh size-consistency GIF. Do not call this a finished walk or keep blind
whole-sheet retries; next motion approach must establish explicit alternating
contact poses while retaining a single consistent source scale/character.
