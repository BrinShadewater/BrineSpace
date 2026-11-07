# Project handoff

Updated: October 15, 2026 · Project: BrineSpace · Task: Godot research

## Objective and acceptance

Owner requested deep research into performance/pacing, rendering/text glitches and
renderer/engine migration. Completed source-linked report in
`docs/GODOT_RESEARCH_2026-10-15.md`. Research only; no runtime experiment or code change.

## Accepted decisions and constraints

Preserve current appearance and accepted fixes. Research recommendations are proposals,
not approved renderer/engine changes. Current Compatibility4.7.2 remains the default.
Use primary sources, pin engine behavior to ed1daf0bf, distinguish issue reports from
local reproduction, retain rejected experiments and avoid new benchmarks for paperwork.

## Current state

Confirmed polygon/mesh batching restriction in both pinned renderer families;
no verified newer stable remedy. ANGLE/Metal exists in pinned Mac source despite
inconsistent setting documentation; actual binary capability/fallback needs checking.
Reviewed local upload, placement, card and precision evidence. Q-like zero remains
unreproduced; black large-room opening was a backing-color fix. Windows-only packet
fallbacks and private LOD baseline limit extrapolation to normal delivery/Mac.
CURRENT_STATUS records this research milestone; game/assets/delivery unchanged.

## Verification

Official release archive, documentation, pinned sources and upstream issue/PR status
checked October15. Two independent read-only research scopes supplied batching and
visual/precision evidence. No Godot/test/benchmark jobs or owner-data writes performed.
Existing tests are evidence for their recorded revisions, not new research validation.

## Next action

Recommended: frozen same-version renderer/driver comparison with exact visual gates,
first Windows nativeGL/ANGLE/Mobile, then real Mac control/ANGLE/Metal as available.
Record effective driver and reject silent fallback. Separate normal-source and private
LOD cohorts. Correlate unexplained stalls with OS/thread/present data. Full procedure,
risks, upstream sources and alternative-engine decision gate are in the report.
