from pathlib import Path
import json,hashlib
P=Path(__file__).resolve().parent;R=P.parents[1];H=P.parent/'bill-death-ground-helmet-north-lateral-v1'
assert not (P/'candidate-evidence.json').exists(), 'Preserve milestone; record a new revision explicitly.'
bare=json.loads((P/'verification.json').read_text());helmet=json.loads((H/'verification.json').read_text())
assert bare['passed'] and bare['checks']==20 and helmet['passed'] and helmet['checks']==34
reports={};files=[]
for folder,count in [('bill-death-ground-north-lateral-candidate-native-v1',37),('bill-death-ground-helmet-north-lateral-candidate-native-v1',38),('bill-death-ground-north-lateral-station-v1',74),('bill-death-ground-north-lateral-paired-station-v1',143)]:
 out=R/'output'/folder;r=json.loads((out/'validation.json').read_text());assert r['returnCode']==0 and r['passed'] and not r['realProfileChanges']
 assert f'{count} checks,0 failures' in (out/'native.log').read_text()
 reports[folder]={'checks':count,**r}
 files.extend(out/name for name in ['validation.json','native.log','profile-before.json','profile-after.json','loaded-water-carry.png'])
audit=json.loads((R/'output/bill-death-ground-north-lateral-paired-station-v1/projection-audit.json').read_text())
assert len(audit['records'])==96
assert all(not row['overlaps'] for row in audit['records'] if row['direction']=='north' and row['slot']>=4)
summary='''Bill north lateral-collapse paired candidate — October 1, 2026.
New six-pose lateral source exec-2ce04e0f-480d-4f18-84fe-df00c2811e58 fitted
with one [.328,.355] ruler into256plane/p128,224/H148; exact accepted bare/equipped
idle entry, six finite slots250/300/350/400/400/300ms and terminal hold at2s.
Authored source floor contacts track the lateral roll; torso is not height-normalized.
One pooled master neutral/hair/skin/burgundy grade preserves subdued matte detail.
Canonical native35x36 rear helmet follows neck/tilt0/20/50/90/90 without scaling;
bare bodies remain pixel-exact outside declared local hair/equipment region.
20 bare/34 helmet package checks and37/38 native player checks pass.148/82 paired
and idle rows reviewed.74 bare/143 paired actual-station checks pass: owner galley
copied to scratch, original geometry and RoomFlooding.kill/renderer, two contacts,
fixture-controlled cardinal headings.96 paired authored pose projections/48 captures.
North lateral settled slots4/5 have zero opaque pixel intrusion into registered
counter collision rectangles at the audited contact and aisle. Native counter/aisle
joins reviewed at original crop scale; head now lies beside counter rather than
across its face. Source final corpse relaxed; canonical head design/color retained.
All four overall runners pass with2,928 owner non-log files unchanged. These clean
intervals do not retrospectively certify earlier failed profile guards.
Candidate injection only: original forward fall retained; no normal contact-aware
choice, saved variant identity or fresh Continue proof yet. Exact kneel/repair limb
joins and intermediate upper-body furniture interaction need finer review. Projected
alpha/counter clearance does not prove anatomical floor footprint or all placement.
South axial terminal remains overlapping at this counter; other directions/gear,
arbitrary hazard/cargo/furniture joins and full-set master polish remain.
Next implement/verify contact-aware candidate choice with persisted variant and
actual death/restore/obstruction evidence, then south-aware source as required.
Generic rest, meal/inspection proof and complete cross-animation polish remain.
Lesson: preserve the open-floor fall and author an obstacle-aware lateral option;
one foot sort point or clear navigation anchor cannot certify a long prone body.
No owner layout, route/reward/economy, normal art binding, commit or export changes.
Full objective stays active.
'''
handoff='''# Project handoff

Updated: October 1, 2026 · Brine Space · Task: Bill north lateral collapse

## Objective and acceptance
Full master-consistent Bill animation set followed by cross-animation polish.

## Accepted decisions and constraints
Exact accepted idle, canonical helmet, matte suit and one ruler. Keep owner geometry.
Reversible candidate work authorized. Scratch profiles for every engine probe.

## Current state
Bare/helmet lateral packages, reproducible tools, manifests, review pages and native
fixtures/runners added. Candidate packages remain separate from normal selection.

## Verification
'''+summary+'''
## Next action
Contact-aware saved variant selection and real mortality/restore proof; wider joins,
south counter fall, remaining life actions and full consistency polish stay open.
'''
(P/'HANDOFF.md').write_text(handoff,encoding='utf-8');(H/'HANDOFF.md').write_text(handoff,encoding='utf-8')
for pack in [P,H]:
 files.extend(f for f in pack.rglob('*') if f.is_file() and '__pycache__' not in f.parts and f.suffix!='.import' and f.name!='candidate-evidence.json')
for name in ['test_bill_death_ground_north_lateral_candidates','test_bill_death_ground_helmet_north_lateral_candidates','test_bill_death_ground_north_lateral_station','test_bill_death_ground_north_lateral_paired_station']:
 files.extend([R/'tests'/(name+'.gd'),R/'tests'/(name+'.gd.uid')])
files.extend(R/'tools'/name for name in ['run_bill_death_ground_north_lateral_candidate_validation.py','run_bill_death_ground_helmet_north_lateral_candidate_validation.py','run_bill_death_ground_north_lateral_station_validation.py','run_bill_death_ground_north_lateral_paired_station_validation.py'])
files.append(R/'output/bill-death-ground-north-lateral-paired-station-v1/projection-audit.json')
e={'status':'paired_lateral_candidate_counter_terminal_reviewed','reports':reports,'packageChecks':54,'scope':summary,'sha256':{f.relative_to(R).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in files},'captureBindings':json.loads((P/'station-review.json').read_text())['captureBindings']}
(P/'candidate-evidence.json').write_text(json.dumps(e,indent=2)+'\n',encoding='utf-8')
heading='## Bill north lateral-collapse paired candidate — October 1, 2026\n\n'
for rel in ['docs/BILL_ANIMATION_CONTINUATION_2026-09-29.md','docs/ASSET_PIPELINE_AND_WORKFLOW.md','docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md','skills/brinespace-character-pipeline/references/crew-consistency.md']:
 with (R/rel).open('a',encoding='utf-8') as f:f.write('\n'+heading+summary)
with Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md').open('a',encoding='utf-8') as f:f.write('\n'+heading+summary)
f=R/'docs/CURRENT_STATUS.md';f.write_bytes((heading+summary+'\nHandoff: character/bill-death-ground-north-lateral-v1/HANDOFF.md.\n\n').encode('utf-8')+f.read_bytes())
print('Recorded paired lateral candidate:54 package and292 native checks pass; normal saved variant choice remains')
