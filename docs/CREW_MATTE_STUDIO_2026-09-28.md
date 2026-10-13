# Project handoff

## Objective and acceptance
Owner preferred matte+linear study and authorized continuation into a Layout Studio room preview. Production adoption still awaits room-context review.

## Current state
`tools/bake_crew_matte_preview.gd` GPU-renders the selected shader into673 temporary preview frames under `character/crew-matte-studio-v1/`. The bake uses exactly the study shader, including Veld's approximate face-region warmth adjustment. Original textures unchanged.

`scripts/room_scale_preview.gd` has an opt-in finish_preview_manifest. Only preview actors given this path load shaded frames and use linear CanvasTextures; room drawing/filtering and normal game assets remain unchanged. Full-art reloading reapplies the preview override. `tools/preview_crew_layout_studio.gd -- matte` enables it for Bill, Veld and Branforth.

## Verification
Native checks confirm three moving actors, latest frame counts, unchanged furnishing draft and character-only linear textures. Nine screenshots cover Research Lab, Medical Bay and Crew Hab at zoom1.25/0.83/0.42 (approximate close/mid/wide). First capture was obscured by recovery dialog in an older scratch profile; rerun uses a fresh isolated profile with only copied room_layouts.json. Do not discard or restore the owner's recovery files. Final evidence in checks.json and verify.log.

## Next action
User reviews the live matte Studio preview and room screenshots. Keep side-head proportions, Branforth side gait and Bill south style open; a finish does not fix those. No generation credits used, last confirmed56. Do not replace production art automatically.
