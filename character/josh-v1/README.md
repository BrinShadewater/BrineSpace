# Josh runtime pack

Larger muted bluish lavender Johnny 5-like robot; selected identity is
../companions/josh-portrait.png. Owner correction explicitly requires treads.
sources/motion.png is the current twin-tread sheet. superseded-biped.png and its
prompt preserve the earlier abandoned direction and are not loaded at runtime.

Built-in image_gen sources and exact prompts are retained. Actual row facings are
south, west, north, east; no mirroring. tools/build_companion_sprites.py performs
deterministic white-background removal, gutter detection and foot registration.

Eight clips / 24 PNGs: two-frame idle and four-frame tracked travel, four directions.
92x92 canvas, pivot (46,86), maximum visible height 70 source pixels versus River's
44. Existing renderer scale is 65.28/74. walk is the shared playback key for rolling,
not a claim that Josh walks on legs. Native instance follows crew through connected
rooms, preserving independent playback and RNG through Continue.

Generic sprite manifest validator: zero errors/warnings. Native emergence, travel,
size comparison and selection visually inspected. Owner motion acceptance pending;
four generated rolling poses contain subtle suspension/arm variation, not a long
continuous tread study. Review: ../companions/review.html. No executable export.
