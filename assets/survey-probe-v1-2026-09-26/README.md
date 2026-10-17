# Survey Probe animation pack

Preview: http://127.0.0.1:8772/.

32-second mission: docked charge, prelaunch beacon, launch/acceleration, outbound
cruise, brake, four-second resource scan, curved turn, nose-first return, cradle
alignment, controlled reverse recovery, data received and charge. Four bay wall
orientations share the same continuous route transformed into their world axes.
Eight independently painted heading views keep the torpedo nose aligned to motion.

52 state/heading clips: idle, cruise, brake, scan and return in eight headings;
launch, dock and recharge in four cardinal headings. Each clip references a stable
rigid body and an optional separate effect layer (wake: 60 frames at 30 fps; topography: 60 frames at 15 fps). 960 PNG effect
frames and 16 atlases provide wakes and right-to-left topography sweeps. Counts describe reusable
state combinations, not 52 independently articulated hull animations. Lamp and
mission root movement are independent in the preview.

Frame canvas 512 square, pivot (256,256), .34 world units per library pixel. East/
west length is about 81 world units, with shorter projected north/south views.
Bay fitting preserves the existing study's probe/launcher ratio. This scale is a
review proposal; native Godot room, wall and crew clearance remain unverified.

Use Complete mission to review launch through recovery. Animation close-up exposes
individual states/directions and a native-size inset. Pause, quarter speed and the
timeline allow endpoint/contact review. The resource marker becomes surveyed at
scan completion and remains so through return and data receipt; Restart/new loop
resets the demonstration.

```
python assets/survey-probe-v1-2026-09-26/build.py
python assets/survey-probe-v1-2026-09-26/validate.py
node assets/survey-probe-v1-2026-09-26/test_mission.mjs
```

build.py registers preserved sources and exports poses/effects/manifest and review
board. mission.mjs is deterministic route/state sampling; test_mission.mjs checks
position continuity, nose alignment, scan stationarity, recovery and loop closure.
preview.mjs composites these with the bay and target. See review/validation.json,
review/mission-checks.log and PROVENANCE.md for evidence and exact prompts.

This delivers an animation preview and reusable assets. It does not install a
Survey Probe Bay, surveying rules, navigation or saved discoveries into the game.
Launcher hatch articulation and native wall occlusion remain integration work;
the preview masks the concealed tube passage between bay and ocean.

Topography revision: the four-second scan maps an area around the probe with a
right-to-left vertical sweep, progressively revealed contour lines and faint grid.
The overlay stays aligned to the environment in every heading and remains visible
after scanning. It is illustrative terrain, not sampled live-game elevation data.
Checks: review/topography-checks.json and review/topography-preview.png.

Hologram follow-up: a blue projection sheet, fine horizontal striations, luminous
core and soft halo now sweep across the area. The contour/grid reveal is retained;
the beam clears at completion while the map persists. Current evidence:
review/hologram-preview.png and review/hologram-checks.json.
