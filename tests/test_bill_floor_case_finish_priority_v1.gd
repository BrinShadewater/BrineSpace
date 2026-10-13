extends SceneTree
const RELEASE=preload("res://character/bill-floor-case-north-v1/release_state.gd")
const FLOOR=preload("res://character/bill-floor-case-north-v1/floor_state.gd")
const FLOOR_SAVE=preload("res://character/bill-floor-case-north-v1/floor_checkpoint.gd")
const SAVE=preload("res://scripts/run_save.gd")
const CHECKPOINT=preload("res://scripts/bill_carry_checkpoint.gd")
const ACTOR=preload("res://character/bill-floor-case-north-v1/finish_actor.gd")
const PLAYER=preload("res://character/bill-carry-cardinal-runtime-v3/stow_player.gd")
const CELL=Vector2i(20,21)
const OUT="res://output/bill-floor-case-finish-priority-v1/"
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
 game.visual_time_seconds+=1.0/60
 if game.bill_npc.active and not game.bill_npc.dead:preload("res://scripts/room_flooding.gd").step_crew(game,game.bill_npc,"bill",1.0/60)
 game.bill_npc.update(game,1.0/60)
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
func new_fixture():
 var game=await fresh();game.paused=false;game.Architects.advance_core(game,10);game.paused=true
 game._place_room("salvage_workshop",CELL,true);game.powered_room_cells[CELL]=true
 var old=game.grid_view.human_water_player;var player=preload("res://character/bill-floor-case-north-v1/finish_player.gd").new()
 for field in ["frames","timing","strides","equipment_frames","equipment_timing","equipment_strides","carry_banks","active_binding"]:player.set(field,old.get(field))
 game.grid_view.human_water_player=player
 var view=preload("res://character/bill-floor-case-north-v1/release_workshop.gd").new()
 view.embedded=true;view.hide();game.grid_view.add_child(view);game.grid_view.rare_room_views["salvage_workshop"]=view
 return [game,player,view]
func run():
 check(OS.get_user_data_dir().replace("\\","/").begins_with(OS.get_environment("APPDATA").replace("\\","/")+"/"),"Scratch APPDATA required")
 var fixture:Array=await new_fixture();var game=fixture[0];var player=fixture[1];var view=fixture[2]
 for event in ["fire","flood","gear","death","removal"]:
  for helmet in [false,true]:
   for target in [.10,.39]:
    if event=="removal":
     game.queue_free();await process_frame;fixture=await new_fixture();game=fixture[0];player=fixture[1];view=fixture[2]
    game.running=false;game.paused=true
    if not game.occupied.has(CELL):game._place_room("salvage_workshop",CELL,true)
    var room:Dictionary=game.occupied[CELL];room.suspended=false;room.fire=0.0;room.water_level=0.0;room.erase(FLOOR.FIELD);game.powered_room_cells[CELL]=true
    view.bind_room(room);player.finish_exit.clear();player.clear_carry();player.current_key="";player.last_time=-1;player.motion.clear();view.embedded_case=false;view.sync_case()
    await prepare(game,helmet)
    var shown:Texture2D;var ready:=false
    for tick in 1600:
     shown=step(game)
     if not player.stow_plan.is_empty() and game.visual_time_seconds-float(player.stow_plan.unload_started)>=target:ready=true;break
    check(ready,"Actual cargo route reaches priority test entrance")
    if failures:quit(1);return
    room.suspended=true;shown=step(game)
    check(not player.finish_exit.is_empty(),"Actual ordinary service loss begins candidate exit")
    var state:Dictionary=FLOOR.payload(room).duplicate(true)
    var name:String=event+"-"+("helmet" if helmet else "bare")+"-"+str(roundi(target*100))
    await record_capture(game,view,name+"-before",shown)
    if event=="fire":room.fire=.5;game.running=true;game.paused=false
    elif event=="flood":room.water_level=1.0;game.running=true;game.paused=false
    elif event=="gear":check(game.bill_npc.set_helmet_equipped(not helmet),"Public gear setter accepted")
    elif event=="death":game.bill_npc.prepare_death_motion(game);game.bill_npc.die()
    else:
     game.placed_rooms.erase(room);game.occupied.erase(CELL);await game.bill_npc.rebuild(game);view.bind_room({})
    shown=step(game)
    check(player.finish_exit.is_empty(),"Priority clears finite ordinary exit on first actual update")
    check(game.bill_npc.animation_state()!="carry","Priority source family replaces stale ordinary carry exit")
    if event=="fire":check(game.bill_npc.goal=="fire-retreat","Actual fire refresh dispatches retreat")
    if event=="flood":check(game.bill_npc.movement_medium=="flooded","Actual flooded room selects flooded medium")
    if event=="gear":check(game.bill_npc.helmet_equipped!=helmet,"Actual gear state changed")
    if event=="death":check(game.bill_npc.dead,"Actual mortality flag retained")
    if event!="removal":check(FLOOR.payload(room)==state,"Priority cannot invent or move released floor case")
    else:check(not game.occupied.has(CELL) and not game.placed_rooms.has(room),"Actual room removal drops owning record")
    game.paused=true
    if event!="removal":await record_capture(game,view,name+"-after",shown)
    else:
     game.selected_room_cell=CELL;game._refresh_all();game.grid_view.queue_redraw();await process_frame;await RenderingServer.frame_post_draw
     check(not game.grid_view.content_canvases.has(CELL),"Removed room submits neither actor nor floor prop")
     check(shown.get_image().save_png(OUT+name+"-after-source.png")==OK,"Removed-room replacement source capture")
     check(root.get_texture().get_image().save_png(OUT+name+"-after-room.png")==OK,"Removed-room actual native capture")
     records.append({"name":name+"-after","foot":[game.bill_npc.foot.x,game.bill_npc.foot.y],"caseOwned":false,"caseEnabled":false,"embedded":false,"finishActive":false,"state":game.bill_npc.animation_state(),"direction":game.bill_npc.direction,"roomRemoved":true})
    for tick in 15:
     step(game);check(player.finish_exit.is_empty(),"Priority cannot resurrect ordinary exit")
     if event!="removal":check(FLOOR.payload(room)==state,"Future priority preserves released floor anchor")
    print("BILL FLOOR FINISH PRIORITY ",name," failures=",failures)
    if failures:quit(1);return
 var f=FileAccess.open(OUT+"records.json",FileAccess.WRITE)
 f.store_string(JSON.stringify({"checks":checks,"failures":failures,"records":records,"scope":"20actual priority takeovers during staged ordinary North service-loss exit: fire refresh, room flooding/medium, public gear, mortality, actual placed-room/occupied removal and topology rebuild. Both gears, before/after release;15future exit/case ticks. Removal is controlled fixture mutation, not demolition UI. No successful refuge/full fall, held-case early disposition, Continue, normal selection or continuous motion acceptance."},"  "))
 print("BILL FLOOR CASE FINISH PRIORITY V1: %d checks,%d failures;20cases"%[checks,failures]);quit(1 if failures else 0)
