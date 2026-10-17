from pathlib import Path
from PIL import Image
import numpy as np,json,hashlib
P=Path(__file__).resolve().parent;R=P.parent.parent
report=json.loads((P/'review.json').read_text(encoding='utf-8'))
changed=[f for f,h in report['inputSHA256'].items() if hashlib.sha256((R/'character'/f).read_bytes()).hexdigest()!=h];assert not changed,changed
a=np.array(Image.open(P/'sources/crouch-master-v2.png').convert('RGBA'));b=np.array(Image.open(P/'sources/crouch-matte-v3.png').convert('RGBA'));assert a.shape==b.shape
report.update(generationMode='built-in image_gen edit',generations=['exec-d17c090e-6582-483a-b757-0ae3f6adc46a','exec-3927ecbf-a486-4e42-874d-92aa22c8e225','exec-2176a06d-8857-4593-b21b-40bf7bd37fe9'],rejectedGeneration='exec-d17c090e-6582-483a-b757-0ae3f6adc46a',frozenInputsStable=len(report['inputSHA256']))
report['materialEditLimits']={'alphaExact':bool(np.array_equal(a[:,:,3],b[:,:,3])),'opaqueMaskExact':bool(np.array_equal(a[:,:,3]>180,b[:,:,3]>180)),'rawOpaqueBoundsBefore':Image.fromarray(a[:,:,3]).point(lambda p:255 if p>180 else 0).getbbox(),'rawOpaqueBoundsAfter':Image.fromarray(b[:,:,3]).point(lambda p:255 if p>180 else 0).getbbox(),'scope':'Whole-source replacement; material instruction does not guarantee protected anatomy or face.'}
report['visualAcceptance']='Inspected original master, both pose raws and rejected matte raw, fixed-density master/arm-ready/old/new crouch comparison, full paired sequence and all neck details. Selected master-v2 deep squat topology and head/build/detail closer to master than old bank and rejected shallow candidate. Matte-v3 rejected for expanded anatomy and altered crouch/crown87 vs114. Selected grade remains brighter and provisional; full head/grade fidelity, continuous motion, contact and adjacent push-off remain pending.'
report['browserEvidence']={'scope':'Paused source crouch controls/label and saved screenshot, not native or continuous motion acceptance','file':'browser-review.png'}
report['sourcePromptSHA256']={f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in (P/'sources').glob('*') if f.is_file()}
(P/'review.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
note='''## Bill West original-master deep crouch source repair — October 2, 2026

Sibling character/bill-land-water-west-v6 replaces only pose2 in both gears. Sole original right-hand left-facing side master authors adult anatomy at fixed148/956 source density. First source rejected: enlarged head and shallow knee bend/crown95. Second source selected provisionally: deepens hips/knees and returns crown114/support224, whole-figure translation only. Matte edit rejected for expanded head/body/hardware and altered crouch/crown87. Both pose raws and rejected matte raw, exact prompts and generation provenance retained. Built-in imagegen edit mode, no mirroring or per-pose height fitting.

Twelve unchanged decoded poses0/1/3/4/5/6 across both gears exactV5. Current idle/arm-ready contexts retained. Canonical40x40helmet scale1/rotation0, all five head fits preserve body outside bounded mask and foreground. Fourteen APNGframes/holds exact,500ms/loop1. Frozen source/normal/master inputs stable. No native/profile interval, normal selection or independent exit update; prior WestV4 native/resume/TitleContinue does not coverV5/V6. Full Bill objective remains active/incomplete.

Reviewed original master, both pose sources and rejected material source, fixed-density old/new/master/arm-ready comparison, full14poseboard and neck details. Deep crouch and head/build/detail improve, but selected pose remains brighter; full head/grade/contact/continuous motion and next push-off remain provisional. Paused browser source crouch inspected/saved. Rejected material edit alpha/mask/bounds compared; darker cloth cannot justify geometry regression.

Lesson: standing-master authorship can enlarge a crouch head or leave knees too shallow even when detailed suit design survives. Explicitly specify deep hip/knee articulation, unchanged head/hardware scale and empty-canvas density; compare at shared physical scale before selecting. Fixed support224 or canonical equipment protection cannot certify crouch topology or original anatomy. Preserve rejected raw/prompt and keep prior native evidence tied to its original bank.

Next West push-off/remaining interiors and independent exit standing/rise; North/South master grade/build, refreshed native contact/motion/resume, guarded normal admission/cargo lifecycle and entire-library consistency/polish.
'''
files=[R/'docs/CURRENT_STATUS.md',R/'docs/BILL_ANIMATION_CONTINUATION_2026-09-29.md',R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]
for f in files:
    with f.open('rb') as s:s.seek(max(0,f.stat().st_size-65536));tail=s.read().decode('utf-8',errors='replace')
    if '## Bill West original-master deep crouch source repair — October 2, 2026' not in tail:
        with f.open('a',encoding='utf-8') as s:s.write('\n\n'+note)
(P/'HANDOFF.md').write_text('''# Project handoff

Updated: October 2, 2026 · Project: Brine Space · Task: Full Bill animation set

## Objective and acceptance
Complete full Bill set following original masters, camera, physical scale/build and matte grade, then cross-family polish and normal integration.

## Accepted decisions and constraints
Original independently authored views and fixed source density; reversible sibling repairs. Preserve owner data/current selections/concurrent work. No per-pose height fitting.

## Current state
West entryV6 replaces crouch2, retaining V5 idle/arm-ready and all other poses. First crouch and later matte edit rejected; second deep crouch staged, with grade still provisional. All raws/prompts, build, paired/neck/master boards, preview/review and six guidance updates retained.

## Verification
12unchanged decoded poses exact;14APNGframes/holds exact500ms/loop1. Five canonical head/body protection fits. Raw/master/registered/paired/neck and paused browser review. Frozen inputs stable. No new native/profile interval; no production selection. Full identity/contact/moving fidelity remains provisional.

## Next action
Repair West push-off/other interiors and separate exit context/rise, then North/South grade/build; refreshed native motion/contact/resume evidence, normal admission/cargo lifecycle and full-library polish. Goal active/incomplete.
''',encoding='utf-8')
print(json.dumps({'frozenInputs':len(report['inputSHA256']),'unchangedPoses':12,'materialLimits':report['materialEditLimits'],'guidanceFiles':6}))
