"""Record provisional whole transitions and actual combined-route evidence."""
from pathlib import Path
import json,hashlib
from PIL import Image
ROOT=Path(__file__).resolve().parents[1];B=ROOT/'character/marsh-water-transition-material-v1'
read=lambda p:json.loads(p.read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for stem,gen in [('pickup-east-01','exec-808ddeef-c10b-4bcd-80b6-47b161c16ad3'),('pickup-east-02','exec-f57f0a4c-d5fd-4882-8d19-c640a4526400'),('drain-north-01','exec-d060d494-7144-4e56-875a-bc7af6973611')]:
    r=read(B/f'sources/{stem}.request.json');assert r['generationId']==gen
    assert sha(B/f'sources/{stem}.raw.png')==r['rawSha256']==sha(Path(r['originalGeneratedPath']))
    assert sha(B/f'sources/{stem}.prompt.txt')==r['promptSha256']
    for q in r['orderedReferences']+r['sourceFrames']:assert sha(ROOT/q['path'])==q['sha256']
    recipe=read(B/f'{stem}-unselected/recipe.json')
    for q in recipe['endpointRecords']:
        source=Image.open(ROOT/q['source']['path']).convert('RGBA');padded=Image.open(B/f'{stem}-unselected'/q['file']).convert('RGBA');x=q['wholeTranslation'][0]
        assert padded.crop((x,0,x+source.width,source.height)).tobytes()==source.tobytes()
for stem,checks,samples,captures,count in [('water-pickup-east-02-native',171,47,6,40),('water-drain-north-01-native',192,54,6,40),('water-transition-world-01',15101,3680,62,1439)]:
    a=ROOT/f'output/marsh-animation-audit/{stem}-2026-10-03';r=read(a/'report.json')
    assert (r['checks'],r['failures'],len(r['samples']),len(r['captures']))==(checks,0,samples,captures)
    assert (a/'native-exit.txt').read_text().strip()=='0';log=(a/'native.log').read_text();assert 'ERROR:' not in log and 'WARNING:' not in log
    for kind,n in [('inputs',count),('owner',2931)]:
        before=read(a/f'{kind}-before.json');assert len(before)==n and before==read(a/f'{kind}-after.json')
# Do not admit first East study: wrong crouch hardware and stretched prone body.
for p in [B/'pickup-east-01-unselected/manifest.json',B/'sources/pickup-east-01.request.json']:
    r=read(p);r.update(rejectedStudy=True,rejection='First crouch exposes two frontal latches versus own side one-edge latch; last swimmer162px long versus146 endpoint. Neutral came FIRST despite requested last; observed extraction order recorded, not assumed.')
    p.write_text(json.dumps(r,indent=2)+'\n')
for stem,findings in [('pickup-east-02','Whole correction removes extra crouch latch. OwnRIGHT implant retained. Upright neutral36x147 remains wider than32x147 master; intermediate head/body/case volume,139x67 launch and158x63 late swimmer versus146x70 endpoint, quiet grade/root/contact/kick remain provisional. Exact standing and swim endpoint source pixels padded only; no body part patches/perpose fit.'),('drain-north-01','Own rear source holds case ahead beyond chest with natural rear occlusion. Four rising stages progress into planted two-foot penultimate pose, normal final carry stride. One146-target ruler rounds to147occupied after BOX/threshold (54wide vs55x146master); do not refit individual poses. Body/grade, feet/floor/case/root contact and rising physical camera remain provisional.')]:
    p=B/f'{stem}-actor-review';v=read(p/'verification.json');assert v['captures']==6 and v['finiteAPNGHolds']==6
    for q in v['nativeParity']:assert sha(ROOT/q['source'])==q['sourceSha256'] and sha(p/q['capture'])==q['captureSha256']
    (p/'visual-assessment.json').write_text(json.dumps({'normalAdmission':False,'fullGoalComplete':False,'wholeSourceAndComparisonInspected':True,'nativePairedBoardsInspected':2,'nativePosePairsInspected':6,'findings':findings},indent=2)+'\n')
p=B/'transition-world-01-review';v=read(p/'verification.json');assert v['sourceNativePairs']==62 and v['actorPlayerRestores']==62
keys=sorted({q['key'] for q in v['sourceParity']})
assessment={'normalAdmission':False,'fullGoalComplete':False,'nativeBoardsInspected':8,'sourceNativePairsInspected':62,'actualWitnessedKeys':keys,'findings':'Actual normal q0 one extraction/safe delayed credit/dryalive, all12phases, normal resource cost/failure flags; staged water banks/pickupEast02/drainNorth01/drycarry+turn+held loaded with own original manifest metadata. Pickup all6; drain slots0..4 including planted hold (final stride reference5 only native gate, world uses carryNorth0 separately). Capture drycarry and all9carryNorthSouth plus stagedSouthunload. Actual exact endpoint joins close former oldpickupEast/newEast and newNorth/oldDrainNorth. Matching normalized endpoint pixels does not prove physical root/contact/continuousmotion/kick or full art acceptance. Other pickup/drain directions remain old; no allrotations/fullSave/visibleContinue/helmet/normaladmission/fullMarsh completion.'}
(p/'visual-assessment.json').write_text(json.dumps(assessment,indent=2)+'\n');v['visualReviewed']=True;(p/'verification.json').write_text(json.dumps(v,indent=2)+'\n')
block='''

## Marsh water pickup/drain first banks — October 3, 2026

character/marsh-water-transition-material-v1 stages ownEast pickup02 and ownNorth
drain01,2of8 required directional transition states/12slots/8new intermediate
drawings, not a complete or admitted family. Originals/projectraw/prompts/ordered
body+exactendpoints+old-motion-onlyrefs/SHA retained. Pickup01 source
exec-808ddeef-c10b-4bcd-80b6-47b161c16ad3 rejected: wrong two-latch crouch case,
162px long swimmer. It placed neutral FIRST: observed order[1,2,3,4,0], not
requested layout, controls extraction. Whole correction02
exec-f57f0a4c-d5fd-4882-8d19-c640a4526400 removes extra latch; one147scale
.30434782608695654 gives89x83/85x111/139x67/158x63/neutral36x147 versus32x147master.
Still wide neutral, small intermediate head/long swimmer/body/case/grade/root/
kick/contact provisional. Reauthor whole poses; no perpart repair/perposefit.

North drain01 exec-d060d494-7144-4e56-875a-bc7af6973611, one146target scale
.2640144665461121 gives69x105/64x120/62x132/59x143/neutral54x147 vs55x146master.
Disclose postBOX/threshold rounding147; do not resize only ruler/individual poses.
Connected forward case naturally rear-occluded, not backpack. Four rise stages
culminate in TWO flat planted feet; final exactcarryNorth0 is a stride reference.
Grid holds PENULTIMATE drain pose while drying, not finalstride: preserve this
functional distinction when authoring/testing, do not replace groundedhold with
walking endpoint. Normal6pose pickup900ms(6x150);drain1040ms(120/180/220/220/180/120)
finite timing retained. Grid maps pickup through .52s actor action, and drain
rise through actual interlock elapsed60%->30% water; native player alone cannot
prove these mappings. World later witnessed their intended selection.

Whole source alpha128/BOX one ruler/integer translations/no opaque clipping,
no mirroring/patches/recolour/perposefit. Own184x184,p92 dry endpoints are padded
to224x208 and WHOLE translated20x to p112; sourceRGBA crop proof exact, noresize.
Alltransition metadata224x208,p112172,H148. Existing dry/other water clips retain
their ORIGINAL individual manifest metadata: do not concatenate their states
under a single shared pivot. combined01-cross-review/manifest-list.json freezes
ordered private original manifests, not normal catalogue admission.

Actual finite player/native gates pickup171checks/47samples/6restores and
drain192/54/6,grid frame_at_elapsed parity/stateful finite player/normal duration/
final clamp/restored sameclock holds; all12nativepairs/4boards seen,12APNG RGBAholds
exact.40inputs stable each/2931owner nonlogs unchanged,0errors/warnings/fails/exit0.
20ms(+1ms after first) samples are not exact internal-boundary proof.

Actual normal dispatched q0 combining new transition and staged water+drycargo
banks:15101checks/3680samples/62actor-player restores+outerprocess pauseholds,
62source/native pairs/8boards ALLseen,12phases/one extraction/safedelayedcredit/
dryalive,1439boundedinputs/2931owner nonlogs stable,0errors/warnings/fails/exit0.
ScratchAPPDATA throughout. Pickup6 and drain0..4 plantedhold witnessed; reference
drain5 only native while actualworld selects carryNorth0 separately. All9dry
carryNorthSouth and currentSouthcarry/unload witnessed. OldpickupEast/newEast and
newNorth/oldDrainNorth joins now exact staged endpoints, but physical camera/
root/contact/kick/grade remain provisional. Other six pickup/drain directions
stay old. Loaded manifest coverage is not allstate witness or full acceptance.
No runtime/normal catalogue changes,allrotation/fullSave/visibleContinue/helmet/
contact/coherentfamily admission/fullMarshset gate. All jobs terminal.

Next own remainingWest/South/North pickups and East/West/South drains, exact own
masters/swim/carry endpoints; then whole-volume/head/grade/camera/root/kick polish,
allroute/persistence/helmet/contact/admission and remaining full Marsh families.
Handoff: docs/MARSH_WATER_TRANSITION01_HANDOFF_2026-10-03.md.
'''
canonical=ROOT/'skills/brinespace-character-pipeline/references/master-repair.md';installed=Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/master-repair.md')
assert canonical.read_bytes()==installed.read_bytes()
for p in [ROOT/'character/ANIMATION_PIPELINE.md',ROOT/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',ROOT/'docs/CURRENT_STATUS.md',canonical]:
    with p.open('a',encoding='utf-8') as f:f.write(block)
installed.write_bytes(canonical.read_bytes())
handoff='''# Project handoff

Updated:2026-10-03 · Project:BrineSpace · Task:Marsh water transitions

## Objective and acceptance
Full master-matched Marsh animation set, followed by cross-family polish.
Goal active, incomplete. Two transition banks and green mechanics do not admit art.

## Accepted decisions and constraints
Whole organic own-direction art/no mirror/patch/recolour/perposefit. One neutral
ruler; exact source endpoints padded/20xwholetranslated184p92->224p112 only.
Each dry/water source manifest retains its own metadata in combinedprivategate.
Drain penultimate is planted HOLD; finalcarrystride is not selected during drain.
All Godot scratchAPPDATA,owner unchanged,normal costs/failures retained.

## Current state
character/marsh-water-transition-material-v1:pickupEast01 retained/rejected,
pickupEast02 and drainNorth01 provisional sources/unselected/native review,
combined01 manifest list and transition-world01 actualq0review.2of8transition
states/12slots/8new intermediate figures. Tools prepare/pack/native/fingerprint/
publish/record and3GodotscriptUIDpairs. Pipeline/bible/status/skillrefs updated.
No runtime/normal selections changed; all jobs terminal.

## Verification
Pickup171checks/47samples/6restores,drain192/54/6,all12pairs/4boards seen,
12exact APNGholds,40inputs stable each. Actualq015101checks/3680samples/
62restoredpauseholds/62pairs/8boards allseen,12phases/safecredit/dryalive,
1439inputs stable.2931ownerfiles unchanged each,0errors/warnings/fails,exit0.
Pickup6/drain0..4 and plantedhold/drycarryNorth0/all9dryNorthSouth/Southunload
witnessed. Drainreference5 nativeonly. Endpoint joins exact but volume/head/
grade/camera/ground-root/contact/kick provisional; no fullSave/helmet/allroutes/
visibleContinue/normal admission/fullset proof. NeutralNorth146target rounds147.

## Next action
Own other6pickup/drain banks from exact currentmasters+swim/drycarry endpoints;
then whole camera/body/head/grade/root/kick polish and real allroute/persistence/
helmet/contact/admission. Remaining fullMarsh families and consistency passes.
'''
(ROOT/'docs/MARSH_WATER_TRANSITION01_HANDOFF_2026-10-03.md').write_text(handoff,encoding='utf-8')
print('Provisional own water transition studies and actual combined route evidence recorded; full goal active.')
