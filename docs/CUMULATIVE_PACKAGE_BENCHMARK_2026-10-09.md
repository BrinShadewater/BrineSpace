# Project handoff

Updated: October 9, 2026 · Project: BrineSpace · Task: accepted-source packaged baseline

## Objective and acceptance

Measure complete accepted source before admitting further performance changes.
Release remains blocked by performance and memory gates. This is an RTX 4070 Ti
Windows measurement, not GTX 1650/M1 certification or a matched improvement claim.

## Accepted decisions and constraints

Keep original visual quality, animation timing, historical bindings, layouts and
saves. No publishing or quality reduction. Preserve both candidate and rollback.
Treat engine texture accounting separately from physical VRAM and within-frame
peaks; nested profiler stages cannot be added into a whole-frame cost.

## Current state

Build `brinespace-60b400041c69f41a`, physical source and delivery identities in
`D:/bs-release-20261009/`. Windows export/PCK audit/normal-entry smoke passed.
Universal 2 Mac export/bundle audit passed with identical 36,245 selected source
hashes and a byte-identical PCK; native Mac/signing/notarization are unverified.

Full Windows benchmark session 35863 is terminal, exit 0. Fresh/original reported
12-room/deterministic 40-room fixtures, 1080p/1440p, three repeats each, all eight
actions at 1x/2x/4x. Each phase has 180 measured uncapped frames. Current Node
simulation driver, bounded trace, actual debug=false and visible-window guards.
Data/logs: `benchmark/`; verified aggregation: `benchmark-results.json`.

## Verification

18/18 runs complete, zero logged errors, 77,760 measured frames. Owner fingerprint
2,936 files unchanged. 177/432 phases meet p95 <=16.7 ms, p99 <=25 ms and max <=100
ms. There are 1,512 measured frames >50 ms and 48 >100 ms; investigate these before
closure. Exact worst frame 193.314 ms. No claim of stall-free gameplay.

Idle values below are medians of the three per-run 1x values. Passing counts cover
all actions/speeds and all three runs. Texture maxima are sampled phase endpoints,
not guaranteed instantaneous peaks.

| Scene | Resolution | Idle mean / p95 ms | Passing phases | Max frame ms | Max sampled textures GiB |
| --- | --- | ---: | ---: | ---: | ---: |
| Fresh | 1080p | 9.59 / 10.81 | 65/72 | 101.32 | 3.05 |
| Fresh | 1440p | 9.00 / 10.21 | 71/72 | 95.10 | 3.07 |
| Original 12-room | 1080p | 14.50 / 16.07 | 27/72 | 72.54 | 3.51 |
| Original 12-room | 1440p | 15.58 / 17.91 | 14/72 | 73.67 | 3.54 |
| Deterministic 40-room | 1080p | 28.67 / 35.92 | 0/72 | 183.24 | 4.72 |
| Deterministic 40-room | 1440p | 29.15 / 34.83 | 0/72 | 193.31 | 4.73 |

First application/profile request-to-ready 11.286–13.279 seconds, OS disk cache
uncontrolled. Warm fresh 4.352–4.981 seconds; reported 5.679–6.241; large
5.901–6.235. Normal intro/dialogue loading and controlled cold-disk certification
remain separate. One automatic report per run; do not silently remove its scope.

Original 12-room textures exceed the 2 GiB budget; large exceeds 3 GiB. First fresh
warmup already retains ~3.02 GiB with one room/no active actors at that sample.
Pool startup uploads 1,610,154,592 decoded-equivalent bytes in 8,188 uploads;
traffic is not complete surviving allocation attribution. Existing private
lossless four-crew storage previously reduced this footprint substantially, but
has not been admitted or validated against this complete current candidate.

Pre-admission compatibility issue reproduced: exact Bill script equality in
`_sync_bill_bound_sources` skips subclasses, leaving bare idle/walk cache stale.
CPU reproduction 26 checks/16 failures across two inheritance depths/four bindings;
original class and unrelated-player guard pass. Private inheritance-chain fix
26/0, original frozen source unchanged, owner 2,936 same. Fixture setup failures
(doubled CRLF, duplicate global class on the diagnostic copy) retained separately;
corrected LF serialization and removed class declaration only in that test copy.
No normal-source admission, actual saved-game/motion/pixel acceptance from this
CPU check. Evidence: `bill-subclass-sync/{red,green}-result.json` and logs.

## Next action

Prepare the existing lossless storage provider plus verified private lease fix on
this exact frozen source, including the Bill inheritance guard. Compare full
normal control versus all-crew candidate with identical inputs and both orders;
verify source execution, memory/lifetime, frame timing, all four bindings, actual
bare/helmet idle/walk after restore, native pixels and scene cleanup before normal
admission. Preserve independent generated images and immutable source pixels.

Then target remaining command rebuilding/rendering and repeated placement,
demolition, lighting/zoom stalls using aligned current-frame attribution.
Investigate the 1,320 packaged world-review files / ~777 MiB dependency lead;
do not delete archives or infer runtime residency from pack size. Complete older
package comparison, original nine reports, save/relaunch/menu/UI coverage, two-hour
soak/ten transitions, target hardware, native Mac and distribution certification.
