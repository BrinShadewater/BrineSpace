# Project handoff

Updated: 2026-09-26 · Project: Brine Space · Task: furnished corner-counter room preview

## Objective and acceptance
Show new counters in a real room renderer with characters and other objects. Native interactive preview and screenshots complete; owner visual acceptance pending.

## Accepted decisions and constraints
Isolated preview only. Preserve owner room layouts and saves. Use proposed 0.34 world units per source pixel and actual crew animation scale. Existing reactor shell/riser study provides the room, not a production redesign.

## Current state
tools/preview_corner_room.gd and tools/preview_corner_room.ps1 launch the native preview. layout.json records five full artwork paths, positions and provisional collision rectangles: northwest wood counter, northeast sink counter, reading chair/table, supply shelf and server. Three crew use real art, with Bill walking and Marsh/Veld stationary. Captures are in captures/. Interactive preview launched after verification. Space pauses, D toggles doors, Tab compares wall versions, S saves screenshot, Escape closes.

## Verification
Godot 4.7.2 native verification passed: all five props survive render filtering, doorway navigation nodes clear, walking exceeds 160 world units with zero segment-clearance failures; pause holds. Owner save fingerprints unchanged. Final revised-open screenshot visually reviewed. Preview-only library/sp-preview identifiers let fixture props through the current art filter without changing production rules.

Collision rectangles are conservative authored fixture estimates, not production registrations. Whole-assembly depth sorting can occlude a character incorrectly near an inner L corner; this fixture places stationary crew clear of that overlap. Rendering proves visual context and movement checks cover this fixture only, not all rooms or interaction poses. Counters still read compact beside crew; final working height remains owner judgment.

## Next action
Refinement completed after the audit: layout now uses `assets/corner-counters-refined-2026-09-26/` wood/sink exports. Seven draw regions replace five single-depth props; north run and return sort independently. The formerly obscured character is back near the sink and visibly draws in front correctly. Native movement/doorway/pause verification passed with owner saves unchanged. This supersedes the earlier screenshot workaround for that demonstrated overlap.

Follow-up ART_AUDIT.md records native comparisons, warm/light wood drift, flatter sink treatment and unresolved L-return depth/occlusion. Preview canvas now explicitly uses nearest filtering; native verification and screenshot review repeated successfully. Existing already-running preview processes retain the prior filter until relaunched.

Owner reviews interactive room and screenshot for scale and fit. Refine geometry/size or split L-counter depth regions if requested before production integration.
