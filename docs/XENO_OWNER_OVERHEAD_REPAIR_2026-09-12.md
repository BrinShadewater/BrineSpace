# Xeno Lab owner overhead repair

Updated September 12, 2026. The Xeno Containment Wall now uses one canonical
strict-overhead bank in all four room orientations. It retains the sealed specimen
lid, containment hatch, scanner tray, inactive controls and glove-port identity,
with a shallow wall footprint and no tall front elevation. Exact quarter turns keep
the rear rail against each wall and place glove ports, controls and access edges
toward the room interior.

The earlier north elevation, unrelated south utility bank and tall side conversions
remain in source history but are no longer selected. A first replacement candidate
was also rejected because it retained a frontal product view and checkerboard-like
exterior. The selected transparent source was cleaned to its largest connected
silhouette before rotation; 1,483 disconnected alpha pixels were removed from 519
secondary components.

Native q0-q3 evidence is in `output/xeno-owner-repair-2026-09-12/candidate-native`.
Build hashes, rejection evidence and review findings are in
`assets/xeno-directional-v2`. The q0 capture is the live catalog card. Existing
independent room machinery, footprints, activity anchors and gameplay behavior are
unchanged.

The 176-layout, 20-side-variant and 47-card checks pass. The native
`test_xeno_registration` test still fails its inherited base-view workbench status
strip check at q1/q2. That test instantiates
`rooms/underwater/batch-two/xeno_lab_view.gd`, not the selected full-wall view, and
its source-aperture audit passes. This wall repair does not claim that separate
operating-effect issue is resolved.
