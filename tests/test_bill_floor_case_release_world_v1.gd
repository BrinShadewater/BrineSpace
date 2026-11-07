extends SceneTree
const RELEASE=preload("res://character/bill-floor-case-north-v1/release_state.gd")
const FLOOR=preload("res://character/bill-floor-case-north-v1/floor_state.gd")
const FLOOR_SAVE=preload("res://character/bill-floor-case-north-v1/floor_checkpoint.gd")
const SAVE=preload("res://scripts/run_save.gd")
const CHECKPOINT=preload("res://scripts/bill_carry_checkpoint.gd")
const ACTOR=preload("res://scripts/bill_carry_npc.gd")
const PLAYER=preload("res://character/bill-carry-cardinal-runtime-v3/stow_player.gd")
const CELL=Vector2i(20,21)
const OUT="res://output/bill-floor-case-release-world-v1/"
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
 records.append({"name":name,"foot":[game.bill_npc.foot.x,game.bill_npc.foot.y],"anchor":[view.case_anchor.x,view.case_anchor.y],"caseEnabled":view.case_enabled,"caseOwned":not FLOOR.payload(game.occupied[CELL]).is_empty(),"embedded":view.embedded_case,"sortY":depth,"propRect":[prop_bounds.position.x,prop_bounds.position.y,prop_bounds.size.x,prop_bounds.size.y],"state":game.bill_npc.animation_state(),"direction":game.bill_npc.direction})
func run():
 check(OS.get_user_data_dir().replace("\\","/").begins_with(OS.get_environment("APPDATA").replace("\\","/")+"/"),"Scratch APPDATA required")
 var game=await fresh();game.paused=false;game.Architects.advance_core(game,10);game.paused=true
 game._place_room("salvage_workshop",CELL,true);game.powered_room_cells[CELL]=true
 var view=preload("res://character/bill-floor-case-north-v1/release_workshop.gd").new()
 view.embedded=true;view.hide();game.grid_view.add_child(view);game.grid_view.rare_room_views["salvage_workshop"]=view;view.bind_room(game.occupied[CELL])
 for event in ["service","fire","gear","death"]:
  for helmet in [false,true]:
   for phase_name in ["before","after","late"]:
    game.running=false;game.paused=true
    for room in game.placed_rooms:
     if room.pos==CELL:room.fire=0.0;room.suspended=false;room.erase(FLOOR.FIELD)
    var player=game.grid_view.human_water_player;player.clear_carry();player.current_key="";player.last_time=-1;player.motion.clear();view.embedded_case=false;view.sync_case()
    await prepare(game,helmet)
    var target:float=.32 if phase_name=="before" else .39 if phase_name=="after" else .55
    var shown:Texture2D;var ready:=false
    for tick in 1600:
     shown=step(game)
     if not player.stow_plan.is_empty() and game.visual_time_seconds-float(player.stow_plan.unload_started)>=target:ready=true;break
    check(ready,"Actual generated route reaches reviewed unload source interior")
    if failures:quit(1);return
    var owned:bool=phase_name!="before";var state:Dictionary=FLOOR.payload(game.occupied[CELL]).duplicate(true)
    check(not state.is_empty()==owned,"Case ownership matches actual source release boundary")
    check(not view.case_enabled,"No duplicate separate prop while actor source embeds floor case")
    var name:String=event+"-"+("helmet" if helmet else "bare")+"-"+phase_name
    await record_capture(game,view,name+"-before",shown)
    if event=="service":game.occupied[CELL].suspended=true
    elif event=="fire":game.occupied[CELL].fire=.5;game.running=true;game.paused=false
    elif event=="gear":check(game.bill_npc.set_helmet_equipped(not helmet),"Public gear setter succeeds")
    else:game.bill_npc.prepare_death_motion(game);game.bill_npc.die()
    shown=step(game)
    check(FLOOR.payload(game.occupied[CELL])==state,"Interruption preserves released case and cannot invent pre-release case")
    if event=="fire":check(game.bill_npc.goal=="fire-retreat","Actual fire refresh dispatches retreat")
    if event=="death":check(game.bill_npc.dead,"Actual mortality applied")
    if event in ["service","fire","death"]:check(player.stow_plan.is_empty(),"Priority/service cancels unload plan")
    check(FLOOR_SAVE.problem(SAVE.capture(game)).is_empty(),"Interrupted case/actor/player checkpoint remains valid")
    game.paused=true
    await record_capture(game,view,name+"-after",shown)
    for tick in 15:
     step(game);check(FLOOR.payload(game.occupied[CELL])==state,"Priority cannot resurrect case or move released anchor")
    print("BILL FLOOR RELEASE WORLD ",name," owned=",owned," failures=",failures)
    if failures:quit(1);return
 var f=FileAccess.open(OUT+"records.json",FileAccess.WRITE)
 f.store_string(JSON.stringify({"checks":checks,"failures":failures,"records":records,"scope":"24actual selected-main workshop unload interruptions, both gears, before/after/late inferred release source8. Explicit staged release observer and renderer, unchanged normal actor/player, generated cargo route. Actual service suspension/fire refresh/public gear/mortality.15future floor-state ticks. No successful evacuation, early held-case return, normal selection, full fall/contact or continuous-film acceptance."},"  "))
 print("BILL FLOOR CASE RELEASE WORLD V1: %d checks,%d failures;24cases"%[checks,failures]);quit(1 if failures else 0)
