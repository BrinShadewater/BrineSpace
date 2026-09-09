# BrineSpace performance and regression pass — September 8, 2026

## Scope and changes
This pass profiles 50/100-room running stations and exercises gameplay, saves, navigation, settings, drones, crew, loading and the layout studio. Existing concurrent art, audio, Observation Room and gameplay changes are retained. No commits, pushes, balance changes or architecture refactor.

- Room layout application skips unchanged resolved layouts and prop state instead of rebuilding library/copy furniture on each room configuration. Reset restores native furniture previously removed through authoring without recreating the room. Invalid flip arrays safely use normal orientation.
- Saved/authored layout changes invalidate retained room surfaces and door/light rendering. Raised-wall settings also participate in the light cache key. Closing the studio redraws the covered station.
- Layout geometry revisions invalidate crew topology and cached room blockers. Hidden props are excluded from collision snapshots. Lighting-only edits refresh visuals without restarting crew navigation.
- Door animation validation checks the specific adjacent pair and reciprocal connectivity directly rather than enumerating all four neighbors for each pair.
- Navigation regression expectations now preserve the accepted BRINE-centered Continue behavior. Discovery expectations include the accepted Observation Room. Test teardown drains music playback before shutdown; headless navigation skips framebuffer capture.

## Measurements
Native Godot 4.6.1, 1600×900, VSync disabled; same 50/100-room fixture, 30 warmup frames and 90 measured frames per scenario. Each sample explicitly advances simulation and forces drawing. These are local fixture comparisons, not general hardware FPS guarantees. No unrelated heavy fixtures were running during the before/after samples.

| Scenario | Before mean | After mean | Reduction |
|---|---:|---:|---:|
| 50 rooms, fit station | 50.21 ms | 46.32 ms | 7.8% |
| 50 rooms, close view | 19.94 ms | 18.41 ms | 7.7% |
| 100 rooms, fit station | 94.92 ms | 86.98 ms | 8.4% |
| 100 rooms, close view | 24.14 ms | 22.57 ms | 6.5% |

Before/after JSON and native screenshots: `output/game-pass/baseline/` and `output/game-pass/after/`. Both profiles completed with zero failures. Screenshots of the final close and overview scenes were inspected. The fixture also exercises construction, menu, zoom, Save and Continue. After-change save CPU time was 3.98 ms; 100-room restore was 380.71 ms, with its first frame 442.73 ms.

## Verification
19 final source fixtures pass with no ERROR/SCRIPT ERROR lines. Consolidated results: `output/game-pass/verified-results.json`; this points to the final log for each test, superseding earlier failed attempts.

Coverage: architect selection, display/menu recovery and paid construction checkpoint, discovery, disk save/restore, station navigation, drone fleet/jobs/battery/finite harvest/lifecycle, studio regression/workflow/performance guards, live layout refresh, station systems, Observation Room, crew room activity, loading transition and paid mining opening. The paid opening runs two five-minute simulations with one/two generators, normal costs and failures enabled, controlled available blueprints. Both survived. The lighting mesh reference comparison also passes.

Initial failures were stale camera/discovery expectations, display testing under a headless window, and fixture audio teardown. An attempted editor count change was reverted: the game has 44 identities but the studio catalog currently has 43 entries. New live-layout fixture first selected the core, which does not use the same authoring path; it now checks Research Lab geometry. These fixture corrections did not alter gameplay rules.

## Package
Frozen Windows debug package and exported checks: `output/game-polish-playtest-20260908/`. Five exported workflows pass with no ERROR lines: editor workflow, live layout/collision refresh, menu/settings/save recovery with paid construction, paid mining opening and paid salvage opening. Both paid variants run one/two-generator five-minute simulations. The normal title startup succeeds (exit 0), but forced `--quit-after` shutdown reports two audio resources still in use; this clean-shutdown check remains failed and is not counted among the five passes. Package hashes were rechecked unchanged after testing. See `checks.json`, `package.json`, `source-manifest.json` and `build/README.txt` for exact evidence. The normal title entry remains; test adapters and dispatch exist only in the frozen export snapshot. Previous accepted packages remain untouched. Concurrent checkout edits after the snapshot include a Radio Lab view substitution and crew completed-activity tracking; these later edits are not part of this package acceptance.

## Remaining limits and next priority
The 100-room overview still costs about 87 ms in this forced-draw fixture; this pass does not achieve a 60 FPS large-station overview. Fit Station can cause a first-frame rebuild hitch (~360 ms measured); restore also has a bounded hitch. The next measured optimization target is retained/batched distant-room floor and prop geometry, with pixel parity checks. This pass deliberately preserves artwork and detail rather than introducing unreviewed distance-based visual loss. Long-duration human playtesting and hardware coverage remain separate. Observation Room is playable and verified but is not yet in the 43-entry layout studio catalog.
