"""Preserve failed whole studies and record limited South drain04 improvement."""
from pathlib import Path
import json,hashlib
from PIL import Image
ROOT=Path(__file__).resolve().parents[1];B=ROOT/'character/marsh-water-transition-material-v1'
read=lambda p:json.loads(p.read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
gens={'02':'exec-9e0dbcdc-54ee-4b39-b389-6f2f564ab86a','03':'exec-6de643ae-b1a3-4699-9387-efa5245852de','04':'exec-eda61b3d-3f5d-48cb-8441-05fe390fb16f'}
sizes={'02':[[70,80],[66,92],[66,111],[64,147],[61,147]],'03':[[66,80],[65,72],[63,100],[59,147],[58,147]],'04':[[72,97],[76,81],[70,117],[65,148],[62,148]]}
for rev,gen in gens.items():
    r=read(B/f'sources/drain-south-{rev}.request.json');recipe=read(B/f'drain-south-{rev}-unselected/recipe.json');assert r['generationId']==gen
    assert sha(B/f'sources/drain-south-{rev}.raw.png')==r['rawSha256']==sha(Path(r['originalGeneratedPath'])) and sha(B/f'sources/drain-south-{rev}.prompt.txt')==r['promptSha256']
    for q in r['orderedReferences']+r['sourceFrames']:assert sha(ROOT/q['path'])==q['sha256']
    assert [q['occupiedSize'] for q in recipe['records']]==sizes[rev]
    for q in recipe['endpointRecords']:
        im=Image.open(ROOT/q['source']['path']).convert('RGBA');pad=Image.open(B/f'drain-south-{rev}-unselected'/q['file']).convert('RGBA');x=q['wholeTranslation'][0];assert pad.crop((x,0,x+im.width,im.height)).tobytes()==im.tobytes()
native=read(B/'drain-south-04-actor-review/verification.json');world=read(B/'transition-world-07-review/verification.json')
assert (native['nativeChecks'],native['samples'],native['captures'],native['playerRestores'],native['finiteAPNGHolds'],native['inputsStableDuringInterval'],native['ownerFilesUnchanged'])==(192,54,6,6,6,44,2931)
for name,v in [('water-drain-south-04-native-2026-10-03',native),('water-transition-world-07-2026-10-03',world)]:
    A=ROOT/'output/marsh-animation-audit'/name;r=read(A/'report.json');assert r['failures']==0 and (A/'native-exit.txt').read_text().strip()=='0';log=(A/'native.log').read_text();assert 'ERROR:' not in log and 'WARNING:' not in log
    for kind in ['inputs','owner']:assert read(A/f'{kind}-before.json')==read(A/f'{kind}-after.json')
assert world['actorPlayerRestores']==world['sourceNativePairs'] and world['unchangedOwnerNonLogFiles']==2931 and len(world['phases'])==12
for q in native['nativeParity']:assert sha(ROOT/q['source'])==q['sourceSha256']
for q in world['sourceParity']:assert sha(ROOT/q['path'])==q['sha256']
keys=sorted({q['key'] for q in world['sourceParity']});assert 'cargo-drain-south' in keys
reason={'02':'First70x80 remains short versus75x106swim, neutral61x147 wider than58x147master; no native02 gate.','03':'Neutral58x147 matches master but early66x80/65x72 and kneeling63x100 remain too small. Ruler agreement does not prove posed volume; no native03 gate.'}
for rev,why in reason.items():
    for p in [B/f'sources/drain-south-{rev}.request.json',B/f'drain-south-{rev}-unselected/manifest.json']:
        r=read(p);r.update(rejectedStudy=True,rejection=why);p.write_text(json.dumps(r,indent=2)+'\n')
finding='Endpoint-only04 preserves extended leg and improves first rise72x97 vs01 65x73 and exact75x106swim. One147scale .25654450261780104, second76x81 lowkneel, third70x117, planted65x148, neutral62x148 vs58x147master. Neutral width/onepixel rounding, low secondpose/caseheight, body/head/grade/camera/kick/root/contact still provisional. Two flat planted boots retained; finalstride is separate. Relative72%standing-height/129%standing-width prompt helps early shape, not reliable metric compliance or fullstyle acceptance. No perpose fitting, patches/mirrors/recolour.'
(B/'drain-south-04-actor-review/visual-assessment.json').write_text(json.dumps({'normalAdmission':False,'fullGoalComplete':False,'preferredPrivateStudy':True,'wholeSourceAndComparisonInspected':True,'nativePairedBoardsInspected':2,'nativePosePairsInspected':6,'findings':finding},indent=2)+'\n')
(B/'drain-south04-cross-review/visual-assessment.json').write_text(json.dumps({'normalAdmission':False,'fullGoalComplete':False,'revisionBoardsInspected':2,'wholeStudiesCompared':['01','02','03','04'],'findings':finding,'rejectedStudies':reason},indent=2)+'\n')
(B/'transition-world-07-review/visual-assessment.json').write_text(json.dumps({'normalAdmission':False,'fullGoalComplete':False,'nativeBoardsInspected':len(world['boards']),'sourceNativePairsInspected':world['sourceNativePairs'],'actualWitnessedKeys':keys,'findings':finding+' Normalq2 actualdispatch/Cycle/actor/grid,12phases/one extraction/safe delayedcredit/dryalive; actor-player restore/outerprocesspause. Drain0..4held planted witnessed, stride5 native-only/carrySouth0 separate. Other states unchanged; not all48loaded states, allrotations/fullSave/TitleContinue/helmet/continuousmotion/contact/fullMarsh/admission proof.'},indent=2)+'\n')
world['visualReviewed']=True;(B/'transition-world-07-review/verification.json').write_text(json.dumps(world,indent=2)+'\n')
(B/'drain-south04-cross-review/verification.json').write_text(json.dumps({'normalAdmission':False,'fullGoalComplete':False,'native':{k:native[k] for k in ['nativeChecks','samples','captures','playerRestores','inputsStableDuringInterval','ownerFilesUnchanged']},'world':{k:world[k] for k in ['checks','samples','sourceNativePairs','actorPlayerRestores','stableBoundedInputs','unchangedOwnerNonLogFiles']},'studies':sizes},indent=2)+'\n')
stats=f"World07: {world['checks']} checks, {world['samples']} samples, {world['sourceNativePairs']} source/native pairs and restored pause holds; {world['stableBoundedInputs']} stable inputs."
block=f'''

## Marsh South drain whole studies — October 3, 2026

Three whole studies retained original/raw/prompts/ordered reference SHA.02 gave
70x80/66x92/66x111/64x147/neutral61x147;03 gave66x80/65x72/63x100/59x147/
neutral58x147. Both rejected before native testing: matching a neutral ruler does
not establish posed physical volume. Do not independently fit those poses.
04 exec-eda61b3d-3f5d-48cb-8441-05fe390fb16f uses only the exact current own
master/swim/carry endpoint board enlarged together3x. No failed study or external
identity interpretation as reference. Explicit relative72%neutral height/129%
neutral width plus extended-leg geometry improves first rise72x97 versus01
65x73 and exact75x106swim. Ratios guide generation, not proof of compliance.

One147scale .25654450261780104:72x97/76x81/70x117/65x148/neutral62x148.
Low second kneel/case height, neutral62x148 versus actual58x147master and
postBOX148rounding remain defects; no perpose/ruler refit to conceal them.
Body/head/grade/camera/kick/root/contact/continuousmotion provisional. Both-flat-
feet penultimate hold preserved, finalcarry stride separate.04 is a preferred
PRIVATE study in cardinal03/combined05 only:8transitions48slots,48combined
states272slots. Two full revision boards and six native pairs/two boards inspected.

Native192checks/54samples/6restores/exactfiniteAPNGholds,44inputs stable.
{stats}
All worldboards inspected, source parity exact,12phases/safecredit/dryalive,
normal economy/failures. ScratchAPPDATA;2931owner nonlogs unchanged each interval,
zeroerrors/warnings/failures/exit0. ActualSouthdrain0..4heldplanted witnessed;
drain5 native-only, actualcarrySouth0 separate. No normal catalogue/runtime
change, all48state/allrotation/persistence/helmet/contact/fullMarsh acceptance.
Full goal remains active, including current normal228states/1190slots, not this
private subset. Next targeted repair:neutral width/lowkneel case and continuous
rise; keep whole ownmaster cross-family review and remaining full-library work.
Handoff:docs/MARSH_WATER_SOUTH_DRAIN04_HANDOFF_2026-10-03.md.
'''
canonical=ROOT/'skills/brinespace-character-pipeline/references/master-repair.md';installed=Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/master-repair.md');assert canonical.read_bytes()==installed.read_bytes()
for p in [ROOT/'character/ANIMATION_PIPELINE.md',ROOT/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',ROOT/'docs/CURRENT_STATUS.md',canonical]:
    with p.open('a',encoding='utf-8') as f:f.write(block)
installed.write_bytes(canonical.read_bytes())
handoff=f'''# Project handoff

Updated:2026-10-03 · Project:BrineSpace · Task:South drain04 whole study

## Objective and acceptance
Complete master-matched Marsh set and consistency/polish. Fullgoal active;
normal228states1190slots, private water/cargo subset not fullset acceptance.

## Accepted decisions and constraints
Whole own geometry/one neutral ruler/no patch/mirror/perposefit. Exact endpoint
whole-padding, original manifest metadata. ScratchAPPDATA, owner fingerprints,
normal resources/failures. No normal admission.

## Current state
Southdrain02/03 rejected before native gates, originals/raw/measurements retained.
04 private preferred first72x97 vsold65x73/exact75x106; second76x81 lowkneel,
third70x117,planted65x148,neutral62x148 vsactual58x147master unresolved. Three
newprep tools, packrevision04, nativeUIDmap/fingerprint/fixture+UID, world07q2
prep/fixture+UID/fingerprint/publisher/record. cardinal03eight states48slots,
combined05ordered48states272slots; all sources/reviews in water-transition root.
Pipeline/bible/status/canonical+installed skillrefs updated. No runtime/catalogue
change; all jobs terminal.

## Verification
Native192/54samples/6restores/6pairs/two boards seen,6exactfiniteAPNGholds,
44inputs stable. {stats}
All worldboards seen,12phases/one extraction/safecredit/dryalive,normalflags,
2931owner nonlogs unchanged;zeroerrors/warnings/failures/exit0. Exact endpoint
pixels preserved. ActualSouthdrain0..4 heldplanted, stride5 nativeonly/carrySouth0
separate. Body/head/case/grade/camera/kick/root/contact still provisional.
No fullSave/Continue/helmet/all48states/allrotation/fullgoal acceptance.

## Next action
Repair whole lowkneel/caseheight/neutralwidth and continuousrise. Do not replace
physical geometry with independent pose scale. Continue other visible water/dry
and full-library joins; persistence/helmet/contact and normal admission remain.
'''
(ROOT/'docs/MARSH_WATER_SOUTH_DRAIN04_HANDOFF_2026-10-03.md').write_text(handoff,encoding='utf-8');print(stats);print('Provisional improvement and rejected studies recorded; full goal active.')
