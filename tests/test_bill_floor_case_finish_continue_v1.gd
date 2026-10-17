extends SceneTree
const RELEASE=preload("res://character/bill-floor-case-north-v1/release_state.gd")
const FLOOR=preload("res://character/bill-floor-case-north-v1/floor_state.gd")
const FLOOR_SAVE=preload("res://character/bill-floor-case-north-v1/finish_checkpoint.gd")
const SAVE=preload("res://scripts/run_save.gd")
const CHECKPOINT=preload("res://scripts/bill_carry_checkpoint.gd")
const ACTOR=preload("res://character/bill-floor-case-north-v1/finish_actor.gd")
const PLAYER=preload("res://character/bill-carry-cardinal-runtime-v3/stow_player.gd")
const CELL=Vector2i(20,21)
const OUT="res://output/bill-floor-case-finish-continue-v1/"
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
 var shown:Texture2D=game.grid_view._get_human_frame_source(game.bill_npc.animation_state(),game.bill_npc.direction)
 RELEASE.observe_source(game,shown)
 game.bill_npc.observe_finish(game,shown)
 var view=game.grid_view.rare_room_views["salvage_workshop"]
 view.bind_frame(shown,game.grid_view.human_water_player,"diving-helmet" if game.bill_npc.helmet_equipped else "",game.bill_npc.foot-(Vector2(CELL)+Vector2.ONE*.5)*384)
 return shown
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
func prop_slot(game):
 if not game.grid_view.content_canvases.has(CELL):return null
 for slot in game.grid_view.content_canvases[CELL].slots:
  if slot.visible and slot.item.get("prop",{}).get("id","")=="bill-floor-case-study":return slot
 return null
func record_capture(game,view,name:String,texture:Texture2D):
 await capture(game,name,texture)
 var slot=prop_slot(game)
 check(slot!=null if view.case_enabled else slot==null,"Floor-prop submission matches fixture state")
 var depth:=0.0;var prop_bounds:=Rect2()
 if slot!=null:
  depth=slot.item.sort_y;prop_bounds=slot.item.prop.rect
  check(prop_bounds==view.case_rect(),"Submitted case remains at fixed registered floor anchor")
 records.append({"name":name,"foot":[game.bill_npc.foot.x,game.bill_npc.foot.y],"anchor":[view.case_anchor.x,view.case_anchor.y],"caseEnabled":view.case_enabled,"caseOwned":not FLOOR.payload(game.occupied[CELL]).is_empty(),"embedded":view.embedded_case,"finishActive":not game.grid_view.human_water_player.finish_exit.is_empty(),"sortY":depth,"propRect":[prop_bounds.position.x,prop_bounds.position.y,prop_bounds.size.x,prop_bounds.size.y],"state":game.bill_npc.animation_state(),"direction":game.bill_npc.direction})
func install_view(game):
 if game.grid_view.human_water_player.get_script().resource_path!="res://character/bill-floor-case-north-v1/finish_player.gd":game.grid_view.human_water_player=FLOOR_SAVE.detached_player(game.grid_view.human_water_player)
 var view=preload("res://character/bill-floor-case-north-v1/release_workshop.gd").new()
 view.embedded=true;view.hide();game.grid_view.add_child(view);game.grid_view.rare_room_views["salvage_workshop"]=view
 view.bind_room(game.occupied[CELL]);return view
func run():
 check(OS.get_user_data_dir().replace("\\","/").begins_with(OS.get_environment("APPDATA").replace("\\","/")+"/"),"Scratch APPDATA required")
 var game=await fresh();game.paused=false;game.Architects.advance_core(game,10);game.paused=true
 game._place_room("salvage_workshop",CELL,true);game.powered_room_cells[CELL]=true
 for helmet in [false,true]:
  for phase_name in ["early","pre-release","released"]:
   game.occupied[CELL].erase(FLOOR.FIELD);game.occupied[CELL].suspended=false;game.powered_room_cells[CELL]=true
   var view=install_view(game)
   var player=game.grid_view.human_water_player;player.finish_exit.clear();player.clear_carry();player.current_key="";player.last_time=-1;player.motion.clear()
   await prepare(game,helmet)
   var shown:Texture2D;var reached:=false;var anchor_world:=Vector2.ZERO
   for tick in 1700:
    shown=step(game)
    var data:Dictionary=FLOOR.payload(game.occupied[CELL])
    if not player.stow_plan.is_empty() and game.visual_time_seconds-float(player.stow_plan.unload_started)>=(.10 if phase_name=="early" else .32 if phase_name=="pre-release" else .39):
     check(not data.is_empty() if phase_name=="released" else data.is_empty(),"Source-bound ownership matches saved release side");reached=true;break
   check(reached,"Actual generated route reaches saved phase")
   if failures:quit(1);return
   game.occupied[CELL].suspended=true;shown=step(game)
   check(not player.finish_exit.is_empty(),"Actual service loss begins saved finite exit")
   var name:String=("helmet" if helmet else "bare")+"-"+phase_name
   await record_capture(game,view,name+"-before",shown)
   var pixels:PackedByteArray=shown.get_image().get_data();var foot:Vector2=game.bill_npc.foot;var clock:float=game.visual_time_seconds
   var state:Dictionary=FLOOR.payload(game.occupied[CELL]).duplicate(true)
   var checkpoint:Dictionary=SAVE.capture(game)
   check(FLOOR_SAVE.problem(checkpoint).is_empty(),"Candidate floor and ordinary actor/player checkpoint valid")
   for fault in ["actor_pair","player_pair","binding","clock","gear","row","seconds","room","foot","floor"]:
    var bad:Dictionary=checkpoint.duplicate(true)
    if fault=="actor_pair":bad.crew.bill.finish_exit={}
    elif fault=="player_pair":bad.crew.playback.bill.water.finish_exit={}
    elif fault=="binding":bad.crew.bill.finish_binding="unsupported"
    elif fault=="clock":bad.state.visual_time_seconds=bad.crew.playback.bill.water.finish_exit.until
    elif fault=="gear":bad.crew.bill.helmet_equipped=not helmet
    elif fault=="row":bad.crew.playback.bill.water.finish_exit.rows[0].index=99
    elif fault=="seconds":bad.crew.playback.bill.water.finish_exit.rows[0].seconds+=.01
    elif fault=="room":bad.crew.bill.finish_exit.cell=Vector2i(1,1)
    elif fault=="foot":bad.crew.bill.finish_exit.foot+=Vector2(1,0)
    else:
     for room in bad.state.placed_rooms:
      if room.pos==CELL:room[FLOOR.FIELD]={"version":1,"source":FLOOR.SOURCE,"anchor":Vector2(NAN,0)}
    check(not await FLOOR_SAVE.restore_staged(game,bad),"Reject malformed paired exit before scene mutation")
    var unchanged:Dictionary=SAVE.capture(game)
    check(unchanged.state==checkpoint.state and unchanged.crew==checkpoint.crew,"Bad finite exit restore is atomic")
   var pool:Dictionary=player.rows_for("diving-helmet" if helmet else "")
   var original:Texture2D=pool["unload-north"][9];pool["unload-north"][9]=pool["unload-north"][8]
   check(not await FLOOR_SAVE.restore_staged(game,checkpoint),"Altered prospective source bank rejected detached")
   pool["unload-north"][9]=original
   var still:Dictionary=SAVE.capture(game)
   check(still.state==checkpoint.state and still.crew==checkpoint.crew,"Source rejection leaves live actor/player/room state unchanged")
   game.running=true
   check(FLOOR_SAVE.write(game,game.run_save_path)==OK,"Actual scratch disk write through staged guard")
   var disk:Dictionary=FLOOR_SAVE.read(game.run_save_path);check(not disk.is_empty(),"Actual disk read preserves candidate room metadata")
   var future:Array=[]
   for tick in 40:
    var texture:Texture2D=step(game)
    future.append({"source":texture.get_image().get_data(),"actor":game.bill_npc.snapshot(),"player":player.snapshot(),"case":FLOOR.payload(game.occupied[CELL]).duplicate(true)})
   game.queue_free();await process_frame;game=await fresh()
   check(await FLOOR_SAVE.restore_staged(game,disk),"Fresh ordinary main restore with detached floor admission")
   game.set_process(false);game.tick_timer.stop();game.crew_comms.set_process(false);game.crew_comms.minimize();game.run_save_path="user://bill-floor-case-continue.loop"
   view=install_view(game);player=game.grid_view.human_water_player
   var restored:Texture2D=game.grid_view._get_human_frame_source(game.bill_npc.animation_state(),game.bill_npc.direction)
   check(restored.get_image().get_data()==pixels and game.bill_npc.foot==foot and game.visual_time_seconds==clock,"Immediate restored source/root/clock exact")
   check(FLOOR.payload(game.occupied[CELL])==state,"Immediate floor presence/anchor/source version exact")
   view.bind_frame(restored,player,"diving-helmet" if game.bill_npc.helmet_equipped else "",game.bill_npc.foot-(Vector2(CELL)+Vector2.ONE*.5)*384)
   await record_capture(game,view,name+"-after",restored)
   var needs:Dictionary=game.bill_npc.needs.duplicate();game._process(.5)
   check(game.bill_npc.foot==foot and game.bill_npc.needs==needs and game.visual_time_seconds==clock and FLOOR.payload(game.occupied[CELL])==state,"Paused restored floor and actor remain fixed")
   for tick in 40:
    var texture:Texture2D=step(game);var expected:Dictionary=future[tick]
    check(texture.get_image().get_data()==expected.source and game.bill_npc.snapshot()==expected.actor and player.snapshot()==expected.player,"Restored actor/source/plans follow exact future")
    check(FLOOR.payload(game.occupied[CELL])==expected.case,"Restored floor state follows exact completion/persistence future")
   check(not FLOOR.payload(game.occupied[CELL]).is_empty(),"Pre-release Continue creates case at cue; released Continue retains case")
   print("BILL FLOOR CASE FINISH CONTINUE ",name," failures=",failures)
   if failures:quit(1);return
 var f=FileAccess.open(OUT+"records.json",FileAccess.WRITE)
 f.store_string(JSON.stringify({"checks":checks,"failures":failures,"records":records,"scope":"Six actual disk/fresh ordinary-main restores during staged ordinary service-loss exit: both gears early, pre-release and released. Bound full actor/player/source/clock/floor admission and atomic malformed/prospective-source rejection. Normal actor/player; exact immediate/future40ticks and pause, malformed floor atomic rejection. Not normal selection, natural chooser approach, all room rotations or full motion acceptance."},"  "))
 print("BILL FLOOR CASE FINISH CONTINUE V1: %d checks,%d failures;6fresh restores"%[checks,failures]);quit(1 if failures else 0)
