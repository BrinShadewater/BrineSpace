# Dr. Veld - Science Officer

Dr. Veld is now a second autonomous character alongside Major Bill. She uses the
same pressure-suit family, physical scale, room navigation and foot alignment,
with cobalt science markings, ivory chest panels, a silver-streaked bun and a
sampling kit. The original concept remains at `concept-01.png`.

## Animation pack

72 exported frames, each 92 x 92, with transparent backgrounds, foot pivot
(46, 86), 74-pixel standing height and a shared 64-colour palette.

| Animation | Directions | Frames per direction | Playback |
|---|---|---:|---|
| Idle | south, north, east, west | 6 | breathing loop |
| Walk | south, north, east, west | 6 | distance-driven loop |
| Interact | east | 6 | handheld scanner, one-shot |
| Kneel | east | 6 | lower for sample inspection |
| Repair | east | 6 | sample-inspection loop |
| Stand | east | 6 | reverse kneel, one-shot |

`repair` retains the shared NPC controller's state name; Veld examines a sample
instead of repairing machinery. There are no mirrored directions. All eleven
source rows were generated from her concept using the built-in image tool.
Standing reverses the generated kneel, and work/idle endpoints share frames to
reduce transition jumps. Running and diagonal animations are omitted because her
current NPC controller uses cardinal walking only.

Source rows were inspected and deterministically sliced, registered, downsampled,
background-keyed and palette-reduced. Small generated pose/detail variations
remain; these are not hand-cleaned pixel animations.

## Files

- `frames/`: all 72 individual PNG frames.
- `rotations/`: four neutral idle fallback sprites.
- `final/spritesheet.png`: six columns by twelve rows, manifest order.
- `final/*-strip.png`: individual animation strips.
- `final/manifest.json`: frame paths, exact timings, pivots and source hashes.
- `final/dr-veld.tres`: native Godot SpriteFrames resource.
- `qa/contact-sheet.png`: every exported frame.
- `qa/animation-preview.gif`: animation gallery.
- `qa/science-sequence.gif`: idle -> kneel -> inspect -> stand -> idle.
- `qa/previews/`: individual animation GIFs.
- `qa/validation.json`: geometry/alpha validation, zero errors or warnings.
- `qa/native/`: ignored native station captures, including both characters.
- `generated/`, `animation-prompts.json`, `generation-sources.json`: retained
  visual sources, exact prompts and generation provenance. Generation used the
  built-in image tool; no API-key CLI fallback was used.

## Gameplay integration

Veld has independent hunger, fatigue, exploration and science-work preferences.
She shares Bill's collision-aware pathfinding and cached room geometry, while
keeping her own position, destinations, needs, random generator and sprite clock.
Her decisions do not consume the station's random sequence. Science work favors
research, biological, xeno, anomaly, archive, nursery and hydroponics rooms.
Only reachable, functioning rooms satisfy service needs. Exploration includes
short handheld scanner readings.

Layered rooms sort both characters with props using their foot depth. Corridors
and legacy rendering also support Veld. Connected doors open for either crew
member based on proximity. Pause and game speed affect both NPCs. New runs reset
both, and the existing status area reports Veld's activity and needs.

This remains a visual NPC prototype: there is no resource consumption, research
reward, staffing bonus or population-count change. Both crew members now save their needs, exact positions, routes, current activities,
visit history, independent random state and animation playback clocks. Continue
remains paused and resumes on the saved action frame. Older checkpoints without
crew data still load and start fresh behavior loops.

Crew maintain a 20-unit separation between their foot collision areas. They
briefly yield, plan a detour around a colleague, or choose another destination
when a resting colleague blocks a goal. Detours use the same prop and wall
clearance checks; horizontal corridor passing favors the front lane. Corridor
rendering sorts both crew members by foot depth. This is local two-character
avoidance, not a population-scale crowd simulation. Work animations still face
east and use compatible prop approaches.


## Rebuild and verification

Run `python character/dr-veld-v1/build_pack.py` from the repository root.
Requires Pillow and NumPy; reuses the deterministic registration/palette helpers
in `character/major-bill-v2/build_pack.py`. Rebuilding uses local source images
only and never calls an image service.

- Sprite skill manifest validator: zero errors, zero warnings.
- `tests/test_dr_veld.gd`: asset loading, native SpriteFrames, timing, matching
  action endpoints, independent clocks/needs/RNG, safe movement, science choices,
  both characters moving, pause and independent door opening.
- `tests/playtest_dr_veld.gd`: native 1600 x 900 room captures of both characters,
  all four walking directions, scanner use and the sample-inspection sequence.
  The fixture uses isolated saves and display preferences.
- `tests/test_major_bill_animations.gd`: Bill's existing 17 animations / 102 frames
  still pass coverage, timing and transition checks.
- `tests/test_bill_npc.gd`: shared navigation regression coverage.
- `tests/test_crew_polish.gd`: head-on corridor passing without foot overlap,
  wall clearance, no teleporting, disk save/restore, exact action-frame recovery,
  malformed crew-data rejection, and compatibility with older checkpoints.
  Also runs natively to capture the passing sequence under `qa/native/crew-passing/`.
- `tests/test_run_save.gd`: existing checkpoint and title Continue regressions.

PNG assets inherit the repository Git LFS rules. GIFs use the local LFS rule.
No source art was overwritten, and no commit or export build was made.
