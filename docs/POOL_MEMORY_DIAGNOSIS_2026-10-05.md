# Bounded pool memory diagnosis

Updated: October 5, 2026 · BrineSpace PC/Mac readiness

## Objective and acceptance

Continue memory work while the owner is on mobile and cannot approve Windows
elevation. Reduce actual retained storage without changing selected pixels,
filtering, placement, timing or animation identity. No new release certification.

## Accepted decisions and constraints

The existing unelevated session cannot start the required kernel trace. Leave it
pending; do not bypass Windows permissions. Continue independent, reversible work.
Keep selected source art and frozen release candidates unchanged. No cropping is
accepted from storage estimates or offline reconstruction alone.

## Current state

Added opt-in `--texture-inventory` to the maintained benchmark runner. The pool
retains at most 20,000 weak upload records only when explicitly enabled, including
after normal lookup-table release. Reports include first source, encoded signature,
decoded bytes, dimensions, format, mipmaps, alpha bounds and expired/dropped counts.
No scene traversal, GPU readback or strong texture retention is required. Snapshot
collection happens after measured phases; default gameplay collects no records.
Unsupported older frozen runtimes explicitly report unavailable coverage.

Changed files: `scripts/crew_texture_pool.gd`, `tools/release_benchmark.gd`,
`tools/run_release_benchmark.py`, `tests/test_crew_texture_pool.gd`.
Evidence/helpers: `output/pool-inventory-2026-10-05/`.

The current-source 40-room native diagnostic completed:

| Pool | Live uploads | Decoded MiB | Collection time |
|---|---:|---:|---:|
| Crew | 8,188 | 1,535.56 | 18.284 ms |
| Rooms | 34 | 194.96 | 0.087 ms |

No records dropped. This is complete **within these pools**, not a complete GPU
allocation inventory. The raw engine counter is 5,139.36 MiB. Current source/art
differs from the frozen release; this is not a matched memory regression or frame
performance comparison. All three short idle phases still fail frame gates.

Read-only reconstruction of all 8,188 source images matches every recorded source
hash. Cropping alpha bounds with a two-pixel border and restoring the original
canvas is byte-identical for 8,152 images, with 1,254,674,448 bytes (~1.17 GiB) of
potential padding removal. The remaining 36 images fail exact reconstruction and
are excluded. This is potential decoded storage saving, not achieved GPU savings.

A separate native draw-rectangle experiment tests the 12 largest eligible savings
at five scales and nearest/linear filtering: 96/120 comparisons are exact. All 60
nearest comparisons pass; 24 linear comparisons at 0.73/1.37 scale differ by up to
2/255 per channel. **General cropping is not accepted.** No runtime crop, shader,
art, preference, save, package or engine replacement was installed.

## Verification

45 native pool checks pass, including identity, pixel/metadata parity, weak lifetime,
lookup release and explicit overflow coverage. Three runner safety tests pass;
Python compilation passes. The inventory run completes with no engine errors.
All native runs preserve 2,936 owner non-log files under isolated profiles. The
experimental renderer's initial type-inference parse error was fixed before its
120 comparisons; failed setup attempts are not accepted evidence.

## Next action

**Further October 5 experiments reject the nearest-only shortcut too.** Pool
auditing now records every distinct requested wrapper filter, including cache hits
where one storage serves mixed wrappers. `scripts/crew_texture_batch.gd` passes
the original filter; it does not change it. Native pool coverage now passes 46
checks, including mixed-filter cache hits. The new 40-room inventory reproduces
5,139.36 MiB on the raw engine counter, with these crew groups:

| Requested filters | Images | Decoded bytes |
|---|---:|---:|
| Inherited only | 1,462 | 311,620,704 |
| Explicit linear only | 6,626 | 1,270,848,768 |
| Inherited and linear | 100 | 27,685,120 |

Inherited does not guarantee nearest everywhere. The station grid requests nearest,
while portrait controls and some preview wrappers request linear. Source consumers
also read original dimensions, reconstruct/composite frames and compare pivots.
No accepted implementation can change these contracts casually.

Additional native experiments retain the same 12 images and five scales:

| Experiment | Exact / 120 | Nearest failures | Maximum channel delta |
|---|---:|---:|---:|
| Tight crop at half-pixel position | 49 | 47 | 255 |
| Crop dimensions restricted to original-size subdivisions | 96 | 0 | 2 |
| Original quad, shader remaps cropped sampling | 102 | 0 | 1 |
| Original quad/remapping at half-pixel position | 62 | 35 | 255 |

The subdivision experiment used the earlier fractional position, not half-pixel
coverage; its nearest passes do not certify boundary behavior. The shader approach
does not establish compatibility with existing crew effects or other GPUs. All
four candidates are rejected as general pixel-exact remedies. These are isolated
output-directory experiments; no cropping shader or geometry change enters runtime.
Every run preserves all 2,936 owner files. Evidence: `filter-summary.json`, the
four `crop-*-render.json` files and their isolated owner checks in the evidence dir.

A read-only decoded-pixel audit across both pools finds 13 duplicate groups with
only 2,013,952 redundant bytes (~1.92 MiB); all encoded source signatures match.
Adding full-image hashing to startup is not justified by this saving alone.

**Next: inventory non-pool storage using explicit bounded roots**, including
generated/mirrored crew banks, environment caches, room art and drone textures.
Avoid the earlier unbounded reflective traversal and GPU readbacks. Keep raw engine
accounting separate from decoded storage. Do not revisit cropping without a new
sampling explanation that passes camera-boundary cases. Windows scheduling trace,
frozen-package comparisons, minimum hardware, Mac native/signing/notarization and
the remaining release gates stay open. No memory reduction is claimed here.
