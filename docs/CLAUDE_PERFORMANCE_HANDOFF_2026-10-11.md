# Project handoff

Updated: October 11, 2026 · Project: `C:/Users/Alex/Documents/Brine Space` · Task: performance continuation for Claude

## Objective and acceptance

Prepare a smooth PC/Mac release preserving selected visuals, layouts and gameplay. After four days of experiments, the owner wants to move beyond this step and is considering Claude taking over. Make the next session one bounded implementation with a reviewable result or specific blocker. This handoff does not certify a release.

Existing gates remain: gameplay p95 ≤16.7 ms / p99 ≤25 ms; investigate >50 ms frames, no reproducible >100 ms stall; cold/warm loading ≤10/6 seconds excluding dialogue; textures ≤2 GiB for 12 rooms / ≤3 GiB for the large station; stable saves, memory and visuals. GTX1650-class PC and M1 are unverified test targets, not published minimum specifications.

## Accepted decisions and constraints

- Follow `AGENTS.md`, current status and relevant development notes. Preserve owner saves/layouts, original art, vendor/legacy dependencies and paired UIDs. No monolith refactor or gameplay changes.
- Tests require scratch APPDATA **and verification of resolved user-data paths**, owner fingerprints before/after, and scratch autosave paths after restoring copied saves. Mac needs platform-specific isolation.
- Native tests: muted, secondary monitor, physical input disabled. No screenshot batches, runtime-tree copies or unnecessary exports; maintain 20 GiB free. Do not broadly delete unknown outputs.
- Whole quoted `res://` paths, runtime PNG loading and Git LFS remain required. No quality reduction, frame removal, global downscaling, renderer upgrade or automatic quality changes.
- Repeat checks only for changes, failures or unresolved concerns. Do not retry rejected experiments unchanged. Itch.io publishing remains separate.

## Current state

**Read the [evidence and tooling map](CLAUDE_PERFORMANCE_EVIDENCE_2026-10-11.md) before proposing a new trial.** It routes earlier accepted work, failed experiments, research, bug coverage and benchmark safeguards. The concise handoff is the entry point, not the complete archive. Prepared locally; no message to Claude or acknowledgement of receipt has occurred. Owner explicitly chose to pause for Claude takeover; do not automatically restart optimization.

**Integrated:** topology-signature cache in `scripts/bill_npc.gd`, new `tests/test_crew_topology_signature.gd` plus UID and crew registration in `tests/index.json`. Bill SHA256: `b0ee1a9b316f12fdf936e222c6e18bd9e59e55d6407601e51c51573b0e732e2a`. Complete inputs and query ordering remain intact; locked cells update even on cache hits. Cache owns no world/art objects. Changes are uncommitted; preserve other existing working-tree work.

**Validated private candidate, not integrated:** three mining-effect sheets use lossless LA8 storage with native tint, original-image fallback, retained immutable encoded original bytes and session-scoped lifetime. Candidate files (`motion.gd`, `display.gd`, `catalog.gd`, `resources.json`, derived PNGs) are in `D:/bs-release-crew-cache-20261009/benchmark-input-isolation/native-effect-adapter-immutable/`. Normal DroneAnimation/art is unchanged. Proposed Windows-only guard is **not yet implemented**; Mac needs native acceptance first.

No `BrineSpace.exe` or `GodotQA.exe` process was running at handoff. Reused diagnostic runtime `D:/bs-release-crew-cache-20261009/floor-slot-trial/prepare-diagnostic/workloads-v2/runtime/` has its empty-scene/guarded-report/benchmark override restored. This is **not** a full-current-source certified release build. No new export was made for this handoff.

## Verification

- Integrated topology: six normal-project tests clean, including 14,567 signature checks, room ownership, navigation prefix, rebuild staggering, Moonbay save and Continue. Native topology CPU cost fell approximately 43–44%; whole-frame gains are modest and tails mixed. [Integration evidence](TOPOLOGY_NORMAL_INTEGRATION_2026-10-11.md), [real-map limits](TOPOLOGY_REAL_MAP_REGRESSIONS_2026-10-11.md).
- Private effects: 576 native whole-image pairs exact; five immutability, 21 fallback/identity/accounting and 34 two-owner session-exit checks pass. Three alternating pairs: 6,480 frames / 36 full state-camera matches. Peak texture counter **2928.086 → 2744.336 MiB**, saving **183.750 MiB every pair**. Mean **29.768 → 29.354 ms**, p95 **44.627 → 44.222**, p99 **52.954 → 53.440**. Gameplay gates still fail. Settled memory unchanged; loading is diagnostic, not cold/warm release certification. [Latest effects evidence](IMMUTABLE_EFFECT_STORAGE_2026-10-11.md).
- Latest completed runs left all 2,938 owner files unchanged. Artifacts: sibling `immutable-effects-mixed-repeats/` and `topology-normal-integration/` under the benchmark-input-isolation directory above. Engine texture accounting is not physical GPU-residency proof; do not relax memory gates.

## Next action

1. Recommend a **60–90 minute cap for the next integration session**, not a completion promise. Integrate the private three-sheet storage path guarded to Windows, preserving APIs, filtering/material fallbacks, immutable originals and cleanup. Add a maintained generator and focused normal-source regression/asset dependency checks; preserve LFS/UIDs. Stop with a patch/checks or one concrete blocker. No broad research loop.
2. Investigate remaining roughly 96 MB cargo/equipment uploads and the unexplained current-map simulation-step spike. Neither is closed. Indexed shader/CanvasGroup providers, larger global drone cache, lookahead and conditional material-write retention already failed matched-workload acceptance; do not retry unchanged.
3. Then freeze physical full-source inputs and follow [release workflow](RELEASE_WORKFLOW.md). Packaged original nine reports, placement/demolition/UI, loading, two-hour soak, ten transitions, target hardware, saves, display/focus/audio and exact PCK audits remain pending. Headless tests/reused diagnostics do not close these gates.
4. Mac remains uncertified: native M1 performance/visuals/Retina/input/save checks, isolation, Developer ID signing, notarization/stapling and downloaded/offline Gatekeeper launch are pending. Universal 2 packaging alone proves none of these. Preserve original storage on unverified platforms.

No reliable overall release ETA exists. A fresh reviewer can improve prioritization and stop conditions; changing models does not guarantee completion. No project configuration or unrelated skill changes are warranted merely for transfer. Current status/handoff govern continuation; dated reports are evidence.
