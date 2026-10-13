"""Record complete source coverage and scoped browser/native verification."""
from pathlib import Path
import json,hashlib,ast,subprocess
R=Path(__file__).resolve().parents[1];D=R/'character/bill-east-walk-master-full-v1';P=R/'character/bill-east-walk-master-pilot-v1'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
read=lambda p:json.loads(p.read_text(encoding='utf-8'))
review=read(D/'review.json');key=read(P/'keypose-review-v1/review.json')
assert all(sha(Path(p))==h for p,h in review['inputs'].items())
assert all(sha(Path(p))==h for p,h in key['selectedInputs'].items())
for rec in key['records']:assert sha(P/f"keypose-review-v1/frames/{rec['slot']:03}.png")==rec['frameSha256']
assert len(review['records'])==48 and len({r['frameSha256'] for r in review['records']})==48
native=read(D/'native/verification.json');v=read(D/'native/validation.json');assert v['passed'] and not v['inputChanges'] and not v['ownerChanges']
native.update(nativePagesReviewed=True,pageHashes={p:sha(D/p) for p in native['pages']},visualFindings='All four full station crop pages inspected. Warm face and matte quilt detail visible at station density; source sole depth preserved. Prescribed stationary phase samples do not certify natural locomotion, full2Dfoot support or continuous joins.')
(D/'native/verification.json').write_text(json.dumps(native,indent=2)+'\n',encoding='utf-8')
review.update(status='complete48_source_candidate_scoped_native_pass',visualReviewed=True,nativeTested=True,fullVisualAcceptance=False,normalAdmission=False,visualFindings='All eight whole/master/density boards and eight full raw/head boards inspected. Browser normal and quarter loops displayed all48 phases; samples0/12/24/36/47 inspected at enlarged and H82/54/27. All four native fixed crop pages inspected. Matte detail and warm face closer to original master; subtle face/collar/boot variation and phase36 width remain provisional. Browser advancement is not continuous visual cadence acceptance.',browserEvidence={'normal':'one complete loop,48 poses displayed observed in DOM','quarter':'two complete loops,48 poses displayed observed in DOM','sampleSlots':[0,12,24,36,47],'screenshots':{p:sha(D/p) for p in ['browser-phase0.png','browser-phase47.png']}},nativeChecks=v['checks'],nativeScope=native['scope'],openIssues=['Natural distance-driven locomotion and idle/walk joins not tested.','Full continuous cadence, face/collar/boot continuity and2Dsupport remain provisional.','West, cardinal, equipment, water, life/hazard, cargo and full-library acceptance remain.'])
(D/'review.json').write_text(json.dumps(review,indent=2)+'\n',encoding='utf-8')
tools=['prepare_bill_walk_remaining_sources_v1.py','prepare_bill_walk_sequence_sheet_v1.py','review_bill_walk_sequence_sheet_v1.py','build_bill_walk_consecutive_review_v1.py','prepare_bill_walk_matched_reference_retry_v2.py','prepare_bill_walk_matched_sources_v2.py','build_bill_east_walk_master_full_v1.py','publish_bill_east_walk_master_full_v1.py','prepare_bill_east_walk_world_v1.py','run_bill_east_walk_world_v1.py','prepare_bill_east_walk_world_v2.py','run_bill_east_walk_world_v2.py','publish_bill_east_walk_native_v2.py','record_bill_east_walk_full_milestone_v1.py']
for name in tools:ast.parse((R/'tools'/name).read_text(encoding='utf-8'))
pngs=list(P.rglob('*.png'))+list(D.rglob('*.png'))
result=subprocess.run(['git','check-attr','-z','--stdin','filter'],input=('\0'.join(p.relative_to(R).as_posix() for p in pngs)+'\0').encode(),cwd=R,capture_output=True,check=True);fields=result.stdout.split(b'\0');assert len(fields)==len(pngs)*3+1 and all(fields[i]==b'lfs' for i in range(2,len(fields)-1,3))
validation=read(D/'validation.json');validation.update(nativeTested=True,nativeChecks=v['checks'],nativeFailures=0,nativeSampleCount=192,nativeCapturePairs=40,nativePagesReviewed=4,pythonSyntaxFiles=len(tools),pngLfsCount=len(pngs),normalAdmission=False,fullVisualAcceptance=False)
(D/'validation.json').write_text(json.dumps(validation,indent=2)+'\n',encoding='utf-8')
note=f'''

## Bill East complete48 whole-source walking revision — October3,2026

`character/bill-east-walk-master-full-v1/` now has48 unique whole authored
walking poses, original48phase durations totaling2000ms,256canvas,pivot128224,
standingH148,stride.1796875. Normal/quarter APNGs decode96exactRGBAframes with
2000/8000ms timing. Source occupied-height deltas[-2,2], Ysole delta0all48;
whole uniform packing/lossless Yregistration only, no head stamps/local grade
or anatomical warping.49selected manifest/frame hashes and four prior preferred
keyframe hashes stable. All16 full/raw/master/density boards inspected.

The six-pose sheet trial failed scale/background/motion fidelity and was rejected
before extraction. Early individual trials4/6/7/8/10 grew or shifted anatomy;
their raws retained and replaced. Initial supporting walk image1254 versus
1024targets was an avoidable reference-size mismatch. Uniform source-derived
1024matched references plus explicit original geometry yielded useful repairs;
this combined change does not prove reference size alone caused the failures.
Six acceptable early individual poses retained with whole Yregistration. No
video provider/key used. All current48 raws saved with receipt/prompt/reference
hashes; all source-authoring jobs terminal. No partial four-hold loop substituted.

Browser normal/quarter displayed all48phases, respectively>=1/2 complete loops;
0/12/24/36/47 inspected enlarged and H82/54/27. Browser phase screenshots retained.
Advancement/static review do not establish full continuous cadence acceptance.
Native V2 actual main/Bill/default furnished ColdStore retained bare renderer:
1129checks0failures,192idle/walk/return prescribed samples,40world/source capture
pairs, four full fixed-crop pages inspected. Engine0/noERROR/WARNING,52.04s;
4707tested inputs and2931owner non-log files unchanged under scratchAPPDATA.
Current matte quilt detail/warm face survive room density; strict Ysole depth
passes. Walk phase prescribed directly for stationary source sampling because
gait advances by distance. Failed V1 retained:84fixture failures caused by
clock-only stationary walk sampling; two browser screenshots added during its
freeze were also detected. V2 sampled correctly and frozen inputs stayed stable.

This is scoped source-submission/size/depth proof, not natural locomotion,
2Dplanted feet, continuous idle/walk joins, normal admission, equipment/water,
natural job dispatch or fresh fullSave/TitleContinue. Face/collar/boot continuity
and phase36 width remain provisional. Current game loaders unchanged.14Python
syntax/{len(pngs)}PNG LFS checks passed. Full Bill objective remains incomplete;
next close natural distance-driven walking/joins, then remaining West/cardinal/
gear/water/life/hazard/cargo full-library checks. Handoff:
`character/bill-east-walk-master-full-v1/HANDOFF.md`. Previous four-key notes are
historical:44missing sources have now been authored, not yet fully accepted.
'''
paths=[R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'docs/CURRENT_STATUS.md',R/'docs/BILL_ANIMATION_CONTINUATION_2026-09-29.md']
for root in [R/'skills/brinespace-character-pipeline',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline')]:paths += [root/'references/crew-consistency.md',root/'references/source-density.md']
for path in paths:
 with path.open('a',encoding='utf-8') as f:f.write(note)
handoff='''# Project handoff

Updated: October3,2026 · Project: Brine Space · Task: Bill complete East walk

## Objective and acceptance
Finish full Bill library against original masters; user wants closeout soon.
48source East walk is a milestone, not full-library acceptance.

## Accepted decisions and constraints
Preserve whole authored poses and original gait timing. No anatomical fitting,
head stamps or local grading to conceal identity drift. Reversible work authorized;
no normal admission/commit/export performed. Preserve concurrent crew work and saves.

## Current state
Full bank, manifest, normal/quarter APNGs,16boards,index comparison, browser
screenshots and native proof in this folder. New generation/preparation/build/
review/publish/record tools tracked by review/validation. Current game unchanged.
Superseded bad sheet/individual/reference trials retained in parent study.

## Verification
48unique sources,2000ms original timing,96APNGdecoded frames exact. Height
delta[-2,2],Ysole0all48;49selected sources and4prior keyframes stable.
All16boards, five browser phases at four densities, four native pages inspected.
Normal/quarter browser advanced48poses. NativeV2 1129checks0;192prescribed
samples,40capture pairs,4707inputs/2931owner files unchanged,scratchAPPDATA.
14Python syntax and PNG LFS passed. V1 failed stationary clock-only gait probe
retained; V2 prescribes source phase directly, not natural movement.

## Next action
Test natural distance-driven East walk and idle/walk joins before normal admission.
Subtle face/collar/boot/phase36width remain provisional. Then finish remaining
West/cardinal/equipment/water/life/hazard/cargo master checks and full runtime
dispatch/fresh save/TitleContinue. Broader goal incomplete; no blocker.
'''
(D/'HANDOFF.md').write_text(handoff,encoding='utf-8')
with (P/'HANDOFF.md').open('a',encoding='utf-8') as f:f.write('\n\nOctober3 continuation: complete48 bank now in ../bill-east-walk-master-full-v1/HANDOFF.md; four-key missing44 statement above is historical. Scoped native1129checks0; natural motion/full acceptance pending.\n')
print(json.dumps({'passed':True,'completeSources':48,'nativeChecks':v['checks'],'pngLfsCount':len(pngs),'updatedRecords':8,'normalAdmission':False}))
