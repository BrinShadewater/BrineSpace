# Hybrid Room Art Pilot Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Produce and verify three individual hybrid room assets before renewing the full station.

**Architecture:** Preserve the existing room renderer and PNG loading. Generate independent canonical room images, inspect their door masks and actual-scale appearance, then replace only the corresponding texture mappings and variant lists. No gameplay or monolith refactor.

**Tech Stack:** Godot 4.6, GDScript, built-in image generation, Git LFS, Windows PowerShell.

**Spec:** docs/superpowers/specs/2026-09-05-room-art-expansion-design.md

## Global Constraints

- Preserve every existing gameplay footprint and canonical door mask.
- Keep originals and save new assets under rooms/hybrid/<room_id>.png through Git LFS.
- No baked labels or synergy hints.
- Use a shared 1280x1280 output canvas with consistent wall and door anchors.
- Player saves are not used or overwritten by tests.
- Preserve the user's project.godot edits.
- This plan covers the art pilot only; the rest remains explicit work in the companion scope ledger.

## File responsibilities

- `rooms/hybrid/reactor.png`: amber central reactor with perimeter circulation and four doors.
- `rooms/hybrid/hydroponics_bay.png`: large planting beds and uncluttered canonical paths.
- `rooms/hybrid/mining_drone_bay.png`: two large drones flanking a north/south aisle.
- `tests/test_hybrid_art.gd` and paired UID: asset dimensions, decoding and mapping regression checks.
- `scripts/main.gd`: card texture mapping and pilot variant counts only.
- `scripts/grid_canvas.gd`: station texture mapping and pilot variant paths only.
- `docs/ROOM_ART_PRODUCTION.md`: prompt provenance, generation method, inspection evidence and accepted files.

## Task 1: Generate the production candidates

**Interfaces:** consumes canonical layouts from `RoomDatabase.all_rooms()` and inspected source PNGs; produces three candidate PNGs outside live mappings.

- [ ] Read imagegen and sprite-pipeline skills; inspect each actual mapped source, canonical layout and `_draw_room` / door placement geometry. Do not use a differently numbered art variant as a topology specification.
- [ ] Read the source files with `view_image` before reference-based generation.
- [ ] Generate one candidate per tool call using this prompt, substituting the explicit subject and canonical doors below:

```text
Production game-room sprite for BrineSpace. Use the inspected image as material and camera reference, not as an unchanged composition. Overhead cutaway industrial pixel illustration, large readable machinery, quiet slate floor, worn metal detail, restrained light, serious haunted orbital mood. Square 1280x1280 canvas, transparent exterior, complete hull inside canvas. No text, labels, characters, UI, cast shadow outside hull or perspective rotation. Match the canonical doorway positions, widths and clear paths of the provided layout. Fewer larger machines, no tiny clutter filling the floor. Keep machinery lights restrained so functioning light effects can be layered later.
```

Subjects: reactor = one prominent amber chamber with a clear perimeter route,
four centered doors; mining bay = two prominent yellow mining drones, clear
north/south center aisle, only north and south doors. Hydroponics = large green
planting beds with a visible irrigation tank, using its canonical layout as read
from the database (do not infer it from the four-door comparison reference).

- [ ] Inspect each generated result for silhouette, incorrect doors, transparent exterior and paths; request a targeted image edit for failures. Do not silently resize a failed generation into apparent compliance.
- [ ] Copy accepted candidates non-destructively into `rooms/hybrid/`; retain generated originals and original shipped PNGs. Record actual prompts, built-in generation method and output paths in the production document.

## Task 2: Validate and wire the pilot

**Interfaces:** produces runtime/card mappings for the three existing room IDs; existing renderer API stays unchanged.

- [ ] Add a SceneTree test using this asset check, plus explicit assertions against both instantiated main and GridCanvas texture path dictionaries:

```gdscript
extends SceneTree

func _initialize() -> void:
    for id in ["reactor", "hydroponics_bay", "mining_drone_bay"]:
        var path := "res://rooms/hybrid/%s.png" % id
        var img := Image.new()
        assert(img.load(path) == OK, "Cannot decode " + path)
        assert(img.get_size() == Vector2i(1280, 1280), path)
        assert(img.get_pixel(0, 0).a == 0.0, "Opaque exterior: " + path)
    print("Hybrid art asset checks passed.")
    quit()
```

For mapping assertions, instantiate `load("res://scenes/main.tscn").instantiate()`
without adding it to the tree, and `load("res://scripts/grid_canvas.gd").new()`.
For each ID assert both `room_texture_paths[id]` equal the path above; assert
GridCanvas `room_texture_variant_paths[id] == [path]`. Free both instances.

- [ ] Run the test before updating mappings and confirm the mapping assertion fails, not a parse error:

```powershell
& 'C:\Users\Alex\Desktop\Projects\Godot_v4.6.1-stable_win64.exe' --headless --path . --script res://tests/test_hybrid_art.gd
```

- [ ] Set the three keys in both texture dictionaries to their hybrid paths. Set their GridCanvas variant arrays to one hybrid path and their main `ROOM_ART_VARIANT_COUNTS` values to 1. Do not alter any other ID.
- [ ] Re-run the asset/mapping test; inspect logs for `SCRIPT ERROR:` and `ERROR:` even if process exit code is zero. Generate and preserve the new script's Godot UID.

## Task 3: Native acceptance and recoverable commit

**Interfaces:** accepted art pilot plus captured actual-scale evidence for approval of remaining production batches.

- [ ] Read `tests/playtest_polish.gd` and use its isolated-save viewport capture approach to capture the pilot rooms in-scene at 1280x720, 1600x900 and 2560x1440. Include cards, rotation, doors, an operating link and an offline room. Do not touch the player's save.
- [ ] Inspect those images with `view_image`: identify each room without its label, verify matching door seams, no clipped machinery and clear overlays. Compare against old art at identical zoom. Correct generated art through image edits if it fails; no claim of animation from a static capture.
- [ ] Run `test_synergy_manager.gd`, `test_discovery_progression.gd`, `test_polish_gameplay.gd`, `test_run_balance.gd` and `playtest_polish.gd` under `res://tests/` using the same Godot command pattern above. Perform main-scene smoke and script parse checks.
- [ ] Record results and exact capture paths in `docs/ROOM_ART_PRODUCTION.md`. Report any unrun check explicitly.
- [ ] Verify `git check-attr filter -- rooms/hybrid/reactor.png rooms/hybrid/hydroponics_bay.png rooms/hybrid/mining_drone_bay.png` returns `lfs` for each. Verify staged blobs are LFS pointers, not raw PNGs; run `git diff --check`.
- [ ] Commit only pilot assets, their tested mapping changes, the test and paired UID, and production documentation. Do not stage project.godot or unrelated files. No push or release.
- [ ] Show the in-game pilot to the owner for the art-quality checkpoint specified by the approved design. Keep all remaining scope open.

## Self-review

This plan deliberately covers the first independently testable subsystem, not the
whole expansion. It preserves both mapping consumers, canonical geometry, LFS,
originals, save isolation and the user-requested production checkpoint. The
companion scope ledger records everything still owed.
