from pathlib import Path
import json,hashlib,os,uuid,time,subprocess
p=Path(__file__).resolve().parent;r=p.parents[1];out=p/'textile-triplet-v84';sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
for folder in [p/'textile-window-v79',out]:
    inputs=json.loads((folder/'inputs.json').read_bytes());assert all(sha(r/f)==v for f,v in inputs['preLaunchSha256'].items())
    native=json.loads((folder/'native-evidence.json').read_bytes());validation=json.loads((folder/'native_probe-validation.json').read_bytes())
    assert native['checks']==47 and native['failures']==0 and native['captures']==3
    assert validation['exitCode']==0 and validation['realProfileUnchanged'] and not validation['profileDelta']
spec=[(1,80,82,'e7ea54a5-1e88-445e-ac9f-81921dece9a5'),(3,81,83,'ab601da8-3f5c-4d71-86ec-bb6f782d9fc5')]
for phase,sourceversion,version,execution in spec:
    folder=p/f'detail-phase{phase}-v{sourceversion}';d=json.loads((folder/'inputs.json').read_bytes())
    for group in ['sourceSha256','referenceSha256']:assert all(sha(r/f)==v for f,v in d[group].items())
    assert sha(folder/'prompt.txt')==d['promptSha256']
    (folder/'generation.json').write_text(json.dumps(dict(state='terminal_copied',execution=execution,rawSha256=sha(folder/'raw.png'),prompt='prompt.txt',inputs='inputs.json',normalChanged=False),indent=2)+'\n')
    f=folder/'package-review.json';review=json.loads(f.read_bytes());review.update(reviewedPairedSourceBoard=True,disposition='generated_detail_source_only_whole_body_not_admitted',sourceAcceptance=False,normalChanged=False,fullGoalComplete=False,findings=['Finer matte textile/gear construction recovered from high-resolution original master.','Whole generated source not selected; only protective textile admission used in staged triplet. Native geometry acceptance not inferred from source bounds.'])
    f.write_text(json.dumps(review,indent=2)+'\n')
f=p/'interior-detail-phase2-v77/package-review.json';review=json.loads(f.read_bytes())
review.update(reviewedSourceBoards=['paired-detail-admission-review.png','enlarged-detail-admission-review.png'],disposition='rejected_partial_ankle_hardware_transfer',sourceAcceptance=False,findings=['Interior alpha protection preserved silhouette but broad calf box copied part of an ankle fitting. Textile material admission must explicitly protect hardware.','Superseded by V78textile-only upper body/thigh admission; no native review or normal selection of V77.'])
f.write_text(json.dumps(review,indent=2)+'\n')
ledger=p/'material-repair-progress.json';progress=json.loads(ledger.read_bytes())
for phase,version in [(1,82),(2,78),(3,83)]:
    folder=p/f'textile-detail-phase{phase}-v{version}';f=folder/'package-review.json';review=json.loads(f.read_bytes())
    assert all(sha(r/name)==v for name,v in review['sourceSha256'].items())
    assert review['alphaPlaneExact'] and review['kneesStrapsCalvesBootsBelow165Exact'] and review['caseGripRegionExact'] and review['pairedBodyBelow110Exact']
    review.update(reviewedPairedSourceBoard=True,reviewedEnlargedSourceBoard=(phase==2),nativeTripletIncluded=True,disposition='retain_provisional_textile_refinement',sourceAcceptance=False,normalChanged=False,fullGoalComplete=False,findings=['Selected textile interiors gain finer quilting from same-pose authored source; baseline alpha, head/shoulder region, case grip and all rows165+ exact.','Baseline itself remains provisional material/geometry candidate, not accepted original-master body.','Only selected cloth detail restored; gear/boots detail, full49motion, neighbor windows outside1/2/3 and normal lifecycle remain incomplete.'])
    f.write_text(json.dumps(review,indent=2)+'\n')
    row=progress['states'][phase];old=row['candidateSources']
    row.setdefault('supersededCandidateSources',[]).append(old)
    row.update(candidateSources={m:dict(file=(folder/f'{m}-head-protected.png').relative_to(r).as_posix(),sha256=sha(folder/f'{m}-head-protected.png')) for m in ['bare','helmet']},reviewStatus='provisional_textile_refinement_master_geometry_contact_motion_pending',sourceAcceptance=False)
assert progress['candidatePhases']==15 and len(progress['remainingSourcePhases'])==34
progress['textileRefinementPhases']=[1,2,3];ledger.write_text(json.dumps(progress,indent=2)+'\n')
for folder,label in [(p/'textile-window-v79','phase2_only_changed'),(out,'three_matching_textile_refinements')]:
    (folder/'review.json').write_text(json.dumps(dict(nativeChecks=47,nativeFailures=0,reviewedNativeCaptures=3,sourceIndices=[1,2,3],durationsMs=[40,40,40],pairedSourceSlots=6,reviewScope=label,reviewedSourceWindowBoard=(folder==out),sourceAcceptance=False,normalChanged=False,fullGoalComplete=False,continuousVisualMotionAcceptance=False,findings=['Selected quilted textile detail restored with baseline silhouette and hardware/contact protection.','Three four-size captures visually reviewed. Not continuous playback, whole49cycle, normal controller/world/Continue or original-master geometry acceptance.']),indent=2)+'\n')
section='''### James carrying textile detail restored without geometry drift — October 2, 2026

V77first phase2interior transfer kept alpha and boots but admitted part of an ankle
fitting through its calf box. Native/enlarged source boards reviewed; rejected,
no native run or installation. V78restricts authored V75detail to sleeve/torso/upper
thigh interiors:444pixels admitted,65092outside exact;443actual pixel changes.
Head/shoulder top115rows, case/front grip, full alpha, two-pixel opaque silhouette
ring and everything below165(knees/straps/calves/boots) remain exact to V69baseline.
This protects the provisional baseline, not certified original-master anatomy.

V80phase1/V81phase3 builtin sources use actual corresponding matte poses and
original high-resolution master construction; raw/prompt/hash evidence copied.
Whole generated bodies are not admitted. V82phase1/V83phase3 textile interiors
admit428/475pixels respectively with the same strict geometry/contact protection.
Two whole-source paired boards and two admitted paired boards reviewed; V78native
and enlarged source boards reviewed. Coherent fine quilting is more readable
without copying changed boot contours or whole-source case/hardware construction.
Restoring all missing gear/boot detail still remains; selected panels are partial.

V79phase2-only trial and V84three-refinement triplet each passed47native checks,
0failures, six exact paired source slots, original40/40/40ms, three four-size captures
actually reviewed per run. V84consecutive source board also viewed. Owner profile
unchanged under scratch APPDATA in both runs; frozen runtime/registry hashes stable.
No continuous artistic motion, full49gait, normal lifecycle or master acceptance.
Ledger now lists V82/V78/V83as provisional refinements for1/2/3;15/49candidate count
and34missing repairs unchanged. Older candidate sources retained in ledger history.

Lesson: opaque interior protection is not material classification; a cloth mask
can still intersect armor and create split fittings. Preserve entire hardware
regions and inspect both full figure and enlarged detail. Reuse same-pose authored
textile pixels without grading, warping or repainting, and review neighboring
frames together. Exact baseline geometry does not establish baseline fidelity.
Next remaining gait sources with original-master detail, full gear/boot fidelity,
loop boundaries, normal carry lifecycle and whole James consistency/polish.
Evidence:character/james-west-carry-walk-keys-v1/textile-triplet-v84/review.json.
'''
paths=[r/'docs/CURRENT_STATUS.md',r/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',r/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',r/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]
for f in paths:
    old=f.read_bytes();entry=section.encode()
    if entry.split(b'\n',1)[0] in old:continue
    if f.name=='CURRENT_STATUS.md':
        at=old.index('### James carrying detail authority restored and old comparison boards corrected'.encode());new=old[:at]+entry+b'\n'+old[at:]
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
folders=[p/name for name in ['interior-detail-phase2-v77','textile-detail-phase2-v78','textile-window-v79','detail-phase1-v80','detail-phase3-v81','textile-detail-phase1-v82','textile-detail-phase3-v83','textile-triplet-v84']]
for folder in folders:
    (folder/'HANDOFF.md').write_text('# Project handoff\n\nObjective: full James master-matched set and complete consistency polish; incomplete.\n\n'+section+'\nChanged: two authored neighbor detail sources, three protected textile refinements, rejected wider admission, two isolated native window reviews, helper files, ledger and five guides. Normal artwork/controller unchanged. Two generations and both native runs terminal. No commit/PR/export.\n',encoding='utf-8')
with (p/'HANDOFF.md').open('ab') as f:f.write(b'\n'+section.encode())
rasters=[f.relative_to(r).as_posix() for folder in folders for f in folder.rglob('*') if f.suffix in ['.png','.apng']]
attrs=subprocess.run(['git','check-attr','-z','filter','--stdin'],cwd=r,input=b'\0'.join(f.encode() for f in rasters)+b'\0',capture_output=True,check=True).stdout.split(b'\0')
assert all(v==b'lfs' for v in attrs[2:-1:3])
print(json.dumps(dict(nativeChecksPerRun=47,nativeRuns=2,failures=0,capturesReviewed=6,textileRefinedPhases=[1,2,3],candidatePhases=15,remaining=34,guides=5,lfsRasters=len(rasters),normalChanged=False)))
