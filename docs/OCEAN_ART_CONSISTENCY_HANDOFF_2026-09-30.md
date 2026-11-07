# Project handoff

Updated: September 30, 2026 · Project: BrineSpace · Task: Ocean art consistency and integration

## Objective and acceptance

Review the recent ocean-floor details, rock features and biome materials together for density, style, overhead perspective, size and consistency; verify their existing live renderer bindings. Native visual review is retained alongside automated checks.

## Accepted decisions and constraints

Retain matte natural source colours, production underwater tint and overhead perspective. Keep the polished overhead ridge and selected fine-grain v2 floor materials; the combined review did not justify further raster rescaling. Transparent 512px prop exports and opaque 1024px continuous ground fields serve different roles. Preserve immutable masters, exact generation briefs and rejected versions. Keep deterministic art selection independent of gameplay, collision, saves and map generation.

## Current state

All recent packs remain integrated through `sub_biome_view.gd` and `site_scenery.gd`. Added `tests/review_ocean_art_consistency.gd` with its UID, `tools/verify_ocean_art_consistency.py`, and three pack preloads in `tests/test_runtime_environment_art.gd`. No raster changed during this combined closeout.

The native size board uses a measured 270 physical pixels per cell: small remains span 54–65px, sample rocks 97px, and larger habitat life 130px. These fit existing shell beds, living urchins, scenery and habitat sizes. Ground fields span 9.2 cells with continuous UVs. Reviewed all seven habitat views under production tint, fog and station lighting, including the three alternate floors.

## Verification

- Final native consistency review: zero failures. Evidence: `output/ocean-art-consistency-v1/final-native/` (nine-feature size board, seven habitat captures, density and seed coverage reports).
- 32 seeded generated maps retain their layouts; brine, coral and iron each exercise original and alternate material selection. Other habitats retain their original floors.
- Runtime environment regression: 102 checks, zero failures. Final runner summary: `output/ocean-art-consistency-20260930-134707/summary.json`.
- Source audits: 11 scoped packs, 36 identities and 105 raster versions; hashes and raster records pass, zero unregistered candidates. Ledger: `output/ocean-art-consistency-v1/source-audits.json`.
- Both native jobs ran with scratch APPDATA/LOCALAPPDATA. All 2,924 real owner files remained unchanged.
- Scoped whitespace check passes; script UID retained. Other concurrent workspace changes preserved.

## Next action

Requested source-game integration and combined review are complete. This evidence covers environmental art and a dedicated visual fixture; it does not establish a new playable export or paid expedition acceptance. Further art work can proceed from this accepted density and perspective reference.
