# Wrecked rooms

Four room-sized wreck variants are integrated: Engineering, Medical, Habitation
and Hydroponics. Each occupies exactly one standard placement cell and renders
at the current `game.get_cell_size()`, using the same square destination as a
standard room. They are external ruins, not operational rooms or blueprint cards.

## Play

New runs start with four fixed wreck sites at (18,18), (22,18), (18,22), (22,22).
The core's four immediate expansion cells remain free. This initial placement
is authored; randomized site generation is separate work.

1. Build to a cell next to a wreck (cardinal adjacency).
2. Select the wreck and choose **Dismantle & Salvage** in the inspector.
3. The basic salvage rig performs one job at a time. Work takes 18 game seconds
   at 1× speed. Global pause and individual job pause retain progress.
4. The full wreck gives way to a stripped interior and then the last foundation.
   Construction stays blocked throughout clearance.
5. Completion grants metal once and releases the cell. Place an ordinary blueprint
   there using normal room costs and door-connection rules.

Current yields are 12 / 8 / 6 / 10 metal respectively. Storage capacity applies;
the inspector discloses this and the completion log reports the amount secured.
Timing and yields are prototype settings, not completed human balance tuning.
No occupants, rescue choices or repairable compartments are hidden in these wrecks.

Wrecks have their own placement occupancy and never enter the operational-room,
walking, door or synergy graphs. Completed foundations remain as faint background
marks that can be covered by new construction. The active job has localized
underwater cutting light and small detached-fragment cues. Stage transitions are
crossfades of registered interiors, not physical disassembly of individual props.

## Art and registration

Eight immutable generated sources provide full and stripped states. Exact prompts
and input references are in `generation-record.json`; hashes, measured dimensions,
alpha counts and registration are in `manifest.json`.

Full wreck sources have real transparent exteriors. All four stripped edits
returned opaque white/checkered exteriors. Those exteriors are **not usable**.
The renderer samples only the normalized inner rectangle `(0.085, 0.115, 0.825,
0.765)` from the stripped source and composites it over the original full wreck.
The original hull therefore retains its silhouette and alpha throughout work.
No raster source was cropped, resized, recoloured or cleaned. Inspector thumbnails
show the original wreck identity; text reports the current job stage.

`index.html` is a review gallery of the same layered compositions. Owner visual
approval remains distinct from passing geometry and runtime checks. Runtime
images are loaded as raw PNGs. The existing raw export plugin includes the entire
environment folder; this pass did not validate a packaged release.

## Persistence and checks

The optional `wrecks` checkpoint field stores kind, progress, active job and cleared
state. Older checkpoints restore with no wrecks, preventing new obstacles from
appearing inside existing stations. Validation rejects invalid coordinates,
unknown variants, non-finite/out-of-range progress, active cleared wrecks,
uncleared overlaps and multiple active jobs. Cleared state prevents duplicate
rewards after Continue.

- `tests/test_wreck_clearance.gd`: reach, occupancy, inspector start, single rig,
  global/job pause, active-save restore, legacy compatibility, invalid progress,
  single payout, normal paid rebuild and post-build restore.
- `tests/playtest_wreck_rooms.gd`: four variants beside standard rooms at
  1280×720, 1600×900 and 2560×1440, plus stripped, foundation, cleared and rebuilt
  captures, changing work pixels and frozen paused pixels.
- `tools/audit_wreck_rooms.py`: source dimensions, hashes, transparent full
  silhouettes, matching stripped registration and review gallery.

Native evidence: `output/wrecked-rooms-v1/`. All fixtures use isolated save paths.

Copyright © 2026 Alex Yesilcimen. All rights reserved. See `NOTICE.md`.
