# Riser and square-wall refresh

44 native Godot room cards with transparent compact framing. Their selected paths live in scripts/room_card_art.gd; three corridor cards remain in their existing pack. Sources are the current layered views, department material crops and60-unit risers. Original source art is preserved. PNGs use Git LFS.

Regenerate with Godot --path . --script res://tools/bake_current_architecture_cards.gd -- --output=res://assets/wall-refresh-v1/cards --compact. Hashes and alpha bounds are in manifest.json; defining wall renderers are in wall-owners.json. The cards were generated from the renderer, not edited raster originals.

See docs/RISER_WALL_REFRESH_2026-09-08.md for eight corrected rooms, native reviews, and the broader Airlock test failures. Owner visual acceptance remains separate from these checks.
