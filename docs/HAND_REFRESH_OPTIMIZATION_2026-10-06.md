# Project handoff

Updated: October 6, 2026 · BrineSpace · Native hand-refresh acceptance

## Objective and acceptance
Remove repeated hand reconstruction without changing displayed content, input,
hover, drag or artwork. Full PC/Mac performance and release gates remain separate.

## Accepted decisions and constraints
Retain normal Main/DraftCard presentation-based reuse. Scene-owned snapshots,
container identities and current displayed state determine invalidation; no
permanent cache, altered quality, gameplay, owner settings or private GPU backend.

## Current state
Changed scripts/main.gd and scripts/draft_card.gd; permanent regression in
tests/test_hand_reuse.gd with paired UID, admitted to cards-bindings in
tests/index.json. Source implementations preceded this continuation; this interval
completed native acceptance and permanent input/visual regression coverage.
Physical diagnostic sources, logs, screenshots, hashes and results:
output/hand-reuse-2026-10-06/. Earlier failures remain historical evidence in
HAND_REUSE_IN_PROGRESS_2026-10-06.md and NATIVE_TEST_ENVIRONMENT_BLOCKER_2026-10-06.md.

## Verification
Permanent isolated native fixture exits 0: 74 checks, zero failures, 12 exact
retained/fresh pixel comparisons. Real thumbnails, duplicate-index clicks, hover,
selection, content/art invalidation, drag ghost/fade, cancellation and stopped-game
input covered. Corrected diagnostic-only missing gradient/carryover; reviewed real
fan thumbnails. 100 unchanged row/fan refreshes take 8.875/8.679 ms.

Three matched native 1080p 40-room pairs use the normal renderer and physical
current Main copies differing only in old/new card refresh plus equal timers.
15 action/speed phases per run, 60 samples each; 3 active actors, 38 initial powered
rooms and active drones. All compared phase action/speed/zoom/power/drone states
match; 16 measured refreshes per run. Median per-run mean card time:
4.449 → 0.167 ms (~96% less). Overall frame means remain ~36–37 ms; no meaningful
overall FPS gain established. Post-change p95 54.6–56.7 ms, p99 68.8–70.0 ms,
max 172.8–173.2 ms; 1–2 frames over 100 ms each run. Texture memory unchanged:
4,283.22 MiB. Loading 15–28 seconds here is not controlled cold/warm acceptance.
This is debug/editor runtime on RTX4070Ti, not packaged/minimum-hardware/Mac proof.
All completed runs preserve 2,936 owner non-log files.

Empty headless/native and hand/station processes now exit cleanly. Fresh QA and
installed engine version controls also exit 0. Earlier 0xC06D007F is not reproduced;
underlying environment failure remains unexplained. No reboot/global changes.

## Next action
The crew-stall follow-up is now retained and verified within its recorded scope:
`docs/DRY_GOAL_REACHABILITY_2026-10-06.md`. It reduces the maintenance decision to
~32 ms and recurring frame to 65–71 ms; other release gates remain open. The
attribution below records why that follow-up was chosen.

The repeatable ~173 ms frame spends ~142 ms in crew update; it occurs away from the
lighting toggle. A separate substage probe reproduces 178.8 ms: James/Branforth
update 145.9 ms, no topology rebuild, resulting maintenance goal; companion,
construction, flood/fire and passage work are small. A diagnostic subclass further
reproduces 174.1 ms; James chooses maintenance in 141.1 ms while dry. At least 128
route attempts are captured (bounded cap), with repeated failed targets; two
galley station attempts take 85.5/10.8 ms and return empty routes. Evidence:
goal-detail.json and crew-detail.json, each clean exit and unchanged owner files.
No normal actor change yet. Next prototype a decision-scoped dry reachability
proof after the first failed search, mirroring the existing swim failure scope.
Require disabled-node/fire/directed-graph/choice-boundary coverage and exact
destination/path/behavior comparisons before admission; do not cache permanent
navigation results or change goal order/RNG/attempt limits.
Other >50 ms engine-wait/render frames, memory budgets, original bug closure,
full native endurance, actual Windows release and Mac certification remain open.
