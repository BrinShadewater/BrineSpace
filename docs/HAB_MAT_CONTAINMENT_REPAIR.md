# Crew Hab mat containment repair

The chair mat changes from offset (-25,9), size 106x45 to (-21,9), 98x45.
The desk mat changes from (-8,18), 112x42 to (-4,18), 104x42. Each loses
four units at both lateral edges, preserving its center and furnishing alignment.
The green woven rug, props, source textures, walls and collision are unchanged.

The original q1 desk and q2 chair captures were inspected. The three flagged
rectangles extended three units beyond the conservative interior bounds.
`output/hab-mat-contained-v4.log` now passes all four rotations. Four new native
captures are in `output/hab-mat-review-v4`; q2 was inspected against the old view.

`output/hab-mat-state-v4.log` exits 0 with no engine errors, input isolation and
eight-assembly/four-rotation host state checks. Fixed injected-clock repeats
are not owning-clock pause proof; this is not a new NPC traversal test.

Native 512-square card mat-v4 was baked, visually inspected and LFS-checked.
Primary card, station fallback, variant list and export manifest select it.
The variant list's four pre-redesign images remain on disk but are no longer
selected by that list. The composition manifest hash is reconciled.

Profile SHA256: `1FB4C9D1E53D13F983A0C486921094C57D5B6F5B92EBCB5AF9E519B46D725F07`.
Card SHA256: `4CFE5D78BEE0A9EE5DA2574599D1F56804710238CF9A36467E21F0256680ED72`.

Fresh batch package verification remains pending; earlier packages retain the
previous mat sizes. This applies the existing pipeline, not new art direction.
