extends SceneTree
## Actual workshop renderer and production movement; prescribed clear East floor route, staged gait only.
const OUT="res://output/bill-carry-east-start-station-v3/"
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
   var player=load("res://character/bill-carry-start-east-v3/carry_start_preview_player.gd").new() if candidate else load("res://scripts/crew_sprite_player.gd").new()
   for property in ["frames","timing","strides","equipment_frames","equipment_timing","equipment_strides","gait_phase_groups"]:player.set(property,normal.get(property).duplicate(true))
   if candidate:
    player.load_manifest("res://character/bill-carry-east-gait-v2/bare-manifest.json",true)
    check(player.load_equipment_manifest("diving-helmet","res://character/bill-carry-east-gait-v2/helmet-manifest.json"),"Fixture staged admission")
   if candidate:
    player.load_manifest("res://character/bill-carry-turn-east-south-motion-v3/bare-manifest.json",true)
    check(player.load_equipment_manifest("diving-helmet","res://character/bill-carry-turn-east-south-motion-v3/helmet-manifest.json"),"Staged quarter-turn admission")
    player.load_manifest("res://character/bill-carry-start-east-v3/bare-manifest.json",true)
    check(player.load_equipment_manifest("diving-helmet","res://character/bill-carry-start-east-v3/helmet-manifest.json"),"Staged paired first-step admission")
    actor.preview_player=player
   game.grid_view.human_water_player=player;game.visual_time_seconds=0
   check(actor.can_stand(actor.foot) and actor.begin_room_activity(),"Actual workshop activity begins")
   check(actor.stage=="workshop_inspect","Normal workshop inspect entry")
   for expected in ["workshop_work","workshop_pickup","workshop_carry"]:
    var duration:float=actor.timer;game.visual_time_seconds+=duration+.001;actor.update(game,duration+.001);check(actor.stage==expected,"Original workshop progression to "+expected)
   check(not actor.path.is_empty(),"Production workshop generates carry path")
   var generated_route:=[]
   for point in actor.path:generated_route.append([point.x,point.y])
   # Use real room collision geometry. This long East route is prescribed for
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
   check(longest>=100.0,"Real workshop has a long clear East contact-review lane")
   if longest<100.0:continue
   actor.foot=begin;actor.direction="south";actor.path=PackedVector2Array([finish]);actor.movement_heading.clear()
   game.grid_view._get_human_frame_source(actor.animation_state(),actor.direction)
   var authored_route:=[]
   for point in actor.path:authored_route.append([point.x,point.y])
   game.selected_card_id="";game.selected_room_cell=cell;game._set_grid_zoom(2.0,true,(Vector2(cell)+Vector2.ONE*.5)/40.0);game._refresh_all();await process_frame
   game.grid_scroll.scroll_horizontal=roundi((cell.x+.5)*game.get_cell_size()-game.grid_scroll.size.x/2);game.grid_scroll.scroll_vertical=roundi((cell.y+.5)*game.get_cell_size()-game.grid_scroll.size.y/2)
   var records:=[];var captured:=[];var previous_clip:="";var onset_foot:=Vector2.ZERO;var onset_time:=-1.0;var turns:=[];var slots:={};var sampled_slots:={};var carrying_samples:=0;var was_starting:=false;var start_seen:=false;var join_seen:=false;var source_ids:={};var keys:={};var wraps:=0;var last_gait_phase:=-1.0;var start_slots:={}
   var tag:String=("staged" if candidate else "normal")+("-helmet" if helmet else "-bare")
   for step in range(900):
    var before:Vector2=actor.foot;game.visual_time_seconds+=1.0/60.0;actor.update(game,1.0/60.0)
    check(actor.can_stand(actor.foot) and actor.segment_clear(before,actor.foot),"Real room route remains physically clear")
    var texture:Texture2D=game.grid_view._get_human_frame_source(actor.animation_state(),actor.direction)
    var clip:String=player.motion.get("clip","")
    if not clip.is_empty() and clip!=previous_clip:onset_foot=actor.foot;onset_time=game.visual_time_seconds
    if clip.is_empty() and not previous_clip.is_empty():turns.append({"clip":previous_clip,"travel":onset_foot.distance_to(actor.foot),"elapsed":game.visual_time_seconds-onset_time})
    var gait_row:Array=player.equipment_frames["diving-helmet"]["carry-east"] if helmet else player.frames["carry-east"]
    var slot:int=gait_row.find(texture)
    var starting:bool=candidate and not player.start_motion.is_empty()
    var turning:bool=not clip.is_empty()
    var source_key:String=str(texture.get_instance_id())
    if not source_ids.has(source_key):
     var sf:String=tag+"-source-%03d.png"%step
     check(texture.get_image().save_png(OUT+sf)==OK,"Exact actual grid source captured")
     source_ids[source_key]=sf
    if was_starting and not starting:
     check(texture==gait_row[0] and is_equal_approx(player.phase,.104),"Actual station bridge exits in exact new gait0/late-contact phase0.104")
     join_seen=true
    if starting:
     start_seen=true;start_slots[player.frames["carry-start-east"].find(texture) if not helmet else player.equipment_frames["diving-helmet"]["carry-start-east"].find(texture)]=true
     check(texture==player.frame_at_elapsed("carry-start-east",game.visual_time_seconds-float(player.start_motion.started),"diving-helmet" if helmet else ""),"Actual station first-step clock")
    was_starting=starting
    if actor.stage=="workshop_carry" and not turning and not starting:
     carrying_samples+=1;slots[slot]=true
     if last_gait_phase>=0:wraps+=maxi(0,floori(player.phase/player.cycle_seconds("carry-east","diving-helmet" if helmet else ""))-floori(last_gait_phase/player.cycle_seconds("carry-east","diving-helmet" if helmet else "")))
     last_gait_phase=player.phase
     check(slot>=0,"Actual grid source belongs to admitted East gait")
     check(actor.direction=="east","Actual path moves East")
     check(actor.foot.distance_to(before)<=.78,"Production movement speed retained")
    records.append({"time":game.visual_time_seconds,"foot":[actor.foot.x,actor.foot.y],"direction":actor.direction,"pose":actor.animation_state(),"stage":actor.stage,"clip":clip,"phase":player.phase,"slot":slot,"turning":turning,"starting":starting,"sourceCapture":source_ids[source_key]})
    if not keys.has(source_key) or step%60==0 or actor.stage=="workshop_unload":
     keys[source_key]=true
     var filename:String=tag+"-%03d.png"%step;game.grid_view.queue_redraw();await process_frame;await RenderingServer.frame_post_draw
     check(root.get_texture().get_image().save_png(OUT+filename)==OK,"Actual workshop native capture")
     check(texture.get_image().save_png(OUT+tag+"-source-%03d.png"%step)==OK,"Actual selected source capture")
     captured.append(filename)
    previous_clip=clip
    if actor.stage=="workshop_unload":break
   check(actor.stage=="workshop_unload","Actual carry route completes into unload")
   check(slots.size()==(8 if candidate else 6),"All actual displayed East gait slots reached")
   if candidate:check(start_seen and join_seen,"Both gears traverse real rendered first-step and exact join")
   check(wraps>=1,"Actual locomotion completes at least one gait cycle")
   if candidate:
    check(start_slots.size()==6,"All6 first-step poses reached at native clock")
    var held:Array=records.filter(func(r):return r.turning)
    check(not held.is_empty(),"Actual planted turn captured")
    if not held.is_empty():
     check(Vector2(held[0].foot[0],held[0].foot[1]).distance_to(Vector2(held[-1].foot[0],held[-1].foot[1]))<.01,"Actual station physical foot held through pivot")
   journeys.append({"candidate":candidate,"helmet":helmet,"route":authored_route,"generatedRouteBeforeOverride":generated_route,"slots":slots.keys(),"completeGaitCycles":wraps,"firstStepSlots":start_slots.keys(),"turns":turns,"records":records,"captures":captured})
   actor.active=false
 var report:=FileAccess.open(OUT+"journeys.json",FileAccess.WRITE);report.store_string(JSON.stringify({"scope":"Actual main-scene workshop service progression, collision geometry, production actor movement, normal grid source/native draw. Prescribed South-facing held start and long clear East floor route replace short generated carry route, original generated path recorded. Candidate authoring movement plants during South/East turn, then bridge-v3 joins gait-v2 at exact contact0 late-phase0.104, both gears. Actual source/render/service progression; not natural chooser/path eligibility, interruptions or Continue.","checks":checks,"failures":failures,"journeys":journeys},"  "))
 print("BILL EAST STATION START JOIN: %d checks,%d failures"%[checks,failures]);quit(1 if failures else 0)
