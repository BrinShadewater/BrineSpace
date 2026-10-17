"""Record partial real-journey evidence and retain the unresolved cardinal failures."""
from pathlib import Path
import hashlib,json
P=Path(__file__).resolve().parent;R=P.parents[1];O=R/'output/veld-distress-escape-v1'
result=json.loads((O/'validation.json').read_text());report=json.loads((O/'journey-checks.json').read_text())
assert not result['passed'] and not result['realProfileChanges'] and len(report['cases'])==4
assert all(r['crossedDryAlive'] and r['safeRecoveryObserved'] and r['minimumAir']<r['initialAir'] for r in report['cases'])
files=[f for f in O.iterdir() if f.is_file()]+[R/'tools/review_veld_distress_escape_v1.gd',R/'tools/review_veld_distress_escape_v1.gd.uid',R/'tools/run_veld_distress_escape_validation_v1.py']
e={'status':'partial_physical_routes_unresolved_vertical_geometry','checks':report['checks'],'failures':report['failures'],'passingPhysicalRoutes':report['cases'],'nativeResult':result,'boundFiles':{f.relative_to(R).as_posix():hashlib.sha256(f.read_bytes()).hexdigest() for f in files},'findings':'q0/q2 bare and helmet cross physically and recover with real respiration. q1/q3 have9 distress-clear tested points and0 routes in authored vertical corridor/storage geometry. Cardinal test remains failed,not promotion evidence.','next':'Probe actual vertical graph doorway connections and per-edge selected swim footprints; distinguish authored furniture/port geometry from safety-route/controller defects before any production change.'}
(P/'escape-investigation.json').write_text(json.dumps(e,indent=2)+'\n',encoding='utf-8')
lesson='''

## Veld cardinal low-air escape investigation open — September 30, 2026

Exact-master joined candidate: real main crew/FloodSafety/room-flow respiration
probe has245 checks/5 failures. Four q0/q2 bare/helmet routes cross physically,
consume oxygen and trigger safe-air recovery. q1/q3 each have9 tested distress
clear points but0 escape routes in vertical corridor/storage geometry. Full
cardinal journey gate remains FAILED; do not select based on four successes.
Preserve current profile and artwork; inspect actual vertical doorway graph links,
per-edge swim footprints and authored furniture before calling it a regression.

Initial fixture failures retained: classification must be primed before route
search; deactivate the unpositioned actor during this priming so bare crew are
not killed by off-station exposure. Restore alive/present independent-case state
before each case. Safe air refills bare breath15,so measure minimum actually
consumed air and observed recovery,not a lower final breath value. Record per-tick
position/medium/pose/air/water/path/goal/recovery before modifying tests or code.
Warning pause is acknowledged as Continue; real air drain remains active.
Owner2914 non-logfiles unchanged. No production navigation change or promotion.
'''
for name in ['docs/VELD_ANIMATION_CONTINUATION_2026-09-29.md','docs/ASSET_PIPELINE_AND_WORKFLOW.md','docs/BRINESPACE_VISUAL_AESTHETIC_BIBLE.md','skills/brinespace-character-pipeline/references/crew-consistency.md','C:/Users/Alex/.codex/skills/brinespace-character-pipeline/references/crew-consistency.md']:
 f=Path(name) if Path(name).is_absolute() else R/name
 if b'## Veld cardinal low-air escape investigation open' not in f.read_bytes():
  with f.open('ab') as stream:stream.write(lesson.encode('utf-8'))
f=P/'HANDOFF.md';s=f.read_text(encoding='utf-8')
if 'Escape investigation:' not in s:
 s=s.replace('## Next action','Escape investigation:245 checks/5 failures; q0/q2 four physical routes consume air and recover. q1/q3 each9 distress-clear tested points/0 routes in vertical corridor/storage. See escape-investigation.json and per-tick output/veld-distress-escape-v1/journey-checks.json. Cardinal escape remains failed; no promotion. Fixture off-station priming/roster and final-breath assumptions corrected; previous intervals retained.\n\n## Next action')
 s=s.replace('Full continuous-motion and swim/distress joins,then normal-loader selection and actual low-air escape journeys.','Probe vertical doorway graph connections and selected per-edge swim clearance versus authored furniture. Resolve cardinal low-air escape before normal selection; first-interior/arbitrary-phase exit motion remains open.')
 f.write_text(s,encoding='utf-8')
f=R/'docs/CURRENT_STATUS.md';current=f.read_bytes()
if b'## Veld cardinal escape route investigation remains open' not in current:
 f.write_bytes('''## Veld cardinal escape route investigation remains open — September 30, 2026

Joined candidate physical low-air probe:245 checks/5 failures. Four q0/q2
bare/helmet routes cross doorways,consume oxygen and recover; q1/q3 each9
distress-clear tested points/0 routes through authored vertical corridor/storage.
Full cardinal journey gate FAILED; staged family remains unselected. Current
16exact master joins/32authored interiors still pass80package/571renderer and
1007furnished/96disk restores. Per-tick trace retained; owner profile unchanged.
Next inspect vertical graph doorway connections,per-edge selected swim bounds
and authored furniture before any navigation change. First-interior/arbitrary
phase motion and full-set death/rest/life/polish remain; goal active.
[Handoff](../character/veld-swim-distress-family-coherent-v1/HANDOFF.md).

'''.encode('utf-8')+current)
print('Recorded four successful horizontal routes and unresolved five cardinal failures; no promotion')
