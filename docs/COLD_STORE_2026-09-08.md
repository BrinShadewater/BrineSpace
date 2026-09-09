# Project handoff

Updated: 2026-09-08 · Project: BrineSpace · Task: Cold Store, smaller matte revision

## Objective and acceptance
Owner requested continued room expansion, then rejected the Cold Store props as too large and shiny. Current V2 reduces scale and brings materials closer to existing station art.

## Accepted decisions and constraints
Fixed north/south through-aisle. Costs 8 Metal, adds 40 Food and 20 Biomass capacity, uses 1 Power per cycle. Outages retain capacity; no spoilage. A connected functioning Galley discovers Cold Chain (+1 Food/cycle), stabilizing research after three functioning cycles. Economy unchanged by the art revision.

## Current state
47 room identities. Assets and current renderer in rooms/underwater/cold-store-v1/. V2 uses matte charcoal, muted ochre and simpler pixel detail instead of polished silver, bright frost and realistic containers. Width reduced from 124 to 92 units (25.8%); collision depth 74 to 54. Ground anchors and stock approaches preserved. New source/cutout/registration files use V2 suffixes; V1 retained as superseded. Card, export hashes and CURRENT_STATUS updated. Exact edit prompts in matte-v2-prompts.md. Three crew use existing idle art for stock checks. Fixed-orientation hints use the selected blueprint's actual name/doors. No commit, push or package rebuild.

## Verification
V2 native bounds, both-door aisle, collisions and operating/frozen/offline checks pass: output/cold-store-matte-art.log. Native completed-room visual review confirms reduced scale and glare. Updated paid construction, connected core/store/galley routes, deck, Save/Continue and all three stock-check actions pass, with disk snapshot/freeze/suspension coverage and 556 continuous route samples: output/cold-store-matte-gameplay.log. Earlier economy and 36-case crew regression remain relevant because this revision changes only art and footprints. PNG LFS verified. Native review is agent review, not owner acceptance.

## Next action
Owner visual review of the smaller matte composition. Requested revision is installed in the checkout; standalone packages remain unchanged.
