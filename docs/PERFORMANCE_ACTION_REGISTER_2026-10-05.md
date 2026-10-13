# Performance research and action register

Updated: October 9, 2026 · BrineSpace · Release remains blocked

Current continuation: installed crew storage/cache lowers sampled texture memory;
Windows/Mac same-input candidates audited, native Mac certification still open.
Private rock batching/buffering remain unadmitted: both preserve checked states,
but large frame gates fail and gains are marginal. Private local wall invalidation
passes22 dependency checks and15 exact packaged cached-vs-forced-wall snapshots;
matched session15478 running. First12-room pair reduces placement/demolition wall
rebuilds, with effectively unchanged mean frame time. See [current status](CURRENT_STATUS.md)
and [wall evidence](LOCAL_WALL_CACHE_TRIAL_2026-10-09.md).

New diagnostic issue: disabling retained surfaces makes the station disappear
behind retained environment layers in the unchanged packaged baseline. The old
direct-renderer pixel reference is invalid for the current layered path. Reproduced
and visually reviewed; no source fix yet. Default retained gameplay remains the
reference for wall trials, compared against forced wall repaint. This is not proof
that every public settings combination is certified.

Session artwork cleanup enabled: last-owner Main/Studio exit releases factory
images/derived templates and both floor generations; live overlap preserved.
18 native checks, three matched pairs: title 682.40→383.46 MiB; following Continue
3,629.99→3,473.92 MiB. Reload-stage median 4.767→5.040 s. Ten final transitions
have <0.1% settled growth; owner files unchanged. Active memory and other release
gates remain open. [Evidence and tradeoffs](SESSION_ART_LIFETIME_2026-10-05.md).

H8 enabled narrowly: Veld's repeated reading-pose GPU scan caches six weak poses
only for explicitly immutable pooled images; identity/metadata guards preserve
replacement and mutable fallbacks. Full-bank three pairs measure 434–437→15 us.
838 focused / 46 pool checks and 22,683 actual interruption/restore checks pass;
56 interruptions / 12 fresh-main disk restores, owner files unchanged. No memory
remedy or overall FPS claim. [Evidence](READING_POSE_CACHE_2026-10-05.md).

R8 enabled narrowly: Reduced Motion retains ordinary split-library live effects;
inactive library props already retained. 373 native checks / 204 pixel pairs and
existing split-prop regression pass. Three pairs per selected room remove repeated
74–124 us effect drawing; normal animation cadence unchanged. No texture/full-FPS
claim; owner profile unchanged. Next prioritize full-roster memory and long stalls.
[Evidence and remaining gates](FROZEN_PROP_EFFECTS_2026-10-05.md).

R7 enabled: light-map one-shot scheduling on existing contents, scroll and size;
quality off/re-enable preserved. 73 native checks / 18 actual-lit-map pixel pairs
plus existing alignment/crew-lamp tests pass. Three stationary pairs remove two
draw calls; small pass (~0.078 ms GPU when continuously rendered), no FPS claim.
Held viewport counters are stale and excluded as fresh work. Owner files unchanged.
Next R8 unchanged live prop output. [Evidence and limits](LIGHT_MAP_SCHEDULING_2026-10-05.md).

R6 water-template candidate rejected: 336 native pixels exact, but filling costs
620→704.5 us versus small fixed-level gains. No runtime cache enabled; prior
cosine hoist retained. Next R7 light-map GPU cost and update scheduling. Owner
files unchanged. [Experiment and next action](MOON_WATER_TEMPLATE_2026-10-05.md).

R6 profiled: 64 native cases / 768 frames measure large-room props ~0.21–0.44 ms
and Moonbay shell ~2.08 ms. Focused profile finds water ~1.15 ms. Applied small
cosine-expression hoist; final 144 pixel comparisons exact, fixture 939→889.5 us.
Large-room retention/culling still open; no overall FPS claim. Owner files unchanged.
See [profile and scope](LARGE_ROOM_PROP_PROFILE_2026-10-05.md).

R5 enabled in source: scene-owned retained terrain cells preserve ordering and
exact progress. 296 native checks / 272 exact pixel comparisons pass. Three
matched 40-room pairs: excavation terrain CPU 5.67–5.86→0.76–0.79 ms; aggregate
frame measure 46.555→41.602 ms. Excavation p95 improves at all speeds; other tails
mixed and long stalls persist. Texture budget remains failed; owner files unchanged.
Next R6 large-room prop profiling. [Implementation and limits](TERRAIN_CELL_RETENTION_2026-10-05.md).

R5 native prototype: per-cell terrain commands preserve original ordering and
match 208 pixel cases. Progress fixture median CPU preparation+draw 2.215→0.479 ms;
draw counts unchanged. No runtime changes enabled. Next integrate scene-owned
host and verify first-frame drawing, zoom, plants, cell/scene lifecycle and real
station excavation performance. [Evidence and scope](TERRAIN_RETENTION_PROTOTYPE_2026-10-05.md).

R4 enabled: bounded per-fleet failed-route cache with content-based topology
invalidation and restore clearing. Boolean-only failure avoids identical fallback.
Production Fleet.advance fixture: 60 blocked updates 120→1 BFS, 191,400→1,595
visits; median 177.688→2.005 ms across nine pairs. 33 new checks, 5,859 matched
state/completion comparisons and six existing suites pass; owner files unchanged.
Targeted headless CPU evidence, not gameplay FPS certification. Next R5 terrain
excavation invalidation. See [implementation](DRONE_ROUTE_CACHE_2026-10-05.md).

R3 closed as already handled in the default path: the live caller pre-expands and
caches split wrappers. Initial direct-call reproduction bypassed that cache.
Candidate removed; retained native regression passes 181 checks, including 144
exact pixel comparisons. No new speed gain claimed; partial candidate benchmarks
discarded. All 2,936 owner files unchanged. Next R4 failed drone routes.
See [corrected finding](SPLIT_PROP_RETENTION_2026-10-05.md).

R2 enabled in source: skip only mineral polygons whose computed vertex alpha is
zero everywhere. 40 native pixel/field comparisons pass, saving 34–36 calls in
the fixture. Three 40-room candidates versus three references (shadows enabled
in both) average 4,958 versus 5,005 calls. Frame-time aggregate 41.704→40.063 ms,
but p95 is mixed and ~1 s stalls remain: no consistent FPS claim. Memory still
~4,097 MiB; owner 2,936 files unchanged. Next reproduce R3 with real renderer.
See [implementation and limits](TERRAIN_DRAW_SKIP_2026-10-05.md).

R1 accepted in source: per-foot contact-band batching now enabled with reference
fallback. Separate geometry/palette caches avoid light-driven vertex rebuilds.
128 maintained pixel comparisons and 192 actual room floor/shadow comparisons
are exact. Three revised 40-room runs versus three references reduce mean of
phase mean-frame-time medians 43.344 to 39.883 ms and draw calls 5,427 to 5,005;
lighting-shadow CPU improves in all speeds. Long stalls and release gates remain
failed; not packaged/Mac acceptance. Owner 2,936 files unchanged. Next R2.
See [implementation and measured limits](CONTACT_SHADOW_BATCH_2026-10-05.md).

Latest loading test: normal title/prefetch path spends ~0.86 s on crew alpha-bound
scans. Moving them to workers worsens median measured startup stages from 3.99 s
(follow-up control) to 4.92 s; candidate removed. Nine warm inventories match all
8,188 records. Retained only additive alpha_bounds_usec diagnostics; native pool
regression passes 46 checks, owner 2,936 files unchanged. Startup fixtures emit
one common exit-leak warning, not release-exit acceptance. Resume R1 then R2,
with full-room parity and matched workloads. See
[normal startup measurement](STARTUP_ALPHA_BOUNDS_2026-10-05.md).

Latest M1 worker test: bounded background decode reduces pod-first Veld preparation
to 14.46 s; worker bounds/direct images with 32 pending jobs reaches 10.34 s.
The latter stays within a 16 MiB pending-image reservation cap, preserves 42 pod
samples and 3,186 frame identities, but misses the fastest thaw window (~1.35 s).
Do not enable recovery-triggered whole-bank deferral or increase gameplay slice
budgets to hide it. Final corrected native runs have zero errors, owner files
unchanged. Next assess worker bounds in actual startup loading, which already
uses background decoding; continue draw-work and full-roster memory remedies.
See [worker preparation results and limits](ABSENT_CREW_WORKER_2026-10-05.md).

Latest M1 absent-crew experiment: pod-first Veld preparation starts with 63 images /
8.14 MiB decoded rather than 1,800 / 365.35 MiB. All 42 pod source-pixel/metadata/
filter samples match; 3,186 frame identities survive. However, deferred preparation
with a 2 ms work target takes 18.67 seconds / 1,069 render slices, too late for
thawing at 4x. No runtime deferral enabled. Next bounded worker decode/small-image
upload test and explicit startup/Continue roster requirements. Two native runs,
zero errors, 2,936 owner files unchanged. See
[absent crew preparation](ABSENT_CREW_PREPARATION_2026-10-05.md).

Latest M2 trace: isolated four-drone workload acquires 1,148.438 MiB; 413.438 MiB
of effect storage is temporarily not submitted but is needed later in the cycle.
Worker decoding still leaves 12.610–19.592 ms main-thread finish per full effect
sheet; synchronous reload takes 105–111 ms. Do not enable active-sheet eviction.
Next inspect absent-crew startup banks and first-use requirements. Evidence:
[drone trace/reload](DRONE_RESIDENCY_TRACE_2026-10-05.md).

Implemented cleanup fix: pending drone image drain now preserves the decoder's
invisibility flag. Actual blank atlas reproduction falls from 96,337,920 bytes to
4; visible pixels unchanged. Drone regression passes 252 clips / 144 directional
samples. Not yet packaged; active fleet's ~1.15 GiB allocation remains unresolved.
See [validated fix](DRONE_PENDING_IMAGE_FIX_2026-10-05.md).

Latest M1 conservative accounting: pinning bare/death, movement/hazard and furniture
families leaves only 41.716 MiB decoded Veld candidates, still requiring current-job
entry/exit protection. Six native pause/cancel/in-memory-restore cases pass with
512 non-null frame requests; all art resident. No production memory saving.
Do not implement a broad inactive-helmet policy from the 202 MiB upper bound.
See [pin accounting and limits](VELD_PIN_POLICY_2026-10-05.md).

Latest M1 deadline test: six normal-delta native equipment actions observed with
all art resident. 4x equip completes in 549 ms / 33 frames; this rejects reloading
all 769 candidate images one per frame at action entry. Idle/walk successors need
advance coverage. A 932 ms interval occurred without eviction and remains open.
Next conservative pin-set accounting and interruption/restore coverage. See
[transition deadlines](VELD_TRANSITION_DEADLINES_2026-10-05.md).

Latest M1 inventory: complete selected Veld banks use 365.35 MiB unique decoded
storage. A fixture retaining bare/death images and detaching other helmet-only
images expires 769 allocations and drops the engine counter by 202.32 MiB.
This is an unsafe-for-gameplay upper bound, not an accepted policy. Next log live
locker preparation deadlines and consumer pins without eviction. See
[full Veld inventory](VELD_RESIDENCY_INVENTORY_2026-10-05.md).

Latest M1 experiment: one selected six-frame crew clip now demonstrates actual
storage release while preserving wrapper identity, 108/108 native image comparisons
and 30 timing checks. About 1.67 MiB drops on the engine texture counter; preparing
five missing images takes about 41 ms spread over five frames. No runtime eviction
enabled. See [residency experiment](ANIMATION_RESIDENCY_EXPERIMENT_2026-10-05.md).

## Objective and acceptance

This is the consolidated entry point for the recent performance investigations
and the forward implementation queue. Linked reports retain detailed evidence;
their dated next-step suggestions do not constitute competing queues. Update this
register as candidates are implemented, rejected or measured.

Release still requires packaged Windows and Mac gameplay, p95 <=16.7 ms and p99
<=25 ms, no reproducible gameplay stall >100 ms, investigation of frames >50 ms,
texture memory <=2 GiB in 12 rooms and <=3 GiB in the large scene, and settled
transition growth <=5%. Loading targets are <=10 s cold / <=6 s warm. The full
workload, endurance, bug and visual gates remain in the
[readiness plan](RELEASE_READINESS_2026-10-04.md) and
[release workflow](RELEASE_WORKFLOW.md).

## Accepted decisions and constraints

Preserve selected art, pixels, filtering, animation timing, layering, gameplay,
owner layouts and explicit settings. No global downscaling, removed frames,
automatic quality cuts, renderer upgrade or broad refactor. Tests use isolated
profiles with resolved user-data verification and owner-file fingerprints.
Frozen releases remain immutable; uploading is a separate action.

Evidence labels below distinguish **prototype** (controlled experiment),
**source** (mechanism found, gameplay impact unmeasured) and **hypothesis**
(requires attribution). None means a packaged performance gate has passed.

## Current state

### What the measurements establish

- The accepted packaged comparison still failed performance/memory gates on the
  owner's RTX 4070 Ti. Reported medians were approximately 4035 MiB for large/1080p
  and 3631 MiB for reported/1080p. Fresh-profile loading is not controlled cold-disk
  loading. These are specific package results, not current-source certification.
  [Package comparison](PERFORMANCE_PACKAGE_RESULTS_2026-10-05.md).
- Frozen-scene attribution found 1221 floor, 873 room-content and 798 combined
  terrain draw-call deltas. These are individual omission experiments, not additive
  CPU/GPU savings. [Render attribution](RENDER_LAYER_ATTRIBUTION_2026-10-05.md).
- Transparent mining-effect draw removal is implemented and pixel-verified, but
  matched gameplay showed no consistent FPS gain and no texture-memory reduction.
  [Matched results](EMPTY_EFFECT_GAMEPLAY_COMPARISON_2026-10-05.md).

### Ranked implementation queue

Order reflects evidence and scope, not estimated FPS. Memory and platform blockers
below remain mandatory even if every small rendering change succeeds.

| ID | Candidate / state | Evidence | Next action and acceptance |
|---|---|---|---|
| R1 | Equipment contact-shadow batching; enabled in source | 128 exact regression / 192 room comparisons; three revised 40-room runs improve measured aggregate frame time ~8% | Packaged/1440p/minimum-hardware/Mac checks pending; retain reference fallback and switch |
| R2 | Skip zero-alpha mineral polygons; enabled in source | 40 exact pixel/state checks, 34–36 fixture calls removed; three matched station pairs show ~47 fewer calls with mixed frame tails | Packaged/minimum-hardware/Mac and actual excavation-loop checks remain; no consistent FPS or memory gain claimed |
| R3 | Already handled in default path; candidate removed | Caller caches expanded wrappers; 181 native checks / 144 pixel comparisons pass on unchanged source | Keep regression coverage; direct raw submission is not the default workload. No new performance gain |
| R4 | Enabled in source | Actual fleet fixture: 120→1 BFS / 60 blocked updates; 177.688→2.005 ms median; 33 checks and 5,859 exact state/completion comparisons | Keep native station/platform gates open; cache bounded and invalidated by blocker contents/restore |
| R5 | Enabled in source | 296 native checks / 272 pixel comparisons; three matched station pairs reduce excavation terrain CPU ~5.8→0.8 ms | Packaged/platform, full camera-motion pixels and endurance gates remain open; no memory remedy |
| R6 | Profiled; retention/culling open | 64 native cases; props ~0.21–0.44 ms, Moonbay shell ~2.08 ms, water ~1.15 ms; small cosine hoist pixel-exact | Target Moonbay water invariant preparation first; preserve mission motion, multi-room ordering, owner props and flood/crew layering |
| R7 | Enabled in source | 73 native checks / 18 pixel pairs and existing alignment/crew-lamp tests; stationary fixture removes two draw calls | Full moving/focus/window/platform/package gates remain; held viewport counters are not new GPU samples |
| R8 | Enabled for frozen ordinary library effects | 373 native checks / 204 pixel pairs; three matched pairs per room eliminate repeated Reduced Motion effect painting | Normal animation unchanged; custom/portable/drone/aquarium excluded, full-station/package gates remain |
| R9 | Terrain chunk culling / compatible geometry batches; source | Full-field retained terrain still submits commands | Measure conservative chunks before batching; preserve UV arithmetic and transparency order; compare pan/zoom boundaries |

Evidence and regression details: [render/terrain research](PERFORMANCE_RESEARCH_2026-10-05.md),
[routing and secondary risks](SECONDARY_PERFORMANCE_RISKS_2026-10-05.md),
[prop/animation research](PROP_ANIMATION_RESEARCH_2026-10-05.md).

### Memory and loading work: required independent track

| ID | Finding / state | Next action |
|---|---|---|
| M1 | Whole-station Veld VRAM/RAM tradeoff measured; experimental | Three paired 12/40-room diagnostics reduce textures ~486–487 MiB, increase Windows working set ~297–365 MiB and slightly worsen phase means. Do not enable by default or claim M1 RAM savings. Pixel/lifecycle gates remain scoped; source admission/full workloads/hardware open. See VELD_WORKLOADS_METAL_GUARD_2026-10-06.md |
| M2 | Upload hitches aligned; live-texture reuse hypothesis negative in 40-room trace | No surviving same-path texture at reupload; do not add weak reuse without benefit. Cropped source pixels exact, but 358/416 native raster pairs differ (nearest boundaries/linear filtering); no crop backend admitted. Next Compatibility UV/sampling or discovery/UI cycle work. See DRONE_ATLAS_REUSE_SAMPLING_2026-10-06.md |
| M3 | Last-owner cleanup; unused floor/deck uploads skipped | Both floor generations release after Main/Studio exit. Profile-grain omission saves 41.98 MiB active (387 checks/96 pixel pairs). Corridor-deck omission saves another 6.00 MiB first-entry in three matched pairs (618 transit checks/144 pixel pairs). Active-session retired meshes still need canvas-reference tracing; no active-state eviction |
| M5 | Cross-scene artwork/material/transit cleanup; enabled | Prior title 682.40→383.46→262.05 MiB. Transit cleanup now 262.05→190.65 MiB; following gameplay 3,431.95→3,417.95 MiB. Three transit pairs and ten transitions pass (<0.19% growth); no final errors/shutdown warning, earlier intermittent warning still unassigned. Loading samples mixed. See TRANSIT_MATERIAL_MEMORY_2026-10-05.md; active animation/fleet budgets remain unresolved |
| M4 | Startup prefetch window bounds count, not pending bytes; source | Collect existing peak/unused-work metrics through title entry; measure final task drain; compare missing/current/stale manifests before changing scheduling |

[Pool diagnosis](POOL_MEMORY_DIAGNOSIS_2026-10-05.md),
[drone diagnosis](DRONE_MEMORY_DIAGNOSIS_2026-10-05.md),
[memory research](PERFORMANCE_RESEARCH_2026-10-05.md),
[mesh lifetime](SECONDARY_PERFORMANCE_RISKS_2026-10-05.md),
[loading coverage](PERFORMANCE_COVERAGE_RESEARCH_2026-10-05.md).

### Measure before changing

| ID | Risk | Discriminating check |
|---|---|---|
| H1 | Automatic reports add a secondary pause | Time readback, snapshot, PNG and ZIP separately in normal entry; script fixtures disable automatic capture, so this cannot explain their original stalls |
| H2 | Error-log bursts | Measure bytes/backlog and parse time; group-count limit does not bound per-poll work; preserve error counts if bounding reads |
| H3 | UI refresh bursts and synchronous saves | Attribute frame spikes to existing refresh/save stages before staggering work; retain immediate feedback and save integrity |
| H4 | First-use shader/art work | Compare first and repeated actions in release gameplay; warm benchmark results miss some first encounters; fresh profile is not proof of cold driver cache |
| H5 | Full-screen effects and display scaling | Record actual drawable size and matched CPU/GPU times; one shared atmosphere screen reader does not imply a copy per effect |
| H6 | Audio decoding | Compare actual playback enabled/stopped with active voice counts; volume zero does not isolate playback; no unbounded music-player growth established |
| H7 | Frame selection and procedural effect allocations | Profile duration scans and repeated geometry construction; cache invariants only with timing/pixel parity; no blanket animation-rate reduction |
| H8 | Repeated reading-pose GPU readbacks; narrow cache enabled | 838 focused checks, 46 pool checks, 56 gameplay interruptions / 12 disk restores; repeated full-bank helper 434–437→15 us | First scan and other interruption/death comparisons remain; this does not enable safe texture eviction or establish overall FPS |
| H9 | Emergency Metal eligibility guard enabled in source | Ample-Metal/off-interval cycles skip observational route queries. Red→green regression + fleet/cache suites pass; three native pairs reduce recurring cycle median 101.932→68.334 ms, state unchanged. Other stalls/gates open. See VELD_WORKLOADS_METAL_GUARD_2026-10-06.md |
| H10 | Stabilization reward persistence combined in source | Four awards use 4 protected writes instead of 8; one matched headless CPU pair 12.671→7.311 ms with all 12 phase states/final progress unchanged. Meta reward/isolation tests pass; discovery suite has existing four-room foundation mismatch. Native pacing still pending. See CYCLE_PERSISTENCE_OPTIMIZATION_2026-10-06.md |
| H11 | Hand control reuse retained in source | Permanent isolated fixture: 74 checks, 12 exact native image pairs, clean exit; art/input/hover/drag/invalidation covered. Three matched normal-renderer 40-room pairs reduce per-run mean card refresh median 4.449→0.167 ms; phase states match. Overall frame means ~36–37 ms, max ~173 ms, textures 4,283 MiB unchanged; full gates open. See HAND_REFRESH_OPTIMIZATION_2026-10-06.md |
| H12 | Dry goal reachability proof retained in source | 142 permanent checks and service/room/swim/clearance suites pass. Three native 40-room pairs reduce maintenance median 140.631→31.905 ms, recurring frame ~174–179→65–71 ms; compared crew paths/needs/RNG and phase state match. Overall frame means, remaining >100 ms stalls and memory still fail gates. See DRY_GOAL_REACHABILITY_2026-10-06.md |
| H13 | Upload attribution; benchmark reporting corrected | Two native traces confirm large rover upload inside exterior callback; draw accumulator now read every measured sample, engine wait excludes collection. Five zoom trace/counter discrepancies remain. Lossless private Veld storage feasibility 365→27 MiB, 1,800 exact decodes; no runtime memory/FPS claim. Next bounded working-storage prototype. See LAYER_UPLOAD_ATTRIBUTION_2026-10-06.md |
| H14 | Compressed private Veld bank implemented; not admitted | 14,450 native checks/4,788 exact image pairs and 48,847 consumer checks pass. Three 40-room pairs save 485.67 MiB textures; median peak working set +38 MiB rather than prior eager-bank +300–365 MiB, no FPS gain, texture gate still fails. Two transitions pass; shared exit warning remains in normal reference. Next other crew/identity coverage and longer ownership tests. See COMPRESSED_VELD_STORAGE_2026-10-06.md |
| H15 | Combined replacement-crew storage prototype; not admitted | James/Marsh native pixel and consumer checks pass. One busy 40-room pair with Veld/James/Marsh active: textures 3,970.52→2,619.40 MiB; 15 recorded crew/world phases match. Loading +3.02 s, peak working set +141.84 MiB; no FPS gain. Fixture texture budget passes, release gates remain open. Next repeatability, stronger states, ten transitions and startup compression cost. See COMPRESSED_REPLACEMENT_CREW_2026-10-06.md |
| H16 | Private bounds cache fixes measured startup redundancy | One uncached/cached busy pair: bounds 1,897.7→572.2 ms; readiness 15.76→14.54 s, texture footprint unchanged. All 15 full actor snapshots match, actual per-actor presentation proved. All three selected-bank pixel/metadata/filter/clock consumer checks pass; owner unchanged. Experimental only; repeatability, lifecycle, loading/frame gates remain. See COMPRESSED_REPLACEMENT_CREW_2026-10-06.md |
| H17 | Combined ten-transition ownership verified; Studio warning open | Candidate 826/normal 296 checks pass; old resources release, title textures equal and growth <5% in four-room lane. Candidate warns once, current normal control clean. Removing Studio eliminates warning; audited effects/context/grid release. Next isolate private routing/Studio interaction; no admission or full endurance claim. See REPLACEMENT_CREW_LIFETIME_2026-10-06.md |
| H18 | Warning trigger narrowed; no speculative fix retained | Studio registration/drawing excluded as sufficient causes. Effects StubGame construction in full scene reproduces; grid and minimal standalone/reload controls clean. Two initialization rewrites fail and remain private experiments. Next full-scene stage reduction; memory/frame/loading/Windows/Mac gates remain open. See STUDIO_CONTEXT_WARNING_ISOLATION_2026-10-06.md |
| H19 | Camera scene lifetime guards retained in source | Actual-method regression changes two failures/ten error lines to zero; attached/revision behavior preserved. Recovered-only and full Studio/two-Continue controls clean, anonymous warning absent with only guards updated. Next guarded ten-cycle confirmation; backend admission/performance/platform gates open. See CAMERA_SCENE_LIFETIME_FIX_2026-10-06.md |
| H20 | Ten-cycle warning remains; separate hashing rejected | Guarded ten-cycle 826 behavioral checks pass and old resources release, but anonymous warning returns once. Loader experiment avoids 3,267 alias decodes yet costs +426 ms due hashing; unaccepted. Next single-buffer loading remedy; camera error fix remains verified. See ENCODED_SHARING_LOADING_2026-10-06.md and CAMERA_SCENE_LIFETIME_FIX_2026-10-06.md |
| H21 | Single-buffer private loader improves first-load bank timing | One matched pair 8.395→7.259 s; all three selected-bank consumer checks pass. Prefetch empty-order 8.665→7.522 s; warm 2.694→2.729 s, no gain. Worker bounds unchanged, worker aliases still decoded. Next full-scene/repeatability/error paths; no normal admission or FPS claim. See SINGLE_BUFFER_LOADING_2026-10-06.md |
| H22 | Single-buffer startup gain repeated in full native station | Three 40-room pairs save 0.783–1.293 s, median paired 1.212 s; 45 full crew/world phases equal, zero missing routes/errors. Textures unchanged, working-set deltas mixed, no FPS gain; loading/frame gates fail. Private only; next title/warm/save/error-path coverage. See SINGLE_BUFFER_STATION_2026-10-06.md |
| H23 | Private loader error paths fixed; short native lifecycle passes | 15 independent error/pixel/status checks pass after two failures/seven errors. Reference/candidate title/transmission/Studio/save/Continue each 154 checks, zero errors, owner unchanged; prior ten-cycle warning remains open. Next progress/worker alias decoding and renderer/upload stalls; no normal admission. See SINGLE_BUFFER_LIFECYCLE_2026-10-06.md |
| H24 | Source loading progress serviced during frame registration | Native 7 checks, existing prefetch test and private 154-check lifecycle pass. Long update gaps reduced, not eliminated; first registration still follows 783/656 ms gap. Whole-scene worker peak ~96.7 MiB; instrumented exit warning open. Next time door finish/card readback/region scans; no FPS or speed certification. See LOADING_PROGRESS_SERVICE_2026-10-06.md |
| H25 | Exact row-endpoint card region scan enabled in source | 406 exact/input checks, 79 runtime paths; paired CPU 447→50 ms. Native 95 calls scan 678→99 ms, optimized Continue 99 ms; actual 154-check lifecycle passes, owner unchanged. Exit warning/readbacks/FPS gates open; next progress confirmation and gameplay upload stalls. See CARD_REGION_SCAN_2026-10-06.md |
| H26 | Raw texture bounds avoid immediate GPU readback in source | 339 native exact texture/header/region/fallback checks and 154 lifecycle checks pass. Observed readback totals ~35 ms lower fresh/Continue; prior scan fix now has 364/322 ms loading gaps. No FPS claim, exit warning open. Next Main direct CPU mipmap preparation and gameplay upload stalls. See RAW_REGION_READBACK_2026-10-06.md |
| H27 | Single-upload mipmapped cards enabled in source | 358 native checks cover all mip chains and 36 exact fan rasters. Three 79-card API preparation pairs save median 66.5 ms; 154 lifecycle checks pass, owner unchanged. No FPS/cold release claim; exit warning/gates remain open. Next gameplay frame pacing and rover uploads. See CARD_SINGLE_UPLOAD_2026-10-06.md |
| H28 | Lossless full-dimension drone palette feasible; private only | Two UV crop remedies fail; full-atlas shader 416 exact. RG8 ID palette body has 208 exact nearest rasters, linear original fallback; reported texture allocation halves ~184→92 MiB, three prepared-image API upload pairs median 14.659→6.272 ms. No gameplay/other-atlas/Mac admission; next one-atlas session provider preserving texture/filter/material/lifetime semantics. See DRONE_LOSSLESS_PALETTE_2026-10-06.md |
| H29 | Private palette effect composition exact | 192 visible-art native pairs match current submersion/fog and actual ambient/point light; zero errors, owner unchanged. Single body/nearest scope; whole-canvas or body-only child routing would violate mixed layers/order. Next ordered complete-drone provider, texture/filter/lifetime and actual station tests. See DRONE_PALETTE_EFFECTS_2026-10-06.md |
| H30 | Ordered private drone provider passes composition/ownership | 136 checks, 120 exact complete-layer rasters, two-drone overlap, inherited filters/material fallbacks, wrapper/image identity and cache accounting. Shared session survives first owner, automatically releases all resources at last exit; owner unchanged, zero errors. Next physical 40-room integration with dust/harvest/admin/survey ordering and actual frame/memory/preparation measurements. See DRONE_ORDERED_PALETTE_2026-10-06.md |

Details: [secondary risks](SECONDARY_PERFORMANCE_RISKS_2026-10-05.md),
[coverage research](PERFORMANCE_COVERAGE_RESEARCH_2026-10-05.md),
[animation research](PROP_ANIMATION_RESEARCH_2026-10-05.md).

### Release blockers and coverage gaps

- **Windows long stalls:** reproduced beyond game content; attempted engine query
  caching did not resolve them. Required scheduling trace is blocked by unavailable
  elevation. Prepared capture exists; do independent optimization work meanwhile.
  [Trace handoff](WINDOWS_QUERY_REMEDY_2026-10-05.md).
- **Benchmark scope:** retain fixed-step, uncapped comparisons, but add normal-clock
  packaged gameplay with saved VSync/cap preferences, first-use actions, focus,
  pause and speed changes. These lanes answer different questions.
- **Mac:** Universal packaging does not certify M1 performance, Retina, inputs,
  saves or audio. Native target checks and Developer ID/notarization/Gatekeeper
  acceptance remain pending. Intel remains unverified.
- **Endurance and bugs:** maintain the nine original reports, save/Continue, Studio,
  navigation, construction, UI scaling and two-hour/ten-transition checks. Research
  does not close these issues. Revalidate the selected final candidate on target
  hardware; do not combine unmatched runs into a passing result.

### Rejected approaches and bounded claims

- Cropping/atlas remapping and duplicate-cell reuse experiments failed native pixel
  comparisons; storage estimates and offline reconstruction are insufficient.
- Screen-reader query caching was tested and did not remedy the Windows stall.
- Transparent draw removal saves those commands; its current matched results do
  not support an FPS or memory improvement claim.
- A texture cache limit, global frame cap, automatic quality reduction, MultiMesh
  conversion or worker-thread migration is not an established remedy for this game.

## Verification

Consolidated existing reports and current status; no new benchmarks, game launches,
runtime changes or owner-profile writes. This register and its CURRENT_STATUS link
are the only changes in this consolidation. Prototype counts retain their original
scope; no newly accepted implementation or release result.

## Next action

R1 and R2 are enabled in source; keep their packaged/platform acceptance open.
R3 is verified as already handled; R4 is enabled with production-caller and
topology-change checks. R5 is enabled with native parity and matched workloads.
R6 is profiled; water-template cache rejected on filling cost. Next R7 GPU
measurement and light-map update scheduling are complete within native fixture scope.
R8 ordinary library Reduced Motion retention is enabled within native fixture scope.
Next prioritize full-roster memory and long-stall attribution; R9 remains open.
Do not reopen broad research unless these experiments expose a new
question. Keep M1 ownership work visible as a mandatory memory remedy, not something
the draw-call queue is expected to solve.

For each completed item record: implementation revision, evidence paths, before/
after p95/p99/stalls/memory for the same workload, behavioral/visual checks, and
decision to retain or revert. Mark unavailable measurements explicitly; never
promote a source finding directly to a confirmed performance gain.
