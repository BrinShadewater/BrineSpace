extends SceneTree
## Real workshop service and generated carry route, fixture-only staged art override.
const OUT="res://output/bill-workshop-carry-journey/"
var game
var checks:=0
var failures:=0
func check(ok:bool,message:String):
 checks+=1
 if not ok:failures+=1;push_error(message)
func _init():call_deferred("run")
func run():
 check(OS.get_user_data_dir().replace("\\","/").begins_with(OS.get_environment("APPDATA").replace("\\","/")+"/"),"Scratch APPDATA required")
 if failures:quit(2);return
 game=load("res://scenes/main.tscn").instantiate();game.meta.save_path="user://bill-workshop.meta";game.run_save_path="user://bill-workshop.loop";root.add_child(game);current_scene=game
 while not game.startup_complete:await process_frame
 game.set_process(false);game.tick_timer.stop();game._set_paused(true,false);game.crew_comms.set_process(false);game.crew_comms.minimize()
 for actor in [game.bill_npc,game.veld_npc,game.branforth_npc,game.marsh_npc]:actor.active=false
 var cell:=Vector2i(20,20);game.occupied.clear();game.placed_rooms.clear();game.selected_rotation=0;game._place_room("salvage_workshop",cell,true);game.powered_room_cells[cell]=true
 var normal=game.grid_view.human_water_player;var journeys:=[]
 var original_actor=game.bill_npc
 for candidate in [false,true]:
  for helmet in [false,true]:
   game.bill_npc=load("res://character/bill-carry-turn-east-south-motion-v3/carry_motion_preview.gd").new() if candidate else original_actor
   var actor=game.bill_npc;await actor.rebuild(game)
   var stations:Array=actor.RoomActivity.stations(actor.geometry[cell]);check(not stations.is_empty(),"Real workshop contact available")
   if stations.is_empty():continue
   var station:Dictionary=stations[0];actor.active=true;actor.dead=false;actor.helmet_equipped=helmet;actor.movement_medium="dry";actor.stage="";actor.state="idle";actor.timer=0;actor.goal="curiosity";actor.goal_cell=cell
   actor.foot=(Vector2(cell)+Vector2.ONE*.5)*384+Vector2(station.point);actor.direction=station.facing;actor.path.clear();actor.needs={"hunger":25.0,"fatigue":15.0,"curiosity":60.0,"maintenance":35.0}
   var player=load("res://scripts/crew_sprite_player.gd").new()
   for property in ["frames","timing","strides","equipment_frames","equipment_timing","equipment_strides","gait_phase_groups"]:player.set(property,normal.get(property).duplicate(true))
   if candidate:
    player.load_manifest("res://character/bill-carry-turn-east-south-motion-v3/bare-manifest.json",true)
    check(player.load_equipment_manifest("diving-helmet","res://character/bill-carry-turn-east-south-motion-v3/helmet-manifest.json"),"Fixture staged admission")
   game.grid_view.human_water_player=player;game.visual_time_seconds=0
   if candidate:actor.preview_player=player
   check(actor.can_stand(actor.foot) and actor.begin_room_activity(),"Actual workshop activity begins")
   check(actor.stage=="workshop_inspect","Normal workshop inspect entry")
   for expected in ["workshop_work","workshop_pickup","workshop_carry"]:
    var duration:float=actor.timer;game.visual_time_seconds+=duration+.001;actor.update(game,duration+.001);check(actor.stage==expected,"Original workshop progression to "+expected)
   check(not actor.path.is_empty(),"Production workshop generates carry path")
   game.grid_view._get_human_frame_source(actor.animation_state(),actor.direction)
   var authored_route:=[]
   for point in actor.path:authored_route.append([point.x,point.y])
   game.selected_card_id="";game.selected_room_cell=cell;game._set_grid_zoom(2.0,true,(Vector2(cell)+Vector2.ONE*.5)/40.0);game._refresh_all();await process_frame
   game.grid_scroll.scroll_horizontal=roundi((cell.x+.5)*game.get_cell_size()-game.grid_scroll.size.x/2);game.grid_scroll.scroll_vertical=roundi((cell.y+.5)*game.get_cell_size()-game.grid_scroll.size.y/2)
   var records:=[];var captured:=[];var previous_clip:="";var onset_foot:=Vector2.ZERO;var onset_time:=-1.0;var turns:=[]
   var tag:String=("staged" if candidate else "normal")+("-helmet" if helmet else "-bare")
   for step in range(900):
    var before:Vector2=actor.foot;game.visual_time_seconds+=1.0/60.0;actor.update(game,1.0/60.0)
    check(actor.can_stand(actor.foot) and actor.segment_clear(before,actor.foot),"Real room route remains physically clear")
    var texture:Texture2D=game.grid_view._get_human_frame_source(actor.animation_state(),actor.direction)
    var clip:String=player.motion.get("clip","")
    if not clip.is_empty() and clip!=previous_clip:onset_foot=actor.foot;onset_time=game.visual_time_seconds
    if clip.is_empty() and not previous_clip.is_empty():turns.append({"clip":previous_clip,"travel":onset_foot.distance_to(actor.foot),"elapsed":game.visual_time_seconds-onset_time})
    records.append({"time":game.visual_time_seconds,"foot":[actor.foot.x,actor.foot.y],"direction":actor.direction,"pose":actor.animation_state(),"stage":actor.stage,"clip":clip,"phase":player.phase})
    if step%60==0 or clip!=previous_clip or actor.stage=="workshop_unload":
     var filename:String=tag+"-%03d.png"%step;game.grid_view.queue_redraw();await process_frame;await RenderingServer.frame_post_draw
     check(root.get_texture().get_image().save_png(OUT+filename)==OK,"Actual workshop native capture")
     check(texture.get_image().save_png(OUT+tag+"-source-%03d.png"%step)==OK,"Actual selected source capture")
     captured.append(filename)
    previous_clip=clip
    if actor.stage=="workshop_unload":break
   check(actor.stage=="workshop_unload","Actual carry route completes into unload")
   check(not turns.is_empty(),"Initial opposite carry heading captured in every comparison")
   var held_records:Array=records.filter(func(record):return not str(record.clip).is_empty())
   check(not held_records.is_empty(),"Displayed turn interval recorded")
   if not held_records.is_empty():
    var first:Vector2=Vector2(held_records[0].foot[0],held_records[0].foot[1]);var last:Vector2=Vector2(held_records[-1].foot[0],held_records[-1].foot[1])
    check(first.distance_to(last)<.01 if candidate else first.distance_to(last)>70,"Physical foot during displayed turn: planted prototype versus retained baseline")
   # Completion includes the first resumed movement step; it is outside the held interval.
   for turn in turns:check(turn.travel<1.0 if candidate else turn.travel>70,"First resumed step bounded separately from planted interval")
   journeys.append({"candidate":candidate,"helmet":helmet,"route":authored_route,"turns":turns,"records":records,"captures":captured})
   actor.active=false
 var report:=FileAccess.open(OUT+"journeys.json",FileAccess.WRITE);report.store_string(JSON.stringify({"scope":"Actual main-scene default workshop contact/service progression/generated route/normal grid source/native draw. Staged comparison injects authoring-only Bill movement subclass with planted interval; normal comparison retains production actor. Fixture placed/powered room and prescribed service entry; no natural chooser/approach or Continue/checkpoint compatibility.","checks":checks,"failures":failures,"journeys":journeys},"  "))
 print("BILL WORKSHOP CARRY JOURNEY: %d checks,%d failures"%[checks,failures]);quit(1 if failures else 0)
