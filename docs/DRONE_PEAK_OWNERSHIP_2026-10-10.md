# Project handoff — concurrent drone texture ownership

Updated: October 10, 2026 · BrineSpace · PC/Mac performance readiness

## Objective and acceptance
Find actual concurrent memory contributors and improve frame pacing without changing
selected pixels, clocks, layering, quality or gameplay. Full release gates stay open.
Previous turn made progress through matched real-map evidence: identical-sheet sharing
was rejected for no peak reduction or average benefit, rather than installed on theory.

## Accepted decisions and constraints
Native Windows debug=false reused runtime, RTX 4070 Ti/1080p, muted secondary display.
Isolated resolved APPDATA, owner fingerprint guards, 20 GiB free-space refusal threshold.
Only small overlays and bounded evidence. No full build copies or art changes.

## Current state
Installed additive read-only accounting in scripts/drone_animation.gd.cache_diagnostics:
observed unique live decoded bytes/images, uncached live decoded bytes, bounded metadata
for 64 images and completeness fields for a maximum 4,096 weak lookup entries. F8/stall
reports already call this method; no per-frame collection. No image readback, eviction,
recency changes, strong resource retention or new long-lived cache. Decode-byte accounting
is explicitly not a complete GPU-residency inventory. Existing fields retained.
Extended tests/test_drone_upload_diagnostics.gd; UID pairing preserved.

## Verification
One private saved40 ownership probe: 3,027.507 MiB engine texture peak at 2x idle
index81. All 1,344 game-tree nodes scanned, complete canvas-pin lookup. Live unique
drone storage 1,149.751 MiB; ordinary cache owns all but 36 bytes. About 459.375 MiB
has last-use age3 and no canvas pins: North mining body/effects (137.813 MiB each),
South collection body/cargo (91.875 MiB each). East/South mining body/effects,
three wheel sheets and small dock/cargo images remain pinned/recent. Four decode jobs
pending (South/North start, North collection body/cargo). Ownership snapshot uses
metadata only and is outside timed samples; engine release counters may lag.
This identifies contributors, not proof that every unpinned byte can disappear at
that engine sample or that active atlas bytes are unnecessary.

Private pre-upload trim candidate invokes existing trim_stale before cache_image
allocation, preserving two-frame age protection/budget/pins. One actual saved40 pair,
810 frames per lane: reference mean27.563/p9543.910/p9952.258/max116.828 ms; candidate
27.429/44.149/50.309/96.113 ms, >50 frames12 to10. Both peak3,027.507 MiB unchanged.
A single small mean/tail difference is not a demonstrated optimization. Candidate
remains private, not installed; snapshot staleness did not imply achievable peak headroom.

Installed report accounting native V2: 21 checks, zero failures. Exact live totals,
externally held image after cache eviction, weak restoration, bounded metadata and all
existing upload history/identity/recency behavior pass. Initial wrapper mixed tabs into
the existing space-indented test: parse failure, exact owned process stopped, config
restored. Corrected wrapper normalizes indentation only; production test unchanged by
that repair. Focused diff check clean. Runtime source change is reporting only, not FPS.

Evidence: D:/bs-release-crew-cache-20261009/benchmark-input-isolation/
drone-peak-ownership, drone-preupload-trim-preliminary, drone-live-ownership-native-v2.
Four owner guards: 2,938 files unchanged. All jobs terminal, override restored.
27.60 MiB evidence+scratch, no full PCK copies; C:126.92/D:78.60 GiB free.

## Next action
Review the already pixel-verified twenty-source lossless indexed candidate against
CURRENT accepted RGBA runtime, rather than its old sixteen-source indexed control.
The current peak includes its measured North/East mining hotspots. Prior tests show
mixed FPS and no source admission; do not claim it accepted. Preserve whole atlas
coordinates/effective filtering and keep fallback/lifecycle explicit. A fresh matched
real-map comparison must show useful memory headroom without mean/tail regression before
using that headroom for bounded early preparation. Also continue redraw-burst attribution.
See INDEXED_DRONE_HOTSPOTS_2026-10-09.md and focused indexed-hotspot runners; do not repeat
cropped/row/grace/sharing experiments unchanged. All performance, endurance, original
bug, frozen PC/Mac package and native M1/signing/notarization gates remain open.
