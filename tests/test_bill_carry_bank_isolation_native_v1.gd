extends SceneTree
const SAVE=preload("res://scripts/run_save.gd")
const CHECKPOINT=preload("res://scripts/bill_carry_checkpoint.gd")
const ACTOR=preload("res://scripts/bill_carry_npc.gd")
const PLAYER=preload("res://character/bill-carry-cardinal-runtime-v3/stow_player.gd")
const CELL=Vector2i(20,21)
const OUT="res://output/bill-carry-bank-isolation-native-v1/"
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
 check(game.bill_npc.get_script().resource_path=="res://scripts/bill_carry_npc.gd","Normal selected Bill actor")
 check(game.grid_view.human_water_player.get_script().resource_path=="res://scripts/bill_carry_player.gd","Normal selected Bill playback")
 return game
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
func step(game):
 game.visual_time_seconds+=1.0/60;game.bill_npc.update(game,1.0/60)
 return game.grid_view._get_human_frame_source(game.bill_npc.animation_state(),game.bill_npc.direction)
func prepare(game,helmet:bool):
 for a in [game.veld_npc,game.branforth_npc,game.marsh_npc]:a.active=false;a.stage="";a.goal="";a.state="idle";a.path.clear();a.expedition.clear()
 var actor=game.bill_npc;await actor.rebuild(game)
 var stations:Array=actor.RoomActivity.stations(actor.geometry[CELL]);check(not stations.is_empty(),"Actual workshop station exists")
 if stations.is_empty():return
 var station:Dictionary=stations[0];actor.active=true;actor.dead=false;actor.helmet_equipped=helmet;actor.movement_medium="dry";actor.stage="";actor.state="idle";actor.timer=0;actor.goal="curiosity";actor.goal_cell=CELL;actor.direction=station.facing;actor.path.clear()
 actor.foot=(Vector2(CELL)+Vector2.ONE*.5)*384+Vector2(station.point);actor.needs={"hunger":0.0,"fatigue":0.0,"curiosity":60.0,"maintenance":0.0};actor.tank_oxygen=60;actor.breath_oxygen=15;actor.starvation=0
 check(actor.begin_room_activity(),"Actual service dispatch")
 game.grid_view._get_human_frame_source(actor.animation_state(),actor.direction)
 for expected in ["workshop_work","workshop_pickup","workshop_carry"]:
  var duration:float=actor.timer;game.visual_time_seconds+=duration+.001;actor.update(game,duration+.001);check(actor.stage==expected,"Real service progression")
  game.grid_view._get_human_frame_source(actor.animation_state(),actor.direction)
func north_lane(game):
 var actor=game.bill_npc;var player=game.grid_view.human_water_player
 player.clear_carry();player.current_key="";player.last_time=-1;player.motion.clear()
 var longest:=0.0;var begin:=Vector2.ZERO;var finish:=Vector2.ZERO
 for x in range(24,361,8):
  var row_start:=Vector2.ZERO
  for y in range(24,361,8):
   var point:Vector2=Vector2(CELL)*384.0+Vector2(x,y)
   if not actor.can_stand(point):row_start=Vector2.ZERO;continue
   if row_start==Vector2.ZERO:row_start=point
   if actor.segment_clear(row_start,point) and point.y-row_start.y>longest:
    longest=point.y-row_start.y;begin=row_start;finish=point
 check(longest>=100.0,"Real workshop has a long clear North contact-review lane")
 if longest<100.0:return
 actor.foot=finish;actor.direction="east";actor.path=PackedVector2Array([begin]);actor.movement_heading.clear()
 game.grid_view._get_human_frame_source(actor.animation_state(),actor.direction)
func run():
 check(OS.get_user_data_dir().replace("\\","/").begins_with(OS.get_environment("APPDATA").replace("\\","/")+"/"),"Scratch APPDATA required")
 var game=await fresh();game.paused=false;game.Architects.advance_core(game,10);game.paused=true
 check(not game.occupied.has(CELL),"Vacant fixture preserves site")
 game.selected_rotation=0;game._place_room("salvage_workshop",CELL,true);game.powered_room_cells[CELL]=true
 for binding in [preload("res://scripts/bill_carry_player.gd").BINDING,preload("res://scripts/bill_carry_player.gd").CURRENT_BINDING]:
  for helmet in [false]:
   for phase_name in ["entry"]:
    game.grid_view.human_water_player.clear_carry();check(game.grid_view.human_water_player.select_binding(binding),"Fixture selects explicit saved source version");await prepare(game,helmet);await north_lane(game);var player=game.grid_view.human_water_player;var actor=game.bill_npc;var ready:=false
    for tick in 1600:
     step(game)
     if phase_name=="entry" and not player.start_motion.is_empty() and player.start_motion.direction=="north" and game.visual_time_seconds-float(player.start_motion.started)>=.1:ready=true
     if phase_name=="settle" and not player.stow_plan.is_empty() and game.visual_time_seconds-float(player.stow_plan.started)>=.4:ready=true
     if phase_name=="rise" and not player.stow_plan.is_empty() and game.visual_time_seconds-float(player.stow_plan.unload_started)>=.55:ready=true
     if ready:break
    check(ready,"Actual natural sequence reaches requested interior phase")
    if failures:quit(1);return
    var source:Texture2D=game.grid_view._get_human_frame_source(actor.animation_state(),actor.direction);var pixels=source.get_image().get_data();var foot:Vector2=actor.foot;var clock:float=game.visual_time_seconds;var name:String=("new" if binding==preload("res://scripts/bill_carry_player.gd").CURRENT_BINDING else "retained")+"-"+("helmet" if helmet else "bare")+"-"+phase_name
    await capture(game,name+"-before",source)
    var data:Dictionary=SAVE.capture(game);check(CHECKPOINT.valid(data) and player.admits_loaded_snapshot(data.crew.playback.bill.water),"Exact actor/source/clock checkpoint admitted")
    var bad:Dictionary=data.duplicate(true)
    if phase_name=="entry":bad.crew.playback.bill.water.carry_start.direction="east"
    else:bad.crew.bill.carry_arrival.until+=.1
    check(not CHECKPOINT.valid(bad),"Reject mismatched actor/display clock or direction")
    check(SAVE.write(game,game.run_save_path)==OK,"Actual scratch disk write")
    var disk:Dictionary=SAVE.read(game.run_save_path);check(CHECKPOINT.valid(disk),"Disk roundtrip preserves exact candidate binding")
    if failures:quit(1);return
    var future:Array=[]
    for tick in 30:
     var shown:Texture2D=step(game);future.append({"foot":actor.foot,"direction":actor.direction,"stage":actor.stage,"timer":actor.timer,"needs":actor.needs.duplicate(),"pixels":shown.get_image().get_data(),"entry":player.start_motion.duplicate(true),"stow":player.stow_plan.duplicate(true)})
    game.queue_free();await process_frame;game=await fresh()
    check(await SAVE.restore_staged(game,disk),"Fresh main scene candidate restore from scratch disk")
    game.set_process(false);game.tick_timer.stop();game.crew_comms.set_process(false);game.crew_comms.minimize();game.run_save_path="user://bill-carry-continue.loop"
    actor=game.bill_npc;player=game.grid_view.human_water_player
    var restored:Texture2D=game.grid_view._get_human_frame_source(actor.animation_state(),actor.direction)
    check(player.carry_binding()==binding and actor.snapshot().carry_binding==binding,"Fresh restore keeps actor and displayed bank bound")
    check(restored.get_image().get_data()==pixels and actor.foot==foot and game.visual_time_seconds==clock,"Fresh source/root/clock exactly preserved")
    await capture(game,name+"-after",restored)
    var needs:Dictionary=actor.needs.duplicate();game._process(.5);check(actor.foot==foot and actor.needs==needs and game.visual_time_seconds==clock,"Paused restore holds clock/root/needs")
    for tick in 30:
     var shown:Texture2D=step(game);var expected:Dictionary=future[tick]
     check(actor.foot==expected.foot and actor.direction==expected.direction and actor.stage==expected.stage and is_equal_approx(actor.timer,expected.timer) and actor.needs==expected.needs,"Physical trajectory/service timer/needs match uninterrupted sequence")
     check(shown.get_image().get_data()==expected.pixels and player.start_motion==expected.entry and player.stow_plan==expected.stow,"Exact restored artwork and motion plans match future")
    records.append({"name":name,"helmet":helmet,"phase":phase_name,"clock":clock,"foot":[foot.x,foot.y],"futureSteps":30,"wrapperOnly":false,"binding":binding});print("BILL CARDINAL CONTINUE ",name," failures=",failures)
    if failures:quit(1);return
 var f=FileAccess.open(OUT+"records.json",FileAccess.WRITE);f.store_string(JSON.stringify({"checks":checks,"failures":failures,"records":records,"scope":"Two focused actual disk/fresh selected-main restores after complete-bank isolation guard: both source versions, bare North first-step. Prior eight-case native interval separately covers both gears and arrival. Real workshop service with prescribed collision-clear North lane. Selected normal loader and RunSave; no source-bank injection. Exact actor/source/clock/needs and30future ticks. Not natural route chooser coverage."},"  "))
 print("BILL BANK ISOLATION NATIVE V1: %d checks,%d failures; %d fresh restores"%[checks,failures,records.size()]);quit(1 if failures else 0)

