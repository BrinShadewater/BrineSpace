# Frozen Windows / Mac release QA — October 16, 2026

Status: candidate freeze, Windows functional QA, controlled benchmark matrix, two-hour normal-process station soak and matching Mac static package completed. **Release certification remains on hold for pacing/cold loading/Save hitches, unresolved live-object growth and target hardware/native Mac checks.** This report describes a new full-current-source candidate; earlier private performance runtimes do not certify it. No production gameplay, art, crew, navigation or rendering changes were made for this task. No publication or commit.

## Candidate and selection

- Evidence/source root: `D:/bs-release-qa-20261016/`; physical source under `source/`, Windows delivery under `windows/`.
- HEAD `67e7db969f7c5d952a3c80830369715d703199c5`, with current dirty/untracked program/runtime bytes. Original and clone index/HEAD membership all match: 60,460 paths. Clone uses long paths; absent nonselected authoring assets deliberately skip-worktree. No source hardlinks.
- 61,620 frozen files / 4.914 GiB: reachable runtime resources, complete current program/config/tools/tests, paired UID/import sidecars and verified official templates. `selection.json` and `frozen-inputs.json` preserve selection and exact input bytes. Nonreachable authoring generations, vendor packs and prior outputs remain in the original workspace.
- Current normal source includes later Marsh water-frame/dead-exterior fixes and accepted Windows LA8/cropped-cargo paths. Private LOD/stable-ID/native-water/structural cohorts and the unproven crew endpoint shortcut are excluded. No old private grid/main/PCK overlay.
- Build **brinespace-b0b5d1b031c6ec29**, source SHA256 `b0b5d1b031c6ec2907b59ac03601e4a389eb096ca3cfb1cd2371470bf5f0abe1`. Maintained Windows exporter; verified editor and official templates **4.7.2.stable.official.ed1daf0bf**.
- Windows EXE 109,283,328 bytes, SHA256 `7208c3a81fbb5e0af24ab319bd377bf2e72e9b5fdcc01d709bafe1550e067b76`.
- Windows PCK 3,629,076,317 bytes, SHA256 `6b3533d80cc940035c2a86ac36f679e9df69d04360b17febf91e3eac7de1c5d4`.
- Manifest: 36,430 entries / 3,596,741,107 source bytes. Delivery has no QA overrides; all native fixtures use a physical copy.

## Package, entry and lifecycle evidence

- Python release manifest **10**, release assertion safety **2**, Mac exporter selection **2** tests pass.
- Empty-project raw asset audit: **35,942 checked; missing/changed/remapped/unexpected all zero**. All **431 selected script/shader sources** and build metadata match. The pack additionally contains **421 scripts** (410 tools, 10 rooms, one scripts); every one matches the complete physical freeze, zero unexpected scripts. The initial selected-only whitelist failure remains preserved. Inclusion cause is unproven; maintained exporter/package were not changed to strip them.
- Actual release normal configured intro/title/New Game and fresh-process Resume: **54 checks each**, debug=false, normal costs/failures, observed architect/transmission/Continue, core wake and simulation. Resume verifies run identity and detached logical saved state. Intro advances before SPACE skip; this does not certify natural full-length playback or audio.
- Real F8 Save button starts asynchronous report writing; completion, ZIP/live snapshot/schema/build ID, checkpoint immutability and exact screenshot pixels pass. No Send/upload. The one-room request took 1.936 ms on main; worker took 270.623 ms (248.922 PNG, 21.666 packaging), with 19 process frames pending. These differ in workload from the earlier large-station report study and are not an optimization delta.
- Dedicated rendering fixture: **57 checks**, final clean shutdown. Connected Farm raised-door endpoint exposes expected `343b3bff` backing; card size/content at 1600×900 and 1280×720, department backing under authored metal frame, live interior fades, integrity warning and retained actor snapshots pass. Native PNGs reviewed. Door endpoints are injected into a renderer copy; no crew-traversal or broad new-art acceptance.
- Ten actual packaged Continue/Return-to-Title cycles: **59 checks**, station textures **1,424,790,909 bytes** and title **162,965,165 bytes** stay flat; settled object/resource/node counts stable after warmup. Packaged title Quit exits cleanly without warnings/errors. Release static-memory and orphan counters report zero but are not usable zero-memory/orphan-free evidence; see the engine-source clarification below.
- Earlier direct UI-helper exits warned about 31/32 generic zero-reference RefCounted objects. The rendering helper initially retained two StyleBoxes on its suspended completion stack; deferring quit until stack unwind fixes that helper's resource warning. Normal lifecycle Quit is clean; these observations do not establish a growing gameplay leak.

## Preserved harness failures

The first rendering harness attempted ordinary save after enabling dedicated free-build/failure suppression. Production correctly returned ERR_UNAVAILABLE / "No active loop to save." The corrected harness verifies that rejection and retains a separate diagnostic snapshot. A subsequent harness used unsupported PackedByteArray.sha256_text; parse failure and its owner guard remain preserved. Final visual-v4 uses exact byte readback and a clean deferred shutdown. No production save guard changed.

The first normal-process soak harness selected integer `4` using Array.find against `[1.0,2.0,4.0]`; a state probe recorded index -1 and three valid UI buttons. Corrected external selection uses float conversion. Preserve initial/probe failures; they are not game speed-handler failures.

The original mixed-large benchmark replaces production carry-aware Bill with plain `bill_npc.gd`, while retaining carry-aware animation playback. Its first Save fails "Bill carry sequence." An after-failure native snapshot confirms actor script `res://scripts/bill_npc.gd`, absent/empty actor carry_binding, nonempty selected player binding and rejected carry validation. Full diagnostic bytes/context and original error retained under `mixed-diagnostic/`.

An actor-only correction exposed a second old fixture error, "recovered crew": its appended Bill record contained only architect_id/alive, lacking a real pod identity/name/origin. `mixed-roster-diagnostic/` preserves native proof with carry validation now passing. The external `mixed-corrected-v2/` fixture keeps the existing production Bill controller, reveals actual seeded recovery sites using SiteDiscovery, completes Bill's real ward/room before computing the 40-room fill, then uses production release and exact roster bookkeeping. It retains the original dedicated pre-timing core-position normalization and validates the entire captured checkpoint before timing. This is synthetic prepared recovery, not gameplay recovery acceptance; the valid 40-room mix includes that ward and differs from the original invalid fixture. No comparison reuses invalid phase timings. All four v2 runs pass package/checkpoint/Save checks, but visual review catches a further repeatability problem: newly sighted identities move Bill's ward from (18,11) to (16,24) on the warm run, changing fitted zoom from 0.07705 to 0.13081. Retain all four as different valid setup variants, outside the controlled-repeat headline. `mixed-corrected-v3` temporarily marks identities sighted while using the production seeded shuffle, then restores prior scratch knowledge; this makes ward placement independent of warm metadata. All four controlled mixed-only reruns pass, with identical recovery origin (16,24), room composition and initial fitted camera (zoom0.130813953488372, scroll1266/1517). No production actor/save code changed. Normal New Game/Resume saves and eight fresh/reported benchmark saves pass.

## Normal-process soak

Actual package, normal 12-room reported station, 4× real timer/process, normal costs/failures: **600.000681 seconds / 35,977 frames / 120 cycles**, 34 checks, clean Return/Quit, no engine/script errors. All callback-to-callback intervals retained, no filters or retention overflow: mean **16.677 ms**, p95 **16.767**, p99 **17.111**, max **33.314**; **zero ≥50/100/400 ms**. Approximately 60 FPS reflects this normal window's presentation cap and is not the uncapped large-station result or a performance improvement. The existing strict 16.7 ms p95 gate is still slightly missed. No paused/unfocused/report-writer interval-end flags, no comms actions.

Bootstrap before the measured 600 seconds generated one automatic report for a **416 ms** frame at uptime 1.886 seconds; that worker completed before measurement. Report count stayed one throughout measured play. This is not a claim of zero startup stalls or zero reports for the process.

Branforth, Margot and River remain active/alive with 119/115/120 moved observations and 81/63/62 goal changes across 121 observations (initial, 119 periodic, final). Sampled displacement is a lower bound, not a route equivalence oracle. No architect/drone/build-order stuck warning; one economy advice flag reports unaffordable hand/no harvesting, as documented by StuckWatch. Do not treat that advice as a crew bug or suppress normal failure rules.

Texture memory grows from **1,420.403 to 1,564.588 MiB** during early warmup, then remains 1,564.588 through later samples. Floor/contact meshes stay 9/6, retired counts zero. Object count **32,144→33,416** grows during play; cause/retained lifetime is unproven, so this is not a general no-leak certification. Release static-memory and orphan counters returning zero are unavailable evidence. `soak-v2.json` retains every frame, periodic actors/resources/memory/errors and final packaged diagnostic snapshot. This historical ten-minute run is separate from the subsequent two-hour workload below.

## Two-hour normal-process Windows station soak

Same frozen build and exact delivery bytes; new physical QA copy and fresh scratch
profile. **7,200.011813 s / 431,863 frames / 1,440 additional cycles**, cycle 323→1763,
normal 4× timers/process, costs and failure rules. **34 checks pass**, no engine/script
errors, log warnings, safe-image failures, foreign Godot processes or visibility
guard failure. Normal Return-to-Title/Save, writer completion and title Quit
finish cleanly. All **2,948 owner files unchanged**. Delivery manifests (11 files
each) and all 32 unique delivery/QA identities match; game exited and editor 46624
remains. Free C:27.971 GiB / D:142.746 GiB, above the 20 GiB reserve.

Every retained interval is positive, has a matching state flag, and sums exactly
to measured elapsed microseconds; no retention overflow or excluded rows. All
flags are zero, including sampled pause/focus/writer/guard state. Mean **16.672 ms**,
p95 **16.770**, p99 **17.093**, max **35.399**; **zero frames ≥50/100/400 ms**.
This is a 12-room fixed-camera Windows workload, 1600×900 window / 1920×1080 design
viewport with VSync enabled, muted Dummy audio and handler-driven UI. Its
59.981 FPS does not improve or certify the separate 40-room benchmark. No route,
actor, normal survival rule or simulation timing was changed by the observer.

**1,439 periodic observations** plus initial/final state retain crew, resources,
memory, errors and reports. Branforth/Margot/River remain active/alive and show
1,433/1,410/1,440 movement observations and 989/933/816 goal changes respectively.
Other architects remain inactive. No retained crew/drone/order stuck keys; the
economy-advice flag persists. Source checkpoint unchanged. The single automatic
report captures **411 ms at engine uptime 1.974 s, before measurement**; report
count stays one through shutdown. Full frame arrays are authoritative; packaged
monitor history remains separately bounded to its latest 120 buckets/32 hitches.

Texture counter warms **1,420.403→1,564.588 MiB**, then stays flat. Floor/contact
meshes remain 9/6, retired counts zero; Nodes settle at 1,166. **Live object count
continues rising: 32,143→41,740**, including 34,993 at 30 minutes. This is an open
allocation/lifetime concern, not no-leak acceptance. The engine's `OBJECT_COUNT`
reads live ObjectDB entries; its orphan count returns zero without `DEBUG_ENABLED`.
Thus earlier release orphan-zero readings in this report also do not prove absence
of orphan Nodes. [Godot 4.7.2 engine implementation](https://github.com/godotengine/godot/blob/4.7.2-stable/main/performance.cpp#L147).

External Windows memory: **1,440 samples**, maximum gap 5.052 s. Five-minute→last
approximately measured sample: resident **1,061.582→1,127.418 MiB**, private
**2,559.813→2,621.793 MiB**. OS peak working set **1,250.668 MiB**. These include
the game/renderer and growing QA frame/flag/periodic retention; they cannot
attribute allocation growth or establish GPU residency. Value-container retention
affects RAM, but source review finds no confirmed observer mechanism explaining
the live ObjectDB growth. Resource/class/lifetime attribution remains a focused
follow-up. Release static-memory zero remains unavailable evidence.

Evidence: `long-soak/{soak,analysis,completion,owner-guard,final-identities}.json`,
`process-memory.csv`, native/driver logs, runtime/provenance and process guard.
Only external duration/retention, graceful scratch-stop and Windows sampling
helpers changed. Python/ABI preflight, exact offline calculations and independent
read-only review pass. This completes the two-hour station stability lane, not
whole-expedition, broad visual/behavior, physical-input/audio, memory-leak,
target-hardware or public-release acceptance.

## Controlled performance matrix

**12 valid runs / 288 phases / 34,560 frames**, two process repeats per resolution at 1600×900 and 1920×1080, fresh/reported/mixed-large stations, idle/pan/zoom/lighting/placement/demolition/interface/Save at 1×/2×/4×. RTX4070Ti, Compatibility/OpenGL, uncapped fixture. All engine/script/shader errors, warnings, placeholder failures, visibility/input and foreign-process guards clear. Original eight fresh/reported runs and final four `mixed-corrected-v3` runs form the controlled headline. All four variable-setup v2 runs and four invalid diagnostic/setup attempts remain preserved. This is a new baseline, with no before/after optimization claim or transfer of old private results.

| Station | Normal idle FPS | 4× idle FPS | 4× placement-phase FPS |
|---|---:|---:|---:|
| Fresh / 1 room | 190.48–212.44 | 175.48–201.11 | 174.49–188.26 |
| Reported / 12 rooms | 99.84–105.46 | 91.71–100.17 | 91.92–98.36 |
| Mixed / 40 rooms | 43.83–45.82 | 40.45–41.31 | 40.15–40.78 |

Large 4× idle p95 **30.231–31.698 ms**, p99 **43.679–47.956**, max **90.781**. Large 4× zoom **35.65–35.97 FPS**, p95 **38.565–41.412**, p99 **47.285–51.526**, max **53.940**. Placement action frames **54.243/54.931/54.335/54.701 ms** (action calls2.300–2.335 ms); following60 each max **34.030/34.898/33.716/34.206**, zero >50 or >100. Whole placement-phase max54.977 ms; p95 **33.716–34.898**, p99 **49.742–54.931**. No placement/zoom frame >100 in controlled cohort.

Existing per-phase pacing check (p95≤16.7, p99≤25, max≤100) passes **183/288**: fresh96/96, reported87/96, large0/96. All outliers retained: **92 frames >50 ms, six >100, worst117.739**. Every >100 is a synchronous Save action: one reported4×117.739; four large1×100.237–105.750 and one large4×103.586. Save readback/validity succeeds; Save pacing remains a release concern. Four automatic reports occurred in full controlled processes, outside a claim of report-free startup; no run/report rows are deleted.

Observed peak engine texture counters: fresh **1,120.686 MiB**, reported **1,560.218**, large **2,609.003** (2.548 GiB, during zoom); large ending **1,942.395–1,949.271 MiB**. These fit documented ≤2GiB/12-room and ≤3GiB/large texture limits; they are not physical GPU residency, total process memory or indefinite lifetime proof. Ten-minute real-play object growth remains unproven as above.

Fixture scene-request-to-ready cold runs span **9.246–13.218 seconds** and warm runs **4.403–5.627**. Under existing cold/warm≤10/6-second gates (dialogue excluded), cold fails5/6, warm passes6/6. These fields include scene resource loading and loading-screen setup; normal intro/dialogue duration and OS disk-cache state are not controlled. Normal-entry functionality was checked separately.

Raw `phases.csv`, `placements.csv`, `benchmark-analysis.json`, per-run full durations/traces and `analysis.log` retain scope and every value. Traces cover all2,880 measured samples per run; collection time is separate. Deterministic developer workloads manually step simulation, suppress failure/free-build costs and disable comms processing; they are not a real-clock whole-game soak, actual physical input or GPU attribution. Camera coverage counts room rectangles, with HUD occlusion not included. A separate normal-process/timer soak above records real-play progress.

## Read-only triage of remaining Save and startup failures

No candidate changes or new timing runs. `startup-triage.json` extracts the twelve
existing final run records. Cold `interface_and_grid` spans **7.306–9.242 s**,
warm **2.922–3.131 s**; scene-resource loading stays **1.099–1.174 s**. All six
cold runs have zero worker submissions/prefetch hits. Warm runs submit and hit
12,693 (fresh) or 13,287 (reported/mixed) decodes. Their 8.42–9.56 s worker totals
overlap and are not elapsed startup duration. Broad `_build_ui()` stage timing and
uncontrolled OS cache prevent attributing the difference solely to prefetch,
PNG decoding, UI layout or texture uploads. Nested startup stages are already
inside `_ready()` elapsed and must not be added again.

Mixed-large startup first restores the **12-room** checkpoint, then constructs
the synthetic 40-room fixture in a separate **7.48–7.86 s** preparation stage.
The loading gate excludes that preparation; these are not direct 40-room
checkpoint-load timings. Normal entry is separately checked above.

Frozen-source inspection identifies repeated cargo-art fingerprinting as a Save
profiling candidate: `RunSave.capture()` always enters James cargo capture when
the player exposes its floor texture; cargo capture fingerprints the floor and
26 unload/settle textures even for an empty return plan. Pixel retrieval, buffer
copies, hex strings and SHA work accompany deep copies, validation, synchronous
serialization/flush/backups and the later progression save. Their individual
share of the measured 100–118 ms is unproven; GPU readback is not established.
Next candidate investigation: time these stages, then consider caching immutable
art bindings with complete invalidation while capturing live plan/stage state
freshly. Keep this separate from asynchronous F8 report writing and from the
frozen package's acceptance.

## Mac twin and remaining certification

Mac export through the maintained wrapper completed successfully from the exact physical selection. **36,430 runtime entries, expected manifest and build metadata match Windows; PCK bytes are identical**, SHA256 `6b3533d80cc940035c2a86ac36f679e9df69d04360b17febf91e3eac7de1c5d4`. Reuse the complete Windows raw/source audits through byte identity; no redundant PCK rescans. Selected manifest has zero case-fold path collisions. Universal 2 static audit confirms arm64+x86_64, executable ZIP mode100755, bundle identifier `com.shadewater.brinespace`, one PCK and no QA overrides. ZIP **3,544,597,228 bytes**, SHA256 `4f1822c8215cfaeb81a55d17afc081552d83ec37395855f3e5291da0e33f6ab0`.

Mac delivery is `D:/bs-release-qa-20261016/mac/BrineSpace.zip`. The local test export uses ad-hoc signing and is not notarized. Native Apple Silicon/Intel gameplay, physical input/audio, Gatekeeper/signature acceptance and distribution notarization cannot be established on this Windows host. Use the delivery README's separate-test-account checklist; static parity is not native acceptance.

## Isolation and remaining scope

Subsequent owner-requested [storage cleanup](STORAGE_CLEANUP_2026-10-16.md)
recovers 77.802 GiB on C: (now 104.636 GiB free), with D: at 110.252 GiB free.
Both current 11-file delivery checksum manifests pass again; all 2,948 player
files unchanged. Current physical selection and QA copies remain intact. Only
byte-identical old C: test runtime binaries were removed with restoration records;
the closed drone-compiled archive moved intact to D: behind its original-path
junction. Earlier free-space snapshots below are historical.

Owner confirmed they will transfer and run the exact ZIP on their Mac, using the
separate-test-account checklist. Native results remain pending. The configured
XcodeBuildMCP tools expose simulator workflows but no native macOS app workflow;
all session defaults are unset. No Apple build/run or system security setting
change was attempted by this task.

Each Godot/export/test run uses scratch APPDATA and resolved-profile guards before writes. Frozen owner layouts/checkpoint inputs are copied; RunSave restore targets are reset to writable scratch paths. Native windows are visible, muted and input-isolated on secondary screen 2; relevant processes are monitored and timings run serially. Final cross-task comparison verifies **all 2,948 protected owner files identical to the starting baseline**. Native timing guards clear; game exited and only owner editor PID46624 remains.

Final source guard checks **61,620 frozen input files**, including **2,044 unchanged UID files**, with **zero unexpected source changes**. The 46 permitted differences are generated manifest/preset/import metadata from the maintained exporters. Windows/Mac delivery identities rechecked; no QA overrides. Both include README, NOTICE, LICENSE, bundled Barlow/Godot licenses and SHA256SUMS. `final-guards.json` records hashes and final storage reserve: C:28.29GiB, D:147.11GiB, both above20GiB. Authoring generations and prior evidence remain preserved. Changed project files for this task are CURRENT_STATUS, this report and the implementation plan; ignored external QA adapters/evidence are separate from the game.

The earlier [real-profile incident caveat](TEST_PROFILE_INCIDENT_2026-10-15.md) remains. The prior rare 393 ms crew stall remains unresolved; it was observed under a different workload. Current checks do not establish full expedition, broad visual/crew behavior equivalence, physical input/audio, general memory-leak or native Mac/public-distribution acceptance. The two-hour station soak above is complete.

GTX1650-class/M1 target-hardware checks remain unrun. This candidate misses mandatory pacing/cold-load gates, has reproducible >100 ms Save frames and unresolved live-object growth, so it remains a local test candidate. Complete the remaining certification lanes after resolving or explicitly accepting release-gate findings. No minimum hardware specification is established here. The continuation's `long-soak/final-identities.json` supersedes the earlier storage figures above and verifies unchanged delivery/QA files; the earlier full-source guard remains evidence for the physical freeze.
