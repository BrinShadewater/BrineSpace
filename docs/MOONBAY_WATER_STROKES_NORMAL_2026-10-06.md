# Project handoff

Updated: October 6, 2026 · Project: BrineSpace · Task: cached water stroke submissions installed

## Objective and acceptance

Continue full PC/Mac performance readiness. Reduce the dominant measured large-base command cost while retaining exact antialiasing, blend order, clocks, scale, materials and default effects. Installed source improvement; no release certification.

## Accepted decisions and constraints

Only cached full-water, zero-clock commands combine consecutive supported open strokes. Moving/partial water remains on its original renderer; unsupported strokes retain original commands. Existing per-canvas16-entry lifetime stays bounded. Geometry contains points/colors/indices, no textures/nodes/RIDs. No artwork, gameplay, owner layouts or experimental texture-provider admission.

## Current state

- `scripts/water_stroke_triangles.gd` and paired UID: ordered core/antialias strips, native float precision and original end-cap/seam geometry.
- `rooms/large-rooms/moonbay.gd`: WaterCommands combines adjacent supported strokes; original timing and command order retained. Internal `--reference-water-strokes` flag provides current-source control. Cache-build timing metadata is additive and only collected on preparation.
- Permanent native tests/UIDs: `test_water_stroke_triangles.gd`, `test_moonbay_water_batch.gd`, registered in test index.
- Godot attribution and MIT notice: `NOTICE.md`, `assets/licenses/godot-engine-MIT.txt`. Manifest special-file allowance and raw exporter include the referenced notice; unrelated text remains unselected. New manifest regression covers that requirement.
- Private proof, native source comparisons and captures: `output/moon-water-strokes-2026-10-06/`. Normal benchmark uses actual Main/Grid/crew/drone source, not private texture providers. Existing dirty changes preserved; no commit/export/upload.

## Verification

Per-type renderer omission attribution: Moonbay accounts for about2,133 of the measured2,687 large-base calls; Tidal~241, Hydro/Storage~156 each. Four native room-type lanes preserve recorded crew/world states; owner2,936 unchanged. Primary-source review identifies three polygon strips for antialiased polylines and independent polygon batches; native comparisons, not upstream revision assumptions, establish this implementation's output. [Godot canvas geometry source](https://github.com/godotengine/godot/blob/master/servers/rendering/renderer_canvas_cull.cpp).

Private stroke180 pairs and complete-room135 checks/80 pairs pass. Installed permanent tests independently pass180 visible exact stroke pairs and135 checks/80 exact overlapping room pairs; zero failures/errors/exit warnings/leaks. Covers fractional scales, mirrors, overlapping curves, repeated points, clamped sharp joins, flood shader, room rotations/filter/material/offline/clock/layout/filter transitions and container release. All owner2,936 files unchanged.

Private matched40 first pair: all six full crew/drone/door/light/power/zoom states equal, textures equal, no missing art/errors/selected ordinary duplicates. Calls~6513→5088 (about1,425 fewer); renderer CPU lower2.5–2.8ms, GPU lower1.9–3.6ms. All six p95 lower in that pair; still far above release target. Initial cached preparation maximum4.542ms per canvas,13.510ms across three bays,26,712 cached vertices/six batches; stable through phases.

Installed actual-normal matched40 pair: all six recorded full states and texture endpoints equal; clean native completion, owner2,936 unchanged. Renderer CPU lower2.52–2.72ms, GPU lower1.90–2.50ms in all phases. Calls similarly~1,425 lower. Cached preparation max4.701ms/canvas,total13.877ms; no recurring base-callback increase. Final normal screenshot inspected; not motion or packaged acceptance.

| Phase | Original-command p95 ms | Installed p95 ms |
|---|---:|---:|
| Idle1x |41.507|38.194|
| Pan1x |41.906|40.219|
| Idle2x |40.395|37.947|
| Pan2x |44.180|39.585|
| Idle4x |54.392|53.328|
| Pan4x |49.279|49.538|

Overall frame result improves at1x/2x;4x remains mixed. Normal texture endpoints~3.63→4.29GiB still fail3GiB large-scene budget. Source readiness12.415/12.483s, one observation, no loading improvement. Neither pair establishes three-run certification, target-GPU performance or Mac acceptance.

Release manifest regression fails before notice allowance,10 tests pass after both path guards corrected. Read-only full selection36,243 files includes helper through Moonbay and notice through helper. Whitespace and unique paired UIDs checked. Raw exporter notice addition is source-validated; refreshed executable/PCK audit remains pending.

## Next action

Investigate remaining measured sustained preparation/rendering and4x upload/simulation stalls; keep private crew/drone storage work distinct. Add actual title/save/Continue and larger endurance coverage for the installed source as part of release validation. Freeze current accepted source and refresh packaged Windows checks/PCK audit, including notice. Original memory/loading/frame gates, nine packaged reports, two-hour large soak and actual Windows/Mac certification remain open.
