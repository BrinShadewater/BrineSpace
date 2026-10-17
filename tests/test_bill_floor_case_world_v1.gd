extends SceneTree
const SAVE=preload("res://scripts/run_save.gd")
const CHECKPOINT=preload("res://scripts/bill_carry_checkpoint.gd")
const ACTOR=preload("res://scripts/bill_carry_npc.gd")
const PLAYER=preload("res://character/bill-carry-cardinal-runtime-v3/stow_player.gd")
const CELL=Vector2i(20,21)
const OUT="res://output/bill-floor-case-world-v1/"
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
 records.append({"name":name,"foot":[game.bill_npc.foot.x,game.bill_npc.foot.y],"anchor":[view.case_anchor.x,view.case_anchor.y],"caseEnabled":view.case_enabled,"sortY":depth,"propRect":[prop_bounds.position.x,prop_bounds.position.y,prop_bounds.size.x,prop_bounds.size.y],"state":game.bill_npc.animation_state(),"direction":game.bill_npc.direction})
func run():
 check(OS.get_user_data_dir().replace("\\","/").begins_with(OS.get_environment("APPDATA").replace("\\","/")+"/"),"Scratch APPDATA required")
 var game=await fresh();game.paused=false;game.Architects.advance_core(game,10);game.paused=true
 game._place_room("salvage_workshop",CELL,true);game.powered_room_cells[CELL]=true
 var view=preload("res://character/bill-floor-case-north-v1/workshop_preview.gd").new()
 view.embedded=true;view.hide();game.grid_view.add_child(view);game.grid_view.rare_room_views["salvage_workshop"]=view
 check(game.grid_view._bill_room_view(game.occupied[CELL])==view,"Only explicit fixture selects staged workshop prop renderer")
 for helmet in [false,true]:
  view.case_enabled=false
  var player=game.grid_view.human_water_player;player.clear_carry();player.current_key="";player.last_time=-1;player.motion.clear()
  await prepare(game,helmet)
  var actor=game.bill_npc;var reached:=false;var shown:Texture2D
  var name:String="helmet" if helmet else "bare"
  for tick in 1500:
   shown=step(game)
   if not player.stow_plan.is_empty() and game.visual_time_seconds>=float(player.stow_plan.until)-.04:reached=true;break
  check(reached,"Actual generated carry route reaches terminal North unload")
  if failures:quit(1);return
  var anchor_world:Vector2=actor.foot
  view.case_anchor=anchor_world-(Vector2(CELL)+Vector2.ONE*.5)*384
  var fixed_rect:Rect2=view.case_rect()
  await record_capture(game,view,name+"-terminal",shown)
  for tick in 60:
   shown=step(game)
   if actor.stage not in ["workshop_carry","workshop_unload"]:break
  check(actor.stage not in ["workshop_carry","workshop_unload"],"Normal carry/unload completes without candidate controller changes")
  check(actor.foot==anchor_world,"Actual idle begins at the unload foot")
  await record_capture(game,view,name+"-idle-baseline",shown)
  view.case_enabled=true
  await record_capture(game,view,name+"-idle-case",shown)
  var slot=prop_slot(game);var canvas=game.grid_view.content_canvases[CELL]
  var actor_slot=null
  for item in canvas.slots:
   if item.visible and item.item.get("kind","")=="actor":actor_slot=item
  print("CASE DEPTH ",name," anchor=",view.case_anchor," actor=",view.actor," propDepth=",slot.item.sort_y if slot!=null else -999," actorDepth=",actor_slot.item.sort_y if actor_slot!=null else -999," slots=",slot.get_index() if slot!=null else -1,"/",actor_slot.get_index() if actor_slot!=null else -1)
  check(slot!=null and actor_slot!=null and slot.get_index()<actor_slot.get_index(),"Registered floor depth draws case behind stationary Bill boots")
  var seen:Dictionary={};var departed:=false
  for tick in 1800:
   shown=step(game)
   check(view.case_anchor==anchor_world-(Vector2(CELL)+Vector2.ONE*.5)*384 and view.case_rect()==fixed_rect,"Floor anchor cannot follow actor movement")
   var distance:float=actor.foot.distance_to(anchor_world)
   for mark in [8,24,48]:
    if distance>=mark and not seen.has(mark):
     seen[mark]=true;await record_capture(game,view,name+"-depart%d"%mark,shown)
   if distance>=48:departed=true;break
  check(departed,"Normal next activity moves Bill away from fixed floor case")
  print("BILL FLOOR CASE WORLD ",name," departure=",actor.foot.distance_to(anchor_world)," failures=",failures)
  if failures:quit(1);return
 var f=FileAccess.open(OUT+"records.json",FileAccess.WRITE)
 f.store_string(JSON.stringify({"checks":checks,"failures":failures,"records":records,"scope":"Explicit unselected workshop renderer prop; normal Bill actor/player and actual generated carry plus next-activity departure, both gears. Paused world/actor60Hz. Floor anchor/depth/submission and terminal/idle/departure captures; no normal selection, ownership/lifetime/save/Continue, natural chooser approach or continuous film acceptance."},"  "))
 print("BILL FLOOR CASE WORLD V1: %d checks,%d failures; %d captures"%[checks,failures,records.size()]);quit(1 if failures else 0)
