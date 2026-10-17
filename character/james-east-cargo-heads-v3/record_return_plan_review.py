from pathlib import Path
import json,os,uuid
p=Path(__file__).resolve().parent;r=p.parents[1]
native=json.loads((p/'return-plan-probe-evidence.json').read_bytes())
guard=json.loads((p/'return-plan-probe-validation.json').read_bytes())
assert native['checks']==4770 and native['failures']==0 and len(native['plans'])==328
assert guard['exitCode']==0 and guard['realProfileUnchanged'] and not guard['timedOut']
def atomic(path,new):
    old=path.read_bytes();temp=path.with_name(path.name+'.'+uuid.uuid4().hex+'.tmp');temp.write_bytes(new)
    assert path.read_bytes()==old;os.replace(temp,path)
path=p/'return-plan-review.json';review=json.loads(path.read_bytes())
review.update({'visualReviewPending':False,'sourceOrderReview':'All six registered boards reviewed: pickup lowers the case through existing reversed drawings; carry retains and completes the visible East/West turn; late North unload is already its final authored source. Existing grade/identity/feet retained. Final standing/case and turn-to-unload bridges remain incomplete. Static source order is not continuous native motion acceptance.'})
atomic(path,(json.dumps(review,indent=2)+'\n').encode())
section='''## James finite cargo return source plans staged — October 2, 2026

Unselected return_plan.gd now constructs finite whole-source plans from the exact
displayed dry cargo key/index/gear. Pickup reverses to its first authored pose;
unload finishes remaining sources; carry completes visible turn/gait remainder
before attempting unload. First pose holds80ms; later holds use original clocks.
Missing full-RGBA joins are explicitly recorded and plans stop without forced
idle. No raster edits, normal selection or actor/controller/save changes.

Normal loaded James bank:328plans covering every dry pickup/carry/unload slot,
both gears;4770checks0fail, engine0/no timeout, scratch owner profile unchanged.
232carry plans have nonidentical held/unload sources requiring registered bridge
review. All328endpoints require registered idle/floor-case review; raw identity
failure alone is not anatomical failure because idle/cargo canvases differ.
No pre-run dependency freeze or broad lifecycle acceptance claim.

All six retained actual interruption cases mapped to exact source-plan rows;
six registered static boards reviewed. Pickup lowers through retained drawings;
East/West carry finishes its visible turn retaining the case and shared helmet;
late North unload already rests on the authored terminal. Source ordering preserves
original identity/material/pivot density. Continuous native motion, collision
clearance, needs/emergency priority, crate release/persistence, standing bridges
and ordinary save Continue remain pending. Staged planner is not selected repair.

Lesson: constructing a reverse action is insufficient when the carried turn and
unload were authored as different held poses. Keep exact visible first source,
separate the valid source segment from unresolved joins, and review registered
body/case contact before admission. Next explicit paired held-to-lower and final
standing/case bridges, then real controller/safety/Continue. Full James master,
directional context and cross-family polish objective active/incomplete.
Evidence: character/james-east-cargo-heads-v3/return-plan-probe-evidence.json and
return-plan-review.json; return-plan-{bare,helmet}-workshop_* boards.
'''
for path in [r/'docs/CURRENT_STATUS.md',r/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',r/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',r/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]:
    old=path.read_bytes()
    if section.splitlines()[0].encode() not in old:atomic(path,section.encode()+b'\n'+old if path.name=='CURRENT_STATUS.md' else old+b'\n\n'+section.encode())
handoff='''# Project handoff

Updated: October 2, 2026 · Project: Brine Space · Task: James finite cargo returns

## Objective and acceptance
Full James set aligned to masters/style/perspective/size/height/proportions/matte
grade, then cross-family consistency/polish. Full objective active/incomplete.

## Accepted decisions and constraints
Retain selected cargo/turn sources and paired helmet. Register declared pivots;
no global scale/grade change. Missing joins must remain explicit until repaired.

## Current state
Unselected return_plan.gd/.uid constructs328finite dry cargo source plans. Normal
selection/controller unchanged; interruption still visibly fails. Six source-plan
boards reviewed, return-plan-review.json and native evidence retained. Five guides
updated. Selected default workshop and six ordinary Continue checks remain prior
evidence; no return lifecycle is integrated yet.

## Verification
4770native checks0fail, engine0/owner profile unchanged under scratch. Every dry
source slot/both gears retains first source and original later holds.232held/unload
nonidentity gaps;328registered idle/floor-case joins pending. Six actual interruption
source plans reviewed statically, not continuous world motion. No pre-run dependency
freeze, new source art, safety/clearance/controller or return save acceptance.

## Next action
Compare paired West held turn endpoint to unload start and author missing lowering
bridge; final standing/floor-case handoff. Then actual source-bound controller,
needs/emergency priority, room clearance, ordinary Continue and motion review.
Remaining cardinal contexts/West tablet hand edges/full master/cross-family polish
stay open. No commit/export.
'''
atomic(p/'HANDOFF.md',handoff.encode())
print('328 staged plans recorded; six boards reviewed; missing joins and full objective remain open.')
