from pathlib import Path
import hashlib,json
P=Path(__file__).resolve().parent;R=P.parent.parent
main=R/'scripts/main.gd';s=main.read_text();needle='const GridCanvasScript := preload("res://scripts/grid_canvas.gd")';assert s.count(needle)==1
(P/'fixture_main.gd').write_text(s.replace(needle,'const GridCanvasScript := preload("res://character/bill-land-water-runtime-east-v1/grid.gd")'),encoding='utf-8')
scene=(R/'scenes/main.tscn').read_text().replace('uid="uid://brine_main_scene"','').replace('res://scripts/main.gd','res://character/bill-land-water-runtime-east-v1/fixture_main.gd');(P/'fixture.tscn').write_text(scene,encoding='utf-8')
source=(R/'tests/test_bill_floor_case_flood_navigation_v1.gd').read_text()
source=source.replace('bill-floor-case-flood-navigation-v1','bill-land-water-runtime-east-v1').replace('res://scenes/main.tscn','res://character/bill-land-water-runtime-east-v1/fixture.tscn')
source=source.replace('if tick%2==0:','if tick in range(60,105) or tick in range(410,460):').replace('if tick%20==0 or tick in [64,66,68,400,402,404]:','if false:')
source=source.replace('  check(distance>20,','  check(game.grid_view.bridge_events.filter(func(e):return e.kind=="start").size()==2,"Actual entry/exit bridge admission")\n  check(game.grid_view.bridge_events.filter(func(e):return e.kind=="complete" and e.endpointExact).size()==2,"Both finite bridges complete on exact incoming gait phase")\n  records.append({"name":label+"-bridge-events","events":game.grid_view.bridge_events})\n  check(distance>20,')
source=source.replace('"embedded":view.embedded_case,','"embedded":view.embedded_case,"bridgeActive":not game.grid_view.bridge.is_empty(),')
source=source.replace('   if tick in range(60,105) or tick in range(410,460):','   if tick==72:check_same_tick_guards(game)\n   if tick in range(60,105) or tick in range(410,460):')
source+='''
func check_same_tick_guards(game):
 var grid=game.grid_view;var actor=game.bill_npc;var player=grid.human_water_player
 check(not grid.bridge.is_empty(),"Active bridge for same-tick guard probes")
 var actor_fields:Dictionary={}
 for field in ["dead","helmet_equipped","direction","stage"]:actor_fields[field]=actor.get(field)
 var grid_fields:Dictionary={};var player_fields:Dictionary={}
 for field in ["human_animation_key","human_animation_started","human_animation_last_time","human_animation_phase","human_animation_last_position"]:grid_fields[field]=grid.get(field)
 for field in ["current_key","current_equipment","phase","last_time","started","last_position","motion"]:
  var value=player.get(field);player_fields[field]=value.duplicate(true) if value is Dictionary else value
 var plan:Dictionary=grid.bridge.duplicate(true);var previous:Dictionary=grid.bridge_previous.duplicate(true);var events:Array=grid.bridge_events.duplicate(true)
 for kind in ["gear","facing","death","stage"]:
  if kind=="gear":actor.helmet_equipped=not actor.helmet_equipped
  elif kind=="facing":actor.direction="west"
  elif kind=="death":actor.dead=true
  else:actor.stage="fixture-priority-takeover"
  var state:String=actor.animation_state();var shown:Texture2D=grid._get_human_frame_source(state,actor.direction)
  check(grid.bridge.is_empty(),"Same-tick "+kind+" clears staged bridge")
  var normal:Texture2D=grid.bridge_normal_source(state,actor.direction)
  check(shown==normal,"Same-tick "+kind+" returns authoritative normal source")
  for field in actor_fields:actor.set(field,actor_fields[field])
  for field in grid_fields:grid.set(field,grid_fields[field])
  for field in player_fields:player.set(field,player_fields[field].duplicate(true) if player_fields[field] is Dictionary else player_fields[field])
  grid.bridge=plan.duplicate(true);grid.bridge_previous=previous.duplicate(true);grid.bridge_events=events.duplicate(true)
 records.append({"name":("helmet" if actor.helmet_equipped else "bare")+"-same-tick-guards","kinds":["gear","facing","death","stage"],"scope":"Synthetic same-clock guard probes on actual active bridge; not natural priority route/death completion/gear gesture."})
'''
source=source.replace('BILL FLOOR CASE FLOOD NAVIGATION V1:','BILL LAND WATER RUNTIME EAST V1:')
source=source.replace('Initial graph-validated path prescribed; subsequent movement and safety use actual controller.','Fixture-only source bridge advances on visual simulation clock, dynamic exact outgoing/incoming phases, union pose envelope admission/recheck and terminal target gait rebind. Initial graph-validated path prescribed; subsequent movement and safety use actual controller.')
(R/'tests/test_bill_land_water_runtime_east_v1.gd').write_text(source,encoding='utf-8');(R/'tests/test_bill_land_water_runtime_east_v1.gd.uid').write_text('uid://cvblwreast01\n')
runner=(R/'tools/run_bill_floor_case_flood_navigation_v1_validation.py').read_text().replace('bill-floor-case-flood-navigation-v1','bill-land-water-runtime-east-v1').replace('test_bill_floor_case_flood_navigation_v1','test_bill_land_water_runtime_east_v1').replace('BILL FLOOR CASE FLOOD NAVIGATION V1:','BILL LAND WATER RUNTIME EAST V1:').replace('helmet-598-candidate-room.png','helmet-459-candidate-room.png')
(R/'tools/run_bill_land_water_runtime_east_v1_validation.py').write_text(runner,encoding='utf-8')
(P/'fixture-inputs.json').write_text(json.dumps({'originalMainSHA256':hashlib.sha256(main.read_bytes()).hexdigest(),'gridSHA256':hashlib.sha256((R/'scripts/grid_canvas.gd').read_bytes()).hexdigest(),'scope':'Generated main copy differs only in GridCanvasScript preload; isolated fixture, no production changes.'},indent=2)+'\n',encoding='utf-8')
for name,uid in [('grid.gd.uid','uid://crbillwater01'),('fixture_main.gd.uid','uid://cbillwater02')]:
 if not (P/name).exists():(P/name).write_text(uid+'\n',encoding='utf-8')
print('Separate source bridge fixture prepared; actual movement/needs/safety and retained room renderer unchanged.')
