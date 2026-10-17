from pathlib import Path
import hashlib,json,re
P=Path(__file__).resolve().parent;R=P.parent.parent;N=P.with_name('bill-land-water-material-north-v3')
def remap(s):
 return s.replace(N.name,P.name).replace('bill-land-water-north-v3','bill-land-water-south-v2').replace('bill-water-exit-north-v1','bill-water-exit-south-v4').replace('bill-land-water-fresh-checkpoint-north-v1','bill-land-water-fresh-checkpoint-south-v1').replace('bill-land-water-title-checkpoint-north-v1','bill-land-water-title-checkpoint-south-v1').replace('bill_land_water_title_checkpoint_north_v1','bill_land_water_title_checkpoint_south_v1').replace('TITLE CHECKPOINT NORTH V1','TITLE CHECKPOINT SOUTH V1').replace('Bill North','Bill South').replace('Current North','Current South').replace('"north"','"south"')
for name in ['title_fixture.gd','title_fixture_main.gd','title_bridge_envelope.gd','seal_title_checkpoints.gd']:
 (P/name).write_text(remap((N/name).read_text(encoding='utf-8')),encoding='utf-8');(P/(name+'.uid')).write_text('uid://cbillsouthtitle'+name.split('.')[0].replace('_','')+'03\n')
title=(R/'scripts/title_screen.gd').read_text(encoding='utf-8');needle='const GAME_SCENE := "res://scenes/main.tscn"';assert title.count(needle)==1
(P/'title_fixture_base.gd').write_text(title.replace(needle,f'const GAME_SCENE := "res://character/{P.name}/title_game.tscn"'),encoding='utf-8')
main=(R/'scripts/main.gd').read_text(encoding='utf-8');needle='const GridCanvasScript := preload("res://scripts/grid_canvas.gd")';assert main.count(needle)==1
(P/'title_fixture_base_main.gd').write_text(main.replace(needle,f'const GridCanvasScript := preload("res://character/{P.name}/grid.gd")'),encoding='utf-8')
for name in ['title_fixture_base','title_fixture_base_main']:(P/(name+'.gd.uid')).write_text('uid://cbillsouth'+name.replace('_','')+'03\n')
(P/'title_game.tscn').write_text((P/'fixture.tscn').read_text(encoding='utf-8').replace('fixture_main.gd','title_fixture_main.gd'),encoding='utf-8')
(P/'title_screen.tscn').write_text((R/'scenes/title_screen.tscn').read_text(encoding='utf-8').replace('res://scripts/title_screen.gd',f'res://character/{P.name}/title_fixture.gd'),encoding='utf-8')
t=remap((R/'tests/test_bill_land_water_title_checkpoint_north_v1.gd').read_text(encoding='utf-8'))
t=t.replace(' game.selected_card_id="";game.selected_room_cell=CELL;', ' var strip=game.find_child("CrewPortraitPanel",true,false);check(strip!=null,"Actual portrait strip exists")\n var expected_presence:Array=[]\n for id in game.Architects.IDS:\n  if game.Architects.present(game,id):expected_presence.append(id)\n strip.refresh()\n game.selected_card_id="";game.selected_room_cell=CELL;')
t=t.replace('if ready:break','if ready and strip.presence==expected_presence:break')
t=t.replace('check(ready,"Actual Bill actor-slot source submitted and camera centered")','check(ready and strip.presence==expected_presence,"Actual Bill source/camera and restored visible crew roster ready")')
f=R/'tests/test_bill_land_water_title_checkpoint_south_v1.gd';f.write_text(t,encoding='utf-8');f.with_suffix('.gd.uid').write_text('uid://cbillsouthtitleprobe03\n')
(R/'tools/run_bill_land_water_title_checkpoint_south_v1_validation.py').write_text(remap((R/'tools/run_bill_land_water_title_checkpoint_north_v1_validation.py').read_text(encoding='utf-8')),encoding='utf-8')
(P/'build_title_checkpoint_review.py').write_text(remap((N/'build_title_checkpoint_review.py').read_text(encoding='utf-8')),encoding='utf-8')
paths=set(json.loads((P/'fresh-targeted-inputs.json').read_text(encoding='utf-8')))
paths.update(['scripts/title_screen.gd','scripts/loading_transition.gd',f.relative_to(R).as_posix(),'tools/run_bill_land_water_title_checkpoint_south_v1_validation.py','output/bill-land-water-fresh-checkpoint-south-v1/records.json'])
for name in ['title_fixture.gd','title_fixture_main.gd','title_fixture_base.gd','title_fixture_base_main.gd','title_bridge_envelope.gd','seal_title_checkpoints.gd','title_screen.tscn','title_game.tscn']:paths.add((P/name).relative_to(R).as_posix())
for file in (P/'fresh-checkpoint-review').iterdir():
 if file.suffix in ['.png','.loop','.bin','.json']:paths.add(file.relative_to(R).as_posix())
pending=[P/'title_screen.tscn',P/'title_game.tscn',f];seen=set()
while pending:
 file=pending.pop();relative=file.relative_to(R).as_posix()
 if relative in seen:continue
 seen.add(relative);paths.add(relative)
 for path in re.findall(r'["\']res://([^"\']+)["\']',file.read_text(encoding='utf-8')):
  if Path(path).suffix in ['.gd','.tscn','.tres','.gdshader'] and (R/path).is_file():pending.append(R/path)
(P/'title-targeted-inputs.json').write_text(json.dumps({f:hashlib.sha256((R/f).read_bytes()).hexdigest() for f in sorted(paths)},indent=2)+'\n',encoding='utf-8')
print(json.dumps(dict(cases=4,frozenInputs=len(paths),scope='South actual TitleContinue in four separate native processes; fixture-only source-bound bridge envelope.')))
