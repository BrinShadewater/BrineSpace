from pathlib import Path
import json,hashlib,uuid,os
P=Path(__file__).resolve().parent;R=P.parents[1];D=R/'character/james-east-cargo-heads-v3'
native=json.loads((P/'selected-cargo-v3-native-evidence.json').read_bytes());guard=json.loads((P/'validate-selected-cargo-v3-validation.json').read_bytes());scale=json.loads((P/'turn-v3-native-evidence.json').read_bytes());selection=json.loads((D/'selection-evidence.json').read_bytes())
assert native['failures']==0 and guard['exitCode']==0 and guard['realProfileUnchanged'] and not guard['timedOut'] and scale['failures']==0
assert all(hashlib.sha256((R/path).read_bytes()).hexdigest()==h for path,h in selection['sourceHashes'].items())
frozen=json.loads((P/'east-turn-v3-inputs.json').read_bytes());changed=[path for path,h in frozen.items() if hashlib.sha256((R/path).read_bytes()).hexdigest()!=h]
assert set(changed)=={'scripts/grid_canvas.gd','character/ACTIVE_ASSETS.json'},changed
def atomic(path,new):
    old=path.read_bytes();tmp=path.with_name(path.name+'.'+uuid.uuid4().hex+'.tmp');tmp.write_bytes(new);assert path.read_bytes()==old;os.replace(tmp,path)
for mode in ['bare','helmet']:
    path=D/(mode+'-manifest.json');pack=json.loads(path.read_bytes());pack['status']='selected_normal_loader_playback_validated_actual_hauling_continue_pending';atomic(path,(json.dumps(pack,indent=2)+'\n').encode())
selection.update({'normalLoaderNativeAcceptance':True,'normalLoaderChecks':native['checks'],'pairedTurnPlaybackCases':12,'nativePairedScaleCapturesReviewed':46,'sourceTurnSlotsReviewed':46,'sourceTurnBoardsReviewed':8,'actualTaskAcceptance':False,'ordinaryRunSaveContinueAcceptance':False,'realOwnerProfileUnchanged':True,'priorChangedInputs':changed,'postValidationManifestChange':'Status metadata only; frames/geometry/clocks unchanged','fullGoalComplete':False})
atomic(D/'selection-evidence.json',(json.dumps(selection,indent=2)+'\n').encode())
section='''## James compact East cargo and connected turns selected — October 2, 2026

`character/james-east-cargo-heads-v3` now normally selected via whole paired
manifest paths in grid_canvas and ACTIVE_ASSETS. Nine states per gear,128source
refs: East pickup/carry/unload and all six East-connected dry carrying turns,
including East/West half turns and reverse sequences. Original bodies/crate/boots,
clocks/pivots/ruler remain from retained poses except recorded head/collar windows.
These rectangles may include collar/backpack, not semantic head-only protection.
Helmet artwork retained unchanged. Six new distinct head/yaw drawings propagate
to22bare turn slots only after exact original full-RGBA alias proof. Remaining
turn sources/endpoint drawings retained; all paired turn reverse aliases exact.

All46bare turn sources reviewed in8master/original/candidate/carry boards.
Native staged player415checks0fail,46paired148/82/54/27captures reviewed in8boards.
Earlier full East cargo source/native evidence retained separately. Actual normal
grid loader740checks0fail: all128 selected source-clock pixels/pivot/ruler exact,
12paired moving-player turn entrances/returns and scratch binary playback snapshot
future equivalence. This is player state serialization, NOT ordinary actor hauling
or RunSave/fresh-main Continue. Terminal engine0/no timeout; strict scratch whole
owner profile unchanged. Prior frozen inputs changed only shared loader/registry
for admission; original sources/manifests unchanged. Production PNG copies match
reviewed source hashes. Post-test status changes are metadata only.

Lesson: prove original full RGBA aliases before spreading local head repair, so
quarter/half turns and their returns reuse one drawing and grade. Copy reviewed
sources into the production pack with complete relative paths and provenance,
then verify normal loader precedence and live player transition completion. Native
source scale and binary player snapshots cannot stand in for world task, occlusion,
ordinary saves or natural scheduling evidence.
Next actual hauling pickup/route/turn/unload in room context, interruptions and
ordinary RunSave/fresh-main Continue, then West hand-edge cleanup and remaining
family/context/master/material/perspective/proportion/motion polish. Full James
goal active/incomplete; no final owner acceptance, commit or export.
'''
for path in [R/'docs/CURRENT_STATUS.md',R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]:
    old=path.read_bytes();assert section.splitlines()[0].encode() not in old;atomic(path,section.encode()+b'\n'+old if path.name=='CURRENT_STATUS.md' else old+b'\n\n'+section.encode())
handoff='''# Project handoff

Updated: October 2, 2026 · Project: Brine Space · Task: James East cargo heads

## Objective and acceptance
Full James set aligned to directional masters/style/perspective/scale/proportions/
matte grade, then cross-family consistency/polish. Full objective incomplete.

## Accepted decisions and constraints
Preserve original carrying bodies/crate/belt wrench/boots/ground pivot/clocks.
Rectangular head/collar extraction can include backpack pixels; no semantic mask
claim. Original shared helmet retained. Exact alias proof before propagating art.

## Current state
Normally selected character/james-east-cargo-heads-v3 paired pack,9states per gear,
128refs. Six unique turn heads repair22slots across six connected turns. East
pickup/carry/unload18bare and18helmet sources included. Shared loader/registry
updated with whole manifest paths; pre-selection backups retained in this folder.
Rejected halo attempts, prompts, pose anchors and packaging sources retained.

## Verification
All46bare turn sources/8boards plus46native paired scale captures/8boards reviewed.
Staged415checks and normal loader740checks pass,0fail.128source refs,12paired
moving-player entrance/return and scratch binary playback snapshot future cases.
Owner profile unchanged. No actual hauling, ordinary RunSave/main Continue or
continuous world-motion acceptance. Production copy hashes exact; statuses only
changed after validation. Current original source/manifests unchanged.

## Next action
Actual hauling pickup/route/turn/unload with registered room contact; interrupts
and ordinary save/fresh-main Continue in scratch. Then West hand-edge cleanup,
other context coverage and full cross-family consistency/master polish.
'''
atomic(P/'HEAD_CANDIDATE_HANDOFF.md',handoff.encode());atomic(D/'HANDOFF.md',handoff.encode()) if (D/'HANDOFF.md').exists() else (D/'HANDOFF.md').write_text(handoff)
print(json.dumps({'normalLoaderChecks':native['checks'],'failures':0,'productionSelected':True,'guidesUpdated':5,'actualTaskAcceptance':False,'fullGoalComplete':False}))
