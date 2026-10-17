from pathlib import Path
import hashlib,json,shutil
from milestone_notes import record_guides
p=Path(__file__).resolve().parent;r=p.parents[1];src=p/'water-stop-bridge-v340';out=p/'water-clearance-review-v342';out.mkdir(exist_ok=True)
for stem in ['clearance_probe','interrupt_probe','probe']:
    v=json.loads((src/f'{stem}-validation.json').read_bytes());assert v['exitCode']==0 and v['realProfileUnchanged'] and not v['timedOut']
    for suffix in ['.log','-validation.json']:shutil.copyfile(src/(stem+suffix),out/(stem+suffix))
clearance=json.loads((src/'clearance-review.json').read_bytes());assert clearance['checks']==3697 and clearance['failures']==0 and clearance['directionChangeResets']==0 and clearance['gearSamples']==272 and clearance['collisionCases']==32
interrupt=json.loads((src/'interrupt-review.json').read_bytes());assert interrupt['checks']==2289 and interrupt['failures']==0
entry=json.loads((src/'traces.json').read_bytes());assert entry['checks']==290 and entry['failures']==0
for name in ['clearance-review.json','interrupt-review.json','traces.json']:shutil.copyfile(src/name,out/name)
bindings={}
for stem in ['phase_player','staged_grid','clearance_probe','interrupt_probe','probe']:
    f=src/(stem+'.gd');assert (src/(stem+'.gd.uid')).is_file();bindings[str(f.relative_to(r))]=hashlib.sha256(f.read_bytes()).hexdigest();shutil.copyfile(f,out/(stem+'.gd.txt'))
report={'version':342,'clearanceChecks':3697,'entryChecks':290,'interruptChecks':2289,'failures':0,'directionChangesPreserved':816,'gearChangesChecked':272,'collisionCases':32,'initialDiagnostic':{'checks':1153,'failures':0,'directionResets':816,'finding':'Diagnostic established every changed heading canceled the stop before its finite rise completed.'},'postRunCodeBindings':bindings,'prelaunchFreeze':False,'normalChanged':False,'sourceAcceptance':False,'fullGoalComplete':False,'ownerProfileUnchanged':True,'scope':'Staged whole-stop pose retention on tread heading changes; nonmutating clearance prediction; fixture renderer hook and actual James collision primitive on synthetic flooded geometry. No main-scene drawing, exterior geometry, cross-heading swimming restart or whole-run Continue acceptance.'}
(out/'review.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
section='''### James staged heading-safe rise and full-bridge clearance — October 3, 2026

V342 staged same exact selected artwork. Initial1153check diagnostic found816
direction changes canceled a still-active stop and jumped upright. Staged player
now completes its finite rise before adopting a new resting heading; actor direction
and physical movement remain independent. Nonmutating preview predicts the exact
clip for clearance, including active rise and helmet bank; no playback time consumed.
Fixture-only Grid subclass passes the predicted whole envelope to actual James
swim_segment_clear on synthetic flooded geometry. Normal renderer remains unchanged.

Final scratch runs:3697clearance/lifecycle checks0,816changed-heading pose matches
and correct terminal facing,272gear changes,32open/intersecting-blocker cases;
290all-phase entry checks0/48cases and2289restart/pause/fresh-restore checks0/272samples
rerun after player changes. Owner profile unchanged. Tested source snapshots and
post-run hashes retained; prelaunch freeze false. Existing V341 pixel chronology
is unchanged, but its older behavioral revision is superseded by these checks.

Not game acceptance: main-scene rendering/ordinary actor routes, exterior geometry,
resuming swimming toward a different heading during the rise, blocked-space
fallback and whole-run Continue remain. Complete temporal review and responsiveness
before normal installation. Full animation coverage/master fidelity and whole-family
polish still incomplete. No generated art, production selection or global crew change.
Handoff: character/james-west-carry-walk-keys-v1/water-clearance-review-v342/HANDOFF.md.
'''
record_guides(r,section,'### James staged swimming chronology and gameplay-size previews — October 3, 2026')
(out/'HANDOFF.md').write_text('# Project handoff\n\nUpdated: October 3, 2026 · Task: James water lifecycle/clearance\n\n## Objective and acceptance\nFull James animations matching original masters, then consistency/polish. Incomplete.\n\n## Accepted decisions and constraints\nPreserve selected pixels/rulers/grade/tools; keep physical heading/movement independent. Staged source remains unselected.\n\n## Current state\n'+section+'\n## Verification\n3697clearance +290entry +2289interruption checks0;816heading/272gear samples;32synthetic collision cases;owner unchanged. Logs/reports/tested text source snapshots retained here; executable pairedUID sources remain in V340.\n\n## Next action\nCheck changed-heading swimming restart and blocked-space fallback, then complete full motion/native main-scene/exterior/Continue evidence before normal integration. Continue remaining families and master fidelity/polish.\n',encoding='utf-8')
with (p/'HANDOFF.md').open('a',encoding='utf-8') as f:f.write('\n'+section)
ledger=p/'material-repair-progress.json';old=ledger.read_bytes();data=json.loads(old);data['waterClearanceReview']={'version':342,'file':str((out/'review.json').relative_to(r)),'clearanceChecks':3697,'failures':0,'directionChangesPreserved':816,'normalChanged':False};assert ledger.read_bytes()==old;ledger.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
print('V342:3697clearance +290entry +2289interruption checks0;816heading changes preserved;five guides/handoff updated;staged only.')
