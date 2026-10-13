"""Assemble private eight-direction transitions and normal q1/q3 fixtures."""
from pathlib import Path
import json,re
ROOT=Path(__file__).resolve().parents[1];B=ROOT/'character/marsh-water-transition-material-v1'
read=lambda p:json.loads(p.read_text())
preferred=['pickup-east-02','pickup-west-03','pickup-north-02','pickup-south-01','drain-east-01','drain-west-01','drain-north-01','drain-south-01']
manifests=[read(B/f'{n}-unselected/manifest.json') for n in preferred]
meta=['frameWidth','frameHeight','pivot','standingHeight','textureFilter']
assert all(all(m[k]==manifests[0][k] for k in meta) for m in manifests)
family={k:manifests[0][k] for k in meta}
family.update(revision='marsh-eight-direction-water-transitions-01-staged',normalAdmission=False,fullGoalComplete=False,states=[s for m in manifests for s in m['states']],sources=preferred)
assert len(family['states'])==8 and sum(len(s['frameFiles']) for s in family['states'])==48
out=B/'cardinal01-cross-review';out.mkdir(exist_ok=True);(out/'family-manifest.json').write_text(json.dumps(family,indent=2)+'\n')
combined=read(B/'combined02-cross-review/manifest-list.json')
combined['manifests']=[n for n in combined['manifests'] if 'marsh-water-transition-material-v1/' not in n]
combined['manifests'].append('character/marsh-water-transition-material-v1/cardinal01-cross-review/family-manifest.json')
out=B/'combined03-cross-review';out.mkdir(exist_ok=True);(out/'manifest-list.json').write_text(json.dumps(combined,indent=2)+'\n')
states={s['id']:s for n in combined['manifests'] for s in read(ROOT/n)['states']}
assert len(states)==48 and sum(len(s['frameFiles']) for s in states.values())==272
base=(ROOT/'tools/review_marsh_water_transition_world01.gd').read_text()
for rev,q,home,target,bounds,card,uid in [('03',1,'21,20','24,21',('20,22','range(21,25)'),'north','uid://db6n4qh8mp2v'),('04',3,'19,20','16,19',('19,21','range(16,20)'),'south','uid://cv8p2nm6qh4r')]:
    s=base.replace('water-transition-world-01',f'water-transition-world-{rev}').replace('WORLD01',f'WORLD{rev}')
    s=s.replace('Vector2i(20,19);var target:=Vector2i(21,16)',f'Vector2i({home});var target:=Vector2i({target})')
    s=s.replace('for y in range(16,20):',f'for y in range({bounds[0]}):').replace('for x in [20,21]:',f'for x in {bounds[1]}:').replace('game.occupied[home].rotation=0',f'game.occupied[home].rotation={q}')
    start=s.index('\tplayer.load_manifest(');end=s.index('\tcheck(game.marsh_npc.get_script()',start)
    s=s[:start]+''.join('\tplayer.load_manifest("res://'+n+'",true)\n' for n in combined['manifests'])+s[end:]
    s=s.replace('key=="swim-carry-west"',f'key=="swim-carry-{card}"').replace('all six West timing slots',f'all six {card} timing slots')
    s=s.replace('actual normal expedition dispatch")','actual normal expedition dispatch; reason="+Trips.reason(game,"marsh",home))')
    s=s.replace('dispatched q0',f'dispatched q{q}').replace('pickupEast02/drainNorth01','all eight private cardinal pickup/drain states').replace('Other pickup/drain directions remain old.','All eight transitions staged; art provisional.').replace('return/West staged loop','return/'+card+' staged loop')
    p=ROOT/f'tools/review_marsh_water_transition_world{rev}.gd';p.write_text(s);p.with_suffix('.gd.uid').write_text(uid+'\n')
    f=(ROOT/'tools/fingerprint_marsh_water_transition_world02.py').read_text().replace('water_transition_world02',f'water_transition_world{rev}').replace(f"'prepare_marsh_water_transition_world{rev}.py'","'prepare_marsh_water_transition_world03.py'")
    (ROOT/f'tools/fingerprint_marsh_water_transition_world{rev}.py').write_text(f)
print('Eight private transition states/48slots/32new drawings; combined48states/272slots. Normal q1/q3 prepared.')
