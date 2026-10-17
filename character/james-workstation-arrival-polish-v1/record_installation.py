from pathlib import Path
import json,uuid
P=Path(__file__).resolve().parent;R=P.parents[1]
def verified(name,required):
 v=json.loads((P/(name+'-validation.json')).read_text());log=(P/(name+'.log')).read_text()
 assert v['exitCode']==0 and not v['timedOut'] and v['realProfileUnchanged']
 assert 'SCRIPT ERROR:' not in log and '\nERROR:' not in log and required in log
verified('native-routes','192 actual goal/movement cases')
verified('test_owner_report_regressions','OWNER REPORT REGRESSIONS PASS')
e=json.loads((P/'route-evidence.json').read_text());assert e['failures']==0
key=lambda x:(x['room'],x['rotation'],x['mode'],x['incoming'])
b={key(x):x for x in e['results'] if x['variant']=='baseline'};a={key(x):x for x in e['results'] if x['variant']=='installed'}
assert len(a)==len(b)==96 and all(a[k]['service'] for k,x in b.items() if x['service'])
assert not any(x['facingSnap'] for x in a.values())
stats=dict(baselineServices=sum(x['service'] for x in b.values()),installedServices=sum(x['service'] for x in a.values()),baselineFacingSnaps=sum(x['facingSnap'] for x in b.values()),installedFacingSnaps=0,lostServiceCases=0)
assert stats['baselineServices']==44 and stats['installedServices']==46 and stats['baselineFacingSnaps']==38
(P/'selection.json').write_text(json.dumps(dict(status='installed_wet_workstation_route_facing',runtimeChanged=True,artChanged=False,fullSetComplete=False,checks=e['checks'],cases=192,**stats,scope=e['scope'],pending=['Swim-to-upright transition clearance and completion at equipment','Life-support approaches from connected rooms; these seeded starts reached no service before or after','Dry workstation transitions and full life/exterior journeys']),indent=2)+'\n')
def atomic(path,fn):
 before=path.read_bytes() if path.exists() else b'';after=fn(before)
 if before==after:return
 tmp=path.with_name(path.name+'.james-'+uuid.uuid4().hex+'.tmp');tmp.write_bytes(after)
 if (path.read_bytes() if path.exists() else b'')!=before:tmp.unlink();raise RuntimeError('Concurrent edit '+str(path))
 tmp.replace(path)
note="""### James wet workstation approach facing installed — September30,2026

James-only wet station_arrival_facing now constrains facing-aware route search to
the equipment heading, scopes failed reachability by desired heading and preserves
route facing through the existing internal smoother. Base hook returns empty;
dry approaches and other actors keep existing behavior. Keep public smooth_route
signature unchanged: adding an optional argument still breaks GDScript subclass
overrides at parse time. The owner-regression fixture caught this; restored API,
clean rerun PASS. Do not update the fixture merely to accommodate the API change.

Actual choose_goal/search/smoothing/move/arrive/normal grid exercised192 paired
baseline/installed cases:3rooms x4rotations x2gear x4starts. 11,515 clean checks
PASS;44 prior service approaches retained,46 now reach services;38 baseline facing
jumps become0. Installed movement tick sweeps retain body/turn clearance; maximum
planned route4 waypoints. Both modes' normal-selected82px arrival pairs reviewed.
The broad tick sweep also flagged2 baseline corner ticks, preserved as diagnostic
failure; final clearance assertions govern installed paths. Real profile unchanged.
Life support reached no station in either variant from these starts; do not claim
its full approach coverage. Prone-to-upright arrival can still jump when transition
clearance is unavailable, visible in reviewed pairs; facing fix is not full motion
acceptance. Connected-room life support, dry equipment and whole journeys remain.
See docs/JAMES_WORKSTATION_ARRIVAL_HANDOFF_2026-09-30.md; full James goal active.

"""
for path in [R/'docs/JAMES_ANIMATION_CONTINUATION_2026-09-29.md',R/'docs/ASSET_PIPELINE_AND_WORKFLOW.md',R/'docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md',R/'skills/brinespace-character-pipeline/references/crew-consistency.md',Path('C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md')]:
 atomic(path,lambda b:b if note.encode() in b else b+b'\n'+note.encode())
headline="""## James wet workstation approach facing installed — September30,2026

Actual paired192-case route test:11,515 clean checks PASS. All44 previous service
approaches retained;46 now reach equipment;38 baseline facing jumps become0.
Owner controller regressions PASS; real profile unchanged. No artwork changes.
Swim-to-upright transitions, connected-room life support and complete journeys
remain. [Handoff](JAMES_WORKSTATION_ARRIVAL_HANDOFF_2026-09-30.md). James goal active.

"""
atomic(R/'docs/CURRENT_STATUS.md',lambda b:b if headline.encode() in b else headline.encode()+b)
handoff="""# Project handoff

Updated:2026-09-30 · Project:Brine Space · Task:James workstation arrival continuity

## Objective and acceptance
Full James animation/master matching and complete cross-family journeys.
Wet equipment-facing route fix installed; full goal and owner acceptance remain.

## Accepted decisions and constraints
Equipment governs facing. Respect body/turn clearance and authored masters;
no blocker bypass, body shrinking or wrong-facing workaround. Preserve public
controller override signatures and unrelated concurrent edits.

## Current state
scripts/bill_npc.gd adds optional desired endpoint heading and cache scope;
_choose_goal invokes James hook and existing internal facing-preserving smoother.
scripts/branforth_npc.gd enables hook for wet consoles/pressure/listening stations.
No art, clocks, layouts or saves changed. Evidence, fixtures and selection in
character/james-workstation-arrival-polish-v1. Pipeline/bible/both skill copies
and current status updated. Historical baseline recorder must not be rerun.

## Verification
11,515 clean checks PASS,192 baseline/installed actual chooser/movement cases.
44 baseline service approaches all retained;46 installed services,38 facing snaps
become0. Installed tick clearance passes;8 selected82px before/after pairs reviewed.
Owner report regressions PASS after restoring unchanged public smooth_route API;
initial signature failure retained. Each final scratch run preserved real profile.
291 controlled-endpoint baseline checks remain diagnostic. These starts reach no
life-support service before or after; do not claim that room's approach accepted.
Clearance probe's2 baseline corner failures retained; final assertions cover new
paths. Paired frames still expose abrupt prone-to-upright arrival when stop lacks
clearance. No full journey, traffic, release or owner visual acceptance claimed.

## Next action
Resolve swim-to-upright equipment arrival using actual pose/transition envelopes;
choose a safe stop point before the contact, not a forced animation through props.
Prove connected-room life-support approaches, dry workstation transitions and full
furniture/meal/equipment/exterior journeys. Keep original full James goal active.
"""
atomic(R/'docs/JAMES_WORKSTATION_ARRIVAL_HANDOFF_2026-09-30.md',lambda b:handoff.encode())
print(json.dumps(dict(checks=e['checks'],cases=192,**stats)))
