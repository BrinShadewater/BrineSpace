# BRINE default entry doors

September 8, 2026. Owner requested doors at every BRINE entry by default. Closed unconnected sockets now render ceramic leaves and aquamarine seals in the existing wall plane. Raised north retains its themed riser door. Split connected/open spans do not draw the default leaves, allowing existing animated doors to take over. No new external traversal or room connections are enabled.

Changed `brine_core_view.gd` and BRINE card paths in both consumers. Native evidence: `cards/brine_core.png`; logs in `output/brine-default-doors/`. Personal layouts untouched. Remaining: owner visual review.

Verification: native four-door card visually reviewed; four rotations and sixteen doorway entries/returns pass (3,827 movement samples). Card/grid/variant consistency passes for 47 identities. The route fixture reports two resources still in use at shutdown after its PASS; this is a cleanup limitation, not a clean-exit claim.
