from pathlib import Path
import json,hashlib,os,uuid,time,subprocess
p=Path(__file__).resolve().parent;r=p.parents[1];out=p/'extended-windows-v68';sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
inputs=json.loads((out/'inputs.json').read_bytes());assert all(sha(r/f)==v for f,v in inputs['preLaunchSha256'].items())
native=json.loads((out/'native-evidence.json').read_bytes());validation=json.loads((out/'native_probe-validation.json').read_bytes());assert native['checks']==131 and native['failures']==0 and native['captures']==9 and validation['exitCode']==0 and validation['realProfileUnchanged'] and not validation['profileDelta']
spec=[(22,64,'471bbde3-45e3-4e59-adb3-c41dfd6a4481'),(26,65,'6217345e-4702-4d0b-b012-045e3833c4f6'),(1,66,'6547cc42-203e-46e1-ba44-e972769e668a'),(47,67,'62e74494-d7be-46ec-9443-1e38db33a872')]
ledger=p/'material-repair-progress.json';progress=json.loads(ledger.read_bytes())
for phase,version,execution in spec:
    folder=p/f'master-material-phase{phase}-v{version}';d=json.loads((folder/'inputs.json').read_bytes())
    for group in ['sourceSha256','referenceSha256']:assert all(sha(r/f)==v for f,v in d[group].items())
    assert sha(folder/'prompt.txt')==d['promptSha256']
    review=json.loads((folder/'package-review.json').read_bytes());review.update(visualReviewPending=False,reviewedPairedSourceBoard=True,nativeWindowIncluded=True,sourceAcceptance=False,normalChanged=False,fullGoalComplete=False,disposition='retain_provisional_material_candidate',findings=['Matte finish consistent in reviewed middle/seam source windows; master/case/body geometry acceptance remains open.','Established top104rows and helmet cap protected; source silhouette and internal geometry remain generated candidates, not exact original master.','No normal source/controller installation or full49source motion acceptance.']);(folder/'package-review.json').write_text(json.dumps(review,indent=2)+'\n')
    (folder/'generation.json').write_text(json.dumps(dict(state='terminal_copied',execution=execution,rawSha256=sha(folder/'raw.png'),prompt='prompt.txt',inputs='inputs.json',normalChanged=False),indent=2)+'\n')
    row=progress['states'][phase];row.update(repairCandidateAvailable=True,sourceAcceptance=False,reviewStatus='provisional_material_candidate_geometry_contact_motion_pending',candidateSources={m:dict(file=(folder/(m+'-head-protected.png')).relative_to(r).as_posix(),sha256=sha(folder/(m+'-head-protected.png'))) for m in ['bare','helmet']})
progress['candidatePhases']=sum(x['repairCandidateAvailable'] for x in progress['states']);progress['remainingSourcePhases']=[x['phase'] for x in progress['states'] if not x['repairCandidateAvailable']];assert progress['candidatePhases']==11 and len(progress['remainingSourcePhases'])==38;ledger.write_text(json.dumps(progress,indent=2)+'\n')
(out/'review.json').write_text(json.dumps(dict(nativeChecks=131,nativeFailures=0,pairedSourceSlots=18,reviewedNativeCaptures=9,reviewedNativeBoards=3,reviewedSourceWindowBoards=2,middleIndices=[22,23,24,25,26],middleMs=190,seamIndices=[47,48,0,1],seamMs=160,originalClocksRetained=True,sourceAcceptance=False,normalChanged=False,fullGoalComplete=False,continuousVisualMotionAcceptance=False,findings=['Reviewed native-size source windows and nine four-size native captures show closer matte family.','Small case contour/grip/stance/internal-detail variation still requires complete source/motion/master acceptance.','Frame22hold30ms, remaining middle40ms; seam all40ms. Do not assume uniform40ms when expanding window.','Only11of49source phases have repair candidates; no complete walk or normal world/controller/Continue claim.']),indent=2)+'\n')
section='''### James carrying middle and cycle-boundary windows extended — October 2, 2026

V64phase22/V65phase26/V66phase1/V67phase47 individual builtin material edits
retain raw/prompt/precall hashes. Four paired source boards reviewed; original
head104rows and established helmet cap preserved. Expanded middle22..26 and
cycle boundary47/48/0/1 source boards reviewed at fixed pivot/H148ruler.
Native131checks/0failures includes18paired exact source slots and original clock
intervals; nine four-size native captures reviewed in three original-resolution
boards. Owner profile unchanged under scratchAPPDATA. Input/code/registry hashes
stable. APNG source pixels and clocks decode exactly; no continuous artistic
motion or normal controller/world/Continue acceptance inferred.

Original middle holds30/40/40/40/40ms total190, boundary40/40/40/40ms total160.
Do not assume every frame is40ms when extending a window. Physical pivot and
declared148ruler remain fixed; source/body/case/grip/stance/detail and sole variation
still need full master and motion judgment. All remain provisional/unselected.
material-repair-progress.json now11/49phases available,38need source repairs.
Normal artwork/controller unchanged. Four generations and engine run terminal,
workspace raws retained; no active handles or commit/PR/export.

Lesson: inspect the cyclic predecessor/successor explicitly and carry original
per-frame timings into extracted reviews; wrapping source order is not enough.
Technical source/clock checks and fixed pivots never override visible anatomy or
case differences. Next extend contiguous repairs, full49source gait/context/motion
and normal admission, then remaining James master/cross-family consistency polish.
Evidence:character/james-west-carry-walk-keys-v1/extended-windows-v68/review.json.
'''
paths=[r/'docs/CURRENT_STATUS.md',r/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',r/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',r/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]
for f in paths:
    old=f.read_bytes();entry=section.encode()
    if entry.split(b'\n',1)[0] in old:continue
    if f.name=='CURRENT_STATUS.md':
        at=old.index('### James middle carrying sleeve highlight repair'.encode());new=old[:at]+entry+b'\n'+old[at:]
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
for folder in folders:(folder/'HANDOFF.md').write_text('# Project handoff\n\nObjective: full James master-matched set and full consistency polish; incomplete.\n\n'+section+'\nChanged: four authored material-source studies, paired derivatives, middle/seam manifests/previews/native evidence/helpers, progress ledger and five guides.\n',encoding='utf-8')
with (p/'HANDOFF.md').open('ab') as f:f.write(b'\n'+section.encode())
rasters=[f.relative_to(r).as_posix() for folder in folders for f in folder.rglob('*') if f.suffix in ['.png','.apng']]
attrs=subprocess.run(['git','check-attr','-z','filter','--stdin'],cwd=r,input=b'\0'.join(f.encode() for f in rasters)+b'\0',capture_output=True,check=True).stdout.split(b'\0');assert all(v==b'lfs' for v in attrs[2:-1:3])
print(json.dumps(dict(nativeChecks=131,failures=0,reviewedNativeCaptures=9,candidatePhases=11,remainingPhases=38,guides=5,lfsRasters=len(rasters),normalChanged=False)))
