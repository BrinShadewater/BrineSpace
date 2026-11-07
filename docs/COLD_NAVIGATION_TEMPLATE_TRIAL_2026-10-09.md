# Project handoff

Updated: October 9, 2026 · Project: BrineSpace · Task: cold navigation template parity

## Objective and acceptance

Reduce the measured cold-template contribution to the remaining frame1256 stall
(6 misses /53.418ms on Veld). Full PC/Mac release-performance scope remains open.
Exact geometry, ordered graph semantics, fire/door policy and mission timing must
remain unchanged. Native parity alone does not certify packaged performance.

## Accepted decisions and constraints

Cold-template shortcut is retained in normal scripts/bill_npc.gd after repeated
targeted gains and normal regressions. Its UID is unchanged. Other shared private
render/storage/drone/water controls remain private; full release certification open.
Only cold authored-cell template generation can reuse precomputed world blockers:
grow0.05, clip to owning cell, retain exact segment_hits_rect sweeps. Both endpoints
are already proven by can_stand and the authored floor/closed-socket half-planes are
convex. Corridors, legacy geometry, sample-all mode and non-build fire checks keep
segment_clear. No replacement of route smoothing or boundary/door validation.

## Current state

Artifacts: D:/BrineSpace-performance/2026-10-08/moon-navigation-owner/cold-template-parity/.
Private candidate SHA8428196fe4fd9bd2ce78b97762ff01adf4122738297df60b5f3e9646d544d1e9.
Normal baseline SHAaa6342f6ad526e4940279aacf2d870e0275b7dcc1be1abb44764c5f707e5a1dc.
Reference switch: --reference-nav-template-generation (now also normal source).
Helpers: output/renderdoc-tools-2026-10-08/test-cold-template-parity.py and
prepare-cold-template-candidate.py. Prepared fixture and isolated runners retained.

## Verification

- Actual current room geometry, available rotations, four socket states, large-room
  component cells and copied owner Studio layouts:1468 cases,2936 exact ordered
  point/link checks,0 failures.1418 cases select fast path including10 edge cases.
  Synthetic cases cover half-open edges,padding,negative cells,clipped props,
  degenerate rectangles,sampling fallback and live fire fallback.
- Same coverage using the candidate's actual sweep helper:2936 checks,0 failures.
  Headless aggregate reference25.888s/candidate10.199s,reference always first.
  This is diagnostic accumulated template time, NOT matched gameplay speedup.
- Actual candidate cold/warm rebuild branches on a multi-room fixture containing
  moonbay,reactor,corridor,salvage workshop:11986 checks,0 failures. Exact global
  lookup,room node order,positions,weights,ordered adjacency and cached templates.
  No animation/render acceptance claimed; this changes geometry work only.
- Every invocation resolves a scratch user-data directory before writes. All2936
  owner files unchanged. Successful runs have no engine/script warnings/errors.
  Initial candidate fixture replacement also rewrote its helper declaration and
  caused a parse error; corrected narrowly before accepted runs. No gameplay fix
  was made to satisfy a test. Processes terminal; normal source hash rechecked.

## Packaged comparison and normal integration

Actual debug=false executable,1080p,40-room fixture,1000 idle samples per1x/2x/4x,
same cached point/link paths in both lanes. Bounded frame1256 probe and branch
metadata only; compiled actor source SHA
c89d6df4273e08ce74803e960d25ebc40dc8cf8d1cd0186912108bde15d0ea49 verified.
Shared private controls limit scope; this is not a full current-checkout export.

| Run order | Six cold templates ref ->candidate | Veld rebuild | Frame1256 crew | Frame1256 total |
|---|---|---|---|---|
| Reference first |55.213 ->15.880ms|92.684 ->50.545ms|162.222 ->119.640ms|197.448 ->156.106ms|
| Candidate first |53.733 ->15.986ms|89.881 ->51.996ms|158.346 ->121.120ms|200.482 ->164.295ms|

Exactly6 template misses/76cells/19695nodes retained; candidate selects fast path
for all6. Other two actors have no misses but still rebuild their full graphs.
No drone uploads occur on frame1256. Gains repeat; no mission timing deferral.

| Order /speed | Mean ms ref ->candidate | p95 ms | p99 ms | Max ms |
|---|---|---|---|---|
| Ref first1x |38.412 ->38.294|45.032 ->44.986|55.117 ->54.708|88.055 ->95.630|
| Ref first2x |39.563 ->38.837|47.590 ->47.176|62.860 ->57.272|197.448 ->156.106|
| Ref first4x |40.205 ->38.660|54.072 ->51.030|75.611 ->72.483|177.651 ->141.578|
| Cand first1x |35.652 ->35.693|38.046 ->39.158|48.298 ->48.727|73.806 ->77.082|
| Cand first2x |36.408 ->36.605|42.480 ->42.948|51.475 ->55.777|200.482 ->164.295|
| Cand first4x |37.587 ->37.379|49.252 ->49.195|68.827 ->70.040|162.419 ->132.593|

Broader means/tails remain mixed. Both candidates still fail frame/stall gates.
All phase crew/drone/mission endpoints and final mission histories/resources match.
Per-source drone upload counts equal,crew uploads4074each,texturepeak2345.481MiB/
exit228.259MiB equal,pending requests0at exit/routerreleased. Both owners2936same,
logsclean/processes terminal/adapters restored. Art changes were not introduced.

Normal post-integration SHA
93e31c06036b2d3d1ec31a7686c1db0cfa6156c5b87ce0c6050368cb82f02e11.
Normal actual cold/warm default-layout graph13306checks/0 (private copied-layout
fixture11986/0),owner90/0 in normal and reference-template modes,segmentclearance
PASS,stagger0failures. Normalvalidation-owner2936unchanged/logsclean/terminal.
Only current cold-template edit captured in normal-template.diff; no UID changes.

Artifacts cold-template-runtime/,cold-template-reverse/,cold-template-summary.json,
cold-template-parity/normal-validation.json and normal-integration.json.
Helpers prepare-cold-template-runtime.py,prepare-cold-template-reverse.py,
integrate-cold-template.py,validate-normal-cold-template.py,analyze-cold-template.py
under output/renderdoc-tools-2026-10-08/.

## Next action

Reduce repeated full graph reconstruction with strict topology/geometry/policy
invalidation and independent actor graph ownership. Candidate frame1256 still spends
about116ms across three full rebuilds; local links/boundaries cost~12ms each per
actor. Any graph retention or changed-cell updates need separate semantic/lifetime
proof and matched measurements; no mission-exit deferral. Full-source package,
broad workloads,original bugs,loading/memory/endurance and Windows/Mac gates open.
