# Tileset library: bought art, owner-decorated rooms

Read this before adding a bought art pack, touching `rooms/tileset-library/`, changing
the Studio asset tray, or sweeping assets the owner marked. It records the contracts the
runtime depends on and every mistake that cost real time in the September 18–19 session.

The owner decorates rooms by hand in the Layout Studio. The agent's job is to make the
library correct, browsable and honest, then get out of the way. Do not auto-decorate
rooms unless asked; when asked to extend the owner's layout (other rotations), start
from their layout and change only what a rule forces.

## What lives where

| Path | What it is |
|---|---|
| `assets/new-tilesets/<set>/` | Converted prop sheets, Git LFS. Folder = slug of the in-universe set name (`galley`, `ghost-deck`, `undercity`). |
| `assets/new-tilesets/floors/floor-NNN.png` | Floor finishes: one 48px tile repeated 4×4 (192px). |
| `rooms/tileset-library/props.json` | The registry: one array entry per prop. Loaded by `scripts/room_asset_library.gd` as group `tileset`. |
| `rooms/tileset-library/floors.json` | `{caption: res://path}` finishes, read by `rooms/whole-room/modular_floor.gd`. |
| `rooms/tileset-library/merged.json` | Alias map, absorbed id → surviving id. Remap every mark file through it after a merge. |
| `rooms/tileset-library/removed.json` | Log of swept props (label, set, source, region). |
| `rooms/tileset-library/{favourites,retired,names,categories}.json` | **Owner data**, written live by the Studio. See below. |
| `legacy/default/`, `legacy/retired/` | The pre-library room and prop art. Character art was not moved. |
| Desktop `New Tilesets/`, `Another Pass/extracted/`, `cyber punk/` | Untouched sources. `New Tilesets Converted/` holds the conversion output. Not in the repo. |

The conversion, scan, theming and merge scripts were written as session scratch and
are **not in the repo yet**. Their parameters are recorded here so they can be rebuilt.

## The registration contract

```json
{"id":"af-01","label":"Industrial 014","category":"Industrial & workshop","tileset":"Foundry",
 "display_width":96.0,"source":"res://assets/new-tilesets/foundry/tile-B-01.png",
 "region":[576.0,96.0,96.0,192.0],"pieces":[[[576,96],[672,96],[672,288],[576,288]]],
 "footprint":[0.08,0.78,0.84,0.22],"method":"Grid-aligned tileset region; raster unchanged"}
```

- **`pieces` are absolute sheet coordinates.** `Library.draw` subtracts a pivot of
  region centre-bottom from every point, exactly as native registrations do. Box-relative
  pieces draw the art displaced by the region's offset: previews render off their 128px
  viewport (3 of 280 painted) and placed art lands far from its selection box.
- **`region` is trimmed to opaque bounds** (alpha ≥ 24), like native registrations.
- **`display_width` equals the region width.** One sheet pixel is one room unit; a 48px
  tile is 48 units against a ~65-unit crew member. The Studio places at 50% by default;
  the owner calibrates size once against a crew member before decorating.
- **`footprint`** is the base of the silhouette as fractions of the rect (the opaque
  bounds of the bottom 22% band, minimum 6px). `room_lighting.gd` shades the footprint,
  not the rect. Without it a cut-out sprite sits on a dark rectangular mat, because the
  equipment shadow assumes art fills its box. Native props carry none and are unchanged;
  mirrored art mirrors it.
- **`id` never changes.** Layouts, stars, renames and moves key on it. When a prop is
  merged away, alias it; when one is split, the first part keeps the id.
- **`label` is `<Kind> NNN`**, numbered within the kind. No pack names, no storefront
  codes. Labels appear only in the Studio; nothing player-facing reads them.
- **`tileset` is an in-universe set name** (Galley, Hydroponics, Infirmary, Reactor Hall,
  Ghost Deck, Undercity). The packs span genres; their real names do not fit the station.
- Sixteen categories, none a leftover bucket. A prop with a measured theme keeps it
  (foliage, screen glow, water, warm crate tones); otherwise it takes its pack's subject.
  That fallback is coarse on purpose: the owner corrects with **Move to category**.

## Owner data is a save file

`favourites.json`, `retired.json`, `names.json` and `categories.json` are tracked, but
between commits they hold the owner's uncommitted Studio decisions. HEAD is older than
their session. A `git checkout` of them once discarded seventeen marks.

- Never restore them from git. Read, remap through `merged.json`, write back.
- Print their contents before any operation that rewrites them.
- Commit them once the marks have been acted on, so they become safe.
- Tests redirect all of them, and `props.json`, through the static `*_PATH` vars on
  `room_layout_editor.gd`. Fingerprint the real files around every native run.
- A prop both retired and starred is the owner's call. Leave it and say so.

## Adding a pack

1. **Look at the art before judging it.** Ten packs were withheld as "grime" on their
   folder names; they held bunks, lab benches, produce crates and server racks.
2. **Convert** each prop sheet: `convert(brightness=0.281, line=0.45, soft=0.22)`; A2 and
   A4 surface sheets get the edge and gloss work only. Alpha is never changed.
3. **Scan** for props: opaque components per sheet, tile size from the image (48, some
   64), a strict pass and a gap-tolerant pass. Both passes survive, so expect a blob
   *and* its parts for touching objects. Handle that in the merge, below.
4. **Pick by eye** from a numbered contact sheet. Exclusions the owner set: mechs,
   outdoor vehicles other than forklifts, spaceships, outdoor buildings, shipwrecks,
   medieval chests, pirate cannons, lifeboats, oars, crashed aircraft, futuristic guns
   and armour, spacemen, solar panels, giant mining vehicles, helicopters. Also drop any
   sign with English text. Exclude at **prop** level: a sheet of mechs also holds lockers.
5. **Merge and trim** (next section), compute footprints, number labels after the last
   of each kind, give the set an in-universe name and a slug folder.
6. **Tone** against the verified source (section after that).
7. **Copy only referenced sheets** into the repo. Unreferenced sheets are dead LFS weight.
8. **Verify** with a probe and the three native suites, then commit with explicit paths.

## One object, one box

Work from the untouched scanner boxes, never by patching a merged result.

- **Blob pre-pass.** A box holding two or more boxes that cover ≥ 70% of it is the
  gap-tolerant blob of separate objects. Drop it, alias its id to its largest part.
  Skipping this made the merge "absorb" single chairs into chair pairs (446 blobs).
- **Merge** two boxes when art crosses their contact: a run of opaque pixels ≥ 60% of
  the shared edge on both sides, and art just beyond each edge.
- **Seam continuity guard**, both axes: refuse when the opaque columns (or rows) either
  side do not line up (overlap < 60% of the wider run) or the mean colour across the
  seam differs by more than 0.16. Two objects placed flush fail one or the other.
- **Refuse** any merge over 240px a side: that is a row of shelf units, not a prop.
- **Extend** a box into art nobody registered, one 48px strip at a time, up to three,
  by the same edge test. **Never grow over a registered box**; doing so and then
  absorbing it bypasses the guard.
- **No automatic split.** Of 227 two-tile-tall boxes with a pinched, discontinuous seam,
  nearly all were single objects: hydrants, bunk beds, sinks with mirrors, IV stands,
  potted plants. The Studio's **Split in two** gives that decision to the owner.
- **Near-duplicates are variants.** 2,598 look-alikes were gun racks with different
  guns, portholes with different views, monitors with different screens. Only four
  props in 10,000 were pixel-identical. Never auto-delete look-alikes.

Result on the first library: art running off a box edge fell from 884 props to a
residue the owner resolves with Split.

## Tone: measure against the owner's own art

Targets come from the game's painted room props (`legacy/**/pack/*.png`), not from taste:

| | owner's props | conversion alone | after repair |
|---|---|---|---|
| prop median luminance | 0.275 | 0.236 | 0.284 |
| darkest decile | 0.194 | 0.145 | 0.19 |
| emissive screen pixels | 0.417 | 0.272 | 0.38 |
| mid-grey pixels | 0.276 | 0.208 | 0.26 |

- Lift with a **gamma curve** per prop: it raises shadows and cannot clip a highlight.
- Lift only props under the floor. A good prop sharing a sheet with a bad one is left
  alone; track a per-sheet "already lifted" mask so no pixel is lifted twice.
- Props crushed harder than the conversion's own ×0.52 are restored to source × 0.52.
  That is what had turned grey rock near-black.
- Plants get a higher target (0.28). The owner flagged dark plants three times before
  the distribution was measured; measure the distribution the first time.
- Screens and mid-greys are restored per pixel toward source × 0.82 and × 0.62, using
  masks built from the **source** sheet. Use the same pixel tests for the repair as for
  the measurement, or most measured pixels never qualify for the lift.
- The library stays a touch under the owner's numbers on purpose. "A bit more" is a
  cheaper correction than "too much".
- Many flagged props are correctly dark (coal, rubble, blacked-out screens) or correctly
  grey (chain-link, steel pipe, newspaper). The packs are also simply less saturated
  than the owner's art (0.21 against 0.50 at source); conversion did not cause that.
  Show the owner the outliers; do not "fix" a number.

**Match a sheet to its source by alpha identity, never by file name.** Packs share names
like `tile-B-01.png`. A name match repaired sheets against the wrong source and came out
blotchy; it was caught only because the before/after was rendered. Hash the alpha channel
(conversion never touches it) and verify per sheet before writing.

## The Studio side

Tray controls: kind filter, set filter, search (label, set and the owner's name), **★
Favourites**, **Marked for removal**, **Star**, **Mark for removal**, **Move to
category…**, **Rename**, **Split in two**; Ctrl/Shift-click selects several and the mark
buttons act on the batch. The crew picker stands Bill, Marsh, Branforth or Veld in the
room. A progress bar under the tray title counts previews as they render.

- The tray renders **one preview per frame** in a SubViewport. It lists at most
  `TRAY_LIMIT` (280) entries and says how many it hid. Without the cap, "All assets"
  pegged a core for sixteen minutes.
- **Never call a whole-catalog scan per entry.** `family_variants()` inside the rebuild
  loop was quadratic: the Studio froze on open and the editor test crept from minutes to
  42. Hoisted, the test takes 24 seconds. A loading screen would have hidden the bug.
- Floor finishes: a room samples a finish as a 4×4 atlas, one quarter per 48-unit cell,
  so a tileset floor is one tile repeated 4×4. The game draws every finish at 42% over
  the base floor; new finishes read as subtle as the existing ones.
- Floor decorations, wall decorations and lights are the game's own authored systems per
  room. The tray offers them nothing because no library art is wired in. They are not
  dead; do not remove them to tidy the list.

## Sweeping what the owner marked

1. Print `retired.json`. Drop anything also in `favourites.json` and tell the owner.
2. Remove the registrations, blank the regions on the sheets (write atomically: temp
   file, then replace), append to `removed.json`, empty `retired.json`.
3. A merge re-run must drop `removed.json` ids and any region left with no opaque art.
4. Delete a folder only when nothing references it, checked across the repo.

## Extending the owner's layout to other rotations

Layouts live outside the repo in `user://room_layouts.json` (on the owner's PC:
`%APPDATA%\Godot\app_userdata\BrineSpace\`), keyed `<asset>/<quarter>`. A missing quarter
falls back to authored defaults, not to quarter 0. The room stays riser-north in every
quarter; only the open door sides move (`Geometry.has_port(room.layout[0], side)`).

Drive the real editor from a `--script` probe: `switch_room`, `switch_rotation(q)`, copy
the whole 0° draft (positions, flips, sizes, floor, removed defaults), nudge anything
intersecting `Store.door_lane(side)` for an open side the shortest way out, require
`issues()` empty, then `save_layout()`. Back the file up first. Screenshot all four and
send them; the owner's eye accepts a layout, the validator only permits it.

## Verifying

- Native lane only: `python tools/run_tests.py --native --only
  test_tileset_library_tools,test_room_layout_editor,test_layout_performance_guards`.
  `--only` is comma-separated. A raw `--headless` run has no textures and proves nothing.
- A passing suite proves the old behaviour survived. It says nothing about a new control
  until a test exercises that control. Say which is which.
- Probes beat reading code. A `--script` probe that opens the Studio, acts and
  screenshots found the displaced art and the shadow mat in minutes each.
- The tests and the game are the same executable. If the owner launches the game and
  force-quits, the run dies with it. Say when a run is in flight.
- An empty output file is not a dead task; Godot buffers stdout to a file. Check CPU
  time, and stop a task with the task tool rather than inferring it has ended.
- `git show HEAD:<png>` returns the LFS pointer. Pipe it through `git lfs smudge` to
  compare against the committed image.
- Other sessions share the checkout. Stage explicit paths; commit promptly.
