# Latest portraits installed

Updated: 2026-09-09.

## Objective and accepted decisions
Owner requested installation of the latest complete portrait set after suit and lighting revisions. BRINE V14; Bill/Veld/Branforth lighting V1; Marsh/River/Josh backgrounds V1; Margot realism V3.

## Current state
Updated scripts/architects.gd selection portrait paths, scripts/crew_comms.gd BRINE path and scripts/companions.gd canonical companion loader. Replaced three canonical companion images and refreshed provenance/hashes in character/companions/manifest.json. Prior versioned sources retained. Complete runtime path inventory: character/installed-portraits.json. Source checkout updated; existing executable not rebuilt.

## Verification
Native fixture adapted from playtest_crew_comms.gd loaded all eight portraits, exercised all four architects and BRINE in comms, plus unlocked architect/companion selection at 1600x900 and 960x540. Captures and invocation script retained under output/portrait-install. Visually reviewed selection top/bottom and BRINE/Branforth comms. Bubble bounds/occlusion/clock test passes. Scoped diff whitespace check passes.

Native log also contains two room-dressing assertions for thermal_pumps and thermal_service_table, plus image-loading export warnings outside the portrait loaders. Portrait-specific assertions passed, but this is not a clean global game or packaged-build validation. Existing BRINE bubble lanes remain clear of the new face/hair at reviewed sizes; no mask change needed.

## Next action
No portrait installation work remains. Existing packaged executable needs rebuilding separately to include these changes. Thermal room assertions remain outside this art task.
