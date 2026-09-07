# Room furnishing status

**Latest selection update:** the [decoration integration](../rooms/decoration-integration/README.md)
now selects new cards across all 40 identities. Earlier card-bound visual findings
and per-pack export selections below are historical until reconciled to those
hashes. See the [consolidated handoff](BRINESPACE_HANDOFF_2026-09-06.md) for the
current package/traffic acceptance gap and ordered next work.

Current inventory v7 contains **40** identities, all with decodable selected cards and furnishing-ledger entries. Pressure Control Chamber, Deepwater Listening Post and Emergency Isolation Vault now have dedicated local profiles and selected cards. The strict review board passes without incomplete-report mode. Full visual acceptance remains pending.

The scope remains every current RoomDatabase identity: the latest native inventory contains 40, including Diving Airlock, T Corridor and the three rare branch-control rooms. Initial furnishing and later detail passes are tracked in [the per-room ledger](ORGANIC_ROOM_ROLLOUT.json); neither stage establishes a natural-looking, finished room. Consult the ledger and selected runtime profiles rather than historical room counts or a fixed next-room list.

## Current work

Recent passes add distinct supported belongings: a crew drying rack, storage staging pallet, mining cutter stand and salvage recovery tray. Their selected cards, profile hashes and native evidence are recorded with each room. The Biodome now also has a propagation shelf with cuttings and tending supplies. Several earlier rooms still have widely separated machinery and need further composition work.

## Packaged evidence

[Windows catalog 40 v1](../output/room-rollout/windows-catalog40-v1/verification.json) is the current technical baseline: 40 source hashes, 80 source/card decodes, 68 component records and 36 profiles pass. The controlled tour reached 60 placed rooms across 162 transitions and 12,525 movement samples. All 40 focused captures decode at 1600 × 900. This includes the dedicated rare-room layouts and recent furnishing changes. Full visual acceptance is still pending; the smaller packages below are historical.

[Windows catalog 37 v2](../output/room-rollout/windows-catalog37-v2/verification.json) now covers all 37 identities: 74 source/card decodes, 61 additional component records and 33 profiles. Its controlled tour reached 56 placed rooms across 150 transitions and 11,502 movement samples. This includes the later office, construction and thermal compositions. It predates the retained-canvas replacement fix described below; visual acceptance remains pending.

The native airlock-to-T-Corridor replacement review caught furniture left visible from the previous occupant of the same cell. The renderer now releases retained contents when the replacement cannot own them. `output/new-room-composition-routes-v2` passes all four rotations of both rooms and the explicit canvas-release assertion; the T Corridor's normal-scale capture was inspected without the ghost furniture. This is source-runtime evidence, not a rebuilt package.

[Windows detail review v1](../output/room-rollout/windows-detail-review-v1/verification.json) passes 35 selected sources, 70 source/card PNG decodes, 58 component records and 32 composition profiles. The packaged current-controller tour visits all 53 placed rooms with 141 transitions and 10,815 movement samples. All 35 focused captures decode at 1600 by 900. This supersedes the earlier activity-review package for technical coverage; full visual acceptance remains pending.

Med Office now has a later, natively verified grouping pass for waiting seats, reference storage and examination furniture; it postdates this package. Construction Drone Bay also has a later assembly-trestle and service-group revision, with corrected fleet draw bounds. Both revisions need updated packaged coverage.

## Remaining acceptance

Review each selected room at normal station zoom, with neighbours and crew for scale. Check supported objects, department-specific character, purposeful service connections, clear working faces and all rotations. A readable new prop does not approve an otherwise sparse room. Keep per-room native checks, visual findings and packaged verification distinct.

## Workflow

Keep selected cards, source/component hashes and composition profiles synchronized. Run dependency closure and floor-hook inheritance audits before packaging. Use the depth review to inspect every furniture front as well as pixel ordering, and use current production movement for route evidence. The [station review](ROOM_COMPOSITION_STATION_REVIEW.md) preserves historical revisions and failures; it is not the current selection registry.


## Current review board

[Selected-card board](room-composition-review.html) is generated from the native inventory audit. It is a same-scale comparison of current card bytes, not fresh station renders. The audit detected two ledger omissions; both are now included. T Corridor also now has an export entry, and routing manifest cards match current selections. The prior 35-room package remains historical; the next full run must include the airlock manifest as well.

### Battery Array: staggered bank/service grouping
The selected battery-composition-v3 profile and battery_array-card-group-v4 move the second bank to the southeast, keep the breaker/distribution group west, and give the supported test cart a northeast working area. Smaller host-bound matting and endpoint-linked service cables replace the detached southeast accessory pair. No new raster source was needed. All 72 depth poses pass, including 24 usable fronts, and battery-group-routes-v4 passes all four rotations and returns. The normal-scale q0 station capture was inspected. This remains a composition revision, not finished visual acceptance: it still reads as separate quadrants and needs more hull-integrated working detail. It postdates the catalog37-v2 package.
The initial routes-v3 run reached the default mixed-station branch because a newline-sensitive insertion silently failed. Its failed result is retained; routes-v4 is the correctly identified focused fixture. Future scripted edits must assert that their exact target occurs once and verify the resulting branch before launch.


### Holographic Core grouping follow-up — 2026-09-06

Offset the supported calibration cart beside its machine, raise the opposite terminal, and connect equipment with perimeter service runs. Reject the first placement: front-access probes passed but the machine interrupted a side entrance. Final depth review has 60 poses and 20 accessible fronts; current-route tour passes all four rotations (`output/holo-group-depth-v2`, `output/holo-group-routes-v2`). This illustrates why local prop access cannot substitute for doorway movement. The selected card is group-v1/profile-v3; the prior 40-room packaged baseline predates this change. Further wall and surface dressing remains a visual task.


### Hull repair preparation surface — 2026-09-06

Shield Generator now has a low clamped panel cradle, supported sealant gun/rag tray and contained hose between monitoring and compound injection. A distinct low support height helps the room avoid a row of repeated electronics benches. Reject the diagonal-camera first source; the second source needed explicit checkerboard cleanup including its enclosed leg opening. Preserve both generation prompts and cleanup seed in panel-cradle-provenance-v2.json. Native card panel-v1 was inspected; 72 depth poses, 24 accessible fronts and all four current doorway rotations pass (`output/shield-panel-depth-v1`, `output/shield-panel-routes-v1`). Catalog40-v1 export predates this revision; package verification remains due.


### Radio listening workstation — 2026-09-06

Radio Lab operator-v1/profile-v3 places an existing operator chair at the listening console, staggers the lower machinery around the supported electronics bench, and adds perimeter signal services with a flush covered doorway crossing. Reuse furniture when its activity fits; avoid copying an entire room accessory set. Final native depth review: 72 poses, 24 accessible fronts, no ordering failures. Current east/west routes pass all four rotations (`output/radio-operator-depth-v1`, `output/radio-operator-routes-v1`). The strict 40-room review board was refreshed from inventory-v8; it includes Holographic Core group-v1 and Shield Generator panel-v1. These three revisions postdate the packaged baseline.


### Current 40-room packaged check — 2026-09-06

windows-catalog40-v2 includes Holo group-v1, Shield panel-v1 and Radio operator-v1. Exported Windows runtime passes 40 source/80 source-card decodes, 70 component records, 36 profiles, 60 arrivals, 162 transitions and 12,525 movement samples. All 40 focused PNGs decode at 1600×900. Shield station capture confirms the low cradle is present with clear central circulation; offline lighting limits fine detail. This is packaged integration evidence, not full furnishing approval. Verification: output/room-rollout/windows-catalog40-v2/verification.json.


### Furnishing completion requires a stopping rule — 2026-09-06

Crew Lounge activity-v3 has been visually reviewed in its card and the functioning catalog40-v2 station capture. Reading, dining, refreshment and games areas have distinct supported objects, secondary furniture and appropriate standing lights, rugs, plants and coats. The clear middle serves circulation. Accept this composition rather than continually adding clutter; record exact card hash and station evidence in the rollout ledger. Technical tests alone never establish this decision, and agent acceptance does not imply owner sign-off.


### Maintenance service connection — 2026-09-06

Maintenance services-v2/profile-v3 adds a diagnostic lead to the parts trolley with a covered central crossing. Keep this run in routes below decals; surface_routes would incorrectly draw it over its own cover (rejected card-services-v1). Native four-rotation route fixture passes; furniture geometry is unchanged. Package catalog40-v2 predates this floor-only revision.


### Nursery substrate preparation — 2026-09-06

Nursery substrate-v1 adds a generated low wheeled stand with supply bags below and measuring tools above. Preserve original RGBA and source provenance; alpha registration uses 11 polygons. Canonical placement alone was insufficient because nursery machinery has authored quarter-specific positions: initial q1/q3 access failed, corrected explicit stand centers pass 72 depth poses with 24 accessible fronts and all four current routes. Evidence: output/nursery-substrate-depth-v2 and output/nursery-substrate-routes-v1. This revision postdates catalog40-v2; visual acceptance and package refresh remain separate.


### Hash-bound visual findings — 2026-09-06

The review board now exposes visual findings and the decision for the selected card. If visual_review.card_sha256 differs, it shows a stale-review warning and suppresses the old decision. Positive/current, stale and escaped-text fixture checks pass. Biodome and Hydroponics station-scale reviews now identify concrete remaining work: Biodome needs a restrained wall care detail; Hydroponics needs a small supported harvest/supply area and wall detail. A readable irrigation system is not by itself complete furnishing.


### Botanical wall care charts — 2026-09-06

Biodome and Hydroponics care-v1 add code-drawn sealed clipboards with simple schedule marks, mounted to north hull segments only when the full 28-unit width fits. They are decorative notices, not interactive systems. Keep this small common fixture subordinate to department props. Both native four-rotation route tours pass; Biodome q3 station capture confirms the mounting and scale. Biodome furnishing now passes native visual review; new package check pending. Hydroponics still needs its supported harvest/supply area.


### Hydroponics harvest stand — 2026-09-06

Harvest-v1/profile-v3 adds a low produce-crate dolly with packing paper and a supported shears/tags tray beside nutrients. Image revisions rejected a backdrop and a clipped handle before source-v3 cleanup; exact prompts, revisions and reviewed gap seeds are in hydro-harvest-provenance-v3.json. Native card inspected; 72 depth poses/24 accessible fronts and four route rotations pass. Updated station-scale visual and package review remain.


### Shared-wall fitting visibility — 2026-09-06

A fitting drawn only inside draw_wall can disappear when the station owns the shared wall between connected rooms. Botanical charts now draw as room detail at their fixed hull mount, outside the 72-unit door bay, while the station retains shell ownership. Closed card previews did not reveal this. Add a connected-neighbor station capture to fitting review. Moving the mount alone did not resolve the handoff and placed it behind foliage; retain rejected v2/v3 cards as diagnostic evidence. Selected cards are care-v4/harvest-v4.


### Medical review follow-up — 2026-09-06

Medical Center services-v1/profile-v3 connects imaging to diagnostics with a perimeter service run and flush east crossing cover. Four native route rotations pass; furniture/collision unchanged. Medical Office grouping is coherent in card and unpowered station view, but powered visual acceptance remains explicitly unproven. Record lighting state with visual findings instead of treating every station capture as equivalent.
