from pathlib import Path
import json,hashlib
P=Path(__file__).resolve().parent;R=P.parents[1]
O=R/'output/bill-floor-case-continue-v1';d=json.loads((O/'records.json').read_text(encoding='utf-8'));v=json.loads((O/'validation.json').read_text(encoding='utf-8'))
unit=json.loads((R/'output/bill-floor-case-state-v1/validation.json').read_text(encoding='utf-8'))
assert v['passed'] and unit['passed'] and d['failures']==0 and len(d['records'])==8
assert not v['realProfileChanges'] and not unit['realProfileChanges']
reg=json.loads((P/'registration.json').read_text(encoding='utf-8'))
for name,digest in reg['protectedInputs'].items():assert hashlib.sha256((R/name).read_bytes()).hexdigest()==digest
files=list(reg['protectedInputs'])+['scripts/bill_carry_player.gd','scripts/bill_carry_npc.gd','scripts/run_save.gd','scripts/grid_canvas.gd','scripts/crew_sprite_player.gd','character/bill-floor-case-north-v1/floor_state.gd','character/bill-floor-case-north-v1/floor_checkpoint.gd','character/bill-floor-case-north-v1/world_workshop.gd','character/bill-floor-case-north-v1/workshop_preview.gd','tests/test_bill_floor_case_state_v1.gd','tests/test_bill_floor_case_continue_v1.gd','tools/run_bill_floor_case_state_v1_validation.py','tools/run_bill_floor_case_continue_v1_validation.py']
(P/'continue-input-hashes.json').write_text(json.dumps({name:hashlib.sha256((R/name).read_bytes()).hexdigest() for name in files},indent=2)+'\n',encoding='utf-8')
evidence={'validation':v,'unitValidation':unit,'records':d,'statePolicy':'Staged cosmetic room-owned latest completed-unload case. One optional version1/source4/finite within-cell anchor payload per workshop. Later delivery replaces one payload; removing room removes state. Legacy absent field stays absent. No inventory/collision/economy effects.','selection':'Staged observer, guard and workshop renderer explicitly used only by native fixture. Normal production save validator/controller/loader unchanged.','visualReview':'Agent reviewed all8native source/room presentations and both paired boards. Terminal and deposited Continue retain captured body/head/helmet, matte material, floor case and source/root registration. Static pairs do not certify full continuous unload or interruption joins.','mechanicalScope':'28headless state guards;356native checks/4disk/fresh selected-main restores, both gears terminal before deposit and24unit departed case, exact immediate source/root/clock/state, pause and30future actor/player/source/floor ticks. Malformed floor anchor restore rejects before scene mutation. Room deletion/replacement and priority non-creation covered as pure state guards, not actual native room-removal/fire/death lifecycle.','failedInterval':'Initial native fixture parse rejected inline preload as type specifier; corrected fixture script guard. First log/report retained, owner unchanged.','sourceProtection':'Four recorded original/native source hashes unchanged. Wider dependency hashes post-run, not prelaunch freeze.','remaining':['Actual partial set-down release cue and interruption ownership','Native actual room removal/rotations/priority and shared renderer binding','Normal production validation/observer/renderer admission','Continuous join/support and full Bill cross-family polish']}
(P/'continue-evidence.json').write_text(json.dumps(evidence,indent=2)+'\n',encoding='utf-8')
section='''## Bill staged room-owned case state and fresh Continue — October 2, 2026

New unselected floor_state/floor_checkpoint/world_workshop helpers define one
cosmetic latest completed-unload case per workshop: optional version1/source4/
finite room-local anchor. Later delivery replaces one payload; room removal
removes its state; legacy field absent stays absent. No inventory/collision/
economy changes. Observer creates only at actual finite unload completion with
valid service, unchanged physical foot and active/dry/non-dead actor. Staged
guard validates complete room payload before ordinary RunSave disk/read/restore;
normal production controller, save validator and loader unchanged.

28state guards0fail/6.15s;356native checks0fail/188.41s, engine0;4ordinary disk/
fresh selected-main restores through explicit staged guard/observer/renderer.
Both gears, terminal before deposit and24unit departed deposited case. Immediate
source/root/clock/floor state, pause and30future actor/player/source/floor ticks
match. Malformed floor anchor restore is atomic before scene mutation. All8native
source/room presentations and2Continue boards reviewed: captured body, helmet,
matte suit and case registration retained. Static pairs are not full continuous
unload/interruption joins. Room-removal/replacement/priority non-creation are
pure state guards; actual native removal/fire/death lifecycle remains pending.
All2931owner non-log files unchanged in both scratch-profile intervals;4recorded
original/native source hashes unchanged. Wider hashes post-run, no broad freeze.

Initial fixture parse failed on inline preload as type specifier; corrected
script-path guard, failed log/report retained, owner unchanged. No raster edits.
Completed-unload ownership is a staged policy; interrupted early set-down needs
an authored release cue and floor ownership review before normal admission.
Next real partial-set-down interruptions, room removal/shared renderer binding,
normal guarded admission and continuous/full-library master/grade polish.
Full objective active/incomplete. Review:character/bill-floor-case-north-v1/
continue-review.html; CONTINUE_HANDOFF.md. No commit/export.

'''
for file in [R/'docs/CURRENT_STATUS.md',R/'docs/BILL_ANIMATION_CONTINUATION_2026-09-29.md']:
 s=file.read_text(encoding='utf-8')
 if section.splitlines()[0] not in s:file.write_text(section+s,encoding='utf-8')
lesson='''
## Optional cosmetic room state through Continue — October 2, 2026

Store a floor prop with its room, independently of actor equipment and playback.
Use an optional strict version/source/finite anchor payload; absent legacy state
must not invent a prop. One latest deposit prevents uncontrolled accumulation.
Validate the entire payload before any save/restore mutation. A staged wrapper
can exercise ordinary RunSave disk/fresh-main while keeping normal admission
separate. Test both sides of the creation boundary and future motion: restoring
before completion must create the same prop; restoring after must retain it.
Bill28state/356native guards,4restores/both gears with30future ticks and8reviewed
presentations pass here. Pure room-removal/priority guards are not native world
lifecycle evidence. Completion-only creation does not settle partial set-down
ownership; review the authored release cue before admitting interruption behavior.
Evidence: character/bill-floor-case-north-v1/continue-evidence.json.
'''
for file in [R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]:
 s=file.read_text(encoding='utf-8')
 if lesson.splitlines()[1] not in s:file.write_text(s+lesson,encoding='utf-8')
handoff='''# Project handoff

Updated: October 2, 2026 · Project: Brine Space · Task: Bill staged case Continue

## Objective and acceptance
Full master-matched Bill set and full cross-family motion/material polish.
Cargo handoffs need coherent ownership and exact saved source/root continuation.

## Accepted decisions and constraints
Completion-owned latest room case is a staged cosmetic policy. Optional legacy
state stays absent; no inventory/collision/economy or production selection change.
All engine intervals scratch APPDATA; original body/source art preserved.

## Current state
floor_state/floor_checkpoint/world_workshop with paired UIDs. One strict version1/
source4/anchor room payload; finite actual completion observer. Staged wrapper
prevalidates before ordinary RunSave disk/read/fresh-main restore. Renderer reads
bound room state and keeps floor anchor independent. Tests/runners/boards/evidence
and current status/pipeline/bible/both skill references updated.

## Verification
28headless0fail/6.15s;356native0fail/188.41s,engine0,4fresh restores/both gears:
terminal before deposit and24unit departure after. Exact immediate source/root/
clock/floor, pause and30future actor/player/source/floor ticks; malformed anchor
restore atomic. All8native presentations/2boards reviewed, captured matte/body/
helmet/case consistent. All2931owner files unchanged;4source hashes unchanged.
Broader hashes post-run. One fixture parse failure retained; corrected guard.

## Next action
Audit actual partial set-down release cue and interruption ownership; pure
priority/removal guards do not prove native lifecycle. Check real room removal,
rotations/shared room renderer, then normal guarded admission. Continuous unload/
support and remaining equipment/actions/full cross-family master/grade polish
stay open. Full objective active/incomplete, no commit/export/owner final approval.
'''
(P/'CONTINUE_HANDOFF.md').write_text(handoff,encoding='utf-8')
print('Staged cosmetic room-state and four fresh Continue milestone recorded.')
