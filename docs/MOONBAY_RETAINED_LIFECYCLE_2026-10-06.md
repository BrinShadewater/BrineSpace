# Project handoff

Updated: October 6, 2026 · Project: BrineSpace · Task: retained renderer lifecycle/material admission checks

## Objective and acceptance

Close remaining demonstrated risks before normal retained large-room integration. Preserve appearance, ordering, filtering, materials, layout mutation and resource lifetime. Full PC/Mac release performance gates remain open.

## Accepted decisions and constraints

Private large-room slot/base/prop chain explicitly inherits the LIVE parent's material so original parent-drawn large-room artwork keeps that material. Flooded equipment stays in the shared parent layer, with the normal per-frame hide/reconfigure contract. No default effects or art change.

## Current state

Corrected private helper: `output/moonbay-retained-lifecycle-2026-10-06/large_slot.gd`. Validated fixture is the patched `probe.gd`, then `stable-filter/probe.gd`; initial `prepare.py` is archived draft preparation and does not contain subsequent fixture corrections. Normal runtime/test index unchanged this turn. Do not regenerate the validated fixture from that draft.

## Verification

Final native lifecycle suite: 77 checks, zero failures, 76 exact image pairs. Four large-room types, all rotations, room-type replacement, dry/flooded overlap, offline overlays, nearest/linear filtering, inherited shader material/modulation, plus stable room state across filter/material transitions. Lifecycle sequence covers wet→dry, shelf helmet visibility, station ports/opening, mission water/clock changes, merged layout/door-style change, hide/show recovery, removal and observed whole-container release. This is renderer-container coverage, not actual Main demolition/save or layout Studio acceptance. Owner layouts were not imported.

Initial expanded fixture failures exposed missing fixture contracts: candidate parent did not hide the shared wet layer, and lifecycle edits refreshed only Moonbay while reference redrew/reconfigured all flooded rooms. Actual Grid already hides the shared layer and configures all visible slots each frame. Corrected fixture models those contracts; rejected logs retained. No runtime wet-cleanup fix is claimed.

Shared-state mixed-station LIVE comparison: `output/moonbay-station-composition-2026-10-06/active-signals`. Twelve exact pairs across three zoom sizes and four mission phases pass with all 40 room bounds on screen and 248 ordinary slots visible per side. Dedicated fixture exposes core north riser, and subclass supplies operating=true/clock=1.25 at actual BRINE signal calls: 12 eligible riser calls and 24 operating view calls per renderer. The preceding `signals` probe established eligible calls but not operating prerequisite; do not use it alone as active trace coverage. Normal gameplay topology/state remains unchanged outside scratch fixtures.

All successful native processes clean and terminal, each 2,936 owner files unchanged. No timing measurements in these image tests. Prior ~6.82–7.22-ms private matched CPU gain retains its original scope; material inheritance revision has not had a new station timing pair. No release/FPS/memory admission.

## Next action

Move corrected helper and complete retained Moonbay key into normal scripts with paired UIDs; integrate ordered large-room slots into Grid and account child callbacks in normal diagnostics. Add permanent native material/lifecycle tests and test actual Grid removal/culling/replacement; verify current normal source and a justified matched station pair. Preserve immediate fallback for Studio/previews and non-retained paths. Then continue other measured large-room/render/system hotspots; p95 still well above 16.7 ms.
