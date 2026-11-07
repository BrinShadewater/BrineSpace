# Character consistency handoff

Updated: September 27, 2026. Project: BrineSpace.

## Objective and acceptance

Continue Veld continuity repair while keeping identity, palette, tone and hue stable across poses. Installed 130 focused corrections and a whole-cast colour drift audit. Agent visual samples reviewed; no new owner acceptance claimed.

## Accepted decisions and constraints

Preserve poses, timing, pivots and locked palettes. Deterministic restoration uses original source artwork. Fixed walk-family tone curves affect neutral cloth below the collar; no per-frame colour grading or new generated art.

## Current state

`character/veld-consistency-v1/` preserves before/after images, curves, hashes, a 346-state comparison viewer and native evidence. Fixed the over-deep bare-head mask in `tools/prepare_veld_east_identity_chain.py`, propagated 34 shared Veld collar frames, and corrected 96 Veld/Branforth bare/equipped walk frames. Added guarded `tools/repair_crew_consistency.py`, whole-cast `tools/audit_character_colour_lock.py` and focused tests. Updated palette viewer/native review and helmet fixture for the explicit new correction layer.

## Verification

Four Python tests pass. Colour audit: seven palettes, 8,575 PNG paths, 1,444 selected state variants, zero unexpected changes. Native real loaders: 792 checks, zero failures, every corrected export compared. Isolated APPDATA and real profile unchanged. First native attempt had an expected-image path join error; corrected rerun passed. Browser and native visual samples reviewed; no exhaustive visual certification claimed.

## Next action

Review the installed consistency comparison. Future art must retain the fixed palette and source-family tone contract, then pass visual review before lock updates. Remaining source differences include walk softness and Marsh work/swim anatomy/style. No executable rebuild.
