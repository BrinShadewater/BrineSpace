extends SceneTree
const SAVE=preload("res://scripts/run_save.gd")
const CHECKPOINT=preload("res://scripts/bill_carry_checkpoint.gd")
const ACTOR=preload("res://scripts/bill_carry_npc.gd")
const PLAYER=preload("res://character/bill-carry-cardinal-runtime-v3/stow_player.gd")
const CELL=Vector2i(20,21)
const OUT="res://output/bill-carry-short-route-audit-v1/"
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
 check(game.grid_view.human_water_player.get_script().resource_path=="res://scripts/bill_carry_player.gd","Selected normal playback")
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
 for rotation in range(4):
  var game=await fresh();game.paused=false;game.Architects.advance_core(game,10);game.paused=true
  game.selected_rotation=rotation;game._place_room("salvage_workshop",CELL,true);game.powered_room_cells[CELL]=true
  # Free fixture placement defaults to zero; exercise the actual rotated resolver.
  game.occupied[CELL].rotation=rotation
  check(int(game.occupied[CELL].rotation)==rotation,"Requested fixture room rotation retained")
  for helmet in [false,true]:
   var player=game.grid_view.human_water_player
   player.clear_carry();player.current_key="";player.last_time=-1;player.motion.clear()
   await prepare(game,helmet)
   check(int(game.bill_npc.geometry[CELL].get("layout",[{}])[0].get("rotation",-1))==rotation,"Actual resolved geometry uses requested rotation")
   var actor=game.bill_npc;var generated:Array=[];var cursor:Vector2=actor.foot;var distance:=0.0
   for point in actor.path:
    generated.append([point.x,point.y]);distance+=cursor.distance_to(point)
    check(actor.segment_clear(cursor,point),"Generated cargo segment collision clear")
    cursor=point
   check(not generated.is_empty(),"Actual workshop generated cargo path")
   var name:String="rot%d-%s"%[rotation,"helmet" if helmet else "bare"]
   var samples:Array=[];var seen:Dictionary={};var completed:=false;var pivot_root:Vector2=actor.foot;var stow_root:Vector2=actor.foot
   var prior_pivot:="";var prior_stow:=-1.0;var travel:=0.0;var start_clock:float=game.visual_time_seconds
   for tick in 1500:
    var before:Vector2=actor.foot;var shown:Texture2D=step(game);travel+=before.distance_to(actor.foot)
    check(shown!=null,"Selected normal source exists")
    if shown==null:break
    var pivot:String=actor.planted_clip if actor.preview_time<actor.planted_until else ""
    if not pivot.is_empty():
     if pivot!=prior_pivot:pivot_root=actor.foot
     check(actor.foot==pivot_root,"Physical foot stays planted through displayed carry turn")
    prior_pivot=pivot
    if not player.stow_plan.is_empty():
     if float(player.stow_plan.started)!=prior_stow:stow_root=actor.foot;prior_stow=float(player.stow_plan.started)
     check(actor.foot==stow_root,"Arrival settlement and unload remain planted")
    check(SAVE.problem(SAVE.capture(game)).is_empty(),"Generated-route actor and playback checkpoint admitted")
    var phase:String="pivot" if not pivot.is_empty() else "entry" if not player.start_motion.is_empty() else "settle" if not player.stow_plan.is_empty() and game.visual_time_seconds<float(player.stow_plan.unload_started) else "unload" if actor.stage=="workshop_unload" else "gait" if actor.stage=="workshop_carry" else "completed"
    var capture_key:String=phase+"-"+actor.direction
    if not seen.has(capture_key):
     seen[capture_key]=true
     await capture(game,name+"-"+capture_key,shown)
     samples.append({"name":name+"-"+capture_key,"time":game.visual_time_seconds-start_clock,"phase":phase,"direction":actor.direction,"foot":[actor.foot.x,actor.foot.y],"state":actor.animation_state(),"key":player.current_key,"entry":player.start_motion.duplicate(true),"stowActive":not player.stow_plan.is_empty()})
    if actor.stage not in ["workshop_carry","workshop_unload"]:
     completed=true;check(player.start_motion.is_empty() and player.stow_plan.is_empty(),"Finished generated route clears programs")
     break
   check(completed,"Actual generated route finishes carry and unload")
   records.append({"name":name,"rotation":rotation,"helmet":helmet,"generatedPath":generated,"pathDistance":distance,"actualTravel":travel,"samples":samples,"completed":completed,"binding":player.carry_binding()})
   print("BILL SHORT ROUTE ",name," distance=",distance," samples=",samples.size()," failures=",failures)
   if failures:quit(1);return
  game.queue_free();await process_frame
 var f=FileAccess.open(OUT+"records.json",FileAccess.WRITE)
 f.store_string(JSON.stringify({"checks":checks,"failures":failures,"records":records,"scope":"Actual workshop-generated cargo paths across four room rotations and both gears, from prescribed service-station dispatch. Normal selected actor/player and unchanged room geometry. Paused world with actor60Hz stepping. Not natural chooser/approach, continuous native film, traffic or full contact certification."},"  "))
 print("BILL SHORT ROUTE AUDIT V1: %d checks,%d failures; %d routes"%[checks,failures,records.size()]);quit(1 if failures else 0)
