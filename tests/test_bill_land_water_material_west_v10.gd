extends SceneTree
const RELEASE=preload("res://character/bill-floor-case-north-v1/release_state.gd")
const FLOOR=preload("res://character/bill-floor-case-north-v1/floor_state.gd")
const FLOOR_SAVE=preload("res://character/bill-floor-case-north-v1/floor_checkpoint.gd")
const SAVE=preload("res://scripts/run_save.gd")
const CHECKPOINT=preload("res://scripts/bill_carry_checkpoint.gd")
const ACTOR=preload("res://character/bill-land-water-material-west-v10/support_actor.gd")
const PLAYER=preload("res://character/bill-carry-cardinal-runtime-v3/stow_player.gd")
const CELL=Vector2i(20,21)
const OUT="res://output/bill-land-water-material-west-v10/"
var checks:=0
var failures:=0
var records:=[]
var mask:="normal"
func check(ok:bool,message:String):
 checks+=1
 if not ok:failures+=1;push_error(message)
func _init():call_deferred("run")
func fresh():
 var game=load("res://character/bill-land-water-material-west-v10/fixture.tscn").instantiate();game.meta.save_path="user://bill-carry-continue.meta";game.run_save_path="user://bill-carry-continue.loop";root.add_child(game);current_scene=game
 while not game.startup_complete:await process_frame
 check(game.get_script().resource_path=="res://character/bill-land-water-material-west-v10/fixture_main.gd","Exact current fixture main selected")
 check(game.grid_view.get_script().resource_path=="res://character/bill-land-water-material-west-v10/grid.gd","Exact current bridge renderer selected")
 game.grid_view.human_water_player.load_manifest("res://character/bill-swim-west-calibrated-v6/bare/manifest.json",true)
 check(game.grid_view.human_water_player.load_equipment_manifest("diving-helmet","res://character/bill-swim-west-calibrated-v6/helmet/manifest.json"),"Current paired swim candidate admitted in fixture only")
 for gear in ["","diving-helmet"]:
  var g:String="bare" if gear.is_empty() else "helmet"
  var files:Array=game.grid_view.human_water_player.frames["swim-west"] if gear.is_empty() else game.grid_view.human_water_player.equipment_frames[gear]["swim-west"]
  check(files.size()==7,"Current swim has seven phases")
  for i in range(7):
   var image=Image.new()
   var paths:Dictionary={"bare":["res://character/bill-swim-west-calibrated-v6/bare/frames/swim-west/000.png","res://character/bill-swim-west-calibrated-v6/bare/frames/swim-west/001.png","res://character/bill-swim-west-calibrated-v6/bare/frames/swim-west/002.png","res://character/bill-swim-west-calibrated-v6/bare/frames/swim-west/003.png","res://character/bill-swim-west-calibrated-v6/bare/frames/swim-west/004.png","res://character/bill-swim-west-calibrated-v6/bare/frames/swim-west/005.png","res://character/bill-swim-west-calibrated-v6/bare/frames/swim-west/006.png"],"helmet":["res://character/bill-swim-west-calibrated-v6/helmet/frames/swim-west/000.png","res://character/bill-swim-west-calibrated-v6/helmet/frames/swim-west/001.png","res://character/bill-swim-west-calibrated-v6/helmet/frames/swim-west/002.png","res://character/bill-swim-west-calibrated-v6/helmet/frames/swim-west/003.png","res://character/bill-swim-west-calibrated-v6/helmet/frames/swim-west/004.png","res://character/bill-swim-west-calibrated-v6/helmet/frames/swim-west/005.png","res://character/bill-swim-west-calibrated-v6/helmet/frames/swim-west/006.png"]}
   check(image.load(paths[g][i])==OK,"Current swim raw source available")
   image.convert(Image.FORMAT_RGBA8)
   var loaded:Image=files[i].get_image();loaded.convert(Image.FORMAT_RGBA8)
   check(image.get_data()==loaded.get_data(),"Current swim loaded pixels exact")
 for enter in [true,false]:
  for gear in ["","diving-helmet"]:
   var bank:Array=game.grid_view.bridge_bank(gear,enter)[0]
   var files:Dictionary={
    "entry-bare":"res://character/bill-land-water-west-v15/bare/manifest.json",
    "entry-helmet":"res://character/bill-land-water-west-v15/helmet/manifest.json",
    "exit-bare":"res://character/bill-water-exit-west-master-v13/bare/manifest.json",
    "exit-helmet":"res://character/bill-water-exit-west-master-v13/helmet/manifest.json"}
   var manifest_path:String=files[("entry" if enter else "exit")+"-"+("bare" if gear.is_empty() else "helmet")]
   var manifest:Dictionary=JSON.parse_string(FileAccess.get_file_as_string(manifest_path))
   check(bank.size()==(7 if enter else 8),"Current source bank has exact seven entry/eight exit frames")
   for index in range(bank.size()):
    var image=Image.new();var path:String=manifest_path.get_base_dir().path_join(manifest.states[0].frameFiles[index])
    check(image.load(path)==OK,"Current raw frame available")
    image.convert(Image.FORMAT_RGBA8)
    var loaded:Image=bank[index].get_image();loaded.convert(Image.FORMAT_RGBA8)
    check(image.get_data()==loaded.get_data(),"Actual loaded pixels equal current entry/exit frame")
 game.set_process(false);game.tick_timer.stop();game._set_paused(true,false);game.crew_comms.set_process(false);game.crew_comms.minimize()
 check(is_instance_of(game.grid_view.human_water_player,preload("res://scripts/bill_carry_player.gd")),"Selected normal playback")
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
 if game.bill_npc.has_method("observe_finish"):game.bill_npc.observe_finish(game,shown)
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
 records.append({"name":name,"foot":[game.bill_npc.foot.x,game.bill_npc.foot.y],"anchor":[view.case_anchor.x,view.case_anchor.y],"caseEnabled":view.case_enabled,"caseOwned":not FLOOR.payload(game.occupied[CELL]).is_empty(),"embedded":view.embedded_case,"bridgeActive":not game.grid_view.bridge.is_empty(),"materialWeight":game.grid_view.material_weight,"headBindingKind":game.grid_view.head_binding_kind,"materialHeadOffset":[game.grid_view.material_head_offset.x,game.grid_view.material_head_offset.y],"finishActive":not game.grid_view.human_water_player.finish_exit.is_empty(),"sortY":depth,"propRect":[prop_bounds.position.x,prop_bounds.position.y,prop_bounds.size.x,prop_bounds.size.y],"state":game.bill_npc.animation_state(),"direction":game.bill_npc.direction})
func new_fixture():
 var game=await fresh();game.paused=false;game.Architects.advance_core(game,10);game.paused=true
 game._place_room("salvage_workshop",CELL,true);game.powered_room_cells[CELL]=true
 var old=game.grid_view.human_water_player;var player=preload("res://character/bill-floor-case-north-v1/finish_player.gd").new()
 for field in ["frames","timing","strides","equipment_frames","equipment_timing","equipment_strides","carry_banks","active_binding"]:player.set(field,old.get(field))
 game.grid_view.human_water_player=player
 var view=preload("res://character/bill-land-water-material-west-v10/view.gd").new()
 view.bridge_grid=game.grid_view
 view.embedded=true;view.hide();game.grid_view.add_child(view);game.grid_view.rare_room_views["salvage_workshop"]=view
 return [game,player,view]
func run():
 check(OS.get_user_data_dir().replace("\\","/").begins_with(OS.get_environment("APPDATA").replace("\\","/")+"/"),"Scratch APPDATA required")
 for helmet in [false,true]:
  var fixture:Array=await new_fixture();var game=fixture[0];var player=fixture[1];var view=fixture[2]
  game.running=false;game.paused=true;game.occupied[CELL].suspended=false;game.occupied[CELL].water_level=0.0
  var actor=ACTOR.new();game.bill_npc=actor;actor.transition_grid=game.grid_view;actor.transition_game=game;actor.preview_player=player;actor.active=true;actor.dead=false;actor.stage="";actor.expedition.clear();actor.helmet_equipped=helmet;actor.movement_medium="dry";actor.breath_oxygen=15;actor.tank_oxygen=60;actor.needs={"hunger":0.0,"fatigue":0.0,"curiosity":0.0,"maintenance":0.0}
  for other in [game.veld_npc,game.branforth_npc,game.marsh_npc]:other.active=false
  await actor.rebuild(game)
  # Plan against the full current pose family, not only the selected old swim.
  # Runtime bridge admission and rechecks remain authoritative and unchanged.
  var gear:String="diving-helmet" if helmet else ""
  var route_poses:Array=[]
  route_poses.append_array(game.grid_view.bridge_bank(gear,true)[0])
  route_poses.append_array(game.grid_view.bridge_bank(gear,false)[0])
  route_poses.append_array(player.frames["swim-west"] if gear.is_empty() else player.equipment_frames[gear]["swim-west"])
  var route_extent:Array=game.grid_view.bridge_extent(route_poses)
  var pair:Array=[];var best:=0.0;var old_clear_count:=0;var current_clear_count:=0
  for a in actor.room_nodes[CELL]:
   var from:Vector2=actor.graph.get_point_position(a)
   for b in actor.room_nodes[CELL]:
    var to:Vector2=actor.graph.get_point_position(b);var length:float=from.distance_to(to)
    if absf(from.y-to.y)>.01 or length<best or length<100:continue
    if actor.segment_clear(from,to) and actor.swim_segment_clear(from,to,"east") and actor.swim_segment_clear(to,from,"west"):
     old_clear_count+=1
     if actor.swim_segment_clear(from,to,"east","east",false,route_extent) and actor.swim_segment_clear(to,from,"west","west",false,route_extent):
      current_clear_count+=1
      pair=[from,to] if from.x<to.x else [to,from];best=length
  var route_report:Dictionary={"gear":gear,"extent":route_extent,"oldClearCandidates":old_clear_count,"currentClearCandidates":current_clear_count,"length":best,"pair":pair}
  var route_file=FileAccess.open(OUT+("helmet" if helmet else "bare")+"-route.json",FileAccess.WRITE);route_file.store_string(JSON.stringify(route_report,"  "));route_file.close()
  print("CURRENT WEST ROUTE: "+JSON.stringify(route_report))
  check(pair.size()==2,"Actual room graph supplies collision-clear current full-pose navigation segment")
  if pair.is_empty():quit(1);return
  actor.foot=pair[1];actor.direction="west";actor.goal="flood-retreat";actor.goal_cell=CELL;actor.state="walk";actor.path=PackedVector2Array([pair[0],pair[1],pair[0],pair[1]]);actor.activity="prescribed collision-clear route"
  var shown:Texture2D=game.grid_view._get_human_frame_source(actor.animation_state(),actor.direction)
  var label:String="helmet" if helmet else "bare";var first:Vector2=game.bill_npc.foot;var distance:=0.0;var previous:Vector2=first;var saw_water:=false;var saw_dry_after:=false;var states:Dictionary={}
  game.running=true;game.paused=false
  var exit_guards_done:=false;var pre_support_seen:=0
  for tick in 600:
   # Prescribed room water history isolates animation/material joins; actual
   # medium selection, oxygen, safety, actor navigation and source clock advance.
   var seconds:float=float(tick)/60.0
   var water:float=clampf(seconds/2.0,0,1) if seconds<6 else clampf(1-(seconds-6)/2.0,0,1)
   game.occupied[CELL].water_level=water
   shown=step(game)
   if game.grid_view.material_weight>=0 and game.grid_view.source_head_centers.has(shown):
    var expected_head:Vector2=(Vector2(game.grid_view.source_head_centers[shown])-Vector2(shown.get_meta("crew_pivot",Vector2(160,224))))*(65.28/float(shown.get_meta("crew_standing_height",148)))
    check(game.grid_view.material_head_offset.distance_to(expected_head)<.00001,"Readability follows exact current selected source and gear center")
   distance+=previous.distance_to(actor.foot);previous=actor.foot
   saw_water=saw_water or actor.movement_medium=="flooded";saw_dry_after=saw_dry_after or (saw_water and actor.movement_medium=="dry")
   states[actor.animation_state()]=true
   check(not actor.dead,"Real oxygen/failure rules keep ten-second route alive")
   check(game.grid_view.material_weight>=0 and game.grid_view.material_weight<=1 if not game.grid_view.bridge.is_empty() else game.grid_view.material_weight==-1,"Material follows finite bridge only")
   if not game.grid_view.bridge.is_empty() and game.grid_view.bridge.target_state=="walk":
    var elapsed:float=game.visual_time_seconds-float(game.grid_view.bridge.started)
    if elapsed>=.065 and elapsed<.095:
     check(shown.get_image().get_data()==game.grid_view.bridge_bank("diving-helmet" if helmet else "",false)[0][1].get_image().get_data(),"Actual renderer presents new lowering-hand pose before supporting hold")
     check(actor.support_holds.is_empty(),"Floating hand-lowering interval precedes support hold")
     pre_support_seen+=1
   if tick==72:await check_same_tick_guards(game)
   if not exit_guards_done and not game.grid_view.bridge.is_empty() and game.grid_view.bridge.target_state=="walk" and game.visual_time_seconds-float(game.grid_view.bridge.started)>=.12:
    await check_same_tick_guards(game);exit_guards_done=true
   if tick in range(60,105) or tick in range(410,460):
    game.paused=true;view.readable_water=true
    var name:String=label+"-"+str(tick).pad_zeros(3)
    await record_capture(game,view,name+"-candidate",shown)
    records.back()["tick"]=tick;records.back()["clock"]=game.visual_time_seconds;records.back()["water"]=water;records.back()["medium"]=actor.movement_medium;records.back()["pathPoints"]=actor.path.size();records.back()["goal"]=actor.goal;records.back()["cell"]=[actor.cell_at(actor.foot).x,actor.cell_at(actor.foot).y]
    if false:
     view.readable_water=false;await record_capture(game,view,name+"-normal",shown)
     records.back()["tick"]=tick;records.back()["clock"]=game.visual_time_seconds;records.back()["water"]=water;records.back()["medium"]=actor.movement_medium;records.back()["pathPoints"]=actor.path.size();records.back()["goal"]=actor.goal;records.back()["cell"]=[actor.cell_at(actor.foot).x,actor.cell_at(actor.foot).y]
    game.paused=false
   if failures:quit(1);return
  var diagnosis:Dictionary={"gear":label,"events":game.grid_view.bridge_events,"activeBridge":game.grid_view.bridge,"state":actor.animation_state(),"direction":actor.direction,"foot":actor.foot,"states":states.keys(),"records":records,"checks":checks,"failures":failures}
  var trace=FileAccess.open(OUT+label+"-diagnosis.json",FileAccess.WRITE);trace.store_string(JSON.stringify(diagnosis,"  "));trace.close()
  print("CURRENT WEST BRIDGE DIAGNOSIS: "+JSON.stringify({"gear":label,"events":game.grid_view.bridge_events,"state":actor.animation_state(),"direction":actor.direction,"states":states.keys()}))
  check(pre_support_seen>=1,"New lowering-hand pose observed in live current bridge")
  check(actor.support_holds.size()>=20,"Supporting exit poses hold the physical root on actual move calls")
  if not actor.support_holds.is_empty():
   var anchor:Vector2=actor.support_holds[0].foot
   var route:PackedVector2Array=actor.support_holds[0].path
   for hold in actor.support_holds:
    check(hold.foot==anchor and hold.path==route,"All support samples keep exact physical root and unconsumed path")
   check(float(actor.support_holds.back().needs.hunger)>float(actor.support_holds[0].needs.hunger),"Normal hunger continues while support movement is held")
   check(actor.foot!=anchor,"Normal physical movement resumes after finite exit")
   records.append({"name":label+"-support-holds","samples":actor.support_holds})
  check(exit_guards_done,"Actual exit bridge supplied active same-tick guard interval")
  check(game.grid_view.bridge_events.filter(func(e):return e.kind=="start").size()==2,"Actual West entry and independent exit admission")
  check(game.grid_view.bridge_events.filter(func(e):return e.kind=="complete" and e.endpointExact).size()==2,"Both finite West bridges complete on exact incoming gait phase")
  records.append({"name":label+"-bridge-events","events":game.grid_view.bridge_events})
  check(distance>20,"Actual controller advances physical route")
  check(saw_water and saw_dry_after,"Actual room medium crosses dry/water/dry")
  check(states.has("swim") or states.has("tread"),"Actual source selection enters water family")
  records.append({"name":label+"-summary","distance":distance,"states":states.keys(),"sawWater":saw_water,"sawDryAfter":saw_dry_after})
  game.running=false;game.paused=true;game.occupied[CELL].water_level=.8
  actor.direction="west";actor.movement_medium="flooded";actor.state="swim"
  game.grid_view.bridge={}
  var probes:Array=player.frames["swim-west"] if not helmet else player.equipment_frames["diving-helmet"]["swim-west"]
  for probe_index in range(probes.size()):
   game.grid_view.head_probe_texture=probes[probe_index]
   for fitted in [false,true]:
    view.source_head_fit_enabled=fitted
    var selected:Texture2D=game.grid_view._get_human_frame_source("swim","west")
    check(selected==probes[probe_index],"Controlled ordinary-swim exact source selected")
    check(game.grid_view.material_weight==-1,"Controlled ordinary-swim uses existing non-bridge tint")
    await record_capture(game,view,label+"-swim-probe-"+str(probe_index)+( "-fitted" if fitted else "-baseline"),selected)
  game.grid_view.head_probe_texture=null;view.source_head_fit_enabled=true
  game.queue_free();await process_frame
  if failures:
   print("BILL LAND WATER MATERIAL WEST V10: %d checks,%d failures; stopped after failed gear interval"%[checks,failures])
   quit(1);return
 var f=FileAccess.open(OUT+"records.json",FileAccess.WRITE)
 f.store_string(JSON.stringify({"checks":checks,"failures":failures,"records":records,"scope":"Actual actor/world-medium/oxygen/safety/navigation and source clock at60Hz; fixture-only supporting exit intercepts move while normal needs/hazard dispatch still runs; West entry and exit boundary capture every60Hz tick plus32synthetic guard presentations. Prescribed ten-second room-water rise/hold/drain, fixture-selected player/workshop treatment, actual normal Bill actor. Fixture-only source bridge advances on visual simulation clock, West entry and independently authored exit, dynamic exact outgoing/incoming phases, union pose envelope admission/recheck and terminal target gait rebind. Initial graph-validated path prescribed; subsequent movement and safety use actual controller. No native checkpoint/Continue, natural job dispatch/hydrology, whole station loop or normal production admission."},"  "))
 print("BILL LAND WATER MATERIAL WEST V10: %d checks,%d failures"%[checks,failures]);quit(1 if failures else 0)

func check_same_tick_guards(game):
 var grid=game.grid_view;var actor=game.bill_npc;var player=grid.human_water_player;var view=grid.rare_room_views["salvage_workshop"]
 var phase:String="entry" if grid.bridge.target_state=="swim" else "exit"
 var label:String=("helmet" if actor.helmet_equipped else "bare")+"-"+phase
 var original_clock:float=game.visual_time_seconds
 var original_geometry:Dictionary=actor.geometry.duplicate(true);var original_swim_cache:Dictionary=actor.swim_region_cache.duplicate(true)
 check(not grid.bridge.is_empty(),"Active bridge for same-tick guard probes")
 var actor_fields:Dictionary={}
 for field in ["dead","helmet_equipped","direction","stage","goal"]:actor_fields[field]=actor.get(field)
 var grid_fields:Dictionary={};var player_fields:Dictionary={}
 for field in ["human_animation_key","human_animation_started","human_animation_last_time","human_animation_phase","human_animation_last_position"]:grid_fields[field]=grid.get(field)
 for field in ["current_key","current_equipment","phase","last_time","started","last_position","motion"]:
  var value=player.get(field);player_fields[field]=value.duplicate(true) if value is Dictionary else value
 var plan:Dictionary=grid.bridge.duplicate(true);var previous:Dictionary=grid.bridge_previous.duplicate(true);var events:Array=grid.bridge_events.duplicate(true)
 await record_capture(game,view,label+"-guard-active-candidate",grid._get_human_frame_source(actor.animation_state(),actor.direction))
 check(view.material_weight>=0,"Live draw binds current bridge weight")
 for kind in ["gear","facing","death","stage","clock","geometry","emergency"]:
  if kind=="gear":actor.helmet_equipped=not actor.helmet_equipped
  elif kind=="facing":actor.direction="east"
  elif kind=="death":actor.dead=true
  elif kind=="stage":actor.stage="fixture-priority-takeover"
  elif kind=="emergency":actor.goal="fire-retreat"
  elif kind=="clock":game.visual_time_seconds=float(plan.started)-.01
  else:
   var center:Vector2=(Vector2(CELL)+Vector2.ONE*.5)*384
   actor.geometry[CELL].blockers.append(Rect2(actor.foot-center-Vector2(100,100),Vector2(200,200)))
  var state:String=actor.animation_state();var shown:Texture2D=grid._get_human_frame_source(state,actor.direction)
  check(grid.bridge.is_empty(),"Same-tick "+kind+" clears staged bridge")
  var normal:Texture2D=grid.bridge_normal_source(state,actor.direction)
  check(shown==normal,"Same-tick "+kind+" returns authoritative normal source")
  await record_capture(game,view,label+"-guard-"+kind+"-candidate",shown)
  check(view.material_weight==-1,"Actual draw clears "+kind+" bridge material")
  check(grid.material_source==shown,"Actual draw source binding current on "+kind)
  game.visual_time_seconds=original_clock;actor.geometry=original_geometry.duplicate(true);actor.swim_region_cache=original_swim_cache.duplicate(true)
  for field in actor_fields:actor.set(field,actor_fields[field])
  for field in grid_fields:grid.set(field,grid_fields[field])
  for field in player_fields:player.set(field,player_fields[field].duplicate(true) if player_fields[field] is Dictionary else player_fields[field])
  grid.bridge=plan.duplicate(true);grid.bridge_previous=previous.duplicate(true);grid.bridge_events=events.duplicate(true)
 records.append({"name":label+"-same-tick-guards","kinds":["gear","facing","death","stage","clock","geometry","emergency"],"scope":"Native synthetic active-bridge takeovers:gear/facing/death/stage at same clock; clock reversal and temporary local collision blocker. Actual retained draw clears material via current-source binding. Not natural priority route/death completion/gear gesture. Geometry/player/clock restored after each capture."})
