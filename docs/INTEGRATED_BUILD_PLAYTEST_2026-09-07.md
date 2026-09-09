# Integrated Windows build and playtest — September 7, 2026

**Result:** 21 automated acceptance runs passed on one frozen Windows debug
package, followed by a clean normal-title-launch smoke check. No gameplay costs,
failure conditions, discovery rules, movement tolerances or balance values changed.
This completes the combined-build and bounded packaged-test step of the September 6
handoff. Human pacing, continuous animation approval and broader hardware testing
remain separate.

## Playable build

Launch `output/integrated-acceptance-20260907-v1/build/BrineSpace.exe` and keep
`BrineSpace.pck` alongside it. Normal launch opens the title screen and uses the
normal BrineSpace save location. Test launches used fresh per-run APPDATA and
LOCALAPPDATA directories; the embedded launcher checked the actual Godot user-data
path before starting each fixture.

- Engine: Godot 4.6.1 stable, Windows x86-64 debug template.
- Renderer tested: OpenGL Compatibility, NVIDIA GeForce RTX 4070 Ti.
- Source baseline: `28e1dd86`, plus the working fixes below.
- PCK: 3,422,266,462 bytes, approximately 3.42 GB. This validation package retains
  source-art libraries and fixtures; it is not a trimmed release.
- PCK SHA256: `8a578c1afc4f5604fb2059b60b35c32c7fea9db4093722ed3b37ebbc504c16f7`.
- EXE SHA256: `8515cd8041a906bdf82a3c9926125e20f642a1062cb2a45a962f3a43dffa41ed`.

`package.json` and `acceptance-summary.json` beside the build record identity and
results. `frozen-export-sources.json` records the actual exported source snapshot;
`source-checkpoint.json`, amendment records and fixture-bridge records preserve its
relationship to the checkout. Runtime tests ran outside the source snapshot.
The final complete hashes matched after the suite.
Untracked `assets/full-wall-props-v1`, `v2` and `v3` folders appeared in the shared
checkout after the snapshot was taken. They were left untouched and are not part
of this tested package; subsequent art work does not inherit this acceptance.

## Defects found and fixed

1. **Missing decoration art in exports.** The raw PNG exporter covered rooms,
   characters, environments and drones, but omitted the new floor/wall decoration
   libraries. A packaged New Loop logged empty-image and null-texture errors even
   though its UI assertions passed. The exporter now covers the entire `assets`
   tree. The final package passed all 40 room render checks without engine errors.
2. **Fresh-checkout icon UID.** `project.godot` depended on a local image-import UID.
   It now references the same tracked `space texture.jpg` directly.
3. **Old animation-study resource paths.** The BRINE study scene pointed at its
   former standalone project root. Its six dependencies now resolve beneath
   `brinecore-animation`; its README matches that layout.
4. **Stale title test.** The test now exercises architect selection/confirmation
   and asserts an open expedition without the retired doctrine screen/deadlines.
5. **Incomplete traffic evidence.** The station fixture now streams all three
   crew members' positions and activity each movement sample, including failed runs.

The acceptance builder materializes tracked LFS sources in an isolated snapshot,
rejects LFS pointers, reconciles staged validation-card consumers to the current
decoration manifest, and records hashes. Historical art-selection manifests in
the checkout were not rewritten as new visual approvals.

## Final-package coverage

| Area | Evidence |
|---|---|
| Title and menus | Native title, keyboard New Loop, architect confirmation, Codex/discovery concealment, Settings and display recovery pass. Separate normal launch exits cleanly after 180 frames. |
| Architects and saves | All three starter selections, exact starting supplies, cryo recovery/unlocks, pause, disk Save/Continue and legacy-save checks pass. |
| Rooms | 40 identities; 320 rotation/power-state renders, 37 shared-edge renders and corridor variants. Current decoration-card hashes checked before export. |
| Furnishing dependencies | 27 composition profiles and all 37 furnished-view host checks pass before export. |
| Airlock | All three architects, four rotations, 1,039 travel samples; helmet fitting/return, ten interlock phases, power interruption, pause and disk saves pass. 277 PNG captures retained. |
| Drones/resources | Fleet, paid construction jobs, charging, finite stock/cargo, depletion, pause and save regressions pass. |
| Station operations | Queue, discovery watch, draft support and navigation checks pass. |
| Crew continuation | Automatic yielding and mid-yield disk restoration pass; both crew reach their original destinations in 169 samples. |
| Two-person regression | Headless movement/geometry/save checks pass; minimum separation 20.36. See the native capture limitation below. |
| Environment | 93 exact PNGs, 22 renderer caches, 66 runtime textures, 11 habitats; native station captures at 1280, 1600 and 2560 widths. |
| Paid openings | Four five-minute scenarios, mining/salvage with one/two generators; all survive with paid construction and failures enabled. Blueprints are controlled by the fixture. |

Final-package screenshots were inspected for the airlock with equipped Bill,
the station/environment at 1600×900, Life Support, Battery Array and Medical Office
powered/unpowered. Rendering completeness is not blanket owner approval of every
composition or continuous animation join.
`visual-inspection.json` binds these six inspected images to their PNG hashes and
the final PCK hash.

## Frozen three-crew traffic evidence

Bill's destinations are scheduled by the fixture; production navigation,
movement, avoidance and the other crew's decisions remain active. These are
48 room **instances**, not 48 distinct room types. All three crew were established
through the fixture's production recovery/thaw setup.

| Run | Bill / Veld / Branforth seeds | Arrivals | Door transitions | Movement samples | Minimum peer separation |
|---|---|---:|---:|---:|---:|
| Repeat A | 77321 / 77322 / 77323 | 48 | 135 | 10,473 | 20.00698 |
| Repeat B | 77321 / 77322 / 77323 | 48 | 135 | 10,473 | 20.00698 |
| Varied | 88432 / 88433 / 88434 | 48 | 135 | 10,433 | 20.06030 |

The two whole-crew traces match byte-for-byte:
`b8ebd6eddda5541846fb63f617546a985ea328f047b5e12824223dc1e5f06a1c`.
Maximum observed movement between successive samples was below 4.601 world units
for each actor; peer separation stayed above 19.99. Bill's traveled segments and
reciprocal door transitions also pass the fixture's registered-geometry checks.
This establishes reproducibility for the repeated seed and success for one varied
seed, not general congestion reliability across arbitrary stations.

## Remaining gameplay finding

Charging power still strongly constrains the controlled opening:

| Opening | Generators | Seconds waiting for power, of 300 | Metal delivered | Survived |
|---|---:|---:|---:|---|
| Mining | 1 | 242.0 | 8 | Yes |
| Mining | 2 | 0.0 | 34 | Yes |
| Salvage | 1 | 250.0 | 4 | Yes |
| Salvage | 2 | 3.3 | 17 | Yes |

These measured scenarios support a focused human playtest of opening power
readability and recovery, not a universal generator requirement or an automatic
balance change. Normal random drafts, player discovery and enjoyment were not
simulated by these controlled-blueprint tests.

## Preserved failures and limits

- Rejected imports/exports and their logs remain under the acceptance output:
  local-only icon UID, obsolete study paths and missing raw decoration PNGs.
- Windows export templates ignore the editor's `--script` option. Acceptance
  fixtures use an embedded Node launcher with SceneTree access/lifecycle adapters.
  The `_initialize` adapter omission was corrected before the final package.
- The legacy crew fixture's native capture path writes into `res://character`,
  which is read-only in a PCK. Its failed native output is preserved in
  `rejected-crew-native-capture`. Its supported headless mode retains movement and
  save assertions; the three separate native station tours provide full-crew
  trajectory/capture evidence. That legacy fixture's native capture writer was
  not repaired in the final package.
- A printed fixture PASS alone was never sufficient: final acceptance also
  requires exit 0, the expected completion marker and no engine/script errors.
  Existing image-loader warnings remain, while actual packaged image loading
  passed the bounded checks.
- Full airlock chamber transit, exterior travel and safe return remain unfinished.
  Swim/helmet transition artwork remains provisional.
- Human expeditions, 101-room performance, gamepad/OS scaling/multi-monitor tests
  and release-size optimization remain open. No release or publication occurred.

## Reproduce

Use a fresh output directory for a new package. Run each test into a fresh label;
the helper refuses to overwrite evidence or rebuild a frozen accepted package.

```powershell
python tools/build_integrated_acceptance.py prepare output/integrated-next --godot C:/Users/Alex/Desktop/Projects/Godot_v4.6.1-stable_win64.exe
python tools/build_integrated_acceptance.py build output/integrated-next --godot C:/Users/Alex/Desktop/Projects/Godot_v4.6.1-stable_win64.exe
python tools/build_integrated_acceptance.py test output/integrated-next --only title
python tools/build_integrated_acceptance.py test output/integrated-next --only tour --label tour-repeat-a --seed 77321
python tools/build_integrated_acceptance.py test output/integrated-next --only tour --label tour-repeat-b --seed 77321
python tools/build_integrated_acceptance.py test output/integrated-next --only tour --label tour-varied --seed 88432
```

Run the other fixture names listed by `--help`, then use `summarize` to require
the complete 21-run set, equal repeated whole-crew traces, peer-motion limits and
matching final package hashes. Fixtures use the exact exported executable.

Next: play a short normal paid expedition from this build, focusing on charging
feedback and recovery choices; then implement the airlock-to-water-to-airlock loop
as a separate gameplay change. Avoid restarting another room-generation batch.
