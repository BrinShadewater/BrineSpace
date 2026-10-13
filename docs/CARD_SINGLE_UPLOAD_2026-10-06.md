# Project handoff

Updated: October 6, 2026 · BrineSpace · Single-upload mipmapped room cards

## Objective and acceptance
Remove duplicate startup uploads while preserving every selected card mip level
and fan-card filtering. No gameplay FPS or packaged platform certification claim.

## Accepted decisions and constraints
Art, filter choices and save rules unchanged. Raw runtime loading retained;
compressed crew still private. Scratch user paths verified and owner fingerprinted.

## Current state
`scripts/main.gd::_load_card_thumbnail` prepares raw image mipmaps before one
upload. The former path uploaded, read back, generated mipmaps, then uploaded
again. Import-only resources retain the previous fallback path. No cache added.

New native `tests/test_card_mipmap_loading.gd` and paired UID, registered in
render-perf. Physical Main generator `prepare-card-profile.py --cards` copies only
this current method into its controlled scene. Benchmark and regression evidence:
`output/compressed-crew-2026-10-06/card-mipmap-benchmark/`,
`card-mipmap-regression/`, and private `single-buffer/card-profile-single-upload/`.

## Verification
358 native checks pass: all 79 runtime cards plus an imported mipmapped fixture,
GPU bytes for the entire mip chain, dimensions/formats/counts, missing fallback,
and 36 exact fan raster pairs (six art families, nearest/mipmap filtering, three
rotations). Initial API preparation totals 617.437→552.061 ms.

Three 79-card same-process comparisons with alternating side order:

| Pair | Previous preparation ms | Single upload ms | Saving ms |
|---|---:|---:|---:|
| 0 | 550.628 | 542.085 | 8.543 |
| 1 | 601.645 | 535.191 | 66.454 |
| 2 | 584.433 | 469.378 | 115.055 |

Median paired saving 66.454 ms. Timer covers synchronous API preparation; GPU
readbacks outside it settle resources before the next side. Disk cache not flushed;
these are not cold end-to-end startup or FPS measurements. No benchmark engine errors.

Actual native title/transmission/Studio/save/title/Continue: 154 checks pass,
zero engine errors, restored crew and sampled resource release. Interface-art
stage observed 612.544 ms fresh / 239.458 ms Continue; separate generated sites
and single runs prevent overall matched speed claims. All 2,936 owner files
unchanged. Existing anonymous exit ObjectDB warning remains open in the private
full-scene lane; regression/benchmark processes exit cleanly. Registry parses and
UID is unique in scripts/tests/rooms.

## Next action
Prioritize recurring gameplay frame time and the measured large rover uploads,
keeping exact sampling constraints. Remaining shared-card readbacks can be revisited
with measured benefits; avoid retaining CPU images as a permanent workaround.
Storage admission, original bug closure, longer warning/endurance, memory and
packaged PC/Mac gates remain open.
