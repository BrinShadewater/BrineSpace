"""Retain source/player evidence without mistaking a study for normal admission."""
from pathlib import Path
import json,hashlib,shutil
from PIL import Image,ImageSequence
ROOT=Path(__file__).resolve().parents[1];B=ROOT/'character/marsh-loaded-swim-material-v1';S=B/'sources';A=ROOT/'output/marsh-animation-audit/loaded-swim-east-native-02-2026-10-02';O=B/'east-loop-02-actor-review';O.mkdir(exist_ok=True)
read=lambda p:json.loads(p.read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
r=read(A/'report.json');assert (r['checks'],r['failures'],len(r['samples']),len(r['captures']))==(244,0,109,6)
assert (A/'native-exit.txt').read_text().strip()=='0' and 'ERROR:' not in (A/'native.log').read_text()
for n,count in [('inputs',46),('owner',2931)]:
    before=read(A/f'{n}-before.json');assert len(before)==count and before==read(A/f'{n}-after.json')
for rev,generation,scale,sizes in [
    ('01','exec-615ef03a-d289-4d71-989d-c6355b68577e',.3567961165048544,[[153,71],[160,71],[150,71],[143,73],[37,147]]),
    ('02','exec-9d6d5d0a-2edb-4161-9562-df9febce8555',.32450331125827814,[[146,70],[153,73],[149,75],[140,76],[35,147]])]:
    request=read(S/f'east-loop-{rev}.request.json');recipe=read(B/f'east-loop-{rev}-unselected/recipe.json')
    assert request['generationId']==generation and sha(S/f'east-loop-{rev}.prompt.txt')==request['promptSha256']
    assert sha(S/f'east-loop-{rev}.raw.png')==request['rawSha256']==sha(Path(request['originalGeneratedPath']))
    for q in request['orderedReferences']+request['sourceFrames']:assert sha(ROOT/q['path'])==q['sha256']
    assert recipe['commonNeutralScale']==scale and [q['occupiedSize'] for q in recipe['records']]==sizes
    request['status']='Whole raw/packed/master comparisons inspected; 02 preferred staged study, no normal admission' if rev=='02' else 'Retained before-correction study; oversized swimmer heads/wider neutral; not admitted'
    (S/f'east-loop-{rev}.request.json').write_text(json.dumps(request,indent=2)+'\n')
    (B/f'east-loop-{rev}-unselected/visual-assessment.json').write_text(json.dumps({'normalAdmission':False,'fullGoalComplete':False,'rawAndWholeStudyBoardSeen':True,'neutralSize':sizes[-1],'selectedMasterSize':[32,147],'findings':'Whole02 correction narrows neutral35 versus first37; selected master32. Muted grade and one-right-edge case latch closer to carry authority. Four complete kick drawings retained; wider neutral, head/body proportions, grade and connected water-action joins remain provisional. No per-part fitting was used.','nativePlayerReview':rev=='02'},indent=2)+'\n')
for c in r['captures']:shutil.copy2(A/c['file'],O/c['file'])
state=read(B/'east-loop-02-unselected/manifest.json')['states'][0]
frames=[Image.open(ROOT/p.removeprefix('res://')).convert('RGBA') for p in state['frameFiles']]
apng=B/'east-loop-02-unselected/player-holds.apng'
frames[0].save(apng,save_all=True,append_images=frames[1:],duration=state['frameDurationsMs'],loop=0,disposal=0,blend=0)
decoded=[f.convert('RGBA').copy() for f in ImageSequence.Iterator(Image.open(apng))]
assert len(decoded)==6 and all(x.tobytes()==y.tobytes() for x,y in zip(frames,decoded))
v={'checks':244,'failures':0,'controlledSamples':109,'timingSlots':6,'authoredFigures':4,'sixNativeBoardsInspected':True,'playerRestoresAndSameClockHolds':6,'stableBoundedInputs':46,'unchangedOwnerNonLogFiles':2931,'decodedApngHolds':6,'normalAdmission':False,'fullGoalComplete':False,'scope':r['scope'],'fixtureWarnings':(A/'native.log').read_text().count('WARNING:'),'limits':'One fixture Image.load_from_file master warning concerns export; this is native editor/player evidence, not export validation. No normal controller/world/water task/helmet/fullSave/contact acceptance. Request and review metadata updated after interval; claim dated interval equality only.'}
(O/'verification.json').write_text(json.dumps(v,indent=2)+'\n')
maintained=ROOT/'skills/brinespace-character-pipeline/references/master-repair.md';installed=Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/master-repair.md');assert maintained.read_bytes()==installed.read_bytes()
marker='## Marsh East loaded-swim whole source and neutral correction — October 2, 2026'
lesson='''

## Marsh East loaded-swim whole source and neutral correction — October 2, 2026

Catalogue inventory currently 77 ordered body manifests, 228 states / 1190 slots:
coverage only, not master fidelity. Continue full Marsh set and cross-family polish;
do not confuse previous numerical coverage with accepted artwork. Following cargo
route/save milestone, loaded swimming is the next older material/body family.

First East loaded-swim whole atlas exec-615ef03a-d289-4d71-989d-c6355b68577e retained
with frozen prompt/ordered case, bodyPRIMARY, motion-only, original identity refs.
Observed unequal five columns despite equal-cell request. Four complete swimmers
plus own standing neutral; do not extract by assumed grid. One neutral147 BOX scale
.3567961165048544 yields153x71/160x71/150x71/143x73, neutral37x147 versus selected
32x147. Raw and six-figure packed comparison inspected. Swimmer heads grew relative
to own neutral; reject as normal admission. Correct whole figures at source, not
smaller pasted heads or independent case/body fitting.

Focused whole02 exec-9d6d5d0a-2edb-4161-9562-df9febce8555 uses raw01 as edit/motion
target, bodyPRIMARY as proportions/grade, cargo authority and original identity.
Explicit same small adult head across swim/neutral and32:147 neutral width. One
neutral147 BOX scale .32450331125827814 yields146x70/153x73/149x75/140x76 andneutral
35x147. Width improved by2 but still+3 versus master. Correct near RIGHT temple,
side inset case/single ivory RIGHT edge latch, connected hands and four distinct
whole leg phases retained. Muted grade closer; proportions/grade remain provisional.
Neither declared ruler nor prompting numbers proves final master equivalence.
Both original raw files, exact prompts/refs/source hashes and nonuniform cells kept.
Whole alpha128 packing, integer translations, zero opaque clipping; no mirroring,
patches, recolouring, cargo-width fit or per-pose scaling. Swim registration uses
forward-head top108/case-right163 for diagnostic comparison, not accepted worldroot.

Private02 manifest preserves selected224x208,p112/172,H148, water metadata and
six180ms looping holds (1080ms), aliasing FOUR authored figures in0,1,2,3,2,1 order.
Do not call six timing slots six authored drawings. Actual CrewSpritePlayer:
244checks,109controlled samples through two wraps, six player restores/same-clock
holds; all six native boards inspected atsource size and65.28worldheight alongside
selected old loop/neutral/master. Six APNG holds decode exact RGBA. 46 bounded
inputs stable DURING interval,2931ownerfiles unchanged scratchAPPDATA,0fail/errors,
exit0. One fixture Image.load_from_file master warning is about export, not an
export check. No actual normal actor/controller/water task/helmet/fullSave/physical
contact/continuousmotion or coherent-family admission established by this fixture.
Normal catalogue/runtime unchanged. Metadata updates follow interval; dated scope.

Next actual normal-water route and pickup/drain/turn joins with candidate02; refine
remaining head/body/grade findings at whole source if joins fail, then other loaded
swim directions/turns and remaining master-matched families. Arrival grounded pivot
and staged drycargo admission remain open. Full set active/incomplete. No live job.
'''
# Assert the coverage statement before appending this dated lesson.
inventory=read(B/'current-catalogue-family-inventory.json');assert (inventory['bodyManifests'],inventory['states'],inventory['slots'])==(77,228,1190)
for p in [ROOT/'character/ANIMATION_PIPELINE.md',ROOT/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',ROOT/'docs/CURRENT_STATUS.md',maintained]:
    with p.open(encoding='utf-8') as f:present=any(marker in line for line in f)
    if not present:
        with p.open('a',encoding='utf-8') as f:f.write(lesson)
installed.write_bytes(maintained.read_bytes())
(ROOT/'docs/MARSH_LOADED_SWIM_MATERIAL02_HANDOFF_2026-10-02.md').write_text('''# Project handoff

Updated: October 2, 2026 · BrineSpace · Marsh East loaded swimming

## Objective and acceptance
Full master-matched Marsh set and all-family consistency/polish active/incomplete.
Current 228 states/1190 slots is coverage only. Older loaded-swim family now in review.

## Accepted decisions and constraints
Original East identity and selected body master authoritative, staged carry case
authority for hardware. Whole sources, same neutral scale, no per-part fitting,
mirrors, patching, per-pose rescale or clipping. Scratch APPDATA/profile fingerprints.
Normal catalogue/runtime unchanged; drycargo admission/pivot polish still open.

## Current state
character/marsh-loaded-swim-material-v1 keeps current inventory, frozen01/02 requests,
raw originals, whole pack studies, preferred staged02 manifest and actor-review boards.
02 neutral35x147 versus01 37x147/master32x147. Four drawings alias six old180ms holds.
New prepare/pack01+02, native02 prepare, .gd/.uid fixture, fingerprint/record helpers.
Pipeline/bible/status/canonical-installed skill references updated. No live job.

## Verification
Both raw sources and whole master comparisons seen.02 six native boards inspected:
244 player checks,109samples/two wraps,six restores/same-clock holds,exact six APNG
decoded holds.46bounded inputs/2931ownerfiles stable,0errors/failures,exit0.
One fixture master image-load export warning retained. Same case hardware and
connected grip clearer; neutralwidth+3,head/body/grade and water-action joins open.
Diagnostic root registration, not actual controller/world/helmet/fullSave acceptance.

## Next action
Actual normal-water route and pickup/drain/turn endpoint joins with private02; whole
source correction for observed failures, then remaining loaded-swim facings/turns.
Continue remaining Marsh families and all-family master consistency/polish.
''',encoding='utf-8')
print('Recorded East loaded-swim whole02 study: 244 player checks, six native boards; full goal incomplete.')
