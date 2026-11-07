# Frozen Windows Candidate and Release QA Implementation Plan

> **For agentic workers:** Use the existing authorized native execution in this session; reviewers inspect independent evidence. No additional approval is needed for the requested reversible freeze/build/QA work.

**Goal:** Build and test an actual full-current-source Windows candidate while preserving appearance and crew behavior, then retain the exact source selection for Mac validation.

**Architecture:** A physical runtime dependency/source snapshot on D: uses a separate complete Git index and the maintained exporters. Delivery files receive no QA overrides; isolated physical copies execute normal-entry and benchmark adapters.

**Tech Stack:** Godot 4.7.2, Python, PowerShell, Compatibility/OpenGL.

**Spec:** User request; `docs/RELEASE_WORKFLOW.md`; `docs/CREW_STALL_HANDOFF_2026-10-16.md`.

## Global constraints

- Preserve visuals, crew behavior, owner saves/layouts, paired UIDs, LFS artwork and all unrelated work.
- No private LOD/stable-ID/native-water/structural overlays, runtime quality changes, commit or publication.
- Every Godot process uses scratch APPDATA and resolved-path guards; fingerprint owner files before/after. Native timing runs serially and visibly, muted on the secondary display.
- Keep 20 GiB free. Freeze required current dirty/untracked runtime bytes physically; no live-source hardlinks.
- Existing 60 FPS/memory/loading gates remain unchanged; measured failures remain failures.

## Review focus

- Stale tracked export lists must not omit current untracked helpers or changed art bindings.
- Actual release templates strip assertions; operations and failures must be explicit.
- Normal entry, async F8 and restart/Resume require actual-package checks, beyond the benchmark adapter.
- Owner-layout benchmarks and clean first-install defaults are separate cases.
- Mac static packaging and native hardware/distribution acceptance remain distinct.

### Task 1: Physical source selection and Windows package

- [x] Save owner/source baselines and selected dependency manifest; include complete current program/config/tools, reachable resources, paired UIDs and verified templates. Exclude authoring-only generations and private runtime trials explicitly.
- [x] Create a separate local Git snapshot with a complete index; deliberately skip absent nonselected authoring assets. Verify index count against HEAD and copied bytes against source hashes.
- [x] Run copied `tools/export_release.ps1` against the frozen root under scratch APPDATA. Retain expected manifest, build metadata, logs and EXE/PCK hashes.
- [x] Audit exact packaged assets and script/config identities from an empty scratch project. Reject missing/changed/unexpected or release-only errors before gameplay QA.

### Task 2: Actual Windows release QA

- [x] Guard BugReport before any session writes in a physical QA copy. Run normal configured entry/New Game/Continue, native visual checks and simulation; preserve failed evidence.
- [x] Exercise the async F8 Save handler, report contents and screenshot correctness; save/restart/Resume using scratch data and observable state.
- [x] Run fresh/reported/large workloads at native resolutions and idle/zoom/placement/door-light relevant actions. Keep full pacing results and overlapping-process/visibility checks; do not compare with old private runtime as a claimed optimization.
- [x] Run a bounded longer soak and relevant transitions where package checks permit. Record remaining release gates explicitly rather than silently broadening scope.

### Task 3: Closeout and Mac continuation

- [x] Recheck delivery/source/owner identities and no delivery overrides; preserve README, NOTICE, licenses, checksums and concise handoff/CURRENT_STATUS milestone.
- [x] Build/audit Mac from the same selected runtime bytes after Windows package QA, preserving Windows expected manifest first. Native Mac gameplay, performance and Gatekeeper/signing acceptance require Mac hardware.

### Continuation: two-hour Windows station soak and native Mac handoff

- [x] Preserve the completed 600-second evidence; use a new physical QA copy of the same EXE/PCK and fresh scratch profile for a 7,200-second normal-process 4× reported-station soak. Completed 7,200.011813 s / 431,863 frames / 34 checks.
- [x] Scale only the external observation fixture's duration/retention limits (1,500,000 frame intervals, 2,048 periodic observations, 4,096 comms actions). Keep all intervals, pauses, reports, warnings and genuine loop endings; no artificial survival or crew changes. Bound the driver at duration +600 seconds and terminate only its own child on failure. A scratch stop sentinel requests graceful partial evidence and normal exit at the next five-second observation.
- [x] Record external Windows process memory at five-second intervals; keep engine texture/object counters separate from process memory and GPU residency. 1,440 samples, no foreign-process overlap.
- [x] Inspect duration, normal simulation/crew progress, errors/stuck observations, memory trend, hitches, Save/Return/Quit and package/owner identities. Existing full-source guard retained; no new production writes. Keep pacing/loading/Save failures open and flag continued live-object growth. Release orphan-zero is unavailable evidence.
- [x] Check configured Apple tool capabilities and preserve exact ZIP/checklist. No native macOS workflow is exposed. Owner confirmed they will run the ZIP on their Mac; no security-setting changes by this task.
- [ ] Review the owner's separate-test-account Mac results. Native launch, gameplay, input/audio, F8, pacing/memory and save/reopen remain pending; static parity is not native acceptance.
- [x] Update current status, dated report and concise handoff with actual outcomes and remaining limits. No source/runtime rebuild, commit, upload or publication.
