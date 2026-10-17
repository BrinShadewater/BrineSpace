from pathlib import Path
import json,hashlib,subprocess
from milestone_notes import record_guides
p=Path(__file__).resolve().parent;r=p.parents[1];out=p/'local-window-v115';sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
d=json.loads((out/'inputs.json').read_bytes());assert all(sha(r/f)==h for f,h in d['preLaunchSha256'].items())
n=json.loads((out/'native-evidence.json').read_bytes());v=json.loads((out/'native_probe-validation.json').read_bytes())
assert (n['checks'],n['failures'],n['captures'])==(60,0,4)
assert v['exitCode']==0 and not v['timedOut'] and v['realProfileUnchanged'] and not v['profileDelta']
manifest=json.loads((out/'bare-manifest.json').read_bytes())['states'][0]
assert manifest['sourceIndices']==[12,13,14,15] and manifest['frameDurationsMs']==[20]*4
findings=['Phase13/14 fittings and fine quilt are more subdued and readable beside repaired12 in source and four-size native views.',
 'Original boots from200 down in13/14 and unrepaired15 retain stronger highlights; lower finish consistency remains pending.',
 'Exact alpha/two-pixel rim, head above110 and boots from200 down protect source registration; interior anatomical/equipment landmarks remain visual candidates.',
 'Static source/native review is not continuous motion or absence-of-flash acceptance. Full49 gait, original-master anatomy, normal carrying lifecycle and cross-family acceptance remain pending.']
ledger=p/'material-repair-progress.json';j=json.loads(ledger.read_bytes());folders=[]
for phase,version,execution in [(13,113,'e26b7d60-1ac9-4bda-ad79-accb0aa1e35f'),(14,114,'48e77c6f-0102-4063-9865-b76c801db89e')]:
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
assert j['candidatePhases']==25 and len(j['remainingSourcePhases'])==24
j['nextVisualRepair']='phase15/16 source/material repair; original lower highlights and full gait continuity'
ledger.write_text(json.dumps(j,indent=2)+'\n')
(out/'review.json').write_text(json.dumps(dict(nativeChecks=60,nativeFailures=0,pairedSources=8,sourceIndices=[12,13,14,15],durationsMs=[20]*4,reviewedNativeCaptures=4,reviewedNativeBoards=['native-review-0.png','native-review-1.png'],reviewedSourceWindowBoard='local-source-review.png',visualReviewer='Codex',findings=findings,continuousVisualMotionAcceptance=False,sourceAcceptance=False,normalChanged=False,fullGoalComplete=False),indent=2)+'\n')
section='''### James carrying material coverage extends through phase14 — October 2, 2026

V113phase13 and V114phase14 local body-crop sources are terminal/copied with exact
prompts and frozen original pose/master textile references. Four source crop/paired
boards reviewed. Admission2668/2732pixels;62868/62804outside exact. Original full
alpha/two-pixel rim/head above110 and boots from200 down exact; paired body below110
exact. Fine quilt and fittings remain readable with less stark highlights. Internal
equipment/anatomical landmarks remain visual candidates, not strict master equality.

V115 actual12/13/14/15 retains20ms each (80ms), eight paired sources;15original
unrepaired. Native60checks/0failures/four paired four-size captures plus source
window all visually reviewed. Scratch APPDATA owner profile unchanged; frozen
input/runtime/registry hashes stable. Body finish13/14closer to repaired12; original
boot highlights13/14and stronger fittings15remain. No continuous visual motion,
absence-of-flash or full49gait acceptance. Ledger25/49provisional source phases,
24remaining. Nothing installed in normal play; full James master anatomy/detail,
normal carrying lifecycle and cross-family consistency/polish remain incomplete.

Lesson: record repair coverage separately for body and lower hardware. An authored
body candidate can increase source coverage while its unchanged boots still need
a coordinated finish pass; do not call the whole frame fully repaired. Next15/16
and remaining24sources, lower/detail joins, full gait/normal lifecycle and master
comparisons across all families. Evidence:character/james-west-carry-walk-keys-v1/
local-window-v115/review.json.
'''
guides=record_guides(r,section,'### James phase12 fine construction restored in neighbour review')
handoff='''# Project handoff

Updated: October2,2026. Task: full James master-matched set and polish.

## Objective and acceptance
All animation families matching original masters in art, proportions, perspective
and colour; full motion, normal integration and consistency polish remain required.

## Accepted decisions and constraints
Reversible repairs authorized; original master authority. Protect original pose
registration, owner profile and normal selections. Tests are not art acceptance.

## Current state
New13/14body candidates; ledger25/49,24remaining. Five guides updated. No normal
installation, commit, PR or export.

## Verification
60 native checks, zero failures; four paired captures/four sizes and source boards
reviewed. Frozen inputs and owner profile unchanged. Lower highlights still differ;
continuous motion, original-master anatomy and full family consistency open.

## Next action
Repair15/16and remaining24sources, coordinate lower finish, then full gait,
normal lifecycle and cross-family master consistency.

'''
for folder in folders+[out]:(folder/'HANDOFF.md').write_text(handoff+section,encoding='utf-8')
with (p/'HANDOFF.md').open('ab') as f:f.write(b'\n'+section.encode())
rasters=[f.relative_to(r).as_posix() for folder in folders+[out] for f in folder.rglob('*') if f.suffix in ['.png','.apng']]
attrs=subprocess.run(['git','check-attr','-z','filter','--stdin'],cwd=r,input=b'\0'.join(f.encode() for f in rasters)+b'\0',capture_output=True,check=True).stdout.split(b'\0')
assert len(attrs)==3*len(rasters)+1 and all(x==b'lfs' for x in attrs[2:-1:3])
print(json.dumps(dict(checks=60,failures=0,capturesReviewed=4,candidates=25,remaining=24,guides=guides,lfsRasters=len(rasters),normalChanged=False,nextRepair=15)))
