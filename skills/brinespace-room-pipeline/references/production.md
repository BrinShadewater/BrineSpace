# Production contract and verification

All paths below are relative to the active BrineSpace checkout, not this skill.
Keep project tools as the single executable source; do not fork copies into skills.

## Source ownership

- `scripts/room_database.gd`: canonical ID, footprint, layout and door masks.
- `scripts/main.gd`: card PNG mapping and variant counts.
- `scripts/grid_canvas.gd`: station PNG/variant mappings, crop/rotation and effects.
- `tools/room_art_pipeline.py`: Pillow cleanup and normalization (inspect `--help`).
- `tests/test_room_art_pipeline.py`: cleanup behavior tests.
- `docs/ROOM_ART_PRODUCTION.md`: production evidence and correction queue.
- `rooms/hybrid/`: current working images, not automatically accepted images.

## Per-room record

Record full prompts, reference roles, source/output hashes, actual dimensions,
processing settings and separate review findings. Use one pack index referencing
room records; the expected-ID set comes from the requested scope and current
database, including approved new IDs not yet added to the database.

Example review record for a currently blocked candidate:

```json
{
  "id": "corner",
  "path": "rooms/hybrid/corner.png",
  "stage": "cleaned",
  "geometry": {
    "expected_doors": ["west", "south"],
    "verdict": "fail",
    "findings": ["Door trim is present but actual west/south openings are missing"]
  },
  "integration": {"station": false, "cards": false},
  "verification": {"native_capture": null, "regression_log": null}
}
```

Do not mark absent evidence as passed. Existing `.provenance.json` files have a
lighter schema; read them as historical records, not full validation certificates.
Introducing a manifest or template generator is implementation work, not something
this reference claims already exists.

## Cleanup

The owner has authorized local background removal and margin normalization for
this room expansion. For other tasks, respect the current user's editing scope.
Use new destinations; the script refuses overwrite:

```powershell
python tools/room_art_pipeline.py output/room-art-pilot/hydroponics-candidate.png output/room-art-review/hydroponics-v2.png
python -m unittest discover -s tests -p test_room_art_pipeline.py
```

Pillow is required. Check availability before running. Cleanup preserves enclosed
light details, but light artwork connected to the exterior can still be removed.
Black backgrounds are not safely removable with a universal dark-color threshold:
station floors and shadows are dark too. Use an explicit mask or targeted edit.

Aspect-preserving bounding-box fitting can leave different side margins and does
not align door anchors. Non-integer nearest-neighbor resizing also changes pixel
cluster widths. Record those tradeoffs and inspect actual-scale output. After
anchors are established, use a shared template transform, not independent tight
cropping on every revision or animation frame.

## Geometry and state checks

For every room, inspect all four sides against the canonical door mask. Verify
openings are centered, widths agree at seams, and closed sides lack false door
trim. Walk the specified paths visually: a conveyor across an aisle is a failure
even if the simulation permits walking through it. Review rotations and adjacent
room pairs, not only a single upright room.

Define interior effect rectangles and pivots in normalized room-local coordinates.
Use the same transform for art and overlays. Do not bake active-only glow into
the sole static texture and call an offline tint a full operating-state system.
Do not infer new collision or resource mechanics from an illustration.

## Native acceptance

Use isolated-save harnesses, never the player's `user://brine_save.json`.
Adapt `tests/playtest_polish.gd` for paid builds, cards, rotation, connected doors,
operation, suspension, pause and discovery states. Inspect native viewport images
at 1280x720, 1600x900 and 2560x1440, plus mature-station zoom. Use paired frames to
prove motion/freeze behavior; a single screenshot cannot prove animation.

Run affected tests, the existing gameplay suites and main-scene smoke. Locate the
configured Godot 4.6 executable rather than hardcoding a user's Desktop path.
Inspect logs for `SCRIPT ERROR:` and `ERROR:` even with exit code zero.
The current suites are test_synergy_manager.gd, test_discovery_progression.gd,
test_polish_gameplay.gd, test_run_balance.gd and playtest_polish.gd under tests/.

Before an authorized commit, check `git check-attr filter -- <PNG paths>` and
confirm staged PNG blobs are LFS pointers. Stage exact intended files only.

## Retry policy

After the same generation defect repeats, improve the input contract or use an
authorized deterministic repair instead of repeating identical prompts. Keep
structurally invalid candidates in the correction queue. Continue independent
in-scope work; ask only when the repair genuinely needs new authority or design.
