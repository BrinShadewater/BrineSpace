"""Record the inspected source revision; never promote it to normal runtime."""
from pathlib import Path
from PIL import Image
import json, hashlib
import numpy as np

P=Path(__file__).resolve().parent
R=P.parent.parent
sha=lambda f:hashlib.sha256(f.read_bytes()).hexdigest()
report=json.loads((P/'review.json').read_text(encoding='utf-8'))
changed=[f for f,h in report['inputSHA256'].items() if sha(R/'character'/f)!=h]
assert not changed,changed
a=np.array(Image.open(P/'sources/lift-head-hands-v3.png').convert('RGBA'))
b=np.array(Image.open(P/'sources/lift-head-v4.png').convert('RGBA'))
assert a.shape==b.shape
different=np.any(a!=b,axis=2)
outside=np.ones(different.shape,dtype=bool)
outside[100:410,280:550]=False
def bounds(im):
    y,x=np.where(im[:,:,3]>180)
    return [int(x.min()),int(y.min()),int(x.max()+1),int(y.max()+1)]
edit_diagnostic=dict(comparison='V9 hands v3 to head v4, same raw canvas',
    headDiagnosticROI=[280,100,550,410],
    rgbaPixelsChanged=int(different.sum()),
    rgbaPixelsChangedOutsideDiagnosticROI=int((different&outside).sum()),
    alphaByteExact=bool(np.array_equal(a[:,:,3],b[:,:,3])),
    opaqueMaskExact=bool(np.array_equal(a[:,:,3]>180,b[:,:,3]>180)),
    priorOpaqueBounds=bounds(a),selectedOpaqueBounds=bounds(b),
    scope='Diagnostic ROI is not a semantic protection mask. Head-only prompt did not guarantee unchanged body; selected raw is a whole-source replacement.')
(P/'source-edit-diagnostic.json').write_text(json.dumps(edit_diagnostic,indent=2)+'\n',encoding='utf-8')
head_audit=json.loads((P/'head-audit.json').read_text(encoding='utf-8'))
assert all(not row['componentTouchesROIEdge'] for row in head_audit)
master=Image.open(R/'character/crew-side-masters-v1/bill-side-master-01.png').convert('RGBA')
assert master.crop((960,5,1140,175)).tobytes()==Image.open(P/'sources/master-head-reference.png').convert('RGBA').tobytes()
report.update(generationMode='built-in image_gen edit',
    generations=[dict(id='exec-498f9934-06ea-4522-ad50-cfcee3a6148f',raw='sources/lift-head-hands-v3.png',prompt='sources/lift-head-hands-prompt-v3.txt',references=['../bill-land-water-west-v8/sources/lift-master-v2.png','../crew-side-masters-v1/bill-side-master-01.png'],status='hands improved; head remains broad'),
                 dict(id='exec-1aa8b59e-0856-41e6-89f6-97e67ef0980d',raw='sources/lift-head-v4.png',prompt='sources/lift-head-prompt-v4.txt',references=['sources/lift-head-hands-v3.png','sources/master-head-reference.png'],status='selected provisional source')],
    exactMasterHeadCrop=[960,5,1140,175],
    frozenInputsStable=len(report['inputSHA256']),
    headProxyAudit=head_audit,sourceEditDiagnostic=edit_diagnostic,
    candidateStatus='provisional_head_hands_improvement',
    registrationScope='Preceding V8 whole-source translation [67,122] retained at148/956 density. New crown [125,148] and support255 measured; not support or posed-height fitting, nor floor-contact proof.',
    visualAcceptance='Selected raw, common-density four-head audit, original/push-off/V8/V9 registered comparison, complete fourteen-pose bare/helmet board, seven neck pairs and paused browser levelling reviewed. Smaller head closer to original and two distinct gloves/wrists readable. Canonical helmet/collar connected in inspected pose. Sequence still has grade and neighboring arm-reach differences; complete anatomy/camera/material/contact/clearance/continuous-motion acceptance remains pending.',
    browserEvidence=dict(file='browser-review.png',poseIndex=4,timeMs=270,scope='Paused source presentation only; not continuous or native game review.'),
    nativeAcceptance=False,normalSelected=False)
report['sourcePromptSHA256']={f.name:sha(f) for f in (P/'sources').iterdir() if f.is_file()}
(P/'review.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
heading='## Bill West levelling head and two-hand source refinement — October 2, 2026'
note=f'''{heading}

Sibling character/bill-land-water-west-v9 selects head-v4 provisional source for pose4 both gears. Hands-v3 separates two gloves/wrists but head remains broad; head-v4 uses exact original master crop [960,5,1140,175] as second reference. Both built-in imagegen raw/exact prompts/ordered references retained. Same original148/956 drawing density and precedingV8 whole-source translation[67,122], no new crown/support/posed-height fit. New crown[125,148], support255 measured, not floor-contact proof.

Common raw-density brown hair/face proxy: original137x141, V8 182x190, hands-v3 168x184, selected head-v4 141x151. All bounded components clear ROI edges. Earlier V8 height172 came from a truncated ROI and is superseded by190; do not compare truncated components. This is a semantic colour proxy, not whole anatomical acceptance. Head-only prompt still changes {edit_diagnostic['rgbaPixelsChangedOutsideDiagnosticROI']} RGBApixels outside diagnostic head ROI; alpha exact={edit_diagnostic['alphaByteExact']}. Treat as whole-source replacement, not protected-body generation.

Twelve other decoded poses exactV8;14APNGframes/holds exact500ms/loop1. Five canonical40x40helmet fits at native scale1/rotation0 protect body outside bounded fitting mask/foreground. {len(report['inputSHA256'])} frozen inputs stable. Selected raw/master/head audit/registered comparison/full paired board/all neck pairs/paused browser pose4 at270ms inspected. Head closer and two hands readable; helmet/collar connected in inspected pose. Sequence grade, neighboring arm reach and full master/camera/contact/clearance/moving continuity remain pending. No native/profile interval or normal selection; prior WestV4 native/resume/Continue does not coverV5..V9.

Lesson: use an exact original head reference at common source density when whole-master edits leave head enlargement. Keep previous whole-source translation so a local head reduction does not automatically shift the entire body to restore its old crown. Guard semantic measurements against ROI-edge truncation; quantify edits outside diagnostic regions and do not infer protected pixels from prompt wording. Canonical helmet fitting cannot certify underlying anatomy or chronology.

Next near-prone source and full West early/late grade/anatomical reach review; independent exit context/rise, North/South master repairs; refreshed native contact/motion/resume, normal admission/cargo lifecycle and full-library consistency/polish. Full Bill goal active/incomplete.
'''
files=[R/'docs/CURRENT_STATUS.md',R/'docs/BILL_ANIMATION_CONTINUATION_2026-09-29.md',R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]
for f in files:
    with f.open('rb') as stream:
        stream.seek(max(0,f.stat().st_size-65536))
        tail=stream.read().decode('utf-8',errors='replace')
    if heading not in tail:
        with f.open('a',encoding='utf-8') as stream:stream.write('\n\n'+note)
(P/'HANDOFF.md').write_text('''# Project handoff

Updated: October 2, 2026 · Project: Brine Space · Task: Full Bill animations

## Objective and acceptance
Complete master-consistent animation set, then cross-family consistency/polish and normal game integration. Full scope remains active/incomplete.

## Accepted decisions and constraints
Original directional masters and fixed drawing density; reversible siblings. Preserve normal selections, owner data and concurrent work. No per-pose height or limb fitting.

## Current state
West entryV9 levelling4 smaller-head/two-hand source selected provisionally in both gears. prepare/build, two raws/exact prompts/master crop, head audit/edit diagnostic, manifests/frames/APNGs, paired/master/neck/browser review and six guidance records updated.

## Verification
12 unaffected decoded poses exactV8;14APNGframes/holds exact500ms/loop1. Five native-size canonical helmet body/foreground protection fits. Frozen inputs checked stable. Master head crop exact; raw/master/common-scale/paired/neck and paused source browser inspected. Head proxy141x151 versus original137x141, not complete anatomy acceptance. Source edit changes body pixels; no pixel-protection claim. No new native/profile interval or normal selection.

## Next action
Near-prone source and complete West chronological grade/anatomical reach; independent exit context/rise, North/South master repairs; refreshed native motion/contact/resume, normal admission/cargo lifecycle and full-library polish.
''',encoding='utf-8')
print(json.dumps(dict(frozenInputs=len(report['inputSHA256']),unchangedPoses=12,decodedFrames=14,guidanceFiles=6,editDiagnostic=edit_diagnostic)))
