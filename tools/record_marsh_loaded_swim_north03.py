"""Publish bounded player evidence and preserve the unresolved whole-source scope."""
from pathlib import Path
import json,hashlib,shutil
from PIL import Image,ImageSequence
ROOT=Path(__file__).resolve().parents[1];B=ROOT/'character/marsh-loaded-swim-material-v1';S=B/'sources';O=B/'north-loop-03-actor-review';O.mkdir(exist_ok=True)
read=lambda p:json.loads(p.read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
r=read(S/'north-loop-03.request.json');recipe=read(B/'north-loop-03-unselected/recipe.json')
assert r['generationId']=='exec-c659329f-8f4c-4e57-881a-e600dbca1c20'
assert sha(S/'north-loop-03.raw.png')==r['rawSha256']==sha(Path(r['originalGeneratedPath']))
assert sha(S/'north-loop-03.prompt.txt')==r['promptSha256']
for q in r['orderedReferences']+r['sourceFrames']:assert sha(ROOT/q['path'])==q['sha256']
assert [q['occupiedSize'] for q in recipe['records']]==[[60,90],[59,76],[60,90],[59,90],[54,146]]
a=ROOT/'output/marsh-animation-audit/loaded-swim-north-native-03-2026-10-02';report=read(a/'report.json')
assert (report['checks'],report['failures'],len(report['samples']),len(report['captures']))==(244,0,109,6)
assert (a/'native-exit.txt').read_text().strip()=='0'
log=(a/'native.log').read_text();assert 'ERROR:' not in log and 'WARNING:' not in log
counts={}
for kind in ['owner','inputs']:
    before=read(a/f'{kind}-before.json');assert before==read(a/f'{kind}-after.json');counts[kind]=len(before)
assert counts=={'owner':2931,'inputs':45}
for c in report['captures']:shutil.copy2(a/c['file'],O/c['file'])
order=[0,1,2,3,2,1];frames=[Image.open(B/f'north-loop-03-unselected/{i:03}.png').convert('RGBA') for i in order]
apng=B/'north-loop-03-unselected/player-holds.apng';frames[0].save(apng,format='PNG',save_all=True,append_images=frames[1:],duration=[180]*6,loop=0,disposal=0,blend=0)
with Image.open(apng) as im:
    decoded=[f.copy().convert('RGBA') for f in ImageSequence.Iterator(im)];assert len(decoded)==6
    for d,f in zip(decoded,frames):assert d.tobytes()==f.tobytes()
verification={'normalAdmission':False,'fullGoalComplete':False,'nativePlayerChecks':244,'samples':109,'timingSlots':6,'authoredFigures':4,'playerRestores':6,'sameClockHolds':6,'decodedAPNGHolds':6,'inputsStableDuringInterval':45,'ownerFilesUnchanged':2931,'errors':0,'warnings':0,'exitCode':0,'nativeBoardsInspected':6,'wholeCrossBoardsInspected':2,'scope':report['scope']}
(O/'verification.json').write_text(json.dumps(verification,indent=2)+'\n')
assessment={'normalAdmission':False,'fullGoalComplete':False,'findings':'North03 source and own-master board, all six native boards and two side cross boards inspected. Whole projection fits with no opaque clipping at one own-neutral146 scale. Neutral54x146 versus own master55x146. Swimmer heads visibly smaller than neutral and staged side heads; elbow spread narrower than camera request. Four kick poses remain distinct; posture02 folds both knees and projects shorter, not a per-pose rescale. Quiet matte family/rear panel preserved; case forward beyond head, not across back. Head/body/case/root and linked joins remain provisional. Correct whole-source proportions before normal admission. No actual actor/world route, fullSave/Continue, helmet or coherent family gate this interval.'}
(O/'visual-assessment.json').write_text(json.dumps(assessment,indent=2)+'\n')
(B/'north-loop-03-cross-review/visual-assessment.json').write_text(json.dumps(assessment,indent=2)+'\n')
r['status']='Whole camera study retained, native player/cross-source reviewed; head/elbow proportions need correction; staged, no normal admission';(S/'north-loop-03.request.json').write_text(json.dumps(r,indent=2)+'\n')
lesson='''

## Marsh North loaded-swim camera studies — October 2, 2026

Own-North whole sources retained with frozen prompts/ordered reference hashes:
raw01 exec-a2e382c4-5383-46c5-8685-c15b8c884962 and raw02
exec-178d1e02-465f-43bb-a1b1-83f4cfb30dce rejected for near-upright
water projection. At one own-neutral146 scale, swimmers124-129 and112-113
high exceed the old top105/208 canvas. Packing asserted opaque clipping;
no native tests ran on those studies, no crop or per-pose shrink to hide it.
Neutral rulers55x146/55x147 show camera drift can persist even when the
standing body matches. Whole source03 prioritised actual old water pose as
camera authority, own body as identity/grade authority, not rejected sheet.
Source03 exec-c659329f-8f4c-4e57-881a-e600dbca1c20: one neutral146 BOX scale
.22188449848024316, whole alpha128 cells/integer translations/no clipping.
Packed figures60x90/59x76/60x90/59x90; neutral54x146 vs own master55x146.
Bounds measurement after resizing raw alpha differs one pixel from packer
threshold-before-BOX route: recipe is actual packed output authority.
Diagnostic whole midpoint112/top105 is not physical world-root acceptance.

Native player244checks,109samples/two1080ms wraps,6restore/same-clock holds,
6timing slots alias4drawings0,1,2,3,2,1 at180ms. Six native boards inspected;
six APNG holds decode exact RGBA.45 bounded inputs stable DURING interval,
2931owner nonlog files unchanged under scratch APPDATA,0errors/warnings/fails,
exit0. Two cross boards/18 unique whole figures inspected against staged
East02/West01 and three own neutrals/masters. Quiet matte family/rear panel
and forward case kept, but North swimmer heads smaller and elbow spread
narrower than requested; do not declare cross-family proportions accepted.
Camera-first references improve projection but can shrink anatomy: retain
the standing ruler and reauthor whole figures to recover head/upper-body
scale, never enlarge isolated heads or fit each pose. Raw03 remains staged.
No normal selection/runtime change, actual world route, fullSave/Continue,
helmet/contact or coherent water-family acceptance this interval.
Next whole North head/elbow correction, then own-South loop and linked whole
water turns/pickup/drain, scoped native/world/persistence joins and admission.
Dry cargo and other full Marsh families/cross-library polish remain open.
Full goal active/incomplete; no live generation or validation job remains.
Handoff: docs/MARSH_LOADED_SWIM_NORTH03_HANDOFF_2026-10-02.md.
'''
canonical=ROOT/'skills/brinespace-character-pipeline/references/master-repair.md';installed=Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/master-repair.md')
assert canonical.read_bytes()==installed.read_bytes()
for p in [ROOT/'character/ANIMATION_PIPELINE.md',ROOT/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',ROOT/'docs/CURRENT_STATUS.md',canonical]:
    with p.open('a',encoding='utf-8') as f:f.write(lesson)
shutil.copyfile(canonical,installed)
handoff='''# Project handoff

Updated: October 2, 2026 · Project: BrineSpace · Task: Marsh North loaded swimming

## Objective and acceptance
Full master-matched Marsh set and cross-family polish remain active/incomplete.
North water loop needs correct own-rear identity, physical adult scale and joins.

## Accepted decisions and constraints
Whole source authoring, one own-neutral scale, no mirrors/patches/per-pose fits.
Case held forward, not across back. Native probes use scratch APPDATA.

## Current state
Three retained raw sheets/prompts/requests in character/marsh-loaded-swim-material-v1/sources.
North01/02 rejected near-upright projection. North03 staged camera study in
north-loop-03-unselected; actor/cross review directories preserve evidence.
New prepare/retain/pack/measurement/native/fingerprint/cross/record tools and paired
review_marsh_loaded_swim_north03.gd/.uid. Pipeline/bible/status/both skill refs updated.
No normal catalogue/gameplay changes. No live jobs.

## Verification
Native player244checks,109samples/two wraps,6restore/hold checks;6APNG RGBA holds.
All6native and2cross boards reviewed.45inputs and2931ownerfiles stable,0errors/
warnings/failures,exit0. Own neutral54x146/master55x146; four drawings/six slots.
Head and elbow proportions remain provisional. No actual world/save/helmet gate.

## Next action
Reauthor whole North figures for larger correct head/elbow spread while retaining
prone projection and neutral ruler. Then South and linked whole water states.
Normal route/persistence/contact/family admission and all remaining Marsh polish.
'''
(ROOT/'docs/MARSH_LOADED_SWIM_NORTH03_HANDOFF_2026-10-02.md').write_text(handoff,encoding='utf-8')
print('North03 scoped native/source evidence published; docs and skill copies updated; full goal open.')
