"""Historical staging recorder: refuses to overwrite an installed selection."""
import json
from pathlib import Path
if json.loads((Path(__file__).resolve().parent/"selection.json").read_text()).get("runtimeInstalled",False):
    raise RuntimeError("Already installed; use record_installation.py, not the historical staging recorder")
from pathlib import Path
import json,uuid
p=Path('character/james-console-water-exit-turn-v1')
for name in ['native-staged','native-journey']:
 report=json.loads((p/(name+'-validation.json')).read_text());assert report['exitCode']==0 and not report['timedOut'] and report['realProfileUnchanged'];log=(p/(name+'.log')).read_text();assert 'ERROR' not in log and 'WARNING' not in log
pkg=json.loads((p/'verification.json').read_text());contact=json.loads((p/'native-staged-evidence.json').read_text());journey=json.loads((p/'native-journey-evidence.json').read_text());assert (pkg['checks'],contact['checks'],journey['checks'])==(52,522,52738);assert len(journey['results'])==8
selection={'status':'staged_actual_move_journey_pass','runtimeInstalled':False,'fullSetComplete':False,'states':['swim-turn-west-north','swim-turn-north-west'],'uniqueFrames':12,'references':24,'packageChecks':52,'nativeContactChecks':522,'stagedJourneyChecks':52738,'journeys':8,'scope':journey['scope'],'pending':['Production James-only wet-console contact/route hooks and stationary turn holds','Interruptions, gear changes, death and disk restore through holds','Other reachable departure goals, traffic and complete cross-family journeys']}
(p/'selection.json').write_text(json.dumps(selection,indent=2)+'\n',encoding='utf8')
lesson='''### James flooded-console approach and compact exit staged - September 30, 2026

A stationary quarter fitting the console does not prove departure. Actual graph
routes after the East-facing reverse immediately turnWest; the old East/West half
cannot fit and is canceled. Diagnostic route probe:32 approach candidates,8 paths
from South storage reach fine contact without intersections/canceled turns. The
first departure probe found14 paths and14 canceled turns. A left-lane egress after
stationary North-to-West gives14 paths but6 other-route cancellations; only the
proved South return route is the current promotion candidate. Missing paths are
not passes. That exploratory egress run retained unrelated Bill artwork warnings;
its counts are diagnostic, not clean runtime acceptance.

Independently authored West/North whole poses and exact reverse now use fixed25/50
cranial density, same muted matte calibration and canonical selected helmet heads
within19px ellipses. Exact selected West/North endpoints; finite520ms preserved.
All middle feet stay within North master's192 rows, full rear reach28.22919. No
mirroring, limb warps, height fitting or body splicing. Raw source/prompt/SHA retained;
12 frame hashes unchanged after deterministic rebuild.52 package/522 clean native
contact checks PASS. Boards and six staged native journey views visually reviewed.

Eight complete staged South-storage approach/console/return paths (four rotations,
two gear) pass52738 checks at120Hz:actual facing-aware graph/smoothing/move and normal
grid player; every selected pose/body clear, no canceled route turns, stationary
East-to-North,6s North swim dwell, stationary North-to-West before translating.
Both candidate manifests and exact selected turn gates are scratch-only; holds
are supplied by the fixture. This proves animation/route composition, NOT normal
update/safety, controller integration, arbitrary next goals, save or owner acceptance.
Production needs explicit stationary holds, contextual exact clip gates, valid fine
contact restore and interruption cleanup. Preserve existing safety handling and dry
station behavior. Runtime/registry/active sources unchanged this milestone.
Evidence:docs/JAMES_CONSOLE_WATER_EXIT_HANDOFF_2026-09-30.md.
'''
def atomic_transform(path,fn):
 path=Path(path);before=path.read_bytes();after=fn(before);temp=path.with_name(path.name+'.james-'+uuid.uuid4().hex+'.tmp');temp.write_bytes(after)
 if path.read_bytes()!=before:temp.unlink();raise RuntimeError('Concurrent change: '+str(path))
 temp.replace(path)
for path in ['docs/ASSET_PIPELINE_AND_WORKFLOW.md','docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md','skills/brinespace-character-pipeline/references/crew-consistency.md','C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md']:
 atomic_transform(path,lambda b:b+b'\n\n'+lesson.encode('utf8') if lesson.splitlines()[0].encode() not in b else b)
status='''## James flooded-console approach and compact exit staged - September 30, 2026

New independent West/North compact quarter and exact reverse retain master density,
matte grade/endpoints and520ms clock.52 package/522 native contact checks PASS.
Eight staged South-storage approach/6s console/return journeys pass52738 checks:
actual graph/smoothing/move and normal grid player, full body/selected poses clear,
no canceled turns; both stationary turns finish before translation. Native views
reviewed; real profiles unchanged. Runtime remains unchanged:fixture supplies hold
stages and candidate clip gates. Production controller holds/contact restore,
interruptions and other departure goals next. Full James goal active.
[Handoff](JAMES_CONSOLE_WATER_EXIT_HANDOFF_2026-09-30.md).

'''
atomic_transform('docs/CURRENT_STATUS.md',lambda b:status.encode()+b if status.splitlines()[0].encode() not in b else b)
old=Path('character/james-console-water-turn-v1/selection.json');d=json.loads(old.read_text());d['stagedJourneyEvidence']='../james-console-water-exit-turn-v1/native-journey-evidence.json';d['pending']=['Production contact/route hooks and stationary arrival/departure holds','Interruption, safety/update and disk restore proof','Other goals, traffic and full cross-family journeys'];atomic_transform(old,lambda b:(json.dumps(d,indent=2)+'\n').encode())
print('Recorded staged exit/journey evidence; status, pipeline, bible and both skill copies updated.')
