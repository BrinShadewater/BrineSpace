from pathlib import Path
import json,hashlib,uuid,os
p=Path(__file__).resolve().parent;r=p.parents[1]
data=json.loads((p/'release-evidence.json').read_bytes())
guard=json.loads((p/'release-validation.json').read_bytes())
registration=json.loads((p/'release-registration-evidence.json').read_bytes())
inputs=json.loads((p/'release-inputs.json').read_bytes())
assert data['checks']==220 and data['failures']==0 and len(data['results'])==14
assert guard['exitCode']==0 and not guard['timedOut'] and guard['realProfileUnchanged']
assert len(registration['matches'])==14
assert all(hashlib.sha256((r/k).read_bytes()).hexdigest()==v for k,v in inputs.items())
for mode in ['bare','helmet']:
    rows=[c for c in data['results'] if c['label'].startswith(mode+'-')]
    assert len(rows)==7 and not rows[0]['owned']
    assert all(c['owned'] for c in rows[1:])
    assert all(c['embedded'] and not c['enabled'] for c in rows[1:3])
    assert all(c['enabled'] and not c['embedded'] for c in rows[3:])
def atomic(path,new):
    old=path.read_bytes();temp=path.with_name(path.name+'.'+uuid.uuid4().hex+'.tmp')
    temp.write_bytes(new);assert path.read_bytes()==old;os.replace(temp,path)
review=json.loads((p/'release-review.json').read_bytes())
review.update(visualReviewPending=False,reviewed='All14 registered source/prop composites and corresponding actual native room captures inspected in both gear boards. Body/head/helmet registration held. Separate generated case hardware/height/material seam remains unaccepted.',continuousMotionAcceptance=False,ordinaryContinueAcceptance=False)
atomic(p/'release-review.json',(json.dumps(review,indent=2)+'\n').encode())
verdict={'selected':False,'fullGoalComplete':False,'checks':220,'failures':0,'actualPrescribedReturns':2,'nativeSourceWorldPairsReviewed':14,'targetedInputsUnchanged':12,'ownerProfileUnchanged':True,'sourceBoundAutomaticReleaseForPrescribedWestStudy':True,'cue':'Original unload-west source4, both hands clear; exact RGBA hex SHA bound.','duplicateSuppression':'Room owns at cue; separate sorted prop hidden while exact source embeds it; visible at idle and fixed through ordinary48.769unit departure.','sourceRegistrationScope':'14 captured source images match current selected original RGBA/pivots/H148; post-run source/manifest hashes, not full prelaunch dependency freeze.','remaining':['Exact continuous case hardware/height/material join.','Before/after release emergency/gear/death/new-service/room-removal priorities.','Paired ordinary RunSave/Continue and normal selection.','Other cardinals; bridge collar/head turn and full master/cross-family polish.']}
(p/'release-acceptance.json').write_text(json.dumps(verdict,indent=2)+'\n')
section='''## James West automatic source-bound floor release — October 2, 2026

Unselected floor_actor/player/state/release_workshop now transfer cosmetic case
ownership at original unload-West4, both hands clear, bound to exact bare/helmet
RGBA hashes and validated source clocks. The room-local anchor remains physical
unload contact. Separate sorted prop is hidden while the exact source embeds its
case, appears at idle and stays fixed through ordinary48.769unit departure.
No manual case enable; normal actor/source selection remains unchanged.

220native checks0fail/two actual prescribed power-loss carry returns. All14
registered source/prop and corresponding actual native room captures inspected;
original body/head/shared helmet registration held. Separate case pad/profile/
height/material seam still unaccepted. Engine0/no timeout/whole owner profile
unchanged under scratch APPDATA;12targeted prelaunch hashes unchanged.14captured
source RGBA matches to current selected originals/pivots/H148 are post-run bindings,
not a full prelaunch world/asset freeze or continuous movie acceptance.

Malformed room payload/clock/wrong artwork/early cue/duplicate observation guards
pass. Lesson: tie ownership to reviewed hands-clear source and observe crossing
before finite plan cleanup; suppress only the exact embedded case at its owned
anchor. Cosmetic room persistence is distinct from actor motion and inventory.
Skipped-cue/large-delta native evidence, before/after priority/room removal,
ordinary paired RunSave/Continue, normal admission and other cardinals remain
separate gates. Full James/master/cross-family objective active/incomplete.
Evidence:character/james-floor-case-west-v1/release-acceptance.json,
release-review.json,release-validation.json. No commit/export.
'''
guides=[r/'docs/CURRENT_STATUS.md',r/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',r/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',r/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]
for path in guides:
    old=path.read_bytes()
    if section.splitlines()[0].encode() not in old:
        atomic(path,section.encode()+b'\n'+old if path.name=='CURRENT_STATUS.md' else old+b'\n\n'+section.encode())
handoff='''# Project handoff

Updated: October 2, 2026 · Project: Brine Space · Task: James West floor-case release

## Objective and acceptance
Full James set matching directional masters/style/perspective/height/proportions/
matte grade, then cross-family polish. Goal incomplete; candidate unselected.

## Accepted decisions and constraints
Preserve selected sources, room geometry and owner profile. Staged cosmetic
latest James case per workshop; no inventory/collision policy admitted.

## Current state
Built-in raw case sources/prompts and aspect-preserving native package retained.
floor_state/floor_actor/floor_player/release_workshop own exact source-bound cue
and duplicate suppression. release.gd, evidence/boards/acceptance record reviewed
automatic handoff. Manual182check study and first failed fixture remain preserved.

## Verification
Automatic220checks0fail/two actual carry returns/both gears/14 source-world pairs
reviewed. Engine0/scratch owner unchanged/12targeted hashes unchanged. Source
bindings/pivots are post-run, not full dependency freeze. Body/helmet registered;
generated case hardware/height/material seam still unaccepted. Five guides updated.

## Next action
Skipped-cue/finite completion crossing; before/after release priority and room
removal; paired ordinary Save/Continue. Polish continuous case join, V9 collar/
head turn, other cardinals and full master/cross-family set. No normal admission,
commit/export or continuous whole-world acceptance.
'''
atomic(p/'HANDOFF.md',handoff.encode())
print('Automatic220check release/14 reviewed pairs recorded;five guides and handoff updated.')
