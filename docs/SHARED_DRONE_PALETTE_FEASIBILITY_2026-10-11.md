# Project handoff

Updated: October 11, 2026 · BrineSpace · Task: different indexed-draw batching approach

## Objective and acceptance

Reduce drone upload pressure without losing pixels or degrading frame pacing.
New storage/rendering experiments remain private until native visual, fallback,
lifetime and matched real-map timing acceptance. Full release goal stays active.

## Accepted decisions and constraints

Preserve installed circle geometry and all accepted production work. Do not rerun
rejected descriptor leases, conditional material retention, global cache increases
or UV paging unchanged. No art deletion, downscaling, frame removal or engine upgrade.
Tests muted, secondary display, isolated profiles, bounded generated evidence.

## Current state

Reconciled newer evidence: `LATEST_INDEXED_PERFORMANCE_AND_LEASE_TRIAL_2026-10-11.md`
confirms hardened 21-source provider saves about 399 MiB, but all nine mean-frame
pairs worsen. Loader/filter/lifetime checks have already progressed beyond the
older COMPLETE_STATE handoff; reuse those records, do not retest old defects as
new discoveries. Descriptor lease and conditional material retention stay excluded.

New approach shares one combined palette/material and sends palette selection
with each rectangle command. Unlike prior per-slot uniform retention, this aims
to remove slot/material switches while retaining the original ordered draw stream.
Encoded rectangles carry a reserved vertex-color marker; vertex code recovers the
palette index and original white RGB/alpha. Ordinary commands use the ordinary
texture/tint branch. No atlas UV/dimension remapping.

Private artifacts under
`D:/bs-release-crew-cache-20261009/benchmark-input-isolation/`:
`native-texture-format-inventory`, `palette-command-carrier`,
`shared-drone-palette`, `shared-palette-pixels`.
Builders/probes in `output/renderdoc-tools-2026-10-08/`:
`check-palette-command-carrier.py`, `build-shared-drone-palette.py`,
`check-shared-palette-pixels.py`. Production source unchanged this pass.

## Verification

Pixel inventory examines every pixel, including transparent RGB, of the twelve
most costly paths from the existing upload ranking. None is fully grayscale or
fully opaque. Native L/LA grayscale and RGB opaque shortcuts therefore do not
apply to these sheets. No texture-format conversion trial or art changes made.

Actual debug=false Windows/Compatibility/RTX4070Ti command-marker oracle:
48 byte-exact image pairs, zero failures. Tagged white-RGB commands and ordinary
white/colored commands, nearest/linear filters, opacity and inherited alpha.
Ordinary background drawing also shares the shader. This does not validate
tagging under inherited RGB tint; that context requires original-art fallback.

Merged palette: all 21 written PNG segments byte-identical to the existing
source palettes; 256×1181 RGBA8, 1,209,344 decoded bytes, PNG236,189 bytes.
Recorded source identities retained. No large atlas files copied or regenerated.
Initial catalog parser rejected GDScript's trailing comma; corrected parser uses
an explicit enum substitution/trailing-comma removal. That preparation failure
was not visual evidence.

Actual debug=false native shared-material oracle: 72 whole mixed-image comparisons,
zero differing bytes. Three real sheets rendered in sequence under ONE material:
RG8 west body, R8 west effects, RG8 steer-right-west, using palette IDs0/1/20.
Frames0/7/59, three scales, mirrors, opacity and inherited alpha. Ordinary opaque
background and a following translucent line preserve mixed-command ordering.
Nearest indexed sampling only. No screenshots saved. Shader compiled and normal
logs have no engine errors. No performance gain measured or claimed.

The [CanvasItem shader documentation](https://docs.godotengine.org/en/stable/tutorials/shaders/shader_reference/canvas_item_shader.html)
describes inherited modulation in COLOR. The [matching 4.7.2 Compatibility renderer](https://raw.githubusercontent.com/godotengine/godot/4.7.2-stable/drivers/gles3/rasterizer_canvas_gles3.cpp)
uses float color attributes for polygon vertices; the native rectangle-marker
oracle establishes the required behavior for the tested draw path. These sources
guide the experiment; they do not certify another backend or Mac.

Both native owner fingerprints unchanged: 2,938 files. Jobs terminal, runtime
override restored. Accepted Grid hash remains
`03a46860e3eb626f31c31e165dc5b5e0ff4c3f4475b612646e306eae9f7b6072`.
Generated images total one small shared palette; no runtime copies/screenshot batches.

## Next action

Additional October 11 shader acceptance: `check-shared-palette-flood.py` combines
the existing flood arithmetic with shared-palette decoding. Actual debug=false
native oracle: 288 whole-image comparisons exact across four waterline/depth/clock
states. Extended run: 1,440 comparisons exact across those states and five ordered
contexts (nearest white, draw RGB tint, inherited RGB tint, linear, nearest white
again). Tinted/linear contexts explicitly select original RGBA textures in the
oracle; this proves that shader branch and the proposed fallback selection rule,
not a completed command backend or its inheritance tracking. Mixed background,
three real sheets and following line remain in one ordered draw stream.
Zero engine errors; owner fingerprint 2,938 unchanged, runtime override restored,
jobs terminal. C134.28/D68.32 GiB free. No screenshots or runtime/art copies.
Artifacts: `shared-palette-flood/{probe.gd,native.log,owner.json}` and small
`shared-drone-palette/shared-flood.gdshader`. Production remains unchanged.

Build a private single-canvas command backend using the hardened provider inputs
and shared palette. Preserve required loading, filtering/material inheritance,
ordinary shapes, original-image fallback and command texture ownership. Tag only
supported white inherited RGB/white indexed draw RGB; use original textures in
other contexts. Verify flood/tint/filter changes and resource teardown before
matched real-station timing. Do not infer a win from reduced material count alone.
Retain full FPS, loading, memory, endurance, original bugs and PC/Mac release gates.

### Private command backend acceptance

`build-shared-command-backend.py` now writes private `shared-command-backend/`
`group.gd` and its local-load oracle version. It retains one ordered child canvas,
one shared material, direct command texture references, ordinary command APIs and
original-texture fallback. It checks effective material/filter and inherited RGB
before tagging; flood parameters are copied at each update. Final redraw is queued
once per update. No production source changed.

`check-shared-command-backend.py` exercises this actual Group, rather than the
earlier oracle's manual selection: 1,440 full-image comparisons byte-exact, zero
engine errors. Uses three real sheets and mixed ordinary background/following line,
four flood states, scales/mirrors/opacity, ancestor modulation, draw tint and
nearest→linear→nearest context sequence. Counters show 1,728 indexed commands and
2,592 original-texture fallback commands. One child canvas asserted; explicit
release clears its commands/material and the Group's palette/material/lookup.
This is command cleanup acceptance, not full session/worker teardown acceptance.
Owner 2,938 files unchanged; native process terminal and override restored.

Next: connect the hardened Bank/Session to the shared palette without retaining
per-source palette GPU copies, preserving validated input and memory accounting;
test complete teardown and unsupported material behavior, then integrate current
accepted source for matched real maps. No FPS measurement or admission yet.

### Shared Bank and Session connected privately

`build-shared-palette-bank.py` now produces a hardened shared Bank, resource map
and Group integration in `shared-command-backend/`. It validates the shared PNG's
decoded dimensions/format/mipmaps and SHA256, then checks each original palette
segment byte-for-byte before admitting its indexed descriptor. One shared GPU
palette; descriptors retain their own index textures, no per-source GPU palette.
Index bytes stay in descriptor accounting; shared bytes are reported once by Bank
as 1,209,344. Session owns Bank and existing worker/cache shutdown remains intact.
The shared decoded CPU image remains bounded to that same size for validation.

Native debug=false `check-shared-palette-bank.py`: 95 checks, zero failures across
all 21 sources. Shape/segment validation admits all; cache identity preserved,
descriptor palettes absent, byte accounting exact. Command ownership retains
shared palette/index until release; weak-reference checks confirm both disappear
after release. Malformed supplied index still uses the hardened original fallback.
Actual Session with two owners: first detach stays open; last detach closes,
waits a submitted worker, clears cache bookkeeping/factory/active canvas and
releases palette; repeated close stays safe. No engine errors.

Initial lifetime fixture failed twice, and diagnostic printing changed the result.
Final fixture obtains weak-reference identity/liveness in short helper calls so
test-expression references cannot influence subsequent cleanup assertions; final
95-check run passes. Do not count the print-sensitive run as ownership acceptance.
Owner 2,938 unchanged, override restored, process terminal. C134.26/D68.32 GiB
free; only small scripts/data/map added, no runtime or art copies. Production
unchanged. Native artifacts: `shared-bank-checks/{probe.gd,native.log,owner.json}`.

Next: unsupported material and integrated Group/Bank native drawing checks, then
merge the private render hooks onto current accepted Grid/Main and run matched
real station comparisons. Remaining full release gates stay open.

### Integrated drawing and current-source real-map pilot

`check-shared-integrated-drawing.py`: 480 byte-exact native comparisons using
actual Bank descriptors and Group's automatic palette connection/trim callback.
Three real sheets, normal/flood/custom shader materials, ancestor RGB, draw tint,
nearest/linear transitions, mirrored regions, opacity and mixed ordinary commands.
384 indexed/1,056 fallback commands, zero engine errors; explicit cleanup passes.

`build-shared-current-grid.py` applies only the private provider hooks to the
current accepted Grid. Keeps synergy geometry, deferred zoom group scheduling,
selection-key retention and workshop camera/scale behavior. Current Main is used
with two benchmark-only paused toast tweens; door membership and current Bill
are preserved. First pilot launch failed from generated Main indentation before
gameplay; fixture generator corrected, failed process terminal before retry.

Actual debug=false native large-station pilot: two runs, 2,160 measured frames,
idle/pan/zoom/lighting at 1×/2×/4×. All 12 complete states/camera paths/action-speed
labels exact. Reference→candidate:

| Metric | Reference | Shared candidate |
| --- | ---: | ---: |
| Mean frame ms | 25.876 | 25.974 |
| p95 ms | 42.181 | 42.129 |
| p99 ms | 51.883 | 48.636 |
| Frames over 50 ms | 15 | 8 |
| Maximum ms | 65.567 | 71.206 |
| Frames over 100 ms | 0 | 0 |
| Peak texture MiB | 3,028.007 | 2,630.399 |
| End texture MiB | 1,924.488 | 2,017.900 |

One pair cannot establish a repeatable timing gain. Mean slightly worse; peak
texture reduction about397.6MiB, but end memory higher. Candidate backend active
in every phase, zero original fallbacks/duplicate ordinary cache entries, final
7,891 indexed commands. No missing runtime-art reports or engine errors. No
production admission or release certification.

Artifacts `shared-palette-real-map-pilot/` include source identities, 12-phase
reports, bounded frame traces, comparison and owner guard; no screenshots/runtime
copies. Owner 2,938 unchanged, jobs terminal, override restored. Next three matched
pairs on each real map, adding shared-bank memory diagnostic fields and comparing
against the prior indexed backend if attribution is needed. Retain all full gates.
