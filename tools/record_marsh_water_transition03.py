"""Record inspected, provisional cardinal transitions and terminal native/world evidence."""
from pathlib import Path
import json,hashlib
from PIL import Image
ROOT=Path(__file__).resolve().parents[1];B=ROOT/'character/marsh-water-transition-material-v1'
read=lambda p:json.loads(p.read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
findings={
 'pickup-north-02':'Strict full rear heading improves on rejected diagonal01. One146scale .29141716566866266 gives78x98/74x147/70x134/71x112/neutral59x146 vs55x146master/69x104swim. Lift is nearly upright, launch/root/physicalcamera/head/case/body/material/kick continuity still provisional.',
 'pickup-south-01':'Observed neutral FIRST; reorder whole cells [1,2,3,4,0]. One147scale .26534296028880866 gives87x93/68x115/98x90/81x85/neutral59x147 matches master bounds. Third stage visibly diagonal; late kick/projection differs from75x106exact swimmer. Right implant viewerLEFT/two front latches retained. Case/head/body/camera/material/root/contact provisional.',
 'drain-east-01':'One147scale .2578947368421053 gives116x92/70x116/68x128/51x147/neutral36x147 vs32x147master. OwnRIGHT implant/one outerRIGHT latch, penultimate both flat feet. Neutral/body wider, case/root/kick/grade/camera/contact provisional. Final carry stride is separate from drain planted hold.',
 'drain-west-01':'One147scale .27121771217712176 gives132x74/87x110/62x137/50x146/neutral33x146 vs31x147master.147target ends146postBOX/threshold, disclosed without refit. NearLEFT temple bare/one outerLEFT latch, penultimate both flat feet. Width/body/case/grade/camera/kick/root/contact provisional.'}
generations={'pickup-north-01':'exec-74b89405-3b5a-4356-a81c-6155f352df12','pickup-north-02':'exec-9aad48a0-f575-4a34-b70b-5a430143390f','pickup-south-01':'exec-13143c46-7dd9-4616-91f5-f23d7d2478b3','drain-east-01':'exec-07658041-db17-4df0-a7ec-278bef2e4abf','drain-west-01':'exec-4127accf-5ede-4f6b-90aa-37111e360ce9'}
for stem,gen in generations.items():
    r=read(B/f'sources/{stem}.request.json');assert r['generationId']==gen
    assert sha(B/f'sources/{stem}.raw.png')==r['rawSha256']==sha(Path(r['originalGeneratedPath']))
    assert sha(B/f'sources/{stem}.prompt.txt')==r['promptSha256']
    for q in r['orderedReferences']+r['sourceFrames']:assert sha(ROOT/q['path'])==q['sha256']
    for q in read(B/f'{stem}-unselected/recipe.json')['endpointRecords']:
        source=Image.open(ROOT/q['source']['path']).convert('RGBA');padded=Image.open(B/f'{stem}-unselected'/q['file']).convert('RGBA');x=q['wholeTranslation'][0]
        assert padded.crop((x,0,x+source.width,source.height)).tobytes()==source.tobytes()
native={}
for stem,description in findings.items():
    O=B/f'{stem}-actor-review';v=read(O/'verification.json')
    assert v['nativeChecks']==(171 if stem.startswith('pickup') else 192) and v['captures']==6 and v['finiteAPNGHolds']==6 and v['ownerFilesUnchanged']==2931 and v['errors']==v['warnings']==v['failures']==v['exitCode']==0
    for q in v['nativeParity']:assert sha(ROOT/q['source'])==q['sourceSha256'] and sha(O/q['capture'])==q['captureSha256']
    native[stem]={k:v[k] for k in ['nativeChecks','samples','captures','playerRestores','inputsStableDuringInterval','ownerFilesUnchanged']}
    (O/'visual-assessment.json').write_text(json.dumps({'normalAdmission':False,'fullGoalComplete':False,'wholeSourceAndComparisonInspected':True,'nativePairedBoardsInspected':2,'nativePosePairsInspected':6,'findings':description},indent=2)+'\n')
for p in [B/'sources/pickup-north-01.request.json',B/'pickup-north-01-unselected/manifest.json']:
    r=read(p);r.update(rejectedStudy=True,rejection='Diagonal rear-right launch violates fixed North heading; retained original/raw/measurements. No native01 gate. Reauthored whole as02, never raster-rotated/patched.');p.write_text(json.dumps(r,indent=2)+'\n')
world={}
for rev in ['03','04','05']:
    O=B/f'transition-world-{rev}-review';v=read(O/'verification.json')
    assert v['failures']==0 and v['unchangedOwnerNonLogFiles']==2931 and v['actorPlayerRestores']==v['sourceNativePairs'] and len(v['phases'])==12
    for q in v['sourceParity']:assert sha(ROOT/q['path'])==q['sha256']
    keys=sorted({q['key'] for q in v['sourceParity']})
    if rev=='03':assert 'swim-pickup-south' in keys and 'cargo-drain-east' in keys
    if rev=='04':assert 'swim-pickup-west' in keys and 'cargo-drain-west' in keys and 'swim-pickup-north' not in keys
    if rev=='05':assert 'swim-pickup-north' in keys
    assessment={'normalAdmission':False,'fullGoalComplete':False,'nativeBoardsInspected':len(v['boards']),'sourceNativePairsInspected':v['sourceNativePairs'],'actualWitnessedKeys':keys,'findings':'Whole source/native pairs inspected. Actual normal dispatch, twelve phases, one extraction/safe delayed credit/dry alive, actor/player restores and outer-process pause holds. Native source exact. Drain0..4 includes plantedhold; carrystride separately selected, drain5 native-only. Head/body/case/grade/camera/kick/root/contact provisional; doorway occlusion visible. Airlock rotation does not determine final site pickup heading: q3 was West, not inferred North; straight q0 northern site adds explicit planned and actual North heading gates. Dated q0/q2 earlier revisions plus q1/q3/straight q0 now cover all eight directional transitions, not one unchanged all-rotation run, all48loaded states or fullMarsh acceptance. FullSave/visibleContinue/helmet/continuouscontact/admission remain open.'}
    (O/'visual-assessment.json').write_text(json.dumps(assessment,indent=2)+'\n');v['visualReviewed']=True;(O/'verification.json').write_text(json.dumps(v,indent=2)+'\n')
    world[rev]={k:v[k] for k in ['checks','sourceNativePairs','samples','actorPlayerRestores','stableBoundedInputs','unchangedOwnerNonLogFiles']};world[rev]['actualKeys']=keys
family=read(B/'cardinal01-cross-review/family-manifest.json');assert len(family['states'])==8 and sum(len(s['frameFiles']) for s in family['states'])==48
(B/'cardinal01-cross-review/verification.json').write_text(json.dumps({'normalAdmission':False,'fullGoalComplete':False,'states':8,'slots':48,'newWholeIntermediateDrawings':32,'native':native,'world':world,'limits':'Coverage and mechanical gates only; full cross-family art/contact/persistence/helmet/admission remain open.'},indent=2)+'\n')
block='''

## Marsh cardinal water transitions — October 3, 2026

All eight pickup/drain directions now have private staged candidates (48 slots,
32 new whole intermediate drawings). Preferred pickup E02/W03/N02/S01; drain
E01/W01/N01/S01. `cardinal01-cross-review/family-manifest.json` combines only
matching224x208/p112,172/H148 metadata. `combined03-cross-review/manifest-list.json`
retains original dry/water metadata:48private states/272slots, not all witnessed.
No normal catalogue/runtime admission. Full Marsh goal remains active.

North01 turned rear-right during launch and was rejected before native testing.
North02 reauthors the whole source with strict heading and exact own endpoints
enlarged together3x; failed01 is excluded as reference. Heading improves, but
neutral59x146 vs55x146master and nearly upright lift remain provisional. South01
neutral was FIRST: observed whole order[1,2,3,4,0], never assume the prompt order.
South neutral59x147 matches master bounds but third pose turns diagonally and
late kick differs. East drain neutral36x147 vs32x147master; West33x146 vs31x147,
147target rounded146afterBOX/threshold. Both side drains hold two flat feet in
penultimate pose; finalcarry stride is selected separately. Head/body/case/grade,
camera, kick, physical root/contact and coherent joins still need polish.
All original/raw/prompt/reference order/SHA retained, one common neutral ruler,
whole integer registration and exact padded endpoints; no perposefit, mirrors,
limb/head/prop patches or raster recolouring. Full measurements and generation
IDs are in source request/recipe and actor-review visual-assessment JSON.

Four new native gates:North02/South01 pickup171checks/47samples each; East/West
drain192/54 each.24native poses/restores/exact finiteAPNG holds,8paired boards
all inspected. Stable input counts41/42/43/43 respectively,2931owner nonlogs
unchanged, zeroERROR/WARNING/failures/exit0. Gates exercise actual finite player
and grid API, not actor/contact/fullSave proof.

Normal q1 Southpickup/Eastdrain:15513checks/3783samples/62captures+restored holds,
1905inputs stable; q3 Westpickup/Westdrain:14761/3589/66,2038stable. All native
boards inspected, source parity exact. Both complete12phases/one extraction/
safe delayedcredit/dryalive with normal economy/failures, scratchAPPDATA and
2931owner nonlogs unchanged. q3 disproved the inferred Northpickup: actual
pathfinders final site approach determines pickup heading, not airlockrotation.
A separate straight northern q0 site explicitly gates planned/actual Northpickup:
12920checks/3146samples/50captures+restoredholds,2181inputs stable. All7boards
inspected, zeroerrors/warnings/failures/exit0,2931owner nonlogs unchanged.
Across dated q0/q2 and these new routes all8transition directions witnessed,
not one unchanged allrotation run or all48loaded states. FullSave/TitleContinue,
helmet, physical-contact/coherent-family admission and other Marsh families
remain open. Next:whole cross-family camera/volume/head/case/grade/root/kick
polish. Handoff:docs/MARSH_WATER_TRANSITION03_HANDOFF_2026-10-03.md.
'''
canonical=ROOT/'skills/brinespace-character-pipeline/references/master-repair.md';installed=Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/master-repair.md');assert canonical.read_bytes()==installed.read_bytes()
for p in [ROOT/'character/ANIMATION_PIPELINE.md',ROOT/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',ROOT/'docs/CURRENT_STATUS.md',canonical]:
    with p.open('a',encoding='utf-8') as f:f.write(block)
installed.write_bytes(canonical.read_bytes())
handoff='''# Project handoff

Updated:2026-10-03 · Project:BrineSpace · Task:Marsh cardinal water transitions

## Objective and acceptance
Complete master-matched Marsh set, then cross-family consistency/polish.
Goal active; coverage and playback gates do not establish coherent art acceptance.

## Accepted decisions and constraints
Whole own-direction authoring, one neutral ruler; no mirrors/patches/perposefit.
Exact dry endpoints padded184p92->224p112 via whole20px translation. Preserve
original metadata per manifest, planted drainhold/finalcarry separate. Scratch
APPDATA, owner fingerprints, normal economy/failures; no normal admission yet.

## Current state
character/marsh-water-transition-material-v1:North01 rejected/retained,North02,
Southpickup01,East/Westdrain01 provisional. All8directions/48slots/32new whole
intermediates in cardinal01; orderedcombined03 includes48states/272slots.
New North02prep, generic native/fingerprint updates and four paired UIDfixtures;
world03q1/world04q3/world05straightNorth fixtures/prep/fingerprints/publisher/
record tools. Pipeline, bible, status, canonical+installed skillrefs updated.
No runtime/catalogue change. All jobs terminal after recording.

## Verification
Four native gates:pickup171/47each,drain192/54each,24captures/restores/exactAPNG
holds; all8boards inspected; inputs41/42/43/43stable. Worlds and actual keys:
'''+''.join(f"World{rev}: {v['checks']}checks/{v['samples']}samples/{v['sourceNativePairs']}pairs+restores, {v['stableBoundedInputs']}inputs stable.\n" for rev,v in world.items())+'''
All worldboards inspected, source parity exact,12phases/safe credit/dryalive,
restored pauseholds, zeroerrors/warnings/failures/exit0.2931owner nonlogs unchanged.
q3actualpickupWest disproved inferredNorth; straight q0 explicitly gates North.
All8transition directions witnessed across dated runs, not one immutable allroute
revision or all48loaded states. Art/body/head/case/grade/camera/kick/root/contact
still provisional; fullSave/Continue/helmet/admission/fullgoal acceptance open.

## Next action
Whole cross-family polish beginning with visible pickup size/kick/root joins and
side neutral/case/body width. Reauthor whole geometry from own masters/endpoints,
measure one ruler and visually review; then meaningful persistence/helmet/contact
and normal admission checks plus remaining fullMarsh families.
'''
(ROOT/'docs/MARSH_WATER_TRANSITION03_HANDOFF_2026-10-03.md').write_text(handoff,encoding='utf-8')
print('Provisional eight-direction coverage and actual-route evidence recorded; full goal active.')
