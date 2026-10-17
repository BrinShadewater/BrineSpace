import json,subprocess
from pathlib import Path
from milestone_notes import record_guides
root=Path.cwd();bank=root/'character/james-west-carry-walk-keys-v1';review=bank/'release-escape-playtest-v354';output=root/'output/james-escape-playtest-v354'
validation=json.loads((output/'validation.json').read_text());data=json.loads((review/'lifecycle-review.json').read_text())
assert validation['exitCode']==0 and validation['ownerUnchanged'] and validation['qaOverrideRemoved']
assert data['failures']==0 and len(data['cases'])==8
assert all(c['retreated'] and c['arrived'] and c['recovered'] and not c['dead'] for c in data['cases'])
assert (review/'escape_playtest.gd.uid').exists()
paths=[p.relative_to(root).as_posix() for p in review.glob('*.png')];assert len(paths)==12
attrs=subprocess.run(['git','check-attr','--stdin','-z','filter'],input=('\0'.join(paths)+'\0').encode(),capture_output=True,check=True).stdout.split(b'\0');assert all(attrs[i]==b'lfs' for i in range(2,len(attrs)-1,3))
section=f'''### James packaged refuge routing — October 4, 2026

V354 unchanged V351 Windows package: {data['checks']} checks, zero failures, eight
cases across four cardinal refuge positions and both gear variants. Normal flood-
safety controller independently selected a retreat goal/path, crossed the authored
storage-room doorway, reached the dry refuge alive and completed natural low-air
recovery. No assigned path/goal or scheduled draining. {len(data['captures'])} native 10Hz
captures retained as eight lossless animated PNGs and four chronology boards.
Four boards viewed; no obvious missing-body or furniture clipping in sampled poses.
Owner unchanged under scratch APPDATA; exact package hashes verified, temporary
QA override removed. Review: release-escape-playtest-v354/review.json in James bank.

Scope: fixture chooses a feasible starting graph contact, sets low initial reserves
with a 3.5-second planned-route margin and supplies normal flooded-cell navigation
classification; two authored storage rooms with fixed flooded/dry water levels.
Actual controller selects and follows its own route at fixed60Hz; not autonomous
station setup, real-time pacing, dynamic water propagation or exterior expedition.
Early fixture bound of 2.5 seconds excluded valid routes (shortest 2.5296 seconds);
failed diagnostics preserved in output/james-escape-playtest-v354, not acceptance.
Animated playbacks supplied, not continuously observed by agent. No production
edits or rebuild. Remaining: exterior expedition and continuous game-scale selected
animation review; cargo material/North unload stance remain recorded polish.
'''
(review/'review.json').write_text(json.dumps({'version':354,'validation':validation,'checks':data['checks'],'cases':data['cases'],'nativeCaptures':len(data['captures']),'visualReview':'Four chronology boards viewed. No obvious missing-body or furniture clipping in sampled poses; animated native playbacks supplied, not continuously observed by agent.','scope':data['scope'],'productionChanged':False,'packageRebuilt':False,'remaining':'Exterior expedition and continuous game-scale selected-clip review; cargo material/North unload stance polish.'},indent=2)+'\n')
handoff='''# Project handoff

Updated: October 4, 2026 · Project: Brine Space · Task: James refuge routing

## Objective and acceptance
Finish James and prepare the next game version. Controller-selected flooded-room
escape and natural recovery verified in the existing packaged Windows candidate.

## Accepted decisions and constraints
Preserve accepted artwork and gameplay rules. Existing reversible work authorized;
owner saves protected. No production edits, rebuilt package or publication here.

## Current state
New V354 escape fixture/UID, preparation/run/media/closeout helpers, eight native
animated PNG playbacks and four chronology boards. V351 package unchanged.

## Verification
'''+section+'''
## Next action
Review exterior expedition and selected clips in continuous motion. Avoid repeating
stationary water studies. Keep cargo material and North unload stance polish explicit.
'''
(review/'HANDOFF.md').write_text(handoff);(output/'HANDOFF.md').write_text(handoff)
record_guides(root,section,'### James packaged survival handoffs — October 4, 2026')
with (bank/'HANDOFF.md').open('a',encoding='utf8') as f:f.write('\n'+section)
f=bank/'material-repair-progress.json';old=f.read_bytes();ledger=json.loads(old);ledger['releaseRefugePlaytest']={'version':354,'checks':data['checks'],'cases':8,'failures':0,'ownerUnchanged':True,'productionChanged':False,'fullVisualGoalComplete':False};assert f.read_bytes()==old;f.write_text(json.dumps(ledger,indent=2)+'\n')
f=root/'docs/JAMES_RELEASE_CLOSEOUT.md';old=f.read_bytes();text=f.read_text();text=text.replace('Final ordinary autonomous water/exterior visual review; blocked transitions retain existing immediate fallback.','V354 controller selects and traverses refuge routes in four cardinal directions/both gears, then completes natural recovery. Final exterior and continuous motion review remain; blocked transitions retain existing immediate fallback.');text=text.replace('Continuous motion and autonomous refuge/exterior hazard playtest remain.','V354 controller-selected refuge escape passes eight cases. Continuous motion and exterior hazard playtest remain.');text=text.replace('Next action: complete autonomous water/exterior and continuous game-scale review','Next action: complete exterior and continuous game-scale review');assert f.read_bytes()==old;f.write_text(text)
print(json.dumps({'version':354,'checks':data['checks'],'cases':8,'failures':0,'ownerUnchanged':True,'rasterLfs':12}))
