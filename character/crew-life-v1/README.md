# Crew life v1

Owner-authorized expansion for Bill, Veld and Branforth. 1,044 authored source-derived frames, 174 manifests / 222 stored states; reverse pickups and composed half-turns produce 258 added runtime clips (86 each), with fitted helmet counterparts.

Includes sitting/rising, seated idle, eating/drinking, lying/sleeping/getting up, underwater low-air distress and dry recovery, ground/swimming pickup, seated reading/standing inspection, dry/wet carrying turns, and south/west/north ground/water death. Existing east deaths remain.

Sources and exact prompts are preserved in `source/`. References are the previously inspected actor sheets in `../crew-actions-v1/`. Registration records source SHA-256, shared row scale, per-frame head anchor and equipment angle. No body mirroring or generated code-drawn anatomy. Reverse clips reuse authored poses; half-turns concatenate quarter-turns. Ground pickup reverses the corrected `crew-actions-v1` unload. Runtime endpoint joins use registered base idle/carry cycles, not per-pose height normalization.

Source selection fixes are explicit in `build_pack.py`: Bill's missing west seated idle and clipped north drink are replaced; Veld's east-facing seated row and incorrectly oriented water death are replaced; north/west cargo corrections replace wrong turns; sleep refinement replaces north/south endpoints and east/west source rows are selected to maintain head orientation. Rejected originals remain for provenance. The first Bill correction's dry turn and first Veld correction's floor-sitting pose are not shipped. Water pickup separators follow empty gutters to preserve detached cargo without adjacent-frame fragments.

Runtime: `scripts/crew_life.gd` owns presentation and stage transitions. `crew_action_pack.gd` adds equipped variants and exact endpoint joins. Berth and lounge positions come from retained room props; visual offsets leave navigation feet on safe floor, and per-frame depth keeps bodies visible on seats/beds. Eating uses inspection when a sealed helmet is worn. Low-air pose and wet cargo turns respect exported fitted bounds. Oxygen rates, room economy and save format remain unchanged; new optional recovery fields have legacy defaults.

Rebuild: run `C:/Python314/python.exe character/crew-life-v1/build_pack.py`, run Godot with `--path . --script tests/preview_crew_life.gd`, then `C:/Python314/python.exe character/crew-life-v1/build_review.py`. Headless preview exports fitted strips too; native mode additionally captures contact sheets. This is a review candidate, not owner visual acceptance.

Review: `output/crew-life-review.html`, `output/crew-life-preview.gif`, native pack contacts and `output/crew-life-room-*-q*.png`. Browser automation for the local HTML was blocked by URL security policy; review evidence uses native Godot and local image inspection.
