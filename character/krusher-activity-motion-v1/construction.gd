extends "res://tests/playtest_nursery_art.gd"
const PROGRESS="res://character/krusher-animation-package-v11/package.json"
const CELL=Vector2i(20,20)
const Construction=preload("res://scripts/crew_construction.gd")
var checks:=0
var records:Array=[]
func check(ok:bool,label:String)->void:
 checks+=1;expect(ok,label)
func pixels(texture:Texture2D)->PackedByteArray:
 return (texture.diffuse_texture if texture is CanvasTexture else texture).get_image().get_data()
func run()->void:
 var uid="res://character/krusher-activity-motion-v1/construction.gd.uid"
 if not FileAccess.file_exists(uid):
  var uf=FileAccess.open(uid,FileAccess.WRITE);uf.store_string(ResourceUID.id_to_text(ResourceUID.create_id())+"\n")
 capture_dir=OS.get_environment("KRUSHER_CONSTRUCTION_OUTPUT")
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
 game.occupied.clear();game.placed_rooms.clear();game.powered_room_cells.clear();game.unpowered_room_cells.clear()
 game._place_room("brine_core",CELL,true,true)
 game.architect_run["selected"]="branforth"
 if game.architect_run.has("core"):game.architect_run.core["recovered"]=true
 var player=preload("res://scripts/james_cargo_player.gd").new();var progress:Dictionary=JSON.parse_string(FileAccess.get_file_as_string(PROGRESS))
 for path in progress.candidatePacks.bare:player.load_manifest(path,true)
 for path in progress.candidatePacks.helmet:check(player.load_equipment_manifest("diving-helmet",path),"paired admission")
 game.grid_view.branforth_player=player;player.game=game
 var actor=game.branforth_npc
 for peer in [game.bill_npc,game.veld_npc,game.marsh_npc]:peer.active=false
 game.recovered_crew=[{"architect_id":"bill","alive":true},{"architect_id":"branforth","alive":true}]
 if not game.hand_collapsed:game._toggle_hand_collapsed()
 var target:=Vector2i(20,19);var cases:Array=[];var initial_resources:Dictionary=game.resources.duplicate(true);var camera:Vector2=(Vector2(CELL)+Vector2.ONE*.5)/float(game.GRID_SIZE)
 for gear in ["","diving-helmet"]:
  game.occupied.erase(target);game.placed_rooms=game.placed_rooms.filter(func(room):return room.pos!=target);game.drone_fleet.orders.clear();game.drone_fleet.sites.erase(target);game.wrecks.erase(target);game.resources=initial_resources.duplicate(true)
  for cell in game.occupied:game.powered_room_cells[cell]=true
  actor.signature="";await actor.rebuild(game);actor.active=true;actor.dead=false;actor.movement_medium="dry";actor.helmet_equipped=not gear.is_empty();actor.stage="";actor.state="idle";actor.goal="";actor.timer=0;actor.path.clear();actor.construction_motion.clear();actor.hull_return.clear();actor.hull_resume.clear();actor.exterior_cancel.clear();actor.preview_player=player
  for need in actor.needs:actor.needs[need]=0.0
  var node:int=actor.nearest_in_room((Vector2(CELL)+Vector2.ONE*.5)*384,CELL,false)
  print("KRUSHER_CORE nodes=%d center_clear=%s chosen=%d"%[actor.room_nodes.get(CELL,[]).size(),actor.can_stand((Vector2(CELL)+Vector2.ONE*.5)*384),node])
  check(node>=0,"Reachable real core floor")
  if node<0:continue
  actor.foot=actor.graph.get_point_position(node);actor.decision_rng=RandomNumberGenerator.new();actor.decision_rng.seed=8244
  game.running=true;game.paused=false;game.hardware.power=true;game.hardware.doors=false
  game.hand.assign(["life_support"]);game._on_card_pressed("life_support")
  var rotation:=-1
  for q in range(4):
   game.selected_rotation=q
   if game.get_placement_problem("life_support",target).is_empty():rotation=q;break
  check(rotation>=0,"Actual blueprint has a valid connected placement")
  if rotation<0:continue
  var metal_before:int=game.resources.metal;game._on_grid_clicked(target)
  check(game.resources.metal<metal_before and game.drone_fleet.reserved(target) and not game.occupied.has(target),"Normal build spends Metal and queues unfinished room")
  var order:Dictionary={}
  for unused in range(3000):
   game.visual_time_seconds+=1.0/60.0;Construction.advance(game,actor,1.0/60.0)
   if actor.state=="weld":
    for item in game.drone_fleet.orders:
     if item.get("builder","")=="branforth":order=item;break
    break
  check(not order.is_empty(),"Production builder reaches sealed work connection")
  if order.is_empty():continue
  check(actor.foot.distance_to(order.work_point)<1.01 and actor.can_stand(actor.foot),"Registered actual work contact")
  game.selected_card_id="";game.selected_room_cell=CELL;game._refresh_all();game._set_grid_zoom(.8,true,camera);await settle()
  for attempt in range(120):
   game.camera_zoom_target=-1.0;game._restore_grid_view_center(camera);await process_frame
   if game._grid_view_center_ratio().distance_to(camera)<.002:break
  var timeline:Array=[];var previous:String="";var interrupted:=false;var completed:=false;var seen:Dictionary={}
  for step in range(1000):
   var action:String=actor.animation_state();var texture:Texture2D=game.grid_view._get_branforth_frame_source(game);var key:String=action+"-"+actor.direction
   check(texture!=null,"Actual torch sprite")
   check(actor.foot.distance_to(order.work_point)<1.01,"Work stays at physical connection")
   seen[action]=true;timeline.append({"time":game.visual_time_seconds,"action":action,"work":order.work,"direction":actor.direction,"foot":[actor.foot.x,actor.foot.y]})
   if action!=previous or step%6==0:await capture_work(actor,texture,gear,"job-"+str(step),camera)
   if not interrupted and float(order.work)>=3.0:
    interrupted=true;var held:PackedByteArray=pixels(texture);var held_work:float=order.work;var held_foot:Vector2=actor.foot
    game.hardware.power=false;Construction.advance(game,actor,0.0)
    check(not actor.construction_motion.is_empty(),"Power loss creates authored torch retraction")
    check(pixels(game.grid_view._get_branforth_frame_source(game))==held,"Interruption holds exact current visible source")
    for unused in range(200):
     game.visual_time_seconds+=1.0/60.0;Construction.advance(game,actor,1.0/60.0)
     var transition_texture:Texture2D=game.grid_view._get_branforth_frame_source(game)
     var transition_pixels:PackedByteArray=pixels(transition_texture)
     if transition_pixels!=get_meta("transition_pixels",PackedByteArray()):
      await capture_work(actor,transition_texture,gear,"transition-"+str(step)+"-"+str(game.visual_time_seconds),camera)
      set_meta("transition_pixels",transition_pixels)
     check(float(order.work)==held_work and actor.foot==held_foot,"Blocked torch motion preserves paid progress/contact")
     if actor.construction_motion.get("phase","")=="hold":break
    check(actor.construction_motion.get("phase","")=="hold","Torch reaches empty idle hold")
    await capture_work(actor,game.grid_view._get_branforth_frame_source(game),gear,"power-held",camera)
    var stopped:PackedByteArray=pixels(game.grid_view._get_branforth_frame_source(game));game.paused=true;Construction.advance(game,actor,1.0)
    check(float(order.work)==held_work and pixels(game.grid_view._get_branforth_frame_source(game))==stopped,"Pause holds paid work and idle pose")
    game.paused=false;game.hardware.power=true
    for unused in range(200):
     game.visual_time_seconds+=1.0/60.0;Construction.advance(game,actor,1.0/60.0)
     var transition_texture:Texture2D=game.grid_view._get_branforth_frame_source(game)
     var transition_pixels:PackedByteArray=pixels(transition_texture)
     if transition_pixels!=get_meta("transition_pixels",PackedByteArray()):
      await capture_work(actor,transition_texture,gear,"transition-"+str(step)+"-"+str(game.visual_time_seconds),camera)
      set_meta("transition_pixels",transition_pixels)
     if actor.construction_motion.is_empty():break
    check(actor.construction_motion.is_empty() and actor.state=="weld","Power restoration returns to work")
    check(float(order.work)>=held_work and float(order.work)-held_work<.04,"Return preserves paid work without jumping progress")
    check(pixels(game.grid_view._get_branforth_frame_source(game))==held,"Resumed torch restores exact held source pose")
    await capture_work(actor,game.grid_view._get_branforth_frame_source(game),gear,"power-resumed",camera)
   previous=action
   game.visual_time_seconds+=1.0/60.0;Construction.advance(game,actor,1.0/60.0)
   if game.occupied.has(target):completed=true;break
  check(completed and game.drone_fleet.orders.is_empty(),"Normal finite paid build completes and releases order")
  check(seen.has("torch-draw") and seen.has("weld") and seen.has("torch-stow"),"Production draw/weld/stow all exercised")
  cases.append({"gear":"bare" if gear.is_empty() else "helmet","direction":actor.direction,"metalBefore":metal_before,"metalAfter":game.resources.metal,"interrupted":interrupted,"complete":completed,"workPoint":[order.work_point.x,order.work_point.y],"timeline":timeline})
 var f=FileAccess.open(capture_dir.path_join("report.json"),FileAccess.WRITE);f.store_string(JSON.stringify({"checks":checks,"failures":failures,"records":records,"cases":cases,"scope":"Two ordinary paid life-support builds at real core connection through production chooser/route/work controller, full draw/weld/stow progression, power-off stow/hold/resume and pause, registered work contact/native snapshots. Krusher manifests in existing James cargo player/actor; no roster/save or continuous station recording claim."},"\t"))
 print("KRUSHER_CONSTRUCTION checks=%d failures=%d captures=%d cases=%d"%[checks,failures,records.size(),cases.size()]);game.free();quit(1 if failures else 0)
func capture_work(actor,texture:Texture2D,gear:String,label:String,camera:Vector2)->void:
 var name:String=("bare" if gear.is_empty() else "helmet")+"-"+label;game._restore_grid_view_center(camera);game.grid_view.queue_redraw();await process_frame;await RenderingServer.frame_post_draw
 check(game._grid_view_center_ratio().distance_to(camera)<.002,"Work camera centered")
 var at:Vector2=game.get_chief_branforth_position()+Vector2(0,game.get_cell_size()*.038);var scale:float=game.get_cell_size()/384.0*65.28/148.0;var screen:Rect2=root.get_stretch_transform()*game.grid_view.get_global_transform_with_canvas()*Rect2(at-Vector2(texture.get_meta("crew_pivot"))*scale,texture.get_size()*scale)
 check((root.get_stretch_transform()*game.grid_scroll.get_global_rect()).encloses(screen),"Entire torch sprite canvas visible")
 var foot_screen:Vector2=root.get_stretch_transform()*game.grid_view.get_global_transform_with_canvas()*at
 var image:Image=root.get_texture().get_image();var crop:Rect2i=Rect2i(screen.grow(7).intersection(Rect2(Vector2.ZERO,image.get_size())))
 image.get_region(crop).save_png(capture_dir.path_join(name+".png"))
 var context_key:String="context-"+("bare" if gear.is_empty() else "helmet")+"-"+actor.direction+"-"+actor.animation_state()
 context_key=context_key.replace("-","_")
 if not has_meta(context_key):image.save_png(capture_dir.path_join(name+"-full.png"));set_meta(context_key,true)
 records.append({"crop":[crop.position.x,crop.position.y,crop.size.x,crop.size.y],"source":game.grid_view.branforth_player.last_source.duplicate(true),"screen":[screen.position.x,screen.position.y,screen.size.x,screen.size.y],"file":name+".png","gear":"bare" if gear.is_empty() else "helmet","label":label,"action":actor.animation_state(),"direction":actor.direction,"foot":[actor.foot.x,actor.foot.y],"screenFoot":[foot_screen.x,foot_screen.y],"time":game.visual_time_seconds,"work":actor.timer})
