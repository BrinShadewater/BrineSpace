from pathlib import Path
import json,hashlib
P=Path(__file__).resolve().parent;R=P.parent.parent
report=json.loads((P/'review.json').read_text(encoding='utf-8'))
changed=[f for f,h in report['inputSHA256'].items() if hashlib.sha256((R/'character'/f).read_bytes()).hexdigest()!=h];assert not changed,changed
report.update(generationMode='built-in image_gen edit',generations=['exec-b1bd2976-ddc0-4afa-b09c-565ed7d10367','exec-70b6f0fe-0d8d-467e-a7ac-97ac8b1078db'],rejectedGeneration='exec-b1bd2976-ddc0-4afa-b09c-565ed7d10367',frozenInputsStable=len(report['inputSHA256']))
report['visualAcceptance']='Original master, previous pose, both new raws and fixed-density original/push-off/previous/new levelling comparisons, complete paired board and all neck details inspected. First extended-arm candidate rejected for excessive reach. Compact bent-elbow version resolves excess reach but head remains broader than original and hands need clearer separation; needs anatomy revision. Detail improved, not full fidelity acceptance. Full head/material/anatomy, adjacent arm-length continuity, moving/contact/clearance acceptance remain pending.'
report['candidateStatus']='needs_anatomy_revision'
report['registrationScope']='Whole-figure crown translation to[130,150]; lowest painted support is a diagnostic, not planted floor contact224. No support/height fitting.'
report['browserEvidence']={'scope':'Paused source levelling pose and screenshot browser-review.png; no full continuous/native acceptance.'}
report['sourcePromptSHA256']={f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in (P/'sources').glob('*') if f.is_file()}
(P/'review.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
note='''## Bill West original-master compact levelling pose — October 2, 2026

Sibling character/bill-land-water-west-v8 stages only pose4 both gears; preceding current idle, master arm-ready/deep crouch/push-off and late poses unchanged. Sole original right-hand left-facing master, original148/956 drawing density and whole-figure crown translation to[130,150]. First raw rejected: long extended arms relative to original anatomical reach. Second compact bent-elbow source needs anatomy revision: head still broader than original and hands need clearer separation. It is diagnostic/provisional, not admitted as a completed repair. Both raw/exact prompts and rejection retained; built-in imagegen editing. No limb rotation/length fitting, mirrored directions or posed-height normalization.

Twelve unchanged decoded poses0/1/2/3/5/6 exactV7,14APNGframes/holds exact500ms/loop1. Canonical40x40helmet native scale1/rotation0, five head fits preserve bounded body/foreground. Twenty frozen inputs stable. Original/previous/bothraw/fixed-density master-push-before-after, full14poseboard and neck pairs inspected, paused browser levelling source saved. Compact arms/detail/build improve, but full anatomical reach, head/material grade, adjacent repaired arm-length continuity, airborne clearance/contact and moving joins remain provisional. No native/profile interval or normal selection; prior WestV4 native/resume/Continue does not coverV5..V8.

Lesson: original-master-only pose instructions can still lengthen outstretched arms. Judge upper-arm/forearm lengths and shoulder-elbow-wrist articulation in whole-body comparisons, not just head/hardware scale or detailed quilting. A compact bent-elbow pose constrains reach, but all neighboring launch poses still need chronological anatomy review. Crown registration/lowest painted support do not prove actual clearance or grounded contact. Keep technical pixel checks separate from fidelity acceptance.

Next resolve levelling head size/two-hand clarity, near-prone source and complete West early/late chronology/head/grade/arm-length review; independent exit context/rise, North/South master repairs; refreshed native contact/motion/resume, guarded normal admission/cargo lifecycle and full-library consistency/polish. Full Bill goal active/incomplete.
'''
files=[R/'docs/CURRENT_STATUS.md',R/'docs/BILL_ANIMATION_CONTINUATION_2026-09-29.md',R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]
for f in files:
    with f.open('rb') as s:s.seek(max(0,f.stat().st_size-65536));tail=s.read().decode('utf-8',errors='replace')
    if '## Bill West original-master compact levelling pose — October 2, 2026' not in tail:
        with f.open('a',encoding='utf-8') as s:s.write('\n\n'+note)
(P/'HANDOFF.md').write_text('''# Project handoff

Updated: October 2, 2026 · Project: Brine Space · Task: Full Bill animations

## Objective and acceptance
Full master-consistent animation set: art/camera/physical size/build/matte grade; cross-family polish and normal integration remain required.

## Accepted decisions and constraints
Original directions and fixed drawing density, reversible source siblings. Preserve normal selections/owner data/concurrent work. No per-pose height or limb-length fitting.

## Current state
West entryV8 diagnostic compact bent-elbow levelling4 candidate; head broader and hands unclear, needs anatomy revision. Long-arm first candidate rejected. Other six poses retained. Raws/prompts/rejection/build/preview/reference/paired/neck/review and six guidance updates retained.

## Verification
12unchanged source poses exact;14APNGframes/holds exact500ms/loop1. Five canonical head/body protection fits,20frozen inputs stable. Raw/master/shared-scale/paired/neck and paused browser inspected. No new native/profile evidence or normal acceptance.

## Next action
Resolve levelling head/two-hand clarity, near-prone source and complete West chronology/grade/anatomical arm reach; independent exit, North/South repairs; refreshed native motion/contact/resume, normal admission/cargo lifecycle and full-library polish. Goal active/incomplete.
''',encoding='utf-8')
print(json.dumps({'frozenInputs':len(report['inputSHA256']),'unchangedPoses':12,'guidanceFiles':6,'supportMeasured':report['opaqueSupportAfter']}))
