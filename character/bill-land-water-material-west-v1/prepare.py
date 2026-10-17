from pathlib import Path
import hashlib,json
P=Path(__file__).resolve().parent;R=P.parent.parent
runtime=(P.parent/'bill-land-water-runtime-east-v1/grid.gd').read_text(encoding='utf-8').replace('"east"','"west"')
start=runtime.index('  var files:Dictionary={')
end=runtime.index('  loader.load_manifest',start)
runtime=runtime[:start]+'''  var files:Dictionary={
   "-enter":"res://character/bill-land-water-west-v2/bare/manifest.json",
   "diving-helmet-enter":"res://character/bill-land-water-west-v2/helmet/manifest.json"}
'''+runtime[end:]
runtime=runtime.replace('"land-swim-east" if enter else "swim-land-east"','"land-swim-west"')
runtime=runtime.replace('var edge:bool=state in ["walk","swim"] and bridge_previous.state in ["walk","swim"] and state!=bridge_previous.state','var edge:bool=state=="swim" and bridge_previous.state=="walk"')
runtime=runtime.replace('## Fixture-only source bridge. Actual actor movement/safety remain authoritative.','## Fixture-only West entry bridge. Exit remains normal source; no reverse-entry substitution.')
# Material values attach to the exact selected source at each draw.
material=(P.parent/'bill-land-water-material-east-v4/grid.gd').read_text(encoding='utf-8')
material=material[material.index('## Per-instance'):material.index('\nfunc bridge_bank')]
material=material.replace('Vector2(171,82),Vector2(177,91),Vector2(180,124),Vector2(183,157),Vector2(187,188)','Vector2(158,80),Vector2(147,114),Vector2(141,118),Vector2(130,150),Vector2(131,188)')
material=material.replace('Vector2(22,-6)','Vector2(-22,-6)').replace('Vector2(8,15)','Vector2(-5,15)')
runtime=runtime.replace('func _get_human_frame_source(state:String,direction:String)->Texture2D:', 'func bridge_source(state:String,direction:String)->Texture2D:')
material=material.replace('super._get_human_frame_source(state,direction)','bridge_source(state,direction)')
(P/'grid.gd').write_text(runtime+'\n'+material,encoding='utf-8');(P/'grid.gd.uid').write_text('uid://cbillwestwetentrygrid01\n')
view=(P.parent/'bill-land-water-material-east-v4/view.gd').read_text(encoding='utf-8')
(P/'view.gd').write_text(view,encoding='utf-8');(P/'view.gd.uid').write_text('uid://cbillwestwetentryview01\n')
main=(R/'scripts/main.gd').read_text(encoding='utf-8');needle='const GridCanvasScript := preload("res://scripts/grid_canvas.gd")';assert main.count(needle)==1
(P/'fixture_main.gd').write_text(main.replace(needle,'const GridCanvasScript := preload("res://character/bill-land-water-material-west-v1/grid.gd")'),encoding='utf-8');(P/'fixture_main.gd.uid').write_text('uid://cbillwestwetentrymain01\n')
(P/'fixture.tscn').write_text((P.parent/'bill-land-water-material-east-v4/fixture.tscn').read_text().replace('material-east-v4','material-west-v1'),encoding='utf-8')
test=(R/'tests/test_bill_land_water_material_east_v4.gd').read_text(encoding='utf-8').replace('bill-land-water-material-east-v4','bill-land-water-material-west-v1').replace('BILL LAND WATER MATERIAL EAST V4:','BILL LAND WATER MATERIAL WEST V1:')
test=test.replace('actor.foot=pair[0];actor.direction="east"','actor.foot=pair[1];actor.direction="west"').replace('PackedVector2Array([pair[1],pair[0],pair[1],pair[0]])','PackedVector2Array([pair[0],pair[1],pair[0],pair[1]])')
test=test.replace('tick in range(60,105) or tick in range(410,460)','tick in range(60,105)')
test=test.replace('size()==2,"Actual entry/exit bridge admission"','size()==1,"Actual West entry-only bridge admission"')
test=test.replace('size()==2,"Both finite bridges complete on exact incoming gait phase"','size()==1,"Finite West entry completes on exact incoming swimming gait phase"')
test=test.replace('elif kind=="facing":actor.direction="west"','elif kind=="facing":actor.direction="east"')
test=test.replace('native boundary capture every60Hz tick','West entry boundary capture every60Hz tick').replace('fixture-selected actor/player/workshop treatment','fixture-selected player/workshop treatment, actual normal Bill actor').replace('dynamic exact outgoing/incoming phases','West entry only, dynamic exact outgoing/incoming phases').replace('No natural job dispatch/hydrology','No authored West exit bridge, native checkpoint/Continue, natural job dispatch/hydrology')
testpath=R/'tests/test_bill_land_water_material_west_v1.gd';testpath.write_text(test,encoding='utf-8');testpath.with_suffix('.gd.uid').write_text('uid://cbillwestwetentrytest01\n')
runner=(R/'tools/run_bill_land_water_material_east_v4_validation.py').read_text(encoding='utf-8').replace('bill-land-water-material-east-v4','bill-land-water-material-west-v1').replace('bill_land_water_material_east_v4','bill_land_water_material_west_v1').replace('BILL LAND WATER MATERIAL EAST V4:','BILL LAND WATER MATERIAL WEST V1:').replace('helmet-459-candidate-room.png','helmet-104-candidate-room.png')
(R/'tools/run_bill_land_water_material_west_v1_validation.py').write_text(runner,encoding='utf-8')
files=['scripts/main.gd','scripts/grid_canvas.gd','scripts/bill_npc.gd','scripts/bill_carry_npc.gd','scripts/bill_carry_player.gd','scripts/crew_sprite_player.gd','character/bill-land-water-material-west-v1/grid.gd','character/bill-land-water-material-west-v1/view.gd','character/bill-land-water-material-west-v1/fixture_main.gd','tests/test_bill_land_water_material_west_v1.gd','character/bill-land-water-west-v2/bare/manifest.json','character/bill-land-water-west-v2/helmet/manifest.json']
for gear in ['bare','helmet']:files.extend(f'character/bill-land-water-west-v2/{gear}/frames/land-swim-west/{i:03}.png' for i in range(7))
(P/'targeted-inputs.json').write_text(json.dumps({f:hashlib.sha256((R/f).read_bytes()).hexdigest() for f in files},indent=2)+'\n',encoding='utf-8')
print('Prepared fixture-only West entry bank, actual normal actor, material/clearance/guards. Exit stays normal; no reversed entry art.')
