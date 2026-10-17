from pathlib import Path
import json,hashlib,uuid,os
p=Path(__file__).resolve().parent;r=p.parents[1]
native=json.loads((p/'world-evidence.json').read_bytes());guard=json.loads((p/'world-validation.json').read_bytes())
records=[c for c in native['results'] if 'label' in c];depths=[c for c in native['results'] if c.get('depthDiagnostic')]
assert native['checks']==182 and native['failures']==0 and len(records)==12 and len(depths)==2
assert guard['exitCode']==0 and not guard['timedOut'] and guard['realProfileUnchanged']
assert all(c['caseIndex']<c['crewIndex'] and c['caseDepth']<c['crewDepth'] for c in depths)
inputs=json.loads((p/'world-inputs.json').read_bytes());assert all(hashlib.sha256((r/k).read_bytes()).hexdigest()==v for k,v in inputs.items())
reference=json.loads((p/'reference-evidence.json').read_bytes());assert hashlib.sha256((r/reference['source']).read_bytes()).hexdigest()==reference['sha256']
registration=json.loads((p/'source-registration-evidence.json').read_bytes())
assert len(registration['matches'])==12 and all(c['standingHeight']==148 for c in registration['matches'].values())
def atomic(path,new):
    old=path.read_bytes();tmp=path.with_name(path.name+'.'+uuid.uuid4().hex+'.tmp');tmp.write_bytes(new)
    assert path.read_bytes()==old;os.replace(tmp,path)
path=p/'world-review.json';review=json.loads(path.read_bytes())
review.update(visualReviewPending=False,reviewed='All12 registered source/prop presentations and actual native room captures inspected in bare/helmet boards. Case contact stays fixed as James departs; source/prop upper panes are presentation composites, lower panes actual native room captures. Original selected body/head/helmet registration retained. Generated case differs slightly in pad detail/height; exact continuous release/material seam remains unaccepted.',continuousMotionAcceptance=False,automaticReleaseAcceptance=False,ordinaryContinueAcceptance=False)
atomic(path,(json.dumps(review,indent=2)+'\n').encode())
verdict={'selected':False,'fullGoalComplete':False,'checks':182,'failures':0,'nativeSourceWorldPresentationsReviewed':12,
    'fixedFloorAnchorAcceptedForPrescribedVisualStudy':True,'nativeDrawOrder':'case slot1 depth25.603189; James crew slot2 depth26.485678',
    'targetedPrelaunchHashesUnchanged':8,'originalTerminalReferenceHashUnchanged':True,
    'sourceRgbaBindingsToCurrentSelectedOriginals':12,'sourceManifestHashScope':'Post-run current manifest/source hashes, not prelaunch full dependency freeze.',
    'authoring':'Built-in image_gen three raw sources/exact prompts preserved. V1/V2 rejected shallow silhouettes; V3 native aspect-preserving45x28cell at shared character registration.',
    'firstFailure':'Fixture searched Bill actor slot. James uses crew member slot. First failed log/fixture/guard/source inputs and six existing before/after/departure source/world pairs preserved. No depth/art change required.',
    'ownerProfileUnchanged':True,'automaticFloorReleaseOrWorldLifetimeAccepted':False,'ordinarySaveContinueAccepted':False,
    'remaining':['Match exact continuous source-to-prop release and case material/height seam.','Source-bound automatic ownership, priority behavior and room removal.','Paired ordinary RunSave/Continue.','Other cardinal floor cases, bridge collar/motion/master polish and full James/cross-family review.']}
(p/'acceptance.json').write_text(json.dumps(verdict,indent=2)+'\n')
section='''## James West fixed floor-case native study — October 2, 2026

New unselected West case prop derived from original terminal unload reference.
Three built-in raw edits/prompts retained. V1/V2 shallow/wide silhouettes rejected;
V3 native aspect-preserving extraction45x28cell on256/p128224/H148, floor222.
Right edge inferred from boot occlusion; generated case not original-pixel exact.
Fixture-only workshop renderer inserts normal sorted prop at fixed physical
room-local unload anchor, sort depth2native pixels behind224crew foot. No room
geometry, normal actor selection or source grading changes.

Actual v9 source-bound power-loss carry returns finish West in both gears; fixture
enables prop after finite return, then ordinary next activity departs48.769units.
182native checks0fail;12terminal/idle baseline/idle-case/8/24/48departure source/
world pairs reviewed. Native case stays on floor and sorts behind boots, slot1
depth25.603189 before actual James crew slot2 depth26.485678. Generated pad detail/
height and exact continuous release/material seam still need polish/admission.

First failure was fixture identity: Bill actor slot queried for James crew member.
Confirmed current consumer and fixed fixture, not depth/art. First failed interval
and six existing source/world pairs retained in first-world-run. Final engine0/
no timeout/whole owner profile unchanged scratch; package interval also clean.
All8targeted prelaunch hashes/original terminal reference unchanged. All12captured
source RGBA match current selected West originals; current manifest pivots184/p92172
versus unload256/p128224 bothH148 produce aligned source presentations. Those
source/manifest hashes are post-run; not full prelaunch asset/world freeze.

Upper review panes are registered source/prop composites; lower actual native
room captures. Source canvas differences do not establish stature change. No
automatic release/ownership, priorities/room removal, ordinary save/Continue,
other cardinal props or continuous whole-world acceptance. Candidate unselected.
Lesson: identify the actual actor's retained queue member and texture before
changing depth; Bill actor assertions cannot be copied onto James crew slots.
Next source-bound release/ownership, material/contact seam and ordinary Continue;
remaining bridge/master/cardinal/full cross-family James objective incomplete.
Evidence: character/james-floor-case-west-v1/acceptance.json, world-review.json,
bare-world-review.png and helmet-world-review.png. Full goal active; no commit/export.
'''
for path in [r/'docs/CURRENT_STATUS.md',r/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',r/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',
    r/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]:
    old=path.read_bytes()
    if section.splitlines()[0].encode() not in old:
        atomic(path,section.encode()+b'\n'+old if path.name=='CURRENT_STATUS.md' else old+b'\n\n'+section.encode())
handoff='''# Project handoff

Updated: October 2, 2026 · Project: Brine Space · Task: James West floor-case handoff

## Objective and acceptance
Full James set matching masters/style/perspective/height/proportion/grade; then
cross-family polish. Full goal active/incomplete; candidate unselected.

## Accepted decisions and constraints
Preserve selected crew/art/geometry, one aspect-preserving case extraction.
Physical anchor and source floor222 govern contact/depth. Native owner profile
isolated under scratch APPDATA. No automatic floor policy/economy change admitted.

## Current state
Original terminal reference; three raw built-in sources/exact prompts. Native
V3 floor sprite and package/UID; fixture sorted workshop renderer; actual v9
return-to-idle/departure world probe with original actor sources unchanged.
Registered source/prop and native room review boards, acceptance evidence. Five
guides updated. V9 bridge collar/head-orientation/material polish remains open.

## Verification
182checks0fail/both gears/12source-world presentations reviewed. Case fixed at
unload as ordinary next activity moves48.769units. Case slot1 behind James crew
slot2, actual draw position matches physical anchor. Engine0/owner unchanged.
8targeted prelaunch/original reference hashes unchanged;12source RGBA match current
selected originals and declared pivots/H148 (post-run source/manifest hashes).
First failed fixture queried Bill actor slot; corrected crew texture identification,
failed interval/captures preserved. No artwork/depth change to fix that assertion.

## Next action
Exact source-to-prop release/material/height seam; source-bound automatic floor
ownership and priority/room-removal lifecycle; ordinary paired Save/Continue.
Other cardinal floor cases and bridge continuous/master/cross-family polish.
No normal selection, commit or export. Do not confuse upper source composites
with native room captures or static samples with continuous motion acceptance.
'''
(p/'HANDOFF.md').write_text(handoff)
print('West floor-case182checks/12presentations recorded;five guides/handoff updated. Lifecycle/Continue/full goal remain pending.')
