extends "res://tests/playtest_nursery_art.gd"
const PROGRESS="res://character/krusher-animation-package-v10/package.json"
const JOBS="res://character/krusher-continuity-audit-v1/bunk-scope.json"
const HAB=Vector2i(20,22)
var checks:=0
var records:Array=[]
func check(ok:bool,label:String)->void:
 checks+=1;expect(ok,label)
func pixels(texture:Texture2D)->PackedByteArray:
 return (texture.diffuse_texture if texture is CanvasTexture else texture).get_image().get_data()
func run()->void:
 var uid="res://character/krusher-continuity-audit-v1/native/bunk.gd.uid"
 if not FileAccess.file_exists(uid):
  var uf=FileAccess.open(uid,FileAccess.WRITE);uf.store_string(ResourceUID.id_to_text(ResourceUID.create_id())+"\n")
 capture_dir="res://character/krusher-continuity-audit-v1/review/bunk"
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
 for job in jobs:
  var gear:String="" if job.gear=="bare" else "diving-helmet";actor.helmet_equipped=not gear.is_empty();actor.bunk_motion=motion.duplicate(true);actor.direction="east";actor.goal_cell=HAB;actor.dead=false;actor.movement_medium="dry"
  var action:String=job.key.trim_suffix("-east");actor.stage={"bunk-enter":"life_lie","bunk-sleep":"life_sleep","bunk-exit":"life_get_up"}[action];actor.state="idle"
  player.current_key="";player.last_time=-1.0;player.last_position=Vector2.ZERO;player.motion.clear()
  game.visual_time_seconds=0.0
  if action=="bunk-sleep":player.frame(action,"east",0.0,actor.foot/384.0,gear)
  var cursor:=0.0
  for i in range(job.files.size()):
   var hold:float=job.durations[i]/1000.0;var elapsed:float=cursor+hold*.5
   game.visual_time_seconds=elapsed
   actor.timer=actor.BUNK_SECONDS-elapsed if action!="bunk-sleep" else 10.4-elapsed
   check(actor.animation_state()==action,"Production lifecycle selects action")
   var texture:Texture2D=game.grid_view._get_branforth_frame_source(game);check(texture!=null,"Native source exists")
   check(pixels(texture)==Image.load_from_file(job.files[i]).get_data(),"Real grid selects exact Krusher pose")
   var at:Vector2=actor.foot-center+actor.observation_visual_offset()
   var t:float=actor.BUNK_SECONDS-actor.timer if action=="bunk-enter" else actor.timer if action=="bunk-exit" else actor.BUNK_SECONDS
   var expected:Vector2=motion.entry
   if t>=.36:expected.y=Vector2(motion.rest).y+16+actor.BUNK_SEAT_ROWS*65.28/148.0
   if t>=.66:expected=Vector2(motion.rest)+Vector2(0,16*(1-clampf((t-.96)/.6,0,1)))
   check(at.distance_to(expected)<.001,"Actual mattress/edge registered contact")
   check(texture.get_meta("crew_standing_height")==148.0,"World ruler preserved")
   var name:String="%s-%s-%02d"%[job.gear,job.key,i]
   game._restore_grid_view_center(camera_center)
   await capture(name)
   check(game._grid_view_center_ratio().distance_to(camera_center)<.002,"Capture camera retains centered room")
   var world_foot:Vector2=game.get_chief_branforth_position()+Vector2(0,game.get_cell_size()*.038)+actor.observation_visual_offset()*game.get_cell_size()/384.0
   var sprite_scale:float=game.get_cell_size()/384.0*65.28/148.0
   var sprite_rect:Rect2=Rect2(world_foot-Vector2(texture.get_meta("crew_pivot"))*sprite_scale,texture.get_size()*sprite_scale)
   var screen:Rect2=root.get_stretch_transform()*game.grid_view.get_global_transform_with_canvas()*sprite_rect
   var clip:Rect2=root.get_stretch_transform()*game.grid_scroll.get_global_rect()
   check(clip.encloses(screen),"Entire registered sprite canvas lies inside visible grid")
   room_pixels(HAB).save_png(capture_dir.path_join(name+"-room.png"))
   records.append({"file":name+"-room.png","key":job.key,"gear":job.gear,"pose":i,"elapsed":elapsed,"hold":hold,"at":[at.x,at.y],"foot":[actor.foot.x,actor.foot.y],"source":job.files[i]});cursor+=hold
  if action=="bunk-sleep":
   check((actor.foot-center+actor.observation_visual_offset()).distance_to(Vector2(motion.rest))<.001,"Sleeper rests at actual mattress point")
 # Ordinary update drives the complete finite lifecycle and releases contact.
 actor.helmet_equipped=false;actor.stage="life_lie";actor.state="idle";actor.timer=actor.BUNK_SECONDS;actor.bunk_motion=motion.duplicate(true)
 actor.update(game,actor.BUNK_SECONDS+.0001);check(actor.stage=="life_sleep","Entry update hands off to sleep")
 actor.update(game,10.4001);check(actor.stage=="life_get_up","Sleep update hands off to exit")
 actor.update(game,actor.BUNK_SECONDS+.0001);check(not actor.bunk_motion_active(),"Exit update releases mattress contact")
 var f=FileAccess.open(capture_dir.path_join("report.json"),FileAccess.WRITE);f.store_string(JSON.stringify({"checks":checks,"failures":failures,"records":records,"scope":"All paired bunk poses in real main scene and production renderer; normal fatigue chooser/route/arrival/update lifecycle; actual registered mattress offsets. Default authored bunk, no roster/save integration; not all furniture or water lifecycle proof."},"\t"))
 print("KRUSHER_BUNK checks=%d failures=%d captures=%d"%[checks,failures,records.size()]);game.free();quit(1 if failures else 0)



