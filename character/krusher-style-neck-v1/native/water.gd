extends "res://tests/playtest_nursery_art.gd"
const PROGRESS="res://character/krusher-animation-package-v9/package.json"
const CELL=Vector2i(20,20)
var checks:=0
var records:Array=[]
func check(ok:bool,label:String)->void:
 checks+=1;expect(ok,label)
func pixels(texture:Texture2D)->PackedByteArray:
 return (texture.diffuse_texture if texture is CanvasTexture else texture).get_image().get_data()
func run()->void:
 var uid="res://character/krusher-style-neck-v1/native/water.gd.uid"
 if not FileAccess.file_exists(uid):
  var uf=FileAccess.open(uid,FileAccess.WRITE);uf.store_string(ResourceUID.id_to_text(ResourceUID.create_id())+"\n")
 var room_id:String="salvage_workshop"
 capture_dir=OS.get_environment("KRUSHER_WATER_OUTPUT")
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
 for direction in ["east","west","south","north"]:
  for gear in ["","diving-helmet"]:
   actor.path.clear();actor.goal="";actor.stage="";actor.state="idle";actor.timer=0;actor.expedition.clear();actor.exterior_cancel.clear();actor.bunk_motion.clear();actor.console_motion.clear();actor.construction_motion.clear();actor.helmet_equipped=not gear.is_empty();actor.direction=direction;actor.preview_player=player;actor.tank_oxygen=100;actor.breath_oxygen=100
   check(actor.set_movement_medium("flooded"),"Flooded medium admitted")
   var horizontal:bool=direction in ["east","west"];var reverse:bool=direction in ["west","north"]
   var start:int=clear_node(actor,center+Vector2(-80,40),center)
   var target:int=clear_node(actor,center+Vector2(112,-32),center)
   if not horizontal:
    start=clear_node(actor,center+Vector2(80,-100),center);target=clear_node(actor,center+Vector2(80,100),center)
   if reverse:
    var swap:int=start;start=target;target=swap
   check(start>=0 and target>=0,"Actual furnished room endpoints exist")
   if start<0 or target<0:continue
   actor.foot=actor.graph.get_point_position(start)
   var route:PackedVector2Array=actor.route_between(start,target);actor.path=actor.smooth_route(route)
   check(not actor.path.is_empty(),"Production furnished swim route exists")
   player.return_plan.clear();player.current_key="";player.last_time=-1.0;player.last_position=Vector2.ZERO;player.motion.clear();game.visual_time_seconds=0;game.paused=false
   await snapshot(direction,gear,"initial-tread",game.grid_view._get_branforth_frame_source(game),player.last_source,camera,actor)
   check(actor.animation_state()=="tread","Clear initial point uses ordinary tread")
   var timeline:Array=[];var moving:=0;var sources:Dictionary={};var previous_key:String="";var first_transition_allowed:bool=false
   for tick in range(1800):
    var old:Vector2=actor.foot;var previous_facing:String=actor.direction
    if not actor.path.is_empty():actor.move(1.0/60.0)
    else:actor.state="idle"
    if tick==0:first_transition_allowed=game.grid_view._water_transition_clear(actor)
    game.visual_time_seconds+=1.0/60.0
    var texture:Texture2D=game.grid_view._get_branforth_frame_source(game);var actual:Dictionary=player.last_source.duplicate(true)
    check(texture!=null,"Flooded native texture exists")
    check(actor.swim_segment_clear(old,actor.foot,actor.direction,previous_facing),"Actual swim footprint clears furniture")
    if old.distance_to(actor.foot)>.001:moving+=1
    if not actual.is_empty():
     var bank:Dictionary=player.frames if gear.is_empty() else player.equipment_frames[gear]
     check(bank.has(actual.key) and pixels(texture)==pixels(bank[actual.key][actual.index]),"Production renderer uses exact Krusher swim pose")
     sources[actual.key]=true
    timeline.append({"time":game.visual_time_seconds,"foot":[actor.foot.x,actor.foot.y],"direction":actor.direction,"action":actor.animation_state(),"source":actual})
    var key:String=str(actual.get("key",""))
    if key!=previous_key or tick%90==0 or (actor.path.is_empty() and tick%30==0):
     await snapshot(direction,gear,"route-%04d"%tick,texture,actual,camera,actor)
    previous_key=key
    if actor.path.is_empty() and tick>30:
     for hold in range(48):
      game.visual_time_seconds+=1.0/60.0;game.grid_view._get_branforth_frame_source(game)
     await snapshot(direction,gear,"arrival-held",game.grid_view._get_branforth_frame_source(game),player.last_source,camera,actor)
     break
   var start_seen:bool=false
   for source_key in sources:
    if str(source_key).begins_with("swim-start-"):start_seen=true
   check(start_seen==first_transition_allowed,"Start clip matches actual full-transition clearance permission")
   check(moving>20 and actor.foot.distance_to(actor.graph.get_point_position(target))<.01,"Real route reaches destination")
   actor.direction=direction;actor.state="idle";actor.tank_oxygen=8;actor.breath_oxygen=3
   var distressed:bool=actor.animation_state()=="swim-distress"
   check(distressed,"Low-air distress clears actual destination furniture")
   if distressed:
    for t in range(120):
     game.visual_time_seconds+=1.0/60.0;var tex:Texture2D=game.grid_view._get_branforth_frame_source(game)
     if t in [0,30,60,90,119]:await snapshot(direction,gear,"distress-%03d"%t,tex,player.last_source,camera,actor)
    actor.tank_oxygen=100;actor.breath_oxygen=100
    check(actor.animation_state()!="swim-distress","Air recovery leaves distress normally")
    await snapshot(direction,gear,"air-restored",game.grid_view._get_branforth_frame_source(game),player.last_source,camera,actor)
   journeys.append({"direction":direction,"gear":"bare" if gear.is_empty() else "helmet","routePoints":route.size(),"movingSamples":moving,"sources":sources.keys(),"distress":distressed,"startTransitionAllowed":first_transition_allowed,"startTransitionPlayed":start_seen,"timeline":timeline})
 var f=FileAccess.open(capture_dir.path_join("report.json"),FileAccess.WRITE);f.store_string(JSON.stringify({"checks":checks,"failures":failures,"records":records,"journeys":journeys,"scope":"Eight staged furnished flooded-room routes with production movement/renderer, both gears, original source pixels/clearance, low-air pose selector and restoration; not natural survival/air economy, exterior cargo cancellation, continuous recording or roster integration."},"\t"))
 print("KRUSHER_WATER checks=%d failures=%d captures=%d journeys=%d"%[checks,failures,records.size(),journeys.size()]);game.free();quit(1 if failures else 0)
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



