"""Record terminal front-quarter, opposite and actual journey evidence."""
from pathlib import Path
import json,hashlib
ROOT=Path(__file__).resolve().parents[1];B=ROOT/'character/marsh-loaded-swim-turn-material-v1'
read=lambda p:json.loads(p.read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for name,checks,samples,captures,count in [('loaded-swim-turn-eastsouth-native-01',185,44,10,49),('loaded-swim-turn-westsouth-native-01',185,44,10,49),('loaded-swim-turn-opposite-ns-native-01',345,84,18,112),('loaded-swim-allfamily-world-01',15017,3680,48,1268)]:
    a=ROOT/f'output/marsh-animation-audit/{name}-2026-10-03';r=read(a/'report.json')
    assert (r['checks'],r['failures'],len(r['samples']),len(r['captures']))==(checks,0,samples,captures)
    assert (a/'native-exit.txt').read_text().strip()=='0'
    log=(a/'native.log').read_text();assert 'ERROR:' not in log and 'WARNING:' not in log
    for kind,n in [('inputs',count),('owner',2931)]:
        before=read(a/f'{kind}-before.json');assert len(before)==n and before==read(a/f'{kind}-after.json')
for side,gen in [('east','exec-73c5df9f-b7e3-448d-ba38-6e6987ee0cb3'),('west','exec-770a7733-7cb9-481e-8f3d-a04f61c16204')]:
    r=read(B/f'sources/{side}-south-01.request.json');assert r['generationId']==gen
    assert sha(B/f'sources/{side}-south-01.raw.png')==r['rawSha256']==sha(Path(r['originalGeneratedPath']))
    for q in r['orderedReferences']+r['sourceFrames']:assert sha(ROOT/q['path'])==q['sha256']
for name,boards,pairs in [('east-south-01',2,10),('west-south-01',2,10),('opposite-ns-01',6,18)]:
    v=read(B/f'{name}-actor-review/verification.json');assert len(v['nativeParity'])==pairs and v['finiteAPNGHolds']==pairs
    (B/f'{name}-actor-review/visual-assessment.json').write_text(json.dumps({'normalAdmission':False,'fullGoalComplete':False,'nativePairedBoardsInspected':boards,'nativePosePairsInspected':pairs,'wholeComparisonInspected':True,'findings':'Whole own-front swimmers maintain case support and side/front latch transition. East ownRIGHT temple remains near/viewerLEFT; West nearLEFT is bare. Requested22.5/45/67.5 degrees are not physically verified: shallow remains too profile and last intermediate already almost frontal. One South147 scale yields147-high neutral but swimmer/head/case volume and kick/root jump into larger South endpoint remain provisional. NorthSouth composed unchanged whole NorthEast02 plus EastSouth01, one exactEast120ms center. Whole sequence reversed for return, not mirrored. Native finite player gates and exact endpoint joins do not establish art acceptance or world physical-root/contact.'},indent=2)+'\n')
world=read(B/'allfamily-world-01-review/verification.json');assert world['sourceNativePairs']==48 and world['actorPlayerRestores']==48
keys=sorted({q['key'] for q in world['sourceParity']});assert len(keys)==9
assessment={'normalAdmission':False,'fullGoalComplete':False,'nativeBoardsInspected':6,'sourceNativePairsInspected':48,'actualWitnessedKeys':keys,'actualStagedWitnessedKeys':[k for k in keys if k.startswith('swim-carry')],'findings':'Actual normal q0 one extraction/safe delayed credit/dry alive, normal cost and resource failure flags retained. Six staged keys witnessed: four loops (East slot0 only, other three six timing slots) and all9EastWest/all5WestSouth poses. All16states loaded is not all16states witnessed. Exact West join into ownWestSouth and exactSouth handoff close former mixed old turn joins. Visual head/body/case/grade/yaw/root/kick remain provisional; old pickupEast to newEast and newNorth to oldDrainNorth remain mismatches. Westpickup/drain mismatches are source-only in q0; actual pickupEast/drainNorth. No allrotation/fullsave/visibleContinue/helmet/contact/coherentfamily admission/fullMarsh acceptance.'}
(B/'allfamily-world-01-review/visual-assessment.json').write_text(json.dumps(assessment,indent=2)+'\n')
world['visualReviewed']=True;(B/'allfamily-world-01-review/verification.json').write_text(json.dumps(world,indent=2)+'\n')
block='''

## Marsh loaded-water complete turn coverage — October 3, 2026

Own EastSouth01 (exec-73c5df9f-b7e3-448d-ba38-6e6987ee0cb3) and
WestSouth01 (exec-770a7733-7cb9-481e-8f3d-a04f61c16204) whole sources retained
with original copies, frozen prompts/ordered own body/endpoints/old-motion-only
references and SHA provenance. Both own fronts were authored independently,
never mirrored. Current South master is candidate-01/000.png,59x147, not the
historical South idle. One147 neutral ruler, alpha128/BOX, whole integer
translation/no opaque clipping: East scale.2300469483568075 gives138x56/108x66/
66x75/neutral57x147; West.24459234608985025 gives135x59/124x66/73x78/58x147.
224x208,p112172,H148 metadata unchanged. Exact own loop0 endpoints referenced,
3whole intermediate poses each; whole reverse for return, finite400ms.

Requested yaw22.5/45/67.5 is not angle proof: shallow figures remain fairly
profile, last intermediate almost frontal. Head/body/case volume, quiet matte
grade, kick/root and size jump into South remain provisional. Matching neutral
height does not make foreshortened swimmer volume match. Reauthor whole figure
when needed; never fix this with separate limb/head edits or per-pose fitting.
Own West nearLEFT temple stays bare; RIGHT implant must emerge naturally at
front on viewerLEFT. Case one side latch transitions to two frontal latches.

NorthSouth/SouthNorth assembled via exactEast02 loop0, unchanged whole
NorthEast02 plus EastSouth01. Nine poses800ms, one120ms central hold,
whole reverse for return. Private opposite-ns-01-unselected/family-manifest.json
has4loops+12turns=16states/100timing slots/28unique swimming drawings. This is
coverage, not coherent water-family acceptance or the full Marsh set.

Native actual directed player gates: EastSouth185checks/44samples/10restores,
WestSouth185/44/10, NorthSouth345/84/18; all38native pose pairs on10boards
inspected,38finiteAPNG decoded RGBAholds exact. Inputs49/49/112 stable respective
intervals; owner2931nonlogs unchanged,0errors/warnings/fails,exit0. Opposite
samples20ms(+1ms after initial) avoid floating boundary ambiguity, not exact
internal-boundary testing. Preserve scripts and their paired UIDs.

Actual normal dispatched q0 with all16states loaded:15017checks/3680samples,
48actor/player restores+outerprocess paused holds,48source/native pairs on6
boards all inspected,12phases,one extraction/safe delayed credit/dry alive.
1268bounded inputs/2931owner nonlogs unchanged,0errors/warnings/fails,exit0.
ScratchAPPDATA throughout. Actually witnessed6staged keys: all4loops (East0
only,others all6timingslots),EastWest all9,WestSouth all5. Loaded coverage must
never be reported as witnessed coverage. Exact West->WestSouth->South source
joins now close former mixed old turn joins. Physical root/kick/art still open.
Old pickupEast->newEast and newNorth->oldDrainNorth remain mismatches; q0's
Westpickup/drain comparisons are source-only. Other old unload retained.
No normal catalogue selection/runtime admission changed; no allrotation/fullSave/
visibleContinue/helmet/contact/coherentwaterfamily/fullMarsh acceptance.

Next: whole master-matched swim-pickup/cargo-drain banks, cross-family volume/
grade/camera/kick/root polish, actual allroute/contact/persistence/helmet gates
before admission, remaining full Marsh animations and final consistency passes.
Evidence: docs/MARSH_LOADED_SWIM_ALLFAMILY01_HANDOFF_2026-10-03.md.
'''
canonical=ROOT/'skills/brinespace-character-pipeline/references/master-repair.md'
installed=Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/master-repair.md')
assert canonical.read_bytes()==installed.read_bytes()
for p in [ROOT/'character/ANIMATION_PIPELINE.md',ROOT/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',ROOT/'docs/CURRENT_STATUS.md',canonical]:
    with p.open('a',encoding='utf-8') as f:f.write(block)
installed.write_bytes(canonical.read_bytes())
handoff='''# Project handoff

Updated: 2026-10-03 · Project: BrineSpace · Task: Marsh complete water-turn coverage

## Objective and acceptance
Full master-matched Marsh animation set, then cross-family consistency/polish.
Goal remains active: coverage and mechanic gates are not final art acceptance.

## Accepted decisions and constraints
Whole organic sources only, own West never mirrored. Own South current master
59x147; one147 ruler for front turns, alpha128/BOX/no opaque clipping. Exact
cardinal loop0 endpoints and whole reverse, original water timing/metadata.
Private overrides only. All Godot tests scratchAPPDATA; owner folder untouched.

## Current state
character/marsh-loaded-swim-turn-material-v1: east-south-01 and west-south-01
sources/unselected/native-review banks; opposite-ns-01 viaEast plus full private
family16states/100slots/28unique figures. allfamily-world-01-review actualq0.
New generic preparation/packing/native/fingerprint/publish/record tools and
three paired Godot UIDs. Pipeline/bible/status/canonical+installed skill refs
updated. Originals retained. No normal selection/runtime changes. Jobs terminal.

## Verification
Front banks each185checks/44samples/10restores, opposite345/84/18; all38native
pairs/10boards inspected,38exact finite APNGholds. Actualq015017checks/3680samples/
48restoredpauseholds/48pairs/6boards all inspected,12phases/safecredit/dryalive.
Inputs49/49/112/1268 stable,owner2931 unchanged each,0errors/warnings/fails,exit0.
q0 witnesses6newkeys, not all16loadedstates. WestSouth joins exact; South size/
kick/root jump and head/body/case/grade/yaw provisional. Old pickup/drain still
mixed. No allrotation/fullsave/visibleContinue/helmet/contact/admission gate.

## Next action
Whole swim-pickup/cargo-drain source banks anchored to current own masters and
exact swim endpoints; then coherent join/body/grade/camera/kick/root polish,
allroute/persistence/helmet/contact/normal admission. Remaining Marsh fullset.
'''
(ROOT/'docs/MARSH_LOADED_SWIM_ALLFAMILY01_HANDOFF_2026-10-03.md').write_text(handoff,encoding='utf-8')
print('Complete turn coverage and provisional art findings recorded; full goal remains active.')
