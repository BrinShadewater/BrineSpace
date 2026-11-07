# Project handoff

Updated: October 9, 2026 · Project: BrineSpace · Task: lossless crew storage on accepted-source candidate

## Objective and acceptance

Reduce retained animation texture memory without changing pixels, clocks, source
bindings, filtering, layering or owner data. Full release gates remain open.
Private startup and pose checks do not certify active-station FPS or saved games.

## Accepted decisions and constraints

Use the exact frozen October 9 candidate, preserve every selected manifest call
and its order, and reuse the previously tested immutable compressed sources and
exclusive presentation leases. No downscaling, art deletion, source selection or
default effects change. Keep normal code and public delivery unchanged until
relevant current-source native/save/frame/memory/lifetime checks pass.

## Current state

Private evidence: `D:/bs-release-20261009/crew-storage-trial/`. Ten individually
hashed helper inputs plus canonical Grid override; Main/scenes/art remain from
the audited full candidate. Grid carries original class declaration in the PCK.
Constructor/adoption changes reuse the original Bill subclass chain and all four
historical dictionaries. Verified Bill inheritance-cache fix and guarded script
draw lease correction included. identity.json proves frozen Grid unchanged and
selected manifest call sequence identical. control.pck adds helpers only;
candidate.pck adds the new Grid. Early bootstrap loads before report/game scripts
and checks the resolved scratch directory before any gameplay writes.

Local drivers: prepare-current-crew-storage.py, run-current-crew-startup.py and
run-current-crew-pixels.py under output/renderdoc-tools-2026-10-08/.

## Verification

Actual debug=false few-room startup pair, terminal session23073: control
3,109.5428 -> candidate1,062.9526 MiB; saving2,046.5901 MiB (~2 GiB). Both settled
exits130.8435 MiB and router released. Candidate compresses1,610,154,592
decoded-equivalent bytes to139,203,414 bytes; this is not retained decoded RAM.
No generated GPU readbacks or missing presentation.33 resolves/2 shown frames/
2 uploads prove actual routing, including an explicit native pose draw. Bill
compression workers peak8; all pending maps/jobs/unused jobs0 at completion.
Request-to-ready10.545/9.488s, single-order/uncontrolled cache, not loading-gate
acceptance. The native startup controls are not title/dialogue certification.

Actual debug=false native pose comparison, terminal session62159:208 exact pixel
pairs/0, equal dimensions/filter/pivot/extent and Bill actual display-cache frame
identity. All208 reference captures nonempty; candidate sample visually reviewed.
Four Bill banks, four crew bare east idle/walk, available Bill/Veld/James helmet
east idle/walk; first/last poses, inherited nearest/linear filters, rect/region
draws and colour modulation. Candidate208 resolves/32 shown frames/missing0.

First fixture incorrectly required helmeted Marsh poses. Current normal player
explicitly returns null for missing equipped coverage. Corrected fixture verifies
matching null for Marsh's idle/walk/swim/tread east helmet requests; **no helmeted
Marsh pixels are claimed**. No fallback or gameplay change. Metadata scope wording
corrected after results without rerunning or changing pixels. Normal source/art
untouched. Each completed lane preserves all2,936 owner files; loader restored
byte-identically. Pixel captures/records are in isolated control/candidate profiles.

## Next action

Actual release restore test completed in both lanes: each passed 24 disk/fresh-scene
restores and 2,189 checks with zero failures. Four Bill bindings x bare/helmet x
entry/settle/rise cover actor/source/clock/root/needs, 30 future steps, actual room
submissions/captures and bare idle/walk display-row/timing checks. Saved records
match across lanes; all 48 before/after source pixel pairs match exactly. Whole-room
captures are not claimed byte-identical because environment animation continues;
one candidate room capture was visually reviewed. Owner 2,936 files unchanged,
loader restored. Evidence: restores/comparison.json.

Matched workload comparison completed, session3147 exit 0: eight actual release runs,
original 12-room and active 40-room stations at 1080p, control/candidate in both
orders, all 24 action/speed phases with 180 measured frames each. All four reported
12-room runs completed. Both orders show identical captured endpoint states across
all 24 phases. Sampled phase texture maxima: control 3,584.138 MiB, candidate
1,537.591 MiB (within the 2 GiB scene budget). Equal-weight phase mean frame times:
forward 15.740/15.911 ms, reverse 15.562/15.639 ms, control/candidate. Frames >50 ms:
8/8 forward, 7/6 reverse; none >100 ms. Combined phase gate passes: 6/5 forward,
7/8 reverse, out of 24 per lane. This is a memory improvement with small measured
frame-time overhead, not full FPS acceptance or statistical regression clearance.
First active 40-room pair complete: identical captured state in all 24 phases,
sampled texture maxima 4,834.388 -> 2,787.884 MiB (below the 3 GiB budget). Equal-
weight phase means 29.891 -> 32.425 ms; >50 ms frames 202 -> 350; >100 ms frames
10 -> 13; max 159.411 -> 167.522 ms. Both lanes pass zero full phase gates. At 1x,
idle/pan/zoom improve while several later actions worsen; no single-hotspot cause
or admission is established. Reverse-order large pair: phase means 28.904 ->
31.010 ms; >50 ms frames 181 -> 226; >100 ms frames 7 -> 8; maximum 153.666 ->
168.325 ms, zero full phase gates. Identical state and texture maxima repeat.
Across all four matched pairs, all 96 phase-end captured states are identical;
34,560 frames measured. All eight lanes have zero logged errors, and candidate
missing presentation/spill peak are zero. Owner 2,936 files unchanged, loader
restored byte-identically. Evidence: workload-comparison/{completed,paired-analysis,owner}.json.
The large-station frame regression repeats in both orders and blocks admission.
Driver run-current-crew-restores.py; evidence restores/{control,candidate}/ plus
identity.json. Original8case fixture adapted to current canonical Main/overlay,
explicit debug=false, deterministic site seed, observed destruction before fresh
Main, and expanded24case phase coverage. Namespace/captures derive from current
driver, not an older absolute test. Root delivery/frozen source remain unchanged.

Attribute the repeated large-station regression to actual component costs before
selecting a remedy; memory-budget success alone is insufficient for admission.
Measure render-boundary peaks and repeated scene exits/transitions before normal
admission. Keep immutable/generated images independent and native-class lease
fallback intact. Original FPS/stalls/loading/endurance/nine issues/target hardware/
native Mac/Developer ID/notarization/delivery requirements remain unresolved.

Prepared next fixture: output/renderdoc-tools-2026-10-08/run-current-crew-lifetime.py.
Python syntax compilation passed; native execution completed, session2336 exit 0. It refuses
to run before the workload batch completes and its owner fingerprint is clean. Ten
paused original-station production disk checkpoint/fresh-Main restores per lane,
observable scene destruction, router cleanup, render-boundary memory sampling and
settled crew/rooms/drone/hardware/companion equality. This does not substitute for
actual title-menu Continue, active endurance or physical VRAM peak certification.

Both lanes pass all ten restores: control settled 3,399.208 MiB, candidate
1,352.446 MiB in every cycle (zero measured growth). All cycle exit values and final
exits are 135.222 MiB, router released, restored selected state identical within
each lane. Render-boundary maxima equal settled values; 547/551 samples and maximum
probe overhead 18/9 microseconds, control/candidate. Owner 2,936 unchanged and
loader restored; evidence lifetime/{results,owner}.json. This paused 12-room test
does not certify large-station endurance, full process-memory growth or title menus.

Source audit also found slots.gd retains every upload duration in upload_usec for
the whole session. No current trial consumer reads this array. Bound diagnostic
history before production integration; do not change live comparison inputs.
Timing presently starts after bank.source_image, so reported upload durations omit
ZSTD decoding. The reverse-order data confirms a regression; separately attribute
decode, presenter lookup/lease and GPU submission before choosing a remedy.

Prepared separate attribution sources at presenter-attribution/ from the exact
tested slots.gd; original/private/live comparison pack inputs unchanged. Fixed-size
aggregate counters replace upload_usec history and separately time source image
decoding and GPU API submission. Added phase-end snapshots and warm-up drain; no
GPU-execution or exact current-frame alignment claim. Local prepare/run drivers:
output/renderdoc-tools-2026-10-08/{prepare,run}-current-crew-attribution.py.
Python compilation passed. First native diagnostic failed before useful workload:
new aggregate methods used spaces, original slot methods used tabs; direct script
parse identified mixed indentation at slots.gd:41. Failed pack/source/logs retained
under presenter-attribution/failure-1. Normal source and original trial unchanged;
owner 2,936 unchanged and loader restored after failure. Preparation now normalizes
new indentation to tabs; direct headless script instantiation and empty aggregate
snapshot pass. This checker initially timed out after trying to instantiate the
invalid script; it now checks can_instantiate before new. No FPS evidence from these
setup attempts. Corrected actual native attribution was restarted after terminal
failure, with isolated profile and original inputs; session56336 completed exit 0.
All 24 instrumented phase-end states equal the prior reverse candidate. 3,748
decodes total 477,262 microseconds; submission API wall total 187,563 microseconds.
Equal-weight averages: 0.1105 ms/frame decode, 0.0434 ms/frame submission. These
direct CPU costs do not explain the prior 2.1-2.5 ms frame delta; deferred renderer/
GPU consequences remain unproven. Instrumented phase mean is 29.458 ms (versus
31.010 ms in earlier reverse candidate), underscoring run variability; this is not
a matched improvement or a causal acceptance of bounded history. Owner 2,936
unchanged, loader restored. Evidence presenter-attribution/{analysis,owner}.json.

Next private hypothesis: recurring poses are repeatedly decoded/uploaded in a
four-slot presenter (3,748 decodes despite 632 distinct shown frame objects in the
previous matched run). Prepared pose-cache/slots.gd keeps up to 128 recent immutable
GPU poses under a 64 MiB source-image byte limit, evicts only unleased least-recent
entries, preserves held canvas commands and uses independent temporary spill for
oversized/all-held working sets. No pixels/frames/timing/filter/selection change.
This targets redundant uploads; it is not a proven explanation of the entire delta.

Native release manual lease/cache check: 18 checks/0 failures. Covers byte and
entry limits, immutable evicted GPU texture bytes, retained second-owner pixels,
repeat hit without upload, oversize/all-held overflow, spill cleanup, metadata/
filter and final resource release. Owner unchanged, loader restored. Evidence
pose-cache/{lease-result,lease-owner}.json. Manual lease checks do not certify
actual canvas routing/motion/FPS. Native 208-pose normal/candidate comparison
completed, session1964 exit 0: 208 exact pairs, matching metadata/filter/selection,
four unavailable Marsh equipped requests retain null, missing presentation zero.
Actual candidate capacity 128, resident source-byte equivalent 5,093,888 below
67,108,864 budget, 32 shown frames/208 resolutions. Owner unchanged and loader
restored. Evidence pose-cache/{pixel-results,pixels-owner,pack-owner}.json.

New matched normal-control/pose-cache comparison completed, session6834 exit 0: both orders,
original 12-room and active 40-room, all 24 action/speed phases x 180 frames each.
Separate evidence pose-cache/workload-comparison/. Uses identical frozen gameplay,
additive bounded phase diagnostics, explicit actual cache/provider budget check.
All four 12-room lanes now complete: both orders have identical captured state
across all 24 phases. Equal-weight frame means control/cache 15.316/15.148 ms
forward and 15.608/15.169 ms reverse; combined phase gate passes 10/13 and 8/13.
Frames >50 ms 7/6 and 9/6; none >100 ms. Worst cache frames 64.113/68.758 ms,
versus control 87.370/62.695 ms. Sampled texture maxima 3,584.138/1,559.233 MiB;
cache remains below 2 GiB. Both cache runs: 1,351 phase decodes, 2,969 cache hits
of 4,320 acquisitions; lifetime uploads 1,463, down from the prior four-slot
provider's 3,714 in this fixture. The latter is a mechanism comparison across
separate batches, not a matched old-provider FPS gain. Resident cached source
bytes peak 17,334,272 and slots 128, below the 64 MiB budget. Missing/spill peak
zero. Large comparisons remain live; full FPS acceptance is still absent.
First large pair complete: captured state identical in all 24 phases. Control/cache
equal-weight mean 30.685/28.954 ms; >50 ms frames 218/179, >100 ms 9/7, worst
171.996/154.440 ms. Both pass zero full phase gates. Sampled texture peaks
4,834.388/2,809.483 MiB; cache remains below 3 GiB. Candidate 1,191 phase decodes,
3,146 cache hits of 4,337 acquisitions; lifetime uploads 1,300 versus the earlier
four-slot fixture's 3,930 (cross-batch mechanism evidence, not matched FPS gain).
Resident source-byte cache peak 17,334,272, missing/spill peak zero. Reverse large
pair: control/cache mean 30.405/28.982 ms, >50 ms frames 212/177, >100 ms 6/6,
worst 193.449/156.096 ms; zero full FPS phase gates. All 96 paired captured states
match across eight runs and 34,560 measured frames. Texture/cache counts repeat;
zero logged errors, owner 2,936 unchanged, loader restored byte-identically.
Cache improves large mean 1.4-1.7 ms in both orders; target-hardware/statistical
certification and 60 FPS gates remain open. No normal admission yet. Evidence:
pose-cache/workload-comparison/{completed,paired-analysis,owner}.json.
Prior historical restore/lifetime checks cover the earlier four-slot provider;
new cache still needs its relevant current-source restore/lifetime checks before
normal admission. Do not overlap GPU tests or
restart a live handle on an observation timeout. Local prepare/run drivers
are output/renderdoc-tools-2026-10-08/*current*pose-cache*.py. Normal source,
audited Windows/Mac delivery and original tested trial remain unchanged.

Prepared cache-specific four-binding disk restore wrapper:
output/renderdoc-tools-2026-10-08/run-current-pose-cache-restores.py. It refuses
execution until the matched workload batch and owner fingerprint finish cleanly;
reuses the identified 24-case fixture with explicit actual cache-capacity checks
and separate output identities. First native attempt session93660 stopped after
three successful control cases: handle missing and no matching OS process, no
terminal result/owner-final record; interruption cause unknown. Preserved full
partial case directory, identity and scratch-profile pointer under
restores-interrupted-01/. Restored the guarded bootstrap's original storage-probe
path. Current owner count is 2,936; no interrupted-lane before/after equality claim.
Fresh full pair completed, session54004 exit 0, in new isolated profiles.
Control passes 24 restores/2,189 checks; cache passes 24 restores/2,214 checks,
both zero failures. Exact saved records and all 48 before/after source-pixel pairs
match. Within-lane future trajectory/needs/timer/source checks pass; owner 2,936
unchanged and guarded loader restored. Cache sample binding-3-bare-rise-after-room
visually reviewed: Bill visible near the left workbench under the water overlay,
room props and compact needs meters present; card hand obscures lower room. No
whole-room byte parity, full motion, original nine-bug or title-Continue acceptance
from this one still. Evidence pose-cache/restores/{results,comparison,owner}.json.
Restore comparison utility now accepts --evidence and requires complete
lane results plus clean final owner fingerprint; Python compilation passed.
Future wrapper invocations now persist owner-before.json as well as final changes;
Python compilation passed. This edit does not change the already-running driver,
so no persisted pre-run fingerprint is claimed for session54004.
Do not restart on observation timeout; inspect the same handle. Studio source audit
finds RoomLayoutEditor uses its own RoomScaleCast/
RoomScalePreview players, not a second GridCanvas/router; opening/closing Studio
still requires native UI/pause/memory acceptance, not inference from this audit.

Prepared cache-specific ten-restore lifetime wrapper:
output/renderdoc-tools-2026-10-08/run-current-pose-cache-lifetime.py. Requires the
new 24-case restore pair and clean owner fingerprint first, then uses isolated
production disk/fresh-Main restore cycles and actual capacity/byte-budget guards.
Python syntax compilation passed; actual native execution completed, session99623
exit0. Both lanes pass ten restores with exact selected state and released router.
Control settled3,399.208 MiB every cycle; cache1,352.446->max1,352.583->1,352.546
MiB, flat final five samples (~0.010% span). Cache exits135.222->135.322 MiB from
cycle5 and then flat; control135.222. Small settled/exit rise is recorded, not zero
growth claimed; below5% criterion and no sustained final growth. Render-boundary
maximum matches cache max; 545/550 samples, probe maxima21/9us, control/cache.
Owner2,936 unchanged, loader restored. Evidence pose-cache/lifetime/{results,owner}.json.
These paused12room texture-accounting checks do not certify physical/process
memory, actual title menus or two-hour active large-station endurance.

Prepared integration-stage/ with 11 tested files under full production resource
paths (scripts/crew_storage/*.gd plus Grid). Transformation is reversible exactly
to tested source after path relocation; selected manifest sequence unchanged.
Normal Grid still matches frozen SHA and its UID hash is recorded. No checkout,
audited delivery or owner-data edits. New helper UIDs, imports, normal-source
native/regression checks and rebuilt candidate certification remain pending after
cache compatibility/lifetime admission. Local stage-current-crew-storage-integration.py.

## Normal source integration — current milestone

After cache-specific compatibility/lifetime completion, installed the 11 staged
files by exact production-path relocation. Normal scripts/crew_storage/ now has
the ten tested helpers; Grid constructors/adoption and Bill inheritance-cache
guard use those full paths. Original Grid UID is unchanged. Backup, installation
hashes and owner-before fingerprint retained in pose-cache/normal-integration/.
Owner 2,936 unchanged on installation. No art, manifest, gameplay, settings or
audited delivery edits. This optimization admission is not release certification.

Godot editor import session40683 ended at600s timeout during older PNG indexing,
without script errors logged; full import is not accepted. All ten new helper
UIDs generated, installed source hashes unchanged, original Grid UID preserved.
Targeted normal script loading/compilation passes all11 installed scripts with
zero errors and11 distinct paired UIDs; owner2,936 unchanged. Evidence
normal-integration/{parse-installed-result,parse-installed-owner,import-owner}.json.
Existing archive duplicate-UID warning is recorded, not repaired by deleting or
regenerating archived source. Relevant normal-source regressions are live47383:
headless feet cache/checkpoint isolation/performance monitor/draw-profiler lifetime,
then native texture pool/batch. Session47383 completed exit0, all six pass;
native batch76/pool46 checks. Owner2,936 unchanged. Maintained tests/test_crew_pose_cache.gd
registered in performance-diagnostics with paired engine-generated UID and native
lane override (automatic heuristic first skipped it as headless-safe; no false
pass claimed). Actual native lane then passes. Scratch resolved profile verified
before tests, owner pre-fingerprint persisted. Normal-entry gameplay,
actual normal-entry gameplay and rebuilt/frozen PC/Mac inputs remain required.
Maintained native lease/cache regression is staged separately as
normal-integration/test_crew_pose_cache.gd; checkout registration pending import
completion. The staged test is now installed/paired and passed as noted above.
Full 60FPS/stalls/loading/bugs/soak/platform/signing gates stay open.

Installed-source native gallery completed session22957:208 exact supported pose
pairs and matching metadata/filtering vs prior original release control, actual
production Bill/Router path,128capacity/64MiB budget, missing0 and 32 shown frames.
This is debug=true QA/editor engine with no PCK override; not a packaged-release
claim. First attempted QA run correctly rejected debug mode; a copied actual
release executable then rejected --path because path overrides are disabled.
Both setup logs/owner records retained. Explicit editor-source mode separately
passes, owner2,936 unchanged. Evidence normal-integration/installed-pixels/{result,owner}.json.
Actual debug=false verification requires a maintained export from newly frozen
inputs. Existing Windows/Mac candidate remains the earlier source; do not call it
the installed optimization's release package.
