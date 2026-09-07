# BrineSpace

A Godot 4.6 underwater station-restoration roguelite prototype. You play BRINE,
a damaged AI core rebuilding a silent station through blueprint drafting,
modular placement, interdependent production and discovered room synergies.

> "The station is quiet. That does not mean it is empty."

![BrineSpace in-game view showing a furnished Crew Hab, seabed, blueprint hand and station controls](docs/screenshots/crew-hab-gameplay.png)

*Actual Godot prototype capture, September 6, 2026. This paused room-review scene
shows the Crew Hab and live game interface; it is not a mockup or a full expedition.*

## Restore a station beneath the ocean

Build a little, watch the systems find their rhythm, and decide whether to risk
one more room. Every expansion needs supplies and a way to connect to the station.
Power keeps machinery running, life support sustains the crew, and drones bring
back the materials needed to rebuild.

The interesting choices come from placement and dependencies. A useful room can
also become another demand on a strained system. Discover relationships between
working rooms, keep them functioning long enough to stabilize their patterns, and
recover new blueprints without a recipe list spoiling the experiments.

The station also holds its missing people. Expand toward derelict cryo wards,
repair them into the base, and thaw the architects inside. Rescuing an architect
adds a named crew member and unlocks that character for future loops.

BrineSpace is designed to be thoughtful and watchable: an open-ended restoration
game with resource pressure, quiet machinery and an AI core with opinions. You can
pause to plan. The pressure comes from the station's needs, not rapid clicking.

## Current checkpoint

The [September 6 handoff](docs/BRINESPACE_HANDOFF_2026-09-06.md) records completed
work, unfinished acceptance, evidence and ordered next priorities. The source
project is newer than the last combined validated Windows package. This repository
checkpoint is not a release or a claim that all current systems passed together.

- 40 room identities with registered furniture, low underwater hulls, matching
  doors, rotations, operating effects and refreshed decoration/card artwork.
- Three architects: Major Bill, Dr. Veld and Chief Engineer Branforth. The selected
  starter wakes in BRINE Core; connected derelict cryo recovery unlocks the others.
- Mining, Salvage and Construction drones, finite deposits/scrap, cargo delivery,
  battery charging, paid construction and clearance.
- A Diving Airlock with lockers and an interlocked flooding/draining chamber.
  Actual crew chamber transit, exterior excursions and full suit changing remain
  unfinished. Swimming and equipment animations are still visually provisional.
- Layered animated title, shared settings/Codex, Save/Continue recovery, station
  search, construction queue, health priorities and resource/charge feedback.
- Authored seabed habitats, wreckage and composed exterior sites.

Current runs are open-ended. Starting doctrines, timed reconstruction directives
and legacy orbital POIs are retired. Construction costs, resource failures and
hidden recipe discovery remain active. Conclude Expedition banks the loop.

## Run locally

Install Git LFS and clone with Windows long-path support:

```sh
git lfs install
git -c core.longpaths=true clone https://github.com/BrinShadewater/BrineSpace.git
cd BrineSpace
git lfs pull
```

Use Godot 4.6 (tested locally with 4.6.1). Open `project.godot`, allow imports to
finish, and press **F5** to run the project through title, architect selection and
Continue. The configured main scene is `res://scenes/title_screen.tscn`;
gameplay is `res://scenes/main.tscn`.

The viewport is designed at 1920×1080 with a 1600×900 default window. Runtime room
art uses raw PNG loading; UI resources still need Godot import. LFS pointers are
not usable image files, so finish the LFS download before diagnosing missing art.

## Play loop

1. Start a New Loop with an unlocked architect and recover the starter from BRINE.
2. Draft and rotate blueprints, pay construction costs and connect matching doors.
3. Supply power, food, oxygen and other room inputs; inspect shortages and reserves.
4. Discover functioning room links and maintain three consecutive functioning
   cycles to stabilize patterns and unlock rewards. Hidden recipes stay hidden.
5. Recover wrecks/architects, harvest finite sites and expand at a sustainable pace.
6. Save/Continue or use Conclude Expedition to bank the loop. Resource collapse
   remains a failure condition; there is no directive deadline or scenario victory.

Controls include WASD panning, Shift + wheel zoom, F to fit, R to rotate a selected
blueprint, Space to pause, J for the journal, and Ctrl+F to find installed rooms.

## Development and verification

Read [AGENTS.md](AGENTS.md), [Development Notes](docs/DEVELOPMENT_NOTES.md) and the
[visual bible](docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md) before changes. Keep the
prototype focused on satisfying placement decisions; avoid unrelated architecture
rewrites or disabling normal costs/failures to make tests pass.

- [Room furnishing status](docs/ROOM_FURNISHING_STATUS.md)
- [Current decoration integration](rooms/decoration-integration/README.md)
- [Architect recovery](rooms/architect-cryo-v1/README.md)
- [Current crew animation revisions](character/crew-underwater-v1/revisions/README.md)
- [Airlock implementation](rooms/underwater/airlock-v1/README.md)
- [Drone fleet](docs/DRONE_FLEET.md) and [finite harvesting](docs/FINITE_DRONE_HARVEST.md)
- [Menus](docs/MENU_SETTINGS.md) and [navigation/Continue](docs/STATION_NAVIGATION_AND_CONTINUE.md)
- [Package and traffic follow-up](docs/MAT_REPAIR_PACKAGE_FOLLOWUP.md)

Tests are under `tests/`; dedicated native capture/export tools are under `tools/`.
Use each report's specific fixture and completion criteria. Native screenshot
fixtures require rendering, while logic checks can run headless. A launched debug
executable does not prove its validation fixture ran. Current priorities are one
frozen integrated package, reproducible multi-crew traffic, continuous animation
review, the complete airlock excursion loop and longer human playtests.

## Repository contents

Game code, runtime assets, source provenance, tests, skills and documentation are
versioned, including selected in-game screenshots under `docs/screenshots/`.
Raster art uses Git LFS. `.godot/`, local backups and `output/` evidence,
review captures, downloaded templates and built executables remain local. Historical
documents may link to those local evidence paths; they are not hosted downloads.

Do not blindly stage generated capture trees. Export presets may refer to local
validation templates under `output/`; install/configure those before rebuilding
validation executables. No release binaries or player saves are included here.

## 📄 Licence

All rights reserved. This repository is public so the work can be read and referenced, not relicensed. The code, copy, and creative assets remain © Brin Shadewater / Shadewater Labs. If you want to use something here, ask.
