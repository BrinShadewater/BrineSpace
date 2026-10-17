from pathlib import Path
import json,hashlib,subprocess
from milestone_notes import record_guides
p=Path(__file__).resolve().parent;r=p.parents[1];folder=p/'local-material-phase9-v105';out=p/'local-window-v106'
sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
d=json.loads((folder/'inputs.json').read_bytes())
for group in ['sourceSha256','referenceSha256']:assert all(sha(r/f)==h for f,h in d[group].items())
assert sha(folder/'prompt.txt')==d['promptSha256']
frozen=json.loads((out/'inputs.json').read_bytes())
assert all(sha(r/f)==h for f,h in frozen['preLaunchSha256'].items())
n=json.loads((out/'native-evidence.json').read_bytes());v=json.loads((out/'native_probe-validation.json').read_bytes())
assert (n['checks'],n['failures'],n['captures'])==(47,0,3)
assert v['exitCode']==0 and not v['timedOut'] and v['realProfileUnchanged'] and not v['profileDelta']
findings=['Frame9 fabric and fittings are more subdued in source and native views; fine quilting and existing grip remain readable.',
 'Unrepaired frame10 has stronger white hardware highlights; frame9 boots remain unrepaired original pixels. Whole-neighbor material consistency is pending.',
 'Original alpha and two-pixel rim, head above110 and boots from200 down are exact. Interior pose landmarks are visually assessed, not proven master geometry.',
 'Three static native captures at four sizes are not continuously watched motion or full49 gait, normal lifecycle or original-master anatomy acceptance.']
(folder/'generation.json').write_text(json.dumps(dict(state='terminal_copied',execution='73405352-2ef0-4875-8415-2f92872deb31',rawSha256=sha(folder/'raw.png'),prompt='prompt.txt',inputs='inputs.json',normalChanged=False),indent=2)+'\n')
f=folder/'package-review.json';review=json.loads(f.read_bytes())
assert all(review[k] for k in ['alphaExact','outerTwoPixelRingExact','headTop110Exact','bootsBelow200Exact','pairedBodyBelow110Exact'])
review.update(disposition='retain_provisional_local_material_candidate',reviewedSourceBoards=['crop-detail-review.png','paired-local-review.png'],visualReviewer='Codex',findings=findings,nativeIncluded=True)
f.write_text(json.dumps(review,indent=2)+'\n')
manifest=json.loads((out/'bare-manifest.json').read_bytes())['states'][0]
assert manifest['sourceIndices']==[8,9,10] and manifest['frameDurationsMs']==[30,20,20]
(out/'review.json').write_text(json.dumps(dict(nativeChecks=47,nativeFailures=0,pairedSources=6,sourceIndices=[8,9,10],durationsMs=[30,20,20],reviewedNativeCaptures=3,reviewedNativeBoards=['native-review-0.png'],reviewedSourceWindowBoard='local-source-review.png',visualReviewer='Codex',findings=findings,continuousVisualMotionAcceptance=False,sourceAcceptance=False,normalChanged=False,fullGoalComplete=False),indent=2)+'\n')
f=p/'material-repair-progress.json';j=json.loads(f.read_bytes());row=j['states'][9]
if not row['repairCandidateAvailable']:
 assert 9 in j['remainingSourcePhases'];j['remainingSourcePhases'].remove(9);j['candidatePhases']+=1
row.update(repairCandidateAvailable=True,sourceAcceptance=False,reviewStatus='provisional_local_material_master_neighbor_boots_motion_pending',candidateSources={m:dict(file=(folder/f'{m}-head-protected.png').relative_to(r).as_posix(),sha256=sha(folder/f'{m}-head-protected.png')) for m in ['bare','helmet']})
assert j['candidatePhases']==21 and len(j['remainingSourcePhases'])==28
f.write_text(json.dumps(j,indent=2)+'\n')
section='''### James carrying material coverage reaches phase9 — October 2, 2026

V105 authors the existing phase9 body crop against the original high-resolution
master textile sample. Terminal raw, exact prompt and frozen references copied.
Protected admission2694pixels;62842outside exact. Original alpha/two-pixel rim,
head above110 and boots from200 down exact; paired body below110 exact. Crop and
paired source boards reviewed: subdued fitting highlights with readable quilting
and grip. Interior landmark fidelity remains visual, not strict master equality.

V106 reviews actual phases8/9/10, last using unrepaired original source. Original
clock30/20/20ms (70ms), six paired sources;47native checks/0failures, three paired
four-size captures plus source window all viewed. Owner profile unchanged under
scratch APPDATA; frozen input/runtime/registry hashes stable. Frame10 retains
stronger hardware highlights and9boots remain original; whole-neighbor finish
and continuous motion pending. Do not loop a70ms slice as an authored gait cycle.

Ledger now21/49provisional source phases,28missing;9candidate added. No normal
selection changes or full-set acceptance. Next extend body repairs10/11/13 and
remaining gait, coordinate lower/detail continuity, then full motion/normal carry
lifecycle and original-master/cross-family consistency. Evidence: character/
james-west-carry-walk-keys-v1/local-window-v106/review.json.

Lesson: advance unrepaired source coverage while preserving both neighbor context
and partial-repair limits. Shorter original gait holds must remain original;
static render review cannot establish temporal smoothness or absence of flashing.
'''
guides=record_guides(r,section,'### James carrying lower finish reviewed through phase8')
handoff='''# Project handoff

Updated: October2,2026. Task: full James master-matched animation set and polish.

## Objective and acceptance
All required animation families, original-master art/proportions/material matching,
complete motion and normal game lifecycle; still incomplete.

## Accepted decisions and constraints
Original master authority. Reversible repairs authorized. Preserve exact head,
original pose registration and owner saves; passing checks are not art approval.

## Current state
V105 new phase9 candidate; V106 neighboring review. Ledger and five guides updated.
Normal selection unchanged. No commit, PR or export.

## Verification
47 checks, zero failures; three native captures/four sizes and source boards
reviewed. Frozen sources and real owner profile unchanged. Motion remains pending.

## Next action
Repair original phases10/11/13 and remaining28 source phases; resolve lower-detail
joins and assess full motion, original-master proportions and normal integration.

'''
for q in [folder,out]:(q/'HANDOFF.md').write_text(handoff+section,encoding='utf-8')
with (p/'HANDOFF.md').open('ab') as q:q.write(b'\n'+section.encode())
rasters=[q.relative_to(r).as_posix() for base in [folder,out] for q in base.rglob('*') if q.suffix in ['.png','.apng']]
attrs=subprocess.run(['git','check-attr','-z','filter','--stdin'],cwd=r,input=b'\0'.join(q.encode() for q in rasters)+b'\0',capture_output=True,check=True).stdout.split(b'\0')
assert len(attrs)==3*len(rasters)+1 and all(x==b'lfs' for x in attrs[2:-1:3])
print(json.dumps(dict(checks=47,failures=0,capturesReviewed=3,candidates=21,remaining=28,guides=guides,lfsRasters=len(rasters),normalChanged=False)))
