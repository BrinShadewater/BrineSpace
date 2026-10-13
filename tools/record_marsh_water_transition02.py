"""Retain rejected whole studies and record provisional West/South evidence."""
from pathlib import Path
import json,hashlib
from PIL import Image
ROOT=Path(__file__).resolve().parents[1];B=ROOT/'character/marsh-water-transition-material-v1'
read=lambda p:json.loads(p.read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
for stem,gen in [('pickup-west-01','exec-5ecafa91-1d33-4ecc-a383-f566a6de5cbc'),('pickup-west-02','exec-fbd28398-c619-4790-b46e-2f8eb18cdcb3'),('pickup-west-03','exec-07100148-723d-473f-ad9d-965db6e93c69'),('drain-south-01','exec-2d85c090-1ba4-4843-8061-0effed02f120')]:
    r=read(B/f'sources/{stem}.request.json');assert r['generationId']==gen
    assert sha(B/f'sources/{stem}.raw.png')==r['rawSha256']==sha(Path(r['originalGeneratedPath']))
    assert sha(B/f'sources/{stem}.prompt.txt')==r['promptSha256']
    for q in r['orderedReferences']+r['sourceFrames']:assert sha(ROOT/q['path'])==q['sha256']
    recipe=read(B/f'{stem}-unselected/recipe.json')
    for q in recipe['endpointRecords']:
        source=Image.open(ROOT/q['source']['path']).convert('RGBA');padded=Image.open(B/f'{stem}-unselected'/q['file']).convert('RGBA');x=q['wholeTranslation'][0]
        assert padded.crop((x,0,x+source.width,source.height)).tobytes()==source.tobytes()
for stem,checks,samples,captures,count in [('water-pickup-west-03-native-2026-10-03',171,47,6,40),('water-drain-south-01-native-2026-10-03',192,54,6,40),('water-transition-world-02-2026-10-03-retry1',15221,3710,62,1653)]:
    a=ROOT/f'output/marsh-animation-audit/{stem}';r=read(a/'report.json')
    assert (r['checks'],r['failures'],len(r['samples']),len(r['captures']))==(checks,0,samples,captures)
    assert (a/'native-exit.txt').read_text().strip()=='0';log=(a/'native.log').read_text();assert 'ERROR:' not in log and 'WARNING:' not in log
    for kind,n in [('inputs',count),('owner',2931)]:
        before=read(a/f'{kind}-before.json');assert len(before)==n and before==read(a/f'{kind}-after.json')
failed=ROOT/'output/marsh-animation-audit/water-transition-world-02-2026-10-03'
assert (failed/'native-exit.txt').read_text().strip()=='1' and 'actual normal expedition dispatch' in (failed/'native.log').read_text()
for kind in ['inputs','owner']:assert read(failed/f'{kind}-before.json')==read(failed/f'{kind}-after.json')
for stem,reason in [('pickup-west-01','Superseded study: launch164x90/late160x56, neutral33x148 vs31x147 master; nearLEFT temple bare/case oneLEFT latch correct, but length/volume drift. No native01 gate.'),('pickup-west-02','Rejected correction: launch157x80/late178x55 worse; neutral34x147. No native02 gate. Reauthor whole geometry, never accept a correction merely because newer.')]:
    for p in [B/f'{stem}-unselected/manifest.json',B/f'sources/{stem}.request.json']:
        r=read(p);r.update(rejectedStudy=True,rejection=reason);p.write_text(json.dumps(r,indent=2)+'\n')
for stem,findings in [('pickup-west-03','Whole third source uses enlarged3x same-scale master/endpoints as Primary and compact folded knees; improves launch150x65 and head readability, retains bare nearLEFT temple and one outerLEFT case latch. Late163x56 remains longer/larger than141x54 endpoint, neutral33x147 vs31x147. Quiet matte grade/physical case/head/body/camera/root/contact/kick still provisional, not accepted. Whole reauthoring without mirrors/patches/perposefit.'),('drain-south-01','Neutral59x147 matches current ownSouth master bounds. FrontRIGHT implant viewerLEFT/two frontal ivory case latches retained; planted penultimate60x147 with both feet flat. First rising65x73 vs75x106 swim endpoint gives visible early size/kick jump; intermediate case/body/head/grade/camera/contact/root continuity provisional. Normal finalcarry stride is separate from held planted pose.')]:
    p=B/f'{stem}-actor-review';v=read(p/'verification.json');assert v['captures']==6 and v['finiteAPNGHolds']==6
    for q in v['nativeParity']:assert sha(ROOT/q['source'])==q['sourceSha256'] and sha(p/q['capture'])==q['captureSha256']
    (p/'visual-assessment.json').write_text(json.dumps({'normalAdmission':False,'fullGoalComplete':False,'wholeSourceAndComparisonInspected':True,'nativePairedBoardsInspected':2,'nativePosePairsInspected':6,'findings':findings},indent=2)+'\n')
p=B/'transition-world-02-review';v=read(p/'verification.json');assert v['sourceNativePairs']==62 and v['actorPlayerRestores']==62
keys=sorted({q['key'] for q in v['sourceParity']})
assessment={'normalAdmission':False,'fullGoalComplete':False,'nativeBoardsInspected':8,'sourceNativePairsInspected':62,'actualWitnessedKeys':keys,'findings':'Actual normal q2 home20,21/target19,24/airlockrotation2 with normal resources/failures and authored free airlock/site fixture. One extraction/safe delayed credit/dryalive,12phases. PickupWest all6; drainSouth slots0..4 including plantedhold, finalstride5 nativeonly while carrySouth0 selected separately; all9drySouthNorth/Northcarry4/Northunload4. Exact endpoint aliases close oldWestpickup/newWest and newSouth/oldSouthdrain joins. Case/head/body/grade/watercamera/kick/physicalroot/contact provisional; natural doorbeam occlusion visible in dry turn. Not all44loaded states witnessed; no allrotation/fullSave/visibleContinue/helmet/contact/admission/fullMarsh proof. Initial dispatch failure was q2 fixture retaining q0 wreck-clear region; corrected established q2 region and passed fresh scratch retry. Failed audit retained unchanged.'}
(p/'visual-assessment.json').write_text(json.dumps(assessment,indent=2)+'\n');v['visualReviewed']=True;(p/'verification.json').write_text(json.dumps(v,indent=2)+'\n')
manifests=read(B/'combined02-cross-review/manifest-list.json')['manifests'];states={}
for n in manifests:
    for s in read(ROOT/n)['states']:states[s['id']]=s
assert len(states)==44 and sum(len(s['frameFiles']) for s in states.values())==248
block='''

## Marsh own West pickup / South drain — October 3, 2026

Water transitions now stage4of8directions/24slots/16new intermediate drawings:
Eastpickup02,Westpickup03,Northdrain01,Southdrain01; four remaining North/South
pickups and East/West drains. Coverage is provisional, not coherent art acceptance.
All whole original/project sources/prompts/orderedreferences/SHA retained.
OwnWest nearLEFT temple BARE, RIGHT implant hidden far side, one leadingLEFT
case latch; South RIGHT implant viewerLEFT/two frontal latches.

West01 exec-5ecafa91-1d33-4ecc-a383-f566a6de5cbc had164x90launch/160x56late,
neutral33x148 vs31x147master and141x54swim endpoint. Neutral again FIRST: observed
order[1,2,3,4,0] controls packing. West02 wholecorrection
exec-fbd28398-c619-4790-b46e-2f8eb18cdcb3 worsened late178x55; rejected before
native testing. Correction is not improvement by provenance or intent. Keep
failed source and measured comparison, never fit limbs/heads/poses to hide it.
West03 exec-07100148-723d-473f-ad9d-965db6e93c69 uses3x enlarged whole exact
master/endpoints together as Primary, not independently enlarged characters;
oldselectedbank motiononly, failed02 excluded. One147scale.3012295081967213:
76x86/94x113/150x65/163x56/neutral33x147. Folded-knee launch/head readability
improves, late remains too long/larger than endpoint: provisional only. Larger
reference board helps clarity but is not a guarantee of physical scale/camera.
01/02 retained rejected/superseded; no native gates for those studies.

South drain01 exec-2d85c090-1ba4-4843-8061-0effed02f120, one147scale
.24581939799331104 gives65x73/63x94/63x126/60x147/neutral59x147. Neutral matches
current59x147master bounds. First rising versus75x106swim endpoint still has
size/kick discontinuity; case/head/body/material/camera/root/contact open.
Penultimate two-flat-feet planted hold retained; finalstride is not selected
during drain. Original6x150pickup900ms and drain120/180/220/220/180/120=1040ms
finite contracts. Whole alpha128/BOX/common ruler/integer translation/noopaque
clipping, no patch/mirror/recolour/perposefit. Dry184p92 endpoints padded224p112
with whole20x translation/sourceRGBA exact; noresampling. Other source manifests
retain their own metadata in ordered combined02list (44private states/248slots,
not all44actually witnessed or fullMarshcoverage).

Native West03:171checks/47samples/6restores;South01:192/54/6; all12pairs/4boards
inspected,12finiteAPNG RGBAholds exact,40inputs stable respective intervals,
2931owner nonlogs unchanged,0errors/warnings/fails/exit0. Finite player/grid API
parity at20ms(+1ms), not exact internal-boundary/world contact proof.
Initial q2 dispatch failed because cloned fixture kept q0 wreck-clear y16..19/
x20,21 while home20,21/target19,24/rotation2 needs established q2 y21..24/x19,20.
Preserve failed audit/exit1/stable1653inputs+2931owner. Corrected fixture only;
no resource/failure/dispatch bypass. Fresh scratch retry1 passed15221checks/
3710samples/62actor-player restores+outerprocess pauseholds,62source/native pairs
on8boards ALLseen,12phases/one extraction/safe delayedcredit/dryalive,
1653inputs/2931owner nonlogs stable,0errors/warnings/fails/exit0. When rotating a
route fixture update physical clear-region along with home/target/rotation; keep
dispatch reason in failure output. Do not turn normal flags off to force a pass.

Actualq2 Westpickup6/Southdrain0..4 plantedhold witnessed, drain5 nativeonly;
actualcarrySouth0 separate, all9drySouthNorth/Northcarry4/Northunload4 captured.
OldWestpickup/newWest and newSouth/oldSouthdrain replaced by exact staged joins.
Natural doorwaybeam occlusion is visible during dryturn; no fullphysical-root/
contact proof. Westdrain mismatch in publisher remains SOURCEONLY (actualSouth
drain). Head/body/case/grade/camera/kick stillprovisional. No normal selection/
runtime change,allroute/fullSave/visibleContinue/helmet/contact/admission/fullgoal
acceptance. All jobs terminal; dated stableintervals don't assert later metadata.
Next remaining4transition directions, then whole cross-family polish, actual
allroute/persistence/helmet/contact/admission and remaining fullMarshfamilies.
Handoff: docs/MARSH_WATER_TRANSITION02_HANDOFF_2026-10-03.md.
'''
canonical=ROOT/'skills/brinespace-character-pipeline/references/master-repair.md';installed=Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/master-repair.md')
assert canonical.read_bytes()==installed.read_bytes()
for p in [ROOT/'character/ANIMATION_PIPELINE.md',ROOT/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',ROOT/'docs/CURRENT_STATUS.md',canonical]:
    with p.open('a',encoding='utf-8') as f:f.write(block)
installed.write_bytes(canonical.read_bytes())
handoff='''# Project handoff

Updated:2026-10-03 · Project:BrineSpace · Task:Marsh Westpickup/Southdrain

## Objective and acceptance
Full master-matched Marsh set, then cross-family consistency/polish. Goal active;
new4of8transition coverage/native/world gates do not admit art or finish fullset.

## Accepted decisions and constraints
Whole own direction/no mirrors/patches/perposefit. One neutral alpha128/BOX;
exact dry endpoints padded184p92->224p112 via20xwholetranslation, noresize.
Drain penultimate groundedhold/finalstride separate. Ordered original manifests
preserve individual metadata. Tests scratchAPPDATA/owner stable/normal flags.

## Current state
character/marsh-water-transition-material-v1:West01/02 raw/provenance/failed
studies retained,West03 provisional/Southdrain01 source/unselected/native review.
combined02original manifest list44states/248slots,transition-world02q2review.
Overall transitions4of8/24slots/16new intermediate drawings. New West02/03prep,
native UIDmaps/fixtures/fingerprints/q2prepare/publish/record tools. Paired UIDs
preserved including untested study fixtures. Pipeline/bible/status/skillrefs
updated. No runtime/normal catalogue change; jobs terminal.

## Verification
West03native171checks/47samples/6restores,South192/54/6;12nativepairs/4boards
seen,12exactAPNGholds,40inputs stable each. q2firstdispatch failed from oldq0
wreck-clear region; retainedaudit exit1/owner+inputs stable. Corrected q2fixture
freshscratch retry1:15221checks/3710samples/62restoredpauseholds/62pairs/8boards
ALLseen,12phases/safedelayedcredit/dryalive,1653inputs stable.2931owner nonlogs
unchanged each;passing gates0errors/warnings/fails/exit0. Pickup6/drain0..4planted/
separatecarrySouth0/all9drySouthNorth/Northcarry+unload witnessed;notall44loaded.
West03late163vs141endpoint, neutral33vs31wide;Southfirst73vs106heightjump.
Head/body/case/grade/camera/kick/root/contact provisional. NofullSave/helmet/
allrotations/visibleContinue/admission/fullgoal proof. Native01/02West untested.

## Next action
Own North/South pickups and East/West drains from currentmasters/exactswim/dry
endpoints. Then whole cross-family camera/volume/head/grade/root/kick polish,
actualallroute/persistence/helmet/contact/admission,remainingMarshfamilies.
'''
(ROOT/'docs/MARSH_WATER_TRANSITION02_HANDOFF_2026-10-03.md').write_text(handoff,encoding='utf-8')
print('Provisional ownWest/South banks, rejected corrections and actualq2 evidence recorded; full goal active.')
