from pathlib import Path
import json,hashlib,uuid,os
p=Path(__file__).resolve().parent;r=p.parents[1]
data=json.loads((p/'motion_rise_v6-evidence.json').read_bytes());guard=json.loads((p/'motion_rise_v6-validation.json').read_bytes());review=json.loads((p/'motion-rise-v6-review.json').read_bytes());inputs=json.loads((p/'motion_rise_v6-inputs.json').read_bytes());source=json.loads((p/'shared-case-source-review.json').read_bytes())
assert data['checks']==685 and data['failures']==0 and guard['exitCode']==0 and guard['realProfileUnchanged'] and not guard['timedOut']
assert len(inputs)==39 and all(hashlib.sha256((r/k).read_bytes()).hexdigest()==v for k,v in inputs.items())
assert review['losslessApngDecodedChecks']==180
assert json.loads((p/'midpoint-body-v1-package-evidence.json').read_bytes())['outsideEditOriginalPixelChecks']==123152
assert json.loads((p/'case-v7-package-evidence.json').read_bytes())['pairedOriginalAndExtractedPixelChecks']==1376
def atomic(path,new):
    old=path.read_bytes();temp=path.with_name(path.name+'.'+uuid.uuid4().hex+'.tmp');temp.write_bytes(new);assert path.read_bytes()==old;os.replace(temp,path)
source.update(visualReviewPending=False,reviewed='Both paired three-pose boards and enlarged boot/case details inspected. Original hardware/material retained through release/midpoint/canonical standing. Explicit case crop trims rightmost low-alpha outline; no obvious toe contamination observed in reviewed presentations. Full world motion scope separate.')
atomic(p/'shared-case-source-review.json',(json.dumps(source,indent=2)+'\n').encode())
review.update(visualReviewPending=False,continuousPlaybackWatched=False,fullHandoffAccepted=False,sampledCaseHardwareSeamResolved=True,reviewed='All90chronological source/native room pairs inspected in six boards. Original case hardware remains consistent through original release4, body-only midpoint5, canonical terminal6, idle and first departure. No duplicated case; feet retain shared root. Sampled case/terminal source seams resolved; full clip/collar/master/continuous motion and normal lifecycle admission remain incomplete.')
atomic(p/'motion-rise-v6-review.json',(json.dumps(review,indent=2)+'\n').encode())
verdict={'selected':False,'fullGoalComplete':False,'preferredStagedBank':'paired rise-v6 manifests','caseArt':'floor-case-west-v7.png','nativeChecks':685,'failures':0,'nativePairsReviewed':90,'apngRgbDurationChecks':180,'targetedInputsUnchanged':39,'ownerProfileUnchanged':True,'originalProtectedMidpointPixelChecks':123152,'originalCaseCropPixelChecks':1376,'caseCrop':[74,192,43,32],'caseCropLimitation':'Trims rightmost low-alpha case outline to avoid adjacent toe. Not a claim of complete unoccluded source extraction.','raw':'midpoint-body-generated-v1.png','prompt':'midpoint-body-prompt-v1.txt','generationMethod':'Built-in image_gen for case-removal/occluded toe only; native original-pixel protection and exact case extraction.','sampledCaseHardwareSeamResolved':True,'sampledStandingIdleBootSeamResolved':True,'fullHandoffAccepted':False,'remaining':['Bind new paired7-frame bank and actual floor-art revision/hash into staged checkpoint.','Exercise ordinary unload actor path and full native V9 return.','Normal disk/title/new-process Continue and natural scheduling; V9 collar/head turn.','All original directional masters/context/full-family and cross-family polish.']}
(p/'shared-case-acceptance.json').write_text(json.dumps(verdict,indent=2)+'\n')
section='''## James West shared original case resolves sampled hardware switch — October 2, 2026

Built-in midpoint case-removal raw/exact prompt saved; native packaging accepts
only x0..119/y192..224 floor/case/tiny toe region. All123152pixels outside edit
match paired V4 midpoints exactly, including original helmets/head/body/most boots.
V7 separate case is deterministic original cue4 crop74/192/43/32 at native position,
1376paired/extracted source pixel checks. No resampling/repaint/grade. Explicit
right boundary trims low-alpha outline to avoid adjacent toe; not an unoccluded
whole-case extraction claim. Two three-pose/foot-detail boards reviewed.

V6 paired unload keeps original0..4/exact release4, body-only midpoint5/canonical
idle-body terminal6. Shared renderer suppresses separate prop only embedded3/4,
then uses same original case through midpoint/standing/idle/first departure.
Two actual power-loss returns/both gears,45native20ms samples each:685checks0fail,
engine0/owner unchanged/39targeted prelaunch hashes unchanged.90source/native
room presentations inspected in six boards;four lossless APNGs180RGB/duration
checks pass.23.9234unit first departure, fixed case anchor/no duplicate prop.
20ms sampled updates/600msviewer terminal hold; no continuous playback claim.

Sampled case hardware/material and standing->idle boot/source seams now resolved.
Preferred staged paired riseV6/caseV7; full handoff/complete animation acceptance
remain incomplete: no full V9 clip/collar review, ordinary unload actor execution,
normal disk/title Continue, natural scheduling or full master/cross-family review.
Old source3payload/checkpoint does not bind new caseV7bytes; revise deliberately
before normal admission. Normal selection, geometry/profile unchanged.

Lesson: reuse native source case hardware instead of repeatedly repainting it.
Prop extraction must exclude adjacent toes and disclose trimmed edges. Body-only
source plus one fixed prop removes frame-dependent hardware/occlusion changes;
renderer must distinguish embedded and body-only rows by the admitted bank.
Next bank/art checkpoint binding, ordinary/full-return native evidence, normal
Continue, V9 collar/head turn and full cardinal/master/cross-family work.
Evidence:character/james-floor-case-west-v1/shared-case-acceptance.json,
motion-rise-v6-review.json,shared-case-source-review.json. Goal incomplete.
No normal selection, commit/export or full motion acceptance.
'''
for path in [r/'docs/CURRENT_STATUS.md',r/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',r/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',r/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]:
    old=path.read_bytes()
    if section.splitlines()[0].encode() not in old:atomic(path,section.encode()+b'\n'+old if path.name=='CURRENT_STATUS.md' else old+b'\n\n'+section.encode())
handoff='''# Project handoff

Updated: October 2, 2026 · Project: Brine Space · Task: James West rise/shared case

## Objective and acceptance
Full James set matching original masters/style/camera/height/proportions/matte
grade, then cross-family polish. Incomplete; staged candidate not normal-selected.

## Accepted decisions and constraints
Original0..4/exact cue4 retained. Body-only midpoint/new canonical terminal are
intentional revised endpoints; original terminal5 unchanged on disk. p128224/H148,
no individual pose normalization; owner profile/geometry/normal selection preserved.

## Current state
Preferred paired riseV6 manifests, midpoint-body-v1/native protection123152pixels,
floor-case-west-v7/native original crop1376checks, shared_case_workshop.gd/UID,
motion_rise_v6.gd/UID and39input freeze/log/guard/evidence. Six reviewed native
boards/four APNGs; shared-case-acceptance.json; five guides updated. Raw/prompt
saved. Exact case crop trims rightmost low-alpha outline to avoid adjacent toe.

## Verification
685native checks0fail/two actual prescribed returns/both gears/90reviewed source
world pairs;180APNG checks/39hashes unchanged/engine0/owner unchanged. Shared
case hardware/material and final boot/source seam resolved in sampled neighborhood.
No continuous playback/full V9/master/ordinary unload/normal Continue acceptance.

## Next action
Bind new bank and actual V7floor-art hash/revision into staged checkpoint; existing
source3payload is not sufficient. Actual ordinary/full-return native motion, normal
title/disk/new-process Continue, V9collar/head turn; full cardinal/master/cross-family
review. No commit/export; full goal active/incomplete.
'''
atomic(p/'HANDOFF.md',handoff.encode())
print('Shared original case milestone recorded;685nativechecks/90reviewed pairs; five guides updated.')
