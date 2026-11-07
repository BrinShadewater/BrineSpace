# Veld extended material pass

Updated: 2026-09-27. Project: Brine Space.

## Objective and acceptance
Continue colour consistency beyond skin/blue/graphite, preserving established motion.

## Accepted decisions and constraints
Locked v4 targets, separate brown hair/silver streak and deterministic remapping
remain authoritative. Owner is on mobile; preview access is not required to continue.

## Current state
character/veld-animation-pilot-v6 adds bounded hair, silver, ivory and bright-steel
masks and authored ramps to all 24 pilot frames. No new poses were generated. Earlier
pilots and sources retained. Native review tool supports v6 with existing paired UID.

## Verification
24 alpha masks identical to v5; exact inspection/idle entry and exit retained.
Geometry validator: zero errors/warnings. Native player: 100 checks pass. All 2670
real-profile hashes unchanged under isolated APPDATA. Contact sheet, diagnostic mask
and native render inspected. Material boundaries are heuristic: tiny logos/fasteners
can share steel treatment; dark metal shadows and instrument pixels remain caveats.

## Next action
Expand missing facing directions and helmet coverage using the established body,
palette and endpoint contracts. Continue inspecting material boundaries as new poses
are introduced. Candidate acceptance and station integration are still pending;
no runtime selection, export or commit in this pass.
