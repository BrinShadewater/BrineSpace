# Bill connected-source review

Updated: 2026-09-21. Workspace: Brine Space. Broad project goal remains open.

## Objective and decisions

Address the owner's disjointed feet report. The earlier18-pose experiment is set
aside: retaining its defective key poses is not an acceptance requirement. Recover
whole connected source poses before deciding whether further motion repair is needed.
No generation, Higgsfield, owner-room edits or live sprite replacement in this study.

## Current state

`output/bill-joint-review-2026-09-21/build_connected.py` stages24 east/west
bare/helmet PNGs from `base_frames(repair_walk=False)`, bypassing Bill's local leg
rig and mixed old-boot/new-limb composite. Complete lower bodies are pixel-identical
to the preserved source poses. Helmet placement uses each original pose's retained
registration rather than the local rig's later fixed-head/bob rule.

Two review manifests retain the installed900ms timing and stride so comparison
isolates the artwork. This is not a claim that the old source foot travel matches
that stride; anatomical contact and cycle review are still required.

## Verification

- 24 lower-body pixel comparisons pass; per-file SHA256 saved in connected/provenance.json.
- Native Godot4.7.2, installed CrewSpritePlayer:54 captured frames across both
  directions and equipment variants. No missing textures or logged engine errors.
- Native fixture explicitly sets1000x540 content size and scale1. Initial captures
  had project viewport scaling and were superseded after visual inspection.
- Bare/helmet key captures and original/current/cast comparison sheet inspected.
  Recovered poses show cleaner continuous ankle/boot contours. Whole-cycle motion,
  state transitions and autonomous station gameplay have not been accepted.
- `bare-native.gif` and `helmet-native.gif` use27 captures at30Hz per900ms cycle;
  GIF durations30/30/40ms preserve total cycle despite centisecond quantization.
  Each shows installed above/recovered below, at source and384-unit room scales.
  These are controlled native drawing studies, not station screenshots.

## Installed follow-up

Canonical `tools/rebuild_bill_art.py` now defaults to complete source poses, with
original per-pose helmet registration. Explicit repair_walk=True retains historical
rig reproduction only. `tools/build_bill_connected_walk.py` is the maintained
review exporter; the normal `repair_bill_walk.py` CLI delegates to it. The old
limb-candidate tool is labeled historical/rejected.

Full rebuild changed exactly24walk PNGs, with2239other art/metadata files unchanged;
all24 match the staged review byte-for-byte. Full validation passes2214frames,
780preserved sources and113source manifests. Three surface tests pass; installed
consumer passes11773checks. Head checking now uses the actual34-pixel source head
band rather than a fixed region that included moving shoulders. Complete lower
bodies are checked against preserved source pixels for both equipment states.

Paid station west capture:240samples/240images, all walking west, costs/failures
enabled; crop containment checked. Station context inspected. Evidence and logs
remain under output/bill-joint-review-2026-09-21. Existing exports predate this fix.

East follow-up completed240samples/captures:125east walk then115south walk, with
paid building and failures enabled. `installed-station.gif` pairs the first120
samples from each actual station run, before the turn; every second30Hz capture
is encoded60/70/70ms for4seconds. This remains controlled opening gameplay,
not owner acceptance or a complete expedition test.

`transitions-registered.png` uses each manifest's pivot. The first unregistered
sheet placed different canvas profiles at identical origins and is not valid
alignment evidence. Corrected sheet shows west work poses still differ in suit
proportions/shading from walk/idle; follow up separately. No claim of full action
consistency or a measured complete anatomical foot lock.

## Next action

Check the recovered original pose sequence's anatomical stance/crossing order and
idle/work transitions. Repair from connected whole limbs only where that review
shows a defect. Connected-source installation and focused checks are complete;
continue full gait/action consistency and owner review. Do not reinstall disjointed
geometry to satisfy old pixel invariants. Release packages remain unchanged.
