from pathlib import Path
from PIL import Image
import json,hashlib,re
P=Path(__file__).resolve().parent;R=P.parent.parent;OLD=P.parent/'bill-land-water-material-north-v3'
entry=P.parent/'bill-land-water-south-v2';exit=P.parent/'bill-water-exit-south-v3'
def remap(s):
 return s.replace(OLD.name,P.name).replace('bill-land-water-north-v3','bill-land-water-south-v2').replace('bill-water-exit-north-v1','bill-water-exit-south-v3').replace('bill_land_water_material_north_v3','bill_land_water_material_south_v2')
grid=remap((OLD/'grid.gd').read_text(encoding='utf-8')).replace('North','South').replace('"north"','"south"').replace('land-swim-north','land-swim-south').replace('swim-land-north','swim-land-south')
e=json.loads((entry/'entry-review.json').read_text());x=json.loads((exit/'exit-review.json').read_text())
crowns=lambda rows:'['+','.join('Vector2(%d,%d)'%tuple(r['crown']) for r in rows)+']'
grid=re.sub(r' var crowns:Array=.*', ' var crowns:Array='+crowns(e['registrations'])+' if enter else '+crowns(x['registrations']),grid)
grid=grid.replace('Vector2(0,-12)','Vector2(0,-4.4)')
(P/'grid.gd').write_text(grid,encoding='utf-8');(P/'view.gd').write_bytes((OLD/'view.gd').read_bytes())
main=(R/'scripts/main.gd').read_text(encoding='utf-8');needle='const GridCanvasScript := preload("res://scripts/grid_canvas.gd")';assert main.count(needle)==1
(P/'fixture_main.gd').write_text(main.replace(needle,f'const GridCanvasScript := preload("res://character/{P.name}/grid.gd")'),encoding='utf-8');(P/'fixture.tscn').write_text(remap((OLD/'fixture.tscn').read_text()),encoding='utf-8')
t=remap((R/'tests/test_bill_land_water_material_north_v3.gd').read_text(encoding='utf-8')).replace('NORTH V3','SOUTH V2').replace('North','South').replace('intermediate South','intermediate North').replace('land-swim-north','land-swim-south').replace('swim-land-north','swim-land-south')
# Mirror only the prescribed direction/route; retain original room graph and collision geometry.
t=t.replace('actor.foot=pair[1];actor.direction="north"','actor.foot=pair[0];actor.direction="south"').replace('[pair[0].lerp(pair[1],.5),pair[1],pair[0],pair[1]]','[pair[0].lerp(pair[1],.5),pair[0],pair[1],pair[0]]').replace('actor.segment_clear(pair[1],pair[0].lerp(pair[1],.5)) and actor.swim_segment_clear(pair[1],pair[0].lerp(pair[1],.5),"north")','actor.segment_clear(pair[0],pair[0].lerp(pair[1],.5)) and actor.swim_segment_clear(pair[0],pair[0].lerp(pair[1],.5),"south")').replace('actor.direction!="north"','actor.direction!="south"').replace('elif kind=="facing":actor.direction="south"','elif kind=="facing":actor.direction="north"')
test=R/'tests/test_bill_land_water_material_south_v2.gd';test.write_text(t,encoding='utf-8')
for f,uid in [(P/'grid.gd','cbillsouthwetgrid02'),(P/'view.gd','cbillsouthwetview02'),(P/'fixture_main.gd','cbillsouthwetmain02'),(test,'cbillsouthwettest02')]:f.with_suffix('.gd.uid').write_text('uid://'+uid+'\n')
runner=remap((R/'tools/run_bill_land_water_material_north_v3_validation.py').read_text()).replace('NORTH V3','SOUTH V2');(R/'tools/run_bill_land_water_material_south_v2_validation.py').write_text(runner,encoding='utf-8')
(P/'build_review.py').write_text(remap((OLD/'build_review.py').read_text()).replace('North','South'),encoding='utf-8')
# Existing maintained selection inventory supplies normal bank paths, refreshed from current pixels.
old_inventory=json.loads((OLD/'source-inventory.json').read_text());inventory={};files=set()
for profiles in old_inventory.values():
 for row in profiles:
  if 'bill-land-water-north-v3/' in row['file'] or 'bill-water-exit-north-v1/' in row['file']:continue
  f=R/row['file']
  if not f.is_file():continue
  im=Image.open(f).convert('RGBA');key=hashlib.sha256(im.tobytes()).hexdigest();inventory.setdefault(key,[]).append(row);files.add(row['file']);files.add(row['manifest'])
for source in [entry,exit]:
 for gear in ['bare','helmet']:
  f=source/gear/'manifest.json';m=json.loads(f.read_text());rel=f.relative_to(R).as_posix();files.add(rel)
  for state in m['states']:
   for i,frame in enumerate(state['frameFiles']):
    ff=f.parent/frame;rr=ff.relative_to(R).as_posix();im=Image.open(ff).convert('RGBA');files.add(rr);inventory.setdefault(hashlib.sha256(im.tobytes()).hexdigest(),[]).append(dict(manifest=rel,file=rr,key=state['id'],index=i,pivot=m['pivot'],standingHeight=m['standingHeight'],size=list(im.size)))
# Refresh current dependency freeze, keeping load-bearing floor/carry fixtures and normal assets.
for rel in json.loads((OLD/'targeted-inputs.json').read_text()):
 if rel.startswith('character/'+OLD.name+'/') or rel=='tests/test_bill_land_water_material_north_v3.gd':continue
 if rel.startswith('character/bill-land-water-north-v3/') or rel.startswith('character/bill-water-exit-north-v1/'):continue
 if (R/rel).is_file():files.add(rel)
pending=[P/'fixture.tscn',P/'view.gd',test];seen=set()
while pending:
 f=pending.pop();rel=f.relative_to(R).as_posix()
 if rel in seen:continue
 seen.add(rel);files.add(rel)
 for resource in re.findall(r'["\']res://([^"\']+)["\']',f.read_text(encoding='utf-8')):
  ff=R/resource
  if ff.is_file() and ff.suffix in ['.gd','.tscn','.tres','.gdshader']:pending.append(ff)
files.add((P/'grid.gd').relative_to(R).as_posix())
(P/'source-inventory.json').write_text(json.dumps(inventory,indent=2)+'\n');(P/'targeted-inputs.json').write_text(json.dumps({f:hashlib.sha256((R/f).read_bytes()).hexdigest() for f in sorted(files)},indent=2)+'\n')
print(json.dumps(dict(frozenInputs=len(files),sourceVariants=len(inventory),scope='South paired entry/exit, actual current normal main/player/controller, fixture-only; no normal admission.')))
