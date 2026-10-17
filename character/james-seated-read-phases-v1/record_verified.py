from pathlib import Path
import json,os,uuid
P=Path(__file__).resolve().parent;R=P.parents[1]
n=json.loads((P/'validate-evidence.json').read_text());w=json.loads((P/'validate-validation.json').read_text());v=json.loads((P/'packaging-validation.json').read_text())
assert not n['failures'] and n['captures']==172 and not v['failures'] and w['exitCode']==0 and not w['timedOut']
cases=[]
for mode in [0,1]:
    records=[r for r in n['records'] if r['room']=='observation_room' and r['mode']==mode]
    stages=[]
    for r in records:
        if not stages or stages[-1]!=r['stage']:stages.append(r['stage'])
    assert stages==['observation_sit','observation_read_enter','observation_read','observation_read_exit','observation_rise'],stages
    first=next(r for r in records if r['stage']=='observation_read_enter')['simTime'];last=next(r for r in records if r['stage']=='observation_rise')['simTime']
    assert abs(last-first-12)<.05
    cases.append({'mode':mode,'stages':stages,'readingSeconds':last-first})
status='installed_native_controller_verified_owner_review_pending'
for mode in ['bare','helmet']:
    f=P/(mode+'-manifest.json');m=json.loads(f.read_text());m['status']=status;f.write_text(json.dumps(m,indent=2)+'\n')
(P/'selection.json').write_text(json.dumps({'status':status,'runtimeInstalled':True,'fullSetComplete':False,'statesPerMode':12,'references':144,'newlyAuthoredDrawings':0,'sourceBindings':'source-bindings.json','packageChecks':v['checks'],'nativeChecks':n['checks'],'nativeCaptures':n['captures'],'controllerCases':cases,'profileGuard':{'realProfileUnchanged':w['realProfileUnchanged'],'profileDelta':w['profileDelta']},'visualReview':'All172 final native chronological source-change captures on12page boards reviewed, actual q0 North lounge/South observation sofa in both gears. Exact existing authored art, fixed supports and scale; lowering now includes lap-tablet source4 before neutral. Frame-change reconstruction is not continuously watched60Hz gameplay.','nativeScope':n['scope'],'remaining':['Actual service-loss/entry and held interruptions','Fresh-scene checkpoint Continue in each new reading phase','All-cardinal phase admission and other furniture/gear/travel handoffs','Full library motion/master/owner/export acceptance']},indent=2)+'\n')
note='''

## James seated tablet draw/held/stow controller — October 1, 2026

Actual furniture review passed1044checks/72prescribed q0 source poses: current
192seated admissions plus normal reachable North lounge/South observation sofa,
both gears. All72native room poses reviewed; visible chair contact, no new depth
offset/art change needed. Advancing actual NPC timers then passed2858checks/164
captures yet exposed a visual defect:12second reading ended on held-tablet source3
and immediately selected empty sit-rise0. Four-way source join checks missed it.

Selected james-seated-read-phases-v1 pairs12states/144references per both gears
combined. Existing whole-source0/4/3/2 aliases draw, source2/3 held-reading loop,
exact reverse0/4/3/2 stow; lap-tablet source4 retained before neutral. Repeated
aliases are holds, zero new authored drawings/pixels/grade/geometry.48frozen old
source refs,32used pose refs. Entire12second budget preserved: .48draw +11.04held
+.48stow. James-only controller override uses own player, exact interrupted
entry reverse and held source retained for first.06exit. Grid loader/ACTIVE_ASSETS
select paired phases after prior helmet pitch; other actors unchanged.

234package/2868actual native controller checks0fail;172chronological source-change
captures on12page boards all reviewed. Normal q0 furniture station arrival,
actual60Hz-stepped NPC update through down/draw/held/stow/rise, North lounge and
South reading sofa both gears, fixed physical foot. Engine0/no timeout/strict
owner unchangedtrue/delta[], scratch APPDATA. First phase fit lacked lap-tablet
lowering; archived before current0/4/3/2/reverse sequence and fresh native run.
Index-1 exit capture denotes dynamically retained held texture outside exit pool,
not a missing rendered frame. GIFs reconstruct recorded simulation intervals;
not continuous60Hz video or autonomous incoming/outgoing travel. No actual service
loss, fresh Continue, all-cardinal/controller/rotation or owner acceptance claim.

Lesson: source joins and prescribed furniture poses cannot certify the stage
boundary the real controller chooses. Capture real source changes across the
entire held timer. Split object draw/held/stow so an item stays out during work
and is lowered before standing. Reuse exact whole authored poses; retain the
physical foot, exposure and total activity budget. Full James goal active;
interruption/Continue and remaining full-family consistency polish open. Handoff:
character/james-seated-read-phases-v1/HANDOFF.md.
'''
for f in [R/'docs/CURRENT_STATUS.md',R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]:
    data=f.read_bytes()
    if b'## James seated tablet draw/held/stow controller' in data:continue
    enc=note.encode();new=enc.lstrip(b'\n')+b'\n'+data if f.name=='CURRENT_STATUS.md' else data+enc
    temp=f.with_name(f.name+'.'+uuid.uuid4().hex+'.tmp');temp.write_bytes(new);os.replace(temp,f)
(P/'HANDOFF.md').write_text('''# Project handoff

Updated:2026-10-01 · Project:Brine Space · Task:James seated tablet phases

## Objective and acceptance
Full James animation/master/style/perspective/proportion/material/motion and
cross-family polish. Active, installed/controller verified, owner review pending.

## Accepted decisions and constraints
Matte masters, belt wrench, stationary furniture supports. Reading item stays
out through work, lowers to lap before stow/rise. Original12second activity budget.

## Current state
Paired12states/144whole-source alias refs; no new artwork. Draw0/4/4/3/2/2,
held2/3 alternation, exact reverse stow. Frozen source bindings; new scripts,
grid_canvas.gd/ACTIVE_ASSETS selection and branforth_npc.gd James-only reading
sequence/exit override. Retain actual held source first.06exit. New native
validate.gd/.uid paired, chronological capture/review builder. First phase
attempt archived before lap-tablet correction. Five guides updated.

## Verification
234package/2868native controller checks0fail,172final source-change captures on
12pages all reviewed. North lounge/South observation q0, both gears, actual NPC
updates from normal station arrival through completion. No anatomy/pixel edits;
fixed physical foot. Engine0/no timeout/scratch APPDATA/owner unchangedtrue.
Earlier furniture1044/72poses and pre-fix2858/164captures preserved; green counts
did not prove original held-to-rise tablet continuity. GIF source intervals,
not continuous60Hz footage or autonomous travel.

## Next action
Deterministic manifest rebuild/current inventory. Add actual service-loss/partial
draw and held interruptions, exact source/contact and valid snapshot admission;
fresh-scene checkpoint Continue in new phases. All-cardinal loader/phase checks,
other contexts and full James master/motion/owner/export acceptance remain open.
No native/provider job live. Keep full goal active.
''')
print(json.dumps({'status':status,'packageChecks':v['checks'],'nativeChecks':n['checks'],'cases':cases}))
