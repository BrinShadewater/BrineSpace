from pathlib import Path
import json,hashlib,subprocess
from milestone_notes import record_guides
p=Path(__file__).resolve().parent;r=p.parents[1];out=p/'thigh-window-v252';sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
n=json.loads((out/'native-evidence.json').read_bytes());v=json.loads((out/'native_probe-validation.json').read_bytes());frozen=json.loads((out/'inputs.json').read_bytes())
assert (n['checks'],n['failures'],n['captures'])==(86,0,6)
assert v['exitCode']==0 and not v['timedOut'] and v['realProfileUnchanged'] and not v['profileDelta']
assert all(sha(r/f)==h for f,h in frozen['preLaunchSha256'].items())
spec=[(0,249,'17fae3f9-e59a-4a0e-be9e-271025435fe2'),(47,250,'0e356245-5fb6-4cfe-ba15-0857a9289e86')];folders=[]
for phase,version,execution in spec:
 folder=p/f'thigh-construction-phase{phase}-v{version}';folders.append(folder);d=json.loads((folder/'inputs.json').read_bytes())
 for group in ['sourceSha256','referenceSha256']:assert all(sha(r/f)==h for f,h in d[group].items())
 assert sha(folder/'prompt.txt')==d['promptSha256']
 review=json.loads((folder/'package-review.json').read_bytes());assert all(review[k] for k in ['alphaExact','outerOnePixelRingExact','outsideRectangleExact','pairedBodyBelow110Exact'])
 rejected=version==249
 findings=['Phase0 correction darkens admitted cloth too strongly: median61.67to47.35 rather than requested modest reduction. Quilt contrast stronger;404 admitted pixels versus441 in prior foundation reflect changed raw opacity coverage, not preserved component geometry. Excluded BEFORE native launch; V244 remains the unselected phase0 study.'] if rejected else ['Phase47 quilt/seam closer to original master surface;387 admitted pixels,65149 outside exact. Same-admission median45.43to47.28,95th89.35to81.14.', 'Raw/detail/paired source boards reviewed before native launch. All six paired V252 native poses and source board reviewed; native phase0 uses earlierV244, not rejectedV249. Family grade and component construction acceptance remain provisional.']
 review.update(disposition='rejected_before_native_darkening_overshoot' if rejected else 'unselected_coordinated_thigh_study_master_grade_pending',reviewedSourceBoards=['thigh-detail-review.png','paired-neighbor-review.png'],rawVisuallyReviewed=True,nativeIncluded=not rejected,findings=findings)
 (folder/'package-review.json').write_text(json.dumps(review,indent=2)+'\n',encoding='utf-8')
 (folder/'generation.json').write_text(json.dumps(dict(state='terminal_copied',execution=execution,rawSha256=sha(folder/'raw.png'),prompt='prompt.txt',referenceRoles=['edit-target','master-quilt-reference']),indent=2)+'\n',encoding='utf-8')
skipped=p/'thigh-construction-phase3-v251';(skipped/'review.json').write_text(json.dumps(dict(disposition='prepared_not_generated_preserve_existing_construction',reviewedTarget='edit-target.png',reason='Current phase3 already visibly retains charcoal quilting and yellow seam. Source coordinates/treatment need motion review, but no replacement generation is justified from this evidence.',selectedUnchanged=True,nativeSource='lower-material-phase3-v237',fullGoalComplete=False),indent=2)+'\n',encoding='utf-8')
ledger=p/'material-repair-progress.json';progress=json.loads(ledger.read_bytes());folder=p/'thigh-construction-phase47-v250';study=dict(phase=47,version=250,sources={gear:dict(file=(folder/f'{gear}-head-protected.png').relative_to(r).as_posix(),sha256=sha(folder/f'{gear}-head-protected.png')) for gear in ['bare','helmet']},selected=False)
progress['thighConstructionStudies']=[s for s in progress.get('thighConstructionStudies',[]) if s['phase']!=47]+[study]
progress['nextVisualRepair']='Phase0 charcoal finish correction without darkening overshoot/raw landmark drift; coordinate remaining original-master thigh construction and moving grade, master anatomy/perspective/contact, normal cargo lifecycle and all-family consistency'
ledger.write_text(json.dumps(progress,indent=2)+'\n',encoding='utf-8')
(out/'review.json').write_text(json.dumps(dict(nativeChecks=86,nativeFailures=0,pairedSources=12,reviewedNativeCaptures=6,reviewedNativeBoards=['native-review-0.png','native-review-1.png'],sourceIndices=[47,48,0,1,2,3],durationsMs=[40]*6,sourceStudies={47:250,48:245,0:244,1:246,2:247,3:237},excludedBeforeNative=[249],findings=['Quilt/yellow seam now visible across the six reviewed poses, with original phase3 preserved. Phase0 remains lighter than1; finish and quilt contrast still require continuous moving review and master construction consistency.', 'Original outline protection and frozen source clocks verified; no anatomical/perspective, planted world contact, normal controller or full49 continuous grade acceptance.'],selected=False,sourceAcceptance=False,continuousVisualMotionAcceptance=False,normalChanged=False,fullGoalComplete=False),indent=2)+'\n',encoding='utf-8')
section='''### James thigh join extended and over-dark frame0 remake rejected - October3,2026

V250phase47 quilt/seam study retained UNSELECTED:387 admitted interior pixels,
65149 outside exact; alpha/rim/shared body exact. Median45.43to47.28,
95th89.35to81.14. V249phase0 remake REJECTED before native: requested modest
darkening overshot61.67to47.35 and raw opacity coverage changed (404 admitted
versus prior441). EarlierV244 remains phase0 study; selected sources unchanged.
PreparedV251phase3 NOT generated: existingV237 already visibly contains quilt
and yellow seam; preserve it pending actual moving construction review.

V25247/48/0..3 usesV250/V245/V244/V246/V247/V237,12sources/240ms original clocks.
86 native checks/0 failures/6 paired four-size captures; source and both native
boards reviewed. Owner profile unchanged, frozen hashes stable. Yellow seam
present across join; phase0 lighter than1 and quilt contrast vary. Not full49
moving-grade, master perspective/anatomy, world contact or normal lifecycle acceptance.
Lesson: requested percentage darkening is not a bounded colour operation; inspect
actual fabric midtones and raw registration before native admission. Preserve
already-correct construction instead of regenerating every neighbour uniformly.
Ledger adds unselectedphase47 study; no rejected candidate selected. Next repair
phase0 grade without raw landmark drift, remaining master construction/motion,
physical proportions/contact, normal cargo integration and all-family polish.
Full objective active/incomplete. Evidence:
character/james-west-carry-walk-keys-v1/thigh-window-v252/review.json.
'''
guides=record_guides(r,section,'### James coordinated thigh construction loop-entry study')
for folder in folders+[out,skipped]:(folder/'HANDOFF.md').write_text('# Project handoff\n\n'+section+'\nChanged: V249/250 raw/protected studies and disposition; V251 prepared-only disposition; V252 manifests/APNG/native probe+UID/captures; study ledger and five guides.\n',encoding='utf-8')
with (p/'HANDOFF.md').open('a',encoding='utf-8') as f:f.write('\n'+section)
rasters=[f.relative_to(r).as_posix() for root in folders+[out,skipped] for f in root.rglob('*') if f.suffix.lower() in ['.png','.apng']]
attrs=subprocess.run(['git','check-attr','-z','--stdin','filter'],input=('\0'.join(rasters)+'\0').encode(),cwd=r,capture_output=True,check=True).stdout.split(b'\0');assert all(attrs[i+2]==b'lfs' for i in range(0,len(attrs)-1,3))
print(json.dumps(dict(unselectedStudy=250,rejectedBeforeNative=249,preparedNotGenerated=251,checks=86,failures=0,reviewedCaptures=6,guides=guides,lfsRasters=len(rasters),goalComplete=False)))
