# Bill locker identity integration

Updated September 22, 2026. Broad animation/polish objective remains active.

## Objective and constraints
Repair the joined legacy locker art while preserving Bill's selected standing
identity, overall helmet preference and existing handoff behavior. No owner-room
edits, Higgsfield calls, publication or commit.

## Current state
Installed 24 bare/precomposed equip/remove frame replacements in major-bill-v3.
tools/build_bill_locker_identity.py reconstructs the preserved source with the
recorded scale, hard alpha and canonical palette. tools/rebuild_bill_art.py calls
it with the canonical idle endpoints before writing output. Existing canvas,
pivot, counts, timing, event timestamps and clearance are unchanged.
Other 2233 inventoried runtime PNG/JSON files are byte-identical.

tests/test_airlock.gd now checks actual selected Bill action textures against
installed source pixels during continuous capture. The full-art validator now
checks the already-installed bunk supplement explicitly: state set, order,
timing, canvas, pivot, furniture depth and source pixels. It retains the original
frozen ledger, rather than accepting unknown states or skipping supplemental art.
Updated pipeline acceptance guidance and installed mirror; source README explains
the canonical builder versus the earlier output-only study.

## Verification
Evidence: output/bill-locker-identity-2026-09-22/.
- Injected native verified preview and installed native run both exit 0.
- Installed: four rotations, 739 travel samples, eight complete action traces,
  360 native captures; selected texture pixels, fixed foot, service completion
  and inspector controls pass. Native shelf view and prior matching contact
  sheet inspected. installed-locker.gif combines the q0 action captures at 20Hz.
- Exactly 24 changed files match the reviewed study pixels; 2233 others unchanged.
- Full-art validation: zero errors, 1149 body and 1095 equipment frame references,
  780 original source frames and 113 source manifests preserved, no border touches.
  Initial outdated-validator failure remains preserved separately.
- Independent second canonical rebuild: all 2257 runtime PNG/JSON files exact.

This is controlled native action evidence, not an unforced expedition. Earlier
pressure-cycle/save checks exercised the same unchanged timing and controller;
this art-only pass did not repeat unrelated chamber tests. Owner motion judgment,
shelf-prop appearance and actual packaged validation remain separate.

## Next action
Continue shelf/equipment consistency and broader motion/expedition review. The
c0508d641e858e5e Windows/Mac packages predate these 24 replacements; refresh them
at the next release milestone. Do not inherit their acceptance for the new frames.
