# Anomaly Lab review

Updated September 21, 2026. Broad polish goal remains active.

## Objective and constraints
Review current bought furnishing and animation without changing protected owner
rooms or the shared asset library. No production edits in this investigation.

## Latest acceptance checkpoint
Maintained regression extended: tests/test_powered_display_retention.gd now covers
Radio, Holo and Anomaly, with independent source-aperture motion checks for all three
Anomaly effects. Native run passes with zero failures (maintained-retention.log).
It reads shipped defaults, never player overrides; the reconciled layout is exercised.
All three rooms run four quarters/on-off-on with identical queues, redraw checks and
exact retained/direct comparisons. Existing test index and paired UID retained.

The effects and reconciled layout are installed; earlier staged/rejected sections
below preserve the investigation history. Native actual-station pause check now
passes in all four quarters (`live-pause/report.json`): operating samples at .2/1.0
seconds differ, then `_set_paused(true,false)` plus a .5-second `_process` call leaves
the clock and full room crop identical. Independent crops confirm orb, kiosk and tank
screen motion separately in all four quarters (`independent-regions.json`). Native
q0 operating crop inspected at gameplay scale. Isolated saves, synthetic funding and
forced power were used; this is rendering/pause evidence, not economy or expedition
acceptance. No engine errors. Owner aesthetic acceptance and new packaged verification
remain open; current 867eac6b1b17b4fc builds predate this room pass.

## Evidence
`output/anomaly-room-review-2026-09-21/current/`: all four native views inspected;
640 walking samples, zero route failures, zero visual overlaps. Seven bought props
persist in all quarters. Bench/stool and left instruments form recognizable groups.
The amber canister (`library/tileset-f22-235`) remains at (60,102) in q3 while the
containment tanks (`library/tileset-mb-45b`) move left; it loses its adjacent host.

Native `operation-anomaly_lab.gd` compares five states per quarter. All four fail
both visible powered-state change and animated-state change checks (eight failures).
Offline and held-clock checks pass. The entire rendered room is identical across
these powered/time states. This is a measured absence of operating feedback, not a
route failure. Current effective props omit the legacy anomaly platform/diagnostics
whose source-specific effects remain in the old renderer.

Relevant bought registrations are frozen in `source-registrations.json`. All logs
and captures preserved. No new generation, card bake, layout write or release change.

## Next action

## Staged screen-layer prototype
`diagnostic-study.gd` is an output-only subclass, not installed production code.
The kiosk screen (source250,614,31,22) becomes dark offline with a restrained live
trace; the tank screen (375,64,18,10) becomes dark offline with three level bars.
Raw source atlases and housing pixels remain untouched. The prototype explicitly
identifies room_id and reuses the production floor profile: a subclass outside the
catalog otherwise selects legacy furniture/floor and can produce misleading passes.
Final native operating/offline/held-clock checks pass in four quarters. Independent
decoded-pixel comparison verifies both screens animate in every quarter, and all
pixels outside aperture masks (2-3px raster tolerance) remain identical to baseline
offline and across powered/time comparisons. Evidence: screen-layer-verification.json.
Native q0 reviewed with the actual dark floor. Earlier diagnostic-only pixel-bound
report is superseded by this two-screen verification. Prototype tests are direct
rendering, not retained-cache, live station pause, or packaged verification.

## Next action (current)
Integration attempt rejected: direct and retained general state checks passed, but
all20 whole-image comparisons against the reviewed prototype differed around the
screens. General motion checks were satisfied by the orb and did not certify the
screen layers. Adding explicit library base drawing did not resolve parity. Saved
attempt: integration-candidate.gd.txt; original production renderer restored from
renderer-before.gd.txt. Thus no production effects are installed. The initial
retention fixture also used defaults missing the saved bought props; saved-layout
retention itself passed, but cannot override the failed visual parity gate.
Next inspect effective props and draw ordering in the full production render path,
assert each screen independently there, then repeat integration/parity. No layout,
source, registry, card or release changes from this attempt.

### Successful integration follow-up
Layout closeout: merged the four effective saved Anomaly keys into defaults and
saved layouts with guards against concurrent target changes. Every other key
preserved. Moved q3 amber prop beside the left tanks to (-174,108); no scaling or
shared source changes. Candidate, installed defaults and installed saved native
reviews each pass four views/640walking samples. Eight saved/default comparisons
match the candidate exactly (layout-parity.json). Refreshed and visually reviewed
assets/room-cards-v2/anomaly_lab.png; LFS filter verified. The card deliberately
renders offline, so the new hologram is absent and screens dark.
Actual station pause remains open; current export packages predate this room pass.

The actual cause was confirmed by a temporary per-prop probe: bought effect props
carry full_wall=true, so the bank-ownership branch returned before the screen
composites. The reviewed subclass added overlays after that return. Production now
excludes only EFFECT_PROPS from that early return and draws their bought base before
the screen layers. The orb already had its dedicated early branch. Probe prints
removed; trace-installed.log preserves the diagnosis.

The corrected room renderer is installed. All20 native powered/time-state images
match the reviewed prototype exactly (installed-parity.json). Saved-layout retained
on/off/on checks pass all12 direct comparisons, with36active redraws per12frames and
zero offline. No shared atlas/registry/layout/card changes. Actual station pause,
saved/default layout reconciliation, q3 amber placement and card refresh remain.
The prior rejection above records the failed attempt; it is superseded by this fix.

### Prototype history
The staged prototype now separates the globe's upper source region (386,586,45,42)
from the lower stand (386,628,45,44), with a restrained emitter rim. Offline globe
is absent; operating globe floats by 0.1-1.5 source pixels. No atlas pixels changed.
Four-quarter independent orb comparisons verify visible power/time differences,
stable lower stand, stable offline/held clock (`orb-layer-verification.json`). Native
on/off q0 reviewed. An initial temporary painter transform reset misplaced the orb;
the corrected prototype constructs its rim in room coordinates without resetting
the caller's transform. Whole-room animation checks alone did not catch that error.

Integrate only after checking full mask containment, source registration through
retained rendering and live station pause. Current captures supersede earlier
screen-only captures; earlier screen-only verification remains dated evidence.
The tank fluid is intentionally unchanged by the screen study; do not describe it
as newly animated or certified offline. Resolve the amber object's purpose and q3
placement, then integrate only dedicated room effects and exercise retention/pause.

## Original repair brief
Inspect source pixels for the orb projector (`cyb-123`), diagnostic cabinet (`hss-53`)
and tanks (`mb-45b`). Separate physical housing from meaningful powered output using
dedicated room registrations/layers so shared assets and other rooms stay intact.
Do not simply pulse the entire sprite. Preserve geometry and quiet offline surfaces;
test changed pixels within intended apertures, retained rendering and actual pause.
Keep the amber canister adjacent to its tank group in q3 or remove it if it adds no
readable function. Then review all quarters/live scale and refresh this room's card.
