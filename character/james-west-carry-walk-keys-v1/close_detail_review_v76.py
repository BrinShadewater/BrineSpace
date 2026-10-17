from pathlib import Path
import json,hashlib,os,uuid,time,subprocess
p=Path(__file__).resolve().parent;r=p.parents[1];out=p/'detail-window-v76';detail=p/'detail-phase2-v75';corrections=p/'comparison-corrections-v74';sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
inputs=json.loads((out/'inputs.json').read_bytes());assert all(sha(r/f)==v for f,v in inputs['preLaunchSha256'].items())
native=json.loads((out/'native-evidence.json').read_bytes());validation=json.loads((out/'native_probe-validation.json').read_bytes())
assert native['checks']==47 and native['failures']==0 and native['captures']==3
assert validation['exitCode']==0 and validation['realProfileUnchanged'] and not validation['profileDelta']
d=json.loads((detail/'inputs.json').read_bytes())
for group in ['sourceSha256','referenceSha256']:assert all(sha(r/f)==v for f,v in d[group].items())
assert sha(detail/'prompt.txt')==d['promptSha256']
(detail/'generation.json').write_text(json.dumps(dict(state='terminal_copied',execution='436152f7-0cba-4ee2-9b19-b0d2e9fdfa0a',rawSha256=sha(detail/'raw.png'),prompt='prompt.txt',inputs='inputs.json',normalChanged=False),indent=2)+'\n')
review=json.loads((detail/'package-review.json').read_bytes())
review.update(reviewedSourceBoards=['detail-and-neighbor-review.png','paired-protected-review.png'],reviewedNativeCaptures=3,disposition='retain_detail_reference_only_not_selected_phase_replacement',sourceAcceptance=False,normalChanged=False,fullGoalComplete=False,findings=['Original high-resolution master recovers finer quilting, subdued stitching, rivets and articulated metal/boot construction compared with softened V69.','New phase2 has more texture than neighboring V66phase1/V70phase3; full family must reconcile finish/detail.','Protected phase2 opaque bounds expand from[97,76,155,223]to[96,76,159,224]; boot contour and one-row sole shift prevent geometry acceptance.','Head104rows and helmet cap exact; paired body below110 exact. No complete animation, controller/context or continuous motion acceptance.'])
(detail/'package-review.json').write_text(json.dumps(review,indent=2)+'\n')
c=json.loads((corrections/'inputs.json').read_bytes())
for item in c['records']:
    phase=item['phase'];version=item['version'];folder=p/f'master-material-phase{phase}-v{version}'
    assert sha(r/item['correctedBoard'])==item['correctedSha256']
    assert sha(folder/'paired-protected-review.png')==item['historicalBoardSha256']
    assert all(sha(folder/f'{m}-head-protected.png')==v for m,v in item['sourceSha256'].items())
    f=folder/'package-review.json';row=json.loads(f.read_bytes())
    row.update(historicalComparisonCorrectionPending=False,correctedPairedBoard=item['correctedBoard'],correctedPairedBothBaselinesPixelVerified=True,correctedBareMasterComparisonReviewed=True,correctedPairedHelmetVisualReviewPending=True,historicalComparisonCorrectionEvidence='character/james-west-carry-walk-keys-v1/comparison-corrections-v74/review.json')
    f.write_text(json.dumps(row,indent=2)+'\n')
(corrections/'review.json').write_text(json.dumps(dict(correctedBoards=10,pixelVerifiedBaselineCrops=20,reviewedBareMasterComparisons=10,reviewedSummaryBoards=['master-comparisons-0.png','master-comparisons-1.png'],correctedPairedHelmetVisualReviewPending=True,originalBoardsPreserved=True,sourcePixelsUnchanged=True,sourceAcceptance=False,normalChanged=False,fullGoalComplete=False,findings=['Matching-stride corrected comparisons confirm subdued finish but simplified quilting/gear detail in several earlier candidates.','Original phase-specific material metrics and actual native windows remain separate valid evidence; historical paired before columns were wrong and now qualified.','Ten new paired boards are generated and baseline verified; actual helmet-board visual review remains pending, not inferred from bare summaries.']),indent=2)+'\n')
(out/'review.json').write_text(json.dumps(dict(nativeChecks=47,nativeFailures=0,reviewedNativeCaptures=3,pairedSourceSlots=6,sourceIndices=[1,2,3],durationsMs=[40,40,40],sourceAcceptance=False,normalChanged=False,fullGoalComplete=False,continuousVisualMotionAcceptance=False,disposition='representative_detail_route_test_not_normal_admission',findings=review['findings']),indent=2)+'\n')
ledger=p/'material-repair-progress.json';progress=json.loads(ledger.read_bytes())
assert progress['candidatePhases']==15 and len(progress['remainingSourcePhases'])==34
progress['representativeDetailStudies']=[dict(phase=2,file=(detail/'package-review.json').relative_to(r).as_posix(),disposition=review['disposition'],replacesListedCandidate=False,sourceAcceptance=False)]
ledger.write_text(json.dumps(progress,indent=2)+'\n')
section='''### James carrying detail authority restored and old comparison boards corrected — October 2, 2026

V74generates ten corrected paired comparisons using their actual original stride,
pixel-verifying20bare/helmet baseline crops. Historical boards and all source art
are unchanged. Two original-resolution bare/master summary boards covering all
ten candidates were visually reviewed. They confirm simplified quilting/gear
detail in several matte candidates. Package records point to corrected boards;
their helmet visual comparison remains pending, not inferred from bare summaries.
V73audit remains historical evidence of the defect; V74records its correction.

V75representative phase2 uses current matte V69as edit target, original high-resolution
master for surface construction, registered original master for native density,
and actual original V16phase2 for pose/construction. Builtin raw/prompt/input hashes
retained. Full square normalized once256; exact head104rows and existing helmet cap
restored. Source/detail/neighbor board and paired board reviewed. Finer quilting,
subdued stitching, rivets and articulated boot/metal details return without white
seam outlines. This is an illustrated sprite; avoid a pixel-art style conversion.

V76paired phase1/2/3 review retains original40ms holds. Native47checks/0failures,
six exact source slots, three four-size captures all viewed; owner profile unchanged
under scratch APPDATA and frozen source/runtime/registry hashes stable. This is a
representative source-detail study, not full motion or normal controller/context.
V75opaque bounds[96,76,159,224]versusV69[97,76,155,223]show boot contour expansion
and sole-row drift. New texture also differs from softened neighboring frames.
Retain V75as detail reference only; do not replace the listed phase2 candidate.
Ledger stays15/49candidate phases,34without repairs; all acceptance false.

Lesson: original high-resolution masters can clarify material construction absent
from upscaled native references. Suppressing highlights must not erase quilt seams,
fine rivets or panel structure. Describe the actual illustrated art rather than
requesting pixel-art conversion. Improved detail still does not excuse changed
silhouette, sole contact or neighbor mismatch. Keep actual pixel provenance checks
for comparison baselines. Next protect geometry while restoring coherent detail,
complete remaining gait, normal lifecycle and whole James master/cross-family polish.
Evidence:character/james-west-carry-walk-keys-v1/detail-window-v76/review.json.
'''
paths=[r/'docs/CURRENT_STATUS.md',r/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',r/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',r/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]
for f in paths:
    old=f.read_bytes();entry=section.encode()
    if entry.split(b'\n',1)[0] in old:continue
    if f.name=='CURRENT_STATUS.md':
        at=old.index('### James carrying cycle window expanded and comparison indexing corrected'.encode());new=old[:at]+entry+b'\n'+old[at:]
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
for folder in [detail,corrections,out]:
    (folder/'HANDOFF.md').write_text('# Project handoff\n\nObjective: full James master-matched set and full consistency polish; incomplete.\n\n'+section+'\nChanged: ten comparison-board corrections and evidence scope; representative detail source/protected derivatives, three-slot native study, progress annotation and five guides. Normal art/controller unchanged. Generation and native run terminal; no commit/PR/export.\n',encoding='utf-8')
with (p/'HANDOFF.md').open('ab') as f:f.write(b'\n'+section.encode())
rasters=[f.relative_to(r).as_posix() for folder in [detail,corrections,out] for f in folder.rglob('*') if f.suffix in ['.png','.apng']]+[item['correctedBoard'] for item in c['records']]
attrs=subprocess.run(['git','check-attr','-z','filter','--stdin'],cwd=r,input=b'\0'.join(f.encode() for f in rasters)+b'\0',capture_output=True,check=True).stdout.split(b'\0')
assert all(v==b'lfs' for v in attrs[2:-1:3])
print(json.dumps(dict(nativeChecks=47,failures=0,nativeCapturesReviewed=3,correctedBoards=10,baselineCropsVerified=20,bareMasterComparisonsReviewed=10,guides=5,lfsRasters=len(rasters),candidatePhases=15,normalChanged=False)))
