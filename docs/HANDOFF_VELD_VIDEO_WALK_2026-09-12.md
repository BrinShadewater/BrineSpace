# Veld whole-body walk milestone

Objective: polish all requested crew animations and movement, improve the asset workflow and maintain the visual bible.

Decisions: Veld is a woman without glasses. Fitted helmets preserve whole-body movement. No mirrored asymmetric equipment. Marsh remains helmet-free; Bill stays outside the replacement.

Current state: all eight Veld walk variants selected from independent directional video sources. East slots 29/34/38/43/48/52, stride 102 dense pixels; west 28/33/36/40/45/48, stride 108; south 24/29/32/36/41/44 and north 26/31/34/38/43/46 retain stride 0.12 cells. Original six durations preserved. North source 02 corrects missing gloves in rejected source 01.

Changed implementation: prepare_veld_video_walk.py and prepare_veld_video_walk_helmet.py support all four directions; veld_scanner_revision.py selects sources, rebuild_human_crew_art.py sets strides. playtest_crew_walk.gd uses actual Vector2 precision for its independent distance oracle. playtest_dr_veld.gd retains short episodes, captures a longer requested direction and isolates scripted art playback from input/automatic processing.

Checks: each selected direction passed 60 native distance-driven frame/cadence samples. Validator reports zero errors/border touches; 670 original frames and 108 manifests unchanged. Live bare/helmet samples reviewed: east 15, west 34, south 53, north 61 per variant, with work approaches or turns. A north helmet timeout and passing isolated retry are retained in logs; retry success alone does not establish the timeout cause.

Remaining: Branforth eight and Marsh four rejected walk variants; broader start/stop/turn review for Veld; other animation/identity/seated work in the clip ledger. Owner acceptance and full goal completion remain open. No export performed.
