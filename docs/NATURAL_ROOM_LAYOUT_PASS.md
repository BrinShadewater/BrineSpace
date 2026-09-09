# Natural layout, floor density and palette pass

The fifteen full-wall rooms now carry explicit activity briefs and preferred
furniture positions in `rooms/full-wall-v1/activity-layouts.json`. Twelve have
movable activity groups; Pressure Control preserves its owner-selected composition,
and Listening Post/Isolation Vault preserve baked wings. Existing geometry resolves
the authored positions around actual doors and other furniture in each rotation.
Large objects settle first; pending objects keep their space until placed. This
prevents fallback placement from overlapping earlier moves. Sources remain available
when there is no clear space. The live drone and recovered cryo layouts remain intact.

Department floor sheets now repeat twice per axis rather than stretching once over
the room. Four-panel source sheets therefore read as eight smaller panels across.
The source remains the only material seam layer; no competing grid is added.
Construction scale, door apertures and collision are unchanged. Profiled surfaces
use this density; procedural corridor geometry retains its existing treatment.

Color review covers all 33 full-wall registrations, with decisions and diagnostic
brightness values in `rooms/full-wall-v1/color-review.json`. Dark frames, restrained
highlights and department materials are the common standard, not equal brightness.
The unused pressure source is labelled explicitly. Crew Hab was the domestic outlier:
its horizontal and side bedding now match the approved autumn lounge reference.
Clinical cream/blue, organic green and engineering charcoal/safety accents are retained.

Validation: 15 rooms × 4 rotations × 2 operating states; all 15 rooms' four-rotation
production crew routes pass with zero assertion failures. The catalog host/mat
audit has no errors. Floor harness renders 43 identities / 344 samples (corridor
state duplicates are not distinct offline coverage). All 43 selected room cards
were refreshed with verified paths/hashes. Cutout source/hash regression tests pass.

Evidence: `output/natural-room-pass/`; final full-wall sheets and composition
coordinates: `output/full-wall-v1/previews/`. These are native acceptance results,
not packaged-build evidence. Visual naturalness remains an owner-review judgment;
the activity briefs make subsequent adjustments explicit and reviewable.
