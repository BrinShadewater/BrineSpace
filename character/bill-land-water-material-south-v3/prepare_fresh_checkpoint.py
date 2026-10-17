from pathlib import Path
import json,hashlib,re
P=Path(__file__).resolve().parent;R=P.parent.parent;N=P.with_name('bill-land-water-material-north-v3')
def remap(s):
 return s.replace(N.name,P.name).replace('bill-land-water-north-v3','bill-land-water-south-v2').replace('bill-water-exit-north-v1','bill-water-exit-south-v4').replace('bill-land-water-fresh-checkpoint-north-v1','bill-land-water-fresh-checkpoint-south-v1').replace('bill_land_water_fresh_checkpoint_north_v1','bill_land_water_fresh_checkpoint_south_v1').replace('FRESH CHECKPOINT NORTH V1','FRESH CHECKPOINT SOUTH V1').replace('land-swim-north','land-swim-south').replace('swim-land-north','swim-land-south').replace('North','South')
codec=(N/'checkpoint.gd').read_text(encoding='utf-8').replace('north','south');(P/'checkpoint.gd').write_text(codec,encoding='utf-8');(P/'checkpoint.gd.uid').write_text('uid://cbillsouthwetcodec03\n')
main=(R/'scripts/main.gd').read_text(encoding='utf-8');needle='const GridCanvasScript := preload("res://scripts/grid_canvas.gd")';assert main.count(needle)==1
(P/'fresh_fixture_main.gd').write_text(main.replace(needle,f'const GridCanvasScript := preload("res://character/{P.name}/grid.gd")'),encoding='utf-8');(P/'fresh_fixture_main.gd.uid').write_text('uid://cbillsouthwetfreshmain03\n')
(P/'fresh_fixture.tscn').write_text((P/'fixture.tscn').read_text(encoding='utf-8').replace('fixture_main.gd','fresh_fixture_main.gd'),encoding='utf-8')
t=remap((R/'tests/test_bill_land_water_fresh_checkpoint_north_v1.gd').read_text(encoding='utf-8'))
a=t.index('  var pair:Array=[];var best:=0.0');b=t.index('  var shown:Texture2D=',a)
route=(R/'tests/test_bill_land_water_material_south_v3.gd').read_text(encoding='utf-8');c=route.index('  var pair:Array=[];var best:=0.0');d=route.index('  var shown:Texture2D=',c);t=t[:a]+route[c:d]+t[b:]
# Refresh actual portrait strip after restored world membership, then observe readiness.
t=t.replace(' game.selected_card_id="";game.selected_room_cell=CELL;', ' var strip=game.find_child("CrewPortraitPanel",true,false);check(strip!=null,"Actual portrait strip exists")\n var expected_presence:Array=[]\n for id in game.Architects.IDS:\n  if game.Architects.present(game,id):expected_presence.append(id)\n strip.refresh()\n game.selected_card_id="";game.selected_room_cell=CELL;')
t=t.replace('if ready:break','if ready and strip.presence==expected_presence:break')
t=t.replace('check(ready,"Actual Bill actor-slot source submitted and camera centered")','check(ready and strip.presence==expected_presence,"Actual Bill source/camera and restored visible crew roster ready")')
f=R/'tests/test_bill_land_water_fresh_checkpoint_south_v1.gd';f.write_text(t,encoding='utf-8');f.with_suffix('.gd.uid').write_text('uid://cbillsouthwetfreshtest01\n')
s=(R/'tools/run_bill_land_water_material_south_v3_validation.py').read_text(encoding='utf-8').replace('output/bill-land-water-material-south-v3','output/bill-land-water-fresh-checkpoint-south-v1').replace('bill_land_water_material_south_v3.gd','bill_land_water_fresh_checkpoint_south_v1.gd').replace('MATERIAL SOUTH V3','FRESH CHECKPOINT SOUTH V1').replace('helmet-459-candidate-room.png','helmet-432-future-after-candidate-room.png').replace('south-v3/targeted-inputs.json','south-v3/fresh-targeted-inputs.json')
(R/'tools/run_bill_land_water_fresh_checkpoint_south_v1_validation.py').write_text(s,encoding='utf-8')
(P/'build_fresh_checkpoint_review.py').write_text(remap((N/'build_fresh_checkpoint_review.py').read_text(encoding='utf-8')),encoding='utf-8')
files=set(json.loads((P/'targeted-inputs.json').read_text(encoding='utf-8')));pending=[P/'fresh_fixture.tscn',P/'checkpoint.gd',f];seen=set()
while pending:
 file=pending.pop();rel=file.relative_to(R).as_posix()
 if rel in seen:continue
 seen.add(rel);files.add(rel)
 for path in re.findall(r'["\']res://([^"\']+)["\']',file.read_text(encoding='utf-8')):
  if Path(path).suffix in ['.gd','.tscn','.tres','.gdshader'] and (R/path).is_file():pending.append(R/path)
(P/'fresh-targeted-inputs.json').write_text(json.dumps({f:hashlib.sha256((R/f).read_bytes()).hexdigest() for f in sorted(files)},indent=2)+'\n',encoding='utf-8')
print(json.dumps(dict(frozenInputs=len(files),cases=4,entryTick=81,entryPose=4,exitTick=432,exitPose=5,malformedKinds=8,scope='South normal disk save/fresh scene restore plus fixture bridge sidecar; Title Continue remains separate.')))
