"""Bind furnished-route evidence to the exact candidates and clearance fixture."""
from pathlib import Path
import hashlib,json
H=Path(__file__).resolve().parent
R=H.parents[1]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
paths=[R/'tools/review_veld_cargo_turn_routes_v1.gd',H/'check_routes.py',H/'measure_clearance.py',H/'validate_clearance.py',H/'candidate-clearance-v1.json',H/'candidate-clearance-profile-v1.json',H/'candidate-clearance-checks-v1.json',R/'character/dr-veld-v2/clearance.json',R/'scripts/grid_canvas.gd',R/'scripts/bill_npc.gd',R/'scripts/crew_life.gd',R/'scripts/crew_sprite_player.gd']
reports={}
for suffix,name,count,cases in [('native-routes-v1','route-checks.json',2403,24),('native-narrow-v1','narrow-guard-checks.json',50,1)]:
    wrapper=H/(suffix+'-checks.json');log=H/(suffix+'.log');report=H/'route-review-v1'/name
    w=json.loads(wrapper.read_text());v=json.loads(report.read_text())
    assert w['exit_code']==0 and not w['engine_errors'] and not w['real_profile_changed_files']
    assert v['checks']==count and v['failures']==0 and len(v['results'])==cases
    assert all(x['started'] and x['arrived'] for x in v['results'])
    if cases==24:
        assert all(x['completed'] and not x['cancelledSafely'] for x in v['results'])
    else:
        assert all(x['cancelledSafely'] and not x['completed'] for x in v['results'])
    reports[name]=v
    paths.extend([wrapper,log,report])
    paths.extend(R/x['capture'].removeprefix('res://') for x in v['results'] if x['capture'])
measurement=json.loads((H/'candidate-clearance-v1.json').read_text());frames={}
for row in measurement['records']:
    for f in row['frames']:
        assert sha(R/f['file'])==f['sha256'];frames[f['file']]=f['sha256']
for family in ['veld-swim-carry-matrix-coherent-v1','veld-salvage-pickup-family-coherent-v1',H.name]:
    paths.extend(R/'character'/family/(gear+'-manifest.json') for gear in ['bare','helmet'])
out=dict(installed=False,routeChecks=2403,routeCases=24,narrowChecks=50,narrowCases=1,frameReferences=336,hashes={p.relative_to(R).as_posix():sha(p) for p in paths},frameHashes=frames,visuallyReviewed=['swim-carry-turn-east-west-bare.png','swim-carry-turn-north-south-helmet.png'],scope='Forced flooded Veld on five authored furnished rooms; actual graph/smoothing/movement/frame selection with candidate profiles. One geometry-selected safe early cancellation. Not full expedition/exterior/natural flooding/traffic/save or owner acceptance.')
(H/'route-evidence-v1.json').write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
print('2403 furnished route checks /24 cases and50 narrow safety checks bound to336refs; runtime unchanged.')
