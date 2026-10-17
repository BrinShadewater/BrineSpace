extends "res://tests/playtest_nursery_art.gd"
class KrusherProxy extends "res://scripts/branforth_npc.gd":
 var review_action := false
 var review_elapsed := 0.0
 func animation_state() -> String:
  return "interact" if review_action else ("walk" if state=="walk" else "idle")
 func action_elapsed() -> float:
  return review_elapsed if review_action else -1.0
 func arrive() -> void:
  state="idle"
  path.clear()
var records:Array=[]
var checks:=0
func check(ok:bool,why:String)->void:
 checks+=1
 expect(ok,why)
func run()->void:
 capture_dir="res://character/krusher-station-review-v1/review"
 DirAccess.make_dir_recursive_absolute(capture_dir)
 root.size=Vector2i(1600,900)
 game=MainScene.instantiate()
 game.Preferences.save_path="user://krusher-review-settings.cfg"
 game.meta.save_path="user://krusher-review-meta.json"
 game.run_save_path="user://krusher-review-run.json"
 root.add_child(game)
 current_scene=game
 while not game.startup_complete:await process_frame
 game.set_process(false)
 game.set_process_input(false)
 game.set_process_unhandled_input(false)
 game.set_process_unhandled_key_input(false)
 root.gui_disable_input=true
 game._confirm_doctrines()
 game._set_paused(true)
 game.placed_rooms.clear()
 game.occupied.clear()
 game.powered_room_cells.clear()
 game.unpowered_room_cells.clear()
 var origin:=Vector2i(20,20)
 game._place_room("brine_core",origin,true,true)
 game._place_room("research_lab",origin+Vector2i.RIGHT,true,true)
 game._place_room("storage_bay",origin+Vector2i.LEFT,true,true)
 for cell in game.occupied:game.powered_room_cells[cell]=true
 game.test_walker_cell=Vector2i(-1,-1)
 game.selected_card_id=""
 game.hover_cell=Vector2i(-1,-1)
 game.architect_run["selected"]="bill"
 if game.architect_run.has("core"):game.architect_run.core["recovered"]=true
 game.recovered_crew=[{"architect_id":"bill","alive":true},{"architect_id":"veld","alive":true},{"architect_id":"branforth","alive":true}]
 game.branforth_npc=KrusherProxy.new()
 var player=preload("res://scripts/crew_sprite_player.gd").new()
 player.load_manifest("res://character/krusher-james-canonical-v4/bare-manifest.json")
 check(player.load_equipment_manifest("diving-helmet","res://character/krusher-james-canonical-v4/helmet-manifest.json"),"Paired Krusher equipment admission")
 game.grid_view.branforth_player=player
 game._refresh_all()
 await settle()
 game._fit_station_view()
 await settle()
 var actor=game.branforth_npc
 actor.rebuild(game)
 var nodes:Array=actor.room_nodes.get(origin,[])
 var center:Vector2=(Vector2(origin)+Vector2.ONE*.5)*384.0
 var chosen:=-1
 var distance:=INF
 for id in nodes:
  var point:Vector2=actor.graph.get_point_position(id)
  if actor.can_stand(point) and point.distance_squared_to(center)<distance:
   chosen=id;distance=point.distance_squared_to(center)
 check(chosen>=0,"Clear reachable core floor")
 if chosen<0:quit(1);return
 actor.foot=actor.graph.get_point_position(chosen)
 actor.active=true
 actor.state="idle"
 actor.stage=""
 actor.activity="Krusher station appearance test"
 game.bill_npc.active=false
 game.veld_npc.active=false
 game.marsh_npc.active=false
 for gear in [false,true]:
  actor.helmet_equipped=gear
  for direction in ["south","east","north","west"]:
   actor.direction=direction
   for elapsed in [0.0,1.4,2.75,5.5]:
    actor.review_action=true
    actor.review_elapsed=elapsed
    var texture:Texture2D=game.grid_view._get_branforth_frame_source(game)
    check(texture==player.frame_at_elapsed("interact-"+direction,elapsed,"diving-helmet" if gear else ""),"Actual grid source uses Krusher pose")
    check(texture.get_meta("crew_pivot")==Vector2(92,172),"Canonical foot pivot")
    var name:="%s-%s-%04d"%["helmet" if gear else "bare",direction,roundi(elapsed*1000)]
    await capture(name)
    room_pixels(origin).save_png(capture_dir.path_join(name+"-room.png"))
    records.append({"file":name+"-room.png","viewport":name+".png","gear":gear,"direction":direction,"elapsed":elapsed,"foot":[actor.foot.x,actor.foot.y]})
 actor.review_action=false
 actor.helmet_equipped=false
 var route:=PackedVector2Array()
 var target:=-1
 for id in nodes:
  var candidate:PackedVector2Array=actor.route_between(chosen,id)
  if candidate.size()>1 and actor.graph.get_point_position(id).distance_to(actor.foot)>80:
   route=candidate;target=id;break
 check(target>=0,"Production navigation supplies a clear walk route")
 var steps:=0
 if target>=0:
  actor.path=route
  actor.goal=""
  var starting:Vector2=actor.foot
  while not actor.path.is_empty() and steps<600:
   actor.move(1.0/30.0)
   game.visual_time_seconds+=1.0/30.0
   check(actor.can_stand(actor.foot),"Walk stays on clear floor")
   if steps%6==0:
    await capture("walk-%03d"%steps)
    room_pixels(origin).save_png(capture_dir.path_join("walk-%03d-room.png"%steps))
   steps+=1
  check(actor.path.is_empty(),"Production walk reaches target")
  check(actor.foot.distance_to(starting)>80,"Actual movement, not an in-place gait")
 var out:=FileAccess.open("res://character/krusher-station-review-v1/review/report.json",FileAccess.WRITE)
 out.store_string(JSON.stringify({"checks":checks,"failures":failures,"records":records,"walkSteps":steps,"scope":"Fixture-only Krusher appearance in existing Branforth slot, actual main scene/core renderer and production route/move; prescribed action clocks, no Krusher roster or autonomous behavior integration"},"\t"))
 print("KRUSHER_STATION checks=%d failures=%d poses=%d walk_steps=%d"%[checks,failures,records.size(),steps])
 game.free()
 quit(1 if failures else 0)
