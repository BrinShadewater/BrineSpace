import json,subprocess
from pathlib import Path
from milestone_notes import record_guides
root=Path.cwd();bank=root/'character/james-west-carry-walk-keys-v1';review=bank/'release-hazard-playtest-v353';output=root/'output/james-hazard-playtest-v353'
validation=json.loads((output/'validation.json').read_text());data=json.loads((review/'lifecycle-review.json').read_text())
assert validation['exitCode']==0 and validation['ownerUnchanged'] and validation['qaOverrideRemoved']
assert data['failures']==0 and len(data['cases'])==16
assert (review/'hazard_playtest.gd.uid').exists()
paths=[p.relative_to(root).as_posix() for p in review.glob('*.png')];assert len(paths)==20
attrs=subprocess.run(['git','check-attr','--stdin','-z','filter'],input=('\0'.join(paths)+'\0').encode(),capture_output=True,check=True).stdout.split(b'\0');assert all(attrs[i]==b'lfs' for i in range(2,len(attrs)-1,3))
section=f'''### James packaged survival handoffs — October 4, 2026

V353 unchanged V351 Windows package: {data['checks']} checks, zero failures, sixteen
cases across four directions/both gear variants and recovery/fatal outcomes.
Actual RoomFlooding.step_crew plus normal actor updates dispatched swim distress,
finite recovery after breathable air returned, and water death after air exhausted.
No direct die() or recovery-pose invocation. {len(data['captures'])} native 10Hz captures,
sixteen lossless animated PNG playbacks and four chronology boards. Four boards
visually reviewed; no obvious cut-off or missing-body transition in sampled poses.
Owner profile unchanged under scratch APPDATA; temporary QA override removed.
Exact package hashes in output/james-hazard-playtest-v353/validation.json.

Scope: scripted low initial reserves, fully flooded authored rooms and scheduled
drain for recovery; fixed60Hz survival/actor updates with normal packaged renderer.
Initial technically passing run obscured by expedition summary after James death;
excluded from visual acceptance. Diagnostic reruns preserved in output subfolders.
The fixture repeatedly stepped survival on the already-dead actor, unlike normal
RoomFlooding.advance, exhausting crew_count. Final fixture follows the live dead-
actor guard, retains another survivor and asserts summary_layer hidden for every
native capture. A child-panel visibility assertion was also corrected. Production
failure rules remain active; no runtime fix was needed.
This establishes survival-triggered animation handoffs, not autonomous refuge
routing, exterior excursions or full-game water propagation. Animated playbacks
supplied for review, not continuously observed by the agent. No production changes
or rebuild. Cargo quilt/North unload stance remain polish; final autonomous water/
exterior playtest and continuous selected-clip acceptance remain open.
'''
(review/'review.json').write_text(json.dumps({'version':353,'checks':data['checks'],'cases':len(data['cases']),'captures':len(data['captures']),'validation':validation,'visualReview':'Four chronology boards viewed; no obvious cut-off or missing-body transition in sampled poses. Native playbacks supplied; not continuously observed by agent.','scope':data['scope'],'productionChanged':False,'packageRebuilt':False,'remaining':'Autonomous refuge/exterior review and full continuous selected-clip acceptance; cargo quilt and North unload stance polish.'},indent=2)+'\n')
handoff='''# Project handoff

Updated: October 4, 2026 · Project: Brine Space · Task: James survival handoffs

## Objective and acceptance
Finish James and prepare the next playable version. Survival-triggered animation
handoffs tested in the existing package; full visual closeout remains open.

## Accepted decisions and constraints
Accepted art and gameplay rules preserved; tests use scratch APPDATA. No new
artwork, production edits, executable rebuild or publication in this milestone.

## Current state
V353 fixture/UID, preparation/run/media/closeout helpers and twenty LFS raster
outputs. Exact tested package remains V351 brinespace-5024faab0e485c1a.

## Verification
'''+section+'''
## Next action
Complete autonomous water/exterior review and continuous game-scale acceptance.
Avoid further stationary water studies. Keep known cargo material/stance polish
explicit; do not claim it fixed or all animations accepted.
'''
(review/'HANDOFF.md').write_text(handoff);(output/'HANDOFF.md').write_text(handoff)
record_guides(root,section,'### James packaged cargo lifecycle — October 4, 2026')
with (bank/'HANDOFF.md').open('a',encoding='utf8') as f:f.write('\n'+section)
f=bank/'material-repair-progress.json';old=f.read_bytes();ledger=json.loads(old);ledger['releaseSurvivalPlaytest']={'version':353,'cases':16,'checks':data['checks'],'failures':0,'ownerUnchanged':True,'productionChanged':False,'fullVisualGoalComplete':False};assert f.read_bytes()==old;f.write_text(json.dumps(ledger,indent=2)+'\n')
f=root/'docs/JAMES_RELEASE_CLOSEOUT.md';old=f.read_bytes();text=f.read_text();text=text.replace('V346 source coverage; V349 actual die() dispatch and normal renderer:419 checks0,16 direction/gear/medium cases,96 captures, eight boards viewed.',f'V353 actual packaged survival triggers pass {data["checks"]} checks and 16 direction/gear/outcome cases: low-air distress, breathable-air recovery and exhaustion death. Four native chronology boards reviewed. Earlier V349 covers dry/water death source dispatch.');text=text.replace('Continuous motion and normal hazard dispatch. Static source review alone does not close runtime acceptance.','Continuous motion and autonomous refuge/exterior hazard playtest remain. Controlled flooding and initial air reserves establish survival dispatch.');text=text.replace('Next action: review ordinary water/hazard behavior','Next action: complete autonomous water/exterior and continuous game-scale review');assert f.read_bytes()==old;f.write_text(text)
print(json.dumps({'version':353,'cases':16,'checks':data['checks'],'failures':0,'ownerUnchanged':True,'rasterLfs':20}))
