# Remaining catalog mat repairs

This closes the recorded rectangular-mat bounds queue, not full room acceptance.

Anomaly's cart mat changes from offset (-4,-3), 64x32 to (-1,-3), 58x32:
three units removed from each lateral edge, preserving its center. Maintenance's
repair-machine pad changes from 114x42 to 108x42 with offset (-3,29) unchanged.
Props, source art, walls, doors and collision are untouched.

`output/catalog-mat-contained-20260906-v2.log` exits 0 without engine errors:
128 mat placements checked, zero outside the interior. The live tool resolves
34 room views; procedural rooms and non-mat floor effects have separate scope.
Earlier 35-identity/33-view totals are historical, not current catalog coverage.

Before images `catalog-mat-review-v1/anomaly_lab-q3.png` and
`maintenance_bay-q2.png` were inspected. Four-rotation native captures in
`output/anomaly_lab-mat-review-v3` and `output/maintenance_bay-mat-review-v3`
exit 0; the same previously flagged rotations were inspected after repair.

Both new 512-square cards were baked, visually inspected, LFS-checked and selected
in their station/card/manifest consumers, including Maintenance's variant list.
Old cards remain. Composition hashes were updated in their respective manifests.

| Asset | SHA256 |
| --- | --- |
| Anomaly profile | 118AF494D1ED1E8CF1FA30515274A5B2CF1D8978E96BD63819EBF905BEA5EBAE |
| Anomaly card mat-v2 | 84730FBC88067C18D7CA46413ACB6659C1AB936397BABBDC9A85351FB30CA3C7 |
| Maintenance profile | 59B1B4E137E2615D88052C0DD947F9085CF07D3757BF3AC8FA2179861CB1B4A8 |
| Maintenance card mat-v3 | 80AD6A1849D7570D2258A8B6EDC9955F4CAB602F35674EBC669598C366C066EB |

## State tests and remaining work

`output/maintenance_bay-mat-state-v3.log` exits 0 without engine errors:
eight assemblies, four rotations and 1092 route samples pass. This is not an
actual NPC tour or fresh package; injected-clock repeats are not pause gating.

`output/anomaly_room-mat-state-v3.log` exits 1 with one assertion:
`Anomaly assemblies do not overlap`. The mat edit does not move props. Inspect
the implicated silhouettes and distinguish real contacts from empty rectangular
bounds before adjusting placement or refining tests. Do not call this room's
broader state acceptance passed. Fresh packaging for the repair batch remains open.

## Anomaly lamp follow-up

The q3 cart/lamp contact was real: registered cutout intersection area was
81.078369140625 square world units. Moving only the task lamp's q3 center from
(-110,110) to (-90,110) clears it; the existing all-pairs overlap assertion remains
unchanged. `output/anomaly-lamp-state-v4.log` reaches `ROOM SCENE PASS` with zero
assertion failures, including six assemblies, four rotations, actual economy
states and 404 socket samples. This is not an actual crew traversal claim.

Fresh `output/anomaly-lamp-final-v5.log` exits 0 with no floor/visual overlaps in
any rotation and all rectangular mats inside the interior. Raw-image loading
warnings remain, with no engine errors. The q3 native image in
`output/anomaly-lamp-clearance-v4` was inspected: lamp and cart are separated.

Current profile SHA256 is
`43B80F2D631F9FBC2093AA7F9C654881270B2A4161BBE6640C9D0EA20B3BF72A`,
already matched by the batch-two export manifest. The proof bake at
`output/anomaly-lamp-card-proof-v4.png` matches the selected mat-v2 card exactly
(`84730FBC88067C18D7CA46413ACB6659C1AB936397BABBDC9A85351FB30CA3C7`),
so no duplicate production card is needed for a q3-only adjustment. Fresh batch
packaging remains pending.
