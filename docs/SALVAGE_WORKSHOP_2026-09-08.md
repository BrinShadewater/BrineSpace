# Project handoff

Updated: 2026-09-08 · Project: BrineSpace · Task: Salvage Workshop

## Objective and acceptance
Owner accepted the proposed salvage workshop: heavy bench, tools, dismantled machinery, task lights, parts storage, repair station, crew work/delivery and placement gameplay.

## Accepted decisions and constraints
Engineering charcoal steel/burnt orange, maintained with contact wear. Fixed south entrance, 8 Metal construction. Converts 3 stored Metal plus 2 Power into 1 Rare Mineral per functioning cycle. This uses existing Metal inventory rather than adding a scrap currency. Connected functioning salvage bay reveals Parts Reclamation (+1 Metal/cycle); its research reward stabilizes after three functioning cycles. Costs and hidden-discovery rules remain active. Crew actions do not add another resource payout.

## Current state
45 live room identities. New source art, native alpha exports, prompts, renderer, card and completed-room preview: rooms/underwater/salvage-workshop-v1/. Room database, card/station consumers, shared activity controller, retained carrier rendering, synergy definitions and floor/export/rollout ledgers updated. All three crew inspect, work, carry a tote and unload. Existing character frames are reused with an attached tote; no new carrying character sheet. Sources and UID pairs preserved, PNGs use LFS. Nothing committed, pushed or published.

## Verification
Godot 4.6.1 native art bounds/collision, operating/frozen/offline pixels, completed-room workbench route, paid construction, fixed entrance, deck and Save/Continue pass. Crew test covers three identities, inspection/work/carry/unload, disk snapshot restoration, zero simulation time, suspension and continuous routes; 222 entry/return samples and three viewport sizes. Four carry captures verify corrected tote registration. Economy covers missing inputs, shared budget, suspension, matched-door discovery, hidden forecast and three-cycle stabilization. Regressions: 36 existing crew activity combinations, power expansion and observation room all pass. Final output/workshop-*.log files have no ERROR lines; unrelated wreck image-loading warnings remain. Native visual review is agent review, not owner acceptance.

## Next action
Requested checkout work is complete. Owner can review composition and playtest the provisional conversion rate in a normal expedition. Standalone builds predate this room and were not rebuilt.
