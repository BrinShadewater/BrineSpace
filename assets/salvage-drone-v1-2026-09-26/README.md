# Salvage drone directional animation set

Preview: http://127.0.0.1:8771/ (local review server).

92 clips: idle, swim, reverse, loaded swim, start, stop, power-on, power-off,
charging and disabled in eight headings; retrieval, release and blocked retrieval
in north/east/south/west. The recovery cycle retrieves scrap, carries it and
releases it into the preview scene. A separate top lamp pulses blue/red/yellow.

This is an animation review pack derived from the accepted v10 Salvage identity.
New directional artwork awaits owner review. Gameplay integration remains pending.
Construction (8767) and Mining (8768) are preserved.

## Contract

- Transparent 512-square PNG frames, 30 fps, registered pivot (256,246).
- Shared fleet display scale .34 world units per library pixel; south width
  120.36 world units. Other views use viewport-diameter feature calibration,
  uniform resizing and independent directional artwork.
- 6,240 body and 6,240 cargo frame references reuse registered poses and
  articulated frames; these are not independently generated paintings.
- Two-second travel/power clips; four-second cardinal work clips.
- Separate 60-phase rotor atlas per heading preserves continuous spin through
  preview transitions; cargo and status lamp are independent layers.
- Preview controller brakes before work, queues departure during retrieval,
  retains carried scrap across headings, and ramps propellers for power states.

## Rebuild and verify

From the repository root:

```
python assets/salvage-drone-v1-2026-09-26/build_full.py
python assets/salvage-drone-v1-2026-09-26/validate_full.py
python assets/salvage-drone-v1-2026-09-26/review_rigs.py
node assets/salvage-drone-v1-2026-09-26/test_motion.mjs
```

The builder accepts heading names for selective rebuilds. Do not use the historical
build_pilot.py for this set: it replaces the manifest with the old five-clip pilot.
manifest.json records frame paths, source hashes, timing, calibration and layers.
review/full-validation.json is the current exhaustive export report; older pilot
validation and screenshots remain historical evidence.

Review the open/closed direction boards and the browser preview at enlarged and
native scale. Native room/Bill evidence in review/salvage-room-scale.png compares
south widths 103/120.36/132; the selected south base remains unchanged. That capture
used isolated APPDATA and matching owner-save fingerprints, not gameplay pathing.
No Godot animation controller or collision/pathfinding integration is included.

Source prompts: PROVENANCE.md and review/DIRECTION_PROMPTS.md. Painted headings
are approximate perspectives, not exact projections of a common 3D model.

Latest polish: review/POLISH_CLOSEOUT.md. Compare authored exports in
review/motion-audit.html and exact native-size light/dark artwork in
review/polish-native-directions.png. Rebuild the density evidence with
`python assets/salvage-drone-v1-2026-09-26/polish_audit.py`.

East/west rear turbines use corrected horizontal-axis source v3. Latest targeted
evidence: review/TURBINE_CORRECTION.md and review/validation-east-west.json.
The validator accepts heading names, e.g. `validate_full.py east west`, and writes
a separate scoped report without replacing the previous full-set report.
