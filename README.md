# BrineSpace

A Godot 4.6 underwater station-restoration roguelite prototype. You play BRINE,
a damaged AI core rebuilding a silent station through blueprint drafting,
modular placement, interdependent production and discovered room synergies.

> "The station is quiet. That does not mean it is empty."

![BrineSpace showing BRINE Core, underwater derelicts, blueprint cards and the station interface](docs/screenshots/station-gameplay-2026-09-09.png)

*Native Godot capture, September 9, 2026. This paused UI verification scene shows
BRINE Core and the current interface; it is not a full expedition.*

Rooms use authored layouts with larger equipment and restrained clutter. Raised walls start enabled; change **Raised room walls** in settings to use low walls. See the [room layout direction](docs/LARGE_ASSET_LAYOUTS_2026-09-09.md).

### A larger station

![A large BrineSpace station viewed at Fit zoom, with many rooms across the ocean floor](docs/screenshots/large-station.png)

*Native large-station performance scene with roughly 100 rooms. This is a
controlled test layout with injected supplies, not a normal paid expedition or
a claim of finished large-station performance.*

### Starting screen

![BrineSpace starting screen with BRINE in her tank, New Loop, Settings, Codex and Meta Progression](docs/screenshots/starting-screen.png)

*The actual starting screen, captured from the layered animated title scene.*

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

## Current checkpoint - September 9, 2026

The [combined polish and release pass](docs/FINAL_POLISH_RELEASE_2026-09-09.md)
brings together the latest room artwork, portraits, expanded companion animations,
flood responses and diagnostic/reporting improvements. Animation frame failures
now retain their timeline slots, and authored clip durations are precomputed.

Start with [current status](docs/CURRENT_STATUS.md) for the latest decisions and
[development notes](docs/DEVELOPMENT_NOTES.md) for the design direction. BrineSpace
is a playable prototype; balance, crew animation and longer expeditions are still
being evaluated.

- **47 room identities** with matching doors, four rotations, operating effects
  and authored furniture layouts. Most furnished rooms favor three or four large
  assets; BRINE Core keeps its more elaborate arrangement.
- **Four architects:** Major Bill, Dr. Veld, Chief Engineer Branforth and Marsh.
  Recover them to unlock future selection. Marsh is an android powered by a
  rechargeable battery; his derelict charging chamber has its own recovery sequence.
- **Three optional companions:** River, Josh and Margot. Find and restore their
  derelicts, unlock future selection, and watch their individual behaviors. River
  and Josh are robots; Margot is a cat you can approach and pet.
- **Working station systems:** paid drone construction, mining and salvage,
  finite deposits, cargo delivery, power demand and battery charging.
- **Underwater hazards:** room flooding, crew breathing and swimming, hull repairs,
  and an interlocked airlock for exterior excursions. Marsh needs charge rather
  than oxygen.
- **Readable planning tools:** placement feedback, resource forecasts, station
  search, diagnostics, a room inspector and a local Room Layout Studio.
- **A paced introduction and dialogue:** the loading introduction waits for
  Continue, and conversations pause the simulation until dismissed.
- **Save/Continue and expedition recaps:** preserve the station, recovered crew,
  companion progress and discoveries between sessions.

Current runs are open-ended. Starting doctrines, timed reconstruction directives
and legacy orbital POIs are retired. Construction costs, resource failures and
hidden recipe discovery remain active. Conclude Expedition banks the loop.

A [Windows build was verified on September 9](docs/WINDOWS_BUILD_2026-09-09.md).
It is a local dated package, not a download published in this repository; later
source changes include companion personality work.

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

The viewport is designed at 1920Ã—1080 with a 1600Ã—900 default window. Runtime room
art uses raw PNG loading; UI resources still need Godot import. LFS pointers are
not usable image files, so finish the LFS download before diagnosing missing art.

## Play loop

1. Start a New Loop with an unlocked architect and optional unlocked companion.
   Read the introduction, press Continue, and recover the starter from BRINE.
2. Draft and rotate blueprints, pay construction costs and connect matching doors.
3. Supply power, food, oxygen and other room inputs; inspect shortages and reserves.
4. Discover functioning room links and maintain three consecutive functioning
   cycles to stabilize patterns and unlock rewards. Hidden recipes stay hidden.
5. Recover architects and companions, harvest finite sites and expand sustainably.
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
executable does not prove its validation fixture ran. The September 9 maintenance pass covers 18 regression suites and native UI checks;
see its [scope and performance limits](docs/MAINTENANCE_2026-09-09.md). Remaining
acceptance includes sustained multi-crew traffic, companion animation/pacing,
dense-station performance and longer human playtests under normal resource costs.

## Repository contents

Game code, runtime assets, source provenance, tests, skills and documentation are
versioned, including selected in-game screenshots under `docs/screenshots/`.
Raster art uses Git LFS. `.godot/`, local backups and `output/` evidence,
review captures, downloaded templates and built executables remain local. Historical
documents may link to those local evidence paths; they are not hosted downloads.

Do not blindly stage generated capture trees. Export presets may refer to local
validation templates under `output/`; install/configure those before rebuilding
validation executables. No release binaries or player saves are included here.

## ðŸ“„ Licence

Source-available, with all rights reserved. See [NOTICE.md](NOTICE.md) for rights
and reuse terms. Third-party components retain their own licences.

## Build a Windows release

Use `powershell -ExecutionPolicy Bypass -File tools/export_release.ps1` after imports
and LFS downloads finish. The helper regenerates selected asset dependencies and
build identity and checks export errors. See [release verification](docs/RELEASE_ASSET_CONTRACT.md)
for actual executable, packaged asset and visual acceptance checks.
