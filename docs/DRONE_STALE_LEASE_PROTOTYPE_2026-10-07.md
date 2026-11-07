# Project handoff

Updated: October 7, 2026 · Project: BrineSpace · Task: stale drone lookup ownership prototype

## Objective and acceptance
Reduce the attributed transient drone texture retention without changing pixels,
animation, retained canvas ownership, or introducing duplicate decode/upload work.
The full PC/Mac release performance and acceptance gates remain open.

## Accepted decisions and constraints
Private prototype only. Normal runtime source and art remain unchanged. Preserve
immutable images held by canvas pins. A weak lookup may reconnect a surviving image,
but must not keep an unused image alive. No FPS or physical VRAM claim.

## Current state
`output/compressed-crew-2026-10-06/test-drone-stale-lease.py` builds a private Motion
copy and native probe in `output/drone-stale-lease-2026-10-07/`.
Prototype connects frame-post-draw trimming through begin(canvas), scans stale
entries while over budget, and adds weak-image restoration to request, finish and
synchronous lookup paths. Test deliberately uses a 1 KiB budget; production budget
remains 256 MiB. No SessionArtCache integration has been made.

## Verification
Native isolated probe: 13 checks, zero failures/errors/warnings/leaked instances.
Recent images survive; stale lookup ownership releases without further uploads;
unheld image expires; held canvas raster stays exact; reacquisition preserves
identity and skips worker decode/GPU upload; expired weak lookup is removed;
replacement canvas pins/commands release the image; actual PNG worker loading and
transparent placeholder behavior pass. Three uploads and three trims recorded.
Owner fingerprint: 2,936 files before/after, zero changes. Process terminal.
Initial probe parse failed because seed() conflicted with Godot's built-in; renamed
fixture method seed_images before successful run. No engine runtime defect implied.

## Next action
Extend coverage for mixed recent/stale order, bounded weak metadata cleanup and
final session-owner signal/lookup release. Run real-atlas tests with the normal
budget and matched large-station gameplay, tracking reported memory, uploads,
decode work and frame timing. Retained pixel tests alone do not establish a
performance gain or justify normal-source admission. Continue zoom-stall work.
