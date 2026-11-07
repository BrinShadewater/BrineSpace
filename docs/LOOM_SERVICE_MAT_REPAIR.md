# Gravity Loom service mat repair

The calibration-bench mat in `loom-composition-v2.json` is now 92x38 instead
of 112x38, retaining offset (-4,-3), colors and its host. This gives the
84-unit bench a small border without extending into the east hull at q2/q3.
No machinery placement, source art, walls, doorways or collision changed.

## Verification

- `output/catalog-mat-after-archive-20260906-v1.log` records the old failures:
  q2 right edge 190 and q3 right edge 196 against interior limit 180.
- `output/loom-mat-contained-20260906-v1.log` exits 0 for all four mat bounds.
- `output/loom-mat-review-20260906-v1` has four native rotation captures;
  q3 was visually compared with `output/catalog-mat-review-v1/gravity_loom-q3.png`.
  The revised mat no longer reaches into the wall.
- `output/loom-mat-state-20260906-v1.log` exits 0 with no engine errors,
  input isolation, three assemblies in four rotations, host state checks and
  1440 standable perimeter samples. These samples are not an actual NPC tour;
  injected-clock repeatability is not owning-clock pause gating.
- Native 512-square card bake exits 0 without engine errors. Card mat-v3 was
  visually inspected and LFS attributes verified. Current station fallback,
  card consumer and room manifest now select it; older cards are retained.
  The manifest's stale activity-v1 selection was reconciled with this revision.

Profile SHA256: `E677677D94B8719CE56A8271D6889AF639E437EEE81ABEABBBB7B591BAEC1822`.
Card SHA256: `9AA76702CE61A000F7237BF1AD9DEFAE086D7A4BFE8EC66FDB5636871444FD72`.

Fresh package evidence remains pending. The existing room-pipeline rule to fit
host-linked mats after final rotated placement directly informed this repair;
no new aesthetic rule or wall-height change was needed.
