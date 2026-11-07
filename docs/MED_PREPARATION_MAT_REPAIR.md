# Medical Bay preparation mat containment

The q3 preparation mat extended through the east hull. Its 150-unit width was
unrelated to the 72-unit host footprint: a host-relative offset of -5 placed the
far edge at x229. The mat now measures 82x39, retaining its offset, colour and
front-of-bench position. Its x extent at q3 is 79..161, within the -180..180
interior. No furniture, collision, walls, doors or bed contours moved.

## Integrated consumers

- `rooms/whole-room/med-bay-composition-v2.json`, SHA-256
  `0D0779E3B12047EC443CB2DB4A58B3B336256D286F85FAB9F04FB61D7F844AF8`.
- New native 512x512 card `med-bay-card-mat-v2.png`, SHA-256
  `91E613DAC43477C827579C882526448CF7785E04BCF9584F172F6BB9E21DE919`.
  Main card mapping, grid fallback and whole-room export manifest now select it.
  Its LFS attribute is verified; previous card retained.
- The manifest's profile hash matches the changed JSON. No source-image edit.

## Evidence

The composition audit now reports host-relative rectangular mats per rotation;
`--require-mats-contained` fails on missing hosts or rectangles outside the room
interior. `med-mat-before-v1` exits 1 on the real q3 overflow; `med-mat-after-v1`
exits 0. This check does not certify routes, decals or all procedural floor art.

`med-mat-contained-review-v1` captures all four rotations at 2x and 0.7x. The
production baseline q3 2x image was visually inspected: mat fully inside the
east wall and proportionate to its preparation bench. The new q0 card was also
inspected. The comparison tool still renders a separate bed-edge candidate;
that candidate is not selected by this card or the game.

`med-mat-state-native-v1` exits 0 without engine/script errors: input isolation,
four-rotation assembly containment, per-host powered/offline effects and socket
infill checks pass. Raw-image warnings remain. Its 808 legacy progress samples
are not current-controller movement evidence. Card bake and review capture also
exit 0 without engine/script errors.

Both pipeline repair-loop copies add mat containment and exterior capture-margin
requirements, match hashes and validate. The bible clarifies that floor-only
decorations share the containment requirement. This resolves the specific mat
overflow, not whole-room art acceptance. Fresh package verification and the
separate bed-edge integration remain pending.
