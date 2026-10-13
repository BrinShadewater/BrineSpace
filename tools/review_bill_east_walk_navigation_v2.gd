extends SceneTree
const Loading=preload("res://scripts/loading_transition.gd")
const OUT="res://output/bill-east-walk-navigation-v2/"
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
 var left=Vector2.ZERO;var right=Vector2.ZERO;var longest=0.0
 for a in actor.room_nodes.get(CELL,[]):
  var pa:Vector2=actor.graph.get_point_position(a)
  if not actor.can_stand(pa):continue
  for b in actor.room_nodes.get(CELL,[]):
   var pb:Vector2=actor.graph.get_point_position(b)
   if absf(pa.y-pb.y)>.01 or pb.x-pa.x<=longest:continue
   if actor.can_stand(pb) and actor.segment_clear(pa,pb):left=pa;right=pb;longest=pb.x-pa.x
 check(longest>138.0,"actual furnished room permits two complete East gait cycles")
 if longest<=138.0:quit(1);return
 var traversals=[]
 for variant in ["candidate","selected"]:
  for key in ["idle-east","walk-east"]:
   var state=key.get_slice("-",0)
   grid.human_animations[state]["east"]=player.frames[key].duplicate() if variant=="candidate" else normal[key].duplicate()
  actor.foot=left;actor.path.clear();actor.direction="east";actor.state="idle";actor.stage="";actor.goal="";actor.timer=20;actor.movement_heading.clear();actor.avoidance_positions=PackedVector2Array();actor.avoidance_position=Vector2.INF
  grid.human_animation_key="";grid.human_animation_last_time=-1;game.visual_time_seconds=100.0;game.paused=false
  var visited={};var walk_steps=0;var total_distance=0.0;var elapsed=0.0
  for i in range(16):
   game.visual_time_seconds+=.02;actor.update(game,.02);var shown=grid._get_human_frame_source(actor.state,actor.direction)
   if i%4==0:await capture("idle before",shown,"idle-east",i,variant)
  actor.path=PackedVector2Array([right]);actor.goal="";actor.goal_cell=CELL;actor.state="walk";actor.timer=0
  grid._get_human_frame_source("walk","east")
  while not actor.path.is_empty() and walk_steps<600:
   var previous=actor.foot;var old_phase=grid.human_animation_phase
   game.visual_time_seconds+=.02;actor.update(game,.02);elapsed+=.02;walk_steps+=1
   check(actor.can_stand(actor.foot),"real actor update keeps legal floor contact")
   check(actor.direction=="east","real actor move retains East facing")
   var distance=previous.distance_to(actor.foot);total_distance+=distance
   check(distance<=actor.movement_rate()*.02+.01,"actual movement bounded by actor speed")
   var shown:Texture2D=grid._get_human_frame_source(actor.state,actor.direction)
   var slot=-1
   for n in range(grid.human_animations[actor.state][actor.direction].size()):
    if same(shown,grid.human_animations[actor.state][actor.direction][n]):slot=n;break
   check(slot>=0,"real source belongs to current state bank")
   if actor.state=="walk":
    visited[slot]=true
    var increment=distance/384.0/float(grid.human_stride_distance.get("walk-east",grid.human_stride_distance["walk"]))*2.0
    check(absf(grid.human_animation_phase-old_phase-increment)<.0001,"renderer gait advances from actual traveled distance")
   samples.append({"variant":variant,"step":walk_steps,"elapsed":elapsed,"state":actor.state,"slot":slot,"foot":[actor.foot.x,actor.foot.y],"phase":grid.human_animation_phase,"distance":distance})
   if walk_steps%4==0 or actor.path.is_empty():await capture("walking route",shown,actor.state+"-east",slot,variant)
  check(actor.path.is_empty() and actor.foot.distance_to(right)<.01,"actual actor move reaches legal destination")
  check(actor.state=="idle","actual arrival selects idle")
  check(visited.size()>=46,"distance-driven route visits almost every gait phase")
  for i in range(16):
   game.visual_time_seconds+=.02;var shown=grid._get_human_frame_source(actor.state,actor.direction)
   if i%4==0:await capture("idle after",shown,"idle-east",i,variant)
  traversals.append({"variant":variant,"steps":walk_steps,"distance":total_distance,"duration":elapsed,"visitedSlots":visited.keys(),"arrived":actor.path.is_empty()})
 game.paused=true
 var file=FileAccess.open(OUT+"report.json",FileAccess.WRITE);file.store_string(JSON.stringify({"checks":checks,"failures":failures,"captures":captures,"samples":samples,"traversals":traversals,"route":{"left":[left.x,left.y],"right":[right.x,right.y],"length":longest},"scope":"Actual Bill.update/move/arrive and distance-driven retained bare renderer in default furnished ColdStore. Candidate/selected same legal route. Explicit route and source binding, simulation stepped .02s with main/tick timer disabled; not autonomous goal choice, normal admission, gear/water or save/TitleContinue."},"\t"));file.close();print("BILL WALK NAVIGATION: ",checks," checks, ",failures," failures");quit(1 if failures else 0)
