from pathlib import Path
import json,hashlib,uuid,os
p=Path(__file__).resolve().parent;r=p.parents[1]
data=json.loads((p/'checkpoint_probe-evidence.json').read_bytes())
guard=json.loads((p/'checkpoint_probe-validation.json').read_bytes())
review=json.loads((p/'checkpoint-review.json').read_bytes())
inputs=json.loads((p/'checkpoint_probe-inputs.json').read_bytes())
cases=[c for c in data['results'] if c.get('checkpoint')]
captures=[c for c in data['results'] if 'label' in c]
assert data['failures']==0 and len(cases)==6 and len(captures)==18
assert guard['exitCode']==0 and not guard['timedOut'] and guard['realProfileUnchanged']
assert all(hashlib.sha256((r/k).read_bytes()).hexdigest()==v for k,v in inputs.items())
assert all(c['sourceExact'] and c['floorRestored'] and c['completed'] for c in cases)
assert {(c['mode'],c['phase']) for c in cases}=={(m,s) for m in ['bare','helmet'] for s in ['before','after','idle']}
def atomic(path,new):
    old=path.read_bytes();temp=path.with_name(path.name+'.'+uuid.uuid4().hex+'.tmp')
    temp.write_bytes(new);assert path.read_bytes()==old;os.replace(temp,path)
review.update(visualReviewPending=False,reviewed='All18 saved/fresh-restored/completed registered source/prop and actual native room presentations inspected across six both-gear phase boards. Immediate restored source whole RGBA exact; contact/helmet/matte registration retained. Separate case profile/material seam remains unaccepted.',ordinaryContinueAcceptance=False,continuousMotionAcceptance=False)
atomic(p/'checkpoint-review.json',(json.dumps(review,indent=2)+'\n').encode())
verdict={'selected':False,'fullGoalComplete':False,'nativeChecks':data['checks'],'failures':0,'actualPrescribedReturnAdmissions':6,'freshMainScenesRestored':6,'actualCandidateDiskRoundTrips':6,'nativeSourceWorldPairsReviewed':18,'targetedInputsUnchanged':len(inputs),'ownerProfileUnchanged':True,'scope':'Staged candidate paired disk contract; normal RunSave capture/base schema validation and SAVE.restore_staged into fresh main, followed by candidate actor/player/renderer restoration. Normal title/new-process Continue and normal write/read are not admitted.','guards':'Exact binding/version/marker, actor-foot/gear/state, finite source clocks, canonical loaded planner equality, every row RGBA/pivot/H148 binding, released room ownership. Ordinary loader rejects candidate marker.','firstFailure':'Probe generator retained old hazard identifier outside its scope. Parse failure before runtime; fixed generator only. Original failed inputs/script/log/owner-profile guard preserved in first-checkpoint-run.','remaining':['Normal paired write/read/title/new-process Continue integration after visual candidate admission.','Full future trajectory/departure/pause/interrupt save combinations and legacy/rejection coverage.','Case hardware/profile/material source-to-prop seam and V9 collar/head-turn polish.','Other cardinals, normal scheduling and full James/master/cross-family set.']}
(p/'checkpoint-acceptance.json').write_text(json.dumps(verdict,indent=2)+'\n')
section=f'''## James West staged paired disk/fresh-main return — October 2, 2026

New unselected checkpoint.gd pairs exact finite return plan/source bindings with
fixed room-owned case state. Staged disk codec uses normal station capture/base
schema validation and actual RunSave.restore_staged in fresh main, then explicit
candidate actor/player/renderer restore. Mandatory unadmitted actor marker means
ordinary normal loader rejects candidate files rather than silently dropping the
motion. This is not normal write/read/title/new-process Continue admission.

{data['checks']}native checks0fail/six actual carry returns and disk/fresh-main restores:
bare/helmet x before release/after release/idle. All18saved/restored/completed
registered source/prop and native room pairs reviewed. Fresh restore paused at
exact clock/contact/plan/room anchor; immediate source whole RGBA exact; resumed
finite returns finish with owned case. Source/head/helmet/material registration
held in reviewed presentations. Exact generated-case profile/material seam still
unaccepted. Engine0/no timeout/whole owner profile unchanged;{len(inputs)}targeted
prelaunch hashes unchanged. No full trajectory/continuous motion/master claim.

Binding/version/marker/clock/actor-floor/expiry/row-pixel changes and missing
post-release ownership reject. Loaded plan must equal current canonical planner;
every row RGBA/pivot/H148 is bound, including generated V9 interior sources.
First probe parse failure from copied hazard identifier retained in
first-checkpoint-run; generator fixed, no art/runtime change to pass it.
Lesson: validate actor and player clock against owning room together, bind saved
artwork to loaded bank, and explicitly reject an unadmitted lifecycle in ordinary
Continue. A staged codec/fresh-scene restore is a precursor, not title admission.

Next normal paired Save/Continue integration after visual admission, more future/
pause/interruption/legacy rejection evidence; case seam/V9 bridge polish, other
cardinals and full James/master/cross-family review. Goal active/incomplete.
Evidence:character/james-floor-case-west-v1/checkpoint-acceptance.json,
checkpoint-review.json,checkpoint_probe-evidence.json. No normal selection/export.
'''
for path in [r/'docs/CURRENT_STATUS.md',r/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',r/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',r/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]:
    old=path.read_bytes()
    if section.splitlines()[0].encode() not in old:
        atomic(path,section.encode()+b'\n'+old if path.name=='CURRENT_STATUS.md' else old+b'\n\n'+section.encode())
handoff=f'''# Project handoff

Updated: October 2, 2026 · Project: Brine Space · Task: James West staged paired restore

## Objective and acceptance
Full James set matching directional masters/style/perspective/size/proportions/
matte grade, then cross-family polish. Incomplete; candidate unselected.

## Accepted decisions and constraints
Preserve selected artwork/normal loader/room geometry/owner profile. Staged
cosmetic latest James case per workshop, no inventory/collision change admitted.
Mandatory candidate marker protects ordinary Continue from silently losing motion.

## Current state
Raw case sources/prompts/native package; floor_state/actor/player/release_workshop.
New checkpoint.gd strict paired disk contract and checkpoint_probe.gd fresh-main
native evidence/boards/acceptance. Source rows bind exact RGBA/pivot/H148.
Probe generator first parse failure retained. Five guides updated.

## Verification
Prior220automatic/88skipped-cue/434priority checks, all0fail. New{data['checks']}checks/
six actual disk/fresh-main restores/both gears/three phases/18reviewed pairs,
0fail/engine0/owner unchanged/{len(inputs)}targeted hashes unchanged. Immediate
source RGBA/contact/clock/room state exact; finite sequence completes. Candidate
codec plus normal base restore, not ordinary normal write/read/title/new process.

## Next action
Polish case profile/material join and V9 collar/head turn, then normal paired
write/read/title/new-process admission with full future/pause/interruption/legacy
coverage. Other cardinals/natural world/master and full cross-family polish remain.
No normal selection, commit/export or full-goal completion.
'''
atomic(p/'HANDOFF.md',handoff.encode())
print('Staged'+str(data['checks'])+'check paired disk/fresh-main milestone recorded;five guides/handoff updated.')
