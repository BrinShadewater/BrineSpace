# Integrated riser-wall collection

## Complete collection — September 26, 2026

All 47 room/corridor IDs now have unique integrated RGBA wall artwork: 42 new edits extend the five existing studies. Each edit references its own original wall for material, colour, perspective and panel geometry. Industrial controls, scientific specimens, habitat pictures/books, medical storage and corridor wayfinding are built into the host panels. Observation-room and archive bookcases remain included.

The gallery defaults to all 47 designs in closed-interior mode. North connections replace the centre slice with the original clear wall; exposed-ocean mode uses original walls and window fittings. The native preview can disable decorations. The gallery's Integrated artwork toggle compares against previous separate fittings, rather than disabling all details. This remains preview-only; production wall decorations stay paused.

`masters/` contains all 47 unmodified generated images; `prompts/` retains exact prompts. `rollout-subjects.json` describes the 42 new subjects. `registrations.json` stores literal resource paths, registered face regions and source/prompt hashes; new entries also record original-reference hashes. `tools/register_integrated_risers.py` reproduces registration and checks completeness, transparent alpha, unique sources and face bounds. Original wall masters remain untouched. `before-native/` preserves prior comparisons for all rooms.

Validation session `8fcd9dca4870441287d0226a92dda121`: 47 designs, 185 native state captures, 44 furnished-room walking checks, zero clearance failures, no logged errors, owner-save fingerprint unchanged. All 44 closed/ocean room pairs were visually reviewed on six sheets in `review/`, plus all three corridor segments and a connected medical-room doorway. Browser search, comparison/window controls, furnished preview and 47/47 default collection checked. PNG paths use Git LFS. New artwork awaits owner visual acceptance; live-game integration is a separate step.

## Earlier study history

### Initial studies

September 26, 2026. Preview candidates; owner visual acceptance pending.

The owner found the separate fittings difficult to read and disconnected from the wall palette. Three whole-wall edits explore details fabricated into the existing panel material: reactor gauges and readout, research sample recesses and printed specimen graphic, and lounge prints and clock attached directly to the fabric panels. Larger shapes, fewer nested frames and restrained colour improve recognition at furnished-room scale.

## Files and rendering

`masters/` preserves the three generated RGBA originals; `prompts/` preserves exact edit prompts. `registrations.json` records source paths, face regions, alpha bounds and image/prompt hashes. Original wall masters remain unchanged. `before-native/` preserves twelve previous native captures.

The gallery defaults to these three studies in closed-interior mode. Integrated artwork switches to the prior separate fittings for comparison. The native preview uses the same registered source regions. Connected north bays retain their original clear centre for doors. Exposed ocean mode retains the existing window treatment. Other 44 designs retain the earlier separate-fitting treatment. This is preview-only; production wall decorations remain paused.

## Verification

Three isolated Godot runs passed: reactor `fe97362bc537477f91ead7e52c2824a1`, research lab `d70e28146e1b45eabc9028d2e5ba335b`, crew lounge `9ac68f4039aa414bb4e43e34c6091b76`. Twelve native state captures, walking checks and owner-save fingerprints passed. Furnished decorated captures for all three were visually reviewed, plus connected reactor and ocean lounge. Browser gallery rendering, comparison toggle and furnished preview were checked visually.

The blue guides in native captures describe the previous narrow fitting/window reserves; integrated art occupies the surrounding physical wall panels. Gallery guides are off by default for artwork review. Remaining work: owner review of this direction before extending it across the remaining collection.

## Bookcase continuation — September 26, 2026

Owner accepted the integrated direction and requested wall bookcases for reading/observatory rooms. The canonical `observation_room` has library tags and a three-walls-of-books description; no separate reading-room ID exists in this gallery. Added observation-room warm timber recessed shelves and data-archive steel reference-book shelves using built-in image generation. Raw masters and exact prompts are retained under their respective IDs, with hashes and measured face registration in registrations.json. All five integrated rooms now appear in the gallery; the remaining 42 retain prior fittings.

Native validation: observation_room session `0b2ee545a6364d83bcf85c4718209ed9`; data_archive session `131b31c5c80a423697560db453af6f2e`. Both passed, eight state captures, owner fingerprints unchanged. Visually reviewed both decorated rooms and observation ocean replacement at furnished character scale. Browser gallery shows 5/47 and the new bookcases. New sources await owner review; production integration remains outside this preview pass.
