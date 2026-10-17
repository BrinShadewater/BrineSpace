from pathlib import Path
import json,hashlib,os,uuid,time,subprocess
p=Path(__file__).resolve().parent;r=p.parents[1];out=p/'local-stride-window-v96';sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
inputs=json.loads((out/'inputs.json').read_bytes());assert all(sha(r/f)==v for f,v in inputs['preLaunchSha256'].items())
native=json.loads((out/'native-evidence.json').read_bytes());validation=json.loads((out/'native_probe-validation.json').read_bytes())
assert native['checks']==112 and native['failures']==0 and native['captures']==8
assert validation['exitCode']==0 and validation['realProfileUnchanged'] and not validation['profileDelta']
spec=[(5,92,'71107307-c228-45b2-b843-140724e1a2fa'),(6,93,'b53ee93a-c8bc-40a7-9f82-a0375dd9942e'),(7,94,'59100390-a8fd-4255-b557-eff819051577'),(8,95,'c1c473c5-cc04-4ef2-b69c-34578de3ee8a')]
ledger=p/'material-repair-progress.json';progress=json.loads(ledger.read_bytes())
for phase,version,execution in spec:
    folder=p/f'local-material-phase{phase}-v{version}';d=json.loads((folder/'inputs.json').read_bytes())
    for group in ['sourceSha256','referenceSha256']:assert all(sha(r/f)==v for f,v in d[group].items())
    assert sha(folder/'prompt.txt')==d['promptSha256']
    (folder/'generation.json').write_text(json.dumps(dict(state='terminal_copied',execution=execution,rawSha256=sha(folder/'raw.png'),prompt='prompt.txt',inputs='inputs.json',normalChanged=False),indent=2)+'\n')
    f=folder/'package-review.json';review=json.loads(f.read_bytes())
    assert review['alphaExact'] and review['outerTwoPixelRingExact'] and review['headTop110Exact'] and review['bootsBelow200Exact'] and review['pairedBodyBelow110Exact']
    review.update(reviewedSourceBoards=['paired-local-review.png','crop-detail-review.png'],nativeWindowIncluded=True,disposition='retain_provisional_local_material_candidate',sourceAcceptance=False,normalChanged=False,fullGoalComplete=False,findings=['Fixed96crop preserves case/knee pose more closely than rejected full-body material outputs in viewed crop/source/native studies. Strict interior landmark equality not claimed.','Some hardware/seam highlights reduced with quilt construction retained; preserved original boot/edge pixels remain brighter than earlier matte phase1..3.','Phase3 is labeled material anchor, not immediate chronological predecessor. Actual neighboring1..8window reviewed separately.','No whole49gait, continuous motion, original-master anatomy/proportion or normal lifecycle acceptance.'])
    f.write_text(json.dumps(review,indent=2)+'\n')
    progress['states'][phase].update(repairCandidateAvailable=True,sourceAcceptance=False,reviewStatus='provisional_local_material_neighbor_finish_geometry_motion_pending',candidateSources={m:dict(file=(folder/f'{m}-head-protected.png').relative_to(r).as_posix(),sha256=sha(folder/f'{m}-head-protected.png')) for m in ['bare','helmet']})
progress['candidatePhases']=sum(x['repairCandidateAvailable'] for x in progress['states']);progress['remainingSourcePhases']=[x['phase'] for x in progress['states'] if not x['repairCandidateAvailable']]
assert progress['candidatePhases']==20 and len(progress['remainingSourcePhases'])==29
ledger.write_text(json.dumps(progress,indent=2)+'\n')
(out/'review.json').write_text(json.dumps(dict(nativeChecks=112,nativeFailures=0,pairedSourceSlots=16,reviewedNativeCaptures=8,reviewedNativeBoards=3,reviewedSourceWindowBoard=True,sourceIndices=list(range(1,9)),durationsMs=[40,40,40,40,40,40,40,30],windowMs=310,originalClocksRetained=True,sourceAcceptance=False,normalChanged=False,fullGoalComplete=False,continuousVisualMotionAcceptance=False,findings=['Actual eight-slot candidate sequence visually inspected at source size and paired four-size native captures.','Local material phase4..8detail/boot/edge brightness remains visibly different from phase1..3matte family. Do not certify a consistent final grade or absence of motion flashes.','Only20of49source phases have provisional candidates; current window is not full gait or authored loop boundary. APNG repeat is viewer replay.']),indent=2)+'\n')
section='''### James local carrying material repairs extended through phase8 — October 2, 2026

Four individually authored local96crop sources V92phase5/V93phase6/V94phase7/
V95phase8 use actual corresponding poses and original high-resolution textile
sample. Raw/prompt/precall hashes retained and results copied. Protected admission
preserves original alpha/two-pixel rim/headtop110 and bootsrows200+; paired body
below110exact.2601/2661/2613/2656interior pixels admitted respectively. Four crop
and four paired full-figure boards visually reviewed. Knee/case pose is preserved
more closely than rejected full-body transfers; exact interior landmarks not proven.
Source comparator phase3now correctly labeled material anchor, not predecessor.

V96actual consecutive phases1..8 uses V82/V78/V83thenV90/V92..95. Source window
board and eight paired four-size native captures in three original-resolution
boards all reviewed. Native112checks/0failures verifies16paired source slots,
original holds40/40/40/40/40/40/40/30ms,310ms total. Phase8is30ms, not40ms.
Scratch APPDATA real profile unchanged; frozen source/runtime/registry hashes stable.
APNG pixel/clock decoding does not prove continuous motion or loop acceptance;
replaying a cropped window resets the viewer, not the actual walking loop.

Some harsh seam/hardware highlights reduced while quilting stays readable. Original
boot/edge pixels preserved in local phase4..8 remain brighter/more detailed than
matte phase1..3. Neighbor grade/detail mismatch remains; no absence-of-flash claim.
Ledger20/49provisional repair candidates,29without sources; all acceptance false.
Normal artwork/controller unchanged. Four generations and engine run terminal,
workspace raws retained. Whole gait/master anatomy/proportions/normal lifecycle
and complete James cross-family consistency/polish still remain.

Lesson: label nonadjacent visual anchors as references; prove immediate joins using
actual ordered frames. Restore exact original variable holds when extending views.
Local material samples limit pose transfer but protective original regions can
retain mismatched brightness. Review protected gear/boots as part of the full
figure rather than treating exact outside pixels as overall consistency acceptance.
Next coherent boot/edge finish, remaining gait source phases, full49motion and
normal carry lifecycle; complete master detail/proportions and cross-family polish.
Evidence:character/james-west-carry-walk-keys-v1/local-stride-window-v96/review.json.
'''
paths=[r/'docs/CURRENT_STATUS.md',r/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',r/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',r/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]
for f in paths:
    old=f.read_bytes();entry=section.encode()
    if entry.split(b'\n',1)[0] in old:continue
    if f.name=='CURRENT_STATUS.md':
        at=old.index('### James carrying pose-drift rejection and local material recovery'.encode());new=old[:at]+entry+b'\n'+old[at:]
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
folders=[p/f'local-material-phase{phase}-v{version}' for phase,version,_ in spec]+[out]
for folder in folders:
    (folder/'HANDOFF.md').write_text('# Project handoff\n\nObjective: full James master-matched animation set and consistency polish; incomplete.\n\n'+section+'\nChanged: four local material source studies/protected pairs, eight-slot native review/manifests/media, generic local helpers, progress ledger and five guides. No normal art/controller change, commit/PR/export. All jobs/run terminal.\n',encoding='utf-8')
with (p/'HANDOFF.md').open('ab') as f:f.write(b'\n'+section.encode())
rasters=[f.relative_to(r).as_posix() for folder in folders for f in folder.rglob('*') if f.suffix in ['.png','.apng']]
attrs=subprocess.run(['git','check-attr','-z','filter','--stdin'],cwd=r,input=b'\0'.join(f.encode() for f in rasters)+b'\0',capture_output=True,check=True).stdout.split(b'\0')
assert all(v==b'lfs' for v in attrs[2:-1:3])
print(json.dumps(dict(nativeChecks=112,failures=0,nativeCapturesReviewed=8,candidatePhases=20,remaining=29,guides=5,lfsRasters=len(rasters),normalChanged=False)))
