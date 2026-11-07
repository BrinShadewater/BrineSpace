extends SceneTree
const Loading=preload("res://scripts/loading_transition.gd")
const OUT="res://output/bill-carry-turn-east-seams-native-v1/"
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
 var grid=game.grid_view;var player=grid.human_water_player
 for manifest in ["res://character/bill-east-carry-master-v1/manifest.json","res://character/bill-east-cargo-handoffs-master-v1/manifest.json","res://character/bill-east-carry-entry-master-v1/manifest.json","res://character/bill-carry-turn-east-seams-v1/manifest.json"]:player.load_manifest(manifest,true)
 var review:Dictionary=JSON.parse_string(FileAccess.get_file_as_string("res://character/bill-carry-turn-east-seams-v1/review.json"));var cases=[]
 game.paused=false;game.visual_time_seconds=100
 for contract in review.records:
  var key:String=contract.key;var from_direction:String=key.get_slice("-",2);var to_direction:String=key.get_slice("-",3)
  var delta:Vector2={"east":Vector2.RIGHT,"west":Vector2.LEFT,"north":Vector2.UP,"south":Vector2.DOWN}[to_direction]*96
  var origin=Vector2.INF
  for id in actor.room_nodes.get(CELL,[]):
   var point:Vector2=actor.graph.get_point_position(id)
   if actor.can_stand(point) and actor.can_stand(point+delta) and actor.segment_clear(point,point+delta):origin=point;break
  check(origin.is_finite(),"legal actual floor segment for "+key)
  if not origin.is_finite():continue
  var row:Array=player.frames[key];var durations:Array=player.timing[key].durations
  check(durations==contract.originalState.frameDurationsMs and row.size()==contract.originalState.frameFiles.size(),"complete original turn clock/poses retained")
  for index in contract.changedSlots:check(same(row[int(index)],player.frames["pickup-east"][10]),"exact repaired shared East whole turn pose")
  player.clear_carry();player.current_key="";player.last_time=-1;player.motion.clear();actor.planted_until=-1;actor.planted_clip=""
  actor.foot=origin;actor.direction=from_direction;actor.state="walk";actor.stage="workshop_carry";actor.goal="curiosity";actor.goal_cell=CELL;actor.timer=0;actor.path=PackedVector2Array([origin+delta]);actor.needs={"hunger":0.0,"fatigue":0.0,"curiosity":0.0,"maintenance":0.0}
  var seen={};var resumed=false;var records=[];var onset=-1.0
  for step in range(450):
   var before:Vector2=actor.foot;game.visual_time_seconds+=.005;actor.update(game,.005)
   var shown:Texture2D=grid._get_human_frame_source(actor.animation_state(),actor.direction)
   check(actor.can_stand(actor.foot) and actor.segment_clear(before,actor.foot),"actual turn floor contact clear")
   if str(player.motion.get("clip",""))==key:
    if onset<0:onset=float(player.motion.started)
    var elapsed:float=game.visual_time_seconds-float(player.motion.started);var cursor=0.0;var slot=row.size()-1
    for i in range(row.size()):
     cursor+=float(durations[i])/1000
     if elapsed<cursor:slot=i;break
    check(same(shown,row[slot]),"actual production turn source identity")
    check(actor.foot.distance_to(origin)<.0001,"production carry pivot remains planted")
    if not seen.has(slot):await capture(key+" / slot "+str(slot),shown,key,slot,"actual-turn");seen[slot]=true
    records.append({"time":game.visual_time_seconds,"elapsed":elapsed,"slot":slot,"foot":[actor.foot.x,actor.foot.y]})
   elif onset>=0 and actor.foot.distance_to(origin)>.01:
    resumed=true;break
  check(seen.size()==row.size() and resumed,"full actual planted turn then resumed movement: "+key)
  check(actor.direction==to_direction,"turn retains requested physical heading")
  cases.append({"key":key,"seen":seen.keys(),"records":records,"resumed":resumed})
 var file=FileAccess.open(OUT+"report.json",FileAccess.WRITE);file.store_string(JSON.stringify({"checks":checks,"failures":failures,"captures":captures,"cases":cases,"scope":"Seven selected-production carry turn programs with fixture-only repaired bare East endpoint/entry/gait. Actual .005s actor.update on prescribed legal96-unit floor segments: full57turn slots, planted pivots and resumed physical headings. Original800/1600ms clocks; seven exact whole East aliases,50other poses unchanged. Not natural dispatch, continuous cadence, equipment, normal admission or Continue."},"\t"));file.close()
 print("BILL TURN SEAMS: ",checks," checks, ",failures," failures");quit(1 if failures else 0)
