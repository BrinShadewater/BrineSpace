# Station composition and rare-room operating effects

Reviewed the current 44-room catalog through the station renderer at 1280, 1600 and 2560 widths, with fifteen neighboring-room captures at initial 52% zoom. Retained department contrast: medical/science interiors are intentionally lighter than engineering and security. No broad recolor, furniture enlargement or automatic layout rewrite was warranted by the inspected views. Owner drafts are isolated from this fixture. This compact catalog arrangement is a visual adjacency review, not a claim that every arbitrary pair has reciprocal ports.

Pressure Control now has restrained gauge motion; Listening Post has a slow sonar sweep. Anchors follow the actual prop visual rectangle and distinct horizontal/side views. Effects use the existing operating flag and visual clock, remain within instruments, and introduce no bloom or room-wide brightness lift. Original source art, geometry, layouts and idle cards are unchanged. Existing baked screen traces remain artwork; the new motion stops offline.

During validation, three newly added full-wall wrappers (Biodome, Tidal Condenser, Solar Array) called nonexistent split drawing methods on their base classes. Removed those unsupported overrides; their registered draw path and authored art remain intact.

Evidence:
- output/station-composition-v1: overview and normal-zoom neighbor captures.
- output/composition-corridors.log: straight, corner and T corridor/foundation checks in all rotations; taper coverage passes.
- output/composition-routes-v1: Pressure Control and Listening Post production crew routes in all four rotations, zero assertion failures. Scheduled destinations exercise real crew movement; this is not a natural autonomous-tour claim.
- output/rare-effects-test and output/rare-motion.log: two rooms x four orientations; changed operating pixels, identical offline pixels, actual owning-clock pause/resume and rendered pause/resume checks.
- output/composition-effects-v1: full-wall geometry and state review.

The reusable station fixture waits for zoom/layout settlement before focusing rooms; otherwise the first close capture could show the previous camera location. Raster sources were not edited. No gameplay balance or player-save changes were made.
