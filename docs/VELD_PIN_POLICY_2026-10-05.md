# Veld conservative pin accounting and interruption coverage

Updated: October 5, 2026 · BrineSpace · No production eviction

## Objective and acceptance

Quantify the residual storage after broad immediate-transition protection, and
exercise equipment cancellation, pause and snapshot restoration with all art loaded.
Do not conflate an inventory estimate with memory actually freed in gameplay.

## Accepted decisions and constraints

Reuse the complete selected-bank inventory with storage-object deduplication.
Keep every bare frame pinned as a conservative baseline, then add helmet families.
No runtime code, animation, equipment behavior or owner settings change. The native
fixture uses normal game delta and renderer in the same isolated three-room station
as the deadline experiment; automatic comms/focus pauses are excluded explicitly.

## Current state

### Pin accounting

| Protected set | Unique pinned images | Remaining candidate images | Candidate decoded storage |
|---|---:|---:|---:|
| All bare + all helmet death clips | 1031 | 769 | 151.765 MiB |
| Above + idle/walk/carry/swim/tread/recover-air families | 1530 | 270 | 61.216 MiB |
| Above + sit/read/lie/get-up/sleep/bunk families | 1608 | 192 | **41.716 MiB** |

Family matching includes authored turns, water starts/stops, distress and cargo
variants by their prefixes. Image membership, not frame-reference count, determines
candidate bytes; any image used by a pinned clip remains pinned. The inventory
hash, complete rules and candidate memberships are in
`output/veld-pin-policy-2026-10-05/accounting.json` and `analyze.py`.

All three rows are **unproven candidate policies**, not safe eviction sets. Even
the final row leaves helmeted eating/drinking, inspection/interaction, kneel/repair/
stand, torch draw/stow, pickup/unload and salvage. Current or imminent work can
request these immediately. In particular, `bill_npc.gd` transitions interrupted
kneel/repair work to stand immediately, so a job pin must include its exit chain,
not only the active clip. A task may start near its interaction point; travel is
not a guaranteed preparation window.

The earlier 202.32 MiB engine-counter drop used the much less conservative first
row in a non-playing fixture. It must not be advertised as the saving available
from this final policy. The remaining 41.716 MiB is decoded storage, not a new
engine-counter measurement, and current-job pins will reduce it further. These
figures establish that this one-character conservative policy cannot by itself
close the game's multi-GiB memory gap. Do not extrapolate across other characters
or assume the same pin sets apply to their controllers.

### Native pause/cancel/restore coverage

The output fixture runs equip and remove at 1x/2x/4x, advances into each action,
then pauses for eight rendered frames. It captures the actor and playback snapshots,
cancels the action, restores both snapshots and lets the action finish normally.
No storage is detached and no loading work is added.

- Six of six cases pass; action timer/equipment remain unchanged during pause.
- Cancellation returns to idle without changing the existing equipment.
- Restored actor snapshot matches exactly and selected frame object identity matches.
- All restored actions complete with the requested equipment state.
- 512 observed frame/frame_at_elapsed requests, zero null results.
- Observed clips include bare equip/remove and bare/helmet idle and walking.
- Zero engine errors; all 2,936 owner non-log files unchanged.

The test restores in-memory actor/player snapshots through the real restore methods.
It does **not** write/read a checkpoint, perform title/Continue, trace locker travel,
exercise death or job interruption, or prove residency misses are absent: all
textures remain resident. Direct pixel reads bypass the frame-method observer.

## Verification

Evidence directory: `output/veld-pin-policy-2026-10-05/`. Contains accounting script,
hashed input reference, fixture generator/probe, guarded runner, coverage JSON,
native log and owner fingerprint. One successful native coverage run; no repeat
benchmark matrix. Source review confirms water/cargo turn selection, cancellation,
Veld snapshot validation and immediate stand-on-work-interruption behavior.

Changed only output experiment files and this handoff, current status and action
register. No frame-time gain, new memory reduction or release acceptance claimed.

## Next action

Do not enable the broad inactive-helmet policy. If pursuing this scoped saving,
trace job selection/start and interruption to pin complete entry/work/exit chains,
then measure a byte/time-bounded preparation queue under normal 4x gameplay.
Restore must prepare the complete required set before resuming. Preserve immediate
public equipment-switch semantics in fixtures rather than silently adding waits.

Before expanding this into a large residency subsystem, compare its remaining
benefit with the larger active drone texture allocation and other character banks.
Use bounded inventories and proven pixel-preserving mechanisms; rejected atlas/
crop approaches stay rejected without new evidence. Retained floor-mesh ownership
is a separate endurance issue. Windows stalls and native Mac acceptance remain open.
