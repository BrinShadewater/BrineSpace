extends SceneTree
const SAVE=preload("res://scripts/run_save.gd")
const CHECKPOINT=preload("res://character/bill-carry-continuation-v1/checkpoint.gd")
const ACTOR=preload("res://character/bill-carry-return-east-v2/return_actor.gd")
const PLAYER=preload("res://character/bill-carry-return-east-v2/return_player.gd")
const CELL=Vector2i(20,21)
const OUT="res://output/bill-carry-return-east-v2/"
var checks:=0
var failures:=0
var records:=[]
func check(ok:bool,message:String):
 checks+=1
 if not ok:failures+=1;push_error(message)
func _init():call_deferred("run")
func fresh():
 var game=load("res://scenes/main.tscn").instantiate();game.meta.save_path="user://bill-carry-continue.meta";game.run_save_path="user://bill-carry-continue.loop";root.add_child(game);current_scene=game
 while not game.startup_complete:await process_frame
 game.set_process(false);game.tick_timer.stop();game._set_paused(true,false);game.crew_comms.set_process(false);game.crew_comms.minimize()
 var normal=game.grid_view.human_water_player;var player=PLAYER.new()
 for property in ["frames","timing","strides","equipment_frames","equipment_timing","equipment_strides","gait_phase_groups"]:player.set(property,normal.get(property).duplicate(true))
 player.load_manifest("res://character/bill-carry-turn-east-south-motion-v3/bare-manifest.json",true)
 check(player.load_equipment_manifest("diving-helmet","res://character/bill-carry-turn-east-south-motion-v3/helmet-manifest.json"),"Candidate paired turn")
 player.load_manifest("res://character/bill-carry-east-gait-v2/bare-manifest.json",true)
 check(player.load_equipment_manifest("diving-helmet","res://character/bill-carry-east-gait-v2/helmet-manifest.json"),"Candidate paired gait")
 player.load_manifest("res://character/bill-carry-start-east-v3/bare-manifest.json",true)
 check(player.load_equipment_manifest("diving-helmet","res://character/bill-carry-start-east-v3/helmet-manifest.json"),"Candidate paired first step")
 game.grid_view.human_water_player=player;return game
func step(game):
 game.visual_time_seconds+=1.0/60.0;game.bill_npc.update(game,1.0/60.0)
 return game.grid_view._get_human_frame_source(game.bill_npc.animation_state(),game.bill_npc.direction)
func prepare(game,helmet:bool):
 for a in [game.veld_npc,game.branforth_npc,game.marsh_npc]:a.active=false;a.stage="";a.goal="";a.state="idle";a.path.clear();a.expedition.clear()
 var actor=ACTOR.new();game.bill_npc=actor;actor.preview_player=game.grid_view.human_water_player;await actor.rebuild(game)
 var stations:Array=actor.RoomActivity.stations(actor.geometry[CELL]);check(not stations.is_empty(),"Workshop service exists")
 if stations.is_empty():return
 var station:Dictionary=stations[0];actor.active=true;actor.dead=false;actor.helmet_equipped=helmet;actor.movement_medium="dry";actor.stage="";actor.state="idle";actor.timer=0;actor.goal="curiosity";actor.goal_cell=CELL;actor.path.clear()
 actor.foot=(Vector2(CELL)+Vector2.ONE*.5)*384+Vector2(station.point);actor.needs={"hunger":0.0,"fatigue":0.0,"curiosity":60.0,"maintenance":0.0};actor.tank_oxygen=60;actor.breath_oxygen=15;actor.starvation=0
 check(actor.begin_room_activity(),"Actual workshop activity dispatch")
 for expected in ["workshop_work","workshop_pickup","workshop_carry"]:
  var duration:float=actor.timer;game.visual_time_seconds+=duration+.001;actor.update(game,duration+.001);check(actor.stage==expected,"Actual workshop progression to "+expected)
 var longest:=0.0;var begin:=Vector2.ZERO;var finish:=Vector2.ZERO
 for y in range(24,361,8):
  var row_start:=Vector2.ZERO
  for x in range(24,361,8):
   var point:Vector2=Vector2(CELL)*384+Vector2(x,y)
   if not actor.can_stand(point):row_start=Vector2.ZERO;continue
   if row_start==Vector2.ZERO:row_start=point
   if actor.segment_clear(row_start,point) and point.x-row_start.x>longest:longest=point.x-row_start.x;begin=row_start;finish=point
 check(longest>=100,"Real room clear East route")
 actor.foot=begin;actor.direction="south";actor.path=PackedVector2Array([finish]);actor.movement_heading.clear();actor.planted_until=-1;actor.planted_clip=""
 game.visual_time_seconds=100;actor.preview_time=100
 var player=game.grid_view.human_water_player;player.current_key="";player.current_equipment="";player.last_time=-1;player.motion.clear();player.start_motion.clear();player.phase=0
 game.grid_view._get_human_frame_source("carry","south")
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
 var game=await fresh();game.paused=false;game.Architects.advance_core(game,10);game.paused=true
 check(not game.occupied.has(CELL) and not game.wrecks.has(CELL),"Fixture preserves actual neighboring site")
 game.selected_rotation=0;game._place_room("salvage_workshop",CELL,true);game.powered_room_cells[CELL]=true
 for helmet in [false,true]:
  for sample in [.3,.95,1.65]:
   game.occupied[CELL].suspended=false
   await prepare(game,helmet)
   if failures:quit(1);return
   for tick in 200:
    step(game)
    if game.visual_time_seconds-100>=sample:break
   var actor=game.bill_npc;var player=game.grid_view.human_water_player
   var before:Texture2D=game.grid_view._get_human_frame_source(actor.animation_state(),actor.direction)
   var name=("helmet" if helmet else "bare")+"-"+str(sample)
   check(actor.stage=="workshop_carry" and actor.service_available(game,CELL),"Real carry service available before interruption")
   await capture(game,name+"-before",before)
   var foot:Vector2=actor.foot
   # Real service predicate changes; no direct actor stage/path/cancel mutation.
   game.occupied[CELL].suspended=true
   check(not actor.service_available(game,CELL),"Actual room suspension disables workshop service")
   var after:Texture2D=step(game)
   check(actor.stage!="workshop_carry","Normal controller interrupts carry on service loss")
   check(actor.foot==foot,"Service loss cannot advance through planted pivot")
   check(actor.planted_clip.is_empty() and actor.planted_until<0 and player.start_motion.is_empty() and player.motion.get("state","")!="carry","Candidate drops stale pivot/first-step/motion metadata")
   check(not CHECKPOINT.valid_candidate(SAVE.capture(game)),"Old checkpoint wrapper rejects unsupported return binding")
   check(not player.return_plan.is_empty() and after.get_image().get_data()==before.get_image().get_data(),"Return entry preserves exact displayed whole source")
   await capture(game,name+"-after",after)
   var interrupted_stage:String=actor.stage;var interrupted_state:String=actor.animation_state();var end:float=player.return_plan.until;var exit_started:float=player.return_plan.started;var seen:Dictionary={};var sampled:Array=[];var timeline:Array=[{"slot":-1,"elapsed":0.0}]
   for tick in 240:
    var hunger_before:float=actor.needs.hunger
    var pose:Texture2D=step(game)
    check(actor.needs.hunger>hunger_before,"Normal needs advance while return holds only movement")
    check(actor.stage!="workshop_carry" and player.start_motion.is_empty() and actor.planted_clip.is_empty(),"Suspended service cannot revive stale carry")
    if game.visual_time_seconds<end:
     check(actor.foot==foot,"Physical foot remains planted throughout finite return")
     for row in player.return_plan.rows:
      if player.rows_for(player.return_plan.gear)[row.key][row.index]==pose:
       var tag:String=row.key+"/"+str(row.index)
       if not seen.has(tag):
        var slot:int=sampled.size();seen[tag]=slot;pose.get_image().save_png(OUT+name+"-return-"+str(slot)+".png");sampled.append({"slot":slot,"key":row.key,"index":row.index,"clock":game.visual_time_seconds})
       timeline.append({"slot":seen[tag],"elapsed":game.visual_time_seconds-exit_started})
       break
    else:
     check(player.return_plan.is_empty(),"Finite return completes without stale clocks")
     await capture(game,name+"-end",pose)
     break
   records.append({"name":name,"sample":sample,"helmet":helmet,"foot":[foot.x,foot.y],"afterStage":interrupted_stage,"afterState":interrupted_state,"returnSeconds":end-(100+sample),"sources":sampled,"timeline":timeline,"duration":end-exit_started})
   print("BILL SERVICE LOSS ",name," failures=",failures)
   if failures:quit(1);return
 var file=FileAccess.open(OUT+"records.json",FileAccess.WRITE);file.store_string(JSON.stringify({"scope":"Actual main/workshop dispatch, prescribed graph-clear East route, actual room service suspension during turn/first-step/gait, normal inherited interruption/chooser then staged finite planted return; needs/hazard/restore integration remains open. Staged candidate only; no natural suspension or standard title Continue claim.","checks":checks,"failures":failures,"records":records},"  "))
 print("BILL CARRY RETURN EAST V2: %d checks,%d failures; %d cases"%[checks,failures,records.size()]);quit(1 if failures else 0)
