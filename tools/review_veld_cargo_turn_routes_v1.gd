extends SceneTree
const MainScene=preload("res://scenes/main.tscn")
const BARE="res://character/veld-swim-carry-turn-matrix-coherent-v1/bare-manifest.json"
const HELMET="res://character/veld-swim-carry-turn-matrix-coherent-v1/helmet-manifest.json"
const OUT="res://character/veld-swim-carry-turn-matrix-coherent-v1/route-review-v1/"
const AXES={"north":Vector2.UP,"east":Vector2.RIGHT,"south":Vector2.DOWN,"west":Vector2.LEFT}
var checks:=0
var failures:=0
func check(ok:bool,message:String)->void:
 checks+=1
 if not ok:failures+=1;push_error(message)
func _init()->void:call_deferred("run")
func straight(points:PackedVector2Array,a:Vector2,b:Vector2)->bool:
 if points.is_empty():return false
 for p in points:
  if Geometry2D.get_closest_point_to_segment(p,a,b).distance_to(p)>.01:return false
 return true
func cargo_pose_clear(npc)->bool:return preload("res://scripts/crew_life.gd").clear(npc,"cargo-turn")
func run()->void:
 check(OS.get_environment("APPDATA").contains("veld-water-material-scratch"),"Scratch profile required")
 if failures:quit(1);return
 DirAccess.make_dir_recursive_absolute(OUT)
 var game=MainScene.instantiate();var prefix="user://veld_turn_routes_%d"%OS.get_process_id()
 game.meta.save_path=prefix+".json";game.run_save_path=prefix+".loop";game.Preferences.save_path=prefix+".cfg"
 root.add_child(game);current_scene=game;game._confirm_doctrines();game._set_paused(true)
 game.architect_run.clear();game.occupied.clear();game.placed_rooms.clear();game.powered_room_cells.clear()
 var origin:=Vector2i(20,20)
 for offset in [Vector2i.ZERO,Vector2i.LEFT,Vector2i.RIGHT,Vector2i.UP,Vector2i.DOWN]:
  var room:Dictionary=game.RoomDatabaseScript.get_room("maintenance_bay" if offset==Vector2i.ZERO else "storage_bay").duplicate(true)
  room.pos=origin+offset;room.rotation=0;game.occupied[room.pos]=room;game.placed_rooms.append(room);game.powered_room_cells[room.pos]=true
 for actor in [game.bill_npc,game.veld_npc,game.branforth_npc,game.marsh_npc]:actor.active=false
 game.test_walker_cell=Vector2i(-1,-1);game.bill_npc.expedition.clear()
 var npc=game.veld_npc;npc.rebuild(game);npc.active=true;npc.set_movement_medium("flooded")
 game.selected_card_id="";game.hover_cell=Vector2i(-1,-1);game._refresh_all()
 var player=game.grid_view.veld_player
 if true:
  player.load_manifest(BARE,true);check(player.load_equipment_manifest("diving-helmet",HELMET),"Candidate equipment compatibility")
 root.mode=Window.MODE_WINDOWED;root.size=Vector2i(1600,900);game._set_grid_zoom(game.DEFAULT_GRID_ZOOM*.65)
 await process_frame;game._center_grid_on_station_now();await process_frame
 player.load_manifest("res://character/veld-swim-carry-matrix-coherent-v1/bare-manifest.json",true)
 check(player.load_equipment_manifest("diving-helmet","res://character/veld-swim-carry-matrix-coherent-v1/helmet-manifest.json"),"Candidate cargo endpoints")
 var candidate:Dictionary=JSON.parse_string(FileAccess.get_file_as_string("res://character/veld-swim-carry-turn-matrix-coherent-v1/candidate-clearance-profile-v1.json"))
 npc.swim_clearance=candidate.swim;npc.tread_clearance=candidate.tread;npc.action_clearance=candidate.actions;npc.swim_link_cache.clear();npc.swim_region_cache.clear()
 preload("res://scripts/crew_life.gd").clearance={"veld":candidate.life}
 npc.expedition={"phase":"return","cargo":{"salvage":1}}
 var nodes:Dictionary={}
 for id in npc.graph.get_point_ids():nodes[npc.graph.get_point_position(id)]=id
 var results:Array=[];var manifest:Dictionary=JSON.parse_string(FileAccess.get_file_as_string(BARE))
 for equipment in ["","diving-helmet"]:
  npc.set_helmet_equipped(not equipment.is_empty())
  for state in manifest.states:
   if "--probe" in OS.get_cmdline_user_args() and (state.id!="swim-carry-turn-south-west" or not equipment.is_empty()):continue
   var parts:PackedStringArray=state.id.split("-");var source:String=parts[3];var dest:String=parts[4];var found:Dictionary={}
   npc.direction=source
   for vertex in nodes:
    var a:Vector2=vertex-AXES[source]*96.0;var b:Vector2=vertex+AXES[dest]*112.0
    if not nodes.has(a) or not nodes.has(b):continue
    npc.foot=vertex;npc.direction=dest
    if not cargo_pose_clear(npc):continue
    var gear:String="bare" if equipment.is_empty() else "helmet"
    var duration:float=player.cycle_seconds(state.id,equipment)
    var swept_turn_clear:bool=npc.swim_segment_clear(vertex,vertex+AXES[dest]*(npc.movement_rate()*duration+3.0),dest,source,false,preload("res://scripts/crew_life.gd").clearance["veld"][gear]["cargo-turn-"+dest])
    if "--probe" in OS.get_cmdline_user_args():
     if swept_turn_clear:continue
    elif not swept_turn_clear:continue
    if not npc.swim_segment_clear(a,vertex,source) or not npc.swim_segment_clear(vertex,b,dest,source):continue
    npc.direction=source;npc.foot=a
    var incoming:PackedVector2Array=npc.smooth_route(npc.route_between(nodes[a],nodes[vertex]))
    npc.direction=dest;npc.foot=vertex
    var outgoing:PackedVector2Array=npc.smooth_route(npc.route_between(nodes[vertex],nodes[b]))
    if not straight(incoming,a,vertex) or not straight(outgoing,vertex,b):continue
    found={"a":a,"b":b,"vertex":vertex,"incoming":incoming,"outgoing":outgoing};break
   check(not found.is_empty(),"Actual furnished graph corner exists: "+state.id+" "+equipment)
   if found.is_empty():results.append({"state":state.id,"equipment":equipment,"cornerFound":false});continue
   npc.foot=found.a;npc.direction=source;npc.state="walk";npc.stage="";npc.goal="curiosity";npc.goal_cell=npc.cell_at(found.b);npc.timer=0.0
   npc.avoidance_positions.clear();npc.avoidance_position=Vector2.INF
   npc.path=found.incoming.duplicate()
   for p in found.outgoing:
    if npc.path.is_empty() or npc.path[-1].distance_to(p)>.01:npc.path.append(p)
   player.motion.clear();player.current_key="";player.current_equipment="";player.last_time=-1.0
   game.visual_time_seconds=0.0;game.grid_view._get_veld_frame_source(game)
   var planned:PackedVector2Array=npc.path.duplicate()
   var seen:Dictionary={};var started:=false;var completed:=false;var cancelled_safely:=false;var turn_started:=0.0;var last_clip:="";var capture:="";var direction_changes:Array=[];var previous:=source
   var row:Array=player.frames[state.id] if equipment.is_empty() else player.equipment_frames[equipment][state.id]
   for tick in range(400):
    if npc.path.is_empty():break
    npc.move(.025);game.visual_time_seconds+=.025
    if npc.direction!=previous:direction_changes.append({"from":previous,"to":npc.direction,"tick":tick,"foot":[npc.foot.x,npc.foot.y],"next":str(npc.path[0]) if not npc.path.is_empty() else "arrived","path":str(npc.path)});previous=npc.direction
    var texture:Texture2D=game.grid_view._get_veld_frame_source(game);var clip:String=player.motion.get("clip","")
    if clip==state.id:
     if not started:turn_started=float(player.motion.started)
     started=true
     var slot:int=row.find(texture);check(slot>=0,"Actual frame source uses selected candidate texture")
     if slot>=0:seen[slot]=true
     check(cargo_pose_clear(npc),"Turn drawn only in safe actual geometry")
     check(game.grid_view._get_veld_frame_source(game)==texture,"Paused simulation retains route phase")
     if capture.is_empty() and slot==3:
      game.grid_view.queue_redraw();await process_frame;await RenderingServer.frame_post_draw
      var image:=root.get_texture().get_image();var cell_size:float=game.get_cell_size();var room_rect:=Rect2(Vector2(npc.cell_at(npc.foot))*cell_size,Vector2.ONE*cell_size)
      var screen:Rect2=root.get_stretch_transform()*game.grid_view.get_global_transform_with_canvas()*room_rect
      capture=OUT+("narrow-" if "--probe" in OS.get_cmdline_user_args() else "")+state.id+("-helmet" if not equipment.is_empty() else "-bare")+".png"
      image.get_region(Rect2i(screen.intersection(Rect2(Vector2.ZERO,image.get_size())))).save_png(capture)
    if started and last_clip==state.id and clip!=state.id and npc.animation_state()=="swim-carry":
     print("TURN COMPLETION TRACE ",state.id," time=",game.visual_time_seconds," foot=",npc.foot," action_clear=",cargo_pose_clear(npc)," direction=",npc.direction," state=",npc.state," motion=",player.motion)
     if game.visual_time_seconds+0.00001>=turn_started+player.cycle_seconds(state.id,equipment):
      completed=true;check(texture.get_image().get_data()==row[-1].get_image().get_data(),"Exact master loop0 after route turn")
     else:
      cancelled_safely=not cargo_pose_clear(npc)
      check(cancelled_safely,"Early cancellation must be required by actual geometry")
    last_clip=clip
   check(started,"Actual path direction change enters candidate: "+state.id)
   if "--probe" in OS.get_cmdline_user_args():
    check(cancelled_safely and not completed,"Narrow-route transition cancelled safely before completion")
   else:
    check(seen.size()==row.size(),"Actual route exercises every phase: "+state.id)
    check(completed,"Finite route turn completes before arrival: "+state.id)
   check(npc.foot.distance_to(found.b)<.01,"Actual move arrives at graph endpoint: "+state.id)
   results.append({"state":state.id,"equipment":equipment,"cornerFound":true,"vertex":[found.vertex.x,found.vertex.y],"incoming":str(found.incoming),"outgoing":str(found.outgoing),"planned":str(planned),"pathPoints":found.incoming.size()+found.outgoing.size(),"directionChanges":direction_changes,"phases":seen.keys(),"started":started,"completed":completed,"cancelledSafely":cancelled_safely,"arrived":npc.foot.distance_to(found.b)<.01,"capture":capture})
 var report:=FileAccess.open(OUT+("narrow-guard-checks.json" if "--probe" in OS.get_cmdline_user_args() else "route-checks.json"),FileAccess.WRITE)
 report.store_string(JSON.stringify({"checks":checks,"failures":failures,"graphNodes":nodes.size(),"results":results,"scope":"Explicit staged12direction candidates; forced flooded Veld on actual five authored furnished rooms, real graph route/smoothing/move/grid frame source. Candidate conservative profile injected; no exterior,natural flooding or concurrent traffic claim."},"\t"));report.close()
 for child in root.get_children():child.process_mode=Node.PROCESS_MODE_DISABLED
 preload("res://scripts/audio_shutdown.gd").stop_audio(root);await create_timer(.2,true,false,true).timeout;game.free()
 if not FileAccess.file_exists("res://tools/review_veld_cargo_turn_routes_v1.gd.uid"):
  var uid:=FileAccess.open("res://tools/review_veld_cargo_turn_routes_v1.gd.uid",FileAccess.WRITE);uid.store_string(ResourceUID.id_to_text(ResourceUID.create_id())+"\n");uid.close()
 print("VELD CARGO TURN ROUTES: ",checks," checks, ",failures," failures")
 quit(0 if failures==0 else 1)
