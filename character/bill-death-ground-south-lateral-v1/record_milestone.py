from pathlib import Path
import json,hashlib
P=Path(__file__).resolve().parent;R=P.parents[1];H=P.parent/'bill-death-ground-helmet-south-lateral-v1'
assert not (P/'candidate-evidence.json').exists(), 'Preserve evidence; record a new revision explicitly.'
bare=json.loads((P/'verification.json').read_text());helmet=json.loads((H/'verification.json').read_text());assert bare['passed'] and bare['checks']==20 and helmet['passed'] and helmet['checks']==37
reports={};files=[]
for folder,count in [('bill-death-ground-south-lateral-candidate-native-v1',37),('bill-death-ground-helmet-south-lateral-candidate-native-v1',38),('bill-death-ground-south-lateral-station-v1',74),('bill-death-ground-south-lateral-paired-station-v1',143)]:
 out=R/'output'/folder;r=json.loads((out/'validation.json').read_text());assert r['returnCode']==0 and r['nativeScreenshot']
 assert f'{count} checks,0 failures' in (out/'native.log').read_text()
 reports[folder]={'checks':count,**r};files.extend(out/name for name in ['validation.json','native.log','profile-before.json','profile-after.json','loaded-water-carry.png'])
audit=json.loads((R/'output/bill-death-ground-south-lateral-paired-station-v1/projection-audit.json').read_text());assert len(audit['records'])==96
assert all(not row['overlaps'] for row in audit['records'] if row['direction']=='south' and row['slot']>=4)
guards='\n'.join(f"{key}: overall {r['passed']}; {r['seconds']}s; {r['realProfileFileCount']:,} owner files; changes {r['realProfileChanges']}" for key,r in reports.items())
summary='''Bill south lateral-collapse paired candidate — October 1, 2026.
Independent front lateral source exec-daa571bf-5553-4248-8762-3b832bef7e49 and
exact prompt preserved. One [.29,.342] ruler,256plane/p128,224/H148, exact accepted
bare/equipped idle, six250/300/350/400/400/300ms finite slots,2s terminal hold.
Authored lateral floor contacts, natural lowering and front master details; one
pooled matte neutral/hair/skin/burgundy grade. No per-frame exposure normalization.
Native36x42 canonical front helmet follows neck/tilt0/18/35/90/90 at scale1.
Closed-eye donor exec-0b1ad8c7-6822-4afb-816d-f4980cb3c9fe saved with exact prompt.
Only24 native RGB pixels in two declared eye windows sampled from authored donor
and face-graded; all component alpha, shell/visor/collar/beard/outline outside those
windows exact. Closed-eye component used only settled frames4/5. Source/review
and paired-body checks bound; donor's changed helmet design discarded entirely.
20 bare/37 helmet package checks and37/38 native player checks pass.74 bare and
143 paired station checks pass: actual galley owner layout copied into scratch,
unchanged geometry, existing RoomFlooding.kill and station renderer, two contacts,
fixture-controlled cardinal headings.96 pose projections and48 native room captures.
South lateral settled slots4/5 have zero opaque-pixel intrusion into registered
counter collision rectangles at audited counter/aisle. Native counter/aisle and
148/82 paired/master rows visually reviewed. Fine eye readability at gameplay size,
collar/arm/kneel joins and full identity/detail matching remain polish work.
Profile guard results are separate from green subsystem checks:
'''+guards+'''
Live real-project process381456 observed; do not stop/restore owner state or retry
to seek a clean interval. Strict failed profile guards remain failures.
Candidates only; forward open-floor art remains. Normal contact-aware variant
choice, saved identity, actual survival-trigger/restore/fresh Continue and wider
obstruction/hazard/furniture/cargo joins still open. Projected terminal clearance is
not anatomical floor-footprint certification or acceptance of every intermediate.
Next combine north/south lateral options with saved contact-aware candidate choice
and appropriate actual mortality/restore/placement proof before normal selection.
Generic rest, meals/inspection proof and full-set cross-animation polish remain.
Lesson: shared helmet identity and terminal expression are separate contracts.
Use an authored semantic donor within a tiny bound RGB window, preserve alpha and
canonical hardware; don't replace the whole wearable merely to close the eyes.
No owner layout, route/reward/economy, normal art selection, commit or export change.
Full goal active.
'''
handoff='''# Project handoff

Updated: October 1, 2026 · Brine Space · Task: Bill south lateral collapse

## Objective and acceptance
Full master-consistent Bill animation set, then cross-animation consistency/polish.

## Accepted decisions and constraints
Fixed anatomical ruler, exact idle and shared helmet, matte materials. Keep owner
geometry and saves intact; every engine fixture uses scratch APPDATA.

## Current state
Bare/equipped south lateral packages, reproducible extraction/grade/equipment/eye
tools, manifests, native fixtures/runners and review pages. Separate candidates.

## Verification
'''+summary+'''
## Next action
Saved contact-aware candidate choice, actual mortality/restore and wider clearance;
remaining life actions and full master polish stay open.
'''
for pack in [P,H]:
 (pack/'HANDOFF.md').write_text(handoff,encoding='utf-8')
 files.extend(f for f in pack.rglob('*') if f.is_file() and '__pycache__' not in f.parts and f.suffix!='.import' and f.name!='candidate-evidence.json')
for name in ['test_bill_death_ground_south_lateral_candidates','test_bill_death_ground_helmet_south_lateral_candidates','test_bill_death_ground_south_lateral_station','test_bill_death_ground_south_lateral_paired_station']:
 files.extend([R/'tests'/(name+'.gd'),R/'tests'/(name+'.gd.uid')])
files.extend(R/'tools'/name for name in ['run_bill_death_ground_south_lateral_candidate_validation.py','run_bill_death_ground_helmet_south_lateral_candidate_validation.py','run_bill_death_ground_south_lateral_station_validation.py','run_bill_death_ground_south_lateral_paired_station_validation.py'])
files.append(R/'output/bill-death-ground-south-lateral-paired-station-v1/projection-audit.json')
(P/'candidate-evidence.json').write_text(json.dumps({'status':'paired_lateral_candidate_terminal_projection_reviewed','nativeArtPassed':True,'reports':reports,'packageChecks':57,'scope':summary,'sha256':{f.relative_to(R).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in files},'captureBindings':json.loads((P/'station-review.json').read_text())['captureBindings']},indent=2)+'\n',encoding='utf-8')
heading='## Bill south lateral-collapse paired candidate — October 1, 2026\n\n'
for rel in ['docs/BILL_ANIMATION_CONTINUATION_2026-09-29.md','docs/ASSET_PIPELINE_AND_WORKFLOW.md','docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md','skills/brinespace-character-pipeline/references/crew-consistency.md']:
 with (R/rel).open('a',encoding='utf-8') as f:f.write('\n'+heading+summary)
with Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md').open('a',encoding='utf-8') as f:f.write('\n'+heading+summary)
f=R/'docs/CURRENT_STATUS.md';f.write_bytes((heading+summary+'\nHandoff: character/bill-death-ground-south-lateral-v1/HANDOFF.md.\n\n').encode('utf-8')+f.read_bytes())
print('Recorded57 package/292 native subsystem passes; strict profile-guard outcomes retained separately')
