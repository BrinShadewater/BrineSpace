from pathlib import Path
import hashlib,json
P=Path(__file__).resolve().parent;R=P.parent.parent
grid=(P.parent/'bill-land-water-material-east-v2/grid.gd').read_text(encoding='utf-8')
grid=grid.replace('var material_weight:float=-1','var material_source:Texture2D\nvar material_weight:float=-1').replace(' var shown:Texture2D=super._get_human_frame_source(state,direction)',' var shown:Texture2D=super._get_human_frame_source(state,direction)\n material_source=shown')
grid=grid.replace('[Vector2(171,88),Vector2(177,118),Vector2(183,157),Vector2(187,188)]','[Vector2(171,82),Vector2(177,91),Vector2(180,124),Vector2(183,157),Vector2(187,188)]')
grid+='''
func bridge_bank(gear:String,enter:bool)->Array:
 if not enter:return super.bridge_bank(gear,enter)
 var id:String=gear+"-enter"
 if not bridge_banks.has(id):
  var files:Dictionary={"":"res://character/bill-land-water-east-v5/bare/manifest.json","diving-helmet":"res://character/bill-land-water-east-v5/helmet/manifest.json"}
  var loader=preload("res://scripts/crew_sprite_player.gd").new();loader.load_manifest(files[gear],true)
  bridge_banks[id]=[loader.frames["land-swim-east"],loader.timing["land-swim-east"].durations]
 return bridge_banks[id]
'''
(P/'grid.gd').write_text(grid,encoding='utf-8');(P/'grid.gd.uid').write_text('uid://cbillwetliftgrid01\n')
(P/'view.gd').write_text((P.parent/'bill-land-water-material-east-v3/view.gd').read_text(encoding='utf-8'),encoding='utf-8');(P/'view.gd.uid').write_text('uid://cbillwetliftview01\n')
main=(R/'scripts/main.gd').read_text(encoding='utf-8');needle='const GridCanvasScript := preload("res://scripts/grid_canvas.gd")';assert main.count(needle)==1
(P/'fixture_main.gd').write_text(main.replace(needle,'const GridCanvasScript := preload("res://character/bill-land-water-material-east-v4/grid.gd")'),encoding='utf-8');(P/'fixture_main.gd.uid').write_text('uid://cbillwetliftmain01\n')
(P/'fixture.tscn').write_text((P.parent/'bill-land-water-material-east-v3/fixture.tscn').read_text().replace('material-east-v3','material-east-v4'),encoding='utf-8')
s=(R/'tests/test_bill_land_water_material_east_v3.gd').read_text(encoding='utf-8').replace('bill-land-water-material-east-v3','bill-land-water-material-east-v4').replace('BILL LAND WATER MATERIAL EAST V3:','BILL LAND WATER MATERIAL EAST V4:')
(R/'tests/test_bill_land_water_material_east_v4.gd').write_text(s,encoding='utf-8');(R/'tests/test_bill_land_water_material_east_v4.gd.uid').write_text('uid://cbillwetlifttest01\n')
s=(R/'tools/run_bill_land_water_material_east_v3_validation.py').read_text(encoding='utf-8').replace('bill-land-water-material-east-v3','bill-land-water-material-east-v4').replace('bill_land_water_material_east_v3','bill_land_water_material_east_v4').replace('BILL LAND WATER MATERIAL EAST V3:','BILL LAND WATER MATERIAL EAST V4:')
(R/'tools/run_bill_land_water_material_east_v4_validation.py').write_text(s,encoding='utf-8')
s=(P.parent/'bill-land-water-runtime-east-v1/build_review.py').read_text(encoding='utf-8').replace('bill-land-water-runtime-east-v1','bill-land-water-material-east-v4')
s=s.replace("rows=[x for x in data['records'] if x['name'].endswith('-candidate')]","rows=[x for x in data['records'] if x['name'].endswith('-candidate') and 'tick' in x]")
s=s.replace("'bill-land-water-east-v3','bill-land-water-helmet-east-v1'","'bill-land-water-east-v5/bare','bill-land-water-east-v5/helmet'")
(P/'build_review.py').write_text(s,encoding='utf-8')
files=['scripts/main.gd','scripts/run_save.gd','scripts/grid_canvas.gd','scripts/bill_carry_npc.gd','scripts/bill_carry_player.gd','scripts/crew_sprite_player.gd','character/bill-land-water-runtime-east-v1/grid.gd','character/bill-land-water-material-east-v4/grid.gd','character/bill-land-water-material-east-v4/view.gd','character/bill-land-water-material-east-v4/fixture_main.gd','tests/test_bill_land_water_material_east_v4.gd','character/bill-land-water-east-v5/bare/manifest.json','character/bill-land-water-east-v5/helmet/manifest.json']
(P/'targeted-inputs.json').write_text(json.dumps({f:hashlib.sha256((R/f).read_bytes()).hexdigest() for f in files},indent=2)+'\n',encoding='utf-8')
print('Prepared new lift bank/native material registration; original exit bank retained.')
