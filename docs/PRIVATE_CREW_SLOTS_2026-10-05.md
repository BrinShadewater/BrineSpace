# Project handoff

Updated: October 5, 2026 · BrineSpace · Private pose slots and CPU source API

## Objective and acceptance

Extend the isolated animation-memory prototype to preserve simultaneous poses,
retained canvas commands, mixed selected frame dimensions and source-image access.
Measure bounded storage and submission/frame costs before gameplay integration.

## Accepted decisions and constraints

Original source art and normal runtime unchanged. Each character presenter has
private mutable storage; immutable source pixels remain CPU-side. Leases belong
to drawing canvases, not merely a process frame. A retained canvas cannot lose
its pose because another canvas redraws. Slot cap four in this fixture; overflow
is explicit and never evicts a leased image. That refusal has no production
fallback yet, so it is not suitable for interactive gameplay integration.

## Current state

New isolated directory `output/private-crew-slots-2026-10-05/`: `bank.gd`,
`slots.gd`, `probe.gd`, `run.py`, plus `cpu_frame.gd`, `source_api.gd` and guarded
API inspection/source runners. Previous prototype/evidence unchanged.
Bank adds the currently loaded Veld West action manifest to the swimming-cargo
turn bare/helmet pair: 216 frames, 184×184 and 256×256, 51.10 MiB CPU payload.
All pixels decoded before presentation. Slot acquisition occurs inside `_draw`
after the owner calls begin_draw: only that canvas's former leases are released.
Other canvases keep theirs. Same-frame requests reuse slots without upload; size/
format/mipmap changes use private set_image, matching configurations use update.
Owner exit releases leases; final-owner exit clears private GPU slots.

Engine introspection confirms Texture2D's virtual image/size/format/mipmap APIs.
Separate CPU-backed source texture supplies dimensions and independent get_image
copies, preserving metadata. It is a source API test, not a GPU-draw replacement
and is not substituted into the measured Player banks. No normal-script edits,
maintained test entry, export or frozen-build change.

## Verification

Godot 4.7.2 native Compatibility / RTX 4070 Ti with isolated guarded user paths.
3,280 slot checks pass: 2,592 exact native raster pairs across all 216 selected
frames, three overlapping poses, actual filtering, tint/alpha, clipped source
regions, three scales and integer/half-pixel origins. CPU pixels/dimensions match
reference; modifying a consumer copy leaves the bank unchanged. A second canvas
holds its pose across 32 other-canvas redraws. Repeated poses skip uploads, capacity
overflow preserves retained art, and owner exit removes leases/storage.

Three alternating matched pairs render 600 uncapped frames with one retained
canvas pose and three changing poses in another canvas. Warmup first 60 excluded.
All pairs agree on steady incremental engine counters:

| Counter above fixture | Reference | Candidate |
|---|---:|---:|
| Texture accounting | 68.13 MiB | 1.10 MiB |
| Static CPU allocations | ~0.99 MiB | 52.29 MiB |
| Retained decoded CPU payload | 0 | 51.10 MiB |

Counter reduction is not physical driver residency or a proven unified-memory
saving. Four slots, 1,801 submissions and 48 dimension replacements per candidate.
Upload API p99 47/46/40 µs; maxima 346/471/397 µs. Submission cost is not isolated
GPU execution. Fixture frame p99 reference 0.529/0.606/0.448 ms versus candidate
0.613/0.769/0.627 ms; candidate median 0.460/0.450/0.444 ms versus reference
0.326/0.290/0.288 ms. Extra work about 0.13–0.16 ms median. No frame >50 ms;
all maxima <1.3 ms. This small fixture does not certify full-station frame gates.
Weak release checks pass; engine texture counter returns exactly to baseline.

CPU source API: 2,593 additional checks pass across all 216 frames, exact source
bytes, copied metadata, size/format/mipmap properties and mutation isolation;
added engine texture bytes zero. Local engine API inventory retained in evidence.
All batches preserve 2,936 owner non-log files. Final native logs no errors or
warnings. Initial mixed-indentation setup error corrected before acceptance;
runner hash-list quoting error corrected without changing measured GDScripts.

## Next action

Keep isolated. Build complete selected-character coverage with CPU source adapters
and private presentation routing. Verify direct drawing, composites/reading/bunk
consumers, effects, retained rooms, multiple viewers and historical Bill bindings;
logical source textures must never be drawn directly with an empty GPU RID.
Make lease overflow preserve complete interactive drawing before enabling anything.
Measure full-bank peak/process RAM and full-station uploads/pacing, especially M1
unified memory. Earlier clock tests remain evidence for the previous prototype,
not newly exercised full-game saves/focus/animation joins. Release gates open.
