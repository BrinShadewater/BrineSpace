from pathlib import Path
import json,hashlib
P=Path(__file__).resolve().parent;ROOT=P.parent.parent;OUT=ROOT/'output/bill-meal-entry-east-candidate-native-v1'
v=json.loads((P/'verification.json').read_text());n=json.loads((OUT/'validation.json').read_text())
assert v['passed'] and n['passed'] and not n['realProfileChanges']
assert '87 checks,0 failures' in (OUT/'native.log').read_text(encoding='utf-8')
handoff='''# Project handoff

Updated: September30,2026 · BrineSpace · Bill east bowl pickup/return candidates

## Objective and acceptance
Complete Bill's full master-consistent animation set,then cross-animation polish.
East bowl pickup/reversed return now join selected idle to new eating candidate.
Full meal family and normal service integration are still incomplete.

## Accepted decisions and constraints
Selected matte east idle owns appearance and standing density. Use exact whole
idle/eating-held donors at both ends,not independently regenerated endpoints.
Waist-height forward hand reach,one supported bowl/short spoon,two connected
arms/hands,upright body and planted feet. Helmet meals keep the installed reader.

## Current state
Primary built-in source exec-84ef5a85-15bb-4bdb-ad4b-79defd58a607 and exact prompt
saved in sources/pickup-v1.png/prompt-pickup.txt. Six448/447/449/444/444/444px figures.
Primary first empty reach was too abrupt; focused two-pose source
exec-bb8b1f90-8d45-499a-8d4e-97ea8a7c5c6b saved reach-v2.png/prompt-reach-v2.txt,
both844px figures. Use reach0 then primary1/2/3/4; reach1 duplicates full extension
and stays raw/unused. Primary0/5 are replaced by exact selected idle/held donors.
Fixed primary[.31,.332]/density1.0 and reach[.156,.17536]/density1.89 rulers,
selected neutral/hair/skin/burgundy grade and front-boot/sole registration.
Two bare states/14refs,seven slots each,580ms60/80/100/100/100/80/60; return is exact
reverse. Plane256/pivot128,224/H148/dry0. build/verify/registration/source hashes
and preview retained. Preview pickup/two eat loops/return totals3.08s,presentation
only. No normal loader/ACTIVE_ASSETS/actor/service clock changes.

## Verification
29package/87native checks PASS12.13s. Source/ruler/donor/frame bindings,five distinct
authored interiors,finite pacing/endpoint hold,dry action metadata,exact idle/held
joins and full-pose reverse verified. Native148/82 board visually reviewed with
master. Short reach now precedes full extension and supported bowl draw-in.
Interior headAxes[[129,77],[129,76],[132,75],[128,77],[131,77]]:2px crown range,
4px fore-aft head-axis range remains for source/family polish. Fine emblems and
interior prop/pose detail remain for final cross-animation comparison. Do not
equate exact endpoints with locked interior registration or actual counter contact.
Scratch APPDATA; all2,914owner non-log files unchanged. Candidate player/finite
joins only; normal meal behavior,counter contact,interruptions/restore unproved.

## Next action
Author matching east cup pickup/return with exact idle/drinking-held joins.
Assemble full east meal sequence and preserve original6s eat/3s drink clocks;
normally install,then prove actual counter/interruptions/disk restore.
Continue cardinal meals,generic rest/drydeath and full-set polish. Inspection
broader contact/hazard/equipped-drink-boundary audits remain open. Goal active.
No commit/export requested; preserve other actors' concurrent work.
'''
(P/'HANDOFF.md').write_text(handoff,encoding='utf-8')
note='''
Bill east bowl pickup/return candidates — September30,2026.
Primary exec-84ef5a85-15bb-4bdb-ad4b-79defd58a607/exact prompt retained; six448/447/
449/444/444/444px figures. Focused short-reach source exec-bb8b1f90-8d45-499a-8d4e-
97ea8a7c5c6b/exact prompt,both844px. Use reach0+primary1/2/3/4,exact selected idle/
eating-held endpoints; duplicate/generated endpoints remain raw but unused.
Two bare states/14refs,seven slots580ms/exact reversed return. Fixed atlas rulers
primary[.31,.332],reach[.156,.17536],master matte grade/sole223/pivot128,224/H148.
29package/87native PASS12.13s;148/82 boards reviewed;2,914owner files unchanged.
Lesson: a smooth pickup needs an authored short empty reach before full extension,
not merely an exact idle join. Add the missing pose and explicit timing; retain
raw sources and independent whole-source rulers. Exact endpoints do not prove
interior registration: crown75–77 and head-axisX128–132 remain for full-set polish.
Source/player finite joins only; no normal actor/registry changes. Next cup
pickup/return/full east meal install and actual counter/interruptions/restore,
then remaining cardinal meals/rest/drydeath/full polish. Full goal active.
Handoff: character/bill-meal-entry-east-v1/HANDOFF.md.
'''
for name in ['docs/BILL_ANIMATION_CONTINUATION_2026-09-29.md','docs/ASSET_PIPELINE_AND_WORKFLOW.md','docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md','skills/brinespace-character-pipeline/references/crew-consistency.md']:
    with (ROOT/name).open('a',encoding='utf-8') as f:f.write(note)
with Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md').open('a',encoding='utf-8') as f:f.write(note)
status=ROOT/'docs/CURRENT_STATUS.md';status.write_bytes(('## Bill east bowl pickup/return candidates — September30,2026\n'+note+'\n').encode()+status.read_bytes())
files=list((P/'sources').glob('*'))+[P/name for name in ['build.py','verify.py','manifest.json','source-rulers.json','registration.json','verification.json','frame-hashes.json','HANDOFF.md','build_preview.py','index.html','contact-sheet.png']]+[ROOT/'tests/test_bill_meal_entry_east_candidates.gd',ROOT/'tools/run_bill_meal_entry_east_candidate_validation.py',OUT/'validation.json',OUT/'loaded-water-carry.png']
(P/'candidate-evidence.json').write_text(json.dumps({'status':'staged_candidate','checks':{'package':29,'native':87},'native':n,'scope':'source/fixed rulers/finite exact idle-held joins only; cup transitions/normal activity/contact/restore/full polish pending','sha256':{f.relative_to(ROOT).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in files}},indent=2)+'\n',encoding='utf-8')
print('Recorded bowl pickup/return milestone; full goal active')
