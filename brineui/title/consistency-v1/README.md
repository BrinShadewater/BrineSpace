# Current title art

`background.png` is the installed stationary stage. `cover.png` supplies the moving BRINE pixels through the registered native silhouette in `character-outline.json`. Both generated sources remain byte-for-byte unchanged. Exact prompts and hashes are recorded in `manifest.json`.

The source size is 1925×817; the renderer maps it to the existing 1584×672 design area and keeps existing monitor coordinates. The outline extends below the image edge so clamped bottom pixels cover the three-pixel float at both extremes. Source-size registration is asserted before drawing. A new source requires a new outline review.

`rejected-character.png` is an opaque checkerboard extraction with changed framing, not a transparent sprite. It is retained for provenance and never loaded by the game. The native polygon avoids deleting dark character colors or shipping that background.

Do not run the older `tools/title/render_cover_loop.py` to regenerate this revision: it produces the preserved original title layers. Current verification uses `tests/test_title_screen.gd` and `tests/test_art_consistency_fixes.gd` with isolated settings/saves. See `docs/ART_FIXES_2026-09-09.md`.
