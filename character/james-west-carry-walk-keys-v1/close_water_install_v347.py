import hashlib,json,subprocess
from pathlib import Path
from milestone_notes import record_guides
r=Path.cwd();p=r/'character/james-west-carry-walk-keys-v1';o=p/'water-install-review-v347'
candidate=json.loads((o/'install-review.json').read_text());native=json.loads((o/'installed-native-review.json').read_text())
for name in ['install_probe','installed_native_probe','crew_regression','allocate_uid']:
    report=json.loads((o/(name+'-validation.json')).read_text());assert report['exitCode']==0 and report['realProfileUnchanged']
assert candidate['failures']==native['failures']==0
assert 'BRANFORTH THREE CREW: PASS' in (o/'crew_regression.log').read_text()
files=[r/'scripts'/name for name in ['james_water_phase_player.gd','james_water_player.gd','james_water_clearance.gd','grid_canvas.gd']]
for f in files:assert f.with_suffix(f.suffix+'.uid').exists()
names=[f.relative_to(r).as_posix() for f in o.glob('*.png')]
result=subprocess.run(['git','check-attr','--stdin','-z','filter'],input=('\0'.join(names)+'\0').encode(),capture_output=True,check=True).stdout.split(b'\0')
assert len(names)==10 and all(result[i]==b'lfs' for i in range(2,len(result)-1,3))
report={'version':347,'selected':True,'candidateChecks':candidate['checks'],'completionCases':candidate['completionCases'],'rows':candidate['rows'],'nativeChecks':native['checks'],'freshSceneDiskRestores':2,'crewRegression':'PASS; minimum separation 32.01','realProfileUnchanged':True,'nativeScope':native['scope'],'sourceArtworkChanged':False,'visualReview':'All ten native route crops viewed. Visible registered poses; exact before/after restore pixels. Deep flood lighting too dim for fine master/material judgment. Static captures do not establish continuous temporal acceptance.','postRunBindings':{f.relative_to(r).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in files},'prelaunchFreeze':False,'remaining':'Final selected-library motion/master review, furniture/hazard lifecycle, ordinary autonomous water/exterior visual review, then fresh release and packaged gameplay/Continue. Blocked transitions retain existing immediate locomotion fallback; not a newly authored smooth blocked-space bridge.'}
(o/'review.json').write_text(json.dumps(report,indent=2)+'\n')
section='''### James swimming handoff installed for release closeout — October 3, 2026

V347 installs scripts/james_water_player.gd and james_water_phase_player.gd,
both inheriting the accepted cargo player. Grid uses this player and builds exact
selected-pose finite rows only after all normal bare/helmet overrides load; fresh
scenes therefore have the same banks before checkpoint restoration. No source art,
grade, scale, pivot or selected original clip clocks changed. Concurrent Grid work
preserved. The former staged water repair is now selected in normal gameplay.

New james_water_clearance.gd checks the entire finite clip along the distance the
actor can travel before completion. Flooded checks use actual segment geometry;
exterior checks use conservative swept alpha bounds against existing wreck/hull/
registered prop blockers, without moving the actor to predict clearance. Obstructed
clips use existing immediate locomotion fallback; smooth blocked cancellation is
not claimed. New heading/stop requests at reorientation completion start from the
completed neutral pose and finish the requested heading before rising.

11521candidate checks0 across288rows/2304completion commands, flooded blocking,
open-sea current/future obstruction and read-only prediction. Installed normal
player/Grid native51checks0, two24-unit move() routes and two fresh-scene whole-run
disk restores; no fixture player/Grid replacement. Actor/playback/clock/pause and
resume pixels exact. Ten native crops actually viewed, all LFS; deep flood lighting
limits material review and stills do not certify full continuous motion. Existing
test_branforth_crew PASS, minimum separation32.01; dry actions, checkpoint admission,
crew clocks and legacy saves covered by that existing regression. All runs use
scratch APPDATA and owner files unchanged. ScriptUIDs paired; post-run bindings
saved, no prelaunch freeze. Initial parse-name collision repaired before testing.

Next: final selected animation motion/master consistency, furniture/hazard lifecycle
and ordinary autonomous water/exterior visual review, then fresh playable export
and packaged gameplay/Continue. Stop adding stationary water studies. Full animation
goal remains incomplete. No executable build or publication yet.
Handoff: character/james-west-carry-walk-keys-v1/water-install-review-v347/HANDOFF.md.
'''
record_guides(r,section,'### James release closeout, moving swim checkpoint and hazard source review — October 3, 2026')
handoff='# Project handoff\n\nUpdated: October 3, 2026 · Task: James swimming installation\n\n## Objective and acceptance\nFinish James for the next playable release soon; full animation goal incomplete.\n\n## Accepted decisions and constraints\nPreserve accepted source art/tools/grade and owner saves. Release focus, no new speculative material trials.\n\n## Current state\n'+section+'\n## Verification\n11521 candidate checks, 51 installed native checks, two fresh-scene disk resumes, existing crew regression PASS; all owner files unchanged. Ten native crops viewed; dim flood lighting and static review limitations retained.\n\n## Next action\nReturn to selected family motion/master and furniture/hazard lifecycle review. Then build and validate the next playable version. No further stationary water studies.\n'
(o/'HANDOFF.md').write_text(handoff)
with (p/'HANDOFF.md').open('a',encoding='utf8') as f:f.write('\n'+section)
ledger=p/'material-repair-progress.json';old=ledger.read_bytes();data=json.loads(old);data['waterInstalledReview']={'version':347,'selected':True,'checks':11521,'nativeChecks':51,'restores':2,'crewRegression':'PASS','file':str((o/'review.json').relative_to(r))};assert ledger.read_bytes()==old;ledger.write_text(json.dumps(data,indent=2)+'\n')
doc=r/'docs/JAMES_RELEASE_CLOSEOUT.md';old=doc.read_text();new=old.replace('V344 establishes real actor dispatch and native stationary staged restart continuity. Production actor identification is fixed. | Moving route, checkpoint resume, blocked clearance, exterior and repeated requests before selecting the staged transition bank.','V347 repair installed in normal gameplay. 11521 transition/clearance checks, 51 installed native checks, two fresh-scene disk resumes and crew regression pass. | Final ordinary autonomous water/exterior visual review; blocked transitions retain existing immediate fallback.').replace('Staged improvements do not count as shipped improvements.','V347 swimming repair is installed; other staged improvements do not count as shipped improvements.').replace('Next action: finish the V345 swimming route/checkpoint result, make a bounded decision on its runtime selection, then review the selected full set in motion and close the concrete defects.','Next action: review the selected full set in motion and close the concrete defects. Swimming installation is complete; do not restart its stationary studies.')
doc.write_text(new)
print('V347 installed:11521candidate/51native checks0;2disk restores;crew regressionPASS;five guides and release checklist updated')
