from pathlib import Path
import json,uuid
P=Path(__file__).resolve().parent;R=P.parents[1]
def atomic(path,data):
 before=path.read_bytes() if path.exists() else None
 tmp=path.with_name(path.name+'.james-'+uuid.uuid4().hex+'.tmp');tmp.write_bytes(data)
 assert (path.read_bytes() if path.exists() else None)==before
 tmp.replace(path)
reports={}
for name in ['native-crowd','native-hazard','native-contact']:
 v=json.loads((P/(name+'-validation.json')).read_bytes());e=json.loads((P/(name+'-evidence.json')).read_bytes())
 assert v['exitCode']==0 and not v['timedOut'] and v['realProfileUnchanged'] and e['failures']==0
 assert not any(x in (P/(name+'.log')).read_text(errors='replace') for x in ['ERROR:','SCRIPT ERROR:','WARNING:'])
 reports[name]=e
c,h,k=(reports[x] for x in ['native-crowd','native-hazard','native-contact'])
assert c['checks']==29 and h['checks']==2571 and k['checks']==39
for name,folder in [('prior-crowd-drop-evidence.json','prior-crowd-captures'),('prior-hazard-fixture-evidence.json','prior-hazard-captures')]:
 path=P/name;data=path.read_bytes().replace(b'/captures/',('/'+folder+'/').encode());atomic(path,data)
path=P/'selection.json';selection=json.loads(path.read_bytes())
selection['crowd']={'checks':29,'actualJourneys':2,'minimumSeparation':32.0,'actualPeerNextService':True,'evidence':'native-crowd-evidence.json'}
selection['hazards']={'checks':2571,'actualJourneys':6,'cases':['fire','flood','oxygen-loss'],'evidence':'native-hazard-evidence.json'}
selection['changedContacts']={'checks':39,'actualJourneys':4,'runtimeCancellation':True,'inMemoryRestoreRejection':True,'freshSceneDiskChangeRestore':False,'evidence':'native-contact-evidence.json'}
selection['remaining']=['Owner visual review','Other source-index native entries, gears/facings/custom layouts and crowded hazards','Changed-contact fresh-scene disk Continue','Full exterior/mortality journeys and cross-family consistency/polish']
atomic(path,(json.dumps(selection,indent=2)+'\n').encode())
title='James meal-return traffic and emergency cleanup — September 30, 2026'
lesson="""
### James meal-return traffic and emergency cleanup — September 30, 2026

Idle cosmetic prop returns must be unavailable to generic step-aside requests.
Queued Bill counter intent reproduced two premature drops; James now finishes
his return, then yields normally. Two actual shared journeys pass29 checks,
minimum separation32 and Bill reaches the counter afterward. Death must clear
James return data inside die(): lethal vitals remove him from the live roster,
so a later actor update cannot perform cleanup. Six real fire/flood/oxygen-loss
cases pass2,571 checks; four counter replacement/removal cases pass39 checks
including in-memory restore rejection. These are bare North/source3/default-site
proofs, not all36 entries or fresh-scene changed-layout Continues.
Test emergency segment safety from the actual pre-move foot: fire logic allows
leaving the current burning room but forbids entering it from a refuge. Reset
running/paused/crew and summary visibility between lethal fixture cases; actual
zero-crew death legitimately ends the run. Bought counters retain facing on
room rotation: rotate-only is not evidence that contact became invalid. Failed
fixtures, genuine defect baselines and modal-covered captures retained.
No new raster/grade/scale edits. All184 dry turn poses previously measured
147–149px vs147–148px masters; preserve authored camera projection. See
JAMES_MEAL_INTERRUPT_TRAFFIC_HANDOFF_2026-09-30.md. Full James goal active.
"""
for path in [R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]:
 before=path.read_bytes()
 if title.encode() not in before:atomic(path,before+lesson.encode())
path=R/'docs/CURRENT_STATUS.md';before=path.read_bytes()
if title.encode() not in before:atomic(path,('## '+title+'\n\nJames now holds a safe meal return against queued idle step-aside and clears\nreturn data immediately on death. 29 traffic checks/two actual queued Bill\nservices, 2,571 hazard checks/six fire/flood/oxygen-loss cases and39 changed-contact\nchecks/four actual counter replacements/removals pass. Scratch owner profiles\nunchanged. Existing whole-source matte/proportions unchanged. Other native entry\ntimings/gears/layouts, changed-contact fresh-scene disk Continue and full exterior/\nmortality/cross-family polish remain. Goal active; owner visual review pending.\n[Handoff](JAMES_MEAL_INTERRUPT_TRAFFIC_HANDOFF_2026-09-30.md).\n\n').encode()+before)
handoff="""# Project handoff

Updated:2026-09-30 · Project:Brine Space · Task:James return traffic/emergency consistency

## Objective and acceptance
Continue the full James set and master/motion consistency. This milestone covers
actual safe North meal returns under queued crew traffic, hazards and lost contacts.
Full goal active; installed_owner_review_pending. No export/commit.

## Accepted decisions and constraints
Matte neutral masters, belt wrench, tablet diagnostics, forward repair torch,
independent facings and fixed pivots. No new raster or per-pose fitting here.
Counters retain facing on room rotation. Authorized reversible work continues.

## Current state
scripts/branforth_npc.gd: can_step_aside excludes active meal returns; die clears
meal_return before shared death. Native-crowd/hazard/contact fixtures, builders,
evidence, logs, captures and selection.json in james-meal-interrupt-north-v1.
Failed intent fixture/actual crowd drops/stale death/counter-rotation assumptions
retained separately. Pipeline/bible/canonical+installed skill lessons updated.

## Verification
29 checks/two actual interrupted North services with queued actual Bill intent;
fixed return/no premature prop drop, separation32, next actual Bill service.
2,571 checks/six normal chooser meals, interrupted mid-return by genuine fire,
flood or oxygen depletion. Immediate preemption/no credit, actual refuge routes
or death, no stale return. Fire segment checks use actual origin context.
39 checks/four actual counter replacement/removal interruptions; runtime contact
cancellation and in-memory snapshot restore rejection. No fresh-scene disk claim.
Every final run exit0/no timeout/no engine warnings, real profile unchanged.
Traffic/contact and representative hazard captures reviewed; death capture is
initial selected pose, not full mortality motion. Earlier report-covered captures
archived; fixture hides summary only for actor review after actual death assertion.

## Next action
Other source-index native entry timings/gears/facings/custom counters; changed-
contact disk Continue, crowded hazards, full exterior/mortality journeys and
cross-family motion/grade polish. Earlier all184 dry turns147–149px vs master
147–148px remains measured evidence; helmet projection differs by facing.
"""
atomic(R/'docs/JAMES_MEAL_INTERRUPT_TRAFFIC_HANDOFF_2026-09-30.md',handoff.encode())
print('Recorded James milestone:29 traffic/2571 hazards/39 changed-contact checks; full goal active')
