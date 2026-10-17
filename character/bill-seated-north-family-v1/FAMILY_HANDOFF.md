# Current reading selection milestone — September 30, 2026

The selected north family now includes sitting, breathing, reading and tablet
entry/exit:12 gear states/72 refs. Normal loader/registry paths stay the same.
New inputs are `bill-reading-north-v1` and `bill-reading-entry-north-v1`.
`scripts/bill_npc.gd` and `scripts/grid_canvas.gd` now follow north/south direction
for tablet transition keys and saved first-slot reading-pose cache. Fixed master
plane and matte/native helmet source authority are retained. No lounge activity
choice or room artwork changed.

92 family checks pass. North normal-loader fixture passes559 checks in45.64sec;
South actual-service regression passes559 in42.80sec. Both include28 partial sit/
entry reversals,12 arbitrary reading-phase exits,10 actual disk restores and64
captures. Fresh north chair captures reviewed;all2,914 real non-logfiles unchanged.
North fixture uses the actual lounge route and sitting chooser, then explicitly
scripts reading at that seat. Its reading stage/contact/renderer/restore proof
does not establish autonomous reading. South retains its actual sofa service.
Test: `tests/test_bill_seated_north_reading_selected.gd`; runner:
`tools/run_bill_seated_north_reading_selected_validation.py`. Preview: reading.html.
Current source/evidence binding: selected-reading-evidence.json.

Full Bill goal remains active. Next: east/west seated and reading sources, then
remaining life/rest actions and whole-world/final consistency polish. Broader
furniture and activity-choice coverage remain separate. Earlier milestone below
is preserved with its original scope and counts.

---

# Project handoff

Updated: September 30, 2026 · BrineSpace · Bill north sitting family

## Objective and acceptance
Complete the full master-consistent Bill animation set, then cross-reference
and polish it. This milestone installs north sit-down, seated breathing and
sit-rise in both gear states. Owner visual acceptance remains separate.

## Accepted decisions and constraints
Matte master materials, frozen source rulers, native selected rear helmet,
exact currently selected standing and seated endpoint bytes. Retained .8-second
sit/rise and .96-second cosmetic breathing cycle. No resource or service changes.

## Current state
Six gear states/36 references use whole literal res paths. Selected by
`scripts/grid_canvas.gd` and `character/ACTIVE_ASSETS.json`; the normal loader
rebuilds Bill's retained cosmetic-loop arrays after loading the new family.
Independent source packs retain historical staging metadata. This family is
the current selection authority. Sources and generation prompts are retained.

`scripts/bill_npc.gd` now reverses only the sitting already performed when
service is interrupted. It consults the loaded actor's forward/reversed frame
timeline to retain the displayed pose at half-open boundaries. Furniture
translation remains continuous. This helper is inherited by Veld/Branforth;
this milestone's native visual/service evidence is specifically Bill.

## Verification
48 family binding/registry/timing checks pass. Normal-loader native test passes
291 checks in40.91sec: exact36 loaded references and density/pivot, cosmetic
array bindings, eight endpoint joins, real lounge approach and stages,44 normal
screenshots,16 actual power-loss cases and two interrupted-rise screenshots.
All2,914 owner non-log files unchanged under scratch APPDATA. Fresh selected
furniture contact sheet visually reviewed. Scope: default north lounge chair,
both gear states. Other quarters/sofa, disk restores, inherited partial-sit
service cases and broader world journeys remain unproven.

Rejected intervals retained: zero-delta fixture never called update; corrected
positive-tick fixture reproduced the real reset-to-seated defect; a blanket
epsilon left four exact-boundary mismatches; actual loaded source-index matching
resolved them. One intermediate compile error was fixed with explicit String
typing. Candidate runtime check177passed before normal selection; earlier package
37 and isolated native83 reports retain their narrower scopes.

## Next action
Author remaining directional seated/reading and other life/rest actions, review
the sofa/other furniture and saved/interrupted stages, then complete the full-set
cross-animation consistency and polish. Full goal remains active.
