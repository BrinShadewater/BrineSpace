# Open-loop station operations

Implemented September 6, 2026 for the open-ended station flow.

- Construction button in the existing station panel opens Journal / Construction.
  The list shows actual paid queued/assigned orders, builder phase, assembly
  percentage, global pause, unavailable bay power and blocked exterior routes.
  Selecting an order closes the journal and locates its unbuilt footprint.
  Journal pause behavior remains unchanged. Completed orders leave the list.
- Station Health starts with at most three actionable priorities: immediate
  oxygen/food/power depletion before forecast room interruptions. Resource links
  open contribution details; room links locate the affected room. Deliberately
  suspended rooms remain in the full report but are excluded from priorities.
- Pattern Watch shows learned, connected, unstabilized patterns, preferring those
  already making progress. The Patterns journal retains all details. Existing
  discovery bursts and clickable toasts remain; unknown recipes stay hidden.
- New-loop drafting stages existing foundation copies: Solar Array, Mining Drone
  Bay and Hydroponics in the initial three, then Life Support and a corridor.
  No additional cards, unlocks, free costs or failure exemptions are introduced.
  Continue retains the saved hand and deck rather than restaging it.
- Room draw passes skip rooms beyond a one-cell margin around the scrolled view.
  Simulation, adjacency, lights and crew continue using the complete station.

## Evidence

`tests/test_station_operations.gd`: actual paid order, queue page, footprint link,
phase transition, pause/offline explanation, completion, hidden/known pattern
progress, priority cap/links, and 500 deterministic full-pool draft seeds.
Native queue capture: `output/operations-queue.png`.

Before staging food/support, the first Hydroponics or Life Support appeared at
mean draw 18.24, worst 44, across 500 full-pool seeds. Afterwards food is draw 3
and Life Support draw 4 in all sampled seeds. This is a draft availability sample,
not a human playthrough or proof of overall resource balance.

Native 1600 x 900, uncapped, 25-room fixture (`tests/profile_station.gd`):
close-up before culling 37.39 ms/frame, 2566 draw calls; after culling 24.26
ms/frame, 1835 draw calls. Approximately 35% lower frame time. Expanded Fit Station
still measures about 35.35 ms/frame because almost every room remains visible.
Paused close-up full-frame pixel comparison with culling off/on is identical.
Measurements apply to this machine and fixture; they do not establish universal
60 FPS. Logs: `output/operations-profile-all.log`, `operations-profile-final.log`.

Two small compile repairs were also needed in concurrent drone work: consistent
indentation and an explicit boolean in drone_fleet, and Vector2i inference in
drone_routes. Their gameplay logic was preserved.

Save/Continue, discovery progression, drone lifecycle, the finite-load fleet
state-machine fixture and native shared-menu tests pass. The older fleet test
assumed extraction stopped after one externally accrued payload; it now uses a
single-load finite site so duplicate-payment assertions remain meaningful under
the concurrently introduced deposit system.
