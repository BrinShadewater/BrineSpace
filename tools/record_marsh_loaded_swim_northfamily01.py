"""Record own West/North, composed East/West and one actual normal q0 journey."""
from pathlib import Path
import json,hashlib,shutil
from PIL import Image
ROOT=Path(__file__).resolve().parents[1];B=ROOT/'character/marsh-loaded-swim-turn-material-v1';S=B/'sources'
read=lambda p:json.loads(p.read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
r=read(S/'west-north-01.request.json');assert r['generationId']=='exec-0dd0f7c4-7c73-4ab3-be0e-f72ab9b4b91e'
assert sha(S/'west-north-01.raw.png')==r['rawSha256']==sha(Path(r['originalGeneratedPath'])) and sha(S/'west-north-01.prompt.txt')==r['promptSha256']
for q in r['orderedReferences']+r['sourceFrames']:assert sha(ROOT/q['path'])==q['sha256']
recipe=read(B/'west-north-01-unselected/recipe.json');assert [q['occupiedSize'] for q in recipe['records']]==[[117,86],[99,93],[70,99],[56,146]]
reports={}
for name,checks,samples,captures,inputs in [('loaded-swim-turn-westnorth-native-01',185,44,10,52),('loaded-swim-turn-opposite-ew-native-01',345,84,18,92),('loaded-swim-northfamily-world-01',15017,3680,48,1080)]:
    a=ROOT/f'output/marsh-animation-audit/{name}-2026-10-03';report=read(a/'report.json')
    assert (report['checks'],report['failures'],len(report['samples']),len(report['captures']))==(checks,0,samples,captures)
    assert (a/'native-exit.txt').read_text().strip()=='0';log=(a/'native.log').read_text();assert 'ERROR:' not in log and 'WARNING:' not in log
    for kind,count in [('inputs',inputs),('owner',2931)]:
        before=read(a/f'{kind}-before.json');assert len(before)==count and before==read(a/f'{kind}-after.json')
    reports[name]=report
for name,captures,boards,holds in [('west-north-01',10,2,10),('opposite-ew-01',18,6,18)]:
    v=read(B/f'{name}-actor-review/verification.json');assert len(v['nativeParity'])==captures and v['finiteAPNGHolds']==holds
    for q in v['nativeParity']:assert sha(ROOT/q['source'])==q['sourceSha256'] and sha(B/f'{name}-actor-review'/q['capture'])==q['captureSha256']
    assessment={'normalAdmission':False,'fullGoalComplete':False,'nativePairedBoardsInspected':boards,'nativePosePairsInspected':captures,'wholeSourceBoardInspected':True,'findings':'Own West/North source uses bare nearLEFT temple, LEFT-leading single edge latch, quiet matte body and forward case progressively occluded, not backpack or mirrored East. First West intermediate already fairly rearward; requested yaw degrees are not verified physical angles. Head/body/case/grade/root and kick joins provisional. Composed opposite uses unchanged whole EastNorth02 and NorthWest01 figures with exact shared North04 loop0, one120ms middle; whole reverse for return. Cardinal endpoints byte-exact; no new body fitting. Native player validates finite timing/selection/restored holds/destination loop0, not full family or world acceptance.'}
    (B/f'{name}-actor-review/visual-assessment.json').write_text(json.dumps(assessment,indent=2)+'\n')
world=reports['loaded-swim-northfamily-world-01'];assert len(world['phases'])==12 and world['actorPlayerRestores']==48
assert set(world['westSlots'])==set(world['pickupSlots'])==set(range(6)) and set(world['unloadSlots'])==set(range(4)) and set(world['drainSlots'])==set(range(5))
assert set(world['turns'])=={'swim-carry-turn-east-west','swim-carry-turn-west-south'}
family=read(B/'opposite-ew-01-unselected/family-manifest.json');staged={q['id'] for q in family['states']}
assert len(staged)==10 and sum(len(q['frameFiles']) for q in family['states'])==62
w=B/'northfamily-world-01-review';v=read(w/'verification.json');assert len(v['sourceParity'])==48
for q in v['sourceParity']:assert sha(ROOT/q['path'])==q['sha256']
assert [q['sameAsNewWestLoop0'] for q in v['endpointChecks']]==[False,True,False,False]
witnessed={}
for q in v['sourceParity']:
    if q['key'] in staged:witnessed.setdefault(q['key'],[]).append(q['slot'])
assert set(witnessed)=={'swim-carry-east','swim-carry-west','swim-carry-south','swim-carry-north','swim-carry-turn-east-west'}
assert witnessed['swim-carry-east']==[0] and set(witnessed['swim-carry-turn-east-west'])==set(range(9))
for key in ['swim-carry-west','swim-carry-south','swim-carry-north']:assert set(witnessed[key])==set(range(6))
(w/'visual-assessment.json').write_text(json.dumps({'normalAdmission':False,'fullGoalComplete':False,'sourceNativePairsInspected':48,'pairedBoardsInspected':6,'stagedStatesActuallyWitnessed':witnessed,'findings':'Actual dispatched q0 completes all12phases with normal cost/failure flags, one extraction and one safe delayed credit, dry/alive. Private10state override; actual5keys witnessed, not all10. New EastWest0 equals stagedEast0, EastWest8 equals stagedWest0; all9halfturn poses and all6West/South/North loop slots captured. Old pickupEast->newEast, newWest->oldWestSouth, oldWestSouth->newSouth, newNorth->oldDrainNorth visibly change pose/body/head/case details. Own West pickup/drain endpoint mismatch is source audit only: q0 pickupEast/drainNorth. Requested yaw progression/head/grade/physicalcase/root/kick seams still provisional. Actor/player48snapshot restores plus actual outer-process pause holds pass. Not allrotations/fullRunSave/TitleContinue/helmet/physicalcontact/coherentwaterfamily/fullMarsh acceptance.'},indent=2)+'\n')
r['status']='Whole own rearLEFT source/native quarter and composed actual q0 reviewed; staged/provisional yaw/head/case/root/grade/joins, no normal admission';(S/'west-north-01.request.json').write_text(json.dumps(r,indent=2)+'\n')
op=read(S/'opposite-ew-01.request.json');op['status']='Whole composition/player and actual q0 EastWest reviewed; staged, physical joins/yaw/grade/coherent family still provisional';(S/'opposite-ew-01.request.json').write_text(json.dumps(op,indent=2)+'\n')
# Native EN02 already gated61 inputs; correct stale publisher metadata, no sprite/timing change.
en=read(B/'east-north-02-actor-review/verification.json');assert en['inputsStableDuringInterval']==61
lesson='''

## Marsh loaded-water own WestNorth and composed opposites — October 3, 2026

Own rearLEFT whole source exec-0dd0f7c4-7c73-4ab3-be0e-f72ab9b4b91e retained
with frozen exact prompt/ordered five refs/original/raw/ref SHA. Paired own
West/North masters and staged West01/North04 endpoints, old motion only,
original West/North identity. NearLEFT temple BARE, leadingLEFT case latch,
progressive forward-case occlusion, never mirror East or draw backpack.
One North146 BOX scale .23434991974317818:117x86/99x93/70x99/neutral56x146
versus own master55x146. Alpha128 unequal whole cells, integer whole midpoint
registration, no clipping/patch/recolour/mirror/per-pose fit. First West yaw
already fairly rearward; labels22.5/45/67.5 are requested angles, not proof of
physical yaw. Proportions/grade/head/case/leg cadence/world root remain open.

Paired WestNorth/NorthWest400ms player185checks/44samples,10restores/same-clock
holds. All10old/staged native pairs on2boards seen;10finite APNG holds exact.
52inputs stable DURING interval,2931ownerfiles unchanged scratchAPPDATA,
0errors/warnings/fails,exit0. Player scope distinct from actual world.

Composed EastWest/WestEast800ms: unchanged whole EastNorth02 plus NorthWest01,
exact shared North04 loop0 once at120ms,9poses per direction. Reverse whole
sequence, never mirror/raster fit. Old reverse pixel sequence also verified
against current catalogue. Opposite player345checks/84samples,18restores/holds,
all18pairs/6boards seen;18finite APNG decoded holds exact. Samples use20ms
steps with1ms offset after initial to avoid ambiguous floating boundaries;
not exact internal-boundary testing.92inputs/2931ownerfiles stable,
0errors/warnings/fails,exit0. Private family4loops+6turns=10states/62slots,
22unique swimming figures; turn coverage6states/38slots of required12/76.
No new authored opposite drawings or normal catalogue/runtime admission.

Fresh actual normal q0 expedition loads private10state family, old other
clips:15017checks/3680controlled20ms samples/48exact source-native pairs,
48actor/player restores and outer-process paused holds, all12phases, one
extraction/one safe delayed credit, dry/alive. All48pairs/6boards inspected.
1080bounded inputs stable DURING interval,2931ownerfiles unchanged scratch,
0errors/warnings/fails,exit0. Actually witnessed stagedEast slot0, all6West/
South/North timing slots, all9EastWest poses:5keys, not all10 loaded states.
Actual EastWest first/last now exact own East/West loop0 bytes; midpoint is
exact North04. Native quarter controls separately cover WestNorth/NorthWest;
do not call q0 direct quarter coverage just because it reuses their figures.

Mixed joins visible: old pickupEast->newEast, newWest->oldWestSouth,
oldWestSouth->newSouth, newNorth->oldDrainNorth. West pickup/drain endpoint
mismatch remains source-only; q0 uses pickupEast/drainNorth. Green mechanics
and endpoint aliases are not continuous kick/body/physicalcase/root acceptance.
No allrotation/fullRunSave/freshvisibleContinue/helmet/coherent-family/fullgoal
acceptance. Requests/assessments/publisher/family metadata changed after freezes:
scope stability to dated intervals. EN02 publisher's stale49 displayed-input
count corrected to actual61 (gate already required61); derive published counts
from verified input maps to avoid stale template metrics, not new gameplay tests.

Next own EastSouth/WestSouth quarters, compose NorthSouth viaEast, then whole
pickup/drain and real route/contact/persistence/helmet/admission. Remaining dry
cargo/full Marsh families and cross-library consistency/polish active/incomplete.
All current jobs terminal. Handoff:
docs/MARSH_LOADED_SWIM_NORTHFAMILY01_HANDOFF_2026-10-03.md.
'''
canonical=ROOT/'skills/brinespace-character-pipeline/references/master-repair.md';installed=Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/master-repair.md');assert canonical.read_bytes()==installed.read_bytes()
for p in [ROOT/'character/ANIMATION_PIPELINE.md',ROOT/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',ROOT/'docs/CURRENT_STATUS.md',canonical]:
    with p.open('a',encoding='utf-8') as f:f.write(lesson)
shutil.copyfile(canonical,installed)
handoff='''# Project handoff

Updated: October 3, 2026 · Project: BrineSpace · Task: Marsh North-route water turns

## Objective and acceptance
Full master-matched Marsh set and cross-library consistency/polish active/incomplete.
New own West/North and composed East/West water turns are staged, not accepted.

## Accepted decisions and constraints
Own directional body/head/temple/case/camera/grade, whole figures/one neutral
scale, no mirrors/patches/per-pose fit. Forward case, scratch APPDATA for probes.

## Current state
character/marsh-loaded-swim-turn-material-v1: ownWestNorth01 raw/prompt/request/
frames, paired quarter manifest/APNG/reviews. opposite-ew01 whole composition
and private family10states/62slots/22figures;6of12turns/38of76turn slots covered.
Northfamily-world01 review retains actualq0 captures/source parity/sixboards.
New preparation/packing/assembly/native/fingerprint/publish/record tools and
three paired Godot script UIDs. Pipeline/bible/status/both skill refs updated.
EN02 display-count metadata corrected61, original gate intact. All jobs terminal.
No normal catalogue/runtime selection changed.

## Verification
Quarter185checks/44samples/10restores, opposite345/84/18, exact finiteAPNGs
10/18. All28player native pairs/8boards seen. Actualq015017checks/3680samples/
48pairs+restoredpauseholds,12phases, dry/alive/safecredit;all6worldboards seen.
52/92/1080inputs stable respective intervals,2931ownerfiles unchanged each,
0errors/warnings/fails,exit0. q0 witnesses5newkeys, not all10 override states.
Yaw/head/case/grade/root/kick/mixed old pickup/drain/WestSouth remain provisional.
No allrotation/fullsave/visibleContinue/helmet/contact/fullfamily admission gate.

## Next action
Own EastSouth and WestSouth quarter sources, compose NorthSouth viaEast and
reverse. Then whole pickup/drain, coherent joins/real routes/persistence/helmet/
physical contact/normal admission. Remaining full Marsh set and polish.
'''
(ROOT/'docs/MARSH_LOADED_SWIM_NORTHFAMILY01_HANDOFF_2026-10-03.md').write_text(handoff,encoding='utf-8')
print('Own WestNorth/composed opposites/actual q0 evidence recorded; full goal active and incomplete.')
