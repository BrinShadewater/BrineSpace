extends "res://tests/playtest_nursery_art.gd"
const PROGRESS="res://character/krusher-animation-package-v3/package.json"
const CELL=Vector2i(20,20)
var checks:=0
var records:Array=[]
func check(ok:bool,label:String)->void:
 checks+=1;expect(ok,label)
func pixels(texture:Texture2D)->PackedByteArray:
 return (texture.diffuse_texture if texture is CanvasTexture else texture).get_image().get_data()
func run()->void:
 var uid="res://character/krusher-station-lifecycle-v2/native/bare_cargo.gd.uid"
 if not FileAccess.file_exists(uid):
  var uf=FileAccess.open(uid,FileAccess.WRITE);uf.store_string(ResourceUID.id_to_text(ResourceUID.create_id())+"\n")
 var room_id:String="salvage_workshop"
 capture_dir=OS.get_environment("KRUSHER_BARE_CARGO_OUTPUT")
 DirAccess.make_dir_recursive_absolute(capture_dir)
 var store=preload("res://scripts/room_layout_store.gd");store.loaded=true;store.data={}
 root.size=Vector2i(1600,900)
 game=MainScene.instantiate();game.set_meta("authored_site_fixture",true)
 game.meta.save_path="user://krusher-lifecycle-meta.json";game.run_save_path="user://krusher-lifecycle-run.json";game.Preferences.save_path="user://krusher-lifecycle-settings.cfg"
 game.meta.unlocked_architect_ids={"bill":true,"branforth":true};game.meta.selected_architect="branforth"
 root.add_child(game);current_scene=game
 while not game.startup_complete:await process_frame
 game.set_process(false);game.crew_comms.set_process(false);game.tick_timer.stop();game.paused=true
 game.set_process_input(false);game.set_process_unhandled_input(false);game.set_process_unhandled_key_input(false);root.gui_disable_input=true
 game.Architects.advance_core(game,10)
 game.occupied.clear();game.placed_rooms.clear();game.wrecks.clear();game.powered_room_cells.clear();game.unpowered_room_cells.clear()
 game.recovered_crew=[{"architect_id":"bill","alive":true},{"architect_id":"branforth","alive":true}]
 var player=preload("res://scripts/james_cargo_player.gd").new();var progress:Dictionary=JSON.parse_string(FileAccess.get_file_as_string(PROGRESS))
 for path in progress.candidatePacks.bare:player.load_manifest(path,true)
 for path in progress.candidatePacks.helmet:check(player.load_equipment_manifest("diving-helmet",path),"paired admission")
 game.grid_view.branforth_player=player;player.game=game
 var actor=game.branforth_npc
 for peer in [game.bill_npc,game.veld_npc,game.marsh_npc]:peer.active=false
 game.drone_fleet.orders.clear()
 if not game.hand_collapsed:game._toggle_hand_collapsed()
 var center:Vector2=(Vector2(CELL)+Vector2.ONE*.5)*384.0;var camera:Vector2=(Vector2(CELL)+Vector2.ONE*.5)/float(game.GRID_SIZE);var journeys:Array=[]
 for offset in [Vector2i.ZERO,Vector2i.LEFT,Vector2i.RIGHT,Vector2i.UP,Vector2i.DOWN]:
  game._place_room("storage_bay",CELL+offset,true)
  game.occupied[CELL+offset].water_level=.93;game.occupied[CELL+offset].flooded=true;game.powered_room_cells[CELL+offset]=true
 actor.signature="";await actor.rebuild(game);actor.active=true;actor.dead=false
 game.selected_room_cell=CELL;game._refresh_all();game._set_grid_zoom(.8,true,camera);await settle()
 for attempt in range(120):
  game.camera_zoom_target=-1.0;game._restore_grid_view_center(camera);game.grid_view.queue_redraw();await process_frame;await RenderingServer.frame_post_draw
  if game.grid_view.pending_layers.is_empty() and not game.grid_view.zoom_settling and not game.grid_view.zoom_preparing and game._grid_view_center_ratio().distance_to(camera)<.002:break
 var target_cell:=CELL+Vector2i.RIGHT
 game.drone_fleet.sites={target_cell:game.drone_fleet.Sites.make_site("salvage",3)}
 var results:Array=[]
 for direction in ["east","west","south","north"]:
  actor.path.clear();actor.goal="";actor.stage="";actor.state="idle";actor.timer=0;actor.exterior_cancel.clear();actor.expedition.clear();actor.helmet_equipped=false;actor.direction=direction;actor.preview_player=player;actor.tank_oxygen=100;actor.breath_oxygen=100;actor.set_movement_medium("flooded")
  var endpoints:Array=cargo_endpoints(actor,player,center,direction)
  var start:int=int(endpoints[0]);var finish:int=int(endpoints[1])
  check(start>=0 and finish>=0,"Actual furnished cargo endpoints "+direction)
  if start<0 or finish<0:continue
  var origin:Vector2=actor.graph.get_point_position(start)
  var destination:Vector2=actor.graph.get_point_position(finish)
  actor.foot=origin;actor.path=actor.smooth_route(actor.route_between(start,finish));actor.expedition={"phase":"return","cargo":{"Scrap":1},"recall":false,"target":target_cell}
  player.return_plan.clear();player.current_key="";player.last_time=-1;player.last_position=Vector2.ZERO;player.motion.clear();game.visual_time_seconds=0
  var moved:=0;var carry_seen:=false
  for tick in range(1000):
   var previous:Vector2=actor.foot
   if not actor.path.is_empty():actor.move(1.0/120.0)
   else:actor.state="idle"
   game.visual_time_seconds+=1.0/120.0
   var texture:Texture2D=game.grid_view._get_branforth_frame_source(game);var source:Dictionary=player.last_source
   check(texture!=null and not source.is_empty(),"Bare cargo renderer source exists")
   if not source.is_empty():
    check(pixels(texture)==pixels(player.frames[source.key][source.index]),"Exact current bare cargo source")
    carry_seen=carry_seen or str(source.key).begins_with("swim-carry-")
   if previous.distance_to(actor.foot)>.001:moved+=1
   check(actor.swim_segment_clear(previous,actor.foot,actor.direction,actor.direction),"Cargo route clears actual furnished geometry")
   if tick==80:await snapshot(direction,"","cargo-moving",texture,source,camera,actor)
   if actor.path.is_empty():break
  check(moved>20 and actor.foot.distance_to(destination)<.01 and carry_seen,"Bare flooded cargo physically arrives "+direction)
  results.append({"kind":"cargo-route","direction":direction,"movingSamples":moved,"arrived":actor.foot.distance_to(destination)<.01})
  for action in ["work","pickup"]:
   for desired in range(6):
    actor.foot=origin;actor.path.clear();actor.state="idle";actor.direction=direction;actor.exterior_cancel.clear()
    var source_key:String=("salvage-" if action=="work" else "swim-pickup-")+direction
    var elapsed:=.000001
    for slot in range(desired):elapsed+=float(player.timing[source_key].durations[slot])/1000.0
    if action=="work":elapsed=elapsed/actor.salvage_cycle_seconds(direction)*(preload("res://scripts/crew_expedition.gd").WORK_SECONDS/6.0)
    actor.expedition={"phase":"salvage" if action=="work" else "pickup","cargo":{},"recall":false,"target":target_cell,"elapsed":elapsed}
    player.motion.clear();player.current_key="";player.last_time=-1;player.phase=0;game.visual_time_seconds=0
    game.drone_fleet.sites[target_cell].erase("james_case_release")
    var before:Texture2D=game.grid_view._get_branforth_frame_source(game)
    check(player.last_source.index==desired,"Actual source interruption index "+source_key+str(desired))
    check(preload("res://scripts/crew_expedition.gd").request_recall(game,actor),"Production recall request accepted")
    check(actor.begin_exterior_cancel(),"Production bare flooded cancellation begins")
    check(actor.exterior_cancel.index==desired,"Cancellation retains selected source index")
    var texture:Texture2D=game.grid_view._get_branforth_frame_source(game)
    check(pixels(before)==pixels(texture),"Bare interrupted whole-pose entrance exact")
    actor.expedition.phase="return";actor.path=actor.smooth_route(actor.route_between(start,finish))
    var clip:String=actor.animation_state()+"-"+direction;var seen:Dictionary={};var case_anchor:=Vector2.INF;var cancellation_moved:=false;var last:Texture2D
    for tick in range(200):
     texture=game.grid_view._get_branforth_frame_source(game)
     if not actor.exterior_cancel_active():break
     var source:Dictionary=player.last_source;seen[source.index]=true
     check(source.key==clip and pixels(texture)==pixels(player.frames[clip][source.index]),"Native renderer uses exact bare cancellation slot")
     var extent:Array=player.clip_extent(clip,"")
     check(actor.swim_segment_clear(actor.foot,actor.foot,direction,direction,false,extent),"Whole cancellation envelope clears furniture")
     if tick in [0,25]:await snapshot(direction,"","cancel-"+action+str(desired)+"-%03d"%tick,texture,source,camera,actor)
     last=texture
     actor.advance_exterior_cancel(game,1.0/120.0,false)
     var previous:Vector2=actor.foot
     if not actor.path.is_empty():actor.move(1.0/120.0)
     if previous.distance_to(actor.foot)>.001:cancellation_moved=true
     game.visual_time_seconds+=1.0/120.0
     var release:Dictionary=game.drone_fleet.sites[target_cell].get("james_case_release",{})
     if not release.is_empty():
      if case_anchor==Vector2.INF:case_anchor=release.foot
      check(case_anchor==release.foot,"Released case retains world anchor")
    check(not actor.exterior_cancel_active(),"Bare cancellation has finite completion")
    check(seen.size()==player.frames[clip].size(),"Every bare cancellation slot rendered")
    check(cancellation_moved,"Cancellation retains physical return movement")
    check((case_anchor!=Vector2.INF)==(action=="pickup" and desired>0),"Only acquired case is deposited")
    check(actor.expedition.cargo.is_empty() and game.drone_fleet.sites[target_cell].units==3,"No extraction or return cargo awarded")
    results.append({"kind":"cancel","direction":direction,"action":action,"index":desired,"slots":seen.keys(),"casePlaced":case_anchor!=Vector2.INF,"moved":cancellation_moved})
 var file=FileAccess.open(capture_dir.path_join("report.json"),FileAccess.WRITE)
 file.store_string(JSON.stringify({"checks":checks,"failures":failures,"records":records,"cases":results,"scope":"Four bare flooded furnished-room cargo routes and48indexed work/pickup cancellations through production move, recall, cancellation, clearance and renderer. Staged in-room cargo/extraction state; not helmetless exterior dispatch, automatic job selection or fresh-scene Continue."},"\t"))
 print("KRUSHER_BARE_CARGO checks=%d failures=%d cases=%d captures=%d"%[checks,failures,results.size(),records.size()]);game.free();quit(1 if failures else 0)
func snapshot(direction:String,gear:String,label:String,texture:Texture2D,source:Dictionary,camera:Vector2,actor)->void:
 var name:String=direction+"-"+("bare" if gear.is_empty() else "helmet")+"-"+label
 game._restore_grid_view_center(camera);await capture(name)
 check(game._grid_view_center_ratio().distance_to(camera)<.002,"Native swim camera remains centered")
 var world_foot:Vector2=game.get_chief_branforth_position()+Vector2(0,game.get_cell_size()*.038)+actor.observation_visual_offset()*game.get_cell_size()/384.0;var scale:float=game.get_cell_size()/384.0*65.28/148.0
 var screen:Rect2=root.get_stretch_transform()*game.grid_view.get_global_transform_with_canvas()*Rect2(world_foot-Vector2(texture.get_meta("crew_pivot"))*scale,texture.get_size()*scale)
 check((root.get_stretch_transform()*game.grid_scroll.get_global_rect()).encloses(screen),"Entire swim sprite canvas visible")
 var foot_screen:Vector2=root.get_stretch_transform()*game.grid_view.get_global_transform_with_canvas()*world_foot
 records.append({"file":name+".png","label":direction+"-"+label,"gear":"bare" if gear.is_empty() else "helmet","time":game.visual_time_seconds,"action":actor.animation_state(),"direction":actor.direction,"source":source.duplicate(true),"screenFoot":[foot_screen.x,foot_screen.y]})

func clear_node(actor,desired:Vector2,center:Vector2)->int:
 var retained:Vector2=actor.foot;var selected:int=-1;var distance:float=INF
 for id in actor.graph.get_point_ids():
  var point:Vector2=actor.graph.get_point_position(id)
  if absf(point.x-center.x)>175 or absf(point.y-center.y)>175:continue
  actor.foot=point
  if not actor.swim_segment_clear(point,point,actor.direction,actor.direction) or not actor.swim_segment_clear(point,point,actor.direction,actor.direction,true) or not actor.Life.clear(actor,"swim-distress"):continue
  var score:float=point.distance_squared_to(desired)
  if score<distance:distance=score;selected=id
 actor.foot=retained
 return selected

func cargo_endpoints(actor,player,center:Vector2,direction:String)->Array:
 var axis:Vector2={"east":Vector2.RIGHT,"west":Vector2.LEFT,"south":Vector2.DOWN,"north":Vector2.UP}[direction]
 var nodes:Array=[]
 var extent:Array=player.clip_extent("swim-carry-"+direction,"")
 for id in actor.room_nodes.get(CELL,[]):
  var p:Vector2=actor.graph.get_point_position(id)
  if p.distance_to(center)>155:continue
  if actor.swim_segment_clear(p,p,direction,direction,false,extent):nodes.append(id)
 nodes.sort_custom(func(a,b):return actor.graph.get_point_position(a).distance_squared_to(center-axis*65)<actor.graph.get_point_position(b).distance_squared_to(center-axis*65))
 var ends:Array=nodes.duplicate()
 ends.sort_custom(func(a,b):return actor.graph.get_point_position(a).distance_squared_to(center+axis*65)<actor.graph.get_point_position(b).distance_squared_to(center+axis*65))
 for start in nodes:
  for finish in ends:
   var origin:Vector2=actor.graph.get_point_position(start);var target:Vector2=actor.graph.get_point_position(finish)
   if (target-origin).dot(axis)<60:continue
   actor.foot=origin
   var route:PackedVector2Array=actor.smooth_route(actor.route_between(start,finish),origin)
   if route.is_empty():continue
   var previous:Vector2=origin;var valid:=true
   for point in route:
    var facing:String=actor.travel_heading(previous,point,direction)
    if facing!=direction or not actor.swim_segment_clear(previous,point,facing,facing,false,extent):valid=false;break
    previous=point
   if valid:
    print("CARGO_ENDPOINTS ",direction," nodes=",nodes.size()," start=",origin," finish=",target)
    return [start,finish]
 return [-1,-1]
