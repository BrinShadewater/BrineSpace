"""Record North whole source and actual carry arrival/timed playback scope."""
from pathlib import Path
import hashlib,json,subprocess,sys
ROOT=Path(__file__).resolve().parents[1];B=ROOT/'character/marsh-cargo-held-material-v1';S=B/'sources';O=B/'north-unload-01-unselected';R=B/'north-action-01-actor-review'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())
r=read(S/'north-unload-01.request.json');recipe=read(O/'recipe.json')
assert r['generationId']=='exec-6e00aeea-e92b-4786-b53c-f33eb077ce65'
assert sha(S/'north-unload-01.prompt.txt')==r['promptSha256'] and sha(S/'north-unload-01.raw.png')==r['rawSha256']==sha(Path(r['originalGeneratedPath']))
for q in r['orderedReferences']+r['sourceFrames']+r['guideDependencies']:assert sha(ROOT/q['path'])==q['sha256']
assert [q['occupiedSize'] for q in recipe['records']]==[[61,117],[56,104],[58,145]]
assert recipe['exactCarryEndpoint'] and recipe['exactIdleEndpoint'] and recipe['exactPickupReversal'] and recipe['decodedApngFrames']==8
subprocess.run([sys.executable,str(ROOT/'tools/publish_marsh_cargo_north_action01.py')],check=True,stdout=subprocess.DEVNULL)
v=read(R/'verification.json');assert (v['checks'],v['captures'],v['samples'],v['actorPlayerRestores'],v['stableBoundedInputs'],v['unchangedOwnerNonLogFiles'])==(514,8,126,8,501,2931)
assert v['cases'][1]['actualArrivalSamples']==35 and v['cases'][1]['exitStage']=='' and v['cases'][1]['exitPose']!='unload'
findings='Own rear-facing body and front-held cargo occlusion retained: standing/half-lowering case hidden, deep squat reveals slate case below torso between legs, not across backplate. Whole-motion, neutral and all8 native/source pairs inspected. Neutral58x145 vs selected55x146, nominal146 calibration; thresholded BOX occupancy lost1px. Width/head/shoulder/limb/grade/case/contact joins provisional; no per-pose rescaling to hide diagnostic drift.'
assessment={'normalAdmission':False,'fullGoalComplete':False,'allEightPairsInspected':True,'pairedBoardsInspected':2,'rawAndFourReferenceVersionsSeen':True,'wholeMotionAndNeutralBoardsSeen':True,'findings':findings,'limits':v['limits']}
(R/'visual-assessment.json').write_text(json.dumps(assessment,indent=2)+'\n')
(O/'visual-assessment.json').write_text(json.dumps({'normalAdmission':False,'fullGoalComplete':False,'findings':findings,'nativeEvidence':'north-action-01-actor-review/verification.json','limits':v['limits']},indent=2)+'\n')
subprocess.run([sys.executable,str(ROOT/'tools/publish_marsh_cargo_north_action01.py')],check=True,stdout=subprocess.DEVNULL)
r.update(status='generated, whole packed and source/native reviewed; unselected and visual joins provisional',limits=v['limits']);(S/'north-unload-01.request.json').write_text(json.dumps(r,indent=2)+'\n')
maintained=ROOT/'skills/brinespace-character-pipeline/references/master-repair.md';installed=Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/master-repair.md');assert maintained.read_bytes()==installed.read_bytes()
marker='## Marsh North lowering and actual workshop arrival — October 2, 2026'
lesson='''

## Marsh North lowering and actual workshop arrival — October 2, 2026

North unload01 exec-6e00aeea-e92b-4786-b53c-f33eb077ce65 retained original/raw/SHA,
frozen exact prompt and four refs; each exact reference viewed before generation.
Own selected rearNorth body PRIMARY, staged front-held occluded cargo, old lowering
motion-only, own original North. Two whole figures +neutral, one146 BOX scale
.1978319783197832, alpha128, whole integer both-boot floor-band registration.
Packed61x117/56x104/neutral58x145 vsselected55x146. Nominal146 scaling gives145
occupied after thresholded BOX; record actual occupancy, don't silently rescale
individual poses. Raw,whole-motion,neutral boards seen. Rear body/cream backplate
preserved, case hidden standing/half-lowering and visible below torso between legs
in deep squat; not cargo on back. Away-facing floor perspective differs from side
view; a common bottom anchor alone proves neither foot nor case floor contact.
Width/head/shoulder/limb/grade/rigid-case/contact joins provisional.

Unselected pickup/unload preserve exact stagedcarryNorth0/selectedidleNorth0, whole
reversal, current metadata and4x130ms nonloop520ms,184/p92/172/H148. Eight source
APNG frames exact. Normal Marsh.update/main/grid/player North pickup enters from
work timer. Separate actual short32px North carry route consumes35x20ms steps and
reaches arrive() which naturally forcesNorth unload; no facing override. Timed
pickup26samples/.52s and unload100samples/2s hold/exit:514checks,8source/nativepairs,
126action samples plus35arrival samples,8actor/player restores+pause.501bounded
inputs stable DURING interval,2931ownerfiles unchanged scratchAPPDATA,0fail/errors,
exit0. All8pairs/two boards seen. Not complete pickup-to-delivery route,expedition,
fullRunSave/visibleTitleContinue/contactfilm/normaladmission/fullset acceptance.

First native run514checks/1failure retained at cargo-north-action-01-2026-10-02-
failed-exit-assert: unload exited, then normalAI immediately chose new Eastwalking.
The fixture incorrectly required action_elapsed<0 for every subsequent action.
Ground start can have a valid nonnegative clock. Keep runtime; test exit from
targeted unload pose/stage, allow next activity. Corrected fixture prints actual
exit stage/state/pose/elapsed/direction and records it; successful scoped rerun
establishes target exit. Generic inactive-clock assertions can reject valid same-
frame scheduling; observe the action under test and retain failures/probes.

Metadata assessments/request updates after501interval mean current tree is not
the exact501 freeze; equality is a dated interval claim. No livejob. South/West
held sources remain, coherent family normal-save/visibleContinue gates and full
remaining set/consistency/polish still required. Goal active/incomplete.
'''
for p in [ROOT/'character/ANIMATION_PIPELINE.md',ROOT/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',ROOT/'docs/CURRENT_STATUS.md',maintained]:
    with p.open(encoding='utf-8') as f:present=any(marker in line for line in f)
    if not present:
        with p.open('a',encoding='utf-8') as f:f.write(lesson)
installed.write_bytes(maintained.read_bytes())
(ROOT/'docs/MARSH_CARGO_NORTH_ACTION01_HANDOFF_2026-10-02.md').write_text('''# Project handoff

Updated: October 2, 2026 · BrineSpace · Marsh North cargo source/playback01

## Objective and acceptance
Full master-matched Marsh set, then consistency/polish. Goal active/incomplete;
East andNorth held source families staged, no normal admission.

## Accepted decisions and constraints
Whole figures/one neutral scale/exact endpoints, current four130ms cargo actions.
Own North master and front-held occlusion. Scratch APPDATA/owner fingerprints.
Preserve normal arrival facing and subsequent AI; no runtime edits for test passage.

## Current state
North sources/raw request original retained in marsh-cargo-held-material-v1/sources.
north-unload-01-unselected and north-action-01-actor-review hold source/native pairs.
New prepare/retain/pack/review(.gd+uid)/fingerprint/publish/record North cargo tools.
East timed512check milestone recorded separately. Pipeline/bible/status/skill mirrors
updated. First failed North audit retained. No live job.

## Verification
North neutral58x145 vsselected55x146; two poses61x117/56x104;8sourceAPNGframes exact.
North514checks/8pairs/126timer samples/8restores+pause andactual35step carry-arrival.
501inputs stable during interval,2931ownerfiles unchanged,0fail/errors,exit0.
All8native pairs andwhole/neutral/raw/refs seen. Corrected test allowed a subsequent
East walk-start clock after unload exited; runtime untouched. Body/case/contact
joins remain provisional. No full delivery/expedition/fullsave/actualvisibleContinue.

## Next action
Author South andWest held poses against own body/cargo guides, then timed/lifecycle
native review. Correct whole poses where proportions/contact/joins drift. Complete
coherent carry-family saves/visibleContinue and normal visual admission, remaining
animation families, then full cross-family consistency/polish. Preserve full scope.
''',encoding='utf-8')
print(json.dumps({'checks':514,'sourceNativePairs':8,'actualArrivalSteps':35,'normalAdmission':False,'fullGoalComplete':False}))
