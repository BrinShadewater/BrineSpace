extends SceneTree
const OUT="res://output/veld-west-sample-controller-v3/"
const CELL=Vector2i(20,21)
const BASE="res://character/veld-library-closeout-v1/west-standing-family-v1/bare-manifest.json"
const BASEHELM="res://character/veld-library-closeout-v1/west-standing-family-v1/helmet-manifest.json"
const PACK="res://character/veld-library-closeout-v1/west-sample-family-v3/bare-manifest.json"
const HELM="res://character/veld-library-closeout-v1/west-sample-family-v3/helmet-manifest.json"
var checks:=0
var failures:=0
var records:Array=[]
func check(ok:bool,message:String):
 checks+=1
 if not ok:failures+=1;push_error(message)
func _init():call_deferred("run")
func fresh():
 var game=load("res://scenes/main.tscn").instantiate()
 game.set_meta("authored_site_fixture",true)
 game.meta.save_path="user://veld-west-sample-controller.meta";game.run_save_path="user://veld-west-sample-controller.loop";game.Preferences.save_path="user://veld-west-sample-controller.cfg"
 game.meta.unlocked_architect_ids={"bill":true,"veld":true};game.meta.selected_architect="veld"
 root.add_child(game);current_scene=game
 while not game.startup_complete:await process_frame
 game.set_process(false);game.crew_comms.set_process(false);game.crew_comms.minimize();game.tick_timer.stop();game._set_paused(true,false)
 game.grid_view.veld_player.load_manifest(BASE,true);game.grid_view.veld_player.load_equipment_manifest("diving-helmet",BASEHELM)
 game.grid_view.veld_player.load_manifest(PACK,true);check(game.grid_view.veld_player.load_equipment_manifest("diving-helmet",HELM),"Fixture paired candidate")
 return game
func capture(game,name:String,texture:Texture2D):
 game.summary_layer.visible=false;game.selected_card_id="";game.selected_room_cell=CELL
 game._set_grid_zoom(2.0,true,(Vector2(CELL)+Vector2.ONE*.5)/40.0)
 var ready:=false
 for attempt in 90:
  game.grid_scroll.scroll_horizontal=roundi((CELL.x+.5)*game.get_cell_size()-game.grid_scroll.size.x/2)
  game.grid_scroll.scroll_vertical=roundi((CELL.y+.5)*game.get_cell_size()-game.grid_scroll.size.y/2)
  game.grid_view.queue_redraw();await process_frame;await RenderingServer.frame_post_draw
  if game.grid_view.content_canvases.has(CELL):
   for slot in game.grid_view.content_canvases[CELL].slots:
    if slot.visible and slot.item.get("kind","")=="crew" and slot.item.member.texture==texture:ready=true
  if ready:break
 check(ready,"Candidate submitted to actual room canvas")
 check(root.get_texture().get_image().save_png(OUT+name+"-room.png")==OK,"Native room capture")
 texture.get_image().save_png(OUT+name+"-source.png")
func run():
 check(OS.get_environment("APPDATA").contains("veld-west-kneel-motion-scratch"),"Scratch profile required")
 if failures:quit(2);return
 DirAccess.make_dir_recursive_absolute(OUT)
 var game=await fresh();game.paused=false;game.Architects.advance_core(game,10);game.paused=true
 check(not game.occupied.has(CELL) and not game.wrecks.has(CELL),"Vacant fixture cell")
 if failures:quit(1);return
 game.selected_rotation=0;game._place_room("research_lab",CELL,true);game.powered_room_cells[CELL]=true
 await game.veld_npc.rebuild(game)
 var actor=game.veld_npc;var foot:=Vector2.ZERO;var found:=false
 for id in actor.room_nodes.get(CELL,[]):
  var point:Vector2=actor.graph.get_point_position(id)
  var local:Vector2=point-(Vector2(CELL)+Vector2.ONE*.5)*384
  if actor.can_stand(point) and actor.RoomActivity.at(actor.geometry[CELL],local).is_empty() and actor.equipment_facing(CELL,local) in ["","west"]:
   foot=point;found=true;break
 check(found,"Clear West sample fixture point")
 if failures:quit(1);return
 for equipped in [false,true]:
  var gear:String="helmet" if equipped else "bare";var equipment:String="diving-helmet" if equipped else ""
  actor.active=true;actor.dead=false;actor.path.clear();actor.expedition.clear();actor.goal="maintenance";actor.goal_cell=CELL;actor.stage="";actor.state="idle";actor.direction="west";actor.foot=foot;actor.helmet_equipped=equipped;actor.movement_medium="dry";actor.timer=0
  actor.tank_oxygen=60;actor.breath_oxygen=15;actor.starvation=0;actor.needs={"hunger":0.0,"fatigue":0.0,"curiosity":0.0,"maintenance":72.0}
  actor.arrive()
  check(actor.stage=="kneel" and actor.direction=="west" and is_equal_approx(actor.timer,1.0),"Actual maintenance arrival dispatch1s West lower")
  var player=game.grid_view.veld_player;player.current_key="";player.motion.clear();player.last_time=-1
  game.visual_time_seconds=100.0
  var bank:Dictionary=player.frames if not equipped else player.equipment_frames[equipment]
  var seen:Dictionary={"kneel":[],"repair":[],"stand":[]};var samples:Array=[];var stage_times:Dictionary={};var captures:=0;var completed:=false
  for tick in 750:
   var texture:Texture2D=game.grid_view._get_veld_frame_source(game)
   check(actor.foot==foot,"Controller retains world foot")
   check(actor.valid_veld_snapshot(actor.snapshot()),"Actual actor snapshot remains valid")
   var stage:String=actor.stage
   if stage.is_empty():
    check(actor.state=="idle" and actor.needs.maintenance<30.0,"Completed activity returns idle and applies maintenance reward; next goal may already be planned")
    completed=true;await capture(game,gear+"-return-idle",texture);break
   check(stage in ["kneel","repair","stand"] and actor.direction=="west","Actual sequence remains West")
   if not stage_times.has(stage):stage_times[stage]=tick/120.0
   var slot:int=bank[stage+"-west"].find(texture)
   check(slot>=0,"Actual renderer selects candidate family slot")
   if not seen[stage].has(slot):
    seen[stage].append(slot)
    if slot in [0,bank[stage+"-west"].size()/2,bank[stage+"-west"].size()-1]:
     await capture(game,gear+"-"+stage+"-%03d"%slot,texture);captures+=1
   samples.append({"tick":tick,"time":tick/120.0,"stage":stage,"timer":actor.timer,"slot":slot,"foot":actor.foot})
   actor.update(game,1.0/120.0);game.visual_time_seconds+=1.0/120.0
  check(completed,"Complete maintenance cycle")
  for stage in ["kneel","repair","stand"]:check(seen[stage].size()==bank[stage+"-west"].size(),"Advancing controller covers every "+stage+" slot")
  check(absf(float(stage_times.get("repair",-100))-1.0)<.017 and absf(float(stage_times.get("stand",-100))-5.0)<.017,"Actual1s lower/4s examination timing")
  records.append({"gear":gear,"stageTimes":stage_times,"coveredSlots":seen,"captures":captures,"samples":samples,"terminalState":actor.state,"nextGoal":actor.goal,"nextRouteSize":actor.path.size(),"maintenanceAfter":actor.needs.maintenance})
 var f=FileAccess.open(OUT+"records.json",FileAccess.WRITE);f.store_string(JSON.stringify(records,"  "));f.close()
 print("VELD WEST SAMPLE CONTROLLER: %d checks, %d failures;2 actual controller cycles"%[checks,failures]);quit(1 if failures else 0)
