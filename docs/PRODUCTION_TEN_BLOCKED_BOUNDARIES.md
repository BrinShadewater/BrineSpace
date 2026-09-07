# Incompatible adjacent-room boundaries

`tests/playtest_production_ten_blocked.gd` places each subject beside Research Lab
with its single socket pointing away from the shared boundary. Across ten rooms
and four rotations, production neighbor selection rejects all forty connections.
One hundred walker updates per case leave the actor in the source room with no
next destination: 4,000 blocked updates total. All assertions pass at 1600x900;
process exit is zero and stderr has no ERROR/SCRIPT ERROR entries.

Evidence: `output/production-ten/blocked-native-1600/`, `blocked-1600.log` and `.err`.
Command Center q0 and q1 frames were visually inspected: both show an uninterrupted
shared wall, no doorframe/open socket, and the actor remaining inside Command.
The other thirty-eight captures await visual review. Auto-fit zoom differs by
orientation, as in the earlier seam fixture; this is not equal-detail closeup
acceptance. Inherited raw-image export warnings remain.

This checks a neighboring room lacking a reciprocal socket, complementing the
open-connection fixtures and the disconnected edge assertions. It does not
certify every department combination, full crossing occlusion or release export.

## Complete sampled doorway review

The focused native-pixel contact sheets in
`output/production-ten/crossing-review-sheets/` were inspected in full. All forty
crossing sequences (280 sampled doorway frames) and forty blocked-boundary centers
were reviewed. Crossing samples keep the walker in the opening with no visible
nearby equipment overlap; blocked centers show continuous infill without false
door trim. This supersedes the earlier partial-review count above.

`review.json` records crop bounds, sheet hashes, findings and limits. Diagnostic
crops preserve 100x100 native pixels and leave originals untouched. They do not
prove every intervening animation frame, every neighbor material combination or
full-room silhouettes. Those remain bounded by the existing fixture scope.
