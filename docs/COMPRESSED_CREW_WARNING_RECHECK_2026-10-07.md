# Project handoff

Updated: October 7, 2026 · Project: BrineSpace · Task: exact crew prototype lifetime recheck

## Objective and acceptance

Resolve prototype release warning with reproducible controls, preserving actual Studio, source pixels and save behavior. Full original release scope remains active. Do not suppress warnings or infer a root cause from a clean run.

## Accepted decisions and constraints

No normal backend admission or art/quality change. Native diagnostics use verified isolated profiles and owner fingerprints. Physical flood implementation is temporarily installed only during its controlled native process, with original bytes retained and restored after termination; paired UID stays untouched. One native process at a time.

## Current state

Private driver `output/compressed-crew-2026-10-06/run-physical-flood-control.py` compares runtime flood helper reload with identical helper pixels/code loaded physically before engine startup. Uses existing full-safe-camera diagnostic main/title/grid/player artifacts; normal source source context is current. It restores physical flood file in finally and asserts no concurrent edit before restoration. Original bytes retained. Comparator `compare-physical-flood-control.py` checks entire recorded crew snapshots plus art ownership fields. Artifacts/logs/owner records: `bounds-cache/physical-flood-control/`.

Driver now supports `--fixed-site`, setting site_seed9062026 on the actual diagnostic Main before _ready via node_added. This setup mirrors the maintained packaged fixture pattern; new branch has not yet been run. Output directory `bounds-cache/physical-flood-fixed-site/` separates the next results. Repeat controls sequentially: driver reload --fixed-site, then physical --fixed-site. Preserve old results.

## Verification

- Fresh native original reload control:826 checks,10 cycles,0 failures/errors/warnings/leaked-instance reports.
- Fresh physical-file control:826 checks,10 cycles,0 failures/errors/warnings/leaked-instance reports. Actual Studio remains included. Source flood restored byte-exactly SHA a7a6a10a472cbca7a226c2c6c57d436b73c43106f92ed94647a9f2bc2b7a4174; both owner2,936 unchanged. No current processes live.
- Title texture endpoints identical in all10 rows162.419→166.178MiB. Current normal resource cleanup differs from historical warning context. Do not attribute historical warning disappearance to cleanup, physical loading or camera guards without a reproducing control.
- Comparator exits1 because all10 gameplay crew rows differ plus8 library-image endpoints differ. Detailed game0 difference: James and Marsh have different recovery positions/goal cells/movement paths; Veld matches. Fixture discovers actual procedural recovery sites but did not set station seed. Thus these two runs are independent lifetime/save checks, **not a matched gameplay memory or behavioral comparison**. Failed comparison and raw evidence retained; no test loosened.
- Earlier warning remains **awaiting reproduction**, not fixed or waived. Small later title growth remains unresolved. No new FPS, target-memory, packaged, full motion, hardware or Mac acceptance.

## Next action

Run deterministic fixed-site lanes and verify site/recovery/complete crew snapshots before comparing rendering or memory. If warning still does not reproduce, stop speculative warning-specific rewrites and use bounded regression monitoring in future combined provider testing. Next meaningful provider work is busy40-room simultaneous slot spills/exit, current selected-bank compatibility, loading costs and matched large scene frame pacing. Full original PC/Mac gates and original nine bug checks remain open.
