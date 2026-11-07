# iPad QA, performance evidence and workspace retention

Use this for BrineSpace physical-iPad validation and native renderer experiments.
Start with CURRENT_STATUS.md for the accepted build/rollback and remaining gates.
Dated reports preserve evidence; they are not a queue to repeat blindly.

## Protect the owner and identify the candidate

- Keep source checkouts, original art, Git/LFS data, Studio marks, frozen releases,
  published Mac/Windows packages and the current/rollback iPad builds intact.
  The monitor checkout is read/fetch only. Use the active validation checkout.
- Record branch/HEAD **and** dirty source fingerprint, selected manifest, PCK and
  signed-executable hashes. An installed dirty build is not identified by HEAD.
- Query the connected device and exact bundle/container. Read a fresh launch result
  and match the current executable before attaching or stopping its PID. Do not
  fall back to an old hardcoded container or terminate every similarly named app.
- Save through the actual UI before changing a device fixture. Stop only the
  identified validation app, back up Documents outside the repo, and hash all five:
  `brine_loop.save`, `brine_loop.save.bak`, `brine_loop.save.comms.json`,
  `brine_save.json`, `brine_save.json.bak`. Take a new backup if play resumed.
- Before replacing an existing installation, verify the new package first. After
  installation, compare all five files before launch. Preserve sidecars and meta
  progression as well as the loop file. A disposable fixture can modify those too.

## Isolate tests and preserve the actual artwork

Run Godot probes with scratch APPDATA/HOME/XDG paths and the project's pinned
user directory; HOME alone is insufficient. Set the expected-profile guard used
by the specific runtime, and fingerprint the real owner directory before/after.
Use a fresh per-batch scratch identifier for repeat test runs. Prepared-cache write fixtures use fixed keys and are not idempotent against an earlier populated test home. Wrap each native batch in a real-owner fingerprint guard with a finally check, including failures.

A restored checkpoint retargets `run_save_path`: reset it to a scratch destination.
Keep `.gd` and `.uid` paired and use complete quoted resource paths.

For cache changes, test both load orders, direct replacement, source revisions,
all relevant rotations, overlapping owners, last-owner release and scene reentry.
A second cache alias can keep a texture alive after the nominal cache was cleared.
Keep processing in cache keys: raw/revised/graded/mirrored sources are not
interchangeable merely because filenames or dimensions resemble each other.

Use a native red/green regression plus source/viewport comparisons. Then audit
selected assets/scripts in the exact PCK and verify the signed bundle uses that
PCK. Keep native/editor, exact-pack and actual-iPad acceptance separate.

### Prepared crew cache working sets

When crew loading dominates `interface_and_grid`, record per-actor manifest,
finish/adoption times and PNG/cache-hit counters before changing UI layout.
Check both file count and bytes in the device index. A sequential working set
larger than the LRU file ceiling can rebuild every frame on each load even when
the byte budget has spare capacity. The current four-bank fixture needs 8,262
prepared files; the file ceiling is 16,384, with the independent 192 MiB byte
budget, 2 MiB index, per-entry validation and four-job decoding window unchanged.
Run the capacity/index/worker/write regressions against the actual PCK, then
verify zero rebuilds on both repeat and fresh-process loads. OS cache eviction
still requires preparation; do not describe cached gains as empty-cache gains
or a larger disk metadata limit as a demonstrated RAM reduction.

Display-metadata helpers can be called from navigation preparation. Check whether
an empty/recovered container invokes a lazy actor getter even though rendering
uses only its housing. Prove both no-bank demand and exact pixels, including
roster-owned occupants, before accepting a lazy-loading shortcut. Distinguish
compressed source payload avoided from real process-footprint changes; active
actors may still require the same bank elsewhere.

When USB/HouseArrest telemetry cannot find the device, first check whether the
existing network devicectl and touch-helper connections remain healthy. Reuse
them for passive file copies; do not restart an authorized helper solely because
usbmux is absent. Keep PID/epoch filters and stale-sample guards, and record the
transport and interrupted test scope.

Navigation cache storage changes must preserve exact ordered graph records and
paths, not just point/edge counts. Compare fresh/warm, staged and revision rebuilds,
room rotations and lock policy. Canonical packed edges avoid retaining thousands
of nested pair Arrays and a second representation. Keep each mutable AStar graph
actor-local. Report native allocator releases separately from actual device
footprint; a small CPU reduction does not establish faster GPU redraw or startup.

Native project runners should refuse launch while the exporter-generated native_optimization_guard.gd exists; use an immutable-PCK runner or wait for the export finally-restore. The runtime profile guard remains a second barrier, not the way to discover overlapping export/test jobs.

Variant registrations may select different regions of one immutable PNG sheet. Inventory source paths and actual texture identities before compressing artwork: cache by canonical source when processing is identical, preserve every region registration, and avoid a second strong alias that survives last-owner cleanup. Verify composed native pixels under nearest/linear filters, reverse load order, overlapping owners, release and reentry. Direct-scene probes and full title-to-station runs can load different variant sets; confirm counts/capacities on the physical device and keep them separate from total process RAM.

## Reuse the touch helper and observe UI state

The local helper currently supports a four-hour session. Check its recorded duration
and authorization state. Its process/log/current game identity live in
`/Users/Shared/BrineSpace-ipad-touch-control/session-state.json`. Reuse a healthy
session across tests and installs. Run one controller at a time. Do not restart
for each check or automatically stop it after a short successful test.

If the session expires, confirm the prior runner exited before starting one
replacement. Apple may require Touch ID/passcode on the iPad. Ask while the owner
is ready, respect that prompt, and wait for a fresh command acknowledgment; a
chat reply or xcodebuild startup alone does not prove the helper connected.
Never collect the passcode or promise authorization can be bypassed.
A packaged in-app QA workload may still run through its documented fixture path
while XCTest is unavailable. Back up the owner first, verify the opt-in marker is
removed afterward, and restore all five files. Such direct-method tests establish
only their recorded workload; they do not certify physical touch or Save/Continue UI.

Use a fresh screenshot/OCR or accessibility state before acting. Wait for the
expected station cycle and visible paused/resume state, not a fixed scene delay
or the iOS launch snapshot. Scroll menus to offscreen controls. The Report dialog
can focus its note field and open the system keyboard: dismiss that keyboard to
reach Save Report, and verify REPORT SAVED. Do not select Send without permission.
Command acknowledgment does not prove a pinch, pan or two-finger gesture changed
in-game state. Record their observed effect or leave that acceptance open.

## Measure one question at a time

1. Freeze a checkpoint, layouts, viewport, zoom, speed, actor conditions and cache
   state. Use the same candidate and workload for comparisons. Record normal costs,
   resource caps, hazards and fixture-only seed/flags. Footprint-valid placement
   does not prove door connectivity or a reachable breathable refuge.
2. Separate first/cold load, repeat load, scene teardown/reentry and fresh-process
   Continue. A warm improvement is not a first-load improvement. Keep timer/speed
   behavior explicit; the current Continue reset to1× is an existing limitation.
3. Separate native texture accounting, decoded/packed CPU bytes and real process
   footprint. Use the device sampler or a valid system recording for the latter.
   An overflow-like backend counter is invalid evidence, not huge memory usage.
4. Use separate short profiler recordings for active rendering and loading. Name
   the device, bundle, PID, build, template, interval and recorder overhead. Attach
   the exact target where supported. If PID attachment fails despite fresh process
   confirmation, record that failure; a short diagnostic all-process fallback must
   be filtered to the exact target and its raw data kept outside the repository.
   Bound collection/finalization; preserve a failed/partial trace
   without claiming it completed. Never terminate unrelated recorders or the game
   merely because a trace is slow to finalize.
5. Export/inspect real CPU samples/call stacks or GPU events before attributing a
   bottleneck. Profiler overhead and GPU waiting can affect observed frame time;
   a trace is attribution evidence, not an uninstrumented benchmark.
6. For clean soaks, keep profilers off, sample real memory continuously and record
   cycle advance, active/paused state, errors and survival. A latest one-second
   frame bucket sampled every30 seconds is **not** a full-run FPS distribution.
   Retain slow frames; exclude suspension only with lifecycle evidence. For rolling telemetry files, retain monotonically new samples across truncation. Use bounded chunk reads and limited transient retries when copying a live AFC file; do not discard the earlier history after wrap.
7. The manual report retains only32recent hitch entries. Loading and paused
   rendering can evict earlier transition frames. For per-transition comparisons,
   save/copy a report immediately after each transition; never equate five
   successful UI cycles with five retained timing measurements.

Keep pixel-exact art optimizations separate from renderer-backend trials. A Metal
candidate needs its own artifact/identity, real iPad RAM and loading evidence,
visual review of UI/fonts/cards, four room rotations, alpha/layering/flooding,
and play/save/lifecycle checks. Native Mac speedups do not qualify the iPad.
Do not replace the tested baseline solely on a promising native benchmark.

## Restore and finish

After disposable testing, restore all five files and verify their hashes before
owner launch. Check Save → title → Continue → Save while paused. Compare the full
saved gameplay state, resources/cards/crew and exact timer against the backup.
Restore the original speed while paused if the known1× reset occurs. Timestamps,
event history and camera/scroll metadata can differ after actual UI use; do not
claim whole-file identity afterward. Leave the station paused/menu closed and
update local session state. Intentional process stops can produce a later
"last session did not close normally" overlay; distinguish that from a real crash.

Record limitations without promoting narrower evidence: a one-crew synthetic
soak, headless survival test, fewer texture bytes or successful signing does not
establish organic multi-crew play, leak clearance, smooth placement or release
readiness. Update the current-status summary and a dated handoff; put compact
portable evidence in docs and keep saves/raw captures outside the repository.

## Keep workspace growth bounded

Retain the current signed export/app, one deliberate rollback, frozen deliveries
and every donor used by a recovery archive. Before another large export, inventory
older QA packages and record a retention decision. Archive superseded PCK copies
with exact hashes and verified full-byte reconstruction before removing them.
Retain binaries/signing data, source snapshots, manifests, logs, screenshots,
rejected evidence and saves; mark the historical app as needing pack restoration.
A delta archive is recoverable only while its named donor remains unchanged.

Generated crew caches under obsolete scratch homes and inactive Xcode
intermediates can be removed after exact enumeration and save protection. Keep
current/rollback/helper build products and active caches. Do not delete an entire
output tree, Git/LFS storage or unique art. Log each removed path and failures.
Measure available disk space as well as logical bytes: APFS sharing and concurrent
system changes mean those numbers differ. Keep recovery instructions beside the
archives, not only in chat. Cleanup is scoped to the current owner authorization.

Byte-identical old report/capture copies may be consolidated with hard links only
within an enumerated inactive QA scope. Hash both files before linking, preserve
every original path and all unique content, and record the mapping. Logical
bytes consolidated do not directly establish physical free space.

An input-disabled synthetic workload cannot dismiss a recovery modal. After
verifying and intentionally stopping its exact validation process, preserve then
clear only that stop's generated session lock before launching the disposable
fixture. Never use this to hide unexpected crashes or change game recovery code.
Derive the fixture's expected cycle from its save; do not assume it matches the
owner checkpoint. Exclude setup failures and backgrounded runs from performance
acceptance, and retain their evidence.

When checking editor eagerness, inspect the editor instance's own texture field
before demanding it through a getter. A shared cache warmed by a desktop fixture
cannot independently prove editor behavior. Retain desktop sharing assertions.

A decoder-policy change can pass source/pixel/worker tests without improving the
physical redraw. Compare actual retained frame buckets as well as loading-stage
boundaries; a covered-phase interval also includes frame scheduling. Revert a
candidate with no useful device gain and preserve its rejected evidence. The
recent hitch list may evict initial loading frames; retained one-second buckets
can still contain them.

For duration-focused normal-rule soaks, record the speed, initial fixture reserves,
active/paused samples and terminal reason. A slower ordinary speed can permit a
longer observation; it does not replace faster-speed stress coverage. Normal crew
death ends that run: report the incomplete duration, never disable failures or
replenish mid-run to claim the target was completed.

When investigating runtime growth, align periodic `runtime_caches` counters with
process-footprint samples and station events. Crew source-reference counts and
compressed-byte inventories can jump when a previously deferred actor bank loads;
that is different from a bank growing repeatedly. The decoded-source inventory is
a virtual pixel total, not resident memory. Drone cache bookkeeping also omits
some ownership such as retained original PNG buffers; do not add overlapping
CPU/GPU counters or treat them as a whole-process allocation graph. Compare later
active windows after warm-up, and capture title cleanup separately after the soak.

Register native texture/pixel fixtures explicitly in `tests/index.json` when the
runner's heuristic cannot identify their lane. A headless-exit guard alone does
not classify a fixture as native. Verify `tools/run_tests.py --list` using the
bundled Python 3.12 interpreter, and include the test against the actual PCK.

Before exporting a roughly4GB iPad pack, keep at least7GiB physically free on the
output volume; the maintained exporter now checks this before changing its preset
or writing output. APFS-cloned packs can make logical directory sizes misleading:
removing an archived copy may reclaim little while another clone retains blocks.
Use actual free-space readings, not the sum of logical file sizes. A failed export
must keep its logs, remove only its incomplete pack and verify all temporary source
configs against their saved bytes before any retry.

Recovery archives can depend on another archived donor. Preserve the complete
root donor and document the restoration order; validate dependency hashes before
cleanup. Old UI evidence may be archived only after every archived file is checked
against its original SHA256. Current session actions, saves and frozen releases
remain excluded. A completed app installer cache is disposable only after checking
that the installed app is the same version and its files match.

The next helper build now supports four hours (14,400seconds,14,700second
execution allowance), in `DerivedData-four-hour`. Helpers compiled before this change
retain their original two-hour deadline; rebuilding does not extend an
already-running session. Start the replacement only after the current runner
ends. Apple authentication, when requested, still requires the owner directly
on the iPad; a longer session does not bypass that requirement.


For asynchronous opening-image staging, preserve Control visibility and layout.
Hold drawing with an explicit flag; hiding the grid can alter ScrollContainer
geometry and invalidate a viewport comparison. Test the real main-scene startup,
including process-mode restoration, the exact paused timer and released worker
buffers, as well as a unit fixture. Validate pending image headers once before
servicing the queue. Report loading-stage time separately from retained redraw
frames: moving work under the loading cover can shorten a redraw pause while
increasing setup time, and overlapping intervals must not be summed.


### Physical-device installation cache

Repeated physical iPad installs can retain full historical app copies in
`~/Library/Containers/com.apple.CoreDevice.CoreDeviceService/Data/Library/Caches/AppInstallationBinaryDeltas`.
On October 20, 2026, 57 BrineSpace installation entries occupied about 223.5 GB
of allocated storage. Removing 55 obsolete entries while retaining the newest
Validation 2 and XCTest helper entries recovered 202.5 GB of actual free space.
This was host installation storage, not the iPad app's runtime memory.

Check this cache's size before/after a series of physical-device installs and
before another package when disk space falls unexpectedly. Within authorized
cleanup, inventory exact app IDs, entry paths, file sizes and dates; ensure no
install/build is active and no cache entry is open. Retain the newest current app
and helper entries. Remove only enumerated obsolete entries for this project;
never remove the CoreDevice container, pairing data, installed app Documents,
source, save backups, current/rollback packages or recovery donors. Preserve a
small metadata inventory and record measured disk free space before/after.
Do not add an unattended deletion job or broaden Full Disk Access for this check.
Temporary privacy permissions should be revoked after an authorized audit.
Local audit/receipt: `/Users/Shared/BrineSpace-workspace-cleanup-20261019-consolidation/coredevice-install-cache-cleanup-20261020.json`.

### Opt-in VM category snapshots in the validation sampler

The validation-only native sampler supports an explicit `Documents/qa_vm_snapshot.request`
marker. It consumes the marker and atomically writes `qa_vm_snapshot.json`, with
PID, epoch, walk completeness, elapsed time, process physical footprint and VM tag
aggregates. Collect a fresh result matching the current candidate PID and request
time. It reports no region addresses, mapped filenames, stacks or memory contents.
The normal 1 Hz sampler does not walk regions without a request. The walk is
bounded to 65,536 leaf regions, 64 submap levels and a cooperative 500 ms check
between kernel calls; distinguish a partial result from a completed walk.

VM resident/dirty page aggregates may alias and do not equal charged physical
footprint or GPU texture ownership. Keep them separate from process footprint,
engine texture counters and virtual decoded-image totals. Requested walks are
diagnostic work and delay the next periodic sample; exclude those intervals from
performance comparisons. Confirm marker consumption before ending the diagnostic.
This capability belongs to the separate validation wrapper, not frozen or public
Mac/Windows releases. Record native sampler and signed executable hashes as well
as the PCK/source build ID, since the wrapper may change independently of the PCK.

## Derived GPU texture trials

Keep original artwork and desktop behavior. Compress offline with the verified editor;
exported builds cannot be assumed to include texture encoders. Preserve logical
image dimensions after block padding, mip policy, processing and UVs. Gate RGB and
alpha error separately, inspect magnified/in-game rendering, and keep rejected or
unsupported formats on the original source path. Query the actual renderer and
record that the derived path was served on the device; a Mac software fallback is
not GPU-memory evidence.

Binary Image `.res` dependencies need both manifest selection and selected-resource
export support. Keep them in Git LFS, verify source/derived hashes before export,
and hash all derived bytes in the actual PCK. The raster audit alone does not
cover binary Image resources. Keep the loader free of global Image/Texture owners;
consume or drain superseded staged PNG jobs and test final-session release.

Use the same checkpoint and camera for memory comparisons. A Save/Title/Continue
replay may restore its changed zoom and is a separate workload. A same-package
reference flag helps separate the texture policy from installation/cache effects.
Mapped driver categories can alias and are not additive to process footprint.
If a touch assertion expects an empty inspector, distinguish placement selection
from a retained preview/hover: verify serialized selected_card_id, hand, rooms and
resources when the visible placement controls have cleared.

Door source sharing: preserve independent skin/progress/tint state. Borrow immutable uploads only through the existing per-style lookups so last-owner cleanup releases every alias; no hidden strong cache. Validate exact composed pixels and reversed load order. Count unique resource identities, not alias dictionary entries. Same-package flag: `--reference-door-source-sharing`.

Staged graph optimization: measure checkpoint copy/apply/crew/finish separately and record per-actor build/yield time. Preserve 4ms yield/cancellation policy, live fire/door checks and irregular-shape fallbacks. Exact weighted graph/connection/lookup order and chosen routes are acceptance gates; performance counters alone are insufficient. Isolate static room_cache for both oracle and candidate. Geometry-only grids must return their owning fixture game. Reconnected baseline: resume capture; never rerun baseline saving over original backups.

For navigation broad phases, prove the exact geometric domain before filtering: the current staged authored links stay in one fixed lattice row or reach its next row. Keep the half-open narrow sweep and all corridor/legacy/live-policy fallbacks. Compare ordered weighted graphs and exact paths, not just counts; keep temporary blockers outside shared caches. Separate reduced candidate checks, CPU/yield time, whole loading and physical RAM.


### Empty audit roots and bounded first-redraw capture

Pack audits must mount into a newly created empty directory, distinct from native
fixture working directories. Fixtures may legitimately write screenshots to their
local `output` folder; Godot directory enumeration merges loose files with a mounted
PCK, so reusing that root can falsely label an old screenshot as a packaged asset.
Retain the failing audit, diagnose the source and rerun against the same package
from a clean root. Do not remove assets or weaken the unexpected-source gate.

Record setup, covered layout/render completion and the first five uncovered
frame-post-draw intervals separately. Cancel on scene replacement, bound the rows,
and avoid retaining scenes or textures. These signal/CPU intervals are not GPU
execution timings. Grid draw counters are since the monitor last read them, may
include several canvases and may overlap stage counters; do not sum them blindly.
Hidden crew canvas retirement must clear retained commands before releasing image
leases, request redraw on reveal and preserve visible peers; test ancestor hide,
direct hide, actual immutable-slot eviction and exact reveal pixels.


## Animation-storage strategy acceptance

Include ordinary fractional zooms (for example0.137,0.29672727 and0.73), fractional positions, cropped source rectangles, transpose, inherited filters and UV-dependent materials. A page can pass0.5/1/1.5scales and still fail broader equivalence. Record the first failing matrix and keep it out of the playable build; a lower uploaded-pixel total alone is not acceptance. Preserve original full-frame metadata, dimensions, UVs and checkpoint signatures.

For cache comparisons, normalize uploads by pose requests and record actual active time separately from comms/menu pauses. Advance test comms through the existing Next action; record those actions. A wall-clock run that spends most of its duration paused is not an active soak. Use fresh results/PIDs, both run orders, matched fixture/camera, and sample windows excluding scene teardown. Eight active minutes across short runs does not replace long-soak or memory-growth acceptance.

On this iOS wrapper, SceneTree.quit() can leave the native application process alive after the Godot result is written. A console client may continue waiting. Verify the exact probe PID/executable against its installed bundle, collect results/native samples, then deliberately stop only that PID. Retain the stop receipt; console exit1 after that known stop is not evidence of a game crash. Sparse console output does not establish an error-free physical game log. Never stop a similarly named owner app by inference.
