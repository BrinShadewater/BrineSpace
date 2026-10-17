from pathlib import Path
import json,hashlib,os,uuid,time,subprocess
p=Path(__file__).resolve().parent;r=p.parents[1];out=p/'local-detail-window-v91';local=p/'local-material-phase4-v90';sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
for folder,checks,captures in [(p/'extended-detail-window-v89',99,7),(out,60,4)]:
    inputs=json.loads((folder/'inputs.json').read_bytes());assert all(sha(r/f)==v for f,v in inputs['preLaunchSha256'].items())
    native=json.loads((folder/'native-evidence.json').read_bytes());validation=json.loads((folder/'native_probe-validation.json').read_bytes())
    assert native['checks']==checks and native['failures']==0 and native['captures']==captures
    assert validation['exitCode']==0 and validation['realProfileUnchanged'] and not validation['profileDelta']
spec=[(4,85,'ccfc7e61-e296-4497-98f7-d9d573bc4a0d'),(5,86,'19662a5a-347a-47b9-8dbe-b299d11e2d4b'),(6,87,'18eeb817-e96d-481d-b07f-f6f8a191c9dd'),(7,88,'e9b978ed-36c0-4153-b2dd-5baa477aa30c')]
for phase,version,execution in spec+[(4,90,'54a58b80-ad81-459f-94cc-6f31665eeca6')]:
    folder=p/(f'master-detail-phase{phase}-v{version}' if version!=90 else 'local-material-phase4-v90')
    d=json.loads((folder/'inputs.json').read_bytes())
    for group in ['sourceSha256','referenceSha256']:assert all(sha(r/f)==v for f,v in d[group].items())
    assert sha(folder/'prompt.txt')==d['promptSha256']
    (folder/'generation.json').write_text(json.dumps(dict(state='terminal_copied',execution=execution,rawSha256=sha(folder/'raw.png'),prompt='prompt.txt',inputs='inputs.json',normalChanged=False),indent=2)+'\n')
    f=folder/'package-review.json';review=json.loads(f.read_bytes())
    if version!=90:
        rejected=json.loads((folder/'registration-rejection.json').read_bytes())
        assert rejected['status']=='rejected_before_protected_derivative_packaging'
        review.update(disposition='rejected_internal_pose_and_registration_drift',reviewedSourceBoards=['master-comparison.png'],sourceAcceptance=False,normalChanged=False,fullGoalComplete=False,findings=['Raw same-pose output moves crown6..12rows and soles13..22rows; knees/case/articulation shift visibly.','Alpha/outer-ring protection preserves a footprint while creating internally incoherent anatomy. Reject all protected derivatives too.','Native99source/clock checks remain technical evidence only; generated art rejected despite zero failures.','New pre-packaging crown/sole drift guard independently rejects this stored raw. Earlier failed study derivatives remain preserved as historical evidence.'])
    else:
        review.update(disposition='retain_provisional_local_material_candidate',reviewedSourceBoards=['paired-local-review.png','crop-detail-review.png'],sourceAcceptance=False,normalChanged=False,fullGoalComplete=False,findings=['Fixed96crop/material-only master sample avoids full-figure standing-pose transfer. Knee/case positioning remains close in reviewed source/native poses.','Original alpha/rim/top110head and rows200+boots exact; interior material pixels remain a generated candidate, not strict landmark equality.','Seam finish somewhat reduced but original boot/edge highlights remain brighter than preceding V83phase3. Neighbor material transition unresolved.','Full49gait, original-master anatomy/proportions, normal lifecycle and continuous visual motion remain open.'])
    f.write_text(json.dumps(review,indent=2)+'\n')
(p/'extended-detail-window-v89/review.json').write_text(json.dumps(dict(nativeChecks=99,nativeFailures=0,capturesProduced=7,nativeCapturesVisuallyReviewed=0,reviewedSourceWindowBoard=True,reviewedMasterComparisonBoards=4,sourceAcceptance=False,normalChanged=False,fullGoalComplete=False,disposition='rejected_art_despite_technical_source_clock_pass',findings=['Raw registration and internal landmarks drift; protected alpha hides footprint drift while leaving fragmented body/case detail.','Do not infer motion/master quality from99checks or fixed silhouette. Source rejection made additional native visual review unnecessary.']),indent=2)+'\n')
(out/'review.json').write_text(json.dumps(dict(nativeChecks=60,nativeFailures=0,pairedSourceSlots=8,reviewedNativeCaptures=4,reviewedSourceWindowBoard=True,sourceIndices=[1,2,3,4],durationsMs=[40,40,40,40],sourceAcceptance=False,normalChanged=False,fullGoalComplete=False,continuousVisualMotionAcceptance=False,findings=['Local phase4 crop preserves actual pose more successfully than rejected full-body outputs.','Phase4 still brighter at boots/seams than prior matte phase3; preserve as provisional repair candidate, not whole-family finish acceptance.']),indent=2)+'\n')
ledger=p/'material-repair-progress.json';progress=json.loads(ledger.read_bytes());row=progress['states'][4]
row.update(repairCandidateAvailable=True,sourceAcceptance=False,reviewStatus='provisional_local_material_neighbor_finish_geometry_motion_pending',candidateSources={m:dict(file=(local/f'{m}-head-protected.png').relative_to(r).as_posix(),sha256=sha(local/f'{m}-head-protected.png')) for m in ['bare','helmet']})
progress['candidatePhases']=sum(x['repairCandidateAvailable'] for x in progress['states']);progress['remainingSourcePhases']=[x['phase'] for x in progress['states'] if not x['repairCandidateAvailable']]
assert progress['candidatePhases']==16 and len(progress['remainingSourcePhases'])==33
progress.setdefault('rejectedSourceStudies',[]).extend([dict(phase=phase,version=version,file=f'master-detail-phase{phase}-v{version}/package-review.json',reason='internal_pose_and_registration_drift') for phase,version,_ in spec])
ledger.write_text(json.dumps(progress,indent=2)+'\n')
section='''### James carrying pose-drift rejection and local material recovery — October 2, 2026

V85..88individual phase4..7 full-body material/detail outputs are REJECTED.
Raw crowns shift6..12native rows and soles13..22rows; knees/case/body articulation
move. Full-canvas normalization preserves those failures. Original alpha/two-pixel
rim and old head restoration hide silhouette drift while leaving incoherent internal
landmarks. Four master comparison boards and seven-slot V89source board reviewed.
V89native99checks/0failures proves14paired sources/clocks only; seven captures
produced but not visually reviewed because source rejection already established.
No adoption. Raw/prompt/input evidence and rejected derivatives remain preserved.

Added pre-packaging same-pose crown/sole drift guard to package_master_detail_stride:
more than3native-row discrepancy rejects before protected derivatives are produced.
Replayed all four stored raw sources: all explicitly rejected as expected. This
is an early diagnostic rejection, not a fidelity acceptance gate. Existing V89
failed derivatives predate guard and remain historical evidence, not valid sources.

V90phase4local96square crop uses actual source and a cropped original high-resolution
textile sample as material authority, avoiding the master's standing silhouette.
Raw/prompt/source hashes copied. Normalized once96at its original crop coordinates;
2547interior pixels admitted,62989outside exact. Original alpha/rim/headtop110 and
bootsrows200+ protected; paired body below110exact. Source whole-figure/crop boards
reviewed: knees/case pose preserved more closely, no strict interior landmark claim.
Some highlights reduced; boot/edge finish still brighter than preceding V83phase3.

V91phase1/2/3/4 window retains40/40/40/40ms. Native60checks/0failures, eight exact
paired sources, four four-size captures and consecutive source board all reviewed.
Owner profile unchanged with scratch APPDATA; frozen source/runtime/registry hashes
stable in V89/V91. No continuous artistic motion, full49gait or normal integration.
Ledger16/49provisional repair candidates,33without repairs. Rejected phase5..7do
not count. Normal artwork/controller unchanged; full James set/polish incomplete.

Lesson: full-reference figures can transfer their pose/registration despite strict
material-only prompts. Alpha projection cannot repair shifted internal anatomy;
reject source registration before packaging. Use actual local pose plus material
sample for local finish edits, but still review knee/case geometry, joins and gear
brightness. Exact outside pixels protect a provisional baseline, not master fidelity.
Next coherent phase4neighbor finish, remaining gait sources and whole49motion,
normal lifecycle, complete original-master detail/proportions and cross-family polish.
Evidence:character/james-west-carry-walk-keys-v1/local-detail-window-v91/review.json.
'''
paths=[r/'docs/CURRENT_STATUS.md',r/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',r/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',r/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]
for f in paths:
    old=f.read_bytes();entry=section.encode()
    if entry.split(b'\n',1)[0] in old:continue
    if f.name=='CURRENT_STATUS.md':
        at=old.index('### James carrying textile detail restored without geometry drift'.encode());new=old[:at]+entry+b'\n'+old[at:]
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
folders=[p/f'master-detail-phase{phase}-v{version}' for phase,version,_ in spec]+[p/'extended-detail-window-v89',local,out]
for folder in folders:
    (folder/'HANDOFF.md').write_text('# Project handoff\n\nObjective: full James master-matched animations and consistency polish; incomplete.\n\n'+section+'\nChanged: four rejected source studies and early diagnostic guard; local material source/protected pair, two isolated native windows, ledger and five guides. All five generations/native runs terminal; copied raws retained. No normal art/controller change, commit/PR/export.\n',encoding='utf-8')
with (p/'HANDOFF.md').open('ab') as f:f.write(b'\n'+section.encode())
rasters=[f.relative_to(r).as_posix() for folder in folders for f in folder.rglob('*') if f.suffix in ['.png','.apng']]
attrs=subprocess.run(['git','check-attr','-z','filter','--stdin'],cwd=r,input=b'\0'.join(f.encode() for f in rasters)+b'\0',capture_output=True,check=True).stdout.split(b'\0')
assert all(v==b'lfs' for v in attrs[2:-1:3])
print(json.dumps(dict(rejectedWholeSources=4,retainedLocalCandidate=1,nativeLocalChecks=60,failures=0,nativeCapturesReviewed=4,candidatePhases=16,remaining=33,guides=5,lfsRasters=len(rasters),normalChanged=False)))
