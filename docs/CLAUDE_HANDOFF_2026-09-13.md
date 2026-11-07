# BrineSpace: return-to-Claude handoff

Updated: September 13, 2026 · Workspace: `C:/Users/Alex/Documents/Brine Space`

## Objective and acceptance

Alex requested consolidation of this gameplay/performance task, updates to the skills, asset workflow and visual bible, and session closure. This document explains the current state and the changes since the recent Claude work. It is a navigation and evidence handoff, not a new release certification or permission to resume paused paid asset generation.

The exact last revision Alex personally used in Claude is not established. The reference point is the September 12 review in [CLAUDE_CHANGE_REVIEW_2026-09-12.md](CLAUDE_CHANGE_REVIEW_2026-09-12.md), which covers the recent Claude mirroring, test, performance and release work. Avoid describing every current feature as newly implemented by this task.

## Accepted decisions and constraints

BrineSpace is a Godot 4.6 underwater station-restoration roguelite prototype. The goal remains satisfying placement, interdependent production and discovery. Normal builds cost resources; failure conditions remain active. Runs are open-ended and end through Conclude Expedition. Do not restore retired timed directives, scenario victory or deadlines. Hidden recipes remain hidden until functioning rooms discover them; three consecutive functioning cycles stabilize a pattern.

Keep `scripts/main.gd` intact unless a refactor is explicitly requested. Preserve paired `.gd.uid` files, LFS raster storage, raw runtime PNG loading and the maintained release exporter. Read AGENTS.md, CURRENT_STATUS.md, DEVELOPMENT_NOTES.md and NOTICE.md before implementation. Search scripts/rooms/tests/tools/docs/assets explicitly; never recursively walk the enormous `output/` tree.

The art direction is now top-down, inward-facing equipment on every wall, matte department-specific materials, credible crew-relative scale and tight floor contact. Older north-elevation acceptance and earlier room TODOs may be superseded. BRINE remains dry and unsettling, not cheerful. Bill was excluded from the other task's character replacements; Veld is a mature woman without glasses; Marsh remains helmet-free with his anatomical right implant preserved.

**The animation task was explicitly closed. Do not resume Higgsfield generation or spend credits without explicit owner approval.** Its final note reports no pending provider job. Preserve existing assets and controller work. This restriction comes from the other task's owner decision, not from an inferred approval rule.

## Current state: what this gameplay task changed

### Paid operation and power feedback

Current operation and next-cycle affordability are different states. A mining bay can spend its final reserve unit at the cycle boundary and still be entitled to the full paid cycle. Reforecasting from the now-empty reserve previously stopped its prepaid charging early. Bay advancement now uses the funded operation map, preserving pause, master-power-off and the next unpaid cycle.

A later regression found the same mistake through another path: fire ignition/extinction refreshed every room from a next-cycle forecast. An unrelated fire could therefore revoke paid bay service. `room_fire.gd` now updates burning/formerly burning compartments only. Other rooms keep their current funded status. Recovery of an extinguished compartment retains the existing forecast check and respects suspension/resource restrictions. This does not settle the broader balance complaint that power feels too scarce.

Power feedback distinguishes generation, supplied demand, reserves and charge/discharge. Turbine feedback names its actual rotated intake cell and obstruction. Cleared wrecks and depleted deposits no longer count as physical blockers; live deposits, occupied cells, bounds and queued construction do. See [power handoff](GAMEPLAY_POWER_HANDOFF_2026-09-12.md), [first performance pass](PERFORMANCE_BUG_POLISH_PASS_2026-09-12.md) and [fire pass](FIRE_PERFORMANCE_POLISH_PASS_2026-09-12.md).

### Gameplay presentation and review tools

- The opening hand requires deliberate selection; it no longer begins with a blueprint implicitly selected.
- Studio provides a Bill standing/walking scale preview using production height, pivots and depth sorting. It is a local clearance aid; the preview does not become authored furnishing data or replace a full live-job traversal test.
- Continue has a separate saved-loop summary/schematic alongside the central actions. Disposable checkpoints test both populated and empty states without changing player saves.
- BRINE startup uses saved simulation time: dark room, staged lights/consoles, then the pod. Cold mist and temporary human tint accompany emergence. These changes do not resolve the separate complaint about weak cryopod animation.
- The airlock has a visible closed north exterior hatch. It closes after the diver clears the doorway, stays flooded while the diver is away and reopens before return entry. Phase, pause/power and Save/Continue checks cover the transition.
- Decorative floor power cables and orphaned bridge plates are filtered at their drawing/placement owners. Equipment pipes and salvage scrap remain. General decoration toggles must not resurrect the retired cables.
- Removed obsolete directive rewards from reroll tooltip text.

Read [startup/hatch handoff](GAMEPLAY_STARTUP_HATCH_HANDOFF_2026-09-12.md), [Studio/menu report](GAMEPLAY_STUDIO_MENU_2026-09-12.md) and the [45-item owner checklist audit](OWNER_PLAYTEST_CHECKLIST_AUDIT_2026-09-12.md) for the detailed mapping and limits.

### Performance fixes and diagnostics

Static floor/wall snapshots no longer rebuild for unrelated changing airlock/fire progress. The first attempt incorrectly omitted chamber water too; pixel comparison caught the stale wet floor. Water remains in the static key because it actually changes floor pixels. In a fixed 60-frame fixture, rebuilds fell from 59 floors plus 59 walls to zero, with retained pixels matching a forced rebuild. This is scoped evidence, not whole-game performance acceptance.

Fire advancement gathers burning rooms once per call, skips safe stations early and avoids emergency-power scans when sprinklers are off. A controlled 300-room comparison measured about 310 to 91–93 microseconds per normal update, and about 1,231–1,264 to 90–97 microseconds per 0.4-second catch-up update. Room state, water spending, damage and logs matched the original implementation. These numbers measure this CPU function only.

There is now a lightweight local monitor:

- **F7:** toggle live FPS, mean/p95/peak frame intervals, hitch count, draw calls, static engine memory and room counts; it does not pause gameplay.
- **F8:** open the existing local bug reporter. Manual bundles now include `diagnostics/performance.json` alongside logs and the separate diagnostic station save. The player checkpoint is not overwritten.
- **F9:** open Room Layout Studio. This resolves Studio's previous collision with F8. All three keys are reserved from gameplay remapping.

The monitor retains 120 approximately one-second buckets and 32 recent hitches in memory. It records pause/focus markers and samples context at bucket end. It does not enable the heavy draw profiler. Frame intervals include vsync, startup, focus loss and pauses. Static memory is not total process/GPU memory. History does not survive a crash; an automatic report on the next launch intentionally excludes new-process timings. See [diagnostics guide](PERFORMANCE_DIAGNOSTICS_2026-09-12.md).

## Other tasks: newer source work to preserve

The following is reported by their current handoffs, not freshly retested by this documentation closeout:

**Room art:** strict overhead direction and crew-scale work cover the current 47-room catalog. There are recorded four-direction reviews, 176 layout checks and 47 card identities. BRINE tube grounding received specific owner approval; that approval does not extend to the entire catalog. Subsequent centerpiece/furnishing passes v1–v9 add large process-specific work surfaces and medium neutral support furnishings, including the latest Radio Lab, Listening Post and Holographic Core batch. Most source work has bounded native review with owner aesthetic acceptance and export still pending. Read [current coverage](ROOM_ART_CURRENT_COVERAGE_AUDIT_2026-09-12.md), [strict overhead closeout](OWNER_ASSET_STRICT_OVERHEAD_CLOSEOUT_2026-09-12.md), [crew-relative scale](CREW_RELATIVE_ART_SCALE_2026-09-12.md), and the furnishing entries at the top of CURRENT_STATUS.md. Later material and drone corrections supersede older pending labels; do not replay the old asset queue blindly.

**Characters:** the closed task reports all 20 targeted walk variants selected with bounded native/live review: eight Veld, eight Branforth and four Marsh. Marsh also has matching four-direction idles and east/west start, stop and short-step controller integration with Save/Continue checks. This is not completion of all transitions, distances, actions or autonomous routes. Veld north seating remains an unselected candidate: 16 native phase samples showed foot sliding and inconsistent anatomy despite zero mechanical fixture failures. Read [animation session close](HANDOFF_CREW_ANIMATION_SESSION_CLOSE_2026-09-13.md) before any continuation.

## Verification and workspace condition

This task's latest gameplay evidence is recorded in the linked reports:

| Scope | Result and evidence |
| --- | --- |
| Power/fire regression | Passed; `output/test-runs/20260912-215552-headless`, including 45 fire checks |
| Native fire gameplay | 36 checks passed; `output/test-runs/20260912-215454-native`; suppression/extinguished captures reviewed |
| Full hazard chain | Passed; `output/test-runs/20260912-215504-headless`; suppression, escape, hull repair and drainage |
| Monitor collector | Passed; `output/test-runs/20260912-214729-headless` |
| Real F7/F8/F9 input and ZIP report | Passed; `output/test-runs/20260912-214701-native`; overlay reviewed at 1600x900 and 960x540 |
| Static surface optimization | Exact retained/rebuilt comparison and invalidation passed; see first performance report |

A printed PASS or zero exit code is insufficient if Godot logged script errors. The maintained runner enforces that. Two fire fixtures previously used the fire-refresh function to bootstrap an unpaid station; they now establish operation through the normal paid economy step. Assertions were retained. Native image-import warnings remain distinct from actual release validation.

At this handoff, HEAD was `b2648fea` and the index and HEAD both contained the same 18,164 tracked paths. The workspace had 332 tracked changes and 777 untracked entries across tasks. These are status entries, not a count of all generated files. Much of the current game is uncommitted; do not reset, clean or assume HEAD represents the playable workspace. This task did not stage, commit, export or publish. No full suite was rerun for this documentation-only closeout, and later concurrent changes do not inherit historical acceptance.

## Skills, workflow and bible update

The maintained room gameplay-preview reference now carries the fire/funded-state lesson, diagnostic interpretation, and performance evidence limits. The character handoff reference explains keeping animation phase/workload constant while optimizing and preserving the paid-generation closure. Targeted installed mirrors are synchronized. ROOM_ART_PRODUCTION.md and the visual bible now connect visual acceptance to runtime state/invalidation and clearly separate proposed rendering optimizations from adopted art direction.

## Next action for Claude

1. Read CURRENT_STATUS.md and inspect current selections/local overrides before editing. Preserve all uncommitted work. Start the configured title scene in Godot 4.6.1 after imports.
2. Run a normal paid expedition with F7 available and capture F8 soon after a reproducible fault. Prioritize the original power/reserve experience and west-facing turbine report; neither is declared closed by these narrower fixes.
3. If performance is the chosen task, remeasure the current build before implementation. Older 25-room timings suggest terrain drawing, live-room drawing and repeated room setup as candidates. Terrain retention/culling and selective room reconfiguration were proposed, **not implemented in this task**. Test excavation, movement, zoom, lighting and invalidation with identical-state pixel comparisons. Do not slow character cadence or remove intended detail simply to improve a benchmark.
4. Review combined art/animation in real gameplay after selecting a stable source state. Preserve known open seating/transition issues and the explicit paid-generation restriction.
5. When a playable build is requested, follow RELEASE_WORKFLOW.md and the maintained exporter. Freeze the source/dependency selection and test the actual release executable, including dynamic art, F7/F8, paid gameplay and Save/Continue. An old PCK or editor check does not certify these newer changes.

This Codex task is closed at the owner's request. No background continuation is intended. The next task should begin from this handoff and the current workspace, not from a reconstructed historical TODO list.
