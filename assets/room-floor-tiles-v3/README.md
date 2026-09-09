# Additional room floors

Three built-in imagegen atlases, each with 16 tile slots (48 total): engineering access plates, life-support drainage and habitation cork composite. Original 1254×1254 RGB outputs are preserved without processing; requested dimensions were 1024 square. Exact prompts are in prompts.json; source hashes and dimensions are in manifest.json.

Use Room Layout Studio → Floor finish. Three choices were added to rooms/whole-room/modular_floor.gd. Existing defaults and personal layouts remain unchanged. Details are flush artwork, with no new machinery behavior. Engineering is more weathered than its brief and is classified as a worn-deck option.

[Visual review](review.html): source atlases and native furnished Research Lab comparisons. Godot 4.6.1 exited 0: three texture loads, 12 rotated meshes and three selection/undo/redo sequences passed. Source and furnished captures were visually inspected: matte surfaces, readable construction and subordinate floor detail. Evidence and review script: output/room-floor-tiles-v3/.

Room modules remain 48 units with 4×4 source sampling. Slight generated seam variation remains; these are not certified seamless/Wang tiles. Corridors retain existing 8×8 alternate-material sampling; full tile designs are intended for rooms. No all-room adoption, card rebake or executable rebuild. PNGs use Git LFS attributes.
