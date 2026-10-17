extends SceneTree
const SAVE=preload("res://scripts/run_save.gd")
const CHECKPOINT=preload("res://scripts/bill_carry_checkpoint.gd")
const ACTOR=preload("res://scripts/bill_carry_npc.gd")
const PLAYER=preload("res://character/bill-carry-cardinal-runtime-v3/stow_player.gd")
const CELL=Vector2i(20,21)
const OUT="res://output/bill-carry-normal-priority-v1/"
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
 check(is_instance_of(game.grid_view.human_water_player,preload("res://scripts/bill_carry_player.gd")),"Selected normal playback")
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
 var actor=ACTOR.new();game.bill_npc=actor;actor.preview_player=game.grid_view.human_water_player;await actor.rebuild(game)
 var stations:Array=actor.RoomActivity.stations(actor.geometry[CELL]);check(not stations.is_empty(),"Actual workshop station exists")
 if stations.is_empty():return
 var station:Dictionary=stations[0];actor.active=true;actor.dead=false;actor.helmet_equipped=helmet;actor.movement_medium="dry";actor.stage="";actor.state="idle";actor.timer=0;actor.goal="curiosity";actor.goal_cell=CELL;actor.direction=station.facing;actor.path.clear()
 actor.foot=(Vector2(CELL)+Vector2.ONE*.5)*384+Vector2(station.point);actor.needs={"hunger":0.0,"fatigue":0.0,"curiosity":60.0,"maintenance":0.0};actor.tank_oxygen=60;actor.breath_oxygen=15;actor.starvation=0
 check(actor.begin_room_activity(),"Actual service dispatch")
 game.grid_view._get_human_frame_source(actor.animation_state(),actor.direction)
 for expected in ["workshop_work","workshop_pickup","workshop_carry"]:
  var duration:float=actor.timer;game.visual_time_seconds+=duration+.001;actor.update(game,duration+.001);check(actor.stage==expected,"Real service progression")
  game.grid_view._get_human_frame_source(actor.animation_state(),actor.direction)
func run():
 check(OS.get_user_data_dir().replace("\\","/").begins_with(OS.get_environment("APPDATA").replace("\\","/")+"/"),"Scratch APPDATA required")
 var game=await fresh();game.paused=false;game.Architects.advance_core(game,10);game.paused=true
 check(not game.occupied.has(CELL),"Vacant fixture preserves site")
 game.selected_rotation=0;game._place_room("salvage_workshop",CELL,true);game.powered_room_cells[CELL]=true
 for event in ["fire","gear","death"]:
  for helmet in [false,true]:
   for phase_name in ["entry","settle","rise"]:
    game.paused=true;game.running=false
    for room in game.placed_rooms:
     if room.pos==CELL:room.fire=0.0
    game.occupied[CELL].fire=0.0
    await prepare(game,helmet);var player=game.grid_view.human_water_player;var actor=game.bill_npc;var ready:=false
    for tick in 1600:
     step(game)
     if phase_name=="entry" and not player.start_motion.is_empty() and player.start_motion.direction=="west" and game.visual_time_seconds-float(player.start_motion.started)>=.1:ready=true
     if phase_name=="settle" and not player.stow_plan.is_empty() and game.visual_time_seconds-float(player.stow_plan.started)>=.4:ready=true
     if phase_name=="rise" and not player.stow_plan.is_empty() and game.visual_time_seconds-float(player.stow_plan.unload_started)>=.55:ready=true
     if ready:break
    check(ready,"Actual natural sequence reaches priority interior")
    if failures:quit(1);return
    var before:Texture2D=game.grid_view._get_human_frame_source(actor.animation_state(),actor.direction)
    if event=="fire":
     for room in game.placed_rooms:
      if room.pos==CELL:room.fire=.5
     game.occupied[CELL].fire=.5;game.running=true;game.paused=false
    elif event=="gear":check(actor.set_helmet_equipped(not helmet),"Public gear setter succeeds")
    else:actor.prepare_death_motion(game);actor.die()
    if event in ["gear","death"]:check(SAVE.problem(SAVE.capture(game)).is_empty(),"Priority snapshot valid before another render")
    var after:Texture2D=step(game)
    check(player.start_motion.is_empty() and player.stow_plan.is_empty(),"Priority cancels pending entry/stow")
    check(after!=null and after.get_image().get_data()!=before.get_image().get_data(),"Priority source replaces prior carry/rise art")
    if event=="fire":check(actor.fire_cells.has(CELL) and actor.goal=="fire-retreat","Actual fire refresh dispatches retreat")
    elif event=="gear":check(actor.helmet_equipped!=helmet,"Public gear change takes effect")
    else:check(actor.dead and actor.animation_state().begins_with("death"),"Mortality source takes precedence")
    var name:String=event+"-"+("helmet" if helmet else "bare")+"-"+phase_name
    for tick in 15:
     step(game);check(player.start_motion.is_empty() and player.stow_plan.is_empty(),"Priority cannot resurrect stale sequence")
    records.append({"name":name,"event":event,"phase":phase_name,"helmetBefore":helmet,"goal":actor.goal,"state":actor.animation_state(),"pathSize":actor.path.size()})
    if event=="fire" and not helmet and phase_name=="settle":
     game.paused=true;await capture(game,"fire-bare-settle",game.grid_view._get_human_frame_source(actor.animation_state(),actor.direction))
    if failures:quit(1);return
 for helmet in [false,true]:
  game.running=false;game.paused=true
  for room in game.placed_rooms:
   if room.pos==CELL:room.fire=0
  game.occupied[CELL].fire=0
  await prepare(game,helmet)
  var player=game.grid_view.human_water_player;var actor=game.bill_npc
  var completed:=false
  for tick in 1800:
   game.visual_time_seconds+=1.0/60;actor.update(game,1.0/60)
   if not player.stow_plan.is_empty() and float(player.stow_plan.until)-game.visual_time_seconds<.04:
    check(SAVE.problem(SAVE.capture(game)).is_empty(),"Terminal unload checkpoint valid before draw")
   if actor.stage!="workshop_carry" and actor.stage!="workshop_unload" and tick>100:
    check(player.stow_plan.is_empty(),"Completion clears expired plan before draw")
    check(SAVE.problem(SAVE.capture(game)).is_empty(),"Completed activity checkpoint valid before draw")
    completed=true;break
   game.grid_view._get_human_frame_source(actor.animation_state(),actor.direction)
  check(completed,"Natural unload returns to ordinary activity")
 var f=FileAccess.open(OUT+"records.json",FileAccess.WRITE);f.store_string(JSON.stringify({"checks":checks,"failures":failures,"records":records,"scope":"18 controlled actual-main priority cases on natural entry/settle/rise: real fire field/refresh dispatch, public gear setter and mortality API. Source cancellation and15future ticks; not successful refuge or full hazard pose review."},"  "))
 print("BILL NORMAL PRIORITY V1: %d checks,%d failures; %d cases"%[checks,failures,records.size()]);quit(1 if failures else 0)
