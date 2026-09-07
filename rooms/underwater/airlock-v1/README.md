# Diving Airlock — pressure chamber revision

Current art refinement: [underwater hull fittings](../airlock-v4/README.md), using
`airlock-v4/card.png` and `output/airlock-v4` native evidence. The source and earlier
card paths below document the previous revision.

Buildable common Engineering room: 6 Metal and 1 Power to construct, 1 Power per
cycle to operate. It is a starting unlock and enters newly generated draft decks.
Existing saved hands/decks are preserved. One station entrance rotates with the
room. The dry preparation area surrounds a separate central pressure chamber.

Select a built, powered airlock, choose an available architect in the inspector,
then use **Fit Diving Helmet** or **Return Diving Helmet**. Bill, Veld and Branforth
walk to the locker bank's west fitting shelf and play their authored east-facing
equipment animation. Gear changes only after the animation completes. The suits
on the rack are room dressing; this version does not animate changing full suits.

The single fitting station reserves itself through the crew's existing pending
request or active animation. Equipment is reusable; there is no finite stock.
Power loss or suspension interrupts service without changing the previous gear
state. Pause holds the action. Pending trips and partial animations use the
existing validated crew Save/Continue state. Existing death and topology changes
cancel pending work. Chamber transit, exterior travel and explicit pickup/deposit
hand motion remain future work; roaming crew stay outside the chamber's collision
footprint, in the dry preparation area.

## Pressure cycle

Inspector controls cycle the chamber independently of the dry locker station.
Outbound: seal inner door (1s), flood (4s), equalize pressure (2s), open outer
hatch (1s). Returning: seal outer hatch (1s), drain (4s), restore station pressure
(2s), open inner door (1s). These are prototype timings at normal simulation speed.
An occupied or obstructed exterior approach refuses an outbound request.

`scripts/airlock_cycle.gd` derives both door apertures, water and pressure from one
phase and elapsed time. Both doors are sealed during flooding, draining and pressure
changes; one door must fully close before the other can start opening. Repeated or
opposite requests during a cycle are rejected. Power loss and suspension freeze
the current state; restoring power resumes it. Pause freezes progress. This is an
animated mechanical sequence, not a physical fluid simulation. It does not consume
the station's potable Water resource. Existing room Power consumption remains.

The optional `airlock_cycle` field on placed rooms persists through Save/Continue.
Unknown phases, non-finite/out-of-range elapsed values and cycle fields on other
room types are rejected before restore. Old saves without a cycle load dry.

## Art and registration

`source.png` is the unmodified imagegen result (1254 × 1254, RGB white background).
`prompt.txt` records its prompt. The existing equipment front cutout was supplied
as the helmet reference. `build_assets.py` performs connected exterior-background
cleanup into RGBA `cutouts.png` and writes `composition.json`; it does not repaint
the source. Four registered props supply the suit lockers, sealed hatch,
compressor and changing bench. The locker bank includes a side fitting shelf to
support the existing east-facing crew animations. Rotation-specific placement
keeps that approach inside the room and outside furniture collision footprints.

`airlock_view.gd` uses the shared room shell, floor and dressing renderer. The
central chamber reuses shared wall and two-leaf door geometry; its registered
floor shows water filling/draining and a pressure gauge. The source hatch's center
reveals a dark aperture when opening. No new source image was generated for this
revision. The fourth rotation's lockers move to keep their approach navigable.
The north-facing hatch now mounts on the rear riser, with its threshold at -190
and crown at approximately -245 in room space. Its 56-unit width keeps its source
aspect ratio within the shared riser's height. The chamber extends back to that
threshold. Wall-mounted hatch art is exempt from furniture floor containment;
its actual bounds are tested against the riser. Other rotations keep their current
layout. The airlock's rear wall omits the decorative window behind the hatch.

`card-v3.png` is the current 512 × 512 native Godot render, baked by
`tests/test_airlock.gd`; older card images remain as history.
`manifest.json` records source, cutout, card and composition hashes.

## Validation

`tests/test_airlock.gd` exercises all three architects, all four Bill room
rotations, collision-free locker travel, fit/return, reservation, power loss,
pause, and real disk saves during both travel and fitting. It also exercises all
ten pressure phases, mutual exclusion and pressure/water conditions at every
100ms step, Save/Continue in each phase and invalid checkpoint rejection.
Native stage captures and 200ms cycle frames are written to `output/airlock-v3`,
with a rear-wall margin included in the captures.
Inspector captures cover 1280, 1600 and 2560 pixel widths.
This is source-project integration, not a packaged export validation.

Latest native run passed with 1,038 travel samples and all three inspector widths.
Crew death/equipment saves, run saves, architect recovery and drone fleet
regressions passed. Composition dependency hashes passed; PNGs use Git LFS and
new Godot scripts have paired resource UIDs.
