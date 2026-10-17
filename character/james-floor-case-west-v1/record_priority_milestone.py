from pathlib import Path
import json,hashlib,uuid,os
p=Path(__file__).resolve().parent;r=p.parents[1]
data=json.loads((p/'priority-evidence.json').read_bytes())
guard=json.loads((p/'priority-validation.json').read_bytes())
review=json.loads((p/'priority-review.json').read_bytes())
inputs=json.loads((p/'priority-inputs.json').read_bytes())
cases=[c for c in data['results'] if c.get('priority')]
captures=[c for c in data['results'] if 'label' in c]
assert data['checks']==434 and data['failures']==0 and len(cases)==24 and len(captures)==48
assert guard['exitCode']==0 and not guard['timedOut'] and guard['realProfileUnchanged']
assert all(hashlib.sha256((r/k).read_bytes()).hexdigest()==v for k,v in inputs.items())
assert all(c['returnCleared'] and c['ownedAfterPriority']==(c['phase']=='after' and c['hazard']!='floor') for c in cases)
assert all(c['height']==148 for c in captures)
def atomic(path,new):
    old=path.read_bytes();temp=path.with_name(path.name+'.'+uuid.uuid4().hex+'.tmp')
    temp.write_bytes(new);assert path.read_bytes()==old;os.replace(temp,path)
review.update(visualReviewPending=False,reviewed='All48 before/replacement registered source/prop presentations and corresponding native room captures inspected across four bare/helmet pre/post-release boards. Replacement dry poses retain source registration; flooded pose uses normal water presentation. Removed room draws neither actor nor case. Source panels for lost floor still show queried idle texture, not an actor drawn in room. Case hardware/profile/material seam remains unaccepted.',continuousMotionAcceptance=False,fullHazardSequenceAcceptance=False,ordinaryContinueAcceptance=False)
atomic(p/'priority-review.json',(json.dumps(review,indent=2)+'\n').encode())
verdict={'selected':False,'fullGoalComplete':False,'nativeChecks':434,'failures':0,'actualPrescribedReturnAdmissions':24,'nativeSourceWorldPairsReviewed':48,'targetedInputsUnchanged':13,'ownerProfileUnchanged':True,'coverage':'Both gears x before/after release x gear/death/fire/water/floor/new-service. Public gear/death APIs, actual fire field/flooding selection, topology removal and prescribed new RoomActivity. New room cannot resurrect old case.','floorPolicy':'No floor case before release; after release the fixed room-owned cosmetic case survives actor interruption, disappears with owning room.','visualScope':'Native texture pivots/H148 recorded; source/prop upper composites and actual native rooms lower. First death source is standing fall entrance, not full mortality sequence; water presentation is normal selected medium, not full escape/refuge review.','remaining':['Exact source-to-prop case hardware/profile/material seam.','Paired ordinary disk RunSave/fresh main Continue for finite return and floor ownership.','Normal selection and natural scheduling/hazard trajectories.','Other cardinals, V9 collar/head-turn/continuous master review, full James/cross-family polish.']}
(p/'priority-acceptance.json').write_text(json.dumps(verdict,indent=2)+'\n')
section='''## James West floor ownership through priorities — October 2, 2026

Staged West floor release tested through24actual prescribed carry power-loss
returns:bare/helmet x before/after hands-clear cue x gear/death/fire/water/floor/
new-service.434native checks0fail/48before-replacement source-world pairs reviewed.
Public gear/death APIs, actual fire dispatch and RoomFlooding medium, topology
removal and prescribed new RoomActivity supersede return. Cue clock crossed before
dispatch: pre-release priority cannot create a case; released case stays fixed in
surviving workshop. Removed room submits no case; new room cannot resurrect it.

Engine0/no timeout/whole owner profile unchanged under scratch APPDATA.
13targeted prelaunch hashes unchanged. Source pivots/H148 captured from actual
native textures; upper panes registered source/prop composites, lower actual room
pixels. Queried idle source after lost floor is not drawn in absent room. Immediate
death replacement is fall entrance, not complete mortality; flooding source/room
is initial selected medium, not full escape/refuge. No continuous full hazard,
natural scheduler/world or original-master identity claim from metadata checks.

Lesson: floor ownership outlives an interrupted actor after the hands-clear cue;
dispatch safety before cue observation, remove drawing with room ownership and
test fresh replacement room independently. Actor return snapshot and room case
persistence need separate paired disk/Continue evidence. Case hardware/profile/
material seam remains unaccepted; V9 collar/head-turn, other cardinals and full
James/master/cross-family polish remain open. Candidate unselected; normal loader
unchanged. Full goal active/incomplete. No commit/export.
Evidence:character/james-floor-case-west-v1/priority-acceptance.json,
priority-review.json,priority-evidence.json,priority-validation.json.
'''
for path in [r/'docs/CURRENT_STATUS.md',r/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',r/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',r/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]:
    old=path.read_bytes()
    if section.splitlines()[0].encode() not in old:
        atomic(path,section.encode()+b'\n'+old if path.name=='CURRENT_STATUS.md' else old+b'\n\n'+section.encode())
handoff='''# Project handoff

Updated: October 2, 2026 · Project: Brine Space · Task: James West floor-case handoff

## Objective and acceptance
Full James animation set matching directional masters/style/perspective/height/
proportions/matte grade, then cross-family polish. Incomplete; candidate unselected.

## Accepted decisions and constraints
Preserve selected sources/room geometry/owner profile. Cosmetic latest James case
per workshop; inventory/collision/shared-actor policy not admitted. Native tests
use scratch APPDATA and fingerprint complete real owner profile.

## Current state
Built-in raw case sources/prompts/native aspect-preserving package retained.
floor_state/actor/player/release_workshop own source4 hands-clear cue, fixed anchor
and embedded-source duplicate suppression. release/delta/priority native evidence,
registered review boards, acceptance JSON and generators retained with paired UIDs.
Manual182check study/first failed fixture and first narrower delta run preserved.

## Verification
Automatic220checks/two returns/14 reviewed source-world pairs. Multi-hold skipped
cue/completion88checks/four returns/eight reviewed pairs. Priority434checks/
24returns/48pairs reviewed, both gears/pre-post release/six triggers. All0fail,
engine0/owner unchanged.12/12/13targeted prelaunch hashes respectively unchanged.
Native priority pivot/H148, not original-master identity certification. Complete
hazard/refuge/death trajectories and continuous motion are outside these gates.
Generated case profile/material seam remains unaccepted; five guides updated.

## Next action
Paired ordinary RunSave/fresh main Continue for finite return plus fixed room
ownership, including legacy/malformed rejection. Polish case source-to-prop seam
and V9 collar/head turn; other cardinal handoffs/normal integration/natural world
and full James/master/cross-family review. No normal selection, commit/export.
'''
atomic(p/'HANDOFF.md',handoff.encode())
print('Priority434checks/24actual returns/48reviewed pairs recorded;five guides/handoff updated.')
