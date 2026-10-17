from pathlib import Path
import json
P=Path(__file__).resolve().parent;R=P.parents[1]
v=json.loads((P/'native-baseline-validation.json').read_text());e=json.loads((P/'baseline-evidence.json').read_text());log=(P/'native-baseline.log').read_text()
assert v['exitCode']==0 and not v['timedOut'] and v['realProfileUnchanged']
assert 'SCRIPT ERROR:' not in log and '\nERROR:' not in log
assert e['checks']==291 and e['cases']==96 and e['facingSnaps']==72 and e['failures']==0
summary=[]
for s in e['resolvedServiceNodes']:
    summary.append(dict(room=s['room'],rotation=s['rotation'],mode=s['mode'],validServiceNodes=len(s['candidates']),clearStopNodes=sum(c['stopAllowed'] for c in s['candidates'])))
(P/'service-node-summary.json').write_text(json.dumps(summary,indent=2)+'\n')
(P/'selection.json').write_text(json.dumps(dict(status='diagnostic_baseline',runtimeChanged=False,fullSetComplete=False,checks=291,cases=96,facingSnaps=72,
    scope=e['scope'],pending=['Facing-aware final workstation approach in James route selection','Actual traversed routes and clearance with both equipment modes','Dry workstation arrival and full life/exterior journeys']),indent=2)+'\n')
def atomic(path,fn):
    before=path.read_bytes() if path.exists() else b'';after=fn(before)
    if before==after:return
    tmp=path.with_name(path.name+'.workstation.tmp');tmp.write_bytes(after)
    if (path.read_bytes() if path.exists() else b'')!=before:tmp.unlink();raise RuntimeError('Concurrent edit '+str(path))
    tmp.replace(path)
note='''### James workstation arrival baseline and clearance — September30,2026

Controlled NPC.arrive at authored workstation contacts,3rooms x4rotations x2gear
x4incoming headings:291 checks/96cases PASS establishes72 immediate facing snaps,
not72 animation fixes. Normal grid selected frames reviewed at82px. Every changed
heading at these exact contacts disallowed ordinary transition clearance.
Life-support may stay prone because upright pose is blocked; pressure/listening
contacts can tread immediately. A blanket swim-turn/stop queue would ignore this
geometry. Inspect valid service graph nodes separately from authored contact:
RoomActivity.at admits nearby36px nodes and choose_goal uses spawn-clear nodes,
not an exact raw contact. Node scan found no clear-stop service node in life
support or listening-post q0/q2; pressure and listening q1/q3 have some.

Next fix should constrain the final route heading to station.facing before
arrival, preserving facing-aware swim search/link clearance and smoother endpoint
heading. Verify real routes,not seeded endpoint playback,before claiming fixed.
Current fixture seeds incoming swim at contact; it does not prove actual chosen
paths/traffic or full workstation journeys. Scratch profile unchanged;runtime
unchanged. See docs/JAMES_WORKSTATION_ARRIVAL_HANDOFF_2026-09-30.md;goal active.
'''
for path in [R/'docs/JAMES_ANIMATION_CONTINUATION_2026-09-29.md',R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]:
    atomic(path,lambda b:b if note.encode() in b else b+b'\n\n'+note.encode())
headline='''## James workstation-facing discontinuity diagnosed — September30,2026

Controlled96 workstation arrivals show72 immediate facing jumps;291 checks PASS,
profile unchanged. Contacts often lack stop/turn clearance; valid nearby service
nodes differ from exact authored contact. Runtime unchanged. Next constrain actual
final route heading to equipment facing and prove traversed approaches.
[Handoff](JAMES_WORKSTATION_ARRIVAL_HANDOFF_2026-09-30.md). James goal active.

'''
atomic(R/'docs/CURRENT_STATUS.md',lambda b:b if headline.encode() in b else headline.encode()+b)
handoff='''# Project handoff

Updated:2026-09-30 · Project:Brine Space · Task:James workstation arrival continuity

## Objective and acceptance
Full James animation/master matching and complete cross-family journeys.
Workstation-facing issue diagnosed;no gameplay fix yet,goal active.

## Accepted decisions and constraints
Stations govern intended facing;walk/swim approach must connect coherently.
Respect actual body/transition clearance,station layout and authored masters.
Do not bypass blockers,shrink bodies or retain wrong facing to hide the jump.

## Current state
character/james-workstation-arrival-polish-v1/native-baseline.gd and evidence
probe normal-grid actual NPC.arrive for life_support,pressure_control,listening_post,
four rotations,bare/helmet,four incoming headings. Baseline contact preview and
valid service-node summaries retained. Runtime unchanged. Skills,pipeline,bible
and continuation updated with geometry-aware diagnosis.

## Verification
291 clean native checks PASS,96 controlled endpoint-arrival cases;72 immediate
facing snaps and72 disallowed transitions at exact authored contacts. Incoming
swim seeded at endpoint,not a traversed/autonomous route. Actual-selected82px
source/arrival pair board reviewed. Separate spawn-clear service graph-node scan:
life support and listening q0/q2 have no clear-stop nodes; pressure and listening
q1/q3 have some. Owner profile unchanged;no running processes.

## Next action
Implement James-only desired endpoint heading in facing-aware route selection:
Bill route_between/_route_between_clear currently accept any target facing;
_choose_goal resolves target_station before route search. Constrain wet James
station endpoints to target_station.facing and preserve final heading through
smooth_route (existing keep_route_facing branch provides a safe starting point).
Scope reachability cache by heading;do not reuse direction-agnostic failure
evidence. Test actual chosen/traversed station paths,clearance and source/arrival
frames in both modes,including stations with no upright stop room. Then dry
workstation transitions and full furniture/meal/equipment/exterior journeys.
Keep original full goal intact;291 baseline checks are diagnosis,not completion.
'''
atomic(R/'docs/JAMES_WORKSTATION_ARRIVAL_HANDOFF_2026-09-30.md',lambda b:handoff.encode())
print('Workstation baseline recorded:96cases/72snaps;actual route-facing repair remains;runtime unchanged')
