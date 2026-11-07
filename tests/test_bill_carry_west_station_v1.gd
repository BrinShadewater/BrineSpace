extends SceneTree
## Actual workshop renderer and production movement; prescribed clear West floor route, staged gait only.
const CELL=Vector2i(20,21)
const OUT="res://output/bill-carry-west-station-v1/"
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
 var original_actor=game.bill_npc
 for candidate in [false,true]:
  for helmet in [false,true]:
   game.bill_npc=original_actor
   var actor=game.bill_npc;await actor.rebuild(game)
   var stations:Array=actor.RoomActivity.stations(actor.geometry[cell]);check(not stations.is_empty(),"Real workshop contact available")
   if stations.is_empty():continue
   var station:Dictionary=stations[0];actor.active=true;actor.dead=false;actor.helmet_equipped=helmet;actor.movement_medium="dry";actor.stage="";actor.state="idle";actor.timer=0;actor.goal="curiosity";actor.goal_cell=cell
   actor.foot=(Vector2(cell)+Vector2.ONE*.5)*384+Vector2(station.point);actor.direction=station.facing;actor.path.clear();actor.needs={"hunger":25.0,"fatigue":15.0,"curiosity":60.0,"maintenance":35.0}
   var player=load("res://scripts/crew_sprite_player.gd").new()
   for property in ["frames","timing","strides","equipment_frames","equipment_timing","equipment_strides","gait_phase_groups"]:player.set(property,normal.get(property).duplicate(true))
   if candidate:
    player.load_manifest("res://character/bill-carry-west-gait-v1/bare-manifest.json",true)
    check(player.load_equipment_manifest("diving-helmet","res://character/bill-carry-west-gait-v1/helmet-manifest.json"),"Fixture staged admission")
   game.grid_view.human_water_player=player;game.visual_time_seconds=0
   check(actor.can_stand(actor.foot) and actor.begin_room_activity(),"Actual workshop activity begins")
   check(actor.stage=="workshop_inspect","Normal workshop inspect entry")
   for expected in ["workshop_work","workshop_pickup","workshop_carry"]:
    var duration:float=actor.timer;game.visual_time_seconds+=duration+.001;actor.update(game,duration+.001);check(actor.stage==expected,"Original workshop progression to "+expected)
   check(not actor.path.is_empty(),"Production workshop generates carry path")
   var generated_route:=[]
   for point in actor.path:generated_route.append([point.x,point.y])
   # Use real room collision geometry. This long West route is prescribed for
   # contact review; production workshop's short generated route is retained above.
   var longest:=0.0;var begin:=Vector2.ZERO;var finish:=Vector2.ZERO
   for y in range(24,361,8):
    var row_start:=Vector2.ZERO
    for x in range(24,361,8):
     var point:Vector2=Vector2(cell)*384.0+Vector2(x,y)
     if not actor.can_stand(point):row_start=Vector2.ZERO;continue
     if row_start==Vector2.ZERO:row_start=point
     if actor.segment_clear(row_start,point) and point.x-row_start.x>longest:
      longest=point.x-row_start.x;begin=row_start;finish=point
   check(longest>=100.0,"Real workshop has a long clear West contact-review lane")
   if longest<100.0:continue
   actor.foot=finish;actor.direction="west";actor.path=PackedVector2Array([begin]);actor.movement_heading.clear()
   game.grid_view._get_human_frame_source(actor.animation_state(),actor.direction)
   var authored_route:=[]
   for point in actor.path:authored_route.append([point.x,point.y])
   game.selected_card_id="";game.selected_room_cell=cell;game._set_grid_zoom(2.0,true,(Vector2(cell)+Vector2.ONE*.5)/40.0);game._refresh_all();await process_frame
   game.grid_scroll.scroll_horizontal=roundi((cell.x+.5)*game.get_cell_size()-game.grid_scroll.size.x/2);game.grid_scroll.scroll_vertical=roundi((cell.y+.5)*game.get_cell_size()-game.grid_scroll.size.y/2)
   var records:=[];var captured:=[];var previous_clip:="";var onset_foot:=Vector2.ZERO;var onset_time:=-1.0;var turns:=[];var slots:={};var sampled_slots:={};var carrying_samples:=0
   var tag:String=("staged" if candidate else "normal")+("-helmet" if helmet else "-bare")
   for step in range(900):
    var before:Vector2=actor.foot;game.visual_time_seconds+=1.0/60.0;actor.update(game,1.0/60.0)
    check(actor.can_stand(actor.foot) and actor.segment_clear(before,actor.foot),"Real room route remains physically clear")
    var texture:Texture2D=game.grid_view._get_human_frame_source(actor.animation_state(),actor.direction)
    var clip:String=player.motion.get("clip","")
    if not clip.is_empty() and clip!=previous_clip:onset_foot=actor.foot;onset_time=game.visual_time_seconds
    if clip.is_empty() and not previous_clip.is_empty():turns.append({"clip":previous_clip,"travel":onset_foot.distance_to(actor.foot),"elapsed":game.visual_time_seconds-onset_time})
    var gait_row:Array=player.equipment_frames["diving-helmet"]["carry-west"] if helmet else player.frames["carry-west"]
    var slot:int=gait_row.find(texture)
    if actor.stage=="workshop_carry":
     carrying_samples+=1;slots[slot]=true
     check(slot>=0,"Actual grid source belongs to admitted West gait")
     check(actor.direction=="west","Actual path moves West")
     check(actor.foot.distance_to(before)<=.78,"Production movement speed retained")
    records.append({"time":game.visual_time_seconds,"foot":[actor.foot.x,actor.foot.y],"direction":actor.direction,"pose":actor.animation_state(),"stage":actor.stage,"clip":clip,"phase":player.phase,"slot":slot})
    if (slot>=0 and not sampled_slots.has(slot)) or step%45==0 or actor.stage=="workshop_unload":
     sampled_slots[slot]=true
     var filename:String=tag+"-%03d"%step
     await capture(game,filename,texture)
     captured.append({"room":filename+"-room.png","source":filename+"-source.png","foot":[actor.foot.x,actor.foot.y],"slot":slot,"time":game.visual_time_seconds})
    previous_clip=clip
    if actor.stage=="workshop_unload":break
   check(actor.stage=="workshop_unload","Actual carry route completes into unload")
   check(slots.size()==6,"All actual displayed West gait slots reached")
   check(carrying_samples>120,"Several physical carrying cycles recorded")
   journeys.append({"candidate":candidate,"helmet":helmet,"route":authored_route,"generatedRouteBeforeOverride":generated_route,"slots":slots.keys(),"turns":turns,"records":records,"captures":captured})
   actor.active=false
 var report:=FileAccess.open(OUT+"journeys.json",FileAccess.WRITE);report.store_string(JSON.stringify({"scope":"Actual main-scene workshop service progression, collision geometry, production actor movement, normal grid source/native draw. Prescribed long clear West floor route replaces short generated carry route for contact review, original generated path recorded. Staged gait-only player override, both gears; not natural chooser/path eligibility, bridge/turns, interruptions or Continue.","checks":checks,"failures":failures,"journeys":journeys},"  "))
 print("BILL WEST STATION GAIT: %d checks,%d failures"%[checks,failures]);quit(1 if failures else 0)
