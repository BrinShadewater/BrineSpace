extends SceneTree
const Loading=preload("res://scripts/loading_transition.gd")
const OUT="res://output/bill-walk-join-context-native-v1/"
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
 var provider=preload("res://tools/bill_east_walk_join_candidate_v1.gd").new()
 var cases=[
  {"name":"helmet","state":"idle","helmet":true},
  {"name":"water","state":"tread","medium":"water"},
  {"name":"west","state":"idle","direction":"west"},
  {"name":"run","state":"run"},
  {"name":"carry","state":"carry"},
  {"name":"weld","state":"weld"},
  {"name":"construction enter","state":"weld","goal":"construction","timer":.2},
  {"name":"inspection","state":"idle","stage":"workshop_inspect","timer":1.0},
  {"name":"meal","state":"idle","stage":"life_eat","timer":1.0}]
 var results=[]
 check(grid.human_walk_join==null,"normal renderer join provider defaults to null")
 for context in cases:
  provider.reset();grid.human_walk_join=provider
  actor.dead=false;actor.helmet_equipped=false;actor.movement_medium="dry";actor.direction="east";actor.stage="";actor.goal="";actor.state="walk";actor.timer=10;actor.foot=start
  grid.human_animation_key="";grid.human_animation_last_time=-1;game.visual_time_seconds=100.0;game.paused=false
  grid._get_human_frame_source("walk","east")
  actor.foot+=Vector2(8,0);game.visual_time_seconds+=.2
  var walked=grid._get_human_frame_source("walk","east")
  check(walked!=null and provider.previous_state=="walk","walking provider active before "+context.name)
  actor.state=context.state;actor.direction=context.get("direction","east");actor.helmet_equipped=context.get("helmet",false);actor.movement_medium=context.get("medium","dry");actor.stage=context.get("stage","");actor.goal=context.get("goal","");actor.timer=context.get("timer",10.0)
  game.visual_time_seconds+=.02
  var shown=grid._get_human_frame_source(actor.state,actor.direction)
  check(provider.previous_state=="" and provider.stopped<0 and provider.last_display==null,"actual dispatch cancels previous walk for "+context.name)
  grid.human_walk_join=null
  var baseline=grid._get_human_frame_source(actor.state,actor.direction)
  check(same(shown,baseline),"special activity source identical to provider-free renderer for "+context.name)
  grid.human_walk_join=provider
  if context.name in ["run","carry","weld"]:await capture(context.name,shown,actor.state+"-east",0,"selected activity")
  actor.helmet_equipped=false;actor.movement_medium="dry";actor.direction="east";actor.stage="";actor.goal="";actor.state="idle";actor.timer=10
  game.visual_time_seconds+=.02
  var returned=grid._get_human_frame_source("idle","east")
  grid.human_walk_join=null;var idle_baseline=grid._get_human_frame_source("idle","east");grid.human_walk_join=provider
  check(same(returned,idle_baseline),"return to dry idle has no stale walking or settle pose for "+context.name)
  await capture("idle after "+context.name,returned,"idle-east",0,"candidate")
  results.append({"context":context.name,"sourceMatchesBaseline":same(shown,baseline),"returnMatchesIdle":same(returned,idle_baseline)})
 game.paused=true;grid.human_walk_join=null
 var file=FileAccess.open(OUT+"report.json",FileAccess.WRITE)
 file.store_string(JSON.stringify({"checks":checks,"failures":failures,"contexts":results,"captures":captures,"scope":"Actual grid getter dispatch, nine prescribed activity/equipment contexts and dry East idle return; default furnished room capture. No autonomous activity choice, physical water contact, full gear/action loops or normal candidate admission."},"\t"));file.close()
 print("BILL JOIN CONTEXT: ",checks," checks, ",failures," failures");quit(1 if failures else 0)
