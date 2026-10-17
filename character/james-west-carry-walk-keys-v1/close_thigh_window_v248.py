from pathlib import Path
import json,hashlib,subprocess
from milestone_notes import record_guides
p=Path(__file__).resolve().parent;r=p.parents[1];out=p/'thigh-window-v248';sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
n=json.loads((out/'native-evidence.json').read_bytes());v=json.loads((out/'native_probe-validation.json').read_bytes());frozen=json.loads((out/'inputs.json').read_bytes())
assert (n['checks'],n['failures'],n['captures'])==(86,0,6)
assert v['exitCode']==0 and not v['timedOut'] and v['realProfileUnchanged'] and not v['profileDelta']
assert all(sha(r/f)==h for f,h in frozen['preLaunchSha256'].items())
spec=[(0,244,'469baa88-698c-4358-a0a2-19367927193c'),(48,245,'36a5a875-159c-4054-9341-1ffea2f73739'),(1,246,'e5ac0c29-45df-464b-aa08-5fd3d2ee1298'),(2,247,'f9bd42b9-9d70-4b0d-92ed-9ac1b7ba183c')];folders=[];studies=[]
findings=['All four raw candidates and source detail/paired boards reviewed before native launch; six-pose combined source and two native boards now reviewed at four sizes for both gears.', 'Muted yellow seam and quilt construction more coherent across48/0/1/2, but selected47/3 still use different construction. Phase0 cloth lighter than1; selected admission masks differ by pose, not equal anatomical samples.', 'Exact alpha/rim/outside rectangles and paired body protection; no anatomical width, perspective, full49 motion or world contact acceptance. Candidates remain unselected until coherent family/grade review.']
for phase,version,execution in spec:
 folder=p/f'thigh-construction-phase{phase}-v{version}';folders.append(folder);d=json.loads((folder/'inputs.json').read_bytes())
 for group in ['sourceSha256','referenceSha256']:assert all(sha(r/f)==h for f,h in d[group].items())
 assert sha(folder/'prompt.txt')==d['promptSha256']
 review=json.loads((folder/'package-review.json').read_bytes());assert all(review[k] for k in ['alphaExact','outerOnePixelRingExact','outsideRectangleExact','pairedBodyBelow110Exact'])
 review.update(disposition='unselected_coordinated_thigh_study_master_grade_pending',reviewedSourceBoards=['thigh-detail-review.png','paired-neighbor-review.png'],rawVisuallyReviewed=True,nativeIncluded=True,findings=findings)
 (folder/'package-review.json').write_text(json.dumps(review,indent=2)+'\n',encoding='utf-8')
 (folder/'generation.json').write_text(json.dumps(dict(state='terminal_copied',execution=execution,rawSha256=sha(folder/'raw.png'),prompt='prompt.txt',referenceRoles=['edit-target','master-quilt-reference']),indent=2)+'\n',encoding='utf-8')
 studies.append(dict(phase=phase,version=version,sources={gear:dict(file=(folder/f'{gear}-head-protected.png').relative_to(r).as_posix(),sha256=sha(folder/f'{gear}-head-protected.png')) for gear in ['bare','helmet']},selected=False))
ledger=p/'material-repair-progress.json';progress=json.loads(ledger.read_bytes())
assert all('lower-material-phase0-v234' in progress['states'][0]['candidateSources'][gear]['file'] for gear in ['bare','helmet'])
progress['thighConstructionStudies']=studies;progress['nextVisualRepair']='Coordinate original-master thigh construction beyond48/0/1/2 and phase0 fabric grade; master anatomy/perspective, full49 moving contact/seam/grade, versioned normal cargo lifecycle and all-family consistency'
ledger.write_text(json.dumps(progress,indent=2)+'\n',encoding='utf-8')
(out/'review.json').write_text(json.dumps(dict(nativeChecks=86,nativeFailures=0,pairedSources=12,reviewedNativeCaptures=6,reviewedNativeBoards=['native-review-0.png','native-review-1.png'],sourceIndices=[47,48,0,1,2,3],durationsMs=[40]*6,studies=studies,findings=findings,selected=False,sourceAcceptance=False,continuousVisualMotionAcceptance=False,normalChanged=False,fullGoalComplete=False),indent=2)+'\n',encoding='utf-8')
section='''### James coordinated thigh construction loop-entry study - October3,2026

V244phase0/V245phase48/V246phase1/V247phase2 remain UNSELECTED coordinated
quilt/seam studies. Raw and source boards reviewed before native launch; V248
47/48/0..3 source board and all six paired native poses/four sizes reviewed.
86 checks/0 failures/6 captures,12sources,240ms original timing; scratch owner
profile unchanged and frozen hashes stable.441/436/448/499 interior pixels
admitted; alpha/rim/outside admission and shared lower body exact.
Same-admission medians0:54.21to62.50;48:53.53to58.50;1:60.11to55.39;
2:54.28to57.50. Quilt/seam more coherent across four poses, but phase0 lighter
than1 and selected47/3 still have different construction. No full49 grade,
perspective/anatomy, contact or normal lifecycle acceptance.
Lesson: restoring a repeated suit seam requires agreement across adjacent poses
and both ends of the loop; shared reference wording alone does not guarantee
cloth midtone continuity. Keep study sources separate from selected ledger rows.
Ledger records four unselected construction studies; selected candidates unchanged.
Next coordinate remaining thigh construction and phase0 grade, master anatomical/
perspective and world-contact review, normal cargo lifecycle and all-family polish.
Full objective active/incomplete. Evidence:
character/james-west-carry-walk-keys-v1/thigh-window-v248/review.json.
'''
guides=record_guides(r,section,'### James proportion and thigh construction comparison')
for folder in folders+[out]:(folder/'HANDOFF.md').write_text('# Project handoff\n\n'+section+'\nChanged: V245..247 references/prompts/raw/protected paired sources; V248 manifests/APNG/native probe+UID/captures; unselected study tracking and five guides.\n',encoding='utf-8')
with (p/'HANDOFF.md').open('a',encoding='utf-8') as f:f.write('\n'+section)
rasters=[f.relative_to(r).as_posix() for root in folders+[out] for f in root.rglob('*') if f.suffix.lower() in ['.png','.apng']]
attrs=subprocess.run(['git','check-attr','-z','--stdin','filter'],input=('\0'.join(rasters)+'\0').encode(),cwd=r,capture_output=True,check=True).stdout.split(b'\0');assert all(attrs[i+2]==b'lfs' for i in range(0,len(attrs)-1,3))
print(json.dumps(dict(studies=4,selected=False,checks=86,failures=0,reviewedCaptures=6,guides=guides,lfsRasters=len(rasters),goalComplete=False)))
