# Project handoff

Updated: October 10, 2026 · BrineSpace · Task: bounded CPU hand-image preparation

## Objective and acceptance

Continue the complete PC/Mac performance/release plan. Prepare required floor/wall
PNG pixels before first preview without shifting a hitch to card arrival, changing
artwork or showing incomplete rooms. This prototype is private, not yet admitted.

## Accepted decisions and constraints

Keep all existing accepted normal changes. Prototype only adds CPU decoding:
ordinary main-thread texture creation and rendering remain unchanged. Maximum two
tasks and16MiB decoded-image reservation. Completed unused jobs are dropped when
the hand changes; scene-end clear joins remaining tasks and releases lookup/results.
Incomplete/absent preparation uses the existing synchronous loader. Startup
prefetch excludes this queue. No worker creates GPU resources or modifies shared
images. Muted secondary-display tests, scratch profiles, owner guards and shared
physical QA runtime; no full package copies.

## Current state

Private `hand-image-preparation-source/` contains queue, instrumented grid,
floor/wall consumer integrations and final-owner cleanup. New view prewarming
records default floor/wall paths; each frame prioritizes hand/selected card requests
and skips already uploaded sources. Native selection probe fixes its preview cell
without moving the physical pointer. Sources under:
`D:/bs-release-crew-cache-20261009/benchmark-input-isolation/`.
Drivers/tests under `output/renderdoc-tools-2026-10-08/`.

The implementation currently prepares default profile/base paths. Borrowed wall
and alternate floor choices need explicit coverage; missed preparation still uses
the original renderer. Existing station views already marked prewarmed may have
no hand-path entry, so preparation eligibility needs review. Header reservation
currently assumes up to4bytes/pixel; strengthen supported bit-depth/dimension
validation before admission. No normal source, new UID or release package changed.

## Verification

First matched selection trial4223, actual debug=false reported12/owner layouts,
four runs/4,320samples. First preview85.483->45.576ms forward and84.811->46.410ms
reverse; twelve phase-end states equal. However, initial hand preparation occurred
during warm-up. Means mixed14.854->14.709 /14.751->14.753ms. Retain scope limitation.

Second matched trial69197 measures card arrival at frame0, selection/preview at20,
direct connected placement at30. Four actual debug=false Windows/1080p RTX4070Ti
runs/4,320samples at1x/2x/4x; twelve phase-end states equal.

| First1x event | Forward reference / prepared | Reverse reference / prepared |
| --- | --- | --- |
| Card arrival |46.688 /45.775ms|47.090 /47.076ms|
| Selection/preview |85.451 /46.137ms|85.850 /46.755ms|
| Placement |57.639 /60.767ms|61.731 /59.577ms|
| Entire run mean |14.771 /14.656ms|14.740 /14.642ms|
| Entire run maximum |85.451 /64.328ms|85.850 /65.696ms|

Five >50ms frames remain each run. This is a preview-loading gain, not60FPS/stall
certification or improved navigation/redraw cost. Two prepared images consumed,
zero pending/reserved after preview; three submissions/one unused result in the
complete sequence. Peak reservation12,575,504bytes (~11.99MiB). It bounds decoded
storage estimates, not total process memory including temporary PNG buffers.

Private queue unit fixture11checks/0failures: two-job/reservation limits, exact
decoded bytes/size/format/mipmap state, consumed lookup release, unused-job pruning,
pending-work scene-end clear, absent fallback and disabled reference behavior.
Native prepared/original GPU image readbacks and16 sampling pairs byte-exact,
covering both source images, nearest/linear filtering, fractional scale/position
and oversampling1/2. This is texture/component coverage, not every moving-room
composition or Mac renderer acceptance.

Every successful run has clean engine/art/input/profile/window guards; every full
owner fingerprint2,938 unchanged. Native jobs terminal, runtime configurations and
fixtures restored. Evidence: `hand-image-preparation-performance/paired-analysis.json`,
`hand-image-arrival-performance/paired-analysis.json`, `hand-image-queue-unit/`,
`hand-image-prepared-pixels/results.json`; source and small overlays retained.
No additional multi-GiB source/PCK copies or unbounded captures.

## Next action

Harden header/budget validation; test immediate and rapid selections, cancellations,
alternate saved floor/wall choices, final-owner cleanup and the40-room station.
Measure the complete arrival/preview/placement workload including preparation costs,
waste and peak memory. Admit only after those checks; keep cold direct-placement
stress and all original release gates. Large-map visible drone uploads remain a
separate priority. Continue bug/UI/input/endurance, target-PC/Mac and packaging/
signing/notarization work. No itch publication.
