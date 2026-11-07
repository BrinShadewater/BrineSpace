# Combined room export with current Bill controller

Evidence: `output/room-rollout/windows-25-current-controller-v1/verification.json`.
Windows debug executable launched from a fresh external working directory.

The fixture includes the original ten production rooms, all ten second-batch
rooms, Thermal Power Control, Acoustic Communications, Hull Integrity Control,
Tidal Condenser and Gravity Loom. Thirteen additional Battery Arrays form the
supporting connected row: 25 distinct identities, 38 placed rooms.

All 25 selected source hashes and 50 raw source/card PNG decodes passed.
The controlled tour scheduled destinations while using Bill's actual graph,
smoothing, update, movement and arrival code. It physically reached all 38 rooms,
crossed 104 reciprocal boundaries and checked 7,925 movement steps for collision
clearance and speed. Exit status and ERROR/SCRIPT ERROR scans passed.

Pack SHA256: `4FD61160498BDE68C23663108B4E7CEA9285BD6126C4888B73B04D8792E6F418`.
Controller hash and individual leg samples are in `controlled-tour-trace.json`.
The start overview was inspected: room art and cards load; some rooms are offline
and the objective overlay obscures the lower-left area. At 15.9% zoom it is not
close-up art acceptance. Other arrival frames are retained without individual
visual acceptance claims.

This does not cover every orientation, arbitrary station topology, autonomous
destination choice, a balanced normal run, or release distribution. The other
nine rollout identities remain outside this combined source-manifest check.
Per-room art cleanup, native progression and shared doorway concerns remain.

## Older-room extension

`windows-31-current-controller-v2` adds Life Support, Hydroponics, Reactor,
Med Bay, Crew Hab and Mycelium Nursery through `rooms/whole-room/export-manifest.json`.
All 31 selected source hashes and 62 PNG decodes pass. The current controller
reaches all 47 placed rooms, with 125 transitions and 9,606 checked steps.
The first attempt timed out at 60 seconds; v2 completed with an explicit
120-second runtime allowance. No close-up visual review is claimed by this run.
BRINE Core, corridor and corner remain outside the selected-source coverage.

## Routing extension

`windows-33-current-controller-v1` adds Corridor and Corner via the routing
manifest. All 33 selected source hashes and 66 PNG decodes pass. The tour reaches
all 50 placed rooms, with 134 reciprocal transitions and 10,290 collision/speed
samples. This extends current-controller coverage to the narrow routing kit in
this layout. BRINE Core is the sole identity outside selected-source coverage;
see `BRINE_CORE_ROLLOUT_AUDIT.md` for its distinct art/component work.

## All 34 identities

`windows-34-current-controller-v1` adds BRINE's registered pearl chamber and
its separately hashed body PNG. All 34 source hashes, 68 source/card PNG decodes
and the body component hash/decode pass. The exported controlled tour physically
reaches all 51 placed rooms, with 135 reciprocal transitions and 10,377 checked
movement steps. Logs contain no assertion errors. Pack SHA256:
`4AC1D1A4BF3327A724823BB490BCE1F76821E6468CB6ABDDBE6FF5CD882F7405`.

This closes selected-source coverage for the 34-identity inventory in one
exported layout. It does not close close-up visual review, arbitrary topology,
normal-run progression, independent overlay motion or release acceptance.
