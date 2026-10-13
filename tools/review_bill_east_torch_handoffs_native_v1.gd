extends SceneTree
const Loading=preload("res://scripts/loading_transition.gd")
const OUT="res://output/bill-east-torch-handoffs-native-v1/"
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
  if game.grid_view.content_canvases.has(CELL):
   var canvas=game.grid_view.content_canvases[CELL]
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
 var grid=game.grid_view;var player=grid.human_water_player;var normal={}
 for key in ["idle-east","walk-east"]:normal[key]=player.frames[key].duplicate()
 player.load_manifest("res://character/bill-east-idle-master-motion-v1/manifest.json",true)
 check(same(grid.human_animations["idle"]["east"][0],normal["idle-east"][0]),"preview load alone leaves retained bare table unchanged")
 check(not same(player.frames["idle-east"][0],normal["idle-east"][0]),"staged idle source differs from selected source")
 player.load_manifest("res://character/bill-east-walk-master-full-v1/manifest.json",true)
 for key in ["idle-east","walk-east"]:
  var state=key.get_slice("-",0)
  for texture in player.frames[key]:texture.set_meta("major_bill_v2",true)
  grid.human_animations[state]["east"]=player.frames[key];grid.human_animation_timing[key]=player.timing[key]
 check(player.frames["walk-east"].size()==48,"complete48 walking phases loaded")
 var review:Dictionary=JSON.parse_string(FileAccess.get_file_as_string("res://character/bill-east-torch-handoffs-master-v1/review.json"))
 var rows={};var timings={}
 for key in review.sources:
  var source:Dictionary=review.sources[key]
  player.load_manifest("res://"+str(source.manifest),true)
  rows[key]=player.frames[key].duplicate();timings[key]=player.timing[key].duplicate(true)
  check(rows[key].size()==source.files.size(),"complete bank: "+key)
  check(timings[key].durations==source.durations and timings[key].loop==source.loop,"original timing/loop: "+key)
 for key in rows:
  player.frames[key]=rows[key];player.timing[key]=timings[key]
  var state:String=key.trim_suffix("-east")
  if not grid.human_animations.has(state):grid.human_animations[state]={}
  grid.human_animations[state]["east"]=rows[key];grid.human_animation_timing[key]=timings[key]
  for texture in rows[key]:texture.set_meta("major_bill_v2",true)
 check(same(rows["torch-draw-east"][0],rows["torch-stow-east"][5]),"exact idle endpoints")
 check(same(rows["torch-draw-east"][5],rows["weld-east"][0]) and same(rows["torch-stow-east"][0],rows["weld-east"][0]),"exact active torch endpoints")
 actor.foot=start+Vector2(8,0);game.paused=false;grid.human_walk_join=null;game.visual_time_seconds=100
 actor.goal="";actor.state="idle";actor.timer=10;grid.human_animation_key=""
 await capture("idle before",grid._get_human_frame_source(actor.animation_state(),"east"),"idle-east",0,"controller")
 var slots=[]
 for key in rows:
  actor.goal="construction";actor.state="weld";var cursor=0.0
  for slot in range(rows[key].size()):
   var phase:float=cursor+float(timings[key].durations[slot])/2000.0
   if key=="torch-draw-east":actor.timer=phase
   elif key=="torch-stow-east":actor.timer=9.48+phase
   else:actor.timer=1.0
   var state:String=actor.animation_state()
   check(state==key.trim_suffix("-east"),"production controller state: %s/%d"%[key,slot])
   if key!="weld-east":check(absf(actor.action_elapsed()-phase)<.00001,"production action clock phase")
   else:check(actor.action_elapsed()<0,"weld keeps loop clock")
   game.visual_time_seconds+=.1;grid.human_animation_key=key;grid.human_animation_last_time=game.visual_time_seconds
   grid.human_animation_last_position=game.get_test_walker_position()/grid._cell_size();grid.human_animation_phase=phase;grid.human_animation_started=game.visual_time_seconds-phase
   player.current_equipment="";player.current_key=key;player.last_time=game.visual_time_seconds;player.last_position=game.get_test_walker_position()/grid._cell_size();player.phase=phase;player.started=game.visual_time_seconds-phase;player.motion={"state":state,"direction":"east","started":game.visual_time_seconds,"clip":""}
   var shown:Texture2D=grid._get_human_frame_source(state,"east")
   check(same(shown,rows[key][slot]),"production source identity: %s/%d"%[key,slot])
   slots.append({"key":key,"slot":slot,"timer":actor.timer,"elapsed":actor.action_elapsed(),"foot":[actor.foot.x,actor.foot.y]})
   await capture(key+" / pose "+str(slot),shown,key,slot,"controller")
   cursor+=float(timings[key].durations[slot])/1000.0
 var boundaries=[]
 for timer_value in [.519999,.520001,9.479999,9.48,9.9999]:
  actor.timer=timer_value
  var state:String=actor.animation_state();var key:String=state+"-east"
  var expected_state:String="torch-draw" if timer_value<.52 else ("torch-stow" if timer_value>=9.48 else "weld")
  var expected_slot:int=5 if state=="torch-draw" or (state=="torch-stow" and timer_value>9.99) else 0
  check(state==expected_state,"production520ms draw/stow boundary state")
  game.visual_time_seconds+=.1;grid.human_animation_key=key;grid.human_animation_last_time=game.visual_time_seconds;grid.human_animation_last_position=game.get_test_walker_position()/grid._cell_size();grid.human_animation_phase=0;grid.human_animation_started=game.visual_time_seconds
  var shown:Texture2D=grid._get_human_frame_source(state,"east")
  check(same(shown,rows[key][expected_slot]),"boundary submitted exact endpoint source")
  boundaries.append({"timer":timer_value,"state":state,"expectedSlot":expected_slot})
  await capture("boundary / "+str(timer_value),shown,key,expected_slot,"boundary")
 actor.goal="";actor.state="idle";actor.timer=0;grid.human_animation_key="";game.visual_time_seconds+=.1
 await capture("idle after",grid._get_human_frame_source(actor.animation_state(),"east"),"idle-east",0,"controller")
 game.paused=true
 var file=FileAccess.open(OUT+"report.json",FileAccess.WRITE)
 file.store_string(JSON.stringify({"checks":checks,"failures":failures,"captures":captures,"slots":slots,"boundaries":boundaries,"scope":"18 source slots and five construction-timer boundaries through production Bill animation_state/action_elapsed and retained furnished ColdStore renderer. Exact current idle/weld endpoints. Prescribed stationary timers; main processing disabled. Not autonomous construction completion, tool ownership, moving routes, gear/save or normal admission."},"\t"));file.close()
 print("BILL TORCH HANDOFFS: ",checks," checks, ",failures," failures");quit(1 if failures else 0)
