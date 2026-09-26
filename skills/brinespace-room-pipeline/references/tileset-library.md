# Tileset library: bought art, owner-decorated rooms

## Owner-authorized composition pilots â€” September 20

The owner now requests help decorating rooms. This authorizes the requested
compositions, not an automatic library-wide furnishing pass. Large and medium
equipment take priority; small pipes, extinguishers and miscellaneous objects
must not be scattered into empty space. Small-prop removal is a separate decision.

Re-read live favourites/names before acting on a dated fix queue. Empty current marks
supersede historical outstanding-star lists; do not recreate old requests. For a
selected layout, record source-region dimensions, display scale and known defect
entries before proposing an upscale. World-units-per-source-pixel is not screen
resolution: inspect normal station zoom and material/detail fit separately. Absence
from hole-report.json is not proof that a prop has no visual defects.

Conversely, an automatic hole flag is not proof of missing material. Life Support's
mat-33 filter rack flagged330pixels; enlarged alpha review showed intentional spaces
between intact cylinders and supports. Preserve those openings. Record the inspected
crop and conclusion instead of filling every flagged region or resetting owner marks.

Group items by their use: workbench with tool storage, specimen preparation with
analysis, beds with personal storage. Preserve quiet working floor and clear door
approaches. A closed north wall can support a continuous equipment line; move only
the pieces obstructing it when another quarter opens that door.

Inspect rendered effective props, not just the local JSON. Authored defaults merge
with local overrides, and original functional furniture may still draw beneath new
props. Suppress obsolete additions explicitly and preserve functioning activity
targets (Crew Hab sleeping berths use named original props). Test those approaches.

Back up both local layouts and defaults. Work against a copied candidate file,
review all four production views beside crew, then merge only the selected room
keys into fresh files after checking for concurrent edits. Preserve every other
layout and all library marks. Bake only the changed room cards after review.

The owner found the first Maintenance/Bio Lab pilot lackluster despite clear routes:
one small item per corner and a sparse rear row do not make a finished workplace.
Choose substantial existing assemblies first, then adjacent storage and operator
stations. Compare in native views before adding anything else. Do not scale down
supporting furniture merely to fill a leftover gap; replace undersized pieces or
leave the space useful. Keep accepted/provisional reference rooms unchanged during
focused revisions.

`tools/review_room_composition.gd` reads an optional `--layouts=res://...` file,
uses the production views, captures all four quarters and records overlapping
visual bounds for inspection; use --strict-visual-overlap only for deliberately
disjoint layouts. It checks door approaches, crew traversal and original sleeping-berth access.
Without `--layouts` it checks shipped defaults independently of local overrides.
Its graph checks and native stills are bounded evidence, not owner acceptance or
an expedition playtest. The first pilot and rollback locations are recorded in
`docs/ROOM_COMPOSITION_PILOT_2026-09-20.md`.

Read this before adding a bought art pack, touching `rooms/tileset-library/`, changing
the Studio asset tray, or sweeping assets the owner marked. It records the contracts the
runtime depends on and every mistake that cost real time in the September 18â€“19 session.

The owner decorates rooms by hand in the Layout Studio. The agent's job is to make the
library correct, browsable and honest, then get out of the way. Do not auto-decorate
rooms unless asked; when asked to extend the owner's layout (other rotations), start
from their layout and change only what a rule forces.

## What lives where

| Path | What it is |
|---|---|
| `assets/new-tilesets/<set>/` | Converted prop sheets, Git LFS. Folder = slug of the in-universe set name (`galley`, `ghost-deck`, `undercity`). |
| `assets/new-tilesets/floors/floor-NNN.png` | Floor finishes: one 48px tile repeated 4Ã—4 (192px). |
| `rooms/tileset-library/props.json` | The registry: one array entry per prop. Loaded by `scripts/room_asset_library.gd` as group `tileset`. |
| `rooms/tileset-library/floors.json` | `{caption: res://path}` finishes, read by `rooms/whole-room/modular_floor.gd`. |
| `rooms/tileset-library/merged.json` | Alias map, absorbed id â†’ surviving id. Remap every mark file through it after a merge. |
| `rooms/tileset-library/removed.json` | Log of removed props: label, title, set, source, region and, for a reviewer's removal, **why**. |
| `rooms/tileset-library/variants.json` | Families of look-alikes the tray folds into one tile. |
| `rooms/tileset-library/hole-report.json` | Props with key holes (automatic estimate, plus what a reviewer saw) and `needs-split`: stuck pairs with no clean seam. |
| `rooms/tileset-library/hole-patches.json` | Hand-chosen regions for `patch_holes.py`. |
| `rooms/tileset-library/{favourites,retired,names,categories}.json` | **Owner data**, written live by the Studio. See below. |
| `legacy/default/`, `legacy/retired/` | The pre-library room and prop art. Character art was not moved. |
| `vendor-art/New Tilesets/`, `vendor-art/Another Pass/extracted/` (includes `cyber punk/`) | The vendors' packs, untouched; gitignored (licensed, 350 MB). Every repair tool reads them through `--sources`, so keep them. They were on the owner's Desktop until Sept 20. |

## The tools

`tools/tileset_library/`, run from the repo root. Every one has `--help`, takes its
paths as arguments, and the four that write have `--dry-run`. Each was checked against
results already in the repo before it was committed.

| Tool | Does | Checked by |
|---|---|---|
| `convert.py SRC DST` | Converts a pack toward the station's look; alpha untouched. | Reproduces the earlier conversion byte for byte. |
| `scan.py DIR --code xyz --out scan.json --contact pick.png` | Finds props, draws the numbered sheet to pick from. | Finds the same 993 props in the Cyberpunk pack. |
| `register.py --scan â€¦ --converted â€¦ --set "Name" --domain "Kind" [--picks picks.json]` | Themes, trims, footprints, labels and registers picks; copies only referenced sheets. `--neon` for neon-lit packs, where blue is not water. | Dry run. |
| `register.py --validate` | Checks the live registry against the contract below, on the sheets themselves. | Found five props a sweep had damaged. |
| `merge.py [--base REV]` | One object, one box. | Rebuilds the committed alias map from the untouched boxes, bar one alias a sweep explains. |
| `tone.py measure\|repair --sources â€¦ [--only set]` | Measures against the owner's props; repairs what is too dark. | `measure` reproduces the known library numbers. |
| `sweep.py` | Removes what the owner marked. | Dry run keeps the prop that is both retired and starred. |
| `sweep.py --restore <id> â€¦ [--category â€¦]` | Undoes a removal: art from the sheet's git history (LFS, across the folder renames), pasted only where the sheet is empty; registration rebuilt from `removed.json`. | Six corpses and skeletons brought back; registry test passes. |
| `sweep.py --show page.png [--set â€¦] [--match â€¦]` | Draws removed props with their ids, for the owner to choose from. | Drew the four Undercity facades. |
| `titles.py sheet "Set" --out â€¦` / `apply file.json` | Real names, a set at a time: numbered pages pinned to ids, then a titles file. | Wet Lab: 198 named, 44 re-filed. |
| `variants.py [--contact â€¦]` | Families of look-alikes for the tray to fold. | Largest family 20; an earlier chained method grew one to 262. |
| `intake.py titles.json [--dry-run]` | Takes in one set's review: names, categories, removals, splits, holes. Trusts none of it. | 39 sets taken in; each verified from the registry. |
| `split.py <id> â€¦` | The Studio's Split button in Python. | Reproduces the Studio's split of the stacked chairs to the pixel. |
| `refit.py --starred` / `refit.py <id> â€¦` | Fixes boxes from the art itself: each connected piece goes to the prop whose box holds most of it, the box regrows to the object, objects standing apart become separate props. Lists what touches a neighbour for cutting by eye. | Of 447 starred props: about 205 refitted, 68 separated, 38 wrong splits rejoined first. |
| `patch_holes.py --suggest-starred` | Adds a `keyed` patch to each starred prop it would change: enclosed holes ringed by light pixels in the source. | 41 props patched; three runs byte-identical. |
| `cut.py cuts.json [--preview â€¦]` | Cuts objects drawn touching, where `refit.py` finds no gap. The reviewer says how many they SEE (`cols`, `rows`, or both for a grid); the tool finds the emptiest lines; `at`/`at_rows` give exact lines for unequal pieces. | 148 starred props cut into about 415, each previewed first. |
| `isolate.py [--preview â€¦]` | Lifts a prop out of art it is tangled with (an arm reaching over its neighbour, a tray inside the box) onto the set's own `fixes.png`; spec in `isolate.json` (`grow`, `drop` rects, `main`). The vendor's sheet is untouched; every run rebuilds from it. | 15 props lifted, two robot arms separated. |
| `split.py --undo <id>` | Rejoins a split (the Studio's **Rejoin parts**). The second id becomes an alias in `merged.json`. | Rejoin then split returns the same two regions. |
| `patch_holes.py --sources â€¦ [--preview â€¦]` | Hand patches for key holes, and whitening of white surfaces. | Three consecutive runs give byte-identical sheets. |
| `unkey.py` | Automatic key-hole repair. **Not safe to run library-wide**; its header says why. Used for detection only. | Three attempts, none good enough. |

Run `register.py --validate` after anything that writes the registry or the sheets.

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
- **`region` is trimmed to opaque bounds** (alpha â‰¥ 24), like native registrations.
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
- Sixteen categories, none a leftover bucket, and every prop has been looked at and filed
  by what it is. `register.py` still seeds a new pack from colour tags and the pack's
  subject, which is only a starting point: colour filed blue beds under Water and green
  armchairs under Plants. A review pass fixes it, and the owner can always **Move**.
- **`title`** says what the prop is ("Hospital bed, blue sheets"). The tray shows it and
  search matches it; the owner's Rename wins over it. Anything broken, rusted, bloodied
  or overgrown is Derelict & damaged whatever else it is.

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
8. **Review** the set: `titles.py sheet`, a reviewer working to
   [tileset-review-brief.md](tileset-review-brief.md), then `intake.py`. This names it,
   fixes its categories, removes what the owner excludes and splits stuck pairs.
9. **Verify** with `register.py --validate`, the registry test and the native suites,
   and commit only when they pass, with explicit paths.

## One object, one box

Work from the untouched scanner boxes, never by patching a merged result.

- **Blob pre-pass.** A box holding two or more boxes that cover â‰¥ 70% of it is the
  gap-tolerant blob of separate objects. Drop it, alias its id to its largest part.
  Skipping this made the merge "absorb" single chairs into chair pairs (446 blobs).
- **Merge** two boxes when art crosses their contact: a run of opaque pixels â‰¥ 60% of
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
- **Near-duplicates are variants.** The look-alikes were gun racks with different guns,
  portholes with different views, monitors with different screens. Only four props in
  10,000 were pixel-identical. Never auto-delete look-alikes; `variants.py` groups them
  and the tray folds each family to one tile. Compare a prop with a family's **first**
  member only: comparing with any member chains unrelated props through a run of
  neighbours. `sweep.py` and `merge.py` keep `variants.json` to props that exist.

## Reviewing a whole library with agents

The first library was 10,600 props: 42 sets, about 170 pages. Three sets were named in
the main session; the other 39 by review agents, which the owner's CLAUDE.md allows for
large independent work. What made it work, and what went wrong:

- **One written brief**, [tileset-review-brief.md](tileset-review-brief.md): what a name
  is, the sixteen categories with guidance, the owner's exclusion list, what counts as a
  split and as a hole. Agents only read page images and write one JSON file per set.
  They never touch the repo; `intake.py` applies their work, one set at a time.
- **Pages carry hints**: `H` where `unkey.py`'s detector sees key holes, `S` where a box
  has a near-empty line through its middle. Hints direct the eye; reviewers confirmed few
  holes at page scale, so the automatic estimate is the better hole list.
- **Save after every page, and run few at once.** Eight agents at once hit the owner's
  usage limit and lost 31 sets held in memory. Three agents, saving per page and resuming
  from partial files, finished.
- **Trust nothing.** Every number covered exactly once, real categories, sane titles, no
  brands; a set that would remove over 60% of itself stops for a person to look; a split
  is made only where there is a real seam. Verify each set **from the registry**, not from
  the printout: two intakes failed unseen behind a filtered log.
- **What the owner touched is theirs.** A reviewer removed a zombie crewman as a humanoid
  figure that the owner had deliberately refiled. `remove_ids` refuses anything starred,
  renamed or moved. Read the reviewer's list of doubts and put the judgement calls to the
  owner (cooling towers, shop fronts, occupied beds, gun turrets).
- **Registry writes are atomic.** `save_json` writes beside the file and swaps it in with
  retries. Opening the registry for writing truncates it, and Windows refuses the open
  while the Studio or the editor reads it; a failure after the truncate would have
  destroyed the registry.
- **Gate the commit on the suites.** One commit went out with two suites failing because
  the command chain did not wait on them.
- **Keep shell heredocs away from prose and regexes.** An apostrophe ends a quoted
  heredoc, and `\b` written through one became a literal backspace that made a filter
  match nothing. Write a script file.

Outcome: every prop named; 969 removed with reasons; 574 stuck pairs split and 25 listed
under `needs-split`; categories rebuilt by what things are (Food & kitchen went from 15
props to 556, and the catch-alls emptied).

## Titles: look, then name

Labels are `<Kind> NNN`, so search cannot find "locker". `titles.py sheet` renders a set
as numbered pages; read them, write `{number: "Title"}` or `{number: ["Title",
"Category"]}`, and `titles.py apply` it. Name what the prop **is**, plainly ("Incubator,
dark window"), and let repeats be numbered: that shows the owner where duplicates are.
The owner's Rename always wins over a title.

The pass is also where categories get fixed, because someone is finally looking. In Wet
Lab the colour tags had filed an eyewash station and an exit sign under Plants,
test-tube racks under Screens and blue reagent bottles under Marine; 44 of 198 moved.
Do one set, let the owner judge, then continue: it is many image reads per set.

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
- Props crushed harder than the conversion's own Ã—0.52 are restored to source Ã— 0.52.
  That is what had turned grey rock near-black.
- Plants get a higher target (0.28). The owner flagged dark plants three times before
  the distribution was measured; measure the distribution the first time.
- Screens and mid-greys are restored per pixel toward source Ã— 0.82 and Ã— 0.62, using
  masks built from the **source** sheet. Use the same pixel tests for the repair as for
  the measurement, or most measured pixels never qualify for the lift.
- The library stays a touch under the owner's numbers on purpose. "A bit more" is a
  cheaper correction than "too much".
- **A repair must be a fixed target per pixel, or every run lifts again.** The first
  repair blended its gain by mask strength, which moves fringe pixels part of the way
  each time. `tone.py` uses a mask-weighted target instead and never lifts a prop past
  90% of its source, so a second run changes nothing and coal stays coal. Because the
  first library was repaired the old way, a library-wide run today would lift fringe
  pixels on most sheets once more: use `--only <set>` for a new pack, and treat a
  library-wide pass as an art decision for the owner.
- Many flagged props are correctly dark (coal, rubble, blacked-out screens) or correctly
  grey (chain-link, steel pipe, newspaper). The packs are also simply less saturated
  than the owner's art (0.21 against 0.50 at source); conversion did not cause that.
  Show the owner the outliers; do not "fix" a number.

**Match a sheet to its source by alpha identity, never by file name.** Packs share names
like `tile-B-01.png`. A name match repaired sheets against the wrong source and came out
blotchy; it was caught only because the before/after was rendered. Hash the alpha channel
(conversion never touches it) and verify per sheet before writing.

## Key holes and grey whites: the vendor's art, not the conversion

Several packs were keyed against white, so white pillows, sheets, panels and highlights
are transparent in the vendor's own files. A fresh extraction of the archive is byte for
byte the working copy, and the colour under the key is erased to black, so re-pulling
originals cannot help. `hole-report.json` lists about 420 affected props.

- **Automatic repair does not converge** (`unkey.py`, three attempts). The worst holes are
  open to the background, the key having eaten through the prop's edge, so enclosure
  tests refuse them; and the only pixels left beside a hole are its dark fringe, so any
  fill sampled there reads as a grey or black patch. An early limited pass on 56 props
  was kept; nothing else.
- **Patch by hand what the owner uses.** They star a prop; render it enlarged over magenta
  with a pixel grid; name the damaged regions by eye in `hole-patches.json`. A patch fills
  what is transparent in the SOURCE inside its region, in the median of the brightest
  third of that surface's surviving pixels. A round housing is an `ellipse`, since its
  hole runs off any rectangle.
- **Whites come out grey**, because the conversion halves every prop's brightness. A
  `whiten` step lifts a white surface as a whole, patches included, to a target (0.80).
  It must be a pure function of the source: two versions that read the sheet being edited
  drifted whiter on every run. Prove stability by running three times and comparing hashes.

## The owner's review pass: stars mean "fix this"

After looking at every prop in the Studio the owner marked 504 for removal and starred
447 as cut wrongly, holding several objects, or holed. The order that worked:

1. **Commit the marks first**, as they are. Everything after rewrites them.
2. `sweep.py` for the removals (undo: `sweep.py --restore`).
3. `refit.py --starred`. Most wrong boxes are wrong the same way: the scanner boxed by
   grid. What it lists as "no art of its own" is usually the half of a wrong split: an
   earlier seam cut single machines in two because `seam()` accepts a line half full of
   art. Rejoin those (`split.py --undo`), then refit the whole.
4. `patch_holes.py --suggest-starred`, with **every** vendor folder in `--sources`
   (a pack left out reads as "no source"). Look at the preview before writing.
5. `cut.py` for what is drawn touching: read review pages, write counts, look at the
   preview, apply. Never run `refit.py` on a piece cut from a scene tile: its art is
   connected to the rest, so the box regrows to the whole tile. Scene tiles often
   overlap each other on the sheet; alias the contained one to the containing piece.
6. Name the new pieces the same way (numbered pages, one JSON of titles per page); no
   title may be left ending in "(part N)".
7. What is left needs eyes: objects drawn touching each other, holes open to the
   background, scene tiles that are several props by design.

Two rules the registry test enforced on the way: an id is never reused once it has been
an alias or a removal (`free_id`), or a layout's alias lands on a different object; and
`remap_marks` leaves marks on the game's own installations alone.

A fill colour must be sampled only from pixels that survive in the SOURCE. Sampling the
sheet let one run's fill colour the next, and one sheet never settled.

## The owner's notes: the rename field as a bug report

When stars alone do not say what is wrong, the owner types the problem into the prop's
Rename field ("remove table next to arm", "transparent sections"). Read `names.json`,
render each noted prop enlarged with a 10-pixel grid and its neighbours, fix it with the
smallest tool that works (`cut.py`, then `isolate.py`, then a hand patch: `solid` for a
soft key, `fill` for holes the source does not show), and delete the note when done.
Judge holes over MAGENTA, never over the floor grey: a grey drum's holes vanish on it.
The Studio's Rejoin button merges every part of a split set; if pieces vanish after the
owner's session, compare ids with HEAD before assuming a tool did it.

## The Studio side

Tray controls: kind filter, set filter, search (label, set and the owner's name), **â˜…
Favourites**, **Marked for removal**, **Star**, **Mark for removal**, **Move to
categoryâ€¦**, **Rename**, **Split in two**; Ctrl/Shift-click selects several and the mark
buttons act on the batch. The crew picker stands Bill, Marsh, Branforth or Veld in the
room. A progress bar under the tray title counts previews as they render.

- The tray renders **one preview per frame** in a SubViewport. It lists at most
  `TRAY_LIMIT` (280) entries and says how many it hid. Without the cap, "All assets"
  pegged a core for sixteen minutes.
- **Never call a whole-catalog scan per entry.** `family_variants()` inside the rebuild
  loop was quadratic: the Studio froze on open and the editor test crept from minutes to
  42. Hoisted, the test takes 24 seconds. A loading screen would have hidden the bug.
- Floor finishes: a room samples a finish as a 4Ã—4 atlas, one quarter per 48-unit cell,
  so a tileset floor is one tile repeated 4Ã—4. The game draws every finish at 42% over
  the base floor; new finishes read as subtle as the existing ones.
- Floor decorations, wall decorations and lights are the game's own authored systems per
  room. The tray offers them nothing because no library art is wired in. They are not
  dead; do not remove them to tidy the list.

## Sweeping what the owner marked

Use `tools/tileset_library/sweep.py`; it does the following, and `--dry-run` shows it first.

1. Print the mark files. Keep anything also in `favourites.json` and tell the owner.
2. Remove the registrations and blank the art on the sheets, written atomically (temp
   file, then replace). **Blank only pixels no surviving prop's region covers.** Boxes
   overlap where props sit close: blanking whole boxes took 54â€“65% of the art out of five
   props the owner had kept. `register.py --validate` caught it; they were restored from
   the commit before the sweep.
3. Append to `removed.json`, empty `retired.json`, then validate.
4. A merge re-run must drop `removed.json` ids and any region left with no opaque art.
5. Delete a folder only when nothing references it, checked across the repo.

## Extending the owner's layout to other rotations

Layouts live outside the repo in `user://room_layouts.json` (on the owner's PC:
`%APPDATA%\Godot\app_userdata\BrineSpace\`), keyed `<asset>/<quarter>`. A missing quarter
falls back to authored defaults, not to quarter 0. The room stays riser-north in every
quarter; only the open door sides move (`Geometry.has_port(room.layout[0], side)`).

Drive the real editor from a `--script` probe: `switch_room`, `switch_rotation(q)`, copy
the whole 0Â° draft (positions, flips, sizes, floor, removed defaults), nudge anything
intersecting `Store.door_lane(side)` for an open side the shortest way out, require
`issues()` empty, then `save_layout()`. Back the file up first. Screenshot all four and
send them; the owner's eye accepts a layout, the validator only permits it.

## Verifying

- `tests/test_tileset_registry.gd` checks the whole registry against the contract on the
  sheets themselves, plus that marks, removals and floors resolve. It is headless, takes
  about five seconds and runs in the default lane, so a sweep that cuts into a kept prop
  or a registration written in the wrong coordinate space fails on the next plain
  `python tools/run_tests.py`. It was proved against planted faults.
- The Studio suites are native lane only: `python tools/run_tests.py --native --only
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
- The game must follow `merged.json` too. `Library.base_id` resolves aliases, because a
  merge once emptied three placed props out of the owner's Research Lab: only the tools
  had followed the map. The registry test checks every alias lands on a registered prop.

## Migrated originals still used by runtime â€” September 20

Do not infer runtime reachability from `legacy/default` versus `legacy/retired`.
Base furniture may still load during Grid initialization or bounds calculation
when a bought layout hides it. Check concatenated and formatted paths as well as
literal paths when moving art. Exercise lazy loaders in all four directions:
`tests/test_runtime_room_art.gd` reproduces the migration failure and covers the
repaired room families. Null-returning raw texture loaders need explicit checks; the runtime test now
checks all five foundation variants as well. For station capture, verify visible
rooms and settled retained layers rather than relying on a fixed frame count.
Use exact bindings for small known sets (such as the three power machines), and
check the release dependency closure. Do not solve a missing path by generating
replacement pixels or by suppressing SafeImage diagnostics. Native editor checks
are not release-executable acceptance. See docs/RUNTIME_ART_MIGRATION_2026-09-20.md.


Owner-reference review (September 21): Research combines overlapping equipment into
assemblies; Crew Lounge layers furniture and rugs. Bounding-box intersection alone
cannot reject these compositions. Record overlaps for visual inspection, and keep
floor access/physical obstruction separate. A straight center-to-door segment test
can flag an indirect route; inspect actual navigation before calling it a gameplay
bug. Never rearrange owner references merely to satisfy a simplistic art-bounds gate.

Door access diagnostics: use the preview navigation graph instead of requiring a
straight route from room center. Report the exact prop collision rectangles at a
blocked endpoint, including actor clearance. A preview failure is not a live-game
navigation finding until effective gameplay props and routing are checked. Research
q2 demonstrates this distinction; preserve the owner's reference layout meanwhile.

A thin stray line beside a prop may be a neighbour caught in its registered crop,
not damaged source pixels. Inspect the whole source sheet and the prop's full
extent (including chair bases) before repainting. For a corrected rectangle, update
region, absolute pieces, display_width and footprint together with set_geometry;
then recheck native placement in every used rotation. Bio's lab-20 correction
removed a neighbouring table edge and restored the chair without editing the sheet.

Battery composition lesson: navigation success does not establish enough visual weight. Review the primary machinery at gameplay zoom before adding filler. A display-scale adjustment is not a source-resolution repair; preserve source art and inspect pixel/detail fit beside the existing crew and room.


Reactor composition lesson: inspect the actual subject as well as its broad
category. A small reactor control housing did not read as the room's main machine.
A reactor stack, cooling assembly and operator console clarified the function
without filling the open service area. Hide unused layout placements, not library
entries. Bought substitutions do not inherit legacy-ID animation overlays; record
static machinery separately from operating-animation acceptance.

## Command Center review lesson (September 21)

Source titles are not visual evidence: ns-154 is labelled an office chair but its
actual crop is a wooden crate. Inspect selected source pixels before composing;
keep registry label repairs separate from owner names/marks. A central briefing
station needs circulation around its base and a clear south-door approach. The
first Command Center candidate at y50 blocked all four quarter checks; y-12 passed.
Use full RGBA array equality for saved/default image comparisons; do not rely on
a difference bounding box that may ignore RGB changes under unchanged alpha.
Installed stills and geometry do not establish operating-console animation.


Salvage rotation lesson (September 21): audit the effective prop IDs after each
rotation-specific restoration, not just navigation. Deleted legacy equipment
returned and the sorter disappeared in q3 even though routes passed. When the
full-wall bank is explicitly removed, retain the layout-store result rather than
reapplying the old bank-specific furniture restoration. Exercise repeated setup
and assert both deleted IDs and surviving functional equipment. Quarantine q2
showed the same failure: berth/filter/monitor returned while the cabinet vanished.
Also inspect inherited default copy entries when a saved override omits them;
absence from an override does not mean deletion from the merged layout.

Promotion lesson: saved layouts are sparse overrides. Materialize previous defaults
merged with candidate overrides before replacing a default key. Otherwise omitted
size/flip/source entries may vanish. Construction q2 lost an inherited panel size;
full RGBA comparison caught the mismatch. Compare effective native saved/default
views after promotion, not just equality of the JSON entries you wrote.


Biomass candidate lesson (September 21): a missing focal machine does not justify
installing the first large processing sprite. Review visible top planes and height
against the camera contract at live scale; tall factory elevations can pass all
walking checks. Establish adjacent inlet/feedstock handling before adding effects.
Repeated door-quarter captures do not prove authored equipment orientations.


Collision/shadow distinction: registration footprint controls floor shadow.
Geometry.prop_collision_rects uses collision_boxes when present, otherwise the
full prop rectangle. Do not claim a footprint change repairs routes, or weaken
collision merely to expose a depth overlap. Check the actual collision consumer.
For a room-specific operating screen, use a dedicated registration so other
rooms sharing the bought source keep their behavior.


When giving a prop a consistent position across quarters, also inspect inherited
size and flip values in each effective layout. Shield q1/q3 used a larger coupling
than q0, blocking west approaches at the same coordinates. Explicit intended size
and removal of the inherited q3 patch rack resolved routes and visual overlap.
Do not infer equal footprints from equal position arrays.


Radio restoration lesson (September 21): assert preservation of explicitly placed
legacy furniture as well as bought props and deleted IDs. A bank wrapper can keep
library entries yet silently discard a standalone bench in one quarter. Repeated
setup regression reproduced this q2 failure. A clean route/overlap report still does
not make isolated corner equipment a coherent workstation; review live scale before
promoting layout candidates. See SUPPORT_ROOM_REVIEW_2026-09-21.md.


Radio panel placement lesson: legacy dressing placement anchors are not always the
upper-left visual corner. Check native prop_visual_bounds against the raised wall;
a route-valid panel can overlap it. Lowering the panel anchor corrected the r3
wall overlap in r4 without changing source pixels or weakening collision. Static
screen imagery must not be reported as operating feedback.


Workshop composition lesson (September 21): inspect existing overhead assemblies
before placing individual tools. A teardown bench already supporting its tools,
parts and workpiece conveys the activity better than an empty table plus a loose
floor tool board. Group bought machining equipment and cargo handling around it.
A restored static powered indicator is not new mechanical animation. Review every
quarter when the primary assembly has separately authored directional art.


Holographic Core lesson (September21): legacy position fallbacks must not overwrite
an explicit merged layout position after apply. Test actual coordinates over repeated
setup, not only retained IDs. Bought hologram glow can be baked imagery with no
operating metadata; restoring another machine's animation does not make it respond
to power. Increasing scale reveals coarse pixels rather than adding missing detail.


Layered projector lesson (September21): keep physical housing in a static source and
render the projection from operating state and the station visual clock. Reserve
transparent effect bounds separately from explicit physical collision boxes; shadow
footprint is not collision. A custom library effect needs custom_library_draw and
live classification in the retained renderer, checked after repeated setup. Test
actual station pause as well as repeated held-clock captures. A repaired projector
does not establish offline correctness for a separate baked-glow chart display.


For a flat bought chart panel, a dedicated registration can sample only the original
stand while the room renderer supplies a dark panel and switched telemetry. This
avoids repainting the shared atlas or placing live curves over still-glowing source
pixels. Verify the stand region stays pixel-identical between powered states and
the custom chart remains live after repeated setup. Preserve its full original
region for placement/scale even when sampled pieces cover only the stand.


Radio display verification lesson: constrain powered and animated pixel differences
to the actual source apertures (with stated raster tolerance), not just the full
machine bounding box. Check both displays independently and preserve surrounding
bezel/cable pixels. Distinguish repaired displays from decorative source indicator
lamps; do not claim that every light in the room has correct power behavior.


Powered-display retention: custom renderers should classify clock-driven emission
as live only while operating when their offline source is static. Test on/off/on
with the same queue and prop objects so power-state invalidation is exercised,
then compare retained and direct pixels. Count the saved redraws without converting
that scoped result into an unmeasured overall FPS claim. Preserve other machines'
classification rules rather than applying a global offline rule.


Medical support lesson (September21): identify whole supported assemblies before
adding accessories. A consultation table includes its seats; the diagnostic console
includes its stool. Do not leave duplicate loose seats, floor laptops or examination
lights floating over unrelated furniture. Records rooms benefit from filing storage,
not inherited medicine cabinets. Med Center q3 also dropped an explicitly placed
console despite passing routes; presence/position checks across repeated setup catch
missing support furniture that route tests cannot.

Power grouping lesson (September21): removing loose gauges can leave a room sparse;
group the remaining medium controls by activity before adding more pieces. Heat
Recovery's tighter grouping blocked a west-door approach despite nonoverlapping
sprites. Keep the actual crew clearance through the service aisle, then review at
gameplay scale. Turbine supports need quarter-specific grouping around directional
machinery. Verify native saved/default pixel parity after promotion and wait for
the card baker to finish before reviewing its outputs.

Anomaly effect integration lesson: bought props can carry full_wall=true after
bank layout application. A full_wall.owns early return can therefore bypass a
room-specific overlay even when custom_library_draw is set. Trace effective flags
and test each intended effect independently. A prototype subclass may work because
its overlay executes after the parent returns; integrating into that parent changes
the order. Require installed/prototype pixel parity, not only whole-room motion.
# Shared-renderer review identity

When replacing activity furniture, validate its service points as well as room
doors. Observation's bought sofa preserved reading but covered a rotated watch
anchor. A nearest-clear-point lookup fixes that interaction only if each activity
uses its own cache scope: `reachable_stations` stores results on the passed data,
so a sofa lookup must not reuse a watch lookup's anchors or mutate its modes.
Use its optional cache key to retain distinct activity lookups on the geometry
dictionary; copying and discarding the cache would repeat the whole point scan.

Airlock furniture review must retain its functional `pressure_chamber` and
`outer_hatch`: a saved null can remove collision and gate/control rendering while
leaving a convincing floor insert behind. Check wet-area exclusion and locker
service approach separately from doorway circulation. Studio's 172px actor bound
differs from production's 176px closed-wall bound; diagnose the actual service
point before moving furniture to satisfy a preview-only limit. See the September
21 saved/default audit for the installed R2 and scoped verification.

A failed Studio grid route is not automatically a sealed passage or a live-game
failure. Probe the same clearance predicates at finer spacing to distinguish a
missed narrow band from obstruction; retain the original failure. Check production
geometry too: narrow corridor furnishing currently does not contribute live crew
blockers, whereas Studio previews do include its footprints. A diagnostic fine
route does not justify claiming the Studio walk passed or increasing production
graph density without measuring cost.

When a catalog reuses a renderer (straight, corner and T corridors), assign its
`room_id` before adding it to the tree, as the Studio does. A correct label does
not establish a correct rendered identity. Compare declared doorway masks with
the actual floor polygon in all rotations before diagnosing route failures.
Corridor hull renderers do not own generic room wall textures: preview helpers
must not call the generic north-wall renderer for these identities. September 21
evidence: `docs/LAYOUT_DEFAULT_AUDIT_2026-09-21.md`.
# Compound furniture collision

Composition refinement: removal-only cleanup can reduce scatter but weaken a
room's visual balance. Compare at unchanged native scale before promotion. A
single medium bought planter can replace loose plants without enlarging source
pixels; retain purposeful growing, tending and seating groups and their routes.
Refresh the relevant rollout-ledger entry and card hash when the selected layout
supersedes old furniture, rather than leaving a historically accurate but stale
prop list as the current review record.
Distinguish absent card-bound reviews from stale hashes and missing art. A valid
selected card with no ledger binding may have newer native evidence in a handoff;
do not automatically mark it visually rejected or overwrite historical review
hashes without inspecting the current artifact. Report generation must preserve
both prose and list-valued legacy limitations safely.

When a bed or other furnishing includes a shorter side cabinet, its full image or
placement rectangle can block visibly empty floor. Inspect the source silhouette
and production padded blockers before moving furniture or compensating with actor
offsets. Use conservative component collision boxes where supported; test solid
components as negative controls and the empty notch for both clearance and a route.
Verify unchanged native rendering separately. Opening a notch does not validate a
previously proposed animation entry or imply that a replacement bunk is functional.

## Furniture foreground layers

Split compound props into complementary full-atlas masks with original polygons
and UVs; separately triangulated pieces can alter filtered edges. Preserve source
textures and collision/layout dictionaries. Cache mask pairs once. Use stable queue
entries for both direct and retained drawing, with opted-in sleeping pose depth.
Layer entries copy presentation dictionaries: same-depth sideways moves must
invalidate those copies. Include rect, registration, flip and source texture in
layer signatures. Resolve variant_source before copy_source for source-specific
masks. Test empty, occupied, mirrored, retained/direct and sideways-move controls.
Use exact image bytes or all-channel differences for framebuffer parity: Pillow
RGBA getbbox can ignore RGB changes when alpha differences are all zero. A test
subclass can lose script.resource_path-based renderer identity; use a scoped switch
on the actual renderer when comparing behavior.
