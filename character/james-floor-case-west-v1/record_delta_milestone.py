from pathlib import Path
import json,hashlib,uuid,os
p=Path(__file__).resolve().parent;r=p.parents[1]
data=json.loads((p/'delta-evidence.json').read_bytes())
guard=json.loads((p/'delta-validation.json').read_bytes())
review=json.loads((p/'delta-review.json').read_bytes())
inputs=json.loads((p/'delta-inputs.json').read_bytes())
rows=[c for c in data['results'] if c.get('crossing')]
assert data['checks']==88 and data['failures']==0 and len(rows)==4
assert guard['exitCode']==0 and not guard['timedOut'] and guard['realProfileUnchanged']
assert len(json.loads((p/'delta-registration-evidence.json').read_bytes())['matches'])==8
assert all(hashlib.sha256((r/k).read_bytes()).hexdigest()==v for k,v in inputs.items())
assert all(c['delta']>.3 and c['before']<c['release']<c['after'] and c['ownedBeforeDrawing'] for c in rows)
assert all(c['returnClearedBeforeDrawing']==(c['jump']=='complete') for c in rows)
def atomic(path,new):
    old=path.read_bytes();temp=path.with_name(path.name+'.'+uuid.uuid4().hex+'.tmp')
    temp.write_bytes(new);assert path.read_bytes()==old;os.replace(temp,path)
review.update(visualReviewPending=False,reviewed='All8 registered source/prop and actual native room presentations inspected in both gear boards. Stable physical contact and registered head/body/helmet across skipped unload holds. Generated separate-case profile/material seam remains unaccepted.',continuousMotionAcceptance=False,ordinaryContinueAcceptance=False)
atomic(p/'delta-review.json',(json.dumps(review,indent=2)+'\n').encode())
section='''## James West skipped release and completion cue — October 2, 2026

Four real prescribed carry power-loss returns/bare and helmet now cross several
remaining unload holds in one actual actor update without intermediate drawing.
88native checks0fail/eight before-after source/world presentations reviewed.
Room ownership asserted before renderer observation: cue crossing retains finite
plan and suppresses duplicate embedded prop; crossing completion first releases,
then clears the plan and draws the separate fixed case. Physical contact held.
Engine0/no timeout/whole owner profile unchanged under scratch APPDATA;
12targeted prelaunch hashes unchanged. Eight captured source RGBA/pivot bindings
to current selected originals are post-run, not a recursive dependency freeze.

Earlier narrower green interval retained in first-delta-run. Final delta values
and source clocks are in delta-evidence.json; no skipped intermediate-frame visual
claim. Lesson: assert ownership before asking renderer for a frame, otherwise a
renderer hook can hide a missing actor cue-crossing path. Review contact separately
from case profile/material continuity. Exact source-to-prop visual seam, native
before/after emergency/gear/death/new-service/room-removal, ordinary paired
Save/Continue, other cardinals and normal admission remain open. V9 bridge and
full James/master/cross-family polish remain incomplete. No commit/export.
Evidence:character/james-floor-case-west-v1/delta-review.json,
delta-evidence.json,delta-validation.json. Staged candidate remains unselected.
'''
for path in [r/'docs/CURRENT_STATUS.md',r/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',r/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',r/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]:
    old=path.read_bytes()
    if section.splitlines()[0].encode() not in old:
        atomic(path,section.encode()+b'\n'+old if path.name=='CURRENT_STATUS.md' else old+b'\n\n'+section.encode())
path=p/'HANDOFF.md';old=path.read_bytes()
addition='''
## Skipped-cue verification
delta.gd/native88checks0fail/four actual returns/both gears/eight registered
source-world pairs reviewed. Ownership checked before drawing after multi-hold
cue/completion jump; exact contact retained.12targeted hashes/owner unchanged.
Earlier narrower green interval retained. Delta evidence/boards and five guides
updated. Next native priorities/room removal before/after release, then paired
ordinary Save/Continue and visual case/V9 bridge/cardinal/master polish.
'''
if b'## Skipped-cue verification' not in old:atomic(path,old+addition.encode())
print('Four multi-hold crossings/88checks/eight reviewed pairs recorded;five guides/handoff updated.')
