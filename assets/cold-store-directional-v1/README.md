# Cold Store directional side banks — September 12, 2026

New family for a previously custom-sprite room: west refrigerator bank and east
food-storage bank. Source references are the original fridge-v2.png and rack-v2.png
under rooms/underwater/cold-store-v1. Exact prompts are adjacent text files.
Three generations, two selected; initial rack rejected for a forward-facing crate
handle and preserved as rack-east-rejected-v1.png. The revision puts that handle
on the inward left edge. Straight back rails face the walls.

Read-only exterior-neutral polygons, threshold 228/spread 22; source RGB pixels
unchanged. Registrations also live in rooms/full-wall-v1/registrations as
side-cold-store-fridge-west.json and side-cold-store-rack-east.json. Banks span
300 world units and touch x=-184/+184. Original sources and layout values retained.
The view preserves original fridge/rack IDs and a live powered refrigerator
indicator. This is a composition revision: three refrigeration modules replace
the earlier single double-door fridge, and shelf inventory changes are visible.

Cold Store has a fixed playable orientation. That native view and refreshed card
are visually reviewed; original art is retained for alternate odd-quarter views.
North/south bank source coverage remains pending in the full-catalog ledger.
176 preferred-layout route cases, 188 layout keys and 47 card bindings pass.
PNG LFS filters verified. No executable export, commit or publication.

Evidence: output/cold-store-directional-2026-09-12/comparison.png. Card consumers
now select assets/cold-store-directional-v1/cards/cold_store.png.


Cold Store state follow-up (September 12): enabled custom_library_draw on the
registered side banks. Native q0 OFF and two powered timestamps show changes only
in the 2x2 indicator area at(139,289)-(141,291). Offline output is RGB-identical
to the retained card. Evidence: output/cold-store-state-2026-09-12/checks.json and
comparison.png. This verifies the formerly bypassed refrigeration pulse.
