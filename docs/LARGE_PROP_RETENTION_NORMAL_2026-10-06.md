# Project handoff

Updated: October 6, 2026 · Project: BrineSpace · Task: normal large-room prop retention

## Objective and acceptance

Install measured static/live prop separation with unchanged selected visuals, effect clocks and layer order. Full PC/Mac release gates remain open.

## Accepted decisions and constraints

Eligible dry library props reuse existing RoomContentCanvas body/effect slots in original order. Final offline wash uses a correctly ordered child. Wet/portable/custom/aquarium/drone cases retain original rendering. Parent material/filtering, layout/rotation/bounds/operating updates and live clocks preserved. No art, animation-frame, quality, simulation or engine changes.

## Current state

Normal `scripts/large_room_canvas.gd` now contains retained prop context/content adapter and final overlay, retaining its existing UID. Updated `tests/test_large_room_retention.gd` preserves its UID/native index registration. All child paint callbacks including offline overlay contribute to normal diagnostics. Original prototype overlay omitted a separate diagnostic callback; normal implementation fixes accounting.

## Verification

Actual normal-source native 135 checks / 80 exact raster pairs pass, including static draw execution and no static redraw while effects advance; material/filter/clock/layout/visibility/replacement/removal/owner lifetime checks retain previous scope. Diff whitespace check passes.

New-helper shared-state native LIVE composition: 12 exact pairs, all 40 room bounds, 248 ordinary prop slots visible per side, active BRINE riser/view execution confirmed. Physical candidate explicitly preloads corrected new helper. Probe excludes floor/wall/foreground passes and is not full gameplay certification. No owner layout imports or actual Main demolition/save in this fixture.

Installed normal helper matched against reconstructed frozen pre-prop normal helper (original immediate props and identical diagnostic aggregation), six mixed40-room idle/pan 1/2/4x phases, 60 frames each. Candidate executes12prop canvases/213slots; prepares24/static_draws236 constant, advances2870→6470/live_draws15897→35697. Live-room CPU including all callbacks:10.06–10.62 ms →7.49–7.99 ms, savings2.34–2.68 ms/frame. Whole-frame p95 baseline51.84–68.13 ms →46.51–60.86 ms, all six lower; still fails release frame gates. Full crew/drone/door/light/power/zoom snapshots equal, texture counters equal in every phase, final3036.131 MiB. No memory saving claim.

These physical fixtures use private crew/drone asset experiments and debug=true, not a packaged release or minimum hardware certification. Two scoped matched comparisons support CPU benefit but do not replace three candidate certification runs. All successful processes clean/terminal; each 2,936 owner files unchanged. Evidence: `output/large-prop-retention-2026-10-06/{composition,normal,normal/station}`.

## Next action

Reattribute complete renderer/backend work with current optimizations. Current measured idle renderer CPU~15.30–15.67 ms and GPU~13.34–15.08 ms in prototype pair; not additive timings or GPU bottleneck proof. Static command retention reduces preparation but not necessarily renderer submissions. Investigate actual layer/command costs and overlap before choosing batch/geometry or overdraw changes. Preserve exact output/default quality and full frame/memory/Windows/Mac release gates.
