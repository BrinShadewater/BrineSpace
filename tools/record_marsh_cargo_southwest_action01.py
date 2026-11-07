"""Record remaining cargo directions, cross-facing findings and dated native scope."""
from pathlib import Path
import hashlib,json,subprocess,sys
ROOT=Path(__file__).resolve().parents[1];B=ROOT/'character/marsh-cargo-held-material-v1';S=B/'sources';R=B/'southwest-action-01-actor-review';C=B/'all-facing-01-cross-review'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())
v=read(R/'verification.json');assert (v['checks'],v['captures'],v['samples'],v['actorPlayerRestores'],v['stableBoundedInputs'],v['unchangedOwnerNonLogFiles'])==(1019,16,252,16,534,2931)
generations={'south':'exec-a86dde1e-b0b6-491e-97d3-779f39f59c54','west':'exec-6c04ba41-ed20-4a2f-b334-eaf33326d663'}
sizes={'south':[[62,125],[71,95],[61,147]],'west':[[69,125],[83,99],[33,147]]}
for f in ['south','west']:
    r=read(S/f'{f}-unload-01.request.json');O=B/f'{f}-unload-01-unselected';recipe=read(O/'recipe.json')
    assert r['generationId']==generations[f] and sha(S/f'{f}-unload-01.prompt.txt')==r['promptSha256']
    assert sha(S/f'{f}-unload-01.raw.png')==r['rawSha256']==sha(Path(r['originalGeneratedPath']))
    for q in r['orderedReferences']+r['sourceFrames']+r['guideDependencies']:assert sha(ROOT/q['path'])==q['sha256']
    assert [q['occupiedSize'] for q in recipe['records']]==sizes[f]
    assert recipe['exactCarryEndpoint'] and recipe['exactIdleEndpoint'] and recipe['exactPickupReversal'] and recipe['decodedApngFrames']==8
    findings='South front/two-latch divided panel retained, ownRIGHT temple viewerLEFT. First lowering fairly upright/shallow;neutral61x147 vsselected58x147, width+3. Head/body/grade/rigid-case/contact joins provisional.' if f=='south' else 'West LEFT profile/bare visibleLEFTtemple and single ivoryLEFTedge side insetpanel retained. Neutral33x147 vsselected31x147 width+2. Floorcase appears larger than exactcarrycase; head/body/grade/case/contact joins provisional.'
    (O/'visual-assessment.json').write_text(json.dumps({'normalAdmission':False,'fullGoalComplete':False,'rawAndFourOrderedRefsSeenBeforeGeneration':True,'wholeMotionAndNeutralBoardsSeen':True,'sourceNativePosesSeen':8,'findings':findings,'nativeEvidence':'southwest-action-01-actor-review/verification.json','limits':v['limits']},indent=2)+'\n')
    r.update(status='generated, whole packed, source/native reviewed; unselected, visual joins provisional',limits=v['limits']);(S/f'{f}-unload-01.request.json').write_text(json.dumps(r,indent=2)+'\n')
(R/'visual-assessment.json').write_text(json.dumps({'normalAdmission':False,'fullGoalComplete':False,'allSixteenPairsInspected':True,'pairedBoardsInspected':4,'findings':'All4Southpickup/4Southunload/4Westpickup/4Westunload exactsource/native pairs seen. Right facings and hardware retained. South halfcrouch shallow; body/head/grade/rigidcase/floorcontact joins remain provisional. Seeded valid unloadstates do not prove actual delivery; normalarrivalforcesNorth.','limits':v['limits']},indent=2)+'\n')
subprocess.run([sys.executable,str(ROOT/'tools/publish_marsh_cargo_southwest_action01.py')],check=True,stdout=subprocess.DEVNULL)
cross=read(C/'verification.json');assert (cross['states'],cross['frameSlots'],cross['wholeFigures'])==(8,32,20)
for q in cross['figures']:assert sha(ROOT/q['path'])==q['sha256']
(C/'visual-assessment.json').write_text(json.dumps({'normalAdmission':False,'fullGoalComplete':False,'wholeComparisonBoardsInspected':2,'wholeFiguresInspected':20,'findings':'All4selectedidles/all4stagedcarry endpoints/all8loweringposes/all4neutralrulers compared. Two-latch South vs side one-edge-latch East/West and frontheld hiddenNorth occlusion retained. South halfcrouch shallow; neutral widths+2/+3, North145postthreshold vs146target. Sidefloorcases appear larger than carry endpoints; relative head/body/grade/foot/support/case joins remain open.','next':'Whole source corrections for rigid case dimensions and body/pose joins; then coherent full delivery/save/actual visible Continue before normal admission.','limits':'8state32slot stagedsource family only, not fullMarshset or normal/adopted family acceptance.'},indent=2)+'\n')
maintained=ROOT/'skills/brinespace-character-pipeline/references/master-repair.md';installed=Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/master-repair.md');assert maintained.read_bytes()==installed.read_bytes()
marker='## Marsh four-facing held-cargo source family and South/West playback — October 2, 2026'
lesson='''

## Marsh four-facing held-cargo source family and South/West playback — October 2, 2026

South unload01 exec-a86dde1e-b0b6-491e-97d3-779f39f59c54 andWest unload01
exec-6c04ba41-ed20-4a2f-b334-eaf33326d663 frozen own-bodyPRIMARY/stagedcargo/
oldmotion-only/original identity refs. Exact four local versions seen before
each call, prompt/source/guide hashes checked, raw originals retained. Two whole
lowering figures and neutral each. South one147 BOX scale .19165580182529335:
62x125/71x95/ruler61x147 vsselected58x147. West .2413793103448276:
69x125/83x99/ruler33x147 vsselected31x147. Alpha128,whole integer floor-band
registration, no opaque clipping/mirror/patch/recolour/per-pose or cargo-width fit.
South uses both boot span, West RIGHT boot band excluding case on LEFT; don't
reuse East LEFT-boot registration for the opposite-facing case. Foot registration
doesn't establish rigid-case scale or physical floor contact.

Raw/allrefs/whole-motion/neutral boards seen. South front two-latch divided case,
RIGHTimplant viewerLEFT retained; first intermediate shallow/fairly upright. West
LEFT side case single ivoryLEFTedge latch/insetpanel and bare visibleLEFTtemple
retained. Neutralwidth+3/+2; head/body/grade/limb/support/contact joins provisional.
All4directions now have stagedpickup/unload, exact unchanged ownstagedcarry0 and
selectedidle0, complete pixel-order reverse (never mirror), original metadata,
four130ms nonloop520ms,184/p92/172/H148. New unselected all-facing-01-cross-review
family-manifest references8states/32slots with wholeliteral res paths. Counts are
sourcecoverage only; normal catalog unchanged. EightAPNGframes exact per facing.

Normal Marsh.update/main/grid/player South/West work-to-pickup and valid seeded
unloads:1019checks,16exactsource/nativepairs,252controlled20ms samples,
16actor/player restores+pause. Four ordered poses per action, pickup natural26
samples/.52s createscarryroute;unload100samples/2s holds final selectedidle after
520ms and exits targetaction. Correct Northlesson allows subsequent walk-start
clock.534bounded inputs stable DURING interval,2931ownerfiles unchanged scratch
APPDATA,0fail/errors,exit0. All16pairs/fourboards seen. NormalarriveforcesNorth:
South/West unload are seededvalidstates, not full delivery/expedition/fullsave/
visibleTitleContinue/continuouscontact/normaladmission/fullset acceptance.

Cross-facing20completefigures on2boards seen:4selectedidles+4stagedcarry endpoints+
8loweringposes+4rulers. Correct case hardware alone is insufficient: side-floor
cases appear larger than carry endpoints. Exact endpoint copies don't repair an
intermediate rigid-object scale change. South shallowhalfpose, neutralwidth/head/
camera/grade/support joins remain open. Next whole-pose corrections preserving
rigid case dimensions and own proportions; no case patch or individual rescale.
Then coherent complete delivery/fullSave/actualvisibleContinue and normal visual
admission. Remaining fullMarshfamilies and consistency/polish stillrequired.
Assessments/request updates after534 interval aren't its current exact freeze;
claim dated interval only. No livejob. Fullgoal active/incomplete.
'''
for p in [ROOT/'character/ANIMATION_PIPELINE.md',ROOT/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',ROOT/'docs/CURRENT_STATUS.md',maintained]:
    with p.open(encoding='utf-8') as f:present=any(marker in line for line in f)
    if not present:
        with p.open('a',encoding='utf-8') as f:f.write(lesson)
installed.write_bytes(maintained.read_bytes())
(ROOT/'docs/MARSH_CARGO_FAMILY01_HANDOFF_2026-10-02.md').write_text('''# Project handoff

Updated: October 2, 2026 · BrineSpace · Marsh held-cargo family01

## Objective and acceptance
Full master-matched Marsh animations, then cross-family consistency/polish.
Goal active/incomplete. All4held directions staged; no normal family admission.

## Accepted decisions and constraints
Own facing PRIMARY body/cargo, motion-only oldposes; whole generated figures,
one neutral scale, no mirrors/body/case patches or per-pose fits. Exact endpoints
and current4x130ms metadata. ScratchAPPDATA/ownerfingerprints. Arrival forcesNorth.

## Current state
South/West01 raw/request retained; packers and two-direction timed native fixture
(.gd+.uid), fingerprint/publish/record helpers added. All-facing-01-cross-review
contains8state32slot unselected family manifest and20figure comparison boards.
Source/native reviews at southwest-action-01-actor-review. Pipeline/bible/status/
skill mirrors updated. Normalcatalog/runtime unchanged. No livejob.

## Verification
South/West1019checks,16pairs,252timed20ms samples,16restores+pause;534inputs stable
during interval,2931ownerfiles unchanged,0fail/errors,exit0. All16pairs seen.
Sources/endpoints/reversal/APNGs exact. Two cross-facing boards/20figures seen.
East512 andNorth514 have dated prior action evidence; North alone covers actual
short carry arrival. South/West unloads seeded validstates. Sourcewidth/head/grade/
contact and sidefloorcase growth findings remain open; South halfcrouch shallow.

## Next action
Correct whole side-lowering poses for rigidcase scale and body/pose joins, compare
against own endpoints/master. Preserve originals and frozen correction provenance.
Then coherent full pickup-carry-turn-arrival-unload, full saves/actual visible
TitleContinue and normal visual admission. Continue remaining animation families,
then full-set cross-family consistency/polish; counts do not narrow original scope.
''',encoding='utf-8')
print(json.dumps({'checks':1019,'reviewedNativePairs':16,'crossReviewedWholeFigures':20,'stagedStates':8,'stagedSlots':32,'normalAdmission':False,'fullGoalComplete':False}))
