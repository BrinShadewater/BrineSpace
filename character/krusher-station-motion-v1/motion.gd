extends "res://tests/playtest_nursery_art.gd"
const PROGRESS="res://character/krusher-animation-package-v11/package.json"
const JOBS="res://character/krusher-continuous-playback-v1/bunk-scope.json"
const HAB=Vector2i(20,22)
var checks:=0
var records:Array=[]
func check(ok:bool,label:String)->void:
 checks+=1;expect(ok,label)
func pixels(texture:Texture2D)->PackedByteArray:
 return (texture.diffuse_texture if texture is CanvasTexture else texture).get_image().get_data()
func digest(data:PackedByteArray)->String:
 var hash=HashingContext.new();hash.start(HashingContext.HASH_SHA256);hash.update(data);return hash.finish().hex_encode()
func run()->void:
 var uid="res://character/krusher-station-motion-v1/motion.gd.uid"
 if not FileAccess.file_exists(uid):
  var uf=FileAccess.open(uid,FileAccess.WRITE);uf.store_string(ResourceUID.id_to_text(ResourceUID.create_id())+"\n")
 capture_dir="res://character/krusher-station-motion-v1/review"
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
 game.wrecks.erase(HAB);game._place_room("corridor",Vector2i(20,21),true);game._place_room("crew_hab",HAB,true);game.occupied[HAB].rotation=3;game.powered_room_cells[HAB]=true
 game.recovered_crew=[{"architect_id":"bill","alive":true},{"architect_id":"branforth","alive":true}]
 var player=preload("res://scripts/crew_sprite_player.gd").new();var progress:Dictionary=JSON.parse_string(FileAccess.get_file_as_string(PROGRESS))
 for path in progress.candidatePacks.bare:player.load_manifest(path,true)
 for path in progress.candidatePacks.helmet:check(player.load_equipment_manifest("diving-helmet",path),"paired candidate admission")
 game.grid_view.branforth_player=player
 var actor=game.branforth_npc;await actor.rebuild(game);actor.active=true
 for peer in [game.bill_npc,game.veld_npc,game.marsh_npc]:peer.active=false
 var stations:Array=actor.RoomActivity.stations(actor.geometry[HAB]);var station:Dictionary={}
 for item in stations:
  if item.get("branforth_bunk",false):station=item;break
 check(not station.is_empty(),"Actual authored compatible bunk exists")
 if station.is_empty():quit(1);return
 var center:Vector2=(Vector2(HAB)+Vector2.ONE*.5)*384.0
 actor.foot=actor.graph.get_point_position(actor.nearest_in_room(center+Vector2(0,130),HAB));actor.path.clear();actor.goal="";actor.stage=""
 for need in actor.needs:actor.needs[need]=100.0 if need=="fatigue" else 0.0
 if actor.decision_rng==null:actor.decision_rng=RandomNumberGenerator.new()
 actor.decision_rng.seed=8923;actor.choose_goal(game)
 check(actor.goal=="fatigue" and actor.goal_cell==HAB,"Normal need chooser selects bunk")
 for unused in range(2000):
  if actor.path.is_empty():break
  actor.move(.05)
 check(actor.path.is_empty() and actor.foot.distance_to(center+station.point)<.01,"Production route reaches exact contact")
 actor.arrive();check(actor.animation_state()=="bunk-enter" and actor.direction=="east","Normal arrival selects bunk animation")
 check(is_equal_approx(player.cycle_seconds("bunk-enter-east"),actor.BUNK_SECONDS),"Animation/controller transition duration")
 var motion:Dictionary=actor.bunk_motion.duplicate(true)
 if not game.hand_collapsed:game._toggle_hand_collapsed()
 game.selected_room_cell=HAB;game._refresh_all();game._set_grid_zoom(.9,true,(Vector2(HAB)+Vector2.ONE*.5)/float(game.GRID_SIZE));game.inspector_focus_button.set_meta("cell",HAB);game._focus_inspected_room()
 await settle()
 var camera_center:Vector2=(Vector2(HAB)+Vector2.ONE*.5)/float(game.GRID_SIZE)
 game._set_grid_zoom(.9,true,camera_center)
 await settle()
 var centered:=false
 for attempt in range(120):
  game.camera_zoom_target=-1.0;game._restore_grid_view_center(camera_center)
  await process_frame
  if game._grid_view_center_ratio().distance_to(camera_center)<.002:centered=true;break
 check(centered,"Camera centers actual bunk room")
 if not centered:quit(1);return
 var jobs:Array=JSON.parse_string(FileAccess.get_file_as_string(JOBS))
 var expected:Dictionary={}
 for job in jobs:
  var hashes:Array=[]
  for source in job.files:hashes.append(digest(Image.load_from_file(source).get_data()))
  expected[job.gear+":"+job.key]=hashes
 var coverage:Dictionary={}
 for gear in ["bare","helmet"]:
  actor.helmet_equipped=gear=="helmet";actor.stage="life_lie";actor.state="idle";actor.timer=actor.BUNK_SECONDS;actor.bunk_motion=motion.duplicate(true)
  actor.path.clear();actor.goal="fatigue";actor.goal_cell=HAB
  for need in actor.needs:actor.needs[need]=0.0
  player.current_key="";player.last_time=-1.0;player.motion.clear()
  var previous_action="";var stages:Array=[];var elapsed=0.0
  for frame in range(600):
   var action:String=actor.animation_state()
   game.visual_time_seconds=elapsed
   var texture:Texture2D=game.grid_view._get_branforth_frame_source(game)
   check(texture!=null,"Controller supplies a visible texture")
   var source_hash:String=digest(pixels(texture))
   var key:String=gear+":"+action+"-east"
   if expected.has(key):
    check(source_hash in expected[key],"Actual controller uses current candidate source")
    if not coverage.has(key):coverage[key]=[]
    if source_hash not in coverage[key]:coverage[key].append(source_hash)
   check(texture.get_meta("crew_standing_height")==148.0,"Station detail ruler retained")
   game._restore_grid_view_center(camera_center);game.grid_view.queue_redraw()
   await process_frame
   await RenderingServer.frame_post_draw
   var filename:String="%s-%04d.png"%[gear,frame]
   var room:Image=room_pixels(HAB);room.save_png(capture_dir.path_join(filename))
   if previous_action!=action:
    stages.append(action)
    root.get_texture().get_image().save_png(capture_dir.path_join("%s-%s-full.png"%[gear,action]))
   var world_foot:Vector2=game.get_chief_branforth_position()+Vector2(0,game.get_cell_size()*.038)+actor.observation_visual_offset()*game.get_cell_size()/384.0
   var sprite_scale:float=game.get_cell_size()/384.0*65.28/148.0
   var sprite_rect:Rect2=Rect2(world_foot-Vector2(texture.get_meta("crew_pivot"))*sprite_scale,texture.get_size()*sprite_scale)
   var screen:Rect2=root.get_stretch_transform()*game.grid_view.get_global_transform_with_canvas()*sprite_rect
   var clip:Rect2=root.get_stretch_transform()*game.grid_scroll.get_global_rect()
   check(clip.encloses(screen),"Whole actor canvas is in the viewport")
   check(game._grid_view_center_ratio().distance_to(camera_center)<.002,"Camera remains on bunk")
   records.append({"file":filename,"gear":gear,"frame":frame,"time":elapsed,"action":action,"stage":actor.stage,"timer":actor.timer,"sourceHash":source_hash,"scale":sprite_scale,"screen":[screen.position.x,screen.position.y,screen.size.x,screen.size.y],"roomSize":[room.get_width(),room.get_height()]})
   previous_action=action
   if stages.size()>=3 and not actor.bunk_motion_active():break
   actor.update(game,1.0/30.0);elapsed+=1.0/30.0
  check(stages.slice(0,3)==["bunk-enter","bunk-sleep","bunk-exit"],"Advancing controller completes entry/sleep/exit in order")
  check(not actor.bunk_motion_active(),"Exit releases real mattress contact")
 for key in expected:
  var seen:Array=coverage.get(key,[])
  for source in expected[key]:check(source in seen,"Advancing draw covers every authored bunk hold source")
 var f=FileAccess.open(capture_dir.path_join("report.json"),FileAccess.WRITE)
 f.store_string(JSON.stringify({"checks":checks,"failures":failures,"records":records,"coverage":coverage,"scope":"Two actual main-scene bunk lifecycles advanced at 30Hz with production actor updates and rendering. Default authored bunk at centered room zoom .9. Captured native frames preserve simulated cadence; PNG capture is not a real-time video, other furniture and roster integration remain separate."},"\t"))
 print("KRUSHER_STATION_MOTION checks=%d failures=%d frames=%d"%[checks,failures,records.size()]);game.free();quit(1 if failures else 0)
