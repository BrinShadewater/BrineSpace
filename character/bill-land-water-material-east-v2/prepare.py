from pathlib import Path
P=Path(__file__).resolve().parent;R=P.parent.parent
s=(P.parent/'bill-land-water-runtime-east-v1/prepare.py').read_text().replace('bill-land-water-runtime-east-v1','bill-land-water-material-east-v2').replace('test_bill_land_water_runtime_east_v1','test_bill_land_water_material_east_v2').replace('run_bill_land_water_runtime_east_v1','run_bill_land_water_material_east_v2').replace('BILL LAND WATER RUNTIME EAST V1:','BILL LAND WATER MATERIAL EAST V2:')
s=s.replace('uid://crbillwater01','uid://cvmatereast01').replace('uid://cbillwater02','uid://cwmatereast02').replace('uid://cvblwreast01','uid://ctmatereast03')
s=s.replace("(R/'tests/test_bill_land_water_material_east_v2.gd').write_text(source,encoding='utf-8')",'''source=source.replace('res://character/bill-floor-case-north-v1/flood_readability_v2.gd','res://character/bill-land-water-material-east-v2/view.gd')
source=source.replace(' return shown',' view.material_weight=game.grid_view.material_weight;view.material_head_offset=game.grid_view.material_head_offset\\n return shown',1)
source=source.replace('"bridgeActive":not game.grid_view.bridge.is_empty(),','"bridgeActive":not game.grid_view.bridge.is_empty(),"materialWeight":game.grid_view.material_weight,"materialHeadOffset":[game.grid_view.material_head_offset.x,game.grid_view.material_head_offset.y],')
source=source.replace('   if tick==72:check_same_tick_guards(game)','   check(game.grid_view.material_weight>=0 and game.grid_view.material_weight<=1 if not game.grid_view.bridge.is_empty() else game.grid_view.material_weight==-1,"Material follows finite bridge only")\\n   if tick==72:check_same_tick_guards(game)')
(R/'tests/test_bill_land_water_material_east_v2.gd').write_text(source,encoding='utf-8')''')
exec(compile(s,str(P/'prepare.py'),'exec'),{'__file__':str(P/'prepare.py')})
