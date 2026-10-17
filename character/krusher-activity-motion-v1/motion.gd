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
 var uid="res://character/krusher-activity-motion-v1/motion.gd.uid"
 if not FileAccess.file_exists(uid):
  var uf=FileAccess.open(uid,FileAccess.WRITE);uf.store_string(ResourceUID.id_to_text(ResourceUID.create_id())+"\n")
 capture_dir="res://character/krusher-activity-motion-v1/review-v2"
 DirAccess.make_dir_recursive_absolute(capture_dir)
 var store=preload("res://scripts/room_layout_store.gd");store.loaded=true;store.data={}
 root.size=Vector2i(1600,900)
 game=MainScene.instantiate();game.set_meta("authored_site_fixture",true)
 game.meta.save_path="user://krusher-lifecycle-meta.json";game.run_save_path="user://krusher-lifecycle-run.json";game.Preferences.save_path="user://krusher-lifecycle-settings.cfg"
 game.meta.unlocked_architect_ids={"bill":true,"branforth":true};game.meta.selected_architect="branforth"
 root.add_child(game);current_scene=game
 print("ACTIVITY setup scene added")
 while not game.startup_complete:await process_frame
 game.set_process(false);game.crew_comms.set_process(false);game.tick_timer.stop();game.paused=true
 game.set_process_input(false);game.set_process_unhandled_input(false);game.set_process_unhandled_key_input(false);root.gui_disable_input=true
 print("ACTIVITY startup complete")
 game.Architects.advance_core(game,10)
 game.recovered_crew=[{"architect_id":"bill","alive":true},{"architect_id":"branforth","alive":true}]
 var player=preload("res://scripts/james_cargo_player.gd").new();player.game=game
 var progress:Dictionary=JSON.parse_string(FileAccess.get_file_as_string(PROGRESS))
 for path in progress.candidatePacks.bare:player.load_manifest(path,true)
 for path in progress.candidatePacks.helmet:check(player.load_equipment_manifest("diving-helmet",path),"paired candidate admission")
 print("ACTIVITY candidate loaded")
 game.grid_view.branforth_player=player
 var actor=game.branforth_npc
 for peer in [game.bill_npc,game.veld_npc,game.marsh_npc]:peer.active=false
 game.drone_fleet.orders.clear()
 if not game.hand_collapsed:game._toggle_hand_collapsed()
 var center:Vector2=(Vector2(HAB)+Vector2.ONE*.5)*384.0
 var camera:Vector2=(Vector2(HAB)+Vector2.ONE*.5)/float(game.GRID_SIZE)
 var episodes:Array=[]
 for room_id in ["crew_lounge","observation_room","salvage_workshop"]:
  for quarter in range(4):
   game.occupied.clear();game.placed_rooms.clear();game.wrecks.clear();game.powered_room_cells.clear();game.unpowered_room_cells.clear()
   game._place_room(room_id,HAB,true);game.occupied[HAB].rotation=quarter;game.powered_room_cells[HAB]=true
   print("ACTIVITY room placed "+room_id+" "+str(quarter))
   actor.signature="";await actor.rebuild(game);actor.active=true
   print("ACTIVITY geometry rebuilt")
   var stations:Array=actor.RoomActivity.stations(actor.geometry[HAB]);var station:Dictionary={}
   for item in stations:
    if room_id=="salvage_workshop" or item.get("mode","")==("sit" if room_id=="crew_lounge" else "read"):station=item;break
   check(not station.is_empty(),room_id+" has an authored activity station")
   if station.is_empty():continue
   game.selected_room_cell=HAB;game._refresh_all();game._set_grid_zoom(.9,true,camera);await settle()
   print("ACTIVITY room settled")
   for attempt in range(120):
    game.camera_zoom_target=-1;game._restore_grid_view_center(camera);game.grid_view.queue_redraw();await process_frame
    if game.grid_view.pending_layers.is_empty() and not game.grid_view.zoom_settling and not game.grid_view.zoom_preparing and game._grid_view_center_ratio().distance_to(camera)<.002:break
   for gear in ["bare","helmet"]:
    actor.foot=center+Vector2(station.point);actor.path.clear();actor.goal="fatigue" if room_id=="crew_lounge" else "curiosity";actor.goal_cell=HAB;actor.stage="";actor.state="idle";actor.timer=0;actor.dead=false;actor.movement_medium="dry"
    actor.bunk_motion.clear();actor.console_motion.clear();actor.expedition.clear();actor.construction_motion.clear();actor.hull_return.clear();actor.hull_resume.clear();actor.meal_return.clear();actor.helmet_equipped=gear=="helmet";actor.preview_player=player;actor.tank_oxygen=100;actor.breath_oxygen=100;actor.air_recovery=0
    for need in actor.needs:actor.needs[need]=0.0
    player.current_key="";player.last_time=-1;player.motion.clear();player.return_plan.clear()
    actor.arrive()
    var label:String="%s-q%d-%s"%[room_id,quarter,gear];var elapsed:=0.0;var previous:String="";var previous_foot:=Vector2.INF;var stages:Array=[];var seen:Dictionary={};var count:=0;var last_action="";var complete:=false
    for tick in range(1800):
     game.visual_time_seconds=elapsed
     var texture:Texture2D=game.grid_view._get_branforth_frame_source(game)
     check(texture!=null,"Actual activity source exists")
     if texture==null:break
     var action:String=actor.animation_state();var stage:String=actor.stage;var source:Dictionary=player.last_source.duplicate(true);var hash:String=digest(pixels(texture))
     var at:Vector2=actor.foot+actor.observation_visual_offset()
     if not stage in stages:stages.append(stage)
     if not source.is_empty():
      var bank:Dictionary=player.frames if gear=="bare" else player.equipment_frames["diving-helmet"]
      check(bank.has(source.key) and pixels(texture)==pixels(bank[source.key][source.index]),"Production selected source pixels exact")
      seen[str(source.key)]=true
     var capture_now:bool=hash!=previous or at.distance_to(previous_foot)>.75 or action!=last_action
     if capture_now:
      game._restore_grid_view_center(camera);game.grid_view.queue_redraw();await process_frame;await RenderingServer.frame_post_draw
      var world_foot:Vector2=game.get_chief_branforth_position()+Vector2(0,game.get_cell_size()*.038)+actor.observation_visual_offset()*game.get_cell_size()/384.0
      var scale:float=game.get_cell_size()/384.0*65.28/148.0
      var screen:Rect2=root.get_stretch_transform()*game.grid_view.get_global_transform_with_canvas()*Rect2(world_foot-Vector2(texture.get_meta("crew_pivot"))*scale,texture.get_size()*scale)
      var clip:Rect2=root.get_stretch_transform()*game.grid_scroll.get_global_rect()
      check(clip.encloses(screen),"Entire activity source canvas visible")
      check(game._grid_view_center_ratio().distance_to(camera)<.002,"Activity camera remains centered")
      var image:Image=root.get_texture().get_image();var name:String="%s-%04d.png"%[label,count]
      var rect:Rect2i=Rect2i(screen.grow(7).intersection(Rect2(Vector2.ZERO,image.get_size())))
      image.get_region(rect).save_png(capture_dir.path_join(name))
      if count==0 or action!=last_action:image.save_png(capture_dir.path_join("%s-%04d-full.png"%[label,count]))
      records.append({"file":name,"episode":label,"time":elapsed,"tick":tick,"action":action,"stage":stage,"direction":actor.direction,"source":source,"sourceHash":hash,"screen":[screen.position.x,screen.position.y,screen.size.x,screen.size.y],"crop":[rect.position.x,rect.position.y,rect.size.x,rect.size.y],"foot":[actor.foot.x,actor.foot.y],"visualOffset":[actor.observation_visual_offset().x,actor.observation_visual_offset().y]})
      previous=hash;previous_foot=at;last_action=action;count+=1
     if stage.is_empty() and tick>2:complete=true;break
     actor.update(game,1.0/30.0);elapsed+=1.0/30.0
    check(complete,label+" completes the actual finite activity lifecycle")
    var required:Array=["life_sit","life_seated","life_rise"] if room_id=="crew_lounge" else ["observation_sit","observation_read_enter","observation_read","observation_read_exit","observation_rise"] if room_id=="observation_room" else ["workshop_inspect","workshop_work","workshop_pickup","workshop_carry","workshop_unload"]
    for stage in required:check(stage in stages,label+" reaches "+stage)
    episodes.append({"label":label,"room":room_id,"rotation":quarter,"gear":gear,"stationFacing":station.facing,"stages":stages,"sources":seen.keys(),"captures":count,"duration":elapsed,"complete":complete})
    print("ACTIVITY "+label+" captures="+str(count)+" complete="+str(complete))
 var f=FileAccess.open(capture_dir.path_join("report.json"),FileAccess.WRITE);f.store_string(JSON.stringify({"checks":checks,"failures":failures,"episodes":episodes,"records":records,"scope":"Staged actual authored room contacts; production arrive/update/render through sit/read/workshop/cargo lifecycles, both gears and four room rotations. Source/offset changes captured while simulation advances at30Hz. Not autonomous dispatch, continuous wall-clock video, all directional source coverage, normal roster integration or fresh Continue."},"\t"))
 print("KRUSHER_ACTIVITIES checks=%d failures=%d episodes=%d captures=%d"%[checks,failures,episodes.size(),records.size()]);game.free();quit(1 if failures else 0)
