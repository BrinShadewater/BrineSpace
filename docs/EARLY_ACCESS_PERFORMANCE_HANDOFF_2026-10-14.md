# Project handoff

Updated: October 14, 2026 · Project: `C:/Users/Alex/Documents/Brine Space` · Task: Early Access performance readiness review

## Objective and acceptance

Identify remaining performance validation for PC and Mac Early Access from the latest
handoff and dated package evidence. This review does not certify either platform.

## Accepted decisions and constraints

- Owner parked Marsh animation polish for a separate session; none started.
- Ordinary Continue around 7 seconds and first launch around 12 seconds remain accepted
  (October 11). Brief zoom-settle misses remain accepted (October 13).
- Object-count investigation and Clone Lab revival remain parked. A longer stability
  check is recommended below; no new optimization or soak was started.
- Preserve visuals, gameplay, owner profiles and unrelated working changes. Use frozen
  inputs and isolated QA saves. Publishing and Apple signing require the owner.

## Current state

HEAD and recorded origin/main: `67e7db969`. Crew Hab description changed in
`scripts/room_database.gd` to "Adds two berths for crew"; uncommitted.
`docs/CURRENT_STATUS.md` records this review and the owner's animation deferral.
Latest tested Windows candidate `brinespace-6d97d875cd6b9d23` predates October 14
changes. Native Mac acceptance remains pending.

## Verification

Read October 14 code handoff, October 13 art handoff, current status, release workflow,
October 11 performance handoff and Mac release plan. Crew Hab text diff check passed.
No new build, benchmark, gameplay or visual checks run.

Recorded latest Windows checks: pack audit, smoke, Continue timing, save/relaunch,
40 starts and 30-minute soak pass; fresh workload 24/24, 12-room workload 20-21/24,
remaining zoom miss accepted. Earlier `42f32cba` stress workload (save excluded due to
fixture limitation): 0/21 phases pass, idle 25.5-26.5 ms, demolition max 105.6 ms.
This predates the lighting fix and does not establish current stress performance.
Object count rises about 80/minute with flat memory. GTX 1650-class PC and M1 are
unverified test targets, not confirmed minimum specifications.

## Next action

Recommended, not executed: freeze current selected inputs; build matching PC/Mac
candidates; audit both; rerun normal startup/save and focused changed-subsystem checks.
Measure the current large-station workload before choosing further optimization or a
supported station-size/FPS target. Check a longer session and repeated title/run transitions
for memory, loading and shutdown stability. Validate actual target PC and M1 hardware,
including Retina/fullscreen/focus on Mac. Establish Mac-specific QA save isolation and
native benchmark launch; the existing packaged benchmark runner supports Windows only.
Mac distribution signing/notarization and download-launch acceptance remain separate
from performance. Intel gameplay needs testing if Intel support is advertised.
