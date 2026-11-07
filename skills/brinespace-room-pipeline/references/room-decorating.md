# Decorating a room from the prop library

For an agent asked to furnish a room. The owner decorates by hand in the Layout Studio
and is the authority; this is what their rooms measure as, what general set-dressing
craft says, and what the first scripted attempt got wrong. Measured September 20, 2026
on the owner's nine hand-made rooms (76 placed library props) against 34 scripted rooms.

## What the owner does (measured)

| | Owner | First script |
|---|---|---|
| Props per room | median 7 (3 to 16) | 10 to 12 |
| Prop size (area, room units) | median 3,700 | 2,300 |
| Placement size | median 61%, middle half 50-72% | 70% flat |
| Gap to the nearest prop, edge to edge | **median 4 units; 63% touch or sit within 8** | median 11; 34% |
| Where | **63% in the back third**, 21% middle, 16% front | 47 / 19 / 34 |
| Against a wall (within 25 units) | 76% | similar |
| Left/right balance | uneven on purpose (0.33) | near symmetric (0.11) |
| Same kind of prop twice in a room | rare (6%) | rare |
| Floor covered | about 19% | similar |

What they put side by side: hospital bed + IV stand + privacy screen + drug trolley;
CNC machine + workbench; computer desk + charging tank; pipe stand + tank unit; analyser
+ steriliser cabinet. Every pair is a **working group**: things a person would use together.

Read as rules:

1. **Fewer, bigger pieces.** Seven substantial props beat twelve small ones.
2. **Build working groups, touching.** Pick a job done in the room (treat a patient, run
   the lathe), place its two to four props edge to edge, then leave floor. Two to three
   groups per room. Never scatter single props along a wall at even spacing.
3. **Weight the back.** Most of the room's mass stands against the back wall and the
   back halves of the side walls; the front third stays mostly open, which also keeps
   the view of the crew clear.
4. **Asymmetry.** One side heavier than the other. Mirror-image rooms read as generated.
5. **No filler.** The owner places almost no generic extras. An extinguisher and a bin in
   every room is a script's idea, not theirs.
6. Leave about four fifths of the floor open, and every door approach clear.

## What set-dressing craft adds (sources below)

- One **focal piece** per room; everything else is subordinate to it. Hero props appear once.
- Compose in **clusters of related detail**; proximity and similarity make a group read as
  one thing. Build them asymmetrically: place one, then a smaller related one, offset.
- Props must keep the space **legible**: the walking route from door to door should read
  at a glance.
- Small clutter tells the story (the mug, the toolbox), but only beside the thing it
  belongs to.

## What worked: groups, not lists (the fourth attempt)

Three passes placed props one by one from a shopping list, hugging the walls. Each fixed
real bugs (overlaps, blocked doors, hallway floors) and still looked generated. The fourth
placed **working groups**: an anchor flush to the wall, its companions touching it on the
same baseline, 26 units of open floor between groups; group one back-left, group two
back-right, group three on a side wall further forward. Measured against the owner:

| | Owner | List passes | Group pass |
|---|---|---|---|
| Props per room | 7 | 10-12 | 7 |
| Gap to nearest prop | 4 | 11 | 4 |
| Touching or within 8 | 63% | 34% | 91% |
| In the back third | 63% | 47% | 63% |
| Prop area | 3,700 | 2,300 | 2,600 |

Still short: the owner picks chunkier art than title matching finds, and title matching
makes odd calls (two dining tables side by side). Rooms whose door lanes cross the middle
(Brine Core, Storage Bay) take few props; leave them sparse.

The tools are `tools/room_decorating/plan_groups.py` and `furnish_groups.gd`.

## Two ways a furnishing script has already gone wrong

**It strips the room first.** `furnish_groups.gd` nulls every authored default prop before
it places anything, keeping a removal only if `issues()` stays clean. On the BRINE Core
that deleted all five authored props — including `brine_chamber`, which the tank, the water
and BRINE's floating body all key off, so she stopped being drawn in her own core room. If
a room has authored furniture worth keeping, place into it instead of through that step.

**It furnishes the name, not the room.** `plan_groups.py` had the Emergency Isolation Vault
down as a strongroom — strongbox, hard case, crate, cot, locker — when the database calls it
*"Reserve power and emergency branch isolation controls"*, Engineering. Read the room's
`description` and `category` in `scripts/room_database.gd` before writing its group list.

## What the Studio does not check (a script must)

`tools/lint_room_layouts.gd` now checks all of this across all 188 room/rotations headless,
using the same collision rule the navigation graph uses, and writes `output/layout-lint.json`.
Run it after any furnishing pass. It found five doorways that crew could not walk through,
every one of them saved without a warning.

- Library props may overlap each other: keep your own list of taken rects.
- Library props may stand in a door approach: test `Store.door_lane(side)` for each open side.
- In hallways props may stand off the floor: test `Corridor.contains_foot`. A hallway is
  about 94 units wide with a 72-unit lane, so props there are about 22 units and touch the hull.
- Drive the real editor (`add_library_asset`, `issues()`, `save_layout()`) on a COPY of the
  layout store (`Store.path`), look at a screenshot of every room, then merge only rooms
  the owner has not made. Back the owner's file up first; never write a room they made.

Sources: [The Level Design Book, Environment Art](https://book.leveldesignbook.com/process/env-art);
[Slynyrd Pixelblog 35, Top Down Interiors](https://www.slynyrd.com/blog/2021/11/30/pixelblog-35-top-down-interiors);
[Environmental Storytelling in Video Games](https://gamedesignskills.com/game-design/environmental-storytelling/).
