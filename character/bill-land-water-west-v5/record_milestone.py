from pathlib import Path
from PIL import Image
import numpy as np,json,hashlib
P=Path(__file__).resolve().parent;R=P.parent.parent;old=P.parent/'bill-land-water-west-v4'
report=json.loads((P/'review.json').read_text(encoding='utf-8'))
a=np.array(Image.open(P/'sources/arm-ready-master-v1.png').convert('RGBA'));b=np.array(Image.open(P/'sources/arm-ready-matte-v2.png').convert('RGBA'))
assert a.shape==b.shape
report['materialEditLimits']={'alphaExact':bool(np.array_equal(a[:,:,3],b[:,:,3])),'opaqueMaskExact':bool(np.array_equal(a[:,:,3]>180,b[:,:,3]>180)),'rawOpaqueBoundsBefore':Image.fromarray(a[:,:,3]).point(lambda p:255 if p>180 else 0).getbbox(),'rawOpaqueBoundsAfter':Image.fromarray(b[:,:,3]).point(lambda p:255 if p>180 else 0).getbbox(),'scope':'Whole-source edit; material instruction does not guarantee pixel-protected anatomy or face.'}
unchanged=[]
for gear in ['bare','helmet']:
    for i in range(2,7):
        aa=Image.open(old/gear/f'frames/land-swim-west/{i:03}.png').convert('RGBA');bb=Image.open(P/gear/f'frames/land-swim-west/{i:03}.png').convert('RGBA');assert aa.tobytes()==bb.tobytes();unchanged.append(f'{gear}:{i}')
report['unchangedDecodedPoses']=unchanged
manifest=R/'character/crew-runtime-matte-v1/bill/manifest.json';m=json.loads(manifest.read_text(encoding='utf-8'));s=next(s for s in m['states'] if s['id']=='idle-west');source=Image.open(manifest.parent/s['frameFiles'][0]).convert('RGBA');padded=Image.new('RGBA',(320,320));padded.alpha_composite(source,(round(160-m['pivot'][0]),round(224-m['pivot'][1])));assert padded.tobytes()==Image.open(P/'bare/frames/land-swim-west/000.png').convert('RGBA').tobytes()
report['currentNormalBareStandingContextExact']=True
report['visualAcceptance']='Raw master-authored and matte sources, registered original/prior/current comparison, final complete paired board, all neck details and paused browser pose inspected. Head/build/detail closer to original master and material restrained; full normal-idle grade, remaining interior head/build consistency, actual contact and continuous motion acceptance provisional.'
report['browserEvidence']={'normalSpeedFiniteTerminal':'Observed Play/Swimming pose7 at500ms after playback','pausedRepair':'Observed Arm ready pose2 at60ms; screenshot browser-review.png','limits':'Browser controls and final states verified; no full continuous chronological motion acceptance.'}
report['sourcePromptSHA256']={f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in (P/'sources').glob('*') if f.is_file()}
(P/'review.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
note='''## Bill West original-master arm-ready source repair — October 2, 2026

Sibling character/bill-land-water-west-v5 replaces bare standing context0 with exact registered current normal idle and pose1 with new original-master arm-ready, both gears. Built-in imagegen exec-17a46ca0-7ba3-4e0c-a45d-148806f18187 used sole original side master, right-hand left-facing figure; material exec-01a57aa3-f277-4ad4-8936-7f230dde3529 used only new pose. Both raws/exact prompts retained. Selected matte-v2 at original whole-source148/956 density,1536x1024 source; whole-figure translation[25,72], crown[157,76], support224. No posed-height fitting/mirroring.

Five remaining poses2..6 in both gears exactly matchV4 (10 decoded frame comparisons). Native40x40 canonical helmet at scale1/rotation0; all five bounded head fits preserve body outside mask/foreground. Fourteen APNGdecoded frames/holds exact,500ms/loop1. Current normal bare standing padded RGBA exact. No independent West exit update, normal candidate selection or fresh native/profile interval. Prior West native/resume/TitleContinue evidence coversV4 only and does not certify this new bank.

Inspected original master, old raw, new pose and material raw, registered comparison, complete14poseboard and neck details. Head/build/detail closer to original and restrained material improves; remaining crouch/push and other interior head/body/grade, moving joins/contact still provisional. Browser finite normal-speed playback reachesSwimming500ms/Play; paused repaired pose2 at60ms inspected/saved. Not full continuous/native motion acceptance. Material-only instruction is treated as whole-source replacement; exact alpha/mask/bounds comparison recorded in review.json.

Lesson: author a drifted standing action directly from the original directional master rather than preserving the already enlarged action head. Keep original physical source density and articulate actual shoulders. Reconcile bare standing context with current normal manifest independently of helmet context. Equipment fitting/body protection cannot certify underlying body fidelity. Retain matte edit geometry diagnostics and do not promise protected face/anatomy from prompt alone.

Next repair remaining West interiors and independent exit standing/rise, North/South master-grade/proportions; refreshed native contact/motion/resume evidence, guarded normal admission/cargo lifecycle and complete-library consistency/polish. Full Bill objective active/incomplete.
'''
files=[R/'docs/CURRENT_STATUS.md',R/'docs/BILL_ANIMATION_CONTINUATION_2026-09-29.md',R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]
for f in files:
    with f.open('rb') as s:s.seek(max(0,f.stat().st_size-65536));tail=s.read().decode('utf-8',errors='replace')
    if '## Bill West original-master arm-ready source repair — October 2, 2026' not in tail:
        with f.open('a',encoding='utf-8') as s:s.write('\n\n'+note)
(P/'HANDOFF.md').write_text('''# Project handoff

Updated: October 2, 2026 · Project: Brine Space · Task: Bill full animations

## Objective and acceptance
Finish full Bill set with master identity, camera, scale/proportions and matte grade; cross-family polish and normal game integration remain required.

## Accepted decisions and constraints
Original independently authored views, fixed source density; reversible siblings. Preserve current game selections and owner data until scoped admission evidence.

## Current state
West entryV5 source candidate: exact current bare idle context0, newly master-authored/graded pose1, canonical helmet. Raw/prompt/provenance/build/review/finite preview retained. Six guidance files updated.

## Verification
14decodedAPNGframes/holds exact;10remainingposecomparisons exact; current bare standing context exact. Five canonical helmet body protection fits. All raw/master/registered/paired/neck boards reviewed; browser finite terminal and paused repair verified. No new native/profile interval. PriorV4 evidence does not coverV5.

## Next action
Repair remaining West interiors and independent exit context/rise, then North/South master grade/build; refresh native motion/contact/resume, guarded normal admission/cargo lifecycle and full-library consistency/polish. Full goal active.
''',encoding='utf-8')
print(json.dumps({'unchangedPoses':len(unchanged),'standingExact':True,'materialLimits':report['materialEditLimits'],'guidanceFiles':len(files)}))
