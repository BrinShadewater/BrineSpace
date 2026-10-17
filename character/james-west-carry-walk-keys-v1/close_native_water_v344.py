from pathlib import Path
import hashlib,json,subprocess,sys
from milestone_notes import record_guides
p=Path(__file__).resolve().parent;r=p.parents[1];o=p/'water-native-review-v344';src=p/'water-stop-bridge-v340'
for stem in ['native_probe','dispatch_probe']:
    v=json.loads((o/(stem+'-validation.json')).read_bytes());assert v['exitCode']==0 and v['realProfileUnchanged'] and not v['timedOut']
native=json.loads((o/'native-review.json').read_bytes());dispatch=json.loads((o/'dispatch-review.json').read_bytes())
assert native['checks']==1314 and native['failures']==0 and len(native['captures'])==328
assert dispatch['checks']==38 and dispatch['failures']==0
index=json.loads((o/'visual-index.json').read_bytes());reviewed={name:hashlib.sha256((o/name).read_bytes()).hexdigest() for name in index['boards']}
subprocess.run([sys.executable,str(p/'review_native_water_v344.py')],check=True,capture_output=True)
assert all(hashlib.sha256((o/name).read_bytes()).hexdigest()==sha for name,sha in reviewed.items()),'New native boards differ from eight actually reviewed boards'
index=json.loads((o/'visual-index.json').read_bytes());index['actuallyViewed']=True;index['reviewLimits']='Very dim deep-flood lighting; placement/pose/room visibility samples only. Fine helmet/material/grade and continuous motion acceptance remain.'
(o/'visual-index.json').write_text(json.dumps(index,indent=2)+'\n',encoding='utf-8')
media=list(o.rglob('*.png'));attrs=subprocess.run(['git','check-attr','--stdin','-z','filter'],input=b''.join(str(f.relative_to(r)).replace('\\','/').encode()+b'\0' for f in media),cwd=r,capture_output=True,check=True).stdout.split(b'\0');assert len(media)==337 and all(attrs[i]==b'lfs' for i in range(2,len(attrs)-1,3))
bindings={}
for f in [r/'scripts/grid_canvas.gd',r/'scripts/james_cargo_actor.gd',src/'phase_player.gd',src/'reorient_player.gd',src/'staged_grid.gd',o/'native_probe.gd',o/'dispatch_probe.gd']:
    assert f.with_suffix('.gd.uid').is_file();bindings[str(f.relative_to(r))]=hashlib.sha256(f.read_bytes()).hexdigest()
report={'version':344,'nativeChecks':1314,'nativeFailures':0,'nativeCaptures':328,'directionGearCases':24,'normalDispatchChecks':38,'normalDispatchFailures':0,'normalCodeChanged':True,'stagedRepairSelected':False,'sourceArtworkChanged':False,'ownerProfileUnchanged':True,'fullGoalComplete':False,'sourceAcceptance':False,'boardsActuallyViewed':index['boards'],'reviewLimits':index['reviewLimits'],'postRunCodeBindings':bindings,'prelaunchFreeze':False,'finding':'Normal JamesCargoActor subclasses Branforth. Filename equality skipped James-specific clearance and generic action bounds canceled the staged stop before capture. Production grid now identifies James through script inheritance; other crew retain their branch. New phase/reorient banks are still fixture-only.','scope':native['scope'],'remaining':'Autonomous moving routes, blocked fallback, repeated command/completion behavior, exterior clearance, normal repair selection, fresh-scene disk Continue and full temporal/material/master/family polish.'}
(o/'review.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
section='''### James native water renderer and actual actor dispatch — October 3, 2026

V344 actual main scene/JamesCargoActor, staged player/Grid subclass and authored
flooded workshop. Initial native attempts failed before entry: generic clearance
reset the stop to tread. Trace proves actual actor is scripts/james_cargo_actor.gd,
not the old branforth_npc.gd filename. Production Grid now walks script inheritance
to recognise James; original James and actual subclass admitted, other crew excluded.
Existing concurrent Grid edits preserved. No new phase/reorient production selection.

Normal dispatch38checks0 on actual subclass/base/other crew and selected envelope
open/obstructed cases. Native recheck after production change1314checks0,24direction/
gear cases and328actual draws. Every prescribed reorientation pose sampled via actual
renderer; entry/terminal pixels and stationary physical foot exact. Eight native
comparison boards actually viewed; rebuilt final boards byte-match reviewed images.
337LFS media including retained failure image; paired scriptUIDs, owner profiles
unchanged. Post-run hashes retained; no prelaunch freeze.

Deep-flood lighting is too dim for fine texture/grade/helmet acceptance. Reviewed
poses are visible and registered without obvious clipping at this fixture location;
stills do not establish continuously observed motion or autonomous movement.
Native probe's legacy normalChanged:false field refers to its staged selection;
production dispatch correction is recorded separately here as normalCodeChanged:true.
Remaining moving routes/blocked fallback/repeated commands/exterior clearance,
fresh whole-run disk Continue and visual timing/material/master/family polish.
Full animation goal active/incomplete. Native pass is not full-game acceptance.
Handoff: character/james-west-carry-walk-keys-v1/water-native-review-v344/HANDOFF.md.
'''
record_guides(r,section,'### James staged changed-heading swimming restart — October 3, 2026')
(o/'HANDOFF.md').write_text('# Project handoff\n\nUpdated: October 3, 2026 · Task: James native water renderer\n\n## Objective and acceptance\nFull James animation set matching original masters, then consistency/polish. Incomplete.\n\n## Accepted decisions and constraints\nPreserve selected artwork, rulers/grade/tools; keep physics independent. Existing authorization covers this actual actor dispatch correction; staged transition bank remains unselected.\n\n## Current state\n'+section+'\n## Verification\n1314native checks0/328draws/24direction-gear cases;38normal actor dispatch checks0;8boards viewed/final rebuild byte-match;337LFS media;owner unchanged. Initial native failures/traces retained.\n\n## Next action\nExercise moving NPC routes and blocked fallback with correct full envelope, fresh whole-run Continue, exterior/repeated commands and temporal review. Improve exposure for fine visual evaluation without changing source grade. Complete remaining families/master consistency/polish.\n',encoding='utf-8')
with (p/'HANDOFF.md').open('a',encoding='utf-8') as f:f.write('\n'+section)
ledger=p/'material-repair-progress.json';old=ledger.read_bytes();data=json.loads(old);data['waterNativeReview']={'version':344,'file':str((o/'review.json').relative_to(r)),'nativeChecks':1314,'dispatchChecks':38,'failures':0,'captures':328,'normalCodeChanged':True,'stagedRepairSelected':False};assert ledger.read_bytes()==old;ledger.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
print('V344:1314native/38normal dispatch checks0;328captures/8reviewed boards/337LFS media;five guides updated;repair remains staged.')
