# Hydroponics harvest mat repair

The harvest mat's old x-offset -76 and width 168 produced visible west-hull
overhang in q1 and q2. It now has x-offset -4 and width 96 around the unchanged
88-unit harvest bench. Height 58, y-offset -7, colours and every prop registration
remain unchanged. This is an authored fit, not a floor-wide clip or auto-clamp.

## Evidence and consumers

- `hydro-mat-before-v1` and `hydro-mat-after-v1` contain matched four-rotation
  native sealed-room diagnostics. The capture helper now accepts `--room=<id>`
  to retain all rotations of a repaired room even when none remain flagged.
- `hydro-mat-contained-v1` exits 0: both mats fit all four interiors.
- The q1 and q2 repaired images were visually inspected; neither harvest mat
  extends beyond the hull. The revised native 512x512 card was also inspected.
- `hydro-mat-state-native-v1` exits 0 without engine/script errors. Input isolation,
  five registered assemblies across four rotations, host-local on/off comparisons,
  repeated paused frames, containment and harvest-display envelope checks pass.
  The fixture's old 'four hosts' footer refers to primary machinery, not its
  complete five-assembly result. It does not establish independent production
  pause-clock gating, economy starvation or current-controller traversal.
- `catalog-mat-after-hydro-v1` retains 13 flagged placements in seven other rooms;
  its child 1 is an expected unresolved catalog audit, not a Hydroponics failure.

Profile SHA-256:
`72BE8BC2E047D192EC68145D4F1961AB00BFC2C15626A2CBD6FA24ABB5E04B83`.
Selected card `hydroponics-card-mat-v2.png` SHA-256:
`0FF4CB2785B48BDF9B62D6271980681CB171918D9054CA05E0A43A60487BE57D`.
Main card mapping, grid fallback, variant list and whole-room export manifest
all select the new card; profile provenance is updated and LFS verified. Earlier
art is preserved. Raw-image warnings remain in native logs.

No room geometry, source pixels, costs, synergies or player save changed. Fresh
package verification remains pending and can cover the remaining mat repairs
together after their individual native review.
