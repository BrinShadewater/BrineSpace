"""Record a whole South pickup improvement without claiming full-family acceptance."""
from pathlib import Path
import json,hashlib
import numpy as np
from PIL import Image
ROOT=Path(__file__).resolve().parents[1];B=ROOT/'character/marsh-water-transition-material-v1'
read=lambda p:json.loads(p.read_text());sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
r=read(B/'sources/pickup-south-02.request.json');recipe=read(B/'pickup-south-02-unselected/recipe.json')
assert r['generationId']=='exec-6f1de6c8-8fd4-4229-9678-910ca28b3d85'
assert sha(B/'sources/pickup-south-02.raw.png')==r['rawSha256']==sha(Path(r['originalGeneratedPath']))
assert sha(B/'sources/pickup-south-02.prompt.txt')==r['promptSha256']
for q in r['orderedReferences']+r['sourceFrames']:assert sha(ROOT/q['path'])==q['sha256']
assert recipe['observedSourceOrder']==[0,1,2,3,4]
assert [q['occupiedSize'] for q in recipe['records']]==[[72,95],[70,98],[72,78],[72,99],[58,147]]
for q in recipe['endpointRecords']:
    im=Image.open(ROOT/q['source']['path']).convert('RGBA');padded=Image.open(B/'pickup-south-02-unselected'/q['file']).convert('RGBA');x=q['wholeTranslation'][0]
    assert padded.crop((x,0,x+im.width,im.height)).tobytes()==im.tobytes()
def bounds(p):
    a=np.array(Image.open(p).convert('RGBA'));a[:,:,3]=np.where(a[:,:,3]>=128,255,0);b=Image.fromarray(a).getbbox();return [b[2]-b[0],b[3]-b[1]]
master=ROOT/r['selectedIdleMaster']['path'];assert bounds(master)==bounds(B/'pickup-south-02-unselected/ruler.png')==[58,147]
native=read(B/'pickup-south-02-actor-review/verification.json');world=read(B/'transition-world-06-review/verification.json')
assert (native['nativeChecks'],native['samples'],native['captures'],native['playerRestores'],native['finiteAPNGHolds'],native['inputsStableDuringInterval'],native['ownerFilesUnchanged'])==(171,47,6,6,6,42,2931)
assert (world['checks'],world['samples'],world['sourceNativePairs'],world['actorPlayerRestores'],world['stableBoundedInputs'],world['unchangedOwnerNonLogFiles'])==(15513,3783,62,62,2325,2931)
for rev,checks,samples,captures in [('water-pickup-south-02-native-2026-10-03',171,47,6),('water-transition-world-06-2026-10-03',15513,3783,62)]:
    A=ROOT/'output/marsh-animation-audit'/rev;report=read(A/'report.json');assert (report['checks'],report['failures'],len(report['samples']),len(report['captures']))==(checks,0,samples,captures)
    assert (A/'native-exit.txt').read_text().strip()=='0';log=(A/'native.log').read_text();assert 'ERROR:' not in log and 'WARNING:' not in log
    for kind in ['inputs','owner']:assert read(A/f'{kind}-before.json')==read(A/f'{kind}-after.json')
for q in native['nativeParity']:assert sha(ROOT/q['source'])==q['sourceSha256']
for q in world['sourceParity']:assert sha(ROOT/q['path'])==q['sha256']
for q in read(B/'south02-cross-review/sources.json')['records']:assert sha(ROOT/q['source'])==q['sha256']
finding='Whole02 fixed frontal launch improves on diagonal01, with narrower compact72x78launch and72x99late vs01 98x90/81x85, exact75x106swim. All ownRIGHT temple viewerLEFT/two frontcase latches. Current master alpha128 bounds58x147 and neutral58x147, correcting carried-forward59label; source SHA072323ccabf81e7e431fb66836492d8da7a072ee32895c70a3aa4d30bb098b5e. One147 neutral scale .25257731958762886, no individual pose fits. Whole shape/case/head/palette closer, not complete physical camera/root/contact/kick or continuousmotion acceptance. Cross-family South drain first65x73 still visibly smaller than75x106swim; repair whole geometry separately.'
(B/'pickup-south-02-actor-review/visual-assessment.json').write_text(json.dumps({'normalAdmission':False,'fullGoalComplete':False,'preferredPrivateStudy':True,'wholeSourceAndComparisonInspected':True,'nativePairedBoardsInspected':2,'nativePosePairsInspected':6,'findings':finding},indent=2)+'\n')
(B/'south02-cross-review/visual-assessment.json').write_text(json.dumps({'normalAdmission':False,'fullGoalComplete':False,'boardsInspected':['pickup-revisions.png','south-family-00.png','south-family-01.png'],'currentMasterBoundsAlpha128':[58,147],'findings':finding},indent=2)+'\n')
keys=sorted({q['key'] for q in world['sourceParity']});assert 'swim-pickup-south' in keys and 'cargo-drain-east' in keys
(B/'transition-world-06-review/visual-assessment.json').write_text(json.dumps({'normalAdmission':False,'fullGoalComplete':False,'nativeBoardsInspected':8,'sourceNativePairsInspected':62,'actualWitnessedKeys':keys,'findings':finding+' Actual q1 normaldispatch,12phases/one extraction/safe delayedcredit/dryalive,62actor-player restores/outerprocesspause holds. NewSouthpickup all6slots, otherbanks unchanged; not all48states, otherrotations/fullSave/TitleContinue/helmet/coherentfullfamily proof.'},indent=2)+'\n')
world['visualReviewed']=True;(B/'transition-world-06-review/verification.json').write_text(json.dumps(world,indent=2)+'\n')
p=B/'sources/pickup-south-01.request.json';old=read(p);old.update(supersededPrivateStudy=True,supersededBy='pickup-south-02',reason='Whole02 fixes launch yaw and improves late endpoint volume;01 retained with scoped prior evidence.');p.write_text(json.dumps(old,indent=2)+'\n')
cat=ROOT/'character/marsh-v2/catalog.json';selected={}
for n in read(cat)['body']:
    p=ROOT/n.removeprefix('res://') if n.startswith('res://') else (cat.parent/n).resolve()
    for s in read(p)['states']:selected[s['id']]=s
scope={'currentCatalogSha256':sha(cat),'currentNormalSelectedStates':len(selected),'currentNormalSelectedSlots':sum(len(s['frameFiles']) for s in selected.values()),'privateWaterTransitions':8,'privateWaterTransitionSlots':48,'combinedPrivateStates':48,'combinedPrivateSlots':272,'fullGoalComplete':False,'limits':'Current ordered normal selection counts preserve full goal scope; they establish inventory, not art/controller acceptance. Private water/cargo subset cannot stand in for complete Marsh set.'}
(B/'south02-cross-review/verification.json').write_text(json.dumps({'normalAdmission':False,'fullGoalComplete':False,'native':native,'world':{k:world[k] for k in ['checks','samples','sourceNativePairs','actorPlayerRestores','stableBoundedInputs','unchangedOwnerNonLogFiles']},'fullScope':scope},indent=2)+'\n')
block='''

## Marsh South pickup whole refinement — October 3, 2026

South pickup02 is the preferred private study, replacing01 in cardinal02 and
ordered combined04 only. Whole source exec-6f1de6c8-8fd4-4229-9678-910ca28b3d85
uses exact own standing/swim endpoints enlarged together3x as primary, original
own identity and OLD motion-only; failed diagonal01 is excluded as reference.
One147scale .25257731958762886:72x95/70x98/72x78/72x99/neutral58x147. Launch
stays frontal; late72x99 approaches75x106swim better than prior81x85. Physical
head/case/projection/kick/root/contact and continuousmotion remain provisional.
Whole authoring only; no patches/mirrors/recolour/perposefit. All originals/raw/
prompts/orderedrefs/SHA retained; exact normalized endpoint pixels unchanged.

Measurement correction: current own South000.png SHA072323ccabf81e7e431fb66836492d8da7a072ee32895c70a3aa4d30bb098b5e
is58x147 at alpha128, matching new neutral58x147. Earlier59width was a carried-
forward label, not a measurement of this current PNG. Inspect actual source hash,
threshold and bounds before interpreting one-pixel drift. Three complete same-
scale cross-family boards reviewed:revision01/02, newpickup+all4Southswim drawings,
Southdrain/own drycarry0/unloadfinal/master. Southdrain first65x73 still visibly
smaller than75x106swim; reauthor connected whole geometry, do not fit it alone.

Native171checks/47samples/6restores/6native poses on2inspected boards; six exact
finite APNG holds,42inputs stable. Actual normalq1 with South02/Eastdrain passed
15513checks/3783samples/62native sourcepairs+restoredpauseholds,12phases/one
extraction/safecredit/dryalive;2325inputs stable. All8worldboards inspected,
zeroerrors/warnings/failures/exit0;2931owner nonlogs unchanged in both intervals.
Other states source-identical; not all48states/rotations/fullSave/TitleContinue/
helmet/contact/fullfamily acceptance. Private transitions remain8states/48slots,
combined48states/272slots. No normal catalogue/runtime change; fullgoal active.
Current full normal inventory counts are recorded in south02-cross-review/
verification.json; private water/cargo coverage cannot replace that full scope.
Next:whole Southdrain early volume/kick continuity, then other visible water/dry
and full-library identity/camera/head/case/grade joins, persistence/contact/admission.
Handoff:docs/MARSH_WATER_SOUTH_PICKUP02_HANDOFF_2026-10-03.md.
'''
canonical=ROOT/'skills/brinespace-character-pipeline/references/master-repair.md';installed=Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/master-repair.md');assert canonical.read_bytes()==installed.read_bytes()
for p in [ROOT/'character/ANIMATION_PIPELINE.md',ROOT/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',ROOT/'docs/CURRENT_STATUS.md',canonical]:
    with p.open('a',encoding='utf-8') as f:f.write(block)
installed.write_bytes(canonical.read_bytes())
handoff=f'''# Project handoff

Updated:2026-10-03 · Project:BrineSpace · Task:Marsh South pickup02

## Objective and acceptance
Complete master-matched Marsh set, then consistency/polish. Fullgoal active;
current normal inventory {scope['currentNormalSelectedStates']}states/{scope['currentNormalSelectedSlots']}slots. Inventory and staged gates do not prove acceptance.

## Accepted decisions and constraints
Whole own-direction authoring/one neutral ruler, no patch/mirror/perposefit.
Exact dry endpoint whole-padding20x; preserve original metadata. Tests scratch
APPDATA/owner fingerprints/normal resources and failures. No normal admission.

## Current state
South02 preferred private:72x95/70x98/72x78/72x99/neutral58x147. Fixed frontal
launch/closer75x106endpoint;01 retained/superseded. Source/raw/prompt/request/
packing/APNG/native reviews in character/marsh-water-transition-material-v1.
cardinal02eight transitions48slots;combined04orderedlist48states272slots.
Three same-direction cross-family boards+assessment. NewSouth02prep/nativeUID,
world06prep/UID/fingerprint/publisher/record tools. Pipeline/bible/status/skillrefs
updated. Actual current master58x147 corrects stale59label. No runtime/catalogue
change; all jobs terminal. Current full scope in south02-cross-review/verification.json.

## Verification
Native171/47samples/6restores/6pairs/2boards allseen;6exactAPNGholds,42inputs stable.
World06normalq1:15513checks/3783samples/62native pairs+restoredpauseholds/8boards
allseen,12phases/safecredit/dryalive,2325inputs stable.2931owner nonlogs unchanged
both intervals;zeroerrors/warnings/failures/exit0. Whole endpoints exact, current
master/ruleralpha128 both58x147. Southdrain first65x73 visibly undersized versus
75x106swim; head/case/grade/camera/kick/root/contact stillprovisional. No all48
state/rotation/fullSave/Continue/helmet/coherentfullMarsh/admission proof.

## Next action
Reauthor whole Southdrain early rise with own current master/swim/drycarry
endpoints and sustained head/case/body volume/kick. Continue full-library joins,
remaining consistency/persistence/helmet/contact and normal admission work.
'''
(ROOT/'docs/MARSH_WATER_SOUTH_PICKUP02_HANDOFF_2026-10-03.md').write_text(handoff,encoding='utf-8')
print('South02 whole improvement and measured current master recorded; full goal active.');print(json.dumps(scope))
