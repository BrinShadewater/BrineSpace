# Render-layer attribution handoff

Updated: October 5, 2026 · BrineSpace PC/Mac release readiness

## Objective and acceptance

Identify substantial rendering targets before changing visuals. This diagnostic
does not certify gameplay performance or accept hidden layers as an optimization.

## Accepted decisions and constraints

Preserve default effects, selected art, animation timing and owner layouts. No
release export or upload. All runs use isolated profiles and guarded user paths.

## Current state

New diagnostic scripts and raw results are under
`output/render-attribution-2026-10-05/`. No game runtime changes in this pass.
The fixture starts the maintained deterministic 40-room scenario at 1080p, then
freezes CPU simulation and measures retained rendering with one layer hidden.
Each measurement discards six frames and collects 24; CPU/GPU numbers are medians.
Shader time can still advance. This is current developer source, not a frozen
packaged candidate or minimum-spec certification.

The initial run exposed a one-time retained-command change after hiding/restoring
the station. The corrected `confirmed/` run settles that transition first,
reverses group order, and checks restored draw counts after every omission.

| Group | Draw calls removed | Render CPU delta ms | Render GPU delta ms |
|---|---:|---:|---:|
| All station surfaces | 2,925 | 6.016 | 5.382 |
| Environment passes | 1,301 | 2.867 | 2.495 |
| Floors | 1,221 | 2.480 | 2.236 |
| Room contents | 873 | 1.927 | 1.928 |
| Terrain | 798 | 1.723 | 1.924 |
| Walls | 445 | 0.726 | 0.293 |
| Foundations | 293 | 0.411 | 0.141 |

Groups overlap; do not sum them. Timing deltas include batching/overdraw interactions
and measurement noise. The ranking agrees with the initial pass, but tiny timing
deltas are not reliable independent cost estimates. Whole-station removal in the
corrected run removes 4,713 calls from the settled 4,987-call baseline.

`floors/` separately omits each room type from only the two floor passes, retaining
other rendering and simulation state. Largest totals: storage 166 calls (4 rooms),
hydroponics 146 (4), mining bays 144 (4), life support 117 (4), solar 112 (4),
research 104 (3). Cost is distributed rather than dominated by a single room.
Omission deltas need not sum exactly because batching boundaries change.

Source tracing establishes that “floors” includes connectors, floor surfaces,
light pools and equipment contact/projected shadows. Tile geometry already uses
cached meshes; projected shadow geometry is already cached and batched per foot.
Do not mistake this result for 1,221 unbatched floor-tile draws.

## Verification

- Corrected layer run: all 16 groups restore their baseline draw count.
- Room-type floor run: all 14 groups restore their baseline draw count.
- Both complete without engine errors; all 2,936 owner non-log files unchanged.
- Experimental omissions restored in-process and never written to layouts/settings.
- No FPS improvement or memory reduction claimed. Prior gameplay failures remain.

## Next action

Attribute floor subcomponents, especially equipment contact shadows in
`rooms/whole-room/room_lighting.gd`, before attempting larger batches. Preserve
overlapping alpha order, antialiasing and original geometry; require native pixel
comparisons across fractional zoom followed by matched active-gameplay benchmarks.
Room contents and terrain are the next independently measured targets.

Windows OS-level stalls still require permitted kernel tracing; Apple Silicon
native gameplay and signing/notarization remain unverified. These blockers remain
separate from render batching work.
