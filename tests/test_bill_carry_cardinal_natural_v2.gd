extends SceneTree
## Actual workshop renderer and production movement; prescribed clear North floor route, staged gait only.
const CELL=Vector2i(20,21)
const OUT="res://output/bill-carry-cardinal-natural-v2/"
var game
var checks:=0
var failures:=0
func check(ok:bool,message:String):
 checks+=1
 if not ok:failures+=1;push_error(message)
func _init():call_deferred("run")
func capture(game,name:String,texture:Texture2D):
 game.selected_card_id="";game.selected_room_cell=CELL;game._set_grid_zoom(2.0,true,(Vector2(CELL)+Vector2.ONE*.5)/40.0);game._refresh_all()
 var ready:=false
 for attempt in 90:
  game.grid_scroll.scroll_horizontal=roundi((CELL.x+.5)*game.get_cell_size()-game.grid_scroll.size.x/2);game.grid_scroll.scroll_vertical=roundi((CELL.y+.5)*game.get_cell_size()-game.grid_scroll.size.y/2)
  game.grid_view.queue_redraw();await process_frame;await RenderingServer.frame_post_draw
  var submitted:=false
  if game.grid_view.content_canvases.has(CELL):
   for slot in game.grid_view.content_canvases[CELL].slots:
    if slot.visible and slot.item.get("kind","")=="actor" and game.grid_view.content_canvases[CELL].renderer.external_actor_texture==texture:submitted=true
  var center:Vector2=game.grid_view.get_global_transform()*((Vector2(CELL)+Vector2.ONE*.5)*game.get_cell_size());ready=submitted and center.distance_to(game.grid_scroll.get_global_rect().get_center())<4
  if ready:break
 var cells:Array=game.grid_view.content_canvases.keys()
 cells.sort_custom(func(a:Vector2i,b:Vector2i):return a.y<b.y or (a.y==b.y and a.x<b.x))
 var ordered:=true
 for index in range(1,cells.size()):
  if game.grid_view.content_canvases[cells[index-1]].get_index()>=game.grid_view.content_canvases[cells[index]].get_index():ordered=false
 check(ordered,"Retained neighboring room draw order independent of fresh restore")
 check(ready,"Actual Bill actor-slot source submitted and camera centered")
 check(texture.get_image().save_png(OUT+name+"-source.png")==OK,"Exact source capture")
 check(root.get_texture().get_image().save_png(OUT+name+"-room.png")==OK,"Actual native room capture")
func run():
 check(OS.get_user_data_dir().replace("\\","/").begins_with(OS.get_environment("APPDATA").replace("\\","/")+"/"),"Scratch APPDATA required")
 if failures:quit(2);return
 game=load("res://scenes/main.tscn").instantiate();game.meta.save_path="user://bill-workshop.meta";game.run_save_path="user://bill-workshop.loop";root.add_child(game);current_scene=game
 while not game.startup_complete:await process_frame
 game.set_process(false);game.tick_timer.stop();game._set_paused(true,false);game.crew_comms.set_process(false);game.crew_comms.minimize()
 for actor in [game.bill_npc,game.veld_npc,game.branforth_npc,game.marsh_npc]:actor.active=false
 var cell:=Vector2i(20,21);game.paused=false;game.Architects.advance_core(game,10);game.paused=true;check(not game.occupied.has(cell) and not game.wrecks.has(cell),"Preserve existing core and neighboring site");game.selected_rotation=0;game._place_room("salvage_workshop",cell,true);game.powered_room_cells[cell]=true
 var normal=game.grid_view.human_water_player;var journeys:=[]
 for helmet in [false,true]:
  var actor=load("res://character/bill-carry-cardinal-runtime-v2/stow_actor.gd").new();game.bill_npc=actor;await actor.rebuild(game)
  var stations:Array=actor.RoomActivity.stations(actor.geometry[cell]);check(not stations.is_empty(),"Real workshop station exists")
  if stations.is_empty():continue
  var station:Dictionary=stations[0];actor.active=true;actor.dead=false;actor.helmet_equipped=helmet;actor.movement_medium="dry";actor.stage="";actor.state="idle";actor.timer=0;actor.goal="curiosity";actor.goal_cell=cell
  actor.foot=(Vector2(cell)+Vector2.ONE*.5)*384+Vector2(station.point);actor.direction=station.facing;actor.path.clear();actor.needs={"hunger":25.0,"fatigue":15.0,"curiosity":60.0,"maintenance":35.0}
  var player=load("res://character/bill-carry-cardinal-runtime-v2/stow_player.gd").new()
  for property in ["frames","timing","strides","equipment_frames","equipment_timing","equipment_strides","gait_phase_groups"]:player.set(property,normal.get(property).duplicate(true))
  check(player.load_candidates(),"Latest full cardinal candidate set admitted")
  actor.preview_player=player;game.grid_view.human_water_player=player;game.visual_time_seconds=0
  check(actor.begin_room_activity(),"Actual workshop activity starts")
  game.grid_view._get_human_frame_source(actor.animation_state(),actor.direction)
  for expected in ["workshop_work","workshop_pickup","workshop_carry"]:
   var duration:float=actor.timer;game.visual_time_seconds+=duration+.001;actor.update(game,duration+.001);check(actor.stage==expected,"Real service progression "+expected)
   game.grid_view._get_human_frame_source(actor.animation_state(),actor.direction)
  var original_route:=[]
  for point in actor.path:original_route.append([point.x,point.y])
  check(not original_route.is_empty(),"Production route exists without replacement")
  var records:=[];var captures:=[];var seen:={};var captured_events:={};var stow_rows:={};var unload_seen:=false;var last_texture:Texture2D;var arrival_plan:Dictionary={};var unload_slots:={};var carry_start:float=game.visual_time_seconds;var tag:String="helmet" if helmet else "bare"
  for tick in range(1800):
   var was_unloading:bool=actor.stage=="workshop_unload";var before:Vector2=actor.foot;game.visual_time_seconds+=1.0/60;actor.update(game,1.0/60)
   check(actor.can_stand(actor.foot) and actor.segment_clear(before,actor.foot),"Production route remains collision clear")
   var texture:Texture2D=game.grid_view._get_human_frame_source(actor.animation_state(),actor.direction)
   check(texture!=null,"Actual grid source exists")
   if texture==null:break
   var started:bool=not player.start_motion.is_empty();var clip:String=player.motion.get("clip","")
   if actor.stage=="workshop_unload":
    if not unload_seen:
     check(not player.stow_plan.is_empty(),"Actual natural arrival admits a settling plan")
     check(texture==last_texture,"Actual arrival begins exact last submitted carry texture")
     arrival_plan=player.stow_plan.duplicate(true)
    unload_seen=true;check(not was_unloading or actor.foot.distance_to(before)<.001,"Physical foot planted after actual arrival through stow/unload");check(not started and not clip.begins_with("carry-turn-"),"Arrival does not leak old bridge/turn into unload")
   var unload_rows:Array=player.equipment_frames["diving-helmet"]["unload-north"] if helmet else player.frames["unload-north"]
   if unload_rows.has(texture):unload_slots[unload_rows.find(texture)]=true
   var plan_row:=-1
   if not player.stow_plan.is_empty():
    var cursor:float=game.visual_time_seconds-float(player.stow_plan.started)
    for index in player.stow_plan.rows.size():
     cursor-=float(player.stow_plan.rows[index].seconds)
     if cursor<0:plan_row=index;break
    if plan_row>=0:stow_rows[plan_row]=true
   var key:String=str(texture.get_instance_id());var event_key:String="stow-"+str(plan_row) if plan_row>=0 else key;var source_file:String=""
   if not captured_events.has(event_key):
    source_file=tag+"-%03d"%tick;await capture(game,source_file,texture);seen[key]=source_file+"-source.png";captured_events[event_key]=true
    captures.append({"room":source_file+"-room.png","source":seen[key],"time":game.visual_time_seconds-carry_start,"foot":[actor.foot.x,actor.foot.y],"direction":actor.direction,"stage":actor.stage,"starting":started,"stowRow":plan_row,"clip":clip})
   records.append({"time":game.visual_time_seconds-carry_start,"foot":[actor.foot.x,actor.foot.y],"direction":actor.direction,"stage":actor.stage,"starting":started,"stowRow":plan_row,"startMotion":player.start_motion.duplicate(true),"clip":clip,"phase":player.phase,"source":seen[key],"timer":actor.timer})
   last_texture=texture
   if unload_seen and actor.stage!="workshop_unload":break
  check(unload_seen,"Unmodified generated route reaches original North unload")
  check(stow_rows.size()==arrival_plan.get("rows",[]).size(),"Every actual arrival-plan row submitted and captured")
  check(unload_slots.size()==14,"All improved North unload/rise sources observed")
  check(actor.needs.hunger>25,"Original needs remain active during staged motion")
  journeys.append({"helmet":helmet,"generatedRoute":original_route,"arrivalPlan":arrival_plan,"unloadSlots":unload_slots.keys(),"records":records,"captures":captures,"unloadSeen":unload_seen});actor.active=false
 var f=FileAccess.open(OUT+"journeys.json",FileAccess.WRITE);f.store_string(JSON.stringify({"checks":checks,"failures":failures,"scope":"Actual main/workshop station generates unmodified short carry route; latest cardinal preview actor/player, both gears. No waypoint/heading/arrival override. Actual last submitted carry source settles, turnsNorth, and enters improved fourteen-row rise; original North unload2s retained. Not all cardinal natural routes, lifecycle interruptions or Continue.","journeys":journeys},"  "))
 print("BILL CARDINAL NATURAL STOW: %d checks,%d failures"%[checks,failures]);quit(1 if failures else 0)
