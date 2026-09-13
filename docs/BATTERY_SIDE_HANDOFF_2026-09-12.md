# Battery Array side-art handoff

Updated: 2026-09-12. Project: Brine Space.

## Objective and acceptance
Continue the full room-facing rollout. Owner dislikes side views; equipment must face inward and sit flush against its wall. Native quality matters independently of passing tests.

## Accepted decisions and constraints
New low overhead companions may use an authored east view mirrored for west. Keep doorway clearance, original art, LFS handling and central equipment.

## Current state
Selected assets/battery-directional-v1/side-overhead.png in four east/west section registrations. Added optional mirror_horizontal handling to split_wall_prop.gd using existing library reflection and UV helpers. Preserved previous registrations. First study repeated gauges/switches per unit; corrected source has three gauges and four switches total. Exact prompts and raw provenance retained.

## Verification
Native q1/q3 reviewed: lower broad tops, inward controls, backing cables flush to wall. Baseline/installed comparison proves q0/q2 RGB unchanged and prop metadata identical in all four directions. 176 layouts and existing 20 variant regressions pass 20260912-150326-headless; new mirror behavior additionally reviewed in native images. Existing q0 card retained. Evidence: output/battery-overhead-2026-09-12 and assets/battery-directional-v1/side-overhead-review.json.

## Next action
Continue remaining side-camera repairs across other rooms. Owner aesthetic acceptance remains open; this revision does not complete the broad goal. No export or commit.
