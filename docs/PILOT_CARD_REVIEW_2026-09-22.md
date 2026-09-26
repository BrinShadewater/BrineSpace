# Current pilot card review

September22,2026. Reviewed selected Maintenance Bay, Bio Lab and Crew Hab cards.
Maintenance groups CNC/parts and manual/robot repair areas; Bio separates preparation
and analysis; Crew Hab separates sleeping/storage from seating. Open central areas
visually separate these uses. Keep current installed versions pending owner feedback.
This is card-only review, not a new route/rotation/live-operation acceptance.

Only visual_review in those three ORGANIC_ROOM_ROLLOUT.json entries changed. All
other ledger fields/entries are equal to the saved backup; no art/layout changes.
Each review binds the inspected card's SHA256 and explicitly states scope.
Maintained engine inventory:47cards,0errors;4current/3stale/40missing review bindings.
Compare hashes against the runtime-selected card, not simply the ledger's own path:
a retired card can still match its old review hash while no longer being selected.
Evidence: output/room-card-review-2026-09-22/inventory.json, inventory.log,
ledger-before.json and guarded record.py. This does not auto-approve other rooms.

Report follow-up: tools/build_room_composition_review.py now displays recorded
review scope beside the status rather than hiding the distinction in details.
Missing legacy scope is explicitly unspecified, not inferred as live acceptance.
Generated review.html contains47entries and all3newcard-only scope statements;
content checks pass. No browser-layout or new station visual acceptance claimed.
