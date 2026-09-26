# Branforth locker identity integration

Updated September 22, 2026. Broad animation, furnishing and polish goal remains active.

## Objective and constraints
Match Branforth's locker actions to his selected standing identity while preserving
existing behavior and exact endpoints. No owner-room edits or publication. One
built-in image-generation call; no Higgsfield. Raw source and exact prompt preserved.

## Current state
Twenty interior equip/remove PNGs replaced; four exact standing endpoints and
2181 other inventoried runtime files unchanged. tools/build_branforth_locker_identity.py
uses the preserved source, single scale, canonical palette and registered cleanup
masks. The raw generation erroneously put faces in carried helmets; masks remove
those interiors before extraction. Existing timing, event timestamps, counts,
canvas, pivots, clearance and controller behavior remain unchanged.

tools/rebuild_human_crew_art.py invokes this repair and now resolves archived
construction inputs through the existing source resolver. The resolver also handles
the explicitly archived crew-helmet-fit-v2 family. Original ledger hashes remain
intact. Human frame writes now reuse the atomic write-if-changed helper after a
direct PNG write failed; no specific external locking cause was established.

tests/test_airlock.gd supports --all-rotations for any human and checks selected
Branforth source pixels as it already did for Veld. The human validator now checks
explicit bought-bunk contracts and Marsh's existing legacy berth registration,
order, timing and depth; it no longer rejects these accepted supplemental states.
Pipeline guidance, installed mirror and visual bible record the source/cleanup
and rebuild lessons.

## Verification
Evidence: output/branforth-locker-identity-2026-09-22/.
- Candidate and installed native runs: four rotations, 739 travel samples each,
  eight completed equip/remove traces, 360 captures, fixed feet, selected source
  pixels and UI checks pass; exit 0, no engine/script errors.
- Source board, native shelf views and installed contact sheet inspected.
  installed-locker.gif combines q0 captures at their 20Hz simulation sample rate.
- All 24 selected frame pixels match the reviewed candidate. Exactly 20 changed
  files; 2181 unchanged. Hard alpha, clear borders and local extraction parity pass.
- Independent full canonical repeat: all 2201 runtime PNG/JSON files exact.
- Branforth validator: zero errors, 1119 body +1071 equipment frame references,
  669 original frames and 108 manifests preserved. Veld validator also passes;
  Marsh passes 734 body references after explicit legacy berth coverage was added.
- Failed archive-path/direct-write attempts and the original overly broad expected
  change set (24 rather than 20 because endpoints were already exact) are separate
  diagnostic evidence, not accepted builds.

These are controlled native actions, not unforced expedition or packaged acceptance.
No new signing, Mac runtime or owner visual acceptance is claimed.

## Next action
Continue shelf/equipment consistency and ordinary expedition review, then refresh
packages at a release milestone. Current c0508d641e858e5e builds predate both Bill's
and Branforth's locker repairs. Preserve Veld's accepted art and protected rooms.
