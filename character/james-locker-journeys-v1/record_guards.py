from pathlib import Path
import json
import os
import uuid
P=Path(__file__).resolve().parent
R=P.parents[1]
TITLE='James fitting Continue and service-loss guards verified - September 30, 2026'
def atomic(path,content,before=None):
    if before is None:before=path.read_bytes() if path.exists() else None
    temp=path.with_name(path.name+'.james-'+uuid.uuid4().hex+'.tmp');temp.write_bytes(content)
    if (path.read_bytes() if path.exists() else None)!=before:
        temp.unlink();raise RuntimeError('Concurrent edit: '+str(path))
    os.replace(temp,path)
reports={}
for name in ['native-locker','native-locker-restore','native-locker-power']:
    validation=json.loads((P/(name+'-validation.json')).read_bytes())
    assert validation['exitCode']==0 and not validation['timedOut'] and validation['realProfileUnchanged'],name
    log=(P/(name+'.log')).read_text(encoding='utf8')
    assert not any(marker in log for marker in ['SCRIPT ERROR:','ERROR:','WARNING:']),name
    reports[name]=json.loads((P/(name+'-evidence.json')).read_bytes())
    assert reports[name]['failures']==0 and len(reports[name]['results'])==8
restores=reports['native-locker-restore'];power=reports['native-locker-power']
assert all(row.get('restore') and row['arrivalHeading']=='east' for row in restores['results'])
assert all(row.get('powerInterruption') and row['arrivalHeading']=='east' for row in power['results'])
restores['scope']='Eight actual disk writes/read/staged Continue restores: before/after shelf markers and mid-held poses for fit/remove, plus both pending approach trips. Exact actor/timer/path, selected pixels, shelf state, simulation clock and paused pixels preserved. All eight normally finish and reach the next chosen task. Real core release supplies roster; original unrecovered pod records retained. Standard four rotations/seed17 only.'
power['scope']='Eight actual room-service power losses during normal fitting/removal at sampled pre/post markers and held poses. No premature gear commit; obsolete requests/routes cleared, same foot, reusable shelf returns, offline UI requests refused. Normal retry finishes all12 selected slots and reaches the next task. Immediate unchanged-gear idle is current abort behavior; finite visual return motion is not proven. Other hazards, layouts and traffic remain separate.'
for name,data in [('native-locker-restore',restores),('native-locker-power',power)]:
    atomic(P/(name+'-evidence.json'),(json.dumps(data,indent=2)+'\n').encode())
selection_path=R/'character/james-helmet-fitting-east-v1/selection.json'
before=selection_path.read_bytes();selection=json.loads(before)
selection['productionFittingGuards']={'continueChecks':restores['checks'],'actualRestores':8,'powerChecks':power['checks'],'serviceLosses':8,'abortVisualPolicy':'Immediate unchanged-gear idle; animated abort-return remains separate.','evidence':['character/james-locker-journeys-v1/native-locker-restore-evidence.json','character/james-locker-journeys-v1/native-locker-power-evidence.json'],'fullSetComplete':False}
selection['limitations']=['Standard four-rotation fitting/next-task journeys, eight actual Continue restores and eight service-loss/retries verified. Other layouts, crowded lockers, refill, other hazards and finite abort-return motion remain separate.']
selection['next']='Review interrupted held-helmet return motion, then continue furniture, meal and exterior journey polish; full James goal active.'
atomic(selection_path,(json.dumps(selection,indent=2)+'\n').encode(),before)
handoff=f'''# Project handoff

Updated: September 30, 2026 · Project: BrineSpace · Task: James equipment checkpoint/guards

## Objective and acceptance
Continue the full James animation and consistency goal. Prior owner acceptance of fitting
art remains; these are agent-verified guard/checkpoint cases, not full-set acceptance.

## Accepted decisions and constraints
Selected source poses, grade, master density and2.14/2.24s fitting clocks unchanged.
Existing reversible-work authorization; no runtime code/art, layout, export or commit.

## Current state
Builders and native fixtures for Continue and room-service power loss added under
`character/james-locker-journeys-v1`. Restore fixture uses an actual core release roster
and retains unrecovered pod records. Normal, restore and power captures have separate
folders; normal captures/review refreshed after separating initial restore output.
Selection metadata removes superseded checkpoint limitations and links scoped evidence.

## Verification
Actual Continue: {restores['checks']:,} checks, eight real scratch disk writes/read/staged
restores. Fit/remove pre/post shelf handoffs and mid-held poses plus both pending trips;
exact actor/timer/path, pixels, shelf, simulation clock, paused pixels and normal resume.
Room-service loss: {power['checks']:,} checks, eight timed losses/retries. Gear uncommitted,
obsolete request/path clear, grounded foot, reusable shelf restored, offline request
refused; retry traverses all12 slots and next task. Normal refreshed baseline:
{reports['native-locker']['checks']:,} checks/eight fitting and next-task journeys.
All native runs serial; clean logs, exit0, no timeout and real profile unchanged.
Canceled bare/equipped native views inspected against masters; no source-grade change.

Current service-loss visual policy is an immediate unchanged-gear idle. It safely
avoids duplicate/early committed gear but does not animate a held helmet back to its
original location. Do not call this finite interruption-motion polish complete.

## Next action
Review finite held-helmet abort-return using existing authored source poses if needed;
preserve uncommitted gear, dry/safety validity, pause and exact checkpoint clocks.
Continue refill/crowded lockers, furniture/meals and full exterior/airlock-return work.
Other hazards/layouts remain separate; full James goal active.
'''
atomic(R/'docs/JAMES_FITTING_GUARDS_HANDOFF_2026-09-30.md',handoff.encode())
lesson=f'''\n### {TITLE}

Actual fitting Continue passes {restores['checks']:,} checks/eight disk restores, covering
both shelf markers, held poses and pending routes. Exact actor/timer/path/pixels/shelf,
simulation clock and pause preserved, then normal completion/next tasks. Actual room
service loss/retry passes {power['checks']:,} checks/eight cases. Clean serial native
scratch runs; owner profile unchanged. Selected artwork/material/clock unchanged.

Use a real release roster and retain unrecovered pod records for valid checkpoints.
Give derived fixtures separate capture folders; preserve native report references when
moving artifacts and refresh the normal review if a derivative overwrote its captures.
Frame/shelf equality must be checked around handoff events, not only at endpoints.

Safe gear cancellation is distinct from smooth interruption art. Current power loss
selects unchanged-gear idle immediately and restores the reusable shelf; it does not
animate a held item returning. Record that limit rather than declaring interruption
motion polished. See docs/JAMES_FITTING_GUARDS_HANDOFF_2026-09-30.md; full goal active.
'''
for path in [R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]:
    before=path.read_bytes()
    if TITLE.encode() not in before:atomic(path,before+lesson.encode(),before)
path=R/'docs/CURRENT_STATUS.md';before=path.read_bytes()
if TITLE.encode() not in before:
    section=f'''## {TITLE}

Eight actual Continue restores pass {restores['checks']:,} checks: exact actor/path/timer,
pose, shelf, paused clock and normal resume. Eight room-service power losses/retries
pass {power['checks']:,} checks without premature gear changes or obsolete requests.
Normal {reports['native-locker']['checks']:,}-check baseline refreshed; all clean serial
scratch runs preserve owner profile. Selected art/code unchanged. Current power-loss
idle return is immediate; finite held-item return polish remains separate. Full goal
active. [Handoff](JAMES_FITTING_GUARDS_HANDOFF_2026-09-30.md).

'''
    atomic(path,section.encode()+before,before)
print(json.dumps({'continueChecks':restores['checks'],'restores':8,'powerChecks':power['checks'],'powerLosses':8,'fullSetComplete':False}))
