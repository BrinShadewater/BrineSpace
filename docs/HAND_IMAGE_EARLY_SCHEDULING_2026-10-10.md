# Project handoff

Updated: October 10, 2026 · BrineSpace · Task: early scheduling and saved surfaces

## Objective and acceptance

Continue the full PC/Mac performance/release plan. Remove the remaining same-frame
preview loading stall and prepare the artwork selected by saved layouts. Keep the
prototype private until rendered override, lifetime/churn and large-map checks pass.

## Accepted decisions and constraints

Normal source and frozen packages remain unchanged. Earlier private V1/V2 retained.
Use the same bounded V2 decoder, original complete synchronous fallback and
main-thread GPU uploads. Prepare before card UI rebuilding, not by delaying input,
reducing quality or showing incomplete rooms. Muted secondary-display native tests,
scratch profiles, owner guards, one reused physical QA runtime; no full copies.

## Current state

Private `hand-image-preparation-v3-source/` includes:

- Shared floor tile-source helper used by actual meshes and preparation path discovery;
  honors selected finish and per-tile materials, resolves source revisions for decoding.
- Shared painted-wall base selection used by actual context and preparation metadata;
  preserves borrowed room/riser source and custom integrated-art suppression.
- Grid preparation derives canonical editor asset/quarter before first layout apply,
  reads saved surfaces, caches at most64 metadata records keyed by layout revision,
  and filters uploads by the correct floor/wall cache key. No view reconfiguration.
- Private Main hook starts preparation before `_refresh_cards` rebuilds the UI.
  Existing startup-prefetch exclusion, two-task/16MiB reservation and cleanup retained.

Default floor/profile lookup and wall choice now cover tested galley overrides.
Corridor shape-specific preparation needs review: current grid discovery still passes
non-corridor geometry to the floor helper. Runtime rendering is unaffected and uses
the ordinary loader when preparation misses; do not claim all-room preparation yet.

## Verification

Actual debug=false Windows/1080p RTX4070Ti reported12 comparison33355, same-frame
card arrival/selection, direct connected placement and demolition at1x/2x/4x:
four runs/4,320 measured frames, twelve phase-end gameplay states equal.

| Metric | Forward reference / prepared | Reverse reference / prepared |
| --- | --- | --- |
| Same-frame arrival/selection/preview |119.568 /81.176ms|116.281 /77.536ms|
| Entire run maximum |119.568 /81.176ms|116.281 /77.536ms|
| Frames >100ms |1 /0|1 /0|
| Mean frame time |14.846 /14.802ms|14.732 /14.792ms|

Prepared lanes consume both images by the first preview; zero pending/reserved
afterward, zero decode failures, three submissions/one unused result overall.
Peak reservation12,575,504bytes (~11.99MiB). Same-frame improvement is measured;
overall means remain mixed and this does not establish60FPS or all release gates.

Headless source-selection fixture26checks/0failures: four rotations, mixed tile
materials, saved finish, borrowed/self/missing wall IDs, canonical saved asset lookup
before first apply, and layout revision invalidation back to the default. Uses
scratch in-memory layouts without saving them. Test-only explicit module bindings
separate these helpers from cached baseline scripts. Initial standalone grid copy
failed duplicate global `GridCanvas` registration; owned headless process209408
stopped and test-only class declaration removed. Corrected fixture passes; failure
logs/owner guards retained. This is source/lifecycle selection coverage, not rendered
wall composition or navigation correctness for all layout options.

Every successful comparison has clean engine/art/input/profile/window guards;
every full owner fingerprint2,938 unchanged. Jobs33355/19267 terminal (first helper
failure retained), corrected helper terminal0. Runtime configuration/fixture restored;
no native processes remain. No production admission, package/export/commit/upload.

Evidence under `D:/bs-release-crew-cache-20261009/benchmark-input-isolation/`:
`hand-image-early-performance/paired-analysis.json`, full traces/logs and owner guard;
`hand-image-surface-sources-v2/` corrected26check log/guard; private V3 source and
`hand-image-early-runtime-pack/`. Drivers/tests in
`output/renderdoc-tools-2026-10-08/`.

## Next action

Validate rendered default/overridden floor and wall composition against current
normal source, fix corridor preparation shape discovery, test selection/rotation/
layout changes while tasks are pending and final-owner integration, then compare
the complete workload on40-room maps. Keep cold direct-placement stress and current
admission limits explicit. Continue separate drone-upload remedies and full original
bug/endurance, target-PC/Mac, frame/stall/memory, packaging/signing/notarization gates.
No itch publication.
