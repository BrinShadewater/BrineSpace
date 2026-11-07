# Project handoff

Updated: October 11, 2026 · BrineSpace · Task: original-pipeline native effect adapter

## Objective and acceptance

Reduce memory/upload bursts without changing selected pixels/quality, frame objects,
simulation or resource lifetime. Private until matched repeated timing/visual/input
acceptance. Full original performance and PC/Mac release plan remains open.

## Accepted decisions and constraints

Original Grid/render order retained. No palette Group/shader/collection look-ahead.
Mask allowed only nearest, white draw/inherited RGB, no material or existing Flood.
Other contexts originalRGBA. Original PNGs/data immutable; explicit whole paths.
No production renderer edits, package/publication or user save changes.

## Current state

`build-native-effect-adapter.py` generates private Motion/Texture2D descriptor/
catalog/resource map in `benchmark-input-isolation/native-effect-adapter/`.
Derived mask decoded on existing worker path; SHA/format/size/mipmap validation,
ordinary original fallback on invalid derived input. Descriptor keeps independent
identity, immutable mask and lazy original. Public image/RID APIs return original
art. Weak storage callback accounts fallback bytes without creating self-cycle;
upload callbacks record lazy original uploads. Original session-cache cleanup used.
No new permanent texture lookup or additional scene/material/command layers.

## Verification

Actual debug=false adapter oracle576 mixed-image pairs exact (frame60): normal,
Flood and custom shader; nearest/linear, draw/parent RGB, scale/mirror/alpha, three
sheets and ordinary surrounding geometry.144 mask/1584 fallback commands actually
execute. Original+mask byte accounting checks3pass. Reuses prior8640 exhaustive
nearest native representation checks; not every adapter frame/context retested.

Worker/identity/lazy accounting/lifetime oracle19checks pass: jobs finish, stable
descriptor identity, maskLA8, fallbackbytesaccounted, nine descriptor/mask/original
weak references disappear after explicit cache cleanup. Invalid derived SHA takes
originalRGBA. Initial fixture tried mutating read-only const catalog; corrected
negative case uses separate immutable fixture catalog, successful run no errors.
Missing derived file guarded before read; missing original explicitly returns error.
Missing-file branch not yet directly exercised. Actual scene-transition cleanup
and all additional flood states remain pending; explicit cleanup is narrower.

Current accepted source mixed pilot: two native release runs/2160frames, all12
full gameplay states/camera paths/labels exact, native loaded Motion source guard
passes. Existing default renderer, active natural Moonbay and powered Tidal fixture.

| Metric | Original | Native adapter |
| --- | ---: | ---: |
| Mean ms | 30.609 | 30.713 |
| p95 ms | 45.680 | 45.707 |
| p99 ms | 55.693 | 55.082 |
| Maximum ms | 100.773 | 84.270 |
| >50ms frames | 23 | 22 |
| >100ms frames | 1 | 0 |
| Peak engine texture MiB | 2928.086 | 2744.336 |
| End texture MiB | 1939.219 | 1939.219 |

Mean+0.34%, p95 essentially flat, p99/max improve, peak183.750MiB lower. One pair
does not prove repeatability or no timing regression. Delayed GPU query means
6.085→6.694ms, not aligned causal work. Every phase native source fields present;
mask counter reaches118, original fallback0. Successful logs no runtime/missing-art
errors. Owner2938unchanged; jobs terminal, override restored. Artifacts adjacent
`native-effect-adapter-pixels`, `native-effect-adapter-lifetime`,
`native-effect-adapter-pilot/{identity.json,comparison.json,*.json,*.log,owner.json}`.

## Next action

Three alternating matched pairs on mixed and original station workloads, with
loaded-source/input/state guards and bounded reports. Do not claim FPS gain from
this pilot. Complete additional flood/filter transitions, invalid/missing derived
resource fallback and real scene cleanup before any admission. Keep unchanged
palette/cache rejections separate; preserve full loading/stutter/endurance/bug/
target-hardware/Windows-Mac release gates. No goal completion yet.
