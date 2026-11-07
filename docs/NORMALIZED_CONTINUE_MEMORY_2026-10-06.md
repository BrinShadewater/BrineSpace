# Project handoff

Updated: October 6, 2026 · Project: BrineSpace · Task: normalized Continue memory and playback

## Objective and acceptance

Continue full PC/Mac performance/release readiness. Compare the same stopped gameplay/playback/camera state across Continue, distinguish activity-dependent resource history from restoration growth, and preserve selected animation behavior. Full station budgets/endurance/provider admission remain open.

## Accepted decisions and constraints

Private diagnostic changes only. The comparison deliberately refreshes stale fixture navigation through normal snapshot restoration and presents each active crew member at the current paused clock before both samples. No simulation advances during that presentation tour. Canonicalization excludes only saved_at and zero-valued optional workspace scroll entries; other checkpoint fields must match.

## Current state

`output/scene-dependency-warning-2026-10-06/`: visible-memory, inventory-memory and repeat-memory probe/runner/log/results/owner files. Current normal source unchanged this turn. Texture inventory reads dimensions/weak references only, without GPU readback; estimates cover selected named groups and RGBA8 base levels, not full memory/format/mip accounting.

## Verification

- Source `crew_sprite_player.gd` advances gait phase from elapsed movement when a visible frame request catches up last_time/last_position. Paused camera presentation removes the earlier James/Branforth phase discrepancy while retaining full NPC snapshots and simulation clock. No playback-restoration defect reproduced in this lane; no animation rewrite made.
- Symmetric snapshot traversal identifies the workspace difference: six missing scroll entries become 0.0 after restore. `workspace_state.number` defaults missing entries to zero, and restore writes each tab's value. These are equivalent optional defaults, not a demonstrated UI defect.
- First normalized control passes 205 checks, zero errors/warnings/anonymous objects. Resource-inventory follow-up also passes 205 and confirms canonical state equality before/after Continue.
- Four-cycle repeated control passes 441 checks, including three explicit canonical before-save/after-Continue equality assertions, full NPC preservation during navigation refresh/presentation, old-resource release and prior save/drone checks. Zero failures, engine errors, leaked objects or shutdown warnings.
- Restored stopped static memory across three Continues: 459,973,499 → 460,154,083 → 460,264,545 bytes (+0.063%). Each is lower than its preceding before-save sample (494,553,705 / 544,445,023 / 544,487,555). This does not reproduce a positive ~50 MB restoration step in matched stopped gameplay states. Resource histories are still different; it is not large-station/two-hour acceptance or a global no-leaks claim.
- Bill frames, interface and room-pool inventory estimates/counts remain equal between compared snapshots. Bill dry/player groups overlap: normal Grid binds dry arrays to player frames; do not sum the two inventories or infer duplication from equal group totals. Room-library exposure varies, 39→32→26 images; this reflects different loaded resource history and remains explicitly outside full resource equivalence.
- The fixture's post-simulation/exterior-exercise observations still show static ~456.85→507.91 MB. Its ordinary drone cache grows 96,337,924→240,844,816 bytes, while indexed cache changes 156,782,592→48,345,088. The ordinary increase is 144,506,892 bytes, matching the size scale of the previously traced 2688×13440 North work atlas, but path-level causality and CPU attribution are not proven by these aggregate counts. Investigate actual cache source paths and remaining unoptimized work-direction uploads.
- All 2,936 owner non-log files unchanged in every completed lane. Processes terminal. No normal source/art edits, export, commit or publication.

## Next action

Move from the disproven unequal-state restoration comparison to explicit activity/cache source attribution. Inventory ordinary/indexed drone cache paths around restored idle and each work heading, then address the largest remaining atlas upload/storage with lossless pixel/clock/layer/material regression coverage. Keep activity-dependent memory growth under review without treating the old ~50 MB number as a confirmed Continue leak. Larger deterministic workloads, normal memory/frame/loading budgets, provider admission, refreshed actual release, original packaged bugs, endurance and actual Mac certification remain open.
