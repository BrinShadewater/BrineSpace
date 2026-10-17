from pathlib import Path
from PIL import Image
import numpy as np
import json,hashlib,os,uuid,time,subprocess
p=Path(__file__).resolve().parent;r=p.parents[1];out=p/'cycle-window-v73'
sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
inputs=json.loads((out/'inputs.json').read_bytes())
assert all(sha(r/f)==v for f,v in inputs['preLaunchSha256'].items())
native=json.loads((out/'native-evidence.json').read_bytes());validation=json.loads((out/'native_probe-validation.json').read_bytes())
assert native['checks']==112 and native['failures']==0 and native['captures']==8
assert validation['exitCode']==0 and validation['realProfileUnchanged'] and not validation['profileDelta']
spec=[(2,69,'a572faa3-aafe-4c6e-ab51-5b287a66b916'),(3,70,'62dfd940-f43b-477e-8506-2cbe91b0f5a6'),(45,71,'a0e2e5ff-61f3-4b93-bd4e-fb45a857351a'),(46,72,'0e92bd8e-89c6-45b4-984f-2f1bef9d799a')]
ledger=p/'material-repair-progress.json';progress=json.loads(ledger.read_bytes())
for phase,version,execution in spec:
    folder=p/f'master-material-phase{phase}-v{version}';d=json.loads((folder/'inputs.json').read_bytes())
    for group in ['sourceSha256','referenceSha256']:assert all(sha(r/f)==v for f,v in d[group].items())
    assert sha(folder/'prompt.txt')==d['promptSha256']
    target=Image.open(p/f'master-head-review-v16/bare-{phase:03d}.png').convert('RGBA')
    before=Image.new('RGBA',(256,256),(47,58,63,255));before.alpha_composite(target)
    board=Image.open(folder/'paired-protected-review.png').convert('RGBA')
    assert np.array_equal(np.asarray(before),np.asarray(board.crop((0,24,256,280))))
    review=json.loads((folder/'package-review.json').read_bytes())
    review.update(visualReviewPending=False,reviewedPairedSourceBoard=True,pairedBeforeColumnPhase=phase,nativeWindowIncluded=True,sourceAcceptance=False,normalChanged=False,fullGoalComplete=False,disposition='retain_provisional_material_candidate',findings=['Reduced shiny stitching/hardware; softer detail than original master remains an unresolved fidelity issue.','Head top104rows and existing helmet cap protected; geometry/contact/case/sole variation still provisional.','Corrected comparison helper before-column indexing; actual matching original stride reviewed.','No full49 motion or normal installation acceptance.'])
    (folder/'package-review.json').write_text(json.dumps(review,indent=2)+'\n')
    (folder/'generation.json').write_text(json.dumps(dict(state='terminal_copied',execution=execution,rawSha256=sha(folder/'raw.png'),prompt='prompt.txt',inputs='inputs.json',normalChanged=False),indent=2)+'\n')
    row=progress['states'][phase]
    row.update(repairCandidateAvailable=True,sourceAcceptance=False,reviewStatus='provisional_material_candidate_geometry_contact_motion_pending',candidateSources={m:dict(file=(folder/(m+'-head-protected.png')).relative_to(r).as_posix(),sha256=sha(folder/(m+'-head-protected.png'))) for m in ['bare','helmet']})
progress['candidatePhases']=sum(x['repairCandidateAvailable'] for x in progress['states'])
progress['remainingSourcePhases']=[x['phase'] for x in progress['states'] if not x['repairCandidateAvailable']]
assert progress['candidatePhases']==15 and len(progress['remainingSourcePhases'])==34
ledger.write_text(json.dumps(progress,indent=2)+'\n')
# Audit earlier paired comparisons without rewriting historical source artifacts.
affected=[]
for phase,version in [(1,66),(12,51),(22,64),(23,58),(24,52),(25,59),(26,65),(36,53),(47,67),(48,55)]:
    folder=p/f'master-material-phase{phase}-v{version}'
    board=Image.open(folder/'paired-protected-review.png').convert('RGBA')
    entry=Image.new('RGBA',(256,256),(47,58,63,255));entry.alpha_composite(Image.open(p/'master-head-review-v16/bare-000.png').convert('RGBA'))
    wrong=bool(np.array_equal(np.asarray(entry),np.asarray(board.crop((0,24,256,280)))))
    assert wrong
    file=folder/'package-review.json';review=json.loads(file.read_bytes())
    review.update(historicalPairedBeforeColumnPhase=0,intendedPairedBeforeColumnPhase=phase,historicalComparisonCorrectionPending=True,historicalReviewScopeCorrection='Before column was original phase0, not this stride; candidate/reference columns and separate phase-specific metrics remain valid. Corrected stride comparison remains pending.')
    file.write_text(json.dumps(review,indent=2)+'\n')
    affected.append(dict(phase=phase,version=version,file=file.relative_to(r).as_posix(),beforeColumnWasPhase0=True,correctedComparisonPending=True))
(out/'historical-comparison-audit.json').write_text(json.dumps(dict(affected=affected,helperFixed=True,sourcePixelsChanged=False,scope='Ten earlier paired boards verified to show phase0 baseline; preserve historical evidence and qualify its comparison scope.'),indent=2)+'\n')
(out/'review.json').write_text(json.dumps(dict(nativeChecks=112,nativeFailures=0,pairedSourceSlots=16,reviewedNativeCaptures=8,reviewedNativeBoards=3,reviewedSourceWindowBoards=1,seamIndices=[45,46,47,48,0,1,2,3],seamMs=320,originalClocksRetained=True,sourceAcceptance=False,normalChanged=False,fullGoalComplete=False,continuousVisualMotionAcceptance=False,reviewedNewPairedBoards=4,originalMasterComparisonReviewed='master-material-phase2-v69/native-material-comparison.png',historicalComparisonCorrectionsPending=10,findings=['Finish subdued but several new frames simplify stitching/gear texture compared with original detailed master. Do not certify full master match.','Whole generated body/case geometry and sole-row differences remain provisional.','New matching-stride before comparisons corrected and pixel-verified. Ten earlier comparisons have been explicitly qualified.','15of49source phases now have candidates,34remain; no whole49 walk or normal controller/context claim.']),indent=2)+'\n')
section='''### James carrying cycle window expanded and comparison indexing corrected — October 2, 2026

Four individual material candidates V69phase2/V70phase3/V71phase45/V72phase46
are copied with raw/prompt/input hashes. Exact existing head104rows and helmet cap
are preserved. Four corrected paired source boards, original-master comparison
for phase2, full45/46/47/48/0/1/2/3 source board and all eight four-size native
captures were visually reviewed. Native112checks/0failures verifies16paired source
slots and original40ms holds,320ms window. Scratch APPDATA owner profile unchanged;
frozen runtime/registry/source hashes stable. No normal installation or full motion
acceptance. APNG pixel/clock decoding is separate from continuous visual motion.

Finish is less shiny but some new stitching and hardware detail is softer than the
original master. Keep all candidates provisional; fixed heads/pivots/declared148
ruler do not prove anatomy, case contact or master detail. Phase45 sole extends
one row compared with source; geometry and complete motion need judgment.
Progress ledger15/49candidate phases,34still require sources, all acceptance false.

Found and fixed package_material_phase.py: its constructed paired-board filename
kept '-000.png' even when literal source paths were correctly phase-specific.
New four before columns now pixel-verified against actual corresponding strides.
Audit confirms ten historical paired boards used phase0 as their before column;
their package records now qualify that comparison and mark correction pending.
Historical source/native-window evidence remains preserved; no retroactive claim
that those boards reviewed the intended before pose. Source art was unaffected.

Lesson: verify review-media provenance as rigorously as runtime sources. Dynamic
filenames in helper templates can escape literal replacements. Add actual-pixel
baseline checks, and judge suppressed highlights against retained fine detail,
not only against brightness. Next correct historical comparisons, resolve master
detail softness, extend full49gait, then normal lifecycle and cross-family polish.
Evidence:character/james-west-carry-walk-keys-v1/cycle-window-v73/review.json.
'''
paths=[r/'docs/CURRENT_STATUS.md',r/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',r/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',r/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]
for f in paths:
    old=f.read_bytes();entry=section.encode()
    if entry.split(b'\n',1)[0] in old:continue
    if f.name=='CURRENT_STATUS.md':
        at=old.index('### James carrying middle and cycle-boundary windows extended'.encode());new=old[:at]+entry+b'\n'+old[at:]
    else:new=old+b'\n'+entry
    tmp=f.with_name(f.name+'.'+uuid.uuid4().hex+'.tmp');tmp.write_bytes(new)
    try:
        for attempt in range(5):
            assert f.read_bytes()==old
            try:os.replace(tmp,f);break
            except PermissionError:
                if attempt==4:raise
                time.sleep(1)
    finally:
        if tmp.exists():tmp.unlink()
folders=[out]+[p/f'master-material-phase{phase}-v{version}' for phase,version,_ in spec]
for folder in folders:
    (folder/'HANDOFF.md').write_text('# Project handoff\n\nObjective: full James master-matched animation set and consistency polish; incomplete.\n\n'+section+'\nChanged: four source studies, protected pairs, eight-slot native fixture/manifests/reviews, helper indexing fix, historical evidence qualifications, progress ledger and five guides. No normal art/runtime change, commit/PR/export. All jobs and native run terminal.\n',encoding='utf-8')
with (p/'HANDOFF.md').open('ab') as f:f.write(b'\n'+section.encode())
rasters=[f.relative_to(r).as_posix() for folder in folders for f in folder.rglob('*') if f.suffix in ['.png','.apng']]
attrs=subprocess.run(['git','check-attr','-z','filter','--stdin'],cwd=r,input=b'\0'.join(f.encode() for f in rasters)+b'\0',capture_output=True,check=True).stdout.split(b'\0')
assert all(v==b'lfs' for v in attrs[2:-1:3])
print(json.dumps(dict(nativeChecks=112,failures=0,reviewedNativeCaptures=8,candidatePhases=15,remainingPhases=34,historicalComparisonsQualified=len(affected),guides=5,lfsRasters=len(rasters),normalChanged=False)))
