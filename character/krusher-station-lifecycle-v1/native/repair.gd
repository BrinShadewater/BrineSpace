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
 var uid="res://character/krusher-station-lifecycle-v1/native/repair.gd.uid"
 if not FileAccess.file_exists(uid):
  var uf=FileAccess.open(uid,FileAccess.WRITE);uf.store_string(ResourceUID.id_to_text(ResourceUID.create_id())+"\n")
 var room_id:String="salvage_workshop"
 capture_dir=OS.get_environment("KRUSHER_REPAIR_OUTPUT")
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
 var center:Vector2=(Vector2(CELL)+Vector2.ONE*.5)*384.0;var camera:Vector2=(Vector2(CELL)+Vector2.ONE*.5)/float(game.GRID_SIZE);var cases:Array=[]
 game._place_room("storage_bay",CELL,true);game.powered_room_cells[CELL]=true
 actor.signature="";await actor.rebuild(game);actor.active=true;actor.dead=false
 var contacts:Dictionary={}
 for id in actor.room_nodes.get(CELL,[]):
  var point:Vector2=actor.graph.get_point_position(id);var facing:String=actor.equipment_facing(CELL,point-center)
  if not facing.is_empty() and not contacts.has(facing) and actor.can_stand(point):contacts[facing]=point
 print("KRUSHER_REPAIR contacts=",contacts.keys())
 game.selected_room_cell=CELL;game._refresh_all();game._set_grid_zoom(.8,true,camera);await settle()
 for attempt in range(120):
  game.camera_zoom_target=-1.0;game._restore_grid_view_center(camera);game.grid_view.queue_redraw();await process_frame;await RenderingServer.frame_post_draw
  if game.grid_view.pending_layers.is_empty() and not game.grid_view.zoom_settling and not game.grid_view.zoom_preparing and game._grid_view_center_ratio().distance_to(camera)<.002:break
 for direction in ["east","west","south","north"]:
  check(contacts.has(direction),"Real reachable equipment contact "+direction)
  if not contacts.has(direction):continue
  for gear in ["","diving-helmet"]:
   actor.foot=contacts[direction];actor.path.clear();actor.goal="maintenance";actor.goal_cell=CELL;actor.stage="";actor.state="idle";actor.timer=0;actor.helmet_equipped=not gear.is_empty();actor.preview_player=player;actor.movement_medium="dry";actor.expedition.clear();actor.bunk_motion.clear();actor.console_motion.clear();actor.exterior_cancel.clear();actor.meal_return.clear();actor.construction_motion.clear();actor.hull_return.clear();actor.hull_resume.clear()
   for need in actor.needs:actor.needs[need]=0.0
   actor.decision_rng=RandomNumberGenerator.new();actor.decision_rng.seed=9123
   player.return_plan.clear();player.current_key="";player.last_time=-1.0;player.last_position=Vector2.ZERO;player.motion.clear();game.visual_time_seconds=0.0;game.paused=false
   actor.arrive();check(actor.stage=="kneel" and actor.direction==direction,"Production maintenance arrival chooses equipment facing")
   var timeline:Array=[];var visited:Dictionary={};var previous:String="";var completed:=false;var contact:Vector2=actor.foot
   for tick in range(500):
    var action:String=actor.animation_state();var texture:Texture2D=game.grid_view._get_branforth_frame_source(game);var actual:Dictionary=player.last_source.duplicate(true);var bank:Dictionary=player.frames if gear.is_empty() else player.equipment_frames[gear]
    check(texture!=null and not actual.is_empty(),"Native maintenance source exists")
    if not actual.is_empty():check(bank.has(actual.key) and pixels(texture)==pixels(bank[actual.key][actual.index]),"Exact Krusher maintenance source selected")
    check(actor.foot==contact and actor.can_stand(actor.foot),"Repair floor contact stays registered and clear")
    visited[action]=true;timeline.append({"time":game.visual_time_seconds,"action":action,"direction":actor.direction,"foot":[actor.foot.x,actor.foot.y],"source":actual})
    if action!=previous or tick%30==0:await capture_repair(actor,texture,gear,direction+"-"+action+"-"+str(tick),camera)
    var stage_before:String=actor.stage;previous=action;game.visual_time_seconds+=1.0/60.0;actor.update(game,1.0/60.0)
    if stage_before=="stand" and actor.stage.is_empty():completed=true;await capture_repair(actor,game.grid_view._get_branforth_frame_source(game),gear,direction+"-complete",camera);break
   check(completed and actor.stage.is_empty() and actor.state=="idle","Maintenance stand stage finishes before normal successor task")
   check(visited.has("kneel") and visited.has("repair") and visited.has("stand"),"Kneel/repair/stand reached")
   cases.append({"gear":"bare" if gear.is_empty() else "helmet","direction":direction,"complete":completed,"successorGoal":actor.goal,"successorActivity":actor.activity,"successorStage":actor.stage,"contact":[contact.x,contact.y],"timeline":timeline})
 var f=FileAccess.open(capture_dir.path_join("report.json"),FileAccess.WRITE);f.store_string(JSON.stringify({"checks":checks,"failures":failures,"records":records,"cases":cases,"scope":"Krusher bank in production James actor/player; eight actual default storage-equipment contacts, staged actual arrival then full kneel/repair/stand/idle via ordinary maintenance controller, exact source every60Hz tick and native visible captures. Not autonomous chooser/approach, all full source-loop cycles, arbitrary interruptions or ordinary roster."},"\t"))
 print("KRUSHER_REPAIR checks=%d failures=%d captures=%d cases=%d"%[checks,failures,records.size(),cases.size()]);game.free();quit(1 if failures else 0)
func capture_repair(actor,texture:Texture2D,gear:String,label:String,camera:Vector2)->void:
 var name:String=("bare" if gear.is_empty() else "helmet")+"-"+label;game._restore_grid_view_center(camera);await capture(name)
 check(game._grid_view_center_ratio().distance_to(camera)<.002,"Repair camera centered")
 var at:Vector2=game.get_chief_branforth_position()+Vector2(0,game.get_cell_size()*.038);var scale:float=game.get_cell_size()/384.0*65.28/148.0;var screen:Rect2=root.get_stretch_transform()*game.grid_view.get_global_transform_with_canvas()*Rect2(at-Vector2(texture.get_meta("crew_pivot"))*scale,texture.get_size()*scale)
 check((root.get_stretch_transform()*game.grid_scroll.get_global_rect()).encloses(screen),"Entire repair sprite canvas visible")
 var foot_screen:Vector2=root.get_stretch_transform()*game.grid_view.get_global_transform_with_canvas()*at
 records.append({"file":name+".png","gear":"bare" if gear.is_empty() else "helmet","label":label,"action":actor.animation_state(),"direction":actor.direction,"foot":[actor.foot.x,actor.foot.y],"screenFoot":[foot_screen.x,foot_screen.y],"time":game.visual_time_seconds})
