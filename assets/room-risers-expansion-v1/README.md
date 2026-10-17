# Bespoke expansion-room risers

28 generated wall masters replace inherited artwork for the 28 newer rooms.
Installed in the production wall registry; all 28 card bindings refreshed.
Review `index.html`, or http://127.0.0.1:8812/ while the local gallery server is running.

- `masters/`: original built-in image_gen output bytes, with genuine exterior alpha.
- `prompts/`, `generation.json`, `briefs.json`: exact prompts, provenance, reference
  roles/hashes and preserved previous bindings. `prepare.py` was the one-time intake;
  do not rerun it over an installed collection.
- `registrations.json`: measured face/cap regions; the PNGs are not cropped or resampled.
- `review/`: 112 native room views, 28 bare walls and eight comparison sheets.
- `cards/`: 28 maintained-baker outputs using scratch-copied owner Studio layouts.
- `evidence/`: source/native/card audits and gallery screenshot. Owner fingerprint
  details, scratch profile and previous-card backups stay local and are gitignored.

Panel fields stay quiet for the current windows and doors. Identity lives in end
fittings, lower service bands and matte department-appropriate materials. Collision,
room layouts, door behavior and window rules are unchanged. Explicit owner material
selections continue to override defaults.

Reproduce source validation with `python assets/room-risers-expansion-v1/register.py`;
use `--install` only when intentionally updating these 28 bindings. Native review:
`python assets/room-risers-expansion-v1/run_review.py`. Card bake: same command with
`--cards`; after visual review, `finish.py` copies cards to their registered paths.
`build_gallery.py` rebuilds diagnostic sheets and the gallery without editing sources.

All source checks pass; Godot 4.7.2 captured 112 orientations with zero failures.
All native comparison sheets and three baked cards were visually inspected.
Browser search/filter/disclosure checked. Owner acceptance is pending. Existing live
Godot processes changed profile breadcrumbs during isolated runs; no claim of profile
byte equality. No playable executable was rebuilt.

See `docs/RISER_EXPANSION_HANDOFF_2026-09-27.md` for the project handoff.
