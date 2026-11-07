# Second ten-room batch

This task owns Cryo Chamber, Clone Lab, Data Archive, Biodome, Xeno Lab,
Anomaly Lab, Bio Lab, Holographic Core, Medical Center and Medical Office.
The owner's other session owns the earlier ten listed in the rollout ledger.

Ten source candidates generated using built-in image generation and inspected.
Exact prompts and department/equipment briefs: production-briefs.json.
Native dimensions, immutable source hashes and per-room findings: source-review.json.
All images are opaque 1254-square RGB, not transparent sprites or 1280 exports.

Current stage: Cryo Chamber, Clone Lab, Data Archive, Biodome, Xeno Lab and Anomaly Lab registered and
station/card integrated, with scoped native checks in CRYO_INTEGRATION.md,
CLONE_INTEGRATION.md, ARCHIVE_INTEGRATION.md, BIODOME_INTEGRATION.md and
XENO_INTEGRATION.md and ANOMALY_INTEGRATION.md. Bio Lab is also integrated with
three-viewport economy tests (BIO_INTEGRATION.md): seven integrated rooms total.
Holographic Core is also integrated (HOLOGRAPHIC_INTEGRATION.md), bringing this
batch to eight integrated rooms. Medical Center is now integrated too, with
three-viewport economy/route/depth evidence (MED_CENTER_INTEGRATION.md): nine total.
Medical Office is now integrated too (MED_OFFICE_INTEGRATION.md).
All ten have live station/card integration and scoped native evidence;
that is not ten fully accepted rooms.
Retain useful furniture; bind it to the existing 384-cell / 48-module / 72-door
contract. Rotate ground centres, keep upright art south-facing, and validate full
silhouettes inside walls. Do not rotate the source bitmap. Sources with wrong
walls remain usable prop candidates, not accepted room geometry.

Next: batch-wide cleanup and acceptance. Finish residual source gaps/indicators,
cross-room route/seam coverage, remaining depth-review gaps and package/export
verification. Per-room integration records own exact tested scope. Coordinate
shared main/grid renderer edits with the other session.

Combined first/second-batch geometric connection evidence is recorded in
CROSS_ROOM_VERIFICATION.md. Use connection-manifest.json with the existing
connection and production-walker tests' --additional-manifest option.

Reproduce the integration-record audit:
`python tools/audit_batch_two_integration.py` verifies source hashes, selected
station/card agreement, card dimensions and record/view/UID presence. It is a
read-only consistency audit, not a gameplay or art acceptance gate.
`python -m unittest discover -s tests -p test_batch_two_asset_audit.py` checks
the current pack and rejection of stale stages, duplicates, hash drift and paths
outside the checkout. `test_batch_two_resource_uids.gd` validates 47 paired IDs,
including generated export fixtures.
`tools/capture_registered_prop_edges.gd` provides offline dark/light contrast
renders of the actual prop draw path. Biodome's first contour repair and remaining
fringe findings are recorded in BIODOME_INTEGRATION.md.
PROP_EDGE_REVIEW.md records inspection of all forty props on both contrast
backgrounds, with prioritized contour and offline-material findings. Review
sheets verify capture hashes and preserve native pixels rather than resizing.

Standalone Windows mixed-station validation now passes for all ten alongside the
first batch. Individual exported fixtures also pass at 1280, 1600 and 2560 widths;
see EXPORT_VERIFICATION.md for exact evidence and remaining scope.
Those mixed-station passes precede the new needs-driven character controller.
The latest V6 combined visitation check fails (23/30); individual room-state
checks pass. V7's separate controlled tour physically traverses all 30 rooms using
the current NPC; it does not change the failed behavioral gate. See
CURRENT_CONTROLLER_TRAVERSAL.md and the caveat in EXPORT_VERIFICATION.md.
The export-manifest.json is checked against current sources and card consumers
by the integration audit; it does not replace source-review.json provenance.

Reproduce the non-destructive source comparison:
`python tools/review_room_batch_two.py`
Output: output/batch-two-source-review-v1.png. This is not gameplay evidence.
