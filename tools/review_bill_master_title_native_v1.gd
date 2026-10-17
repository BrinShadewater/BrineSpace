extends SceneTree
const Loading=preload("res://scripts/loading_transition.gd")
const OUT="res://output/bill-master-title-native-v1/"
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
 game.meta.save_path="user://brine_save.json";check(game.meta.save_to_disk()==OK,"scratch selected Bill profile")
 var cases=[]
 for binding in [bank_script.CURRENT_BINDING,bank_script.MASTER_BINDING]:
  var origin=Vector2.INF
  for id in actor.room_nodes.get(CELL,[]):
   var point:Vector2=actor.graph.get_point_position(id)
   if actor.can_stand(point) and actor.can_stand(point+Vector2(96,0)) and actor.segment_clear(point,point+Vector2(96,0)):origin=point;break
  check(origin.is_finite(),"legal East source-bound route")
  if not origin.is_finite():quit(1);return
  check(player.select_binding(binding),"checkpoint source version selected")
  player.clear_carry();player.current_key="";player.last_time=-1;player.motion.clear();actor.planted_until=-1;actor.planted_clip=""
  actor.foot=origin;actor.direction="east";actor.state="walk";actor.stage="workshop_carry";actor.goal="curiosity";actor.goal_cell=CELL;actor.timer=0;actor.path=PackedVector2Array([origin+Vector2(96,0)]);actor.helmet_equipped=false;actor.needs={"hunger":0.0,"fatigue":0.0,"curiosity":0.0,"maintenance":0.0}
  game.paused=false;game.visual_time_seconds+=1
  for tick in range(26):game.visual_time_seconds+=.005;actor.update(game,.005);grid._get_human_frame_source(actor.animation_state(),"east")
  var source:Texture2D=grid._get_human_frame_source(actor.animation_state(),"east");var pixels=source.get_image().get_data();var foot:Vector2=actor.foot;var clock:float=game.visual_time_seconds
  check(not player.start_motion.is_empty(),"title checkpoint during real carry entry")
  await capture("before Title Continue / "+binding,source,"carry-start-east",2,"before")
  var path:String="user://bill-master-title-"+str(cases.size())+".loop";game.run_save_path=path
  check(Save.write(game,path)==OK,"valid isolated disk checkpoint")
  var future=[]
  for tick in range(30):
   game.visual_time_seconds+=.005;actor.update(game,.005)
   future.append({"foot":actor.foot,"pixels":grid._get_human_frame_source(actor.animation_state(),actor.direction).get_image().get_data(),"entry":player.start_motion.duplicate(true)})
  game.queue_free();await process_frame
  var title=load("res://scenes/title_screen.tscn").instantiate();title.run_save_path=path;root.add_child(title);current_scene=title;await process_frame
  check(title.continue_button.visible and not title.continue_button.disabled,"normal title Continue enabled")
  var title_id:int=title.get_instance_id();title.continue_button.emit_signal("pressed")
  var resumed=null;deadline=Time.get_ticks_msec()+120000
  while Time.get_ticks_msec()<deadline:
   if is_instance_valid(current_scene) and current_scene.get_instance_id()!=title_id and current_scene.get("startup_complete")==true:resumed=current_scene;break
   await process_frame
  check(is_instance_valid(resumed),"normal Title Continue starts and restores fresh main")
  if not is_instance_valid(resumed):quit(1);return
  game=resumed;game.set_process(false);game.tick_timer.stop();game.crew_comms.set_process(false);game.crew_comms.dismiss();game.run_save_path=path
  for node in root.get_children():
   if node.get_script()==Loading:
    deadline=Time.get_ticks_msec()+20000
    while is_instance_valid(node) and node.continue_button.disabled and Time.get_ticks_msec()<deadline:await process_frame
    if is_instance_valid(node):node.continue_button.emit_signal("pressed")
    while is_instance_valid(node) and Time.get_ticks_msec()<deadline:await process_frame
    check(not is_instance_valid(node),"normal loading Continue clears overlay")
  actor=game.bill_npc;grid=game.grid_view;player=grid.human_water_player
  var restored:Texture2D=grid._get_human_frame_source(actor.animation_state(),actor.direction)
  check(player.carry_binding()==binding and actor.snapshot().carry_binding==binding,"title restored bound source version")
  check(actor.foot==foot and absf(game.visual_time_seconds-clock)<.000001 and game.paused,"title exact physical root/clock and pause")
  check(restored.get_image().get_data()==pixels,"title retained exact source RGBA")
  game._process(.5);check(actor.foot==foot and absf(game.visual_time_seconds-clock)<.000001,"paused main holds root and clock")
  camera=(Vector2(CELL)+Vector2.ONE*.5)/float(game.GRID_SIZE);game._set_grid_zoom(2.0,true,camera)
  for attempt in range(180):
   await process_frame;await RenderingServer.frame_post_draw;game._restore_grid_view_center(camera)
   if grid.pending_layers.is_empty() and not grid.zoom_settling and not grid.zoom_preparing:break
  await capture("after normal Title Continue / "+binding,restored,"carry-start-east",2,"after")
  game.paused=false
  for expected in future:
   game.visual_time_seconds+=.005;actor.update(game,.005)
   var shown:Texture2D=grid._get_human_frame_source(actor.animation_state(),actor.direction)
   check(actor.foot==expected.foot and shown.get_image().get_data()==expected.pixels and player.start_motion==expected.entry,"fresh main deterministic future root/source/entry")
  cases.append({"binding":binding,"futureSteps":future.size(),"scope":"Same native process; fresh normal title and main scenes, normal Continue/loading buttons and pending disk restoration. Bare legacy/current source versions."})
 var file=FileAccess.open(OUT+"report.json",FileAccess.WRITE)
 file.store_string(JSON.stringify({"checks":checks,"failures":failures,"cases":cases,"captures":captures},"  "))
 print("BILL MASTER TITLE CONTINUE: ",checks," checks, ",failures," failures");quit(1 if failures else 0)
