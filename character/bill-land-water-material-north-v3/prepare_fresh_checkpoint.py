from pathlib import Path
import json,hashlib,re
P=Path(__file__).resolve().parent;R=P.parent.parent;W=P.parent/'bill-land-water-material-west-v3'
codec=(W/'checkpoint.gd').read_text(encoding='utf-8').replace('west','north')
(P/'checkpoint.gd').write_text(codec,encoding='utf-8');(P/'checkpoint.gd.uid').write_text('uid://cbillnorthwetcodec03\n')
main=(R/'scripts/main.gd').read_text(encoding='utf-8');needle='const GridCanvasScript := preload("res://scripts/grid_canvas.gd")';assert main.count(needle)==1
(P/'fresh_fixture_main.gd').write_text(main.replace(needle,'const GridCanvasScript := preload("res://character/bill-land-water-material-north-v3/grid.gd")'),encoding='utf-8');(P/'fresh_fixture_main.gd.uid').write_text('uid://cbillnorthwetfreshmain03\n')
(P/'fresh_fixture.tscn').write_text((P/'fixture.tscn').read_text(encoding='utf-8').replace('fixture_main.gd','fresh_fixture_main.gd'),encoding='utf-8')
t=(R/'tests/test_bill_land_water_fresh_checkpoint_west_v1.gd').read_text(encoding='utf-8').replace('bill-land-water-material-west-v3',P.name).replace('bill-land-water-west-v4','bill-land-water-north-v3').replace('bill-water-exit-west-v1','bill-water-exit-north-v1').replace('bill-land-water-fresh-checkpoint-west-v1','bill-land-water-fresh-checkpoint-north-v1').replace('FRESH CHECKPOINT WEST V1','FRESH CHECKPOINT NORTH V1')
t=t.replace('bank.size()==7,"Current source bank has seven frames"','bank.size()==(9 if enter else 8),"Current North entry9/exit8 bank frames"')
a=t.index('  var pair:Array=[];var best:=0.0');b=t.index('  var shown:Texture2D=',a)
north=(R/'tests/test_bill_land_water_material_north_v3.gd').read_text(encoding='utf-8');c=north.index('  var pair:Array=[];var best:=0.0');d=north.index('  var shown:Texture2D=',c)
t=t[:a]+north[c:d]+t[b:]
t=t.replace('authored West','authored North')
f=R/'tests/test_bill_land_water_fresh_checkpoint_north_v1.gd';f.write_text(t,encoding='utf-8');f.with_suffix('.gd.uid').write_text('uid://cbillnorthwetfreshtest01\n')
runner=(R/'tools/run_bill_land_water_material_north_v3_validation.py').read_text(encoding='utf-8').replace('output/bill-land-water-material-north-v3','output/bill-land-water-fresh-checkpoint-north-v1').replace('bill_land_water_material_north_v3.gd','bill_land_water_fresh_checkpoint_north_v1.gd').replace('MATERIAL NORTH V3','FRESH CHECKPOINT NORTH V1').replace('helmet-459-candidate-room.png','helmet-432-future-after-candidate-room.png').replace('north-v3/targeted-inputs.json','north-v3/fresh-targeted-inputs.json')
(R/'tools/run_bill_land_water_fresh_checkpoint_north_v1_validation.py').write_text(runner,encoding='utf-8')
s=(W/'build_fresh_checkpoint_review.py').read_text(encoding='utf-8').replace('bill-land-water-fresh-checkpoint-west-v1','bill-land-water-fresh-checkpoint-north-v1').replace('Bill West','Bill North').replace("(81,'bill-land-water-west-v4',3),(432,'bill-water-exit-west-v1',4)","(81,'bill-land-water-north-v3',4),(432,'bill-water-exit-north-v1',5)").replace('land-swim-west','land-swim-north').replace('swim-land-west','swim-land-north').replace('authored West','authored North')
(P/'build_fresh_checkpoint_review.py').write_text(s,encoding='utf-8')
files=set(json.loads((P/'targeted-inputs.json').read_text(encoding='utf-8')))
pending=[P/'fresh_fixture.tscn',P/'checkpoint.gd',f];seen=set()
while pending:
 file=pending.pop();rel=file.relative_to(R).as_posix()
 if rel in seen:continue
 seen.add(rel);files.add(rel)
 for path in re.findall(r'["\']res://([^"\']+)["\']',file.read_text(encoding='utf-8')):
  if Path(path).suffix in ['.gd','.tscn','.tres','.gdshader'] and (R/path).is_file():pending.append(R/path)
(P/'fresh-targeted-inputs.json').write_text(json.dumps({f:hashlib.sha256((R/f).read_bytes()).hexdigest() for f in sorted(files)},indent=2)+'\n',encoding='utf-8')
print(json.dumps(dict(frozenInputs=len(files),cases=4,entryTick=81,entryPose=4,exitTick=432,exitPose=5,malformedKinds=8,scope='Normal disk save/fresh scene restore and staged North sidecar, actual current normal actor/player; TitleContinue separate.')))
