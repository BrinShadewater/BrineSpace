# Project handoff

Updated: October 14, 2026 · Project: BrineSpace · Task: prototype cache reuse and visibility

## Objective and acceptance

Owner approved the next measured target from the expanded room-image experiment:
avoid unnecessary zoom-time recapture and per-frame visibility churn, preserving
live crew/doors/warnings and original close rendering. Compare against the frozen
expanded prototype, not an unrelated historical FPS number. Keep changes private.

## Accepted decisions and constraints

Same eight ordinary room types and three large rooms, zoom thresholds, image sizes,
source filtering, one-room-per-frame capture budget and readiness callbacks. Only
ordinary RoomContentCanvas policy changes. Standard library queues require explicit
layout_flip; custom/portable/interactive/actor/wet/hazard cases retain original drawing.

Capture generation follows a deep snapshot of room ID, renderer script, complete
ordered expanded items and static state, rather than retained-slot apply serials.
Camera placement is applied to the canonical image without recapturing it. Count,
geometry, nested registrations, texture-resource identity, kind/order, operation,
layout revision, bounds, filtering and Reduced Motion remain invalidating inputs.
Texture pixels are immutable after loading in this scope; in-place texture edits
would need explicit revision invalidation. No new image/animation assets.

The full visibility mask records normal culling decisions independently of raster
hiding. Live slots restore on exit/invalidation; cached advance updates clock/water,
checks current eligibility, then skips hidden redraw work. The image redraws only
when its destination changes. Unselected/occupied/hazard rooms avoid semantic-copy
work, and a pending new image remains hidden until ready.

## Current state

**Normal game source and Windows delivery remain unchanged.** New drivers/fragments:
`output/room-lod-reuse-20261014/`; frozen source, packs, JSON and logs:
`C:/bs-room-lod-reuse-20261014/`. Reuse the existing physical QA runtime only, serially.
Reference source is byte-frozen from the expanded candidate; candidate changes only
private RoomContentCanvas. Preserve all earlier prototype evidence.

Same actual release/debug=false fixture, RTX 4070 Ti, Godot 4.7.2 Compatibility,
1920x1080 secondary display, muted/disabled input/fixed window, fresh scratch APPDATA,
resolved profile checks, source/instance hashes and owner fingerprints. No export,
commit, publication, gameplay change or source admission requested.

## Verification

Native original prototype: 22 checks, two expected failures: unchanged advance causes
visibility transitions; equal-value props plus serial-only change rebake. Candidate:
**30 checks / zero failures**. Positive invalidation checks cover nested geometry,
flip, texture resource, kind, order, tail, operating state and in-place prop mutation.
Prior actual Bill/fire fallback and close-pixel checks remain green; all frozen states
match. Independent read-only source review found no actionable issue.

Matched native timing completed serially: 5,760 steady + 8,640 zoom frames =
**14,400 measured frames**, 36 exact state/camera comparisons. Each lane uses fresh
scratch progression. Steady: idle/pan/zoom/lighting at 1x/2x/4x, 120 samples/phase.
Hitches: cold/repeated/interrupted zoom at 1x/4x, 360 samples/phase, normal animated
0.20/0.32 requests and fixed station center. Both execution orders retained.

| Comparison | Expanded reference mean | Reuse candidate mean | Candidate change | P95 improves |
|---|---:|---:|---:|---:|
| Steady, reference first | 27.981 ms | 28.470 ms | 1.75% slower | 7/12 |
| Steady, candidate first | 27.503 ms | 26.784 ms | 2.62% faster | 7/12 |
| Zoom, reference first | 27.551 ms | 28.177 ms | 2.27% slower | 2/6 |
| Zoom, candidate first | 29.677 ms | 26.780 ms | 9.76% faster | 5/6 |

These results do **not** establish a reliable whole-frame/FPS or hitch improvement.
Candidate passes 0/24 steady and 0/12 zoom phases at the existing gate (p95 <=16.7,
p99 <=25, maximum <=100 ms). Steady live-room mean CPU drops 6.747->6.563 and
6.602->6.192 ms, but total frame variation is larger. Draw calls barely change.
End texture memory is identical per matched pair: 2,107.87 MiB steady, 2,227.47 MiB
zoom. Do not compare these totals directly to earlier experiments with other scopes.

Redundant work is demonstrably removed: both steady runs finish with 130->30
cumulative captures; both zoom runs record 284->86 captures (69.7% fewer). Both lanes
retain at most one capture owner/frame. Eligibility and actual content still invalidate.
Zoom candidate maxima are 91.024/77.022 ms vs reference 88.359/110.030 ms. Whole zoom
frames >50 ms are 55/23 candidate vs 34/50 reference; candidate has no >100 ms zoom
frame. Thirty-frame windows after each far request also remain mixed: forward maxima
improve 2/6, reverse 5/6. No hitch-free claim. See `entry-windows.json` for the exact
request-window definition and samples; these windows are requests, not capture events.

The forward steady candidate's 101.050 ms zoom-1x outlier overlaps two mining body
sheet uploads: 275.625 MiB / 42.042 ms upload API time. Before-render wall time is
89.804 ms; grid drawing 83.199 ms includes exterior actors 54.267 ms, while live rooms
record 6.994 ms. Cache counters remain 29->29 throughout that phase (reference 29->57).
This points toward a separate upload/exterior-drawing hitch source. Overlapping scopes
must not be added; delayed viewport queries do not establish that frame's GPU cost.
Read-only independent analysis: `steady-zoom1-hitch-analysis.json`.

Final distant captures at fitted zoom and 0.24 visually reviewed: no obvious new
artifact. Frozen repeats are exact; 0.30/0.50 full fallback remains pixel-exact. This
does not establish all animation frames, rotations or tint/material combinations.
All nine accepted native/timing runs verify loaded source and immutable overlay
identity; no engine errors or SafeImage failures. Twelve owner guards preserve all
2,948 files; normal five runtime sources match pre-prototype references. No QA game
process remains (existing editor left alone). Evidence: `final-audit.json`,
`steady-analysis.json`, `hitches-analysis.json`. Candidate pack SHA-256:
`b53a14bc0cd44fbea2642763eeeb762b8008329ce9f46d2ea617220712b1c253`;
reference is the previously accepted expanded pack
`2a613b14040dab84dda01afef6c9d4eab31184c22207a383943faab3a4e9dd3c`.

## Next action

Keep this candidate private: structural savings are verified, but whole-frame gains
are mixed. The next evidence-backed target is mining-drone body-sheet upload timing
and exterior-actor drawing; profile before changing asset or caching policy. Broader
rotations, arbitrary effects, ancestor tint/materials, other actor poses, long-run
memory, target PC/Mac and owner appearance acceptance remain production work.
