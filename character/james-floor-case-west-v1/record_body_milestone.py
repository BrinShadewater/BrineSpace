from pathlib import Path
import json,hashlib,uuid,os
from PIL import Image
p=Path(__file__).resolve().parent;r=p.parents[1]
data=json.loads((p/'motion_rise_v5-evidence.json').read_bytes());guard=json.loads((p/'motion_rise_v5-validation.json').read_bytes());review=json.loads((p/'motion-rise-v5-review.json').read_bytes());inputs=json.loads((p/'motion_rise_v5-inputs.json').read_bytes());bindings=json.loads((p/'canonical-standing-bindings.json').read_bytes())
assert data['checks']==677 and data['failures']==0 and guard['exitCode']==0 and guard['realProfileUnchanged'] and not guard['timedOut']
assert len(inputs)==32 and all(hashlib.sha256((r/k).read_bytes()).hexdigest()==v for k,v in inputs.items())
assert review['losslessApngDecodedChecks']==180
motions=[x for x in data['results'] if x.get('motion')];assert len(motions)==2 and all(x['bodySamples']>=3 and x['midpointSamples']==4 for x in motions)
for gear,b in bindings.items():
    source=Image.open(r/b['source']).convert('RGBA');body=Image.open(p/f'standing-body-v2/{gear}/000.png').convert('RGBA');registered=Image.new('RGBA',(256,256));registered.alpha_composite(source,(36,52))
    assert registered.tobytes()==body.tobytes()
def atomic(path,new):
    old=path.read_bytes();temp=path.with_name(path.name+'.'+uuid.uuid4().hex+'.tmp');temp.write_bytes(new);assert path.read_bytes()==old;os.replace(temp,path)
for name in ['standing-body-v1-review-evidence.json','standing-body-v2-review-evidence.json']:
    d=json.loads((p/name).read_bytes());d.update(visualReviewPending=False,selected=False,reviewed='Both paired four-column source/prop/registered-next-source boards inspected. V1 authored lower feet shorter than selected idle; not preferred. V2 exact registered next idle body preferred; original upper193rows exact, original lower boots intentionally revised. Static source review only.')
    atomic(p/name,(json.dumps(d,indent=2)+'\n').encode())
review.update(visualReviewPending=False,continuousPlaybackWatched=False,fullHandoffAccepted=False,reviewed='All90chronological source/native room presentations inspected in six boards. Canonical terminal body and next idle keep identical boot/body source registration; separate case already enabled at terminal, no standing->idle case switch. Embedded midpoint->terminal separate case hardware still changes; full handoff not accepted.')
atomic(p/'motion-rise-v5-review.json',(json.dumps(review,indent=2)+'\n').encode())
verdict={'selected':False,'fullGoalComplete':False,'nativeChecks':677,'failures':0,'nativePairsReviewed':90,'losslessApngRgbDurationChecks':180,'targetedInputsUnchanged':32,'ownerProfileUnchanged':True,'canonicalBodyMethod':'Exact currently selected West idle source/pivot registration, no resampling/repaint; terminal endpoint deliberately revised.','upperOriginalPixelChecks':98816,'bodyBindings':bindings,'generatedDraft':{'raw':'standing-body-only-generated-v1.png','prompt':'standing-body-only-prompt-v1.txt','method':'Built-in image_gen','preferred':False,'reason':'Generated lower boots do not match exact next idle; original idle source reuse preferred.'},'standingToIdleSourceBootSeamResolved':True,'wholeRiseCaseSeamResolved':False,'remaining':['Embedded midpoint->canonical terminal separate case hardware still changes; unify case across released source frames.','New terminal/bank/floor-art checkpoint binding; ordinary unload actor path and full native return.','Normal title/disk/new-process Continue and natural scheduling.','V9 collar/head turn; full directional masters and cross-family polish.']}
(p/'body-motion-acceptance.json').write_text(json.dumps(verdict,indent=2)+'\n')
section='''## James West canonical standing body removes final boot switch — October 2, 2026

Built-in body-only standing V1/raw/exact prompt saved, paired native package
preserves99328original upper pixels. Eight original/body/prop/next-source views
inspected; generated boots shorter than actual next idle, not preferred. Traced
next submitted source to current ordered normal West idle overrides and hashes.
V2 reuses exact184idle canvas translated36/52 into256/p128224/H148, no resampling
or grade. Both upper193rows equal original standing:98816native pixel checks.
Original lower boots differ and are deliberately revised; terminal endpoint is
NOT unchanged original5. Exact whole registered idle-body equality checked.

V5 paired unload bank keeps original0..4/release4 and V4 midpoint5, replaces
terminal6 with canonical body only. Separate case enabled at terminal6; existing
embedded source3..5 still suppress it. Native actual power-loss returns/both
gears:677checks0fail/engine0/owner unchanged,90source/world pairs reviewed in six
boards;4midpoint samples/gear, at least3terminal samples, finite completion and
23.9234world-unit departure. Four lossless APNGs180RGB/duration checks pass;
32targeted prelaunch hashes unchanged.20ms sampled updates,600msviewer hold;
no continuous browser playback or natural full scheduling acceptance claimed.

Standing->idle boot/body and case-switch seam removed in sampled review. Remaining
case hardware changes at embedded midpoint->terminal separate prop; full rise/
handoff visual acceptance still incomplete. Earlier cue/lifecycle/checkpoint
reports retain old sources/bindings; new bank/art not admitted to normal Save.
Original camera, masters, normal selection, geometry and profile unchanged.

Lesson: trace original next source before inventing hidden feet. Upper-body
identity does not prove original boots also identical; first strict right-lower
equality assertion failed and prevented package. Correctly record lower revision.
First native V2 package also failed on blank transparent RGB: Color.TRANSPARENT
is white/zero-alpha; use explicit black/zero-alpha for exact original RGBA packaging.
First failed script/log/guard retained; successful native retry verifies equality.
Prop width diagnostics must exclude adjacent boot pixels; old44px case ruler
can include toe contamination nearx117+. No cropped case extraction admitted.

Next unify case hardware through released frames/boots and bind bank/floor-art
checkpoint revision, normal action/full native motion and normal title/Continue;
V9 collar/head turn; full cardinal/master/cross-family polish. Goal incomplete.
Evidence:character/james-floor-case-west-v1/body-motion-acceptance.json,
canonical-standing-bindings.json,motion-rise-v5-review.json. No commit/export.
'''
for path in [r/'docs/CURRENT_STATUS.md',r/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',r/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',r/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]:
    old=path.read_bytes()
    if section.splitlines()[0].encode() not in old:atomic(path,section.encode()+b'\n'+old if path.name=='CURRENT_STATUS.md' else old+b'\n\n'+section.encode())
handoff='''# Project handoff

Updated: October 2, 2026 · Project: Brine Space · Task: James West rise/case seam

## Objective and acceptance
Full James set matching masters/style/camera/height/proportions/matte grade,
then full cross-family polish. Incomplete; candidates not normal-selected.

## Accepted decisions and constraints
Preserve original cue4/source0..4, owner profile/geometry/normal selection. Terminal
endpoint intentionally revised to exact registered selected idle body (V2), both
gears. Do not claim unchanged original5. Shared p128224/H148, no pose normalization.

## Current state
Body-only generatedV1/raw/prompt/native package rejected against next idle boots.
Canonical V2 source bindings/native frames preserve upper193rows exactly; reuse
full original selected idle184canvas translated36/52. Paired riseV5 manifests,
body_release_workshop.gd/UID distinguish embedded3..5/body-only6, native motion
fixture/log/32input hashes/evidence, six reviewed boards/four APNGs. Five guides
updated. New bank/floor-art checkpoint still unadmitted. No commit/export.

## Verification
98816original upper pixel checks; exact registered whole idle body equality.
677native checks0fail/two actual prescribed power-loss returns/both gears,
90reviewed source/world pairs;180APNG checks/32hashes/owner unchanged. Terminal
uses one separate case; final boot/body/case-switch seam removed in sampled view.
Earlier hardware switch at midpoint->terminal still visible. No full playback,
ordinary actor West unload, normal Continue or natural scheduling acceptance.

## Next action
Unify case across released midpoint/terminal frames; avoid boot-contaminated case
rulers. Then bind new bank/art into checkpoint, actual ordinary/full return motion,
normal title/disk/new-process Continue; V9 collar/head turn, all directions/full
master/cross-family polish. Goal active/incomplete.
'''
atomic(p/'HANDOFF.md',handoff.encode())
print('Canonical terminal body milestone recorded;677checks/90reviewed pairs; five guides updated.')
