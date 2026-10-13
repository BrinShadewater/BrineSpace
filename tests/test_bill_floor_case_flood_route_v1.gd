extends SceneTree
const RELEASE=preload("res://character/bill-floor-case-north-v1/release_state.gd")
const FLOOR=preload("res://character/bill-floor-case-north-v1/floor_state.gd")
const FLOOR_SAVE=preload("res://character/bill-floor-case-north-v1/floor_checkpoint.gd")
const SAVE=preload("res://scripts/run_save.gd")
const CHECKPOINT=preload("res://scripts/bill_carry_checkpoint.gd")
const ACTOR=preload("res://character/bill-floor-case-north-v1/finish_actor.gd")
const PLAYER=preload("res://character/bill-carry-cardinal-runtime-v3/stow_player.gd")
const CELL=Vector2i(20,21)
const OUT="res://output/bill-floor-case-flood-route-v1/"
var checks:=0
var failures:=0
var records:=[]
var mask:="normal"
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
  game.grid_view.queue_redraw();await process_frame
  if mask=="floor-hidden" and game.grid_view.flood_surfaces.has(CELL):game.grid_view.flood_surfaces[CELL].hide()
  if mask=="foreground-hidden":game.grid_view.surface_passes[game.grid_view.Surface.FOREGROUND].hide()
  await RenderingServer.frame_post_draw
  var submitted:=false
  for cell in game.grid_view.content_canvases:
   for slot in game.grid_view.content_canvases[cell].slots:
    if slot.visible and slot.item.get("kind","")=="actor" and game.grid_view.content_canvases[cell].renderer.external_actor_texture==texture:submitted=true
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
 var view=preload("res://character/bill-floor-case-north-v1/flood_readability_v2.gd").new()
 view.embedded=true;view.hide();game.grid_view.add_child(view);game.grid_view.rare_room_views["salvage_workshop"]=view
 return [game,player,view]
func run():
 check(OS.get_user_data_dir().replace("\\","/").begins_with(OS.get_environment("APPDATA").replace("\\","/")+"/"),"Scratch APPDATA required")
 for helmet in [false,true]:
  var fixture:Array=await new_fixture();var game=fixture[0];var player=fixture[1];var view=fixture[2]
  game.running=false;game.paused=true;game.occupied[CELL].suspended=false;game.occupied[CELL].water_level=0.0
  await prepare(game,helmet)
  var shown:Texture2D;var ready:=false
  for tick in 1600:
   shown=step(game)
   if not player.stow_plan.is_empty() and game.visual_time_seconds-float(player.stow_plan.unload_started)>=.39:ready=true;break
  check(ready,"Actual cargo route reaches released exit entrance")
  game.occupied[CELL].suspended=true;shown=step(game);check(not player.finish_exit.is_empty(),"Actual ordinary exit begins")
  var label:String="helmet" if helmet else "bare";var first:Vector2=game.bill_npc.foot;var distance:=0.0;var previous:Vector2=first;var saw_water:=false;var saw_dry_after:=false;var states:Dictionary={}
  game.running=true;game.paused=false
  for tick in 600:
   # Prescribed room water history isolates animation/material joins; actual
   # medium selection, oxygen, safety, actor navigation and source clock advance.
   var seconds:float=float(tick)/60.0
   var water:float=clampf(seconds/2.0,0,1) if seconds<6 else clampf(1-(seconds-6)/2.0,0,1)
   game.occupied[CELL].water_level=water
   shown=step(game)
   var actor=game.bill_npc;distance+=previous.distance_to(actor.foot);previous=actor.foot
   saw_water=saw_water or actor.movement_medium=="flooded";saw_dry_after=saw_dry_after or (saw_water and actor.movement_medium=="dry")
   states[actor.animation_state()]=true
   check(not actor.dead,"Real oxygen/failure rules keep ten-second route alive")
   if tick%2==0:
    game.paused=true;view.readable_water=true
    var name:String=label+"-"+str(tick).pad_zeros(3)
    await record_capture(game,view,name+"-candidate",shown)
    records.back()["tick"]=tick;records.back()["clock"]=game.visual_time_seconds;records.back()["water"]=water;records.back()["medium"]=actor.movement_medium;records.back()["pathPoints"]=actor.path.size();records.back()["goal"]=actor.goal;records.back()["cell"]=[actor.cell_at(actor.foot).x,actor.cell_at(actor.foot).y]
    if tick%20==0 or tick in [64,66,68,400,402,404]:
     view.readable_water=false;await record_capture(game,view,name+"-normal",shown)
     records.back()["tick"]=tick;records.back()["clock"]=game.visual_time_seconds;records.back()["water"]=water;records.back()["medium"]=actor.movement_medium;records.back()["pathPoints"]=actor.path.size();records.back()["goal"]=actor.goal;records.back()["cell"]=[actor.cell_at(actor.foot).x,actor.cell_at(actor.foot).y]
    game.paused=false
   if failures:quit(1);return
  check(distance>20,"Actual controller advances physical route")
  check(saw_water and saw_dry_after,"Actual room medium crosses dry/water/dry")
  check(states.has("swim") or states.has("tread"),"Actual source selection enters water family")
  records.append({"name":label+"-summary","distance":distance,"states":states.keys(),"sawWater":saw_water,"sawDryAfter":saw_dry_after})
  game.queue_free();await process_frame
 var f=FileAccess.open(OUT+"records.json",FileAccess.WRITE)
 f.store_string(JSON.stringify({"checks":checks,"failures":failures,"records":records,"scope":"Actual actor/world-medium/oxygen/safety/navigation and source clock at60Hz; native capture every2ticks/30Hz. Prescribed ten-second room-water rise/hold/drain, fixture-selected actor/player/workshop treatment. No natural hydrology, whole station loop or normal production admission."},"  "))
 print("BILL FLOOR CASE FLOOD ROUTE V1: %d checks,%d failures"%[checks,failures]);quit(1 if failures else 0)
