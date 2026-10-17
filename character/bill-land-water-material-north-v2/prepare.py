"""Test North waterline continuity without repainting or rescaling source art."""
from pathlib import Path
import hashlib,json
P=Path(__file__).resolve().parent;R=P.parent.parent;OLD=P.parent/'bill-land-water-material-north-v1'
name=P.name
for file in ['grid.gd','fixture.tscn']:
 (P/file).write_text((OLD/file).read_text(encoding='utf-8').replace(OLD.name,name),encoding='utf-8')
main=(R/'scripts/main.gd').read_text(encoding='utf-8');needle='const GridCanvasScript := preload("res://scripts/grid_canvas.gd")';assert main.count(needle)==1
(P/'fixture_main.gd').write_text(main.replace(needle,f'const GridCanvasScript := preload("res://character/{name}/grid.gd")'),encoding='utf-8')
view=(R/'character/bill-land-water-material-east-v2/view.gd').read_text(encoding='utf-8')
view=view.replace('var material_weight:float=-1','var bridge_grid\nvar material_weight:float=-1')
view=view.replace('func draw_actor()->void:\n','''func draw_actor()->void:
 material_weight=-1
 if is_instance_valid(bridge_grid) and external_actor_texture==bridge_grid.material_source:
  material_weight=bridge_grid.material_weight
  material_head_offset=bridge_grid.material_head_offset
''')
oldline=' var line:float=WATER.crew_waterline(actor.y,flood_water,false)+sin(clock*2)*.55'
assert view.count(oldline)==1
view=view.replace(oldline,''' # Both waterline formulas use the same physical actor root. As the pose
 # becomes horizontal, advance the surface split toward the normal swim line.
 var dry_line:float=WATER.crew_waterline(actor.y,flood_water,false)
 var swim_line:float=WATER.crew_waterline(actor.y,flood_water,true)
 var line:float=lerpf(dry_line,swim_line,clampf(material_weight,0,1))+sin(clock*2)*.55''')
(P/'view.gd').write_text(view,encoding='utf-8')
t=(R/'tests/test_bill_land_water_material_north_v1.gd').read_text(encoding='utf-8').replace(OLD.name,name).replace('NORTH V1','NORTH V2')
test=R/'tests/test_bill_land_water_material_north_v2.gd';test.write_text(t,encoding='utf-8')
for f,uid in [(P/'grid.gd','cbillnorthwetgrid02'),(P/'view.gd','cbillnorthwetview02'),(P/'fixture_main.gd','cbillnorthwetmain02'),(test,'cbillnorthwettest02')]:f.with_suffix('.gd.uid').write_text('uid://'+uid+'\n',encoding='utf-8')
runner=(R/'tools/run_bill_land_water_material_north_v1_validation.py').read_text(encoding='utf-8').replace(OLD.name,name).replace('bill_land_water_material_north_v1','bill_land_water_material_north_v2').replace('NORTH V1','NORTH V2')
(R/'tools/run_bill_land_water_material_north_v2_validation.py').write_text(runner,encoding='utf-8')
for file in ['source-inventory.json','build_review.py']:(P/file).write_bytes((OLD/file).read_bytes())
files=json.loads((OLD/'targeted-inputs.json').read_text(encoding='utf-8'))
paths=[f.replace(OLD.name,name).replace('bill_land_water_material_north_v1','bill_land_water_material_north_v2') for f in files]
(P/'targeted-inputs.json').write_text(json.dumps({f:hashlib.sha256((R/f).read_bytes()).hexdigest() for f in paths},indent=2)+'\n',encoding='utf-8')
print(json.dumps(dict(frozenInputs=len(paths),sourceInventoryIdentical=True,artChange=False,change='Standing-to-swimming waterline blend only; actual current main fixture.')))
