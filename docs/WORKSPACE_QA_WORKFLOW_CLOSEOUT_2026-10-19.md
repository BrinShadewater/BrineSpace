# Workspace cleanup and iPad QA workflow — October 19, 2026

Archived 12 superseded QA builds/24 duplicate PCK copies as verified binary deltas;
their full reconstructed SHA-256 matched before deletion. Preserved 290,894 other
files at the archive stage, including source snapshots, saves and reports.
Removed 124 enumerated obsolete scratch crew-cache/Xcode cache directories;
445 protected save files remained hash-identical. Current shared-floor build,
life-room rollback and frozen Mac signatures passed after both stages.

Recovery toolkit/manifests: `/Users/Shared/BrineSpace-workspace-cleanup-20261019/README.md`.
Keep its named immutable donor. About 91 GiB logical packages were replaced, but
APFS shares blocks: this is not 91 GiB of recovered capacity. The cache stage alone
increased free space from 11,286,958,080 to 15,659,364,352 bytes (~14.58 GiB free).
No source, art, Git/LFS storage, owner saves, frozen deliveries or current builds
were removed. Older native binaries and signing metadata remain; their PCK must
be restored before use.

The previous 56,696-line current-status journal is preserved byte-exact at
[status history](CURRENT_STATUS_HISTORY_2026-10-19.md), SHA-256
`63901bc6ed7600594ea49e9f3bc7c736d2253efc6f88900cb83217c7c5796d6b`.
[Current status](CURRENT_STATUS.md) now provides a concise continuation map.
[iPad QA workflow](IPAD_QA_WORKFLOW.md) records save isolation, helper reuse,
exact-package evidence, profiler limits and retention. The maintained project
room-pipeline skill and storage reference point to it. The visual bible gained
a renderer acceptance rule; its complete previous body remains unchanged.
No global/plugin skill was overwritten.

## Continued profiling

Used installed Validation2 `brinespace-2e6262a522a7271a`, A14/4GB physical iPad,
connected 40-room disposable fixture and normal costs/caps/hazards at 4×.
Local evidence: `/Users/Shared/BrineSpace-ipad-optimization-20261019/render-profiler`.
Original saves were freshly backed up before fixture replacement.

Time Profiler PID attach returned “Cannot find process for provided pid” despite
fresh devicectl confirmation of the exact container/PID 24341. A diagnostic
all-process capture requested 20 s and ended after 2.298327 s with “Device disconnected”.
Exported data contains 1,272 target samples, 1,138 on the main thread; all stack
frames are unsymbolicated addresses. This interrupted capture establishes neither
a CPU/GPU bottleneck nor loading/footprint improvement. Raw capture stays outside
the repository. No renderer or game-source change, rebuild or installation was
made in this cleanup/documentation pass. Tested baseline remains installed.

## Owner restored and verified

All five original files were restored hash-exact before owner launch. Actual
Save → title → Continue → Save passed full gameplay-state and exact timer parity:
cycle64, seven rooms, speedindex2/4× and timer1.11834893097652. Only save metadata,
event history, scroll and camera metadata differed after UI use. Native parity
probe used isolated storage and verified the real Mac owner profile unchanged.
Final Save92.939ms, logged errors0. Screenshot confirms station paused,4× selected
and menu closed. Continue still resets speed to1×; restored4× manually while
paused. The healthy two-hour helper was retained. Current build and rollback
remain unchanged. No new performance gain or iPad release clearance is claimed.
