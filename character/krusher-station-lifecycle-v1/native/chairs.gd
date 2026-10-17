extends "res://tests/playtest_nursery_art.gd"
const PROGRESS="res://character/krusher-complete-animation-v1/progress.json"
const CELL=Vector2i(20,20)
var checks:=0
var records:Array=[]
func check(ok:bool,label:String)->void:
 checks+=1;expect(ok,label)
func pixels(texture:Texture2D)->PackedByteArray:
 return (texture.diffuse_texture if texture is CanvasTexture else texture).get_image().get_data()
func run()->void:
 var uid="res://character/krusher-station-lifecycle-v1/native/chairs.gd.uid"
 if not FileAccess.file_exists(uid):
  var uf=FileAccess.open(uid,FileAccess.WRITE);uf.store_string(ResourceUID.id_to_text(ResourceUID.create_id())+"\n")
 var room_id:String=OS.get_environment("KRUSHER_ROOM")
 check(room_id in ["crew_lounge","observation_room"],"Known room review")
 capture_dir=OS.get_environment("KRUSHER_CHAIR_OUTPUT")
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
 var player=preload("res://scripts/crew_sprite_player.gd").new();var progress:Dictionary=JSON.parse_string(FileAccess.get_file_as_string(PROGRESS))
 for path in progress.candidatePacks.bare:player.load_manifest(path,true)
 for path in progress.candidatePacks.helmet:check(player.load_equipment_manifest("diving-helmet",path),"paired admission")
 game.grid_view.branforth_player=player
 var actor=game.branforth_npc
 for peer in [game.bill_npc,game.veld_npc,game.marsh_npc]:peer.active=false
 if not game.hand_collapsed:game._toggle_hand_collapsed()
 var center:Vector2=(Vector2(CELL)+Vector2.ONE*.5)*384.0;var camera:Vector2=(Vector2(CELL)+Vector2.ONE*.5)/float(game.GRID_SIZE);var seen:Dictionary={}
 for quarter in range(4):
  game.occupied.clear();game.placed_rooms.clear();game.powered_room_cells.clear();game.unpowered_room_cells.clear();game.selected_rotation=quarter
  game._place_room(room_id,CELL,true);game.occupied[CELL].rotation=quarter;game.powered_room_cells[CELL]=true
  actor.signature="";await actor.rebuild(game);actor.active=true;actor.dead=false;actor.movement_medium="dry";actor.bunk_motion.clear();actor.console_motion.clear();actor.exterior_cancel.clear();actor.meal_return.clear()
  for need in actor.needs:actor.needs[need]=0.0
  var station:Dictionary={}
  for candidate in actor.RoomActivity.stations(actor.geometry[CELL]):
   if candidate.get("mode","") in ["sit","read"] and actor.can_stand(center+candidate.point):station=candidate;break
  check(not station.is_empty(),"Reachable actual furniture q"+str(quarter))
  if station.is_empty():continue
  actor.foot=center+station.point;actor.path.clear();actor.goal="fatigue" if room_id=="crew_lounge" else "curiosity";actor.goal_cell=CELL;actor.stage="";actor.arrive()
  check(actor.stage==("life_sit" if room_id=="crew_lounge" else "observation_sit"),"Production arrival selects sitting")
  var direction:String=actor.direction;seen[direction]=true
  game.selected_room_cell=CELL;game._refresh_all();game._set_grid_zoom(.8,true,camera)
  await settle()
  var settled:=false
  for attempt in range(120):
   game.camera_zoom_target=-1.0;game._restore_grid_view_center(camera);game.grid_view.queue_redraw()
   await process_frame;await RenderingServer.frame_post_draw
   if game.grid_view.pending_layers.is_empty() and not game.grid_view.zoom_settling and not game.grid_view.zoom_preparing and game._grid_view_center_ratio().distance_to(camera)<.002:settled=true;break
  check(settled,"Visible room/camera settled")
  if not settled:continue
  var stages:Array=["life_sit","life_seated","life_rise"] if room_id=="crew_lounge" else ["observation_sit","observation_read_enter","observation_read","observation_read_exit","observation_rise"]
  for gear in ["","diving-helmet"]:
   actor.helmet_equipped=not gear.is_empty()
   for phase in stages:
    actor.stage=phase;actor.state="idle";actor.timer=.8;actor.tablet_exit_pose=-1
    var action:String=actor.animation_state();var key:String=action+"-"+direction;var pool:Dictionary=player.frames if gear.is_empty() else player.equipment_frames[gear];var timing:Dictionary=player.timing if gear.is_empty() else player.equipment_timing[gear]
    check(pool.has(key),"Staged animation exists "+key)
    if not pool.has(key):continue
    var row:Array=pool[key];var cursor:=0.0
    player.current_key="";player.last_time=-1.0;player.last_position=Vector2.ZERO;player.motion.clear();game.visual_time_seconds=0.0
    if phase in ["life_seated","observation_read"]:player.frame(action,direction,0.0,actor.foot/384.0,gear)
    for i in range(row.size()):
     var hold:float=timing[key].durations[i]/1000.0;var elapsed:float=cursor+hold*.5;game.visual_time_seconds=elapsed
     if phase in ["life_sit","life_rise"]:actor.timer=.8-elapsed
     elif phase in ["observation_sit","observation_rise"]:actor.timer=.65-elapsed*.65/.8
     elif phase in ["observation_read_enter","observation_read_exit"]:actor.timer=.48-elapsed
     else:actor.timer=7.4-elapsed if phase=="life_seated" else 11.04-elapsed
     var texture:Texture2D=game.grid_view._get_branforth_frame_source(game);check(texture!=null,"Native sprite")
     check(pixels(texture)==pixels(row[i]),"Production grid pose source "+key+str(i))
     check(texture.get_meta("crew_standing_height")==148.0,"World ruler")
     var offset:Vector2=actor.observation_visual_offset();var factor:=1.0
     if phase in ["life_sit","observation_sit"]:factor=elapsed/.8
     elif phase in ["life_rise","observation_rise"]:factor=1.0-elapsed/.8
     var resolved:Dictionary=actor.RoomActivity.seated_contact(actor.geometry[CELL],station.point) if phase.begins_with("life_") else actor.RoomActivity.at(actor.geometry[CELL],station.point)
     var expected:Vector2=(Vector2(resolved.rest_point)-Vector2(station.point))*factor if resolved.has("rest_point") else Vector2.ZERO if phase.begins_with("life_") else Vector2(0,8.0*factor)
     check(offset.distance_to(expected)<.001,"Registered furniture transition offset")
     var name:String="q%d-%s-%s-%02d"%[quarter,"bare" if gear.is_empty() else "helmet",key,i]
     game._restore_grid_view_center(camera);await capture(name)
     check(game._grid_view_center_ratio().distance_to(camera)<.002,"Capture camera stays centered")
     var world_foot:Vector2=game.get_chief_branforth_position()+Vector2(0,game.get_cell_size()*.038)+offset*game.get_cell_size()/384.0
     var scale:float=game.get_cell_size()/384.0*65.28/148.0;var rect:Rect2=Rect2(world_foot-Vector2(texture.get_meta("crew_pivot"))*scale,texture.get_size()*scale)
     var screen:Rect2=root.get_stretch_transform()*game.grid_view.get_global_transform_with_canvas()*rect;var clip:Rect2=root.get_stretch_transform()*game.grid_scroll.get_global_rect()
     check(clip.encloses(screen),"Entire sprite canvas visible")
     room_pixels(CELL).save_png(capture_dir.path_join(name+"-room.png"));records.append({"file":name+"-room.png","room":room_id,"quarter":quarter,"gear":"bare" if gear.is_empty() else "helmet","stage":phase,"key":key,"pose":i,"elapsed":elapsed,"hold":hold,"foot":[actor.foot.x,actor.foot.y],"offset":[offset.x,offset.y],"hasRestPoint":resolved.has("rest_point"),"prop":resolved.get("prop",station.get("prop",""))});cursor+=hold
  # Production stage completion, including tablet enter/exit handoffs.
  actor.helmet_equipped=false;actor.state="idle";actor.stage="life_sit" if room_id=="crew_lounge" else "observation_sit";actor.timer=.8 if room_id=="crew_lounge" else .65
  actor.update(game,actor.timer+.00001);check(actor.stage==("life_seated" if room_id=="crew_lounge" else "observation_read_enter"),"Normal sitting update advances")
  if room_id=="observation_room":
   actor.update(game,.48001);check(actor.stage=="observation_read","Tablet enters reading")
   actor.update(game,11.04001);check(actor.stage=="observation_read_exit","Reading hands off to tablet exit")
   actor.update(game,.48001);check(actor.stage=="observation_rise","Tablet exit hands off to rising")
  else:
   actor.update(game,7.40001);check(actor.stage=="life_rise","Seated rest hands off to rising")
  actor.update(game,(.8 if room_id=="crew_lounge" else .65)+.00001);check(actor.stage.is_empty(),"Rising releases furniture activity")
 var f=FileAccess.open(capture_dir.path_join("report.json"),FileAccess.WRITE);f.store_string(JSON.stringify({"checks":checks,"failures":failures,"records":records,"facings":seen.keys(),"scope":"Merged Krusher candidates, reachable actual default furniture in four room rotations; production arrival and update sit/read/rise handoffs; all source slots, contact offsets and visible camera checks. Staged reachable approach, no autonomous path/normal Krusher roster/save integration; no continuous station playback claim."},"\t"))
 print("KRUSHER_CHAIRS room=%s checks=%d failures=%d captures=%d"%[room_id,checks,failures,records.size()]);game.free();quit(1 if failures else 0)
