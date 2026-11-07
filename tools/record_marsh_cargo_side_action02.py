"""Record whole side corrections and staged preference without normal admission."""
from pathlib import Path
import hashlib,json,subprocess,sys
ROOT=Path(__file__).resolve().parents[1];B=ROOT/'character/marsh-cargo-held-material-v1';S=B/'sources';R=B/'side-action-02-actor-review';C=B/'side02-cross-review'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())
v=read(R/'verification.json');assert (v['checks'],v['captures'],v['samples'],v['actorPlayerRestores'],v['stableBoundedInputs'],v['unchangedOwnerNonLogFiles'])==(1019,16,252,16,551,2931)
generations={'east':'exec-319a749d-48b8-42ed-b627-2507aa507672','west':'exec-811615fc-ec19-46dd-ab38-92c84715da34'}
sizes={'east':[[75,120],[85,98],[36,147]],'west':[[69,120],[78,102],[35,146]]}
for f in ['east','west']:
    r=read(S/f'{f}-unload-02.request.json');O=B/f'{f}-unload-02-unselected';recipe=read(O/'recipe.json')
    assert r['generationId']==generations[f] and sha(S/f'{f}-unload-02.prompt.txt')==r['promptSha256']
    assert sha(S/f'{f}-unload-02.raw.png')==r['rawSha256']==sha(Path(r['originalGeneratedPath']))
    for q in r['orderedReferences']+r['sourceFrames']+r['guideDependencies']:assert sha(ROOT/q['path'])==q['sha256']
    assert [q['occupiedSize'] for q in recipe['records']]==sizes[f]
    assert recipe['exactCarryEndpoint'] and recipe['exactIdleEndpoint'] and recipe['exactPickupReversal'] and recipe['decodedApngFrames']==8
    (O/'visual-assessment.json').write_text(json.dumps({'normalAdmission':False,'fullGoalComplete':False,'preferredStagedRevision':True,'allFourReferenceVersionsAndRawSeen':True,'wholeMotionAndNeutralBoardsSeen':True,'sourceNativePairsSeen':8,'findings':'Whole02 redraw brings case size closer to carry endpoint while retaining side inset panel and correct one-edge latch, own facing/temple identity. Case improvement is visual, not independent rectangle/body fitting. Neutral width+4 versus selected master; West nominal147 becomes146 post-threshold. Head/body/grade/foot-support/contact joins remain open. Preferred staged revision02, originals01 preserved.','limits':v['limits']},indent=2)+'\n')
    r.update(status='whole redraw retained/packed/source-native reviewed; preferred staged02, no normal admission',limits=v['limits']);(S/f'{f}-unload-02.request.json').write_text(json.dumps(r,indent=2)+'\n')
(R/'visual-assessment.json').write_text(json.dumps({'normalAdmission':False,'fullGoalComplete':False,'allSixteenPairsInspected':True,'pairedBoardsInspected':4,'findings':'All4Eastpickup/4Eastunload/4Westpickup/4Westunload poses inspected. Correct profiles/case hardware and unchanged carry/idle endpoints. Whole02 case size closer than01; proportion/grade/contact still provisional.','limits':v['limits']},indent=2)+'\n')
subprocess.run([sys.executable,str(ROOT/'tools/publish_marsh_cargo_side_action02.py')],check=True,stdout=subprocess.DEVNULL)
cross=read(C/'verification.json');assert (cross['wholeFigures'],cross['states'],cross['slots'])==(18,8,32)
for q in cross['sourceParity']:assert sha(ROOT/q['path'])==q['sha256']
(C/'visual-assessment.json').write_text(json.dumps({'normalAdmission':False,'fullGoalComplete':False,'wholeComparisonBoardsInspected':2,'wholeFiguresInspected':18,'preferredStagedFamily':'SouthNorth01/EastWest02','findings':'Twelve complete old/new half/floor/endpoint figures and six neutral/master figures inspected. Side crate growth reduced visually, no patch/mirror/rescale. New neutral widths36/35 vsselected32/31; West146 vsnominal147, body/head/grade/contact joins open.','next':'Coherent normal pickup/carry/turn/arrival/unload sequence and full saves/actual visible TitleContinue; source corrections where joins fail; normal admission only after scopeappropriate gates.'},indent=2)+'\n')
maintained=ROOT/'skills/brinespace-character-pipeline/references/master-repair.md';installed=Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/master-repair.md');assert maintained.read_bytes()==installed.read_bytes()
marker='## Marsh whole side-case redraw02 and staged family preference — October 2, 2026'
lesson='''

## Marsh whole side-case redraw02 and staged family preference — October 2, 2026

Whole West02 exec-811615fc-ec19-46dd-ab38-92c84715da34 andEast02
exec-319a749d-48b8-42ed-b627-2507aa507672 redraw BOTH intermediates plus own
neutral. Exact frozen prompt/refs/source/guide SHA checked; local versions seen,
raw originals retained. Put exactcarry case authority FIRST, bodyPRIMARY SECOND,
oldmotion-only THIRD, original master FOURTH. Explicit approximate case34x23
relative to147neutral (23%width/16%height) is an authoring constraint, NOT a
license to crop/patch or separately fit crate/body. Correct rigid object growth
by complete source figures, keeping unchanged endpoints and one shared scale.

West one147 BOX .20445062586926285 gives69x120/78x102/neutral35x146 vsselected
31x147;East .20910384068278806 gives75x120/85x98/neutral36x147 vsselected32x147.
Alpha128,whole integer own-facing boot registration,no opaque clipping/mirror/
patch/recolour/perposefit. West postthreshold nominal147 gives146actual; don't
silently fit individual poses to conceal diagnostic. Both full/raw/motion/neutral
boards andusedrefs seen. Correct sidepanel/oneivoryedge latch andownEastRIGHT
implant/WestbareLEFTtemple retained. Source02 case size visually closer to exact
carry than01, especially floorpose. Width+4, head/body/grade/sole/casefloorcontact
joins remain open. Keep01 originals, prefer02 STAGED for next coherent validation;
preference is not normal admission or fullgoal/art acceptance.

Normal Marsh.update/main/grid/player02 East/West timed actions:1019checks,
16exactsource/nativepairs,252controlled20ms samples,16actor/player restores+pause.
All4poses peraction andpickup26sample/.52s transition toactualcarryroute; seeded
unload100samples/2s finalidle hold andtargetedexit.551bounded inputs including
source/master frames stable DURING interval,2931ownerfiles unchanged scratch
APPDATA,0fail/errors,exit0. All16pairs/fourboards seen. NormalarriveforcesNorth,
so these are validseeded sideunloads, not complete side delivery/expedition/
fullRunSave/visibleTitleContinue/continuouscontact/normaladmission/fullsetproof.

Side02 crossreview18completefigures/twoboards seen:12old/new half/floor/endpoint
figures plus6master/01/02neutral figures. Private family02 referencesSouthNorth01/
EastWest02:8states32slots,wholeliteral respaths,current4x130ms nonloopmetadata,
exact unchangedcarry0/selectedidle0 andwhole pickup reversals. No normalcatalog
change. Correct visiblehardware andsourcepixel parity do not prove rigidgeometry,
footcontact orbodyidentity; both source andruntime comparisons remain necessary.

Next coherent complete normal pickup/carry/turn/arrival/unload with preferred
staged family, then independent fullsaves/actualvisibleTitleContinue before normal
coherent-family admission; correct whole source poses where joins fail. Remaining
fullMarshfamilies andfull consistency/polish remain. Metadata assessments/request
updates after551interval aren't that exactcurrentfreeze;datedinterval equality
only. No livejob. Fullgoal active/incomplete, never shrink to cargo or greenchecks.
'''
for p in [ROOT/'character/ANIMATION_PIPELINE.md',ROOT/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',ROOT/'docs/CURRENT_STATUS.md',maintained]:
    with p.open(encoding='utf-8') as f:present=any(marker in line for line in f)
    if not present:
        with p.open('a',encoding='utf-8') as f:f.write(lesson)
installed.write_bytes(maintained.read_bytes())
(ROOT/'docs/MARSH_CARGO_SIDE02_HANDOFF_2026-10-02.md').write_text('''# Project handoff

Updated: October 2, 2026 · BrineSpace · Marsh whole side-case redraw02

## Objective and acceptance
Full master-matched Marsh set and cross-family consistency/polish active/incomplete.
Preferred staged held family SouthNorth01/EastWest02. No normal admission yet.

## Accepted decisions and constraints
Whole figures, exact endpoints, one neutral scale; no crate/body patches or mirrors.
Case authority first/bodyPRIMARY second; rigidcase dimensions relative toadult.
ScratchAPPDATA/owner fingerprints. Normal workshop arrival forcesNorth.

## Current state
East/West02 frozen requests/raws retained, packers and timed-state fixture(.gd+uid),
fingerprint/publish/record helpers added. side02-cross-review holds18wholefigures
andprivate8state32slot family02; side-action-02-actor-review holds16renderpairs.
Pipeline/bible/status/canonical-installed skills synchronized.01 originals preserved.
Normalcatalog/runtime unchanged. No livejob.

## Verification
1019checks,16pairs,252timed20ms samples,16restores+pause;551inputs stable during
interval,2931ownerfiles unchanged,0fail/errors,exit0. All16pairs/18crossfigures seen.
Both source02 cases closer to carry size; bodies remain wider than master (East36
vs32,West35vs31), West146actual vs147target. Proportion/head/grade/contact findings
open. Seeded sideunloads, not complete delivery/fullsave/actual visible Continue.

## Next action
Probe complete normal pickup->carry->turn->actualNortharrival->unload with preferred
staged sources. Independent fullRunSave/actual visible TitleContinue gate and whole
pose corrections where joins fail, then normal coherent-family admission. Continue
remaining full animation families and allset consistency/polish. Preserve full scope.
''',encoding='utf-8')
print(json.dumps({'checks':1019,'nativePairsReviewed':16,'crossFiguresReviewed':18,'preferredStagedFamily':'SouthNorth01/EastWest02','normalAdmission':False,'fullGoalComplete':False}))
