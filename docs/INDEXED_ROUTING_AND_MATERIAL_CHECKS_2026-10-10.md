# Project handoff — routed props and material state

Updated: October 10, 2026 · BrineSpace · PC/Mac performance readiness

## Objective and acceptance
Verify narrowed provider routing and test the hypothesis that material reset/rebinding
contributes to its remaining overhead. Previous turn completed normal-game comparison:
private memory benefit but slower mean, no admission. This turn closes routing visual
coverage and rejects an unsuccessful material optimization; full goal unchanged.

## Accepted decisions and constraints
Native debug=false Windows/RTX4070Ti/1080p, muted secondary display, resolved scratch
APPDATA/owner guards,20GiB refusal threshold. No normal source/art/package installation,
full release copies, asset deletion or automatic quality changes.

## Current state
Targeted routing remains PRIVATE: non-props go directly to normal paint; only mining
docks use the provider (all twenty encoded paths are mining artwork). Old indexed
children release/hide when slots route back. No changed selected-pixel generator.
Private conditional-material trial avoids reset-to-null before a palette draw and tracks
palette texture identity to skip redundant sampler binding; shader changes invalidate
identity, ordinary/fallback paths explicitly inherit normal material. It passes sampled
visual checks but is NOT retained for further candidates because measured means worsen.
Targeted resources.json still references prior batched group, not material trial.

## Verification
Actual construction/salvage dock routing versus prior private provider:244checks,
zero failures,48exact actual-art pairs. Docked/launching, three scales(.613/1/1.6),
mirrored/unmirrored, nearest/linear, actual production PNG/component preparation.
All cases require visible output. Same slots reused for non-prop actor rendering:
exact output, stale indexed child hidden and all batched command references cleared.
Renderer fixture supplies normal context; library's actual normal drone draw path used.
Not all room composition/motion/flood/hidden-legacy or Mac certification.

Conditional-material native check:180checks/zero failures,36mixed-command base image
pairs plus72same-slot nearest/linear fallback-switch comparisons. Existing tint/mirror/
scale/normal-flood-unsupported material contexts retain exact pixels; command cleanup
passes. This does not prove all palette-source or parent-material transitions.

One matched PRIVATE targeted-provider versus conditional-material pair per12/40 map,
idle/pan/zoom/lighting1x/2x/4x,4,320frames:
| Map/lane | Mean ms | p95 ms | p99 ms | Max ms | Peak MiB |
|---|---:|---:|---:|---:|---:|
| Saved12 existing |12.821|19.624|23.543|25.679|1528.343|
| Saved12 material trial |12.984|19.297|23.247|26.902|1528.343|
| Expanded40 existing |26.048|42.396|53.155|81.326|2629.355|
| Expanded40 material trial |26.287|43.346|54.053|83.455|2629.355|

Both means slower(~1.27%/0.92%), large tails worse, no memory gain. Reject trial
rather than broaden repeats on this evidence. All24full gameplay snapshots/camera
start-end snapshots exact. No normal-game FPS claim; release gates still fail.

All jobs terminal/override restored, three owner guards2,938 files unchanged.
200.79MiB evidence+scratch/no full PCK copies, C126.90/D77.69GiB free. Evidence under
D:/bs-release-crew-cache-20261009/benchmark-input-isolation/indexed-targeted-dispatch-native,
indexed-stable-material-native and indexed-stable-material-preliminary; comparison.json/
storage-summary.json in latter, test sources/logs retained in corresponding trial folders.

## Next action
Repeat NORMAL-versus-targeted batched/prewarm provider12/40 with corrected framing,
explicit zoom, three pairs. The earlier targeted one-pair averages improved while tails
regressed; routed pixels now checked but performance admission remains unproven. Do not
include failed conditional-material code. If no repeatable benefit, keep provider private
and move to larger renderer/redraw hotspots rather than incremental speculative binding
changes. Whole-scene art/motion/fallback/lifecycle/loader checks, hardware/endurance,
original bug register and PC/Mac release/nativeM1/signing/notarization gates remain open.
