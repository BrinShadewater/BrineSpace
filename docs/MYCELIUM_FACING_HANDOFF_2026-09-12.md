# Mycelium Nursery facing handoff

## Objective and decisions
Continue all room directions. Preserve populated cultivation state and inward
service access under the south overhead camera.

## Changes
New source/prompt and previous registration/layout in assets/mycelium-directional-v1.
Active south registration and q2 defaults place bank flush at y184. Duplicate
reservoir explicitly omitted. New tools/compare_room_art.py reports native pixel,
inventory and placement differences. Coverage, bible and workflow updated.

## Verification
Final native q2 reviewed. Only south-bank pixels change, all prop IDs preserved;
q0/q1/q3 identical, q0 card unchanged. 176 routes,20 variants,188 layout keys pass.
Comparison tool demonstrated on rejected duplicate-reservoir capture and final
capture. Evidence output/mycelium-directional-2026-09-12/verified-comparison.json.
PNG LFS attribute confirmed. No export or owner visual acceptance claimed.

## Remaining
Other Mycelium directions need facing review. Other catalog families and missing
banks remain in scope; full goal active.
