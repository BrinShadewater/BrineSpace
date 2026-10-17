from pathlib import Path
import json,hashlib,os,uuid
p=Path(__file__).resolve().parent;r=p.parents[1];o=p/'cadence'
def atomic(path,new):
    old=path.read_bytes();tmp=path.with_name(path.name+'.'+uuid.uuid4().hex+'.tmp');tmp.write_bytes(new)
    assert path.read_bytes()==old;os.replace(tmp,path)
guard=json.loads((p/'cadence_probe-validation.json').read_bytes());assert guard['exitCode']==0 and guard['realProfileUnchanged']
data=json.loads((o/'evidence.json').read_bytes());assert data['checks']==2151 and data['failures']==0
report=json.loads((o/'review.json').read_bytes());assert report['pairedNativePresentations']==46
report.update(visualReviewPending=False,reviewed='All four chronological boards/46paired source-change and pre-departure captures inspected; both West departure full148/82/54/27px views and enlarged heads/collars compared. Cap dip correction retained. Normal dispatch clocks/finite completion/gait0 correct; source West turn-to-walk head/torso/case articulation still abrupt. No continuous watched/natural actor scheduling or full set acceptance.',simulationSamples=sum(len(case['samples']) for case in data['cases']))
atomic(o/'review.json',(json.dumps(report,indent=2)+'\n').encode())
departure=json.loads((o/'departure-review.json').read_bytes());departure.update(visualReviewPending=False,finding='Both West departures inspected: shared planted turn endpoint switches to materially same but differently articulated head/collar/torso/case source. Destination walking carry0 exactly equals unloadWest0 for both gears. Existing V9 carry-settle endpoint pair therefore also describes this missing ordinary departure articulation; do not append an unreviewed bridge or fabricate new endpoints. Head source join repair and lifecycle handoff remain open.')
atomic(o/'departure-review.json',(json.dumps(departure,indent=2)+'\n').encode())
section='''### James normal turn dispatch and West walking join — October 2, 2026

Actual normal grid/player factories, both gears, four corrected turn routes driven
through player.frame at268prescribed20ms simulation samples, finite .8/1.6s then
short distance-driven departure.2151checks0fail/engine0/owner profile unchanged
under scratchAPPDATA.46paired native source-change/pre-departure captures, all
four chronological boards and two full/enlarged West departure boards inspected.
46APNG RGB/duration checks. Fixed display root, prescribed player input; no actual
actor scheduler/room/priority or continuously watched cadence acceptance.

Installed cap correction retained; finite clocks and destination gait0 correct.
West departure still visually abrupt in head/collar/torso/case source articulation.
Actual loaded departure carryWest0 exactly equals unloadWest0 for both gears;
RGBA hashes bind both aliases and preceding turn endpoint. Existing V9 bridge
endpoint pair therefore also covers ordinary West turn-to-walking articulation,
not just work-return hold. Repair its intermediate upper join before considering
native chained turn/settle/gait behavior and save binding; do not invent endpoints.

First parse attempt used unsupported PackedByteArray.sha256_text; corrected to
HashingContext. First executed2143/32fail fixture started at first epsilon sample
but compared elapsed against earlier declared .3 origin. Start turn exactly at .3,
then sample epsilon:2151/0. Both failure intervals retained, no animation changes.
Lesson: compare actual simulation origin and source aliases before classifying
clock failures as art bugs; correct finite selection does not prove seamless source
motion. Same physical source join can serve work-return and moving departure,
but each lifecycle still needs its own admission/interrupt/Continue proof.
Normal artwork/code selection unchanged this turn. Five guides updated; full goal
active/incomplete. Evidence: character/james-helmet-turn-dip-v1/cadence/{review.json,
departure-review.json,evidence.json}, cadence_probe-validation.json, HANDOFF.md.
'''
for path in [r/'docs/CURRENT_STATUS.md',r/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',r/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',r/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]:
    old=path.read_bytes()
    if section.splitlines()[0].encode() in old:continue
    if path.name=='CURRENT_STATUS.md':
        at=old.index(b'### James helmet cap dip corrected and selected');new=old[:at]+section.encode()+b'\n'+old[at:]
    else:new=old+b'\n\n'+section.encode()
    atomic(path,new)
handoff='''# Project handoff

Updated: October 2, 2026 · Project: Brine Space · Task: James normal turn cadence

## Objective and acceptance
Full James set matching masters/style/camera/height/proportions/matte grade,
then cross-family polish. Incomplete; cap correction remains normally selected.

## Accepted decisions and constraints
Preserve canonical anatomy/material/foot root. Work-return V9/riseV6/caseV7
unchanged. Separate source motion from clock/fixture bugs and lifecycle admission.

## Current state
cadence_probe.gd/UID normal player dispatch plus cadence evidence/captures,
four chronology previews, two enlarged departure boards and source alias audit.
All in character/james-helmet-turn-dip-v1; five guides updated. No selection change.

## Verification
2151checks0fail/268prescribed20ms samples;46paired captures all reviewed plus
both West departure details.46APNG RGB/duration checks; owner profile unchanged
under scratchAPPDATA. Actual clocks/end/gait0 correct, cap fixed; West source
head/torso/case jump remains. Loaded carry0 equals unload0 both gears, exact
preceding turn endpoint hashes bound. First parse failure and2143/32fixtureclock
failure retained; exact .3 origin fixes epsilon mismatch without changing art.
No continuously watched/actual scheduler/room/context/master/full-set claim.

## Next action
Repair coherent V9 intermediate head/collar/shoulder join for shared West endpoint
pair; then review work-return and ordinary turn/settle/walk lifecycle independently.
Other cardinal/context/master/material/proportion/cross-family polish remains.
Goal active/incomplete; no blocker or live job. No commit/export.
'''
atomic(p/'HANDOFF.md',handoff.encode())
print(json.dumps({'checks':2151,'failures':0,'samples':report['simulationSamples'],'reviewedPairedCaptures':46,'guidesUpdated':5,'remaining':'Shared West upper/source join plus separate lifecycle admission.'}))
