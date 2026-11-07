# Project handoff

Updated: October 5, 2026 · BrineSpace · Private animation textures

## Objective and acceptance

Test keeping animation pixels ready in CPU memory and presenting through a small
set of private GPU textures. Preserve source pixels, logical frame identity,
metadata, filtering and playback; measure memory and upload/frame costs before
normal gameplay integration.

## Accepted decisions and constraints

Owner authorized this isolated experiment. Original source art, immutable shared
GPU images and normal gameplay remain unchanged. Mutable presentation textures
are private to their presenter and never inserted in the immutable texture pool.
No PNG decoding on frame changes. Total RAM cost matters, especially on M1 shared
memory; lowering a GPU counter alone does not establish an overall memory win.

## Current state

Prototype only: `output/private-crew-texture-2026-10-05/bank.gd`, `probe.gd`,
`run.py`; evidence JSON/logs/source hashes and owner checks in the same directory.
Uses the selected Veld swimming-cargo turn manifests, bare and helmet: 12 clips
per gear / 192 frames, uniform 256×256 RGBA8. Existing deferred Player loader
creates original logical wrappers/metadata. Prototype decodes all surviving
images before playback, supplies original alpha extents and keeps those images
CPU-side. Each private presenter uses ImageTexture.update for a changed frame;
held frames skip updates. Normal Player clocks/snapshots select original logical
frames. Stable descriptors have unallocated diffuse textures; this is not yet a
drop-in replacement for production consumers.

## Verification

Godot 4.7.2 native Compatibility / RTX 4070 Ti, isolated profiles guarded by resolved
user directory. 4,347 validation checks pass: 1,536 exact native pixel comparisons
across every selected frame, actual linear filtering, four scales and integer/
half-pixel positions; original metadata, held-frame upload omission and independent
presenters. 1,080 playback comparisons use original Player at 30/60/120 sample
rates, 1×/2×/4× clocks, pause, clip interruptions, gear changes and snapshot
restoration. Not actual gameplay focus/input/save integration.

Three alternating matched pairs run 600 uncapped frames with two presenters,
switching clips/gear; first 60 frames excluded from frame statistics. Source bank
is shared CPU-side between presenters. Incremental allocations above fixture:

| Counter | Reference | Candidate |
|---|---:|---:|
| Engine texture accounting | 64.00 MiB | 0.515 MiB |
| Engine static CPU allocations | 0.815 MiB | 48.953 MiB |
| Retained decoded CPU pixel payload | 0 | 48.00 MiB |

All pairs reproduce allocation figures. GPU storage is approximately two full
256×256 images plus descriptor overhead in this fixture. Engine accounting is
not certified driver residency, and texture.update can change counter accounting.
CPU/GPU counters cannot simply be summed into physical memory, especially on Mac.
This is a potential discrete-GPU-capacity remedy, not a proven M1 RAM remedy.

Upload API-call p99 60/72/75 µs; maxima 434/406/406 µs. These are submission costs,
not isolated GPU execution. Full fixture frame p99 reference 0.812/1.203/0.827 ms,
candidate 0.684/0.653/1.548 ms; maximum frame <13 ms in either arm. Zero >50 ms
frames. Medians candidate 0.372/0.374/0.409 ms versus reference
0.331/0.317/0.298 ms: uploads add work; no general FPS improvement claimed.
Preparation ~162–173 ms candidate versus ~177–190 ms reference; no packaged
loading acceptance. CPU bank, Player and presenters release; final engine texture
accounting returns exactly to baseline. No errors or shutdown warnings in final
validation/comparison logs. All 2,936 protected owner files unchanged.

Initial type-inference setup error corrected. First benchmark retained its last
presenter in the upload-statistics loop: reference held CPU bank, invalidating
that teardown measure. Statistics moved into a helper, weak-release checks added,
and all three pairs rerun. Final comparison files supersede that prototype run.

## Next action

Keep this isolated. Add multiple simultaneous pose slots per character with draw-
frame leases before production: updating one texture twice before deferred drawing
would overwrite an earlier pose. Handle production get_size/get_image consumers,
reading/bunk composites, cached draw commands, effects and Bill historical bindings
without making logical wrappers mutable. Then test a complete selected character
bank, variable dimensions/formats, full-station frame pacing and peak/process RAM.
Native M1 total-memory checks and original release gates remain open. No runtime
feature flag, maintained test entry, export, frozen-source change or release claim.
