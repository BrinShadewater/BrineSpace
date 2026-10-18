# BrineSpace

A Godot 4.7 underwater station-restoration roguelite prototype. You play BRINE,
a damaged AI core rebuilding a silent station through blueprint drafting,
modular placement, interdependent production and discovered room synergies.

> "The station is quiet. That does not mean it is empty."

![A BrineSpace station on the sea floor: BRINE Core at the centre, rooms connected around it, the room inspector open and a draft hand of blueprints](docs/screenshots/station-gameplay-2026-09-16.png)

*Native Godot capture, September 16, 2026, from a scripted scene rather than a played
expedition. The station lights its own hull; the sea floor past the lamps is dark on purpose.*

Rooms use authored layouts with larger equipment and restrained clutter. Raised walls start enabled; change **Raised room walls** in settings to use low walls. See the [room layout direction](docs/LARGE_ASSET_LAYOUTS_2026-09-09.md).

### A larger station

![A large BrineSpace station viewed at Fit zoom, with many rooms across the ocean floor](docs/screenshots/large-station.png)

*Native large-station scene, September 16, 2026: 164 rooms placed by script with free
building on. A controlled layout with injected supplies, not a normal paid expedition
or a claim of finished large-station performance.*

### Starting screen

![BrineSpace starting screen with BRINE in her tank, New Loop, Settings, Codex and Meta Progression](docs/screenshots/starting-screen.png)

*The actual starting screen, captured from the layered animated title scene at the
design size and reduced for this page.*

## Restore a station beneath the ocean

For playtesting, **F7** toggles live performance statistics, **F8** opens the local
bug reporter, and **F9** opens Room Layout Studio. Manual bug reports include recent
frame timings and a separate live station snapshot. See the
[performance diagnostics guide](docs/PERFORMANCE_DIAGNOSTICS_2026-09-12.md) for limits.

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
adds a named crew member for the rest of the expedition. Spend Archived Data on
the Meta Progression page to bring recovered characters into future loops.

BrineSpace is designed to be thoughtful and watchable: an open-ended restoration
game with resource pressure, quiet machinery and an AI core with opinions. You can
pause to plan. The pressure comes from the station's needs, not rapid clicking.

## Current development — October 18, 2026

BrineSpace is a playable Godot 4.7 prototype, locally tested with 4.7.2.
Windows, Mac and iPad are being developed toward a shared release. Published
source branches and validation candidates are available for review; no downloadable
GitHub release is currently published. Large-station performance, iPad memory
headroom and longer expeditions remain under evaluation.

The default `main` branch retains the October 14 gameplay checkpoint, with this
repository overview refreshed on October 18. Later work is published separately:

- [Windows preservation](https://github.com/BrinShadewater/BrineSpace/tree/codex/windows-preservation-20261017)
  records the broader Windows source and art work.
- [Windows / Mac / iPad integration](https://github.com/BrinShadewater/BrineSpace/tree/codex/windows-mac-ipad-integration-20261017)
  reconciles the shared runtime for review. Read its
  [integration handoff](https://github.com/BrinShadewater/BrineSpace/blob/codex/windows-mac-ipad-integration-20261017/docs/WINDOWS_MAC_IPAD_INTEGRATION_HANDOFF_2026-10-17.md).
- [Native Apple validation](https://github.com/BrinShadewater/BrineSpace/tree/codex/mac-ipad-native-validation-2026-10-17)
  records Mac and physical iPad checks; [later iPad memory and placement work](https://github.com/BrinShadewater/BrineSpace/tree/codex/ipad-memory-placement-2026-10-17)
  remains a separate integration input.
- [F10 visual audition](https://github.com/BrinShadewater/BrineSpace/tree/codex/look-audition-20261018)
  adds an optional session-only tilt-shift and pixel-grid comparison to the shared
  review baseline. It starts off and does not change saved preferences. Read the
  [controls and validation notes](https://github.com/BrinShadewater/BrineSpace/blob/codex/look-audition-20261018/docs/LOOK_AUDITION_2026-10-18.md).

These branches have not been merged into `main`. Read the current-status file and
handoff on the branch you are using; their checks apply to their recorded revision
and platform. For the default branch, start with [current status](docs/CURRENT_STATUS.md)
and [development notes](docs/DEVELOPMENT_NOTES.md).

### Prototype systems

- **47 room identities** with matching doors, four rotations, operating effects
  and authored furniture layouts. Most furnished rooms favor three or four large
  assets; BRINE Core keeps its more elaborate arrangement.
- **Four architects:** Major Bill, Dr. Veld, Chief Engineer Branforth and Marsh.
  Recover them for the current loop; purchase their return with Archived Data.
  Marsh is an android powered by a
  rechargeable battery; his derelict charging chamber has its own recovery sequence.
- **Three optional companions:** River, Josh and Margot. Find and restore their
  derelicts, purchase their return for later loops, and watch their individual behaviors. River and Josh
  are robots; Margot is a cat you can approach and pet. Each answers a click with their own
  dialogue window: Josh talks, River chirps with a status-lamp translation, Margot is a cat.
- **Working station systems:** paid drone construction, mining and salvage, finite
  deposits and cargo delivery. Building is never blocked for want of power; it draws the
  reserve instead. At a quarter of capacity the lights and exterior lamps stutter, and when
  generation plus reserve cannot cover every running room the whole station blacks out for
  the cycle rather than shedding rooms one at a time.
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

Local Windows and Apple validation packages are described in the branch handoffs
above. They are dated test candidates; this repository does not currently offer
a published release download.

## Run locally

Install Git LFS and clone with Windows long-path support:

```sh
git lfs install
git -c core.longpaths=true clone https://github.com/BrinShadewater/BrineSpace.git
cd BrineSpace
git lfs pull
```

Use Godot 4.7 (tested locally with 4.7.2). Open `project.godot`, allow imports to
finish, and press **F5** to run the project through title, architect selection and
Continue. The configured main scene is `res://scenes/title_screen.tscn`;
gameplay is `res://scenes/main.tscn`.

The viewport is designed at 1920x1080 with a 1600x900 default window. Runtime room
art uses raw PNG loading; UI resources still need Godot import. LFS pointers are
not usable image files, so finish the LFS download before diagnosing missing art.

## Play loop

1. Start a New Loop with an unlocked architect and optional unlocked companion.
   Read the introduction, press Continue, and recover the starter from BRINE.
2. Draft and rotate blueprints, pay construction costs and connect matching doors.
3. Supply power, food, oxygen and other room inputs; inspect shortages and reserves.
4. Discover functioning room links and maintain three consecutive functioning
   cycles to stabilize patterns: later loops double their per-cycle bonus, award
   Archived Data, and halve the related blueprint cost. Buy blueprints, crew and
   companions on the Meta Progression page. Hidden recipes stay hidden.
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
executable does not prove its validation fixture ran. Run them with
`python tools/run_tests.py`, which takes `--subsystem <group>` from `tests/index.json`,
`--only <names>` and `--native` for the tests that need a real display. On September 16,
2026 the headless groups and the native lane pass: room-art 16, gameplay 48, crew 27,
layout-studio 4, flood-water 8 and native 66. The September 9 maintenance pass documents
the [scope and performance limits](docs/MAINTENANCE_2026-09-09.md) behind those checks. Remaining
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

## Licence

Source-available, with all rights reserved. See [NOTICE.md](NOTICE.md) for rights
and reuse terms. Third-party components retain their own licences.

## Build a Windows release

Use `powershell -ExecutionPolicy Bypass -File tools/export_release.ps1` after imports
and LFS downloads finish. The helper regenerates selected asset dependencies and
build identity and checks export errors. See [release verification](docs/RELEASE_ASSET_CONTRACT.md)
for actual executable, packaged asset and visual acceptance checks.
