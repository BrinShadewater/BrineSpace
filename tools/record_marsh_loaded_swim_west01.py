"""Record whole own-West source, actual q0 route and scoped side comparison."""
from pathlib import Path
import json,hashlib,shutil,subprocess,sys
from PIL import Image,ImageSequence
ROOT=Path(__file__).resolve().parents[1];B=ROOT/'character/marsh-loaded-swim-material-v1';S=B/'sources';O=B/'west-loop-01-actor-review';O.mkdir(exist_ok=True)
read=lambda p:json.loads(p.read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
request=read(S/'west-loop-01.request.json');recipe=read(B/'west-loop-01-unselected/recipe.json')
assert request['generationId']=='exec-fd5045a0-c705-4d01-83ff-14840725a9b1'
assert sha(S/'west-loop-01.prompt.txt')==request['promptSha256'] and sha(S/'west-loop-01.raw.png')==request['rawSha256']==sha(Path(request['originalGeneratedPath']))
for q in request['orderedReferences']+request['sourceFrames']:assert sha(ROOT/q['path'])==q['sha256']
assert recipe['commonNeutralScale']==.3442622950819672 and [q['occupiedSize'] for q in recipe['records']]==[[141,54],[130,56],[133,66],[131,61],[33,146]]
reports={}
for name,checks,samples,captures,inputs in [('loaded-swim-west-native-01',244,109,6,75),('loaded-swim-west-world-01',15017,3680,48,765)]:
    a=ROOT/f'output/marsh-animation-audit/{name}-2026-10-02';r=read(a/'report.json')
    assert (r['checks'],r['failures'],len(r['samples']),len(r['captures']))==(checks,0,samples,captures)
    assert (a/'native-exit.txt').read_text().strip()=='0' and 'ERROR:' not in (a/'native.log').read_text() and 'WARNING:' not in (a/'native.log').read_text()
    for kind,count in [('inputs',inputs),('owner',2931)]:
        before=read(a/f'{kind}-before.json');assert len(before)==count and before==read(a/f'{kind}-after.json')
    reports[name]=r
    if captures==6:
        for c in r['captures']:shutil.copy2(a/c['file'],O/c['file'])
world=reports['loaded-swim-west-world-01'];assert len(world['phases'])==12 and world['actorPlayerRestores']==48
assert set(world['westSlots'])==set(world['pickupSlots'])==set(range(6)) and set(world['unloadSlots'])==set(range(4)) and set(world['drainSlots'])==set(range(5))
assert set(world['turns'])=={'swim-carry-turn-east-west','swim-carry-turn-west-south'}
w=B/'west-loop-01-world-review';v=read(w/'verification.json');assert len(v['endpointChecks'])==4 and not any(q['sameAsNewWestLoop0'] for q in v['endpointChecks'])
for q in v['sourceParity']:assert sha(ROOT/q['path'])==q['sha256']
(w/'visual-assessment.json').write_text(json.dumps({'normalAdmission':False,'fullGoalComplete':False,'all48SourceNativePairsInspected':True,'pairedBoardsInspected':6,'findings':'West01 readable in actual q0 dispatched seabed return; near LEFT temple bare, single case LEFT edge latch, four whole kick figures. Old EastWest endpoint->newWest0 and newWest3->oldWestSouth first visibly change body/pose/case hardware. Old pickupEast->newEast0 also remains a mixed join. Four West linked source endpoints still old; actual q0 pickupEast and drainNorth, so West pickup/drain mismatch is source-only evidence. Body/head/grade and registration/contact remain provisional.','next':'Whole North/South loops, then consistent whole linked pickup/turn/drain family before normal selection; full save/Continue, helmet and additional routes remain scoped gates.'},indent=2)+'\n')
subprocess.run([sys.executable,str(ROOT/'tools/publish_marsh_loaded_swim_west_world01.py')],check=True,stdout=subprocess.DEVNULL)
state=read(B/'west-loop-01-unselected/manifest.json')['states'][0]
frames=[Image.open(ROOT/p.removeprefix('res://')).convert('RGBA') for p in state['frameFiles']]
apng=B/'west-loop-01-unselected/player-holds.apng';frames[0].save(apng,save_all=True,append_images=frames[1:],duration=state['frameDurationsMs'],loop=0,disposal=0,blend=0)
decoded=[f.convert('RGBA').copy() for f in ImageSequence.Iterator(Image.open(apng))];assert len(decoded)==6 and all(x.tobytes()==y.tobytes() for x,y in zip(frames,decoded))
(O/'verification.json').write_text(json.dumps({'checks':244,'failures':0,'controlledSamples':109,'timingSlots':6,'authoredFigures':4,'nativeBoardsInspected':6,'playerRestoresSameClockHolds':6,'stableBoundedInputs':75,'unchangedOwnerNonLogFiles':2931,'decodedApngHolds':6,'normalAdmission':False,'fullGoalComplete':False,'scope':reports['loaded-swim-west-native-01']['scope']},indent=2)+'\n')
(O/'visual-assessment.json').write_text(json.dumps({'normalAdmission':False,'fullGoalComplete':False,'rawAllFourReferencesWholeStudyAndSixNativeBoardsSeen':True,'findings':'Whole own-West body and case retain correct directional hardware. Neutral33x146 against master31x147, nominal147 common ruler becomes146 post-threshold: disclosed, not refit per pose. Swimming figures141x54/130x56/133x66/131x61; head/body/grade/root remain provisional. Four unique figures, six timing holds0,1,2,3,2,1; no mirroring, anatomy patches or independent cargo fitting.'},indent=2)+'\n')
cross=B/'side01-cross-review';cv=read(cross/'verification.json');assert (cv['wholeFigures'],cv['states'],cv['slots'],cv['authoredSwimmingFigures'])==(12,2,12,8)
for q in cv['sourceParity']:assert sha(ROOT/q['path'])==q['sha256']
(cross/'visual-assessment.json').write_text(json.dumps({'normalAdmission':False,'fullGoalComplete':False,'wholeComparisonBoardInspected':True,'wholeFiguresInspected':12,'findings':'Eight own-facing complete swimmers plus own neutrals and masters inspected. East02 neutral35x147 versus32x147;West01 33x146 versus31x147. Own East implant/West bare left temple and right/left edge latches differ correctly. Similar matte family, but bone/head/grade/case/root diagnostics remain open. Natural knee differences change swimming bounds; do not normalize each swimmer independently. Two private side loops, not completed water family.'},indent=2)+'\n')
request['status']='Whole own-West source/master/cross-source/native player and actual q0 route reviewed; staged, no normal admission';(S/'west-loop-01.request.json').write_text(json.dumps(request,indent=2)+'\n')
maintained=ROOT/'skills/brinespace-character-pipeline/references/master-repair.md';installed=Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/master-repair.md');assert maintained.read_bytes()==installed.read_bytes()
marker='## Marsh own-West loaded swim and side cross-review — October 2, 2026'
lesson='''

## Marsh own-West loaded swim and side cross-review — October 2, 2026

Whole own-West source exec-fd5045a0-c705-4d01-83ff-14840725a9b1 retained with frozen
exact prompt/ordered refs/source hashes. Put bodyPRIMARY FIRST, case authority
SECOND, old swim MOTION ONLY THIRD, original West identity FOURTH. All four local
versions and resulting raw/whole study inspected. West nearLEFT temple BARE, RIGHT
implant far side; case side inset panel and oneivory LEFT edge latch. Author own
poses, never mirror East. Four full kick figures and same standing neutral.
One neutral147 BOX scale .3442622950819672, alpha128, observed unequal columns,
integer whole translations, no opaque clipping/patch/recolour/perpart/perpose fit.
Figures141x54/130x56/133x66/131x61; neutral33x146 versus master31x147. Post-threshold
nominal147 becomes146 actual; disclose instead of silently refitting ruler/poses.
Own selected West case-left50 / forward-head top106 is diagnostic registration,
not mirror-derived geometry or accepted world root/contact. Width+2, head/body/
grade and rigid case consistency remain provisional. Normal art selection unchanged.

Private West01 six180ms looping slots (1080ms) alias FOUR drawings0,1,2,3,2,1,
224x208,p112/172,H148 and original water metadata. Actual player244checks,
109controlled samples/two wraps, six snapshot restores/same-clock holds; all six
native source-size/65.28worldheight comparisons alongside own master/neutral seen.
Six APNG holds decode exact RGBA.75 bounded inputs stable DURING interval,
2931ownerfiles unchanged scratchAPPDATA,0errors/warnings/failures,exit0. Fixture
uses PNG buffers; no Image.load_from_file export warning. Player-only scope distinct
from world, saving, helmet, grounded contact and artwork acceptance.

Fresh actual normal q0 dispatched expedition loads private East02+West01 loops,
old other states.15017checks,12phases,3680controlled20ms samples,48 exact-source/
native pairs and48actor/player restores+outer-process paused holds. All6West timing
slots (4drawings),6pickupEast,4unloadSouth,5drainNorth, actual EastWest andWestSouth
cargo water turns, one extraction andone correctly delayed delivery credit; dry/
alive completion.765bounded inputs stable during interval,2931ownerfiles unchanged,
0errors/warnings/failures,exit0. All48pairs/sixboards seen. Prior q2 East route used
newEast only, oldWest: dated independent scope, not a fresh combined-family q2 gate.

Actual oldEastWest8->newWest0 andnewWest3->oldWestSouth0 visibly switch body/pose/
case details. Four linked West source endpoints are still old: West pickup last,
EastWest turn last,WestSouth turn first,West drain first. q0 actual pickupEast and
drainNorth; West pickup/drain mismatch is source-audit only. Old pickupEast->newEast0
also mixed. Do not equate green mechanics with coherent-family art acceptance or
close intermediate consistency by changing endpoint pixels alone.

Side cross-review12completefigures/oneboard seen:8swimmers plus2own neutrals and
2masters. East35x147/master32x147;West33x146/master31x147. Correct temple/case-edge
identity and similar matte family; proportions/grade/case/root remain open.
Private two-state side family12timing slots/8drawings saved; not full waterfamily.
Requests/assessment/APNG/boards updated after intervals: claim dated freezes only.
Next wholeNorth/South loaded loops, then linked whole turn/pickup/drain sources,
additional normal routes/fullSave/freshvisibleContinue/helmet/physical joins before
normal family admission. Drycargo admission/arrival grounded pivot and remaining
fullMarsh families still open. Fullgoal active/incomplete. No live job at milestone.
'''
for p in [ROOT/'character/ANIMATION_PIPELINE.md',ROOT/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',ROOT/'docs/CURRENT_STATUS.md',maintained]:
    with p.open(encoding='utf-8') as f:present=any(marker in line for line in f)
    if not present:
        with p.open('a',encoding='utf-8') as f:f.write(lesson)
installed.write_bytes(maintained.read_bytes())
(ROOT/'docs/MARSH_LOADED_SWIM_WEST01_HANDOFF_2026-10-02.md').write_text('''# Project handoff

Updated: October 2, 2026 · BrineSpace · Marsh own-West loaded swim

## Objective and acceptance
Full master-matched Marsh set and all-family consistency/polish active/incomplete.
East02 andWest01 side loaded-swim candidates staged; full waterfamily not coherent.

## Accepted decisions and constraints
OwnWest master first/case second/motion only third/original fourth. Bare visible
LEFT temple, oneLEFT case edge latch. Whole figures, one neutral scale, no mirrors/
patches/per-part fitting. Scratch APPDATA and profile fingerprints. Normal catalogue
unchanged. Use main expedition orchestration and outer paused process.

## Current state
WholeWest raw/prompt/request retained, own-West packer/source study, native and q0
world prepare/.gd+.uid/fingerprint/publish helpers plus recorder/cross-review helper.
character/marsh-loaded-swim-material-v1 keeps West study, six player comparisons,
48 world pairs and side01-cross-review twelve complete figures/two-state family.
Pipeline/bible/status/canonical-installed skills updated. No live job.

## Verification
West neutral33x146 vs master31x147; one nominal147 scale. Body/head/grade/case/root
open.244player checks/109samples/two wraps/6restores,6native boards seen,75inputs
stable. Actual q0 route with East02+West01:15017checks,12phases,3680samples,
48restores+pause,48exactsource/nativepairs/sixboards seen,765inputs stable. All6
West holds/6pickup/4unload/5drain and2turns;1safe delivery.2931ownerfiles unchanged
per interval,0errors/warnings/failures,exit0. Twelve whole crossfigures seen.
Old turn endpoints visibly mix body/case; four linked West endpoints still old.
q0 pickupEast/drainNorth, so West pickup/drain mismatch source-only. Prior q2 had
onlyEast new andWest old; do not combine dated scopes as a fresh family gate.

## Next action
WholeNorth/South loops with own masters, then whole linked turns/pickup/drain with
coherent exact endpoints; route rotations/fullsave/visibleContinue/helmet/contact
before normal selection. Drycargo admission/pivot and remaining all-set work open.
''',encoding='utf-8')
print('Recorded West source/player/q0 route and 12-figure cross-review; full goal incomplete.')
