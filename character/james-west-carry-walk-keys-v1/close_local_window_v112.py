from pathlib import Path
import json,hashlib,subprocess
from milestone_notes import record_guides
p=Path(__file__).resolve().parent;r=p.parents[1];out=p/'local-window-v112';sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
d=json.loads((out/'inputs.json').read_bytes());assert all(sha(r/f)==h for f,h in d['preLaunchSha256'].items())
n=json.loads((out/'native-evidence.json').read_bytes());v=json.loads((out/'native_probe-validation.json').read_bytes())
assert (n['checks'],n['failures'],n['captures'])==(60,0,4)
assert v['exitCode']==0 and not v['timedOut'] and v['realProfileUnchanged'] and not v['profileDelta']
manifest=json.loads((out/'bare-manifest.json').read_bytes())['states'][0]
assert manifest['sourceIndices']==[10,11,12,13] and manifest['frameDurationsMs']==[20]*4
findings=['Phase12 now retains fine quilt, fitting and boot construction instead of the earlier V51 simplified body; closer visual continuity with10/11.',
 'Unrepaired13 and protected original boot rims still have bright highlights. Lower12 upper-tail highlights reduce modestly while median rises; not uniform darkening.',
 'Original pose alpha and protected upper body/head remain exact; internal anatomical/equipment landmarks are visually assessed rather than strict original-master geometry.',
 'Static reviewed sources/native poses do not prove continuous motion, absence of flash, full49 gait, normal lifecycle or cross-family acceptance.']
folders=[]
for name,execution,boards,guards in [
 ('local-material-phase12-v110','52e91268-f4e4-420c-9ef0-86b65b687753',['crop-detail-review.png','paired-local-review.png'],['alphaExact','outerTwoPixelRingExact','headTop110Exact','bootsBelow200Exact','pairedBodyBelow110Exact']),
 ('lower-material-phase12-v111','d09693fc-5780-4bab-aad9-72e3c7be2ec3',['lower-detail-review.png','paired-lower-review.png'],['alphaExact','outerOnePixelRingExact','allRowsAbove181Exact','pairedBodyBelow110Exact'])]:
 folder=p/name;folders.append(folder);d=json.loads((folder/'inputs.json').read_bytes())
 for group in ['sourceSha256','referenceSha256']:assert all(sha(r/f)==h for f,h in d[group].items())
 assert sha(folder/'prompt.txt')==d['promptSha256']
 (folder/'generation.json').write_text(json.dumps(dict(state='terminal_copied',execution=execution,rawSha256=sha(folder/'raw.png'),prompt='prompt.txt',inputs='inputs.json',normalChanged=False),indent=2)+'\n')
 f=folder/'package-review.json';review=json.loads(f.read_bytes());assert all(review[k] for k in guards)
 review.update(disposition='retain_provisional_phase12_detail_refinement',reviewedSourceBoards=boards,visualReviewer='Codex',nativeIncluded=True,findings=findings)
 f.write_text(json.dumps(review,indent=2)+'\n')
ledger=p/'material-repair-progress.json';j=json.loads(ledger.read_bytes());row=j['states'][12];folder=folders[-1]
sources={m:dict(file=(folder/f'{m}-head-protected.png').relative_to(r).as_posix(),sha256=sha(folder/f'{m}-head-protected.png')) for m in ['bare','helmet']}
if row['candidateSources']!=sources:row.setdefault('supersededCandidateSources',[]).append(row['candidateSources'])
row.update(candidateSources=sources,sourceAcceptance=False,reviewStatus='provisional_phase12_detail_refinement_master_neighbor_motion_pending')
j['lowerMaterialRefinementPhases']=sorted(set(j['lowerMaterialRefinementPhases']+[12]));j['nextVisualRepair']='phase13 source/material repair; lower detail continuity and full gait review'
assert j['candidatePhases']==23 and len(j['remainingSourcePhases'])==26
ledger.write_text(json.dumps(j,indent=2)+'\n')
(out/'review.json').write_text(json.dumps(dict(nativeChecks=60,nativeFailures=0,pairedSources=8,sourceIndices=[10,11,12,13],durationsMs=[20]*4,reviewedNativeCaptures=4,reviewedNativeBoards=['native-review-0.png','native-review-1.png'],reviewedSourceWindowBoard='local-source-review.png',visualReviewer='Codex',findings=findings,continuousVisualMotionAcceptance=False,sourceAcceptance=False,normalChanged=False,fullGoalComplete=False),indent=2)+'\n')
section='''### James phase12 fine construction restored in neighbour review — October 2, 2026

V110local body repair starts from original phase12 V16 pose, not simplified V51.
V111lower material repair starts from V110. Both generated raws/prompts/frozen
references copied and terminal. Four source boards visually reviewed. Body admits
2587pixels with62949outside exact, original alpha/two-pixel rim/head above110 and
boots from200 down exact. Lower admits1005pixels with64531outside exact, original
alpha/one-pixel rim/rows above181exact. Both paired body below110 exact. Internal
equipment/pose landmarks remain visual candidates, not strict master geometry.

V112 reviews actual10/11/12/13 (13original unrepaired),20ms each,80ms total. Native
60checks/0failures/four paired four-size captures plus source window all reviewed.
Scratch APPDATA owner profile unchanged; frozen input/runtime/registry hashes
stable. Phase12 fine quilt/fittings/boots now closer to10/11 than prior simplified
V51. Phase13 and protected boot rims retain stronger highlights. Lower12 local
95thpercentile172.20to169.23 while median64.92to68.48; modest highlight restraint,
not uniformly darker material or25percent reduction. No continuous visual motion
or full gait/master anatomy acceptance. Ledger12 now V111, V51preserved; coverage
still23/49provisional phases with26remaining. Nothing installed in normal play.

Lesson: recover lost construction from the original same-pose source rather than
polishing a simplified intermediate. Separate body/lower repairs can retain pose
registration, but protected outlines do not prove internal anatomy. Check the
next unrepaired neighbour before claiming sequence material consistency. Next13
and remaining26sources, coordinated lower joins, full motion/normal lifecycle,
original-master proportions and cross-family consistency. Full goal incomplete.
Evidence:character/james-west-carry-walk-keys-v1/local-window-v112/review.json.
'''
guides=record_guides(r,section,'### James carrying phase10/11 repairs reveal phase12 detail join')
handoff='''# Project handoff

Updated: October2,2026. Task: James complete master-matched set and polish.

## Objective and acceptance
Full animation library matching masters, complete motion/integration and
cross-family consistency. Still incomplete.

## Accepted decisions and constraints
Original same-pose source and high-resolution master are authorities. Reversible
work authorized; preserve owner profile and normal selections.

## Current state
Phase12 body/lower detail repaired; prior candidate retained. Ledger and five
guides updated. No normal installation, commit, PR or export.

## Verification
60 native checks, zero failures; four paired captures and source boards reviewed.
Frozen inputs and owner profile unchanged. Continuous motion/master anatomy open.

## Next action
Repair phase13 and remaining26 sources; resolve lower/detail joins, full motion,
normal lifecycle and cross-family consistency.

'''
for folder in folders+[out]:(folder/'HANDOFF.md').write_text(handoff+section,encoding='utf-8')
with (p/'HANDOFF.md').open('ab') as f:f.write(b'\n'+section.encode())
rasters=[f.relative_to(r).as_posix() for folder in folders+[out] for f in folder.rglob('*') if f.suffix in ['.png','.apng']]
attrs=subprocess.run(['git','check-attr','-z','filter','--stdin'],cwd=r,input=b'\0'.join(f.encode() for f in rasters)+b'\0',capture_output=True,check=True).stdout.split(b'\0')
assert len(attrs)==3*len(rasters)+1 and all(x==b'lfs' for x in attrs[2:-1:3])
print(json.dumps(dict(checks=60,failures=0,capturesReviewed=4,candidates=23,remaining=26,guides=guides,lfsRasters=len(rasters),normalChanged=False,nextRepair=13)))
