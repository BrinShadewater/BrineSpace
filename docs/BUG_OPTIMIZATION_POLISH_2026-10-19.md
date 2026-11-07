# Bug, optimization and polish pass — October 19, 2026

Local source pass requested by the owner. Current Desalination, crew traffic, Marsh charging, later-loop stabilization, costs, room rates and accepted look remain intact.

## Changes

- **Clone Lab Power accounting:** the shortage preflight still skipped a lab when berths were full and treated each earlier lab as adding an unnamed survivor. The real economy already produces Data without spawning crew. Removed those retired conditions: every fuelled, enabled lab now counts its demand, including multiple labs. Insufficient station Power causes the existing station-wide blackout; missing Biomass or suspension still prevents that lab from drawing Power.
- **Finite cargo feedback:** Metal/Data hover tips and reserve details now separate Mining/Salvage cargo per extracted load from recurring room output. Two Mining bays each list +2 per load; their cargo is not presented as +4 per load or fixed production each cycle. True Refinery production, bay Power upkeep, offline reasons and exact stored delivery totals remain visible. Copy explains finite stock, docking and delivery timing; one-cycle headings use the singular.
- **Bounded optimization:** each economy forecast sorts room priority once and reuses that order in both budget passes. No persistent order cache or invalidation scheme. Sprinkler controls reuse their sampled outlook for the tooltip instead of querying the station again. Existing quarter-second polling and immediate explicit refresh remain.

Changed runtime files: `scripts/main.gd`, `scripts/room_fire.gd`, `scripts/hardware_panel.gd`. Added two paired regression fixtures and registered them in `tests/index.json`.

## Verification

- Demonstrated pre-fix failures: four economy/ordering assertions and seven cargo/polling assertions. Final new fixtures pass, including full/part-filled berths, multiple labs, fuel starvation, suspension, read-only forecasts, duplicate bays and delivery window wording.
- **10 focused headless test files pass**: economy consistency, cargo feedback, real crew berths, Power expansion/regressions, resource delivery ledger, room fire, sprinkler feedback and both stabilization/checkpoint fixtures. Native fire gameplay, correctly routed out of headless, passes **36 checks**.
- **39 native presentation/continuation checks pass**. Metal and Data panels, their scrolling lower sections, and room links reviewed at 1600×900 and 960×540. Supplied full-berth lab fixture reproduces the shortage, preserves unpaid inputs, writes/validates/restores its checkpoint, and recovers operation with one more stored Power. This fixture sets crew count for the accounting case; it is not a fresh crew-recovery run.
- **96 seeded mixed-station forecasts match the pre-change output byte for byte**; those parity cases exclude the intentionally corrected Clone Lab scenarios. A 121-room operation-count fixture confirms two priority sorts become one. A changed-fire control poll uses one station-list read with stored Power, down from two; unchanged frames before the poll read none. These are operation counts, not measured FPS or CPU-time improvement.
- All **2,971 player files**, **40 other protected source/art inputs**, and the signed Windows ZIP size/mtime match the before receipt. No art, release export, signing, upload, Git integration or cleanup.

Evidence: `output/bug-optimization-polish-20261019/FINAL.json`, `preservation.json`, `session.patch`, focused/native logs and reviewed PNGs. Initial visual fixtures accidentally reopened an already-open journal and scrolled its hidden text backing rather than the widget scroller; corrected fixtures assert the selected resource and actual scroll movement. Earlier captures are retained separately. Existing shutdown resource-cleanup messages in the stabilization fixture are retained in its log; no script failure or new runtime error was observed in this pass.

## Remaining scope

Source only. Packaging/release gameplay, broader pacing, frame-time/memory/endurance, physical Apple testing and general large-station acceptance remain separate. No balance values were retuned. The next useful acceptance step is owner play in an isolated current-source run, then the maintained release checks if a Windows candidate is requested.
