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
 var uid="res://character/krusher-station-lifecycle-v2/native/workshop.gd.uid"
 if not FileAccess.file_exists(uid):
  var uf=FileAccess.open(uid,FileAccess.WRITE);uf.store_string(ResourceUID.id_to_text(ResourceUID.create_id())+"\n")
 var room_id:String="salvage_workshop"
 capture_dir=OS.get_environment("KRUSHER_WORKSHOP_OUTPUT")
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
 for quarter in range(4):
  game.occupied.clear();game.placed_rooms.clear();game.powered_room_cells.clear();game.unpowered_room_cells.clear();game.selected_rotation=quarter
  game._place_room(room_id,CELL,true);game.occupied[CELL].rotation=quarter;game.powered_room_cells[CELL]=true
  actor.signature="";await actor.rebuild(game);actor.active=true;actor.dead=false;actor.movement_medium="dry";actor.bunk_motion.clear();actor.console_motion.clear();actor.exterior_cancel.clear();actor.meal_return.clear();actor.construction_motion.clear();actor.hull_return.clear();actor.hull_resume.clear()
  var station:Dictionary={}
  for candidate in actor.RoomActivity.stations(actor.geometry[CELL]):
   if actor.can_stand(center+candidate.point):station=candidate;break
  check(not station.is_empty(),"Reachable workshop contact q"+str(quarter))
  if station.is_empty():continue
  game.selected_room_cell=CELL;game._refresh_all();game._set_grid_zoom(.8,true,camera);await settle()
  for attempt in range(120):
   game.camera_zoom_target=-1.0;game._restore_grid_view_center(camera);game.grid_view.queue_redraw();await process_frame;await RenderingServer.frame_post_draw
   if game.grid_view.pending_layers.is_empty() and not game.grid_view.zoom_settling and not game.grid_view.zoom_preparing and game._grid_view_center_ratio().distance_to(camera)<.002:break
  for gear in ["","diving-helmet"]:
   game.occupied[CELL].erase(preload("res://character/james-floor-case-west-v1/checkpoint_floor_state_v2.gd").FIELD)
   actor.foot=center+station.point;actor.path.clear();actor.goal="curiosity";actor.goal_cell=CELL;actor.stage="";actor.state="idle";actor.timer=0;actor.helmet_equipped=not gear.is_empty();actor.preview_player=player
   for need in actor.needs:actor.needs[need]=0.0
   actor.decision_rng=RandomNumberGenerator.new();actor.decision_rng.seed=9123
   player.return_plan.clear();player.current_key="";player.last_time=-1.0;player.last_position=Vector2.ZERO;player.motion.clear();game.visual_time_seconds=0.0;game.paused=false
   check(actor.begin_room_activity(),"Production workshop begins at actual station")
   check(actor.stage=="workshop_inspect","Production inspection entry")
   var timeline:Array=[];var previous_stage:String="";var previous_clip:String="";var visited:Dictionary={};var sources:Dictionary={};var moving_samples:=0;var route:Array=[];var start:Vector2=actor.foot;var release_seen:=false;var completed:=false
   # Run the whole ordinary service and carry journey, recording every simulation frame.
   for step in range(3000):
    var old_foot:Vector2=actor.foot;var old_stage:String=actor.stage;var old_clock:float=actor.action_elapsed()
    if not actor.path.is_empty() and route.is_empty() and actor.stage=="workshop_carry":
     for point in actor.path:route.append([point.x,point.y])
    game.visual_time_seconds+=1.0/60.0;actor.update(game,1.0/60.0)
    var action:String=actor.animation_state();var key:String=action+"-"+actor.direction
    var texture:Texture2D=game.grid_view._get_branforth_frame_source(game)
    check(texture!=null,"Live workshop sprite")
    check(actor.can_stand(actor.foot) and actor.segment_clear(old_foot,actor.foot),"Generated route stays on real floor")
    if old_foot.distance_to(actor.foot)>.001:moving_samples+=1
    visited[actor.stage]=true
    var actual:Dictionary=player.last_source.duplicate(true);var bank:Dictionary=player.frames if gear.is_empty() else player.equipment_frames[gear]
    if not actual.is_empty():
     check(bank.has(actual.key) and pixels(texture)==pixels(bank[actual.key][actual.index]),"Current renderer uses exact Krusher bank pose")
     sources[actual.key]=true
    var clip:String=player.motion.get("clip","")
    var placed:bool=game.occupied[CELL].has(preload("res://character/james-floor-case-west-v1/checkpoint_floor_state_v2.gd").FIELD)
    release_seen=release_seen or placed
    timeline.append({"time":game.visual_time_seconds,"stage":actor.stage,"action":action,"direction":actor.direction,"source":actual,"foot":[actor.foot.x,actor.foot.y],"clip":clip,"floorCase":placed})
    if actor.stage!=previous_stage or clip!=previous_clip or (actor.stage=="workshop_unload" and old_clock<.6 and actor.action_elapsed()>=.6) or (step%60==0 and actor.stage=="workshop_carry"):
     var name:String="q%d-%s-%s-%04d"%[quarter,"bare" if gear.is_empty() else "helmet",actor.stage if not actor.stage.is_empty() else "idle",step]
     game._restore_grid_view_center(camera);await capture(name);check(game._grid_view_center_ratio().distance_to(camera)<.002,"Camera centered during service/journey")
     var world_foot:Vector2=game.get_chief_branforth_position()+Vector2(0,game.get_cell_size()*.038)+actor.observation_visual_offset()*game.get_cell_size()/384.0;var scale:float=game.get_cell_size()/384.0*65.28/148.0
     var screen:Rect2=root.get_stretch_transform()*game.grid_view.get_global_transform_with_canvas()*Rect2(world_foot-Vector2(texture.get_meta("crew_pivot"))*scale,texture.get_size()*scale)
     check((root.get_stretch_transform()*game.grid_scroll.get_global_rect()).encloses(screen),"Entire service sprite canvas visible")
     room_pixels(CELL).save_png(capture_dir.path_join(name+"-room.png"));records.append({"file":name+"-room.png","quarter":quarter,"gear":"bare" if gear.is_empty() else "helmet","time":game.visual_time_seconds,"stage":actor.stage,"action":action,"direction":actor.direction,"source":actual,"foot":[actor.foot.x,actor.foot.y],"floorCase":placed})
    if old_stage=="workshop_unload" and actor.stage.is_empty():completed=true;break
    previous_stage=actor.stage;previous_clip=clip
   check(completed,"Ordinary unload completes service")
   check(visited.has("workshop_work") and visited.has("workshop_pickup") and visited.has("workshop_carry") and visited.has("workshop_unload"),"Every production service phase reached")
   check(not route.is_empty() and moving_samples>20 and actor.foot.distance_to(start)>40,"Production carry journey moves case through room")
   journeys.append({"quarter":quarter,"gear":"bare" if gear.is_empty() else "helmet","route":route,"steps":timeline.size(),"movingSamples":moving_samples,"visited":visited.keys(),"sources":sources.keys(),"floorReleaseObserved":release_seen,"timeline":timeline})
 var f=FileAccess.open(capture_dir.path_join("report.json"),FileAccess.WRITE);f.store_string(JSON.stringify({"checks":checks,"failures":failures,"records":records,"journeys":journeys,"scope":"Krusher manifests in production James cargo player/actor and actual workshop renderer; eight default room rotation/gear service journeys through inspection/work/pickup/generated carry route/unload; every simulation frame/source, floor clearance, visible camera snapshots. Staged reachable service approach, no autonomous chooser/save/roster or full continuous recording claim."},"\t"))
 print("KRUSHER_WORKSHOP checks=%d failures=%d captures=%d journeys=%d"%[checks,failures,records.size(),journeys.size()]);game.free();quit(1 if failures else 0)
