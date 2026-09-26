# Marsh north loaded swimming

Updated: September 22, 2026. Project: BrineSpace. Task: continue cargo presentation.

## Objective and acceptance

Repair rear-facing underwater pickup and loaded swimming. Integrated and technically
checked; normal expedition and owner motion acceptance remain open.

## Accepted decisions and constraints

No Higgsfield. Independently authored source, no mirroring. Cargo stays ahead of
the torso in the travel direction, with hands gripping forward and body occlusion.
No cargo-credit, controller timing, dry unloading or earlier art changes.

## Current state

Sources/prompts: `character/marsh-swim-cargo-v1/sources/north-loop-01.*`, corrected
`north-loop-02.*`, and `north-pickup-01.*`. Source01 was too elongated/upright and
is preserved but unselected. Source02 shortens projected back/legs while keeping
head and shoulders stable. Loop scale .25; pickup .28 with measured shoulders.

Direction-aware preparation/installation now includes north in canonical rebuild.
Runtime: `character/marsh-v2/supplemental/loaded-swim-north/`. Twelve selected frames,
224x208,pivot112,172,standingHeight148. Non-looping pickup has six150ms slots mapped
to existing0.52s action time; loaded loop uses six180ms slots and four poses in
0,1,2,3,2,1 order. Exact registered salvage and loaded-frame-zero endpoints.
Catalog, source contract and clearance updated; earlier PNGs remain unchanged.
Review GIF/contact: `character/marsh-swim-cargo-v1/review/north-chain-01/`.

## Verification

- All36 selected east/west/north frames reproduce exactly, with endpoint joins.
- Validator:184 states/926 references, no errors/border touches;211 source frames
  and one source manifest unchanged.
- Native player:90 rendered samples, exact loaded endpoint and paused-pose restore,
  zero failures. Agent inspected the contact and native rear loaded capture.
- Complete packs:20,767 checks, zero failures. Existing fixture source-loading
  warnings do not establish release compatibility.
- Evidence: `output/marsh-north-loaded-swim-2026-09-22/`.
- Native battery/route gate:PASS,93 route samples with recalculated clearance.
- No export, commit or publication. Full expedition visual acceptance remains open.

## Next action

South-facing loaded swim and pickup, then twelve cargo-swimming turns. Review
recall, water-to-dry continuity and full expedition before fresh builds/Mac testing.
