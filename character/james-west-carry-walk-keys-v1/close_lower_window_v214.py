from pathlib import Path
import json,hashlib,subprocess
from milestone_notes import record_guides
p=Path(__file__).resolve().parent;r=p.parents[1];out=p/'lower-window-v214';folder=p/'lower-material-phase34-v212'
sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
n=json.loads((out/'native-evidence.json').read_bytes());v=json.loads((out/'native_probe-validation.json').read_bytes());frozen=json.loads((out/'inputs.json').read_bytes());d=json.loads((folder/'inputs.json').read_bytes())
assert (n['checks'],n['failures'],n['captures'])==(73,0,5)
assert v['exitCode']==0 and not v['timedOut'] and v['realProfileUnchanged'] and not v['profileDelta']
assert all(sha(r/f)==h for f,h in frozen['preLaunchSha256'].items())
for group in ['sourceSha256','referenceSha256']:assert all(sha(r/f)==h for f,h in d[group].items())
assert sha(folder/'prompt.txt')==d['promptSha256']
findings=['V212 remake uses original phase34 target and original-master material crop, omitting the different-pose provisional finish image from generation. Raw/protected and paired source boards reviewed before native launch: diagonal toe/heel/sole alignment substantially closer to source than rejectedV210; retained provisionally.', 'Local95th172.15to168.20, median66.48to67.60. Highlight reduction modest; median slightly brighter. Not final matte grade or full moving continuity acceptance.', 'Source window and all five paired native captures/four sizes reviewed. Original35/36 brighter toe highlights; master anatomy, contact, full49 motion/grade/seam and normal lifecycle remain open.']
review=json.loads((folder/'package-review.json').read_bytes())
assert all(review[k] for k in ['alphaExact','outerOnePixelRingExact','allRowsAbove181Exact','pairedBodyBelow110Exact'])
review.update(disposition='retain_provisional_lower_finish_remake',reviewedSourceBoards=['lower-detail-review.png','paired-lower-review.png'],findings=findings,nativeIncluded=True)
(folder/'package-review.json').write_text(json.dumps(review,indent=2)+'\n',encoding='utf-8')
(folder/'generation.json').write_text(json.dumps(dict(state='terminal_copied',execution='942c3f81-f131-4bcf-82c9-e7f145f4d760',rawSha256=sha(folder/'raw.png'),prompt='prompt.txt',generationReferenceRoles=d['generationReferenceRoles'],remakeOf=d['remakeOf']),indent=2)+'\n',encoding='utf-8')
ledger=p/'material-repair-progress.json';progress=json.loads(ledger.read_bytes());row=progress['states'][34]
sources={m:dict(file=(folder/f'{m}-head-protected.png').relative_to(r).as_posix(),sha256=sha(folder/f'{m}-head-protected.png')) for m in ['bare','helmet']}
if row['candidateSources']!=sources:row.setdefault('supersededCandidateSources',[]).append(row['candidateSources'])
row.update(candidateSources=sources,sourceAcceptance=False,reviewStatus='provisional_lower_finish_master_motion_pending')
progress['lowerMaterialRefinementPhases']=sorted(set(progress['lowerMaterialRefinementPhases']+[34]))
progress['nextVisualRepair']='Coordinate lower finish35 onward; full49 moving grade/master anatomy/contact/seam, normal carry lifecycle and all-family consistency'
assert progress['candidatePhases']==49 and not progress['remainingSourcePhases']
ledger.write_text(json.dumps(progress,indent=2)+'\n',encoding='utf-8')
(out/'review.json').write_text(json.dumps(dict(nativeChecks=73,nativeFailures=0,reviewedNativeCaptures=5,reviewedNativeBoards=['native-review-0.png','native-review-1.png'],sourceIndices=[32,33,34,35,36],durationsMs=[40]*5,findings=findings,sourceAcceptance=False,continuousVisualMotionAcceptance=False,normalChanged=False,fullGoalComplete=False),indent=2)+'\n',encoding='utf-8')
section='### James carrying phase34 geometry-preserving finish remake - October3,2026\n\nV212phase34 replaces priorV145 provisionally; rejectedV210 remains unselected.\nOriginal phase34 target plus original-master material crop used for generation;\ndifferent-pose phase5 finish image omitted. Prompt describes actual diagonal boot\nlandmarks and forbids horizontal side-view substitution. Raw/protected/paired\nsource boards reviewed BEFORE native launch: toe/heel/ankle arrangement much\ncloser to original thanV210.1034 admitted/64502 outside-exact pixels; alpha/rim/\nabove181/paired lower body exact. Local95th172.15to168.20,median66.48to67.60:\nsmall upper highlight reduction, median slightly brighter; final grade still open.\n\nV214phase32..36 five40ms sources200ms:73 native checks/0 failures/5 paired\nfour-size captures. Source board and both packed native boards visually reviewed;\nscratch owner profile unchanged, frozen hashes stable.35/36 original toe highlights\nbrighter. Lesson: remove competing-pose imagery from a failed local-edit retry and\nstate actual toe/heel/sole orientation; then inspect raw and protected interior\nlandmarks separately. This helped this candidate, not a general geometry guarantee.\n\n49/49 candidate coverage unchanged; full master anatomy/proportions/contact and\ncontinuous motion/grade/seam still require acceptance. Normal selection unchanged.\nNext lower finish35 onward, normal carry lifecycle and all-family consistency.\nEvidence: character/james-west-carry-walk-keys-v1/lower-window-v214/review.json.\n'
guides=record_guides(r,section,'### James carrying phase33 finish and phase34 geometry rejection')
handoff='# Project handoff\n\nFull James master-matched animation set and cross-family polish remain active.\n\nChanged: V212phase34 remake raw/protected sources, frozen two-reference prompt\nand evidence; V214paired source/native review manifests/APNG/probe+UID/captures;\nledger34 fromV145 toV212; status/pipeline/bible/repository and installed skill notes.\n\nChecks:73 native/0/5,200ms original window; all source/native boards reviewed;\nowner profile unchanged, frozen hashes stable. Original alpha/upper body retained.\nV210 boot drift rejected; V212 arrangement closer, finish remains provisional.\n\nRemaining: lower finish35 onward; full49 moving grade/contact/master anatomy/seam;\nversioned normal carrying lifecycle and all-family consistency. No final acceptance\nor normal selection change.\n'
for f in [folder,out]:(f/'HANDOFF.md').write_text(handoff,encoding='utf-8')
with (p/'HANDOFF.md').open('a',encoding='utf-8') as f:f.write('\n'+section)
rasters=[f.relative_to(r).as_posix() for root in [folder,out] for f in root.rglob('*') if f.suffix.lower() in ['.png','.apng']]
a=subprocess.run(['git','check-attr','-z','--stdin','filter'],input=('\0'.join(rasters)+'\0').encode(),cwd=r,capture_output=True,check=True).stdout.split(b'\0');assert all(a[i+2]==b'lfs' for i in range(0,len(a)-1,3))
print(json.dumps(dict(retained=[34],checks=73,failures=0,reviewedCaptures=5,guides=guides,lfsRasters=len(rasters),goalComplete=False)))
