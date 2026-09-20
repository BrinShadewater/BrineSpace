# Review brief: naming a tileset set

Give this to whoever reviews a set, person or agent. It is the contract `intake.py`
checks their file against. NAMING is the folder `titles.py sheet` wrote its pages to.

You are naming pixel-art props for a game called Brine Space: an **underwater research
station**. The owner decorates rooms by hand in an editor and finds props by typing in a
search box, so a name must say plainly what the prop IS. You only READ images and WRITE
one JSON file per set. Do not touch any file in the game repo.

## What you are given

Folder: NAMING, the output folder of `python tools/tileset_library/titles.py sheet`.

For each set, with `<slug>` = the set name lower-cased with spaces as hyphens
(e.g. "Reactor Hall" -> `reactor-hall`):
- `<slug>-0.png`, `<slug>-1.png`, ... : pages of up to 60 props, 10 per row.
- Under each prop: its NUMBER, then the first letters of its current category.
- A small magenta tag in a prop's top-right corner is an automatic hint, often wrong:
  `H` = may have holes where the art was keyed out, `S` = may be two objects in one box.
- `manifest.json` lists every set with its page count. Read EVERY page of your sets.

## What to write

For each set, write `NAMING/<slug>-titles.json`:

```json
{"set": "Reactor Hall",
 "index": "NAMING/<slug>-index.json",
 "titles": {"0": "Coolant pump, twin", "1": ["Control desk, reactor", "Screens & computers"]},
 "remove": {"14": "armoured truck: outdoor vehicle"},
 "split": [22, 23],
 "holes": [5, 31]}
```

Use the real absolute path for "index". Every prop number on every page must appear in
exactly one of `titles` or `remove`.

### titles
- A string, or `[title, category]` when the current category is wrong.
- 2 to 5 words. Object first, then what distinguishes it: "Locker, steel", "Hospital bed,
  blue sheets", "Test tube rack, amber", "Workstation bank, three desks".
- Plain words a person would type: locker, crate, barrel, desk, console, monitor, pump,
  tank, pipe, valve, shelf, cabinet, bench, bed, chair, plant, sign, door, hatch, ladder.
- Distinguish look-alikes by colour, size, state or view: "side view", "back view",
  "open", "broken", "stocked", "empty", "pair", "set of three".
- If several props really are the same thing, give them the same title; they are numbered
  automatically. Do not invent differences.
- No brand names, no real-world place names, nothing that contradicts an underwater
  station. No words copied from text drawn in the art unless it is what the object is.
- If you cannot tell what something is, describe it honestly: "Machine, grey with dial",
  "Panel, blue lights". Never guess a specific function you cannot see.

### category: exactly one of these sixteen, spelled exactly
Seating & tables | Storage | Screens & computers | Lab & science | Plants & growing |
Power & reactor | Industrial & workshop | Water & marine | Medical | Food & kitchen |
Mining | Military & security | Ship interior | Offworld surface | Shelter & survival |
Derelict & damaged

The current categories were assigned by COLOUR and are often wrong: blue beds were filed
under Water & marine, green armchairs under Plants, blue bottles under Marine, test-tube
racks under Screens. Fix them. Guidance:
- Chairs, sofas, benches, desks, tables, counters -> Seating & tables
- Lockers, cabinets, shelves, crates, barrels, boxes, bins, drawers -> Storage
- Monitors, consoles, terminals, servers, phones, printers -> Screens & computers
- Lab glassware, microscopes, centrifuges, specimen tanks, fume hoods -> Lab & science
- Real plants, planters, grow beds, hydroponic racks -> Plants & growing
- Reactors, generators, batteries, turbines, transformers, fuel -> Power & reactor
- Machine tools, workbenches, robot arms, conveyors, pipes, valves, pumps -> Industrial & workshop
- Aquaria, fish, coral, diving gear, water tanks, boats' fittings -> Water & marine
- Beds for patients, scanners, IV stands, first aid -> Medical
- Cooking, eating, food, drink, vending -> Food & kitchen
- Ore, carts, rails, picks, rock piles -> Mining
- Gun racks and armoury furniture, cameras, barriers, turrets -> Military & security
- Doors, hatches, windows, wall panels, floor plates, ladders, lights, signs, bunks -> Ship interior
- Rocks, craters, alien terrain and growths -> Offworld surface
- Survival supplies, camp gear, bunker fittings -> Shelter & survival
- Anything broken, rusted, bloodied, ruined or overgrown -> Derelict & damaged
  (this one wins: a broken monitor is Derelict & damaged, not Screens)

### remove: things the owner has excluded. Give a short reason.
Mechs and mech parts; outdoor vehicles other than forklifts (cars, trucks, tanks, rovers);
spaceships, rockets, satellites; helicopters and aircraft; warships, boats, lifeboats,
life rafts, oars; outdoor buildings, bunkers, domes, hangars; shipwrecks; medieval chests;
cannons, deck guns, missiles, torpedoes, loose guns, swords, armour suits; spacemen and
any human or humanoid figure; solar panels; giant mining vehicles; signs or screens whose
main content is readable English text.
Also remove anything that is not an object at all: a block of floor or wall swatches, a
stray fragment, an empty-looking sliver.
KEEP furniture even when it holds weapons (gun rack, armoury bench, ammo shelf), and keep
forklifts, cranes, robot arms, radar dishes, rocket engines as machinery, EVA-suit racks.
When unsure, KEEP and name it.

### split: numbers of props that are clearly TWO OR MORE SEPARATE OBJECTS in one box
Two chairs stacked, two monitors one above the other, a plant and a lamp side by side
with clear space between. Still give the prop a title (describe the group). Do NOT list
single objects that are merely tall (a hydrant, a bunk bed, a sink with a mirror, a
potted plant, an IV stand) or deliberate sets that belong together (a desk with its chair).

### holes: numbers of props with visible transparency damage
Patches where the background shows through a surface that should be solid: pillows,
sheets, white panels, highlights, screens. The page background is grey-green, so a hole
looks like grey-green showing INSIDE an object. Do not list real gaps: between rails,
under furniture, through a ladder, in a mesh or grille, the opening of a scanner.

## Working method
- SAVE AFTER EVERY PAGE. Write (or rewrite) `<slug>-titles.json` as soon as a page is done,
  with everything so far. A previous run lost hours of work by holding results in memory
  until the end and then being cut off. A partial file is valuable; an unwritten one is not.
- If `<slug>-titles.json` ALREADY EXISTS, load it, keep its entries, and continue from the
  first number it does not cover. If it already covers every number, skip that set.
- Do your sets in the order given. Finish one set completely before starting the next.
- Read a page, then write its entries before reading the next. Do not batch from memory.
- Count: the last number on the last page is (props - 1) from manifest.json.
- Before you finish a set, check the JSON parses and every number is covered:
  `python -c "import json;d=json.load(open(r'<file>'));n=len(json.load(open(d['index'])));m=[str(i) for i in range(n) if str(i) not in d['titles'] and str(i) not in d.get('remove',{})];print(n,'props; missing:',m)"`
- Your final reply: one line per set with counts of titled / re-categorised / removed /
  split / holes, and anything you were unsure about. Be honest about uncertainty.
