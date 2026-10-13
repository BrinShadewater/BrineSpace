# Project handoff

Updated: October 6, 2026 · BrineSpace · Lossless private frame-storage experiment

## Objective and acceptance
Resolve the eager private bank's RAM penalty while preserving selected art, frame
identity/metadata, filtering, timing, ownership and actual gameplay. Default runtime
admission and the full PC/Mac release gates remain separate.

## Accepted decisions and constraints
Prototype only in output/compressed-veld-2026-10-06/. No normal source/art/UID,
engine, renderer or settings changed. Original images remain untouched. Sources
store losslessly compressed raw pixels plus exact dimensions/format/mipmap headers;
each decode creates an independent Image. Only bounded private GPU presentation
slots/spills retain draw storage; frame objects and their metadata stay distinct.
Reference and candidate loader bodies come from current normal Grid selection,
restricted to Veld for standalone testing. Selection/hash evidence retained.

## Current state
Experimental frame/batch/player/bank/slots and per-canvas router/display/flood
adapters implemented. Current Main/Grid physical copies support a Veld-only
experimental flag and normal reference. No maintained feature flag/default
enablement, release export, commit or upload. Sources/results/hashes all in the
named output directory; comparison.json aggregates matched measurements.

## Verification
Native source/render test: 14,450 checks, zero failures; all source dimensions/
bytes and consumer-edit isolation checked, 4,788 exact image pairs plus 33 overflow
comparisons across tested scales/half-pixel positioning/clipping/filtering. Held
canvases preserve leases; exiting owners release presentation storage.

Native consumer test: 48,847 checks, zero failures; 390 clips, 3,186 logical frame
references, metadata/timing/filter/source API checks, 24 reading interruptions,
1,080 replay steps across FPS/speed/pause/restore coverage from the inherited fixture.
Raw equivalent 383,095,296 bytes stored as 28,583,336 compressed bytes; no generated
GPU readbacks in this selected bank.

Three native standalone pairs: texture savings 486.50 MiB, median peak Windows
working-set saving 336.54 MiB. Preparation 2.49–2.58 s reference versus 3.06–3.08 s
candidate. Candidate frame p99 2.007/0.986/1.069 ms versus 0.704/0.632/0.932 ms;
no >50 ms frames. This is not station performance acceptance.

Three actual native 1080p 40-room pairs: texture 3,903.21→3,417.53 MiB in every pair
(485.67 MiB less). Compared crew/world/drone states match in all 15 phases per pair;
one active selected Veld, active drones/production. Zero missing private routes,
148 distinct source frames, four slots/four live spills; no runtime art failures.
Windows peak working-set candidate-minus-reference +38.29/+77.10/−26.83 MiB;
private-commit savings 446.29/379.32/540.72 MiB. Do not sum process counters with
engine texture counters or infer M1 physical memory. Median working set is still
~38 MiB higher, but the earlier eager-bank ~300–365 MiB penalty is mostly avoided.
Overall means remain ~34 ms, candidate slightly slower in these pairs; no FPS gain.
The 3 GiB large-scene texture gate still fails by ~346 MiB.

Native two-cycle New Game/dialogue/Studio/save/title/Continue probe: zero behavioral
failures; old player/router/cache owners release. Candidate and current reference
both settle at title 171.08→174.55 MiB; this is not the ten-transition/2-hour gate.
Both produce the same single anonymous RefCounted reference-count-zero exit warning,
also recorded in the earlier eager prototype. Thus it is not introduced by this
codec, but its cause remains open. No unexplained warning is waived for release.
All completed probes preserve 2,936 owner non-log files.

Related primary engine reports describe similar warnings with different triggers:
[sub-threaded LoadToken issue](https://github.com/godotengine/godot/issues/120661),
[inherited C# resource issue](https://github.com/godotengine/godot/issues/122001).
This project uses GDScript and load_threaded_request's default sub-thread flag;
those reports do not establish the cause here or justify an engine upgrade.

## Next action
Extend isolated storage/presentation coverage to the other replacement crew banks,
preserving James's specialized player/bridges and all historical bindings. Start
with current declarations, not archived loader snapshots; keep Bill separate until
its historical-save identity requirements are tested. Require native byte/render/
consumer checks and matched station memory before any normal admission. Complete
ten-transition ownership checks and identify the shared exit warning independently.
Large rover atlas transfers, sustained frame budget, full roster, original report
closure, endurance, packaged Windows and native Mac certification remain open.
