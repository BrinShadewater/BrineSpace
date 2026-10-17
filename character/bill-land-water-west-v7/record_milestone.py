from pathlib import Path
from PIL import Image,ImageDraw
import json,hashlib
P=Path(__file__).resolve().parent;R=P.parent.parent
report=json.loads((P/'review.json').read_text(encoding='utf-8'))
changed=[f for f,h in report['inputSHA256'].items() if hashlib.sha256((R/'character'/f).read_bytes()).hexdigest()!=h];assert not changed,changed
report.update(generationMode='built-in image_gen edit',generation='exec-571f0882-0b61-49de-8aab-6406b7c2a6b7',frozenInputsStable=len(report['inputSHA256']),registrationScope='Whole-figure crown bound to[140,117]. Opaque lowest support232 is a measurement, not planted ground contact224. No foot/support fit or per-pose height normalization.')
report['visualAcceptance']='Original master, previous source pose, generated raw, fixed-density original/crouch/previous/new push comparison, full paired sequence and all neck details inspected. Master design/detail and head/build closer; adjacent original-master poses retain readable adult build. Full head/material fidelity, continuous moving joins, actual contact/clearance and remaining late poses provisional.'
report['browserEvidence']={'scope':'Paused source push-off and source controls verified; screenshot browser-review.png. Not full continuous or native motion acceptance.'}
(P/'review.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
board=Image.new('RGB',(1280,720),'#182932');d=ImageDraw.Draw(board)
for row,g in enumerate(['bare','helmet']):
    frames=[Image.open(P/g/f'frames/land-swim-west/{i:03}.png').convert('RGBA') for i in range(4)]
    for col,im in enumerate(frames):board.paste(im,(col*320,row*360+25),im);d.text((col*320+5,row*360+5),g+' '+['Current normal idle','Master arm-ready','Master deep crouch','Master push-off'][col],fill='white');d.line((col*320,row*360+249,col*320+319,row*360+249),fill='#6aa39e')
board.save(P/'initial-four-comparison.png')
note='''## Bill West original-master airborne push-off source repair — October 2, 2026

Sibling character/bill-land-water-west-v7 replaces only pose3 both gears, retaining V6 current normal idle/master arm-ready/deep crouch and remaining late poses. Built-in imagegen exec-571f0882-0b61-49de-8aab-6406b7c2a6b7 uses sole original right-hand left-facing master; raw/exact prompt retained. Same1536x1024 original148/956 source density, whole-figure crown translation[49,88] to[140,117]. Lowest opaque support232 measured, not planted contact224. No foot/support fitting, limb transforms, mirroring or per-pose height normalization.

Twelve unchanged decoded poses0/1/2/4/5/6 exactV6;14APNGdecodedframes/holds exact500ms/loop1. Canonical40x40helmet native scale1/rotation0, five bounded head fits protect body/foreground. Twenty frozen inputs stable. Original/master/previous raw/new raw, registered master/crouch/before/after comparison, full14posepaired board and neck pairs reviewed. Paused source push-off browser controls/screenshot reviewed. Master detail and head/build improve; full material/head fidelity, continuity, actual airborne/water/floor clearance, remaining late poses remain provisional. No new native/profile interval, normal selection or independent exit update; older WestV4 native/resume/Continue evidence does not coverV5/V6/V7.

Lesson: pose registration depends on action. An airborne push-off can preserve a selected crown path while its lowest painted boot lies below the standing foot ruler. Do not force every support to224 or compress anatomical height to make static alignment pass. Review root-relative motion/collision/contact in native context separately. Sole-master whole-pose authorship restores details lost in older action sources; shared helmet fitting still cannot certify underlying body fidelity.

Next initial-four chronological/grade and airborne contact review, remaining West lift/prone/interiors and independent exit context/rise; North/South master grade/build; refreshed native contact/motion/resume, guarded normal admission/cargo lifecycle and full-library consistency/polish. Full Bill objective active/incomplete.
'''
files=[R/'docs/CURRENT_STATUS.md',R/'docs/BILL_ANIMATION_CONTINUATION_2026-09-29.md',R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]
for f in files:
    with f.open('rb') as s:s.seek(max(0,f.stat().st_size-65536));tail=s.read().decode('utf-8',errors='replace')
    if '## Bill West original-master airborne push-off source repair — October 2, 2026' not in tail:
        with f.open('a',encoding='utf-8') as s:s.write('\n\n'+note)
(P/'HANDOFF.md').write_text('''# Project handoff

Updated: October 2, 2026 · Project: Brine Space · Task: Bill full animation set

## Objective and acceptance
Finish full Bill set matching masters/camera/scale/build/matte grade, then full-library consistency/polish and normal integration.

## Accepted decisions and constraints
Reversible sibling repairs; independently authored directions, fixed source density. Keep current game selections and owner data safe. No posed-height fitting or forcing airborne boots to standing ruler.

## Current state
West entryV7 replaces only push-off3 both gears; V6 idle/arm-ready/crouch retained. Raw/exact prompt, reproducible builder/prepare, reference/full paired/neck/initial-four boards and finite preview/review retained; six guidance files updated.

## Verification
12unchanged poses exact;14APNGframes/holds exact500ms/loop1. Five canonical helmet body/foreground protection fits;20frozen inputs stable. Source/master/registered/fullpaired/neck and paused browser reviewed. No new native/profile evidence, full visual acceptance or normal selection.

## Next action
Initial-four chronological/grade and actual airborne contact/clearance review; remaining West sources/independent exit, North/South master refinements; refreshed native motion/resume, normal admission/cargo lifecycle and complete-library polish. Goal active/incomplete.
''',encoding='utf-8')
print(json.dumps({'frozenInputs':len(report['inputSHA256']),'unchangedPoses':12,'guidanceFiles':6,'supportMeasured':232}))
