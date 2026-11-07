# Project handoff

Updated: October 6, 2026 · Project: BrineSpace · Task: stopped-state Continue memory attribution

## Objective and acceptance

Continue full PC/Mac performance/release readiness. Compare fresh and restored allocations without further simulation, matching station topology, crew snapshots, camera and presentation before attributing the earlier ~50 MB step. Do not close memory growth using unequal states.

## Accepted decisions and constraints

Private diagnostics only; current normal source unchanged this turn. Use actual existing recovery/save/title/Continue flow and scratch profiles. Preserve failed/misaligned evidence; only accepted controls support conclusions.

## Current state

Evidence: `output/scene-dependency-warning-2026-10-06/`: equivalent-memory, aligned-memory and state-differences probe/runner/log/results/owner files. Detailed comparison snapshots exclude saved_at timestamp only. The existing private current-Main/crew/indexed-drone fixture is used; no provider normal admission.

## Verification

- Initial stopped comparison passes 194 checks, zero errors/warnings. Fresh station contains five rooms but all three active crew graphs cover four (1,407 points, stale topology signatures). Continue graphs cover five (1,655 points, current signatures). The fixture adds its mining bay after its last manual simulation step, so the earlier fresh/restored observations were not equivalent.
- Refreshing fresh navigation through normal snapshot restoration preserves all three full NPC snapshots and updates each graph to five rooms/1,655 points. Immediate static allocation increase only 600,532 bytes: this is not an explanation for the ~50 MB step.
- First alignment implementation mistakenly retained actor references in the suspended scene loop and read grid_zoom from the wrong checkpoint dictionary level. It failed release assertions/one script access; excluded, source/log retained as aligned-memory-rejected. Corrected helper lifetime and checkpoint state access.
- Next control passed 197 checks but camera still differed because its own zoom call queued deferred centering. Preserved as aligned-memory-camera-mismatch; excluded from equivalent-view conclusions.
- Corrected camera target yields identical captured scroll/zoom. Latest detailed control passes 197 checks with zero failures/errors/warnings/anonymous objects, all old-resource release checks intact. Five-room navigation matches and full NPC state is retained, but playback/workspace snapshots are not identical.
- The detailed remaining playback differences are James/Branforth phase 0.5061757405→1.5718218014, last_time 1.3333333333→2.0, last_position (19.24648,16.42844)→(19.32277,16.45199), and motion.started 1.3333333333→2.0. This may involve offscreen presentation catching up, but intended behavior and causality are not proven. Do not equate six-field NPC restoration checks with full presentation-state equivalence. Dictionary comparison currently reports changed existing keys; workspace inequality without a printed leaf may involve added/removed keys and needs symmetric traversal.
- Latest samples: fresh-before-save static 494,522,231/texture 2,319,980,470 bytes; restored-before-further-simulation static 459,779,793/texture 1,939,844,474. Restoration does not reproduce a positive ~50 MB step at these boundaries, but unequal playback/resources prevent a broad memory or leak conclusion. The earlier post-simulation step remains unexplained.
- All 2,936 owner non-log files unchanged in every completed control. Processes terminal. No normal source/art edits, export, commit or publication.

## Next action

Normalize visible/offscreen presentation at the same clock and camera tour before saving and after Continue, record complete symmetric workspace/playback differences, and inventory source/presenter/ordinary GPU resources alongside static allocations. Test whether James phase catch-up is expected and preserve actual animation timing. Then compare equivalent settled samples and investigate remaining post-simulation resource changes. Keep larger station pressure, provider admission, refreshed actual release, all frame/loading/memory/original bugs/endurance and actual Mac gates open.
