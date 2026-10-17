from pathlib import Path
import json,hashlib,subprocess
from milestone_notes import record_guides
p=Path(__file__).resolve().parent;r=p.parents[1];out=p/'local-window-v109'
sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
frozen=json.loads((out/'inputs.json').read_bytes())
assert all(sha(r/f)==h for f,h in frozen['preLaunchSha256'].items())
n=json.loads((out/'native-evidence.json').read_bytes());v=json.loads((out/'native_probe-validation.json').read_bytes())
assert (n['checks'],n['failures'],n['captures'])==(60,0,4)
assert v['exitCode']==0 and not v['timedOut'] and v['realProfileUnchanged'] and not v['profileDelta']
manifest=json.loads((out/'bare-manifest.json').read_bytes())['states'][0]
assert manifest['sourceIndices']==[9,10,11,12] and manifest['frameDurationsMs']==[20]*4
findings=['New phase10/11 textile and fittings are subdued and remain readable in source crops, whole figures and four-size native views.',
 'Earlier phase12 candidate has smoother textile, simpler boot construction and different case/body presentation than phase9..11. Join remains visibly inconsistent; correct detail before full motion acceptance.',
 'Exact original alpha, two-pixel rim, head above110 and boots from200 down protect source registration; internal material landmarks and original-master anatomy remain visual candidates.',
 'Original boot highlights in10/11 remain; full49 natural motion, normal carrying lifecycle and cross-family acceptance remain pending.']
ledger=p/'material-repair-progress.json';j=json.loads(ledger.read_bytes());folders=[]
for phase,version,execution in [(10,107,'dd19a645-e61a-47c5-9cdb-ef87e6d2ebdc'),(11,108,'be572197-d265-4219-914e-fd0a0b959076')]:
 folder=p/f'local-material-phase{phase}-v{version}';folders.append(folder);d=json.loads((folder/'inputs.json').read_bytes())
 for group in ['sourceSha256','referenceSha256']:assert all(sha(r/f)==h for f,h in d[group].items())
 assert sha(folder/'prompt.txt')==d['promptSha256']
 (folder/'generation.json').write_text(json.dumps(dict(state='terminal_copied',execution=execution,rawSha256=sha(folder/'raw.png'),prompt='prompt.txt',inputs='inputs.json',normalChanged=False),indent=2)+'\n')
 f=folder/'package-review.json';review=json.loads(f.read_bytes())
 assert all(review[k] for k in ['alphaExact','outerTwoPixelRingExact','headTop110Exact','bootsBelow200Exact','pairedBodyBelow110Exact'])
 review.update(disposition='retain_provisional_local_material_candidate',reviewedSourceBoards=['crop-detail-review.png','paired-local-review.png'],visualReviewer='Codex',nativeIncluded=True,findings=findings)
 f.write_text(json.dumps(review,indent=2)+'\n')
 row=j['states'][phase]
 if not row['repairCandidateAvailable']:
  assert phase in j['remainingSourcePhases'];j['remainingSourcePhases'].remove(phase);j['candidatePhases']+=1
 row.update(repairCandidateAvailable=True,sourceAcceptance=False,reviewStatus='provisional_local_material_master_neighbor_boots_motion_pending',candidateSources={m:dict(file=(folder/f'{m}-head-protected.png').relative_to(r).as_posix(),sha256=sha(folder/f'{m}-head-protected.png')) for m in ['bare','helmet']})
assert j['candidatePhases']==23 and len(j['remainingSourcePhases'])==26
j['nextVisualRepair']='phase12 smoother textile, simplified boots and case/body presentation discontinuity against9..11'
ledger.write_text(json.dumps(j,indent=2)+'\n')
(out/'review.json').write_text(json.dumps(dict(nativeChecks=60,nativeFailures=0,pairedSources=8,sourceIndices=[9,10,11,12],durationsMs=[20]*4,reviewedNativeCaptures=4,reviewedNativeBoards=['native-review-0.png','native-review-1.png'],reviewedSourceWindowBoard='local-source-review.png',visualReviewer='Codex',findings=findings,continuousVisualMotionAcceptance=False,sourceAcceptance=False,normalChanged=False,fullGoalComplete=False),indent=2)+'\n')
section='''### James carrying phase10/11 repairs reveal phase12 detail join — October 2, 2026

V107phase10 and V108phase11 local body-crop sources are terminal/copied with exact
prompts and frozen original master textile/pose references. Four crop/paired source
boards reviewed. Protected admission2635/2663pixels;62901/62873outside exact.
Original full alpha/two-pixel rim, head above110 and boots from200 down exact;
paired body below110 exact. Fittings are less stark and quilting readable. Interior
pose/equipment landmarks remain visual candidates, not original-master equality.

V109 actual consecutive9/10/11/12 keeps20ms each (80ms), eight paired sources.
Native60checks/0failures; all four paired four-size captures plus source window
reviewed. Scratch APPDATA owner profile unchanged; frozen input/runtime/registry
hashes stable. Phase12 V51 visibly differs: smoother textile, simpler boots and
different case/body presentation. Technical success does not accept that join.
Original bright boot pixels remain in10/11. Static captures do not establish
continuous motion or absence of a flash. Next repair12 construction against its
original pose and the master, then remaining26phase sources and full gait review.

Ledger23/49provisional candidate phases,26remaining. New10/11 sources retained;
no normal selection changes. Full original-master anatomy/detail, carrying
lifecycle, cross-family consistency/polish remain incomplete. Lesson: earlier
whole-body matte repairs can lose fine construction; check them when local
repairs reach their neighbours, rather than equating darker finish with matching
detail. Evidence:character/james-west-carry-walk-keys-v1/local-window-v109/review.json.
'''
guides=record_guides(r,section,'### James carrying material coverage reaches phase9')
handoff='''# Project handoff

Updated: October2,2026. Task: full James master-matched animation set and polish.

## Objective and acceptance
All families matching original masters in art, proportions, perspective and grade;
full motion, normal game lifecycle and cross-family polish remain incomplete.

## Accepted decisions and constraints
Reversible repairs authorized. Original master is authority. Preserve normal
selection and owner profile. Passing technical checks are not visual acceptance.

## Current state
Two local body sources10/11 retained provisionally; ledger and five guides updated.
No normal installation, commit, PR or export.

## Verification
60 native checks, zero failures; four paired captures at four sizes and source
boards reviewed. Frozen hashes and owner profile unchanged. Phase12 join fails
detail consistency; full motion and master anatomy acceptance remain pending.

## Next action
Repair phase12 lost construction against original pose and master, then extend
remaining26 phases, review complete gait and normal lifecycle/cross-family joins.

'''
for folder in folders+[out]:(folder/'HANDOFF.md').write_text(handoff+section,encoding='utf-8')
with (p/'HANDOFF.md').open('ab') as f:f.write(b'\n'+section.encode())
rasters=[f.relative_to(r).as_posix() for folder in folders+[out] for f in folder.rglob('*') if f.suffix in ['.png','.apng']]
attrs=subprocess.run(['git','check-attr','-z','filter','--stdin'],cwd=r,input=b'\0'.join(f.encode() for f in rasters)+b'\0',capture_output=True,check=True).stdout.split(b'\0')
assert len(attrs)==3*len(rasters)+1 and all(x==b'lfs' for x in attrs[2:-1:3])
print(json.dumps(dict(checks=60,failures=0,capturesReviewed=4,candidates=23,remaining=26,guides=guides,lfsRasters=len(rasters),normalChanged=False,nextRepair=12)))
