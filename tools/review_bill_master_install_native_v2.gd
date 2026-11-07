extends SceneTree
const Loading=preload("res://scripts/loading_transition.gd")
const OUT="res://output/bill-master-install-native-v2/"
const CELL=Vector2i(20,21)
var game
var checks:=0
var failures:=0
var captures:Array=[]
var samples:Array=[]
var contact_findings:Array=[]
func _init():call_deferred("run")
func check(ok:bool,message:String):
 checks+=1
 if not ok:failures+=1;push_error(message)
func same(a:Texture2D,b:Texture2D)->bool:
 return a!=null and b!=null and a.get_image().get_data()==b.get_image().get_data()
func sole(texture:Texture2D)->Vector2:
 var im=texture.get_image();var bottom=-1;var total=0.0;var count=0
 for y in range(im.get_height()):
  for x in range(im.get_width()):
   if im.get_pixel(x,y).a>.5:
    if y>bottom:bottom=y;total=0;count=0
    if y==bottom:total+=x;count+=1
 return Vector2(total/maxi(1,count),bottom+1)
func occupied_height(texture:Texture2D)->int:
 var im=texture.get_image();var top=im.get_height();var bottom=-1
 for y in range(im.get_height()):
  for x in range(im.get_width()):
   if im.get_pixel(x,y).a>.5:top=mini(top,y);bottom=maxi(bottom,y)
 return bottom-top+1
func capture(label:String,texture:Texture2D,key:String,slot:int,variant:String):
 var ready=false
 for attempt in range(90):
  game.grid_view.queue_redraw();await process_frame;await RenderingServer.frame_post_draw
  if game.grid_view.content_canvases.has(game.bill_npc.cell_at(game.bill_npc.foot)):
   var canvas=game.grid_view.content_canvases[game.bill_npc.cell_at(game.bill_npc.foot)]
   for child in canvas.slots:
    if child.visible and child.item.get("kind","")=="actor" and same(canvas.renderer.external_actor_texture,texture):ready=true
  if ready:break
 check(ready,"actual retained Bill actor slot submits requested source")
 var n=captures.size();var world="world-%03d.png"%n;var source="source-%03d.png"%n
 check(root.get_texture().get_image().save_png(OUT+world)==OK,"actual station screenshot saved")
 check(texture.get_image().save_png(OUT+source)==OK,"actual submitted RGBA saved")
 captures.append({"label":label,"key":key,"slot":slot,"variant":variant,"worldFile":world,"sourceFile":source,"foot":[game.bill_npc.foot.x,game.bill_npc.foot.y]})
func run():
 if DisplayServer.get_name()=="headless":quit(2);return
 check(OS.get_user_data_dir().replace("\\","/").begins_with(OS.get_environment("APPDATA").replace("\\","/")+"/"),"scratch APPDATA active")
 DirAccess.make_dir_recursive_absolute(OUT);root.size=Vector2i(1600,900)
 preload("res://scripts/title_settings.gd").reduced_motion=true
 var store=preload("res://scripts/room_layout_store.gd");store.loaded=true;store.data={}
 game=load("res://scenes/main.tscn").instantiate();game.set_meta("authored_site_fixture",true)
 game.meta.save_path="user://bill_master_world.meta";game.run_save_path="user://bill_master_world.loop"
 game.meta.unlocked_architect_ids={"bill":true};game.meta.selected_architect="bill"
 root.add_child(game);current_scene=game
 var deadline=Time.get_ticks_msec()+120000
 while not game.startup_complete and Time.get_ticks_msec()<deadline:await process_frame
 check(game.startup_complete,"observable normal main startup")
 if not game.startup_complete:quit(1);return
 game.set_process(false);game.tick_timer.stop();game.crew_comms.set_process(false);game.crew_comms.dismiss()
 var overlay=null
 for child in root.get_children():
  if child.get_script()==Loading:overlay=child;break
 if overlay!=null:
  deadline=Time.get_ticks_msec()+20000
  while overlay.continue_button.disabled and Time.get_ticks_msec()<deadline:await process_frame
  check(not overlay.continue_button.disabled,"loading Continue available");overlay.continue_button.pressed.emit()
  while is_instance_valid(overlay) and Time.get_ticks_msec()<deadline:await process_frame
  check(not is_instance_valid(overlay),"loading overlay actually gone")
 game._confirm_doctrines();game.tick_timer.stop();game.set_process(false)
 check(game.running and not game.testing_free_build and not game.testing_disable_failures,"normal paid and failure flags")
 game.paused=false;game.Architects.advance_core(game,10);game.paused=true
 check(not game.occupied.has(CELL) and not game.wrecks.has(CELL),"prescribed station site unoccupied")
 game._place_room("cold_store",CELL,true);game.powered_room_cells[CELL]=true
 var actor=game.bill_npc;actor.signature="";await actor.rebuild(game)
 actor.active=true;actor.dead=false;actor.helmet_equipped=false;actor.movement_medium="dry";actor.state="idle";actor.direction="east";actor.stage="";actor.goal="";actor.path.clear();actor.expedition.clear();actor.timer=10
 actor.needs={"hunger":0.0,"fatigue":0.0,"curiosity":0.0,"maintenance":0.0}
 for peer in [game.veld_npc,game.branforth_npc,game.marsh_npc]:peer.active=false
 var start=Vector2.INF
 for id in actor.room_nodes.get(CELL,[]):
  var point:Vector2=actor.graph.get_point_position(id)
  if actor.can_stand(point):start=point;break
 check(start.is_finite(),"actual room graph has standing contact")
 if not start.is_finite():quit(1);return
 actor.foot=start;game.selected_room_cell=CELL;game._refresh_all();game.hand_panel.hide()
 var camera=(Vector2(CELL)+Vector2.ONE*.5)/float(game.GRID_SIZE);game._set_grid_zoom(2.0,true,camera)
 var settled=false
 for attempt in range(180):
  await process_frame;await RenderingServer.frame_post_draw;game._restore_grid_view_center(camera)
  if game.grid_view.pending_layers.is_empty() and not game.grid_view.zoom_settling and not game.grid_view.zoom_preparing and game._grid_view_center_ratio().distance_to(camera)<.002:settled=true;break
 check(settled,"observable camera and room layers settled")
 var grid=game.grid_view;var player=grid.human_water_player
 var bank_script=preload("res://scripts/bill_carry_player.gd");var Save=preload("res://scripts/run_save.gd")
 check(player.carry_binding()==bank_script.MASTER_BINDING,"normal loader selects reviewed master family")
 var selected_slots=0
 for path in bank_script.MASTER_BANKS:
  var manifest:Dictionary=JSON.parse_string(FileAccess.get_file_as_string(path))
  for state in manifest.states:
   var row:Array=player.frames[state.id]
   check(row.size()==state.frameFiles.size(),"normal complete selected source row")
   for i in range(row.size()):
    var im=Image.load_from_file(str(state.frameFiles[i]))
    check(row[i].get_image().get_data()==im.get_data(),"normal selected source exact RGBA")
    selected_slots+=1
 var outside={}
 for key in player.frames:
  if key not in bank_script.SOURCE_KEYS:outside[key]=player.frames[key].duplicate()
 for binding in bank_script.SOURCE_BINDINGS:
  check(player.complete_bank(binding) and player.select_binding(binding),"all current and legacy source versions complete")
  for key in outside:check(player.frames[key]==outside[key],"unrelated selected source stays exact")
 check(player.select_binding(bank_script.MASTER_BINDING),"return to master source version")
 for key in bank_script.SOURCE_KEYS:
  var legacy:Array=player.carry_banks[bank_script.CURRENT_BINDING].equipment_frames["diving-helmet"][key]
  check(player.equipment_frames["diving-helmet"][key]==legacy,"helmet source selection remains exact")
 var saves=[]
 var origin=Vector2.INF
 for id in actor.room_nodes.get(CELL,[]):
  var point:Vector2=actor.graph.get_point_position(id)
  if actor.can_stand(point) and actor.can_stand(point+Vector2(96,0)) and actor.segment_clear(point,point+Vector2(96,0)):origin=point;break
 check(origin.is_finite(),"legal East resume segment")
 if origin.is_finite():
  for binding in [bank_script.CURRENT_BINDING,bank_script.MASTER_BINDING]:
   for helmet in [false,true]:
    check(player.select_binding(binding),"explicit source version for disk resume")
    player.clear_carry();player.current_key="";player.last_time=-1;player.motion.clear();actor.planted_until=-1;actor.planted_clip=""
    actor.foot=origin;actor.direction="east";actor.state="walk";actor.stage="workshop_carry";actor.goal="curiosity";actor.goal_cell=CELL;actor.timer=0;actor.path=PackedVector2Array([origin+Vector2(96,0)]);actor.helmet_equipped=helmet;actor.needs={"hunger":0.0,"fatigue":0.0,"curiosity":0.0,"maintenance":0.0}
    game.paused=false;game.visual_time_seconds+=1
    for tick in range(26):game.visual_time_seconds+=.005;actor.update(game,.005);grid._get_human_frame_source(actor.animation_state(),"east")
    var source:Texture2D=grid._get_human_frame_source(actor.animation_state(),"east");var pixels=source.get_image().get_data();var foot:Vector2=actor.foot;var clock:float=game.visual_time_seconds
    check(not player.start_motion.is_empty(),"disk save is inside actual carry entry")
    await capture("disk resume before / "+binding+(" / helmet" if helmet else " / bare"),source,"carry-start-east",2,"save")
    game.run_save_path="user://bill_master_bound.loop"
    var snapshot:Dictionary=Save.capture(game)
    check(Save.problem(snapshot).is_empty(),"normal source-bound checkpoint valid: "+Save.problem(snapshot))
    check(Save.write(game,game.run_save_path)==OK,"isolated source-bound disk write")
    var disk:Dictionary=Save.read(game.run_save_path);check(not disk.is_empty(),"source-bound disk read validates")
    if disk.is_empty():continue
    var future=[]
    for tick in range(30):
     game.visual_time_seconds+=.005;actor.update(game,.005)
     future.append({"foot":actor.foot,"pixels":grid._get_human_frame_source(actor.animation_state(),actor.direction).get_image().get_data(),"entry":player.start_motion.duplicate(true)})
    check(await Save.restore_staged(game,disk),"source-bound checkpoint restored into actual main")
    game.set_process(false);game.tick_timer.stop();game.crew_comms.set_process(false);game.crew_comms.dismiss();game.run_save_path="user://bill_master_bound.loop"
    actor=game.bill_npc;player=game.grid_view.human_water_player;grid=game.grid_view
    var restored:Texture2D=grid._get_human_frame_source(actor.animation_state(),actor.direction)
    check(player.carry_binding()==binding and actor.snapshot().carry_binding==binding,"actor and selected playback restore same version")
    check(restored.get_image().get_data()==pixels and actor.foot==foot and absf(game.visual_time_seconds-clock)<.000001,"exact source/root/clock restored")
    await capture("disk resume after / "+binding+(" / helmet" if helmet else " / bare"),restored,"carry-start-east",2,"save")
    game.paused=false
    for expected in future:
     game.visual_time_seconds+=.005;actor.update(game,.005);var shown:Texture2D=grid._get_human_frame_source(actor.animation_state(),actor.direction)
     check(actor.foot==expected.foot and shown.get_image().get_data()==expected.pixels and player.start_motion==expected.entry,"continued source and physical entry motion deterministic")
    saves.append({"binding":binding,"helmet":helmet,"futureSteps":future.size()})
 check(player.select_binding(bank_script.MASTER_BINDING),"normal repaired family restored after legacy review")
 player.clear_carry();actor.helmet_equipped=false;actor.stage="";actor.goal="";actor.path.clear();actor.state="idle";actor.foot=start;actor.timer=0
 grid._get_human_frame_source("idle","east")
 grid.human_walk_join=null;game.visual_time_seconds=100;game.paused=false
 var target=Vector2i(21,20);game.wrecks.erase(target);game.drone_fleet.sites.erase(target)
 game.hand.assign(["corridor"]);game._on_card_pressed("corridor")
 var legal=false
 for quarter in range(4):
  game.selected_rotation=quarter
  if game.get_placement_problem("corridor",target).is_empty():legal=true;break
 check(legal,"actual east paid construction site legal: "+game.get_placement_problem("corridor",target))
 var metal:int=game.resources.metal
 if legal:game._on_grid_clicked(target)
 check(game.resources.metal<metal and game.drone_fleet.reserved(target),"actual paid room order spends metal and reserves site")
 actor.timer=0
 var records=[];var seen={};var previous="";var completed=false
 for step in range(6000):
  var before:Vector2=actor.foot
  game.visual_time_seconds+=.01;actor.update(game,.01)
  var pose:String=actor.animation_state();var key=pose+"-"+actor.direction
  var texture:Texture2D=grid._get_human_frame_source(pose,actor.direction)
  var slot=-1
  for i in range(player.frames.get(key,[]).size()):
   if same(texture,player.frames[key][i]):slot=i;break
  if pose in ["torch-draw","weld","torch-stow"]:
   check(actor.direction=="east" and actor.goal=="construction","actual builder faces paid east connection")
   seen[key+"/"+str(slot)]=true
  records.append({"job":"construction","time":game.visual_time_seconds,"stage":actor.stage,"pose":pose,"key":key,"slot":slot,"foot":[actor.foot.x,actor.foot.y],"timer":actor.timer})
  if key!=previous or (pose in ["torch-draw","torch-stow"] and not seen.has("capture/"+key+"/"+str(slot))):
   await capture("paid construction / "+key+" / "+str(slot),texture,key,slot,"actual")
   seen["capture/"+key+"/"+str(slot)]=true
  previous=key
  if game.occupied.has(target):completed=true;break
 check(completed and not game.drone_fleet.reserved(target),"production Bill completes paid room and releases reservation")
 for key in ["torch-draw-east","weld-east","torch-stow-east"]:
  for slot in range(player.frames[key].size()):check(seen.has(key+"/"+str(slot)),"actual construction visits source "+key+"/"+str(slot))
 # Real service progression at the authored, standable workshop bench.
 game.occupied.erase(CELL)
 for i in range(game.placed_rooms.size()-1,-1,-1):
  if game.placed_rooms[i].pos==CELL:game.placed_rooms.remove_at(i)
 game.selected_rotation=0;game._place_room("salvage_workshop",CELL,true);game.powered_room_cells[CELL]=true
 actor.signature="";await actor.rebuild(game)
 var stations:Array=actor.RoomActivity.stations(actor.geometry[CELL]);check(not stations.is_empty(),"actual workshop bench available")
 if not stations.is_empty():
  var station:Dictionary=stations[0]
  actor.goal="curiosity";actor.goal_cell=CELL;actor.stage="";actor.state="idle";actor.timer=0;actor.path.clear()
  actor.foot=(Vector2(CELL)+Vector2.ONE*.5)*384+Vector2(station.point);actor.direction=station.facing
  actor.needs={"hunger":0.0,"fatigue":0.0,"curiosity":60.0,"maintenance":0.0}
  check(actor.can_stand(actor.foot) and actor.begin_room_activity(),"real workshop service contact starts")
  game._refresh_all();previous="";var pickup_seen=false;var pickup_slots={};var carry_seen=false;var unload_seen=false;var finished=false
  for step in range(6000):
   var before:Vector2=actor.foot
   game.visual_time_seconds+=.01;actor.update(game,.01)
   var pose:String=actor.animation_state();var key=pose+"-"+actor.direction
   var texture:Texture2D=grid._get_human_frame_source(pose,actor.direction)
   if actor.stage=="workshop_pickup":
    pickup_seen=pickup_seen or pose=="pickup"
    var slot:int=player.frames[key].find(texture);pickup_slots[slot]=true
    if not seen.has("workshop/"+key+"/"+str(slot)):
     await capture("actual workshop pickup / "+str(slot),texture,key,slot,"actual");seen["workshop/"+key+"/"+str(slot)]=true
   if actor.stage=="workshop_carry":carry_seen=true
   if actor.stage=="workshop_unload":unload_seen=true
   records.append({"job":"workshop","time":game.visual_time_seconds,"stage":actor.stage,"pose":pose,"key":key,"foot":[actor.foot.x,actor.foot.y],"timer":actor.timer,"clip":player.motion.get("clip","")})
   check(actor.can_stand(actor.foot) and actor.segment_clear(before,actor.foot),"actual cargo route has legal floor contact")
   var identity=actor.stage+"/"+key+"/"+str(player.motion.get("clip",""))
   if identity!=previous:await capture("actual workshop / "+identity,texture,key,-1,"actual")
   previous=identity
   if unload_seen and not actor.stage.begins_with("workshop_"):finished=true;break
  check(pickup_seen,"production workshop pickup dispatches pickup art")
  check(pickup_slots.size()==11,"actual pickup visits all11 repaired source slots")
  check(carry_seen and unload_seen and finished,"production workshop carries, arrives and completes service")
 var file=FileAccess.open(OUT+"report.json",FileAccess.WRITE)
 file.store_string(JSON.stringify({"checks":checks,"failures":failures,"captures":captures,"records":records,"seen":seen,"saves":saves,"selectedSlots":selected_slots,"scope":"Normal loader and installed source-bound bare East master family; all selected slots exact, legacy banks and helmet sources retained, four actual disk entry resumes and deterministic future motion; actual paid construction dispatch/approach/work/completion and prescribed real workshop bench service entry followed by production pickup/generated carry route/arrival/unload completion. Monotonic .01s updates, no source clock seeding. Other directions retained selected banks. Actual main disk restore covers legacy/current bare and helmet entry; not fresh Title Continue, natural workshop choice or all equipment/life/water animation review."},"\t"));file.close()
 print("BILL ACTUAL JOBS: ",checks," checks, ",failures," failures");quit(1 if failures else 0)
