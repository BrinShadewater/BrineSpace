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
 var uid="res://character/krusher-station-lifecycle-v2/native/west.gd.uid"
 if not FileAccess.file_exists(uid):
  var uf=FileAccess.open(uid,FileAccess.WRITE);uf.store_string(ResourceUID.id_to_text(ResourceUID.create_id())+"\n")
 var room_id:String="salvage_workshop"
 capture_dir=OS.get_environment("KRUSHER_WEST_OUTPUT")
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
 var original_player=game.grid_view.branforth_player
 for original_gear in ["","diving-helmet"]:check(preload("res://character/james-floor-case-west-v1/checkpoint_floor_state_v2.gd").cue_available(original_player,original_gear),"Original James cue remains admitted")
 var player=preload("res://scripts/james_cargo_player.gd").new();var progress:Dictionary=JSON.parse_string(FileAccess.get_file_as_string(PROGRESS))
 for path in progress.candidatePacks.bare:player.load_manifest(path,true)
 for path in progress.candidatePacks.helmet:check(player.load_equipment_manifest("diving-helmet",path),"paired admission")
 game.grid_view.branforth_player=player;player.game=game
 var actor=game.branforth_npc
 for peer in [game.bill_npc,game.veld_npc,game.marsh_npc]:peer.active=false
 game.drone_fleet.orders.clear()
 if not game.hand_collapsed:game._toggle_hand_collapsed()
 var center:Vector2=(Vector2(CELL)+Vector2.ONE*.5)*384.0;var camera:Vector2=(Vector2(CELL)+Vector2.ONE*.5)/float(game.GRID_SIZE);var journeys:Array=[]
 game._place_room(room_id,CELL,true);game.powered_room_cells[CELL]=true
 actor.signature="";await actor.rebuild(game);actor.active=true;actor.dead=false;actor.movement_medium="dry"
 game.selected_room_cell=CELL;game._refresh_all();game._set_grid_zoom(.8,true,camera);await settle()
 for attempt in range(120):
  game.camera_zoom_target=-1.0;game._restore_grid_view_center(camera);game.grid_view.queue_redraw();await process_frame;await RenderingServer.frame_post_draw
  if game.grid_view.pending_layers.is_empty() and not game.grid_view.zoom_settling and not game.grid_view.zoom_preparing and game._grid_view_center_ratio().distance_to(camera)<.002:break
 var floor=preload("res://character/james-floor-case-west-v1/checkpoint_floor_state_v2.gd")
 for gear in ["","diving-helmet"]:
  var bank:Dictionary=player.bank_for(gear);check(floor.cue_available(player,gear),"Exact Krusher cue admitted")
  var cue:Texture2D=bank["unload-west"][4];var bad_image:Image=cue.get_image().duplicate();bad_image.set_pixel(0,0,Color.RED);bank["unload-west"][4]=ImageTexture.create_from_image(bad_image)
  check(not floor.cue_available(player,gear),"Altered cue rejected");bank["unload-west"][4]=cue
  for index in range(7):
   game.powered_room_cells[CELL]=true;game.unpowered_room_cells.erase(CELL);game.occupied[CELL].erase(floor.FIELD)
   actor.active=true;actor.dead=false;actor.path.clear();actor.goal="curiosity";actor.goal_cell=CELL;actor.stage="workshop_unload";actor.state="idle";actor.helmet_equipped=not gear.is_empty();actor.direction="west";actor.preview_player=player;actor.expedition.clear();actor.exterior_cancel.clear();actor.bunk_motion.clear();actor.console_motion.clear();actor.meal_return.clear();actor.construction_motion.clear();actor.hull_return.clear();actor.hull_resume.clear()
   for need in actor.needs:actor.needs[need]=0.0
   var extent:Rect2=Rect2();var first:=true
   for key in ["unload-west","carry-settle-west"]:
    for tex in bank[key]:
     var e:Rect2=tex.get_meta("crew_alpha_extent");extent=e if first else extent.merge(e);first=false
   var best:Vector2=Vector2.INF;var distance:float=INF
   for node in actor.room_nodes.get(CELL,[]):
    var at:Vector2=actor.graph.get_point_position(node)
    if not actor.can_stand(at) or not actor.swim_segment_clear(at,at,"west","west",false,[extent.position.x,extent.position.y,extent.end.x,extent.end.y]):continue
    if at.distance_squared_to(center)<distance:best=at;distance=at.distance_squared_to(center)
   check(best!=Vector2.INF,"Clear actual floor envelope exists")
   if best==Vector2.INF:continue
   actor.foot=best;var origin:Vector2=best
   var clocks:Dictionary=player.timing if gear.is_empty() else player.equipment_timing[gear]
   var elapsed:=0.0
   for j in range(index):elapsed+=float(clocks["unload-west"].durations[j])/1000.0
   elapsed+=float(clocks["unload-west"].durations[index])*.0005;actor.timer=2.0-elapsed
   player.return_plan.clear();player.motion.clear();player.current_key="";player.last_time=-1;player.last_position=Vector2.ZERO;game.visual_time_seconds=10.0;game.paused=false
   var initial:Texture2D=game.grid_view._get_branforth_frame_source(game)
   check(pixels(initial)==pixels(bank["unload-west"][index]),"Actual renderer selects staged West source index")
   # Ordinary controller owns the floor case once the release cue has passed.
   actor.update(game,.000001)
   var already:bool=game.occupied[CELL].has(floor.FIELD);check(already==(index>=4),"Ordinary release matches original source cue")
   await shot(actor,gear,"index%d-before"%index,camera)
   game.powered_room_cells.erase(CELL);game.unpowered_room_cells[CELL]=true
   actor.update(game,.000001)
   records.append({"diagnostic":true,"gear":gear,"index":index,"stage":actor.stage,"goal":actor.goal,"service":actor.service_available(game,CELL),"reason":actor.return_reason,"source":player.last_source.duplicate(true),"geometry":str(actor.return_geometry)})
   var plan:Dictionary=player.return_plan.duplicate(true);check(not plan.is_empty(),"Service loss starts source-bound return")
   if plan.is_empty():continue
   check(plan.source=="unload-west" and plan.sourceIndex==index,"Return starts from actual displayed source")
   check(pixels(game.grid_view._get_branforth_frame_source(game))==pixels(initial),"Exact interrupted entrance")
   var seen:=[];var placed:=already
   var clock:float=plan.started
   for row in plan.rows:
    game.visual_time_seconds=clock+float(row.seconds)*.5;actor.update(game,.000001)
    var texture:Texture2D=game.grid_view._get_branforth_frame_source(game)
    check(pixels(texture)==pixels(bank[row.key][row.index]),"Every return source row exact")
    check(actor.foot==origin and actor.can_stand(actor.foot),"Fixed registered physical foot")
    var owned:bool=game.occupied[CELL].has(floor.FIELD);placed=placed or owned
    if owned:check(game.occupied[CELL][floor.FIELD].anchor==origin-center,"Floor case anchor stays registered")
    await shot(actor,gear,"index%d-return-%02d"%[index,seen.size()],camera)
    seen.append({"key":row.key,"index":row.index,"floorCase":owned});clock+=float(row.seconds)
   check(placed,"Actual rendered return leaves floor case")
   game.visual_time_seconds=plan.until+.00001;actor.update(game,.000001)
   check(player.return_plan.is_empty(),"Finite return completes")
   check(game.occupied[CELL].has(floor.FIELD),"Released case persists through completion")
   await shot(actor,gear,"index%d-complete"%index,camera)
   journeys.append({"gear":"bare" if gear.is_empty() else "helmet","index":index,"alreadyReleased":already,"placed":placed,"rows":seen,"foot":[origin.x,origin.y]})
 var f=FileAccess.open(capture_dir.path_join("report.json"),FileAccess.WRITE);f.store_string(JSON.stringify({"checks":checks,"failures":failures,"records":records,"cases":journeys,"scope":"Actual workshop clear floor, staged West unload source at seven indices/both gears, ordinary release and actual service-loss return controller/source rows/fixed foot/persistent case. Original James cue and altered cue guard. No autonomous chooser or fresh-scene Continue claim."},"\t"))
 print("KRUSHER_WEST checks=%d failures=%d cases=%d captures=%d"%[checks,failures,journeys.size(),records.size()]);game.free();quit(1 if failures else 0)
func shot(actor,gear:String,label:String,camera:Vector2)->void:
 var name:String=("bare" if gear.is_empty() else "helmet")+"-"+label;game._restore_grid_view_center(camera);await capture(name)
 check(game._grid_view_center_ratio().distance_to(camera)<.002,"West camera centered")
 room_pixels(CELL).save_png(capture_dir.path_join(name+"-room.png"));records.append({"file":name+"-room.png","gear":"bare" if gear.is_empty() else "helmet","label":label,"source":game.grid_view.branforth_player.last_source.duplicate(true),"floorCase":game.occupied[CELL].has(preload("res://character/james-floor-case-west-v1/checkpoint_floor_state_v2.gd").FIELD)})
