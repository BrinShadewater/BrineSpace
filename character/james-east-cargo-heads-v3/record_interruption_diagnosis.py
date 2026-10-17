from pathlib import Path
import hashlib, json, os, uuid

p = Path(__file__).resolve().parent
r = p.parents[1]
guard = json.loads((p/'interruption-probe-validation.json').read_bytes())
probe = json.loads((p/'interruption-probe-evidence.json').read_bytes())
audit = json.loads((p/'interruption-source-audit.json').read_bytes())
assert guard['exitCode'] == 0 and not guard['timedOut'] and guard['realProfileUnchanged']
assert probe['checks'] == 54 and probe['failures'] == 0 and len(probe['results']) == 6
assert all(x['sameFoot'] and x['afterPose']=='idle' and x['afterStage']=='' for x in probe['results'])
assert all(all(c['matches'] for c in x['captures']) for x in audit['results'])
assert hashlib.sha256((r/'scripts/grid_canvas.gd').read_text().encode()).hexdigest() == audit['loaderSha256']
assert all(hashlib.sha256((r/path).read_bytes()).hexdigest()==h for path,h in audit['manifestHashesAtAudit'].items())

def atomic(path, new):
    old = path.read_bytes()
    temp = path.with_name(path.name+'.'+uuid.uuid4().hex+'.tmp')
    temp.write_bytes(new)
    assert path.read_bytes() == old
    os.replace(temp,path)

verdict = {
    'nativeDiagnosticChecks':54, 'diagnosticFailures':0,
    'visualInterruptionAcceptance':False,
    'visualReview':'All six source/room before-after comparisons and all four directional standing endpoints in both gears reviewed.',
    'findings':[
        'Power loss clears workshop stage and selects idle within one 20ms update; physical foot remains fixed in all six cases.',
        'Pickup and carry visibly lose the held crate with an abrupt body/arm change; North unload switches to a different standing endpoint.',
        'Carry samples are East-to-West turn source index2, not ordinary West gait; aliases include other connected turns.',
        'North unload uses unload-north index5 while locomotion cache still says West; do not infer action facing from that cache.',
        'Pickup/unload exact reversal does not prove a registered return to selected idle or persistence of the floor crate.',
        'Idle source canvas184/pivot92,172 and cargo256/pivot128,224 share standingHeight148. Pivot-aligned four-direction comparison shows close standing heights; raw-canvas placement is invalid for size review.'
    ],
    'correctionSelected':False, 'fullGoalComplete':False,
    'next':'Author a finite return from the exact displayed source, including interrupted turns and explicit crate release/standing join. Verify needs and emergency priority, then ordinary Continue and native motion.'
}
(p/'interruption-review-evidence.json').write_text(json.dumps(verdict,indent=2)+'\n')
section='''## James workshop interruption defect confirmed — October 2, 2026

Actual default workshop power-loss diagnostic completed: six prescribed pickup,
mid-turn carry and North unload cases, both initial gears. Native54checks0fail,
engine0/no timeout; whole owner profile unchanged under scratch APPDATA. These
checks certify diagnostic execution, not visual acceptance. All six source/world
before-after comparisons reviewed: stage clears and idle replaces the pose within
20ms at unchanged physical foot. Held crate disappears abruptly in pickup/carry;
unload switches to a different standing stance. Visual interruption acceptance FAILED.

Current ordered James manifests resolve every native before/after source exactly.
Carry before is East-to-West turn index2, not ordinary West gait. North unload is
unload-north5 although locomotion cache still says West. Source aliases alone do
not identify active transition/facing. Exact pickup/unload reversal holds for the
reviewed endpoint directions but does not bridge selected idle or retain a floor
crate. Four-direction/both-gear endpoint board aligns declared pivots: idle184/
p92,172 versus cargo256/p128,224, both H148. Standing heights look close after
registration; do not globally rescale from unregistered canvas comparisons.

Lesson: diagnostic green checks can expose failed animation joins. Record visual
failure separately. Capture displayed texture plus actor action and active turn
clock; cached locomotion facing can be stale during actions. A complete return
must preserve the visible first pose, finish/reverse interrupted turn safely,
release cargo coherently and reach selected idle while needs/safety remain live.
No corrective controller/art/selection change yet. Next finite source-bound
return and crate disposition, interruptions/Continue/motion; remaining master,
material/perspective/proportion/height and full cross-family polish remain open.
Evidence: character/james-east-cargo-heads-v3/interruption-review-evidence.json,
interruption-before-after-review.png and cargo-standing-endpoint-review.png.
'''
for path in [r/'docs/CURRENT_STATUS.md',r/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',r/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',r/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]:
    old=path.read_bytes()
    if section.splitlines()[0].encode() not in old:
        atomic(path,section.encode()+b'\n'+old if path.name=='CURRENT_STATUS.md' else old+b'\n\n'+section.encode())
path=p/'selection-evidence.json'
selection=json.loads(path.read_bytes())
selection['workshopPowerLossInterruptionAcceptance']=False
selection['workshopPowerLossEvidence']='interruption-review-evidence.json'
atomic(path,(json.dumps(selection,indent=2)+'\n').encode())
handoff='''# Project handoff

Updated: October 2, 2026 · Project: Brine Space · Task: James workshop interruptions

## Objective and acceptance
Full James master/style/perspective/size/height/proportion/matte set, then
cross-family polish. Full objective active/incomplete.

## Accepted decisions and constraints
Retain selected corrected East cargo/turn artwork and original shared helmet.
No owner room/profile or global scale change. Pivot-aligned source review required.

## Current state
Selected9states/128refs retain prior actual default workshop and six disk Continue
acceptances. New interruption-probe and source audit establish a visual defect:
pickup/carry/unload snap to idle at real power loss. Two comparison boards and
interruption-review-evidence.json record reviewed failure; five guides updated.
No production animation/controller repair yet.

## Verification
Prior actual workshop3382checks0fail. New interruption54checks0fail are diagnostic,
not visual acceptance; engine0/owner profile unchanged. All12native source captures
bind exactly to current ordered manifests. Six before-after source/world cases
and four directions/both gears standing endpoints reviewed. Manifest/loader audit
hashes checked at recording. No full continuous motion or natural scheduler claim.

## Next action
Finite return from exact displayed source, preserve mid-turn source/clock, coherent
crate release/floor and idle join; needs/safety priority and ordinary Continue.
Then remaining turn/room contexts, West tablet hand edges and full cross-family
master/material/proportion/perspective/height/motion polish. No commit/export.
'''
atomic(p/'HANDOFF.md',handoff.encode())
print('Recorded six failed visual joins, source bindings, registered endpoint review and next repair requirements; five guides updated.')
