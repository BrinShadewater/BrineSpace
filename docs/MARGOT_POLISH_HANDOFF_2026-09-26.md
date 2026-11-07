# Project handoff

Updated: 2026-09-26 · Project: BrineSpace · Task: Margot artwork and movement polish

## Objective and acceptance
Owner approved the first-pass look, reported a slight sitting colour shift and requested the remaining actions. A subsequent "keep going" continued into native integration. Full existing state coverage is now installed in the source project; owner playtesting remains useful.

## Accepted decisions and constraints
Keep the selected portrait's white/tabby identity, blue-gray eyes, right muzzle patch and frog bonnet. Match the current detailed painted style and approximately the existing small world scale. Preserve old packs and owner data. Native binding and wake timing changes are limited to Margot; no economy, navigation-rule or save-format changes.

## Current state
`character/margot-polish-v1/` contains preserved generated sources with exact prompts, extracted cells, reproducible build, manifest, 71 clips / 349 frame references, frozen old comparison frames and browser preview at http://127.0.0.1:8773/ (server PID 259380). All existing Margot dry/actions/water state names are covered. 184px frames retain twice the old export density; no palette reduction. Colour source selection is south V3, north V4, original sides V1. New grooming/nap/pet/stretch/yawn/swim sources are recorded in README and expansion provenance. Shared endpoints and reversed recoveries are declared; swimming has a separate surface effect and bonnet anchor. First-pass files are retained under review/.

## Verification
`validate.py` passes 71/71 state coverage, bounds, binary alpha, positive timing, six unique walk phases in all directions, shared action endpoints, source hashes, no source upscale and byte-identical active baseline. JS syntax passes. Browser controls sampled 37 direction/action combinations; sources and registered contact sheets visually inspected. North swim clipping found and corrected. Colour diagnostics and rejected broad-side recolour are recorded. Evidence is under `review/`. No Godot test or native room acceptance; the Bill/sofa scale view is an illustrative composite.

## Next action
Native integration is complete. `scripts/companion_npc.gd` selects the explicit full paths to 8 locomotion / 55 actions / 8 water manifests. Build emits water clearance and preserves original walk stride; waterline is 148px. Wake-before-pet consumes its actual authored duration. ACTIVE_ASSETS and ANIMATION_PIPELINE reflect the selection. New `tests/test_margot_polish.gd` and paired UID cover loaded density, coverage, stride, complete wake, pause and checkpoint restore, with 21 native action captures. `tools/run_margot_check.py` isolates APPDATA and fingerprints the real profile. The test is registered in the crew group.

Native follow-up evidence: animation-expansion PASS; companion-water headless/native PASS (real room routes, flood interruption, pause, restore, draining); new Margot native fixture PASS after correcting its initial artificial navigation/roster setup. Godot 4.7.2. Captures/logs under `output/margot-polish-native/` and `output/companion-water/`; selected dry/wet screenshots copied into pack review. Real owner progress remained unchanged. Earlier full-profile guards recorded concurrent unrelated door-test logs/new hatch fixture; final native-water fingerprints were entirely unchanged. Do not restore or delete concurrent files.

Next: owner playtests the installed source game. No further animation states are missing from the existing contract. A packaged executable has not been rebuilt or release-tested.
