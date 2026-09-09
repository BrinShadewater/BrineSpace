# Art material consistency pass — in progress

Owner request: review all game artwork for excessive shine and consistent color/vibe. Preserve department identity and maintained condition. Matte material correction requires repainting highlight structure, not global tinting or desaturation.

Current findings from the 44 non-corridor furnished review captures: shared science accessories are a repeated outlier, with chrome-like rails, white jar reflections and polished blue/white containers. Bright laboratory furniture and cylindrical equipment need asset-level inspection next. Warm habitation, industrial decks and small floor service details should retain their departmental contrast; matching does not mean making every room the same color. This is not a complete review of characters, UI, terrain, corridors, cards or animation frames.

Two material-repair attempts of rooms/production-ten/decor/research-v1.png were generated. Candidate one substantially reduced chrome-like rim highlights. Both exports are 1254-square RGB with baked checkerboard, while the original is also 1254-square with alpha (the earlier 1280 claim was incorrect). Candidate two also brightened the blue accents. Neither is integrated, registered, or accepted. Original game assets remain intact. Exact exports and hashes: output/art-material-polish/candidates.json.

A subsequent plain-white generation is now integrated using read-only vector silhouettes; no raster background cleanup was performed. See MATERIAL_REPAINT_BATCH_2026-09-08.md for integration and verification. Remaining game art categories still require review; do not report the overall pass complete.


## All-room review follow-up

The room-only review is complete in ROOM_MATERIAL_REVIEW_2026-09-08.md: 47 default powered views inspected, 376 native rotation/state samples rendered, and eight targeted offline/side comparisons inspected. Nineteen priority repaints, nineteen targeted adjustments and nine retain findings are agent review judgments, not owner acceptance. No source art changed during that review. The subsequent repaint batch is recorded separately. The complete-game polish objective remains open for repaint integration and the other art categories.


The owner-approved Tidal matching follow-up now includes Life Support, Research and Clone Lab wall/equipment families, structural trim and the shared bench. See [current batch evidence](MATERIAL_MATCHING_TIDAL_REFERENCE_2026-09-08.md). Eleven new source images are integrated; the full-game scope remains open.
