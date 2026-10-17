# Project handoff

Updated: October 15, 2026 · Project: BrineSpace · Task: placement frame pacing

## Objective and acceptance

Investigate the previous128.026-ms placement frame, reduce repeatable work without
changing appearance or crew behavior, and compare the same release workload.
Admit the small navigation reduction for its consistent local CPU saving.
The original outlier's additional slowdown and smooth pacing remain unresolved.

## Accepted decisions and constraints

No deferred visible changes, actor movement changes, new textures or graph sharing.
Keep exact point IDs, weights, ordered edges, paths and prefix bookkeeping.
Use isolated APPDATA, copied owner layouts, real-profile fingerprints, silent
input-disabled native1920x1080 secondary windows and serial GPU/CPU validation.
Private room LOD remains private. No export, commit or publication requested.

## Current state

- `scripts/bill_npc.gd`: during synchronous graph assembly, an already connected
  reciprocal seam between two authored cells reuses its earlier validation.
  The original connection calls and boundary records remain in their order.
  Within the generated +/-176 lattice, the existing grown blocker sweep also
  proves endpoint clearance, avoiding repeated `can_stand` blocker scans.
  Outside-lattice direct calls retain the original endpoint checks. Staged,
  corridor/legacy, sampled and general route paths retain their fallback.
- `tests/test_navigation_boundary_reuse.gd` + UID and `tests/index.json`: old-helper
  oracle, half-open blockers, all directions, negative coordinates, asymmetric
  sockets, locks, exact graph/route order, placement/removal and layout revisions.
- Driver/evidence: `output/placement-pacing-20261015/` and
  `C:/bs-placement-20261015/`. Final series is **compare2**, not compare1/series.

Installed Bill source SHA256:
`5148c44a50ce08b1196e87ace9c4bd073f6bfd27078fca4ab03a20d8644a4eb3`.
It matches the final measured private candidate byte for byte. Both lanes include
the previous accepted Grid/companion/water changes and the same private LOD.
The physical frozen release source supplies Bill; loaded source hashes verify
the actual overlay program before measurement. Delivery remains unchanged at
`C:/bs-release-wall-env-20261014/windows/BrineSpace.exe`.
Reference overlay SHA256:
`cb28d0291936e69903eda3fc93fa5ec470d88cac430b1b142d391fa94b7d7803`;
candidate overlay SHA256:
`feaf4d33b9d55a5a1c84ef7de011658ffec53a272e18b8a7d15cf50edd740530`.

## Verification

The historical128-ms event is placement frame30, with no drone upload in its
sampled/current frame. The other seven historical placement frames take76–83 ms.
Thus there is a repeatable placement cost even without that outlier. A new
instrumented release run reproduces76.529 ms: action7.915 ms, simulation22.039 ms,
and about34 ms drawing. Navigation rebuild boundary work totals6.951 ms across
crew/companions, geometry4.348 ms, points/links5.707 ms and prefix work1.551 ms.
No cold local template is generated on that frame. These nested scopes are not
additive whole-frame or GPU timings. Free benchmark placement does not refresh
the whole UI; the recorded action is different from paid construction completion.
No additional delayed placement spike occurs in its following five sampled frames.

The small patch removes duplicate boundary validation. The first intentional RED
has two expected failures. Expanded direct-call tests expose the outside-lattice
case (four failures), then pass after its guard is added. Six normal maintained
regressions pass in `output/test-runs/20261015-004155-headless/`: boundary reuse,
navigation prefix, room ownership, segment parity, rebuild staggering and
companion topology. New test: **24,054 checks,46,840 ordered graph records and447
paths**, zero failures. Other fixtures add110,180 graph records/984 paths and
153,824 segment comparisons. Logs are clean. Independent final source review
finds no remaining actionable issue; no independent runtime review claimed.

Final actual debug=false release comparison: **6,720 measured frames**, seven
actions at1x/4x, both run orders. All28 phase-end gameplay/camera pairs match.
All loaded-source/overlay identity checks pass. The0.5-second process guard
detects no foreign Godot worker or duplicate game; it does not measure all OS load.

| Placement frame30 | Reference | Candidate | Crew CPU saved |
|---|---:|---:|---:|
| Forward,1x |74.169 ms|73.572 ms|2.595 ms|
| Forward,4x |76.611 ms|76.050 ms|2.800 ms|
| Reverse,1x |80.081 ms|70.761 ms|4.330 ms|
| Reverse,4x |76.880 ms|74.539 ms|3.086 ms|

Demolition crew CPU also saves2.235–3.626 ms across four events. Drawing remains
about30–36 ms on these structural-change frames. The patch does not reduce that
work, so the whole-frame gain is smaller and variable.

Whole-workload mean23.834->22.402 ms forward and22.337->22.312 ms reverse;
p95 improves7/14 and5/14 phases. >50-ms frames25->14 and12->13. Max115.209->81.234
and81.120->77.984 ms. The115-ms reference event is4x idle with a144,506,880-byte
drone upload, not placement. **0/28 candidate60 FPS phase gates pass.** Do not
attribute every removed outlier or the forward mean difference to this patch.
It establishes local CPU improvement, not general pacing or60 FPS acceptance.
Texture peaks remain identical2784.653 MiB; no retained cache/allocation is added.
End-of-run native screenshots were visually reviewed, but dynamic pixels differ;
they are not exact-image acceptance. Rendering code/art are unchanged, with graph,
route and matched-state checks guarding the movement behavior this patch touches.

All19 completed profile guards preserve2,948 owner files. Exploratory exclusions:
one isolated extraction attempt timed out; a first headless test exits its profile
guard before workload and is excluded; a fixture missing its Grid owner is fixed
before the intentional RED. A helper import accidentally launches an unrelated
diagnostic workload; that series and its later interrupted/contaminated compare1
run are excluded entirely. The corrected compare2 series runs serially with the
process guard clean. No task-owned QA process remains. No extra release validation
is inherited by the unchanged Windows executable.

## Next action

This investigation and small source optimization are complete. Next substantial
target is the broad retained floor/content redraw after a structural change;
reduce its invalidation scope while preserving compositing order and lighting.
The extra slowdown in the original128-ms frame has no proven separate cause.
Frame pacing, full-current PC/Mac release, endurance and60 FPS acceptance remain open.
