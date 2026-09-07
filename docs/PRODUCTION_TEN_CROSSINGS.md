# Production walker crossing captures

The seam fixture now supports `--crossings`. It advances `_update_test_walker()`
in controlled time steps instead of assigning each sampled path position. All
forty room/rotation pairs arrive in the neighboring Battery Array. Each crossing
has seven native frames at 0, 25, 45, 50, 55, 75 and 100 percent progress, using
one common 30% zoom. `crossings.json` records the requested fraction, actual cell,
room, rotation, viewport and zoom; all 280 indexed files exist.

Evidence: `output/production-ten/crossings-native-1600/`, `crossings-1600.log` and
`.err`. Exit zero; no ERROR/SCRIPT ERROR entries. Three Command Center q1 frames
at 45/50/55 percent were inspected: the walker approaches, occupies and leaves
the open doorway without visible equipment overlap. Remaining sequences await
visual review; captures alone are not acceptance. This uses controlled calls to
the production state machine while the game is paused, not a free-running long
station simulation. The fixtures retain isolated saves and ordinary economy rules.

The common zoom improves comparability over auto-fit, but is not a closeup.
High-detail occlusion, incompatible neighbors, mature mixed stations and standalone
release export remain separate work. Inherited raw-image warnings persist.

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
