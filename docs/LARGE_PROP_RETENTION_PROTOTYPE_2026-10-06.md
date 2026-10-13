# Project handoff

Updated: October 6, 2026 · Project: BrineSpace · Task: remaining large-room prop rendering

## Objective and acceptance

Reduce measured static prop work without changing pixels, effect clocks, ordering or default quality. Private prototype only; full PC/Mac release gates remain open.

## Accepted decisions and constraints

Use existing RoomContentCanvas static/live splitting for eligible dry library props. Keep body/effect pairs adjacent in original prop order; keep offline overlay after the complete prop group. Wet, portable, custom, aquarium and drone-dock cases use original drawing. Stable per-room context/key preserves layout/rotation/operating/bounds changes; advance only live effects between changes. Inherit parent material and filtering.

## Current state

Normal source unchanged this turn. Attribution: `output/large-prop-attribution-2026-10-06`. Private helper: `output/large-prop-retention-2026-10-06/large_room_canvas.gd`. Validated patched execution probe under `execution/`; initial `prepare.py` predates its execution assertions. Matched physical station fixtures/results under `station/`.

## Verification

Native per-stage attribution, three idle 1/2/4x phases: 147 eligible props/frame, body/shadow drawing ~2.90–2.93 ms, live screens/effects ~0.93–0.95 ms, placement/flip ~0.111–0.114 ms. Values sum across all 12 large rooms; probe overhead means not whole-frame acceptance. No special portable/drone drawing recorded.

Private native 135 checks, zero failures / 80 exact image pairs. Existing four-room composition/material/filter/lifecycle suite plus explicit execution checks: real retained content slots built, initial static drawing occurs, static draw counters remain unchanged while clock advances, and changing live effects still match immediate original pixels. Covers dry/flooded fallback, offline ordering, parent material, nearest/linear, layout/mission/ports, replacement, visibility and owner release within original fixture scope.

Matched native mixed40-room pair: six idle/pan 1/2/4x phases, 60 frames each; current normal large-base retention is baseline. Candidate executes 12 prop canvases / 213 slots, prepares24 constant, static_draws236 constant, advances2870→6470, live_draws15897→35697. Live-room CPU profile includes prop slot callbacks: baseline10.16–10.66 ms → candidate7.52–8.10 ms; ~2.47–2.71 ms saved. Detailed `children_usec` console field excludes the newly named prop-slot label, so use the complete live_rooms total rather than that partial detail sum. Private offline overlay callback time is not individually recorded yet; whole-frame timing includes it. Fix diagnostic accounting before normal admission.

Whole-frame p95 baseline52.97–64.06 ms →46.26–61.11 ms, all six lower. One pair is promising, not packaged or three-run release acceptance; all frame gates still fail. Crew/drone/door/light/power/zoom states equal. Texture history differs during intermediate phases; final3036.131 MiB equal. No memory saving claim. Fixtures retain private crew/drone experiments and debug=true, not normal-release certification.

All successful processes clean and terminal; each 2,936 owner files unchanged. No art, simulation timing, engine or quality-setting changes.

## Next action

Account offline overlay child timing; check actual shared station LIVE composition with ordinary props/active BRINE signals using new helper, then install into normal large-room module and add permanent execution/static-retention tests. Verify actual normal-source test and an appropriately justified matched comparison after those changes. Continue whole-frame renderer/system work; neither prop optimization nor earlier Moonbay optimization meets 16.7-ms target.
