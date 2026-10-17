from pathlib import Path
import json,hashlib,subprocess
from milestone_notes import record_guides
p=Path(__file__).resolve().parent;r=p.parents[1];sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
folders=[p/'arrival-journey-v323',p/'arrival-join-v324']
for version,o,total in [(323,folders[0],2520),(324,folders[1],2522)]:
 v=json.loads((o/'native_probe-validation.json').read_bytes());n=json.loads((o/'native-evidence.json').read_bytes());inputs=json.loads((o/'inputs.json').read_bytes())
 assert v['exitCode']==0 and not v['timedOut'] and v['realProfileUnchanged'] and not v['profileDelta']
 assert (n['checks'],n['failures'],len(n['results']))==(total,0,2)
 log=(o/'native_probe.log').read_text(encoding='utf-8');assert 'SCRIPT ERROR:' not in log and 'ERROR:' not in log
 for path,h in inputs['preLaunchSha256'].items():
  f=o/'tested-player-before-join.gd.txt' if version==323 and path=='scripts/james_cargo_player.gd' else r/path
  assert sha(f)==h
 assert all(len(row['captures'])==16 and len(row['checkpoints'])==2 and len(row['observedSlots'])==12 for row in n['results'])
 assert all((r/path[6:]).exists() for row in n['results'] for path in row['captures'])
 assert len(json.loads((o/'review-boards.json').read_bytes()))==4
 report=dict(version=version,disposition='normal_paired_arrival_journey_review',checks=total,failures=0,routes=2,nativeCapturesReviewed=32,freshSceneWholeRunDiskRestores=4,candidateBanksLoaded=False,ownerProfileUnchanged=True,normalFirstUnloadSourceChanged=version==324,continuousVisualAcceptance=False,titleContinueTested=False,autonomousGoalSelectionTested=False,fullGoalComplete=False,findings=['Prescribed collision-clear96-world-unit west approaches use actual normal James update/move/arrive. Both equipment versions automatically enter north turn/unload, remain physically stationary through2s stage and release origin on completion. All6normal turn and6unload slots observed per gear.', 'Four actual whole-run disk checkpoints: mid-turn and mid-unload per gear. Fresh normal scene, no candidate reinstall, staged restore; actor/playback/visual clocks and source pose exact, paused processing holds. This is RunSave fresh-scene restore, not title-screen Continue.', 'All32native capture regions reviewed in4boards per run, no rescaling. Screenshot framing changes after fresh-scene restore; exact source checks separately establish resumed pose. Static advancing simulation samples are not continuously observed real-time motion.', '323 visual evidence shows old first unload source steps one foot forward after planted turn endpoint.324 James-owned loader reuses whole exact turn endpoint as first north unload source in each gear, guarded by canvas/pivot/standing-height compatibility. Existing clocks, later poses, other crew and raw art files preserved. No body painting or fitting.', 'The next unloading stance, broad/deep bend, body/head/gear/material changes and final rise remain. Current normal bank is older artwork;317/320and latest49cargo/306turn candidates remain unselected. Master fidelity/full family/integration acceptance still incomplete.'])
 (o/'review.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
o=folders[1];ledger=p/'material-repair-progress.json';old=ledger.read_bytes();d=json.loads(old)
d['northArrivalJourneyReview']=dict(version=324,file=(o/'review.json').relative_to(r).as_posix(),checks=2522,failures=0,routes=2,capturesReviewed=32,freshSceneWholeRunDiskRestores=4,normalFirstUnloadSourceChanged=True,normalRawArtworkChanged=False,latestCandidatesSelected=False,visualAcceptance=False)
d['normalChanged']=True;d['normalFirstUnloadSourceChanged']=True;d['normalRawArtworkChanged']=False
d['nextVisualRepair']='324 normal paired west arrival joins unload0 to exact turn endpoint;2522checks0/32native captures/4fresh normal whole-run disk restores. Remaining first stance/bend/material/head/gear/final rise/case-to-idle and shared helmet; latest49carry/306turn/317or320unload master source fidelity remains unselected. Next advancing paired motion and autonomous goal-selection/full titleContinue/interruptions, all-family consistency.'
assert ledger.read_bytes()==old;ledger.write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8')
section='''### James normal arrival journey and exact unload entrance - October3,2026

V323 normal paired west routes through actual update/move/arrive:2520checks0,
32native captures/all viewed,4fresh-scene whole-run disk restores (mid-turn and
mid-unload per gear), no candidate bank reinstall. Both6turn/6unload slots observed,
physical target stays fixed through2s arrival, origin clears on completion. Source
actor/playback/visual clocks/pixels exact after restore; pause holds; owner unchanged.
Review exposes old unload0 one-foot-forward pose after planted turn endpoint.

V324 owned James loader reuses whole registered turn endpoint for first north
unloading frame in each gear, checking canvas/pivot/standing-height compatibility
and preserving3argument manifest loader contract. Clocks/later poses/raw artwork
and other crew unchanged. Rechecked same paired actual journeys:2522checks0,
32native captures/all viewed,4fresh normal whole-run disk restores; exact endpoint
reuse verified. Frozen324code hashes unchanged;323tested player snapshot matches
original pre-run hash. All new screenshots under LFS. No generated body patch.

Lesson: valid selector timing can still jump to an incompatible first drawing.
Judge the actual room cut, then reuse a compatible whole accepted endpoint where
the action should remain stationary. Verify bare/equipment bank load order and
fresh normal restore, not merely a staged source manifest. These are prescribed
routes and sampled advancing simulation: not autonomous goal choice, title-screen
Continue or continuously watched real-time motion. Remaining next stance/bend,
material/head/gear/height/support/rise/case-to-idle and helmet are not approved.
Latest49carry/306turn/317and320unload candidates remain unselected; full master
consistency and all-family integration/polish open. Handoff:
character/james-west-carry-walk-keys-v1/arrival-join-v324/HANDOFF.md.
'''
guides=record_guides(r,section,'### James cargo constructor identity and crew regression - October3,2026')
handoff='''# Project handoff

Updated: October3,2026 · Project: Brine Space · Task: James normal arrival join

## Objective and acceptance
Full master-matched James set, real integration and all-family polish. Sampled
simulation, exact source checks and visual motion acceptance are separate.

## Accepted decisions and constraints
Matte master/engineering identity, fixed support, wrench on belt, diagnostics
tablet/forward torch. Preserve raw art, timings, other crew and owner profile.

## Current state
scripts/james_cargo_player.gd owned loader hooks reuse exact registered turn end
as first north unload source in bare/equipment banks.323/324 normal journey probes,
UIDs/frozen code/logs/traces/64captures/8review boards, generation/assembler helpers,
ledger/five guides. No new generated art; latest review candidates unselected.

## Verification
3232520checks0 exposes old foot step at cut;3242522checks0 after source reuse.
Both2routes/32reviewed captures/4fresh-scene whole-run disk restores, no candidate
reinstall, exact actor/playback/pose/clock/pause, all12turn/unload slots per gear.
Owner unchanged,324hashes stable,323tested player text matches pre-run hash.
No autonomous choice/titleContinue or continuous real-time visual acceptance.

## Next action
Review paired advancing motion and repair remaining next stance/deep bend,
material/head/gear/height/support/final rise/case-to-idle/helmet. Latest49carry,
306turn and317/320unload master fidelity remains unselected. Autonomous goal
selection, full titleContinue and interruptions, all-family polish remain. Full
goal active, no external blocker.
'''
(o/'HANDOFF.md').write_text(handoff,encoding='utf-8')
(folders[0]/'HANDOFF.md').write_text(handoff.replace('Task: James normal arrival join','Task: James normal arrival evidence before join')+'\n323 is pre-fix evidence; current implementation and next work live in324.\n',encoding='utf-8')
with(p/'HANDOFF.md').open('a',encoding='utf-8') as f:f.write('\n'+section)
rasters=[f.relative_to(r).as_posix() for folder in folders for f in folder.rglob('*.png')]
attrs=subprocess.run(['git','check-attr','-z','--stdin','filter'],input=('\0'.join(rasters)+'\0').encode(),cwd=r,capture_output=True,check=True).stdout.split(b'\0');assert all(attrs[i+2]==b'lfs' for i in range(0,len(attrs)-1,3))
print(json.dumps(dict(currentChecks=2522,currentFailures=0,currentCapturesReviewed=32,currentFreshSceneDiskRestores=4,normalEntrySourceReuse=True,guides=guides,lfsRasters=len(rasters),fullGoalComplete=False)))
