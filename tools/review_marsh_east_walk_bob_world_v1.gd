extends SceneTree
const Normal=preload("res://scripts/marsh_npc.gd")
const Loading=preload("res://scripts/loading_transition.gd")
const OUTPUT="res://output/marsh-animation-audit/east-walk-bob-world-v1-2026-10-03/"
class CountedMarsh extends Normal:
 var arrivals:=0
 func arrive() -> void:arrivals+=1;super.arrive()
var game
var checks:=0
var failures:=0
var captures:Array=[]
var samples:Array=[]
var restored_slots:Dictionary={}
func _init():call_deferred("run")
func check(ok:bool,message:String):
 checks+=1
 if not ok:failures+=1;push_error(message)
func settle_camera(camera:Vector2)->bool:
 game._set_grid_zoom(.8,true,camera)
 for unused in range(180):
  await process_frame;await RenderingServer.frame_post_draw
  game._restore_grid_view_center(camera)
  if game.grid_view.pending_layers.is_empty() and not game.grid_view.zoom_settling and not game.grid_view.zoom_preparing and game._grid_view_center_ratio().distance_to(camera)<.002:return true
 return false
func contact(texture:Texture2D)->Vector2:
 var image:=texture.get_image();var bottom:=-1;var sum:=0.0;var count:=0
 for y in range(image.get_height()):
  for x in range(image.get_width()):
   if image.get_pixel(x,y).a>.5:
    if y>bottom:bottom=y;sum=0;count=0
    if y==bottom:sum+=x;count+=1
 return Vector2(sum/maxi(1,count),bottom)
func capture(label:String,key:String,slot:int,normal_texture:Texture2D):
 var p=game.grid_view.marsh_player;var texture:Texture2D=game.grid_view._get_marsh_frame(game)
 var index:=captures.size();var record={"label":label,"key":key,"slot":slot,"foot":[game.marsh_npc.foot.x,game.marsh_npc.foot.y],"position":[game.get_marsh_position().x,game.get_marsh_position().y]}
 for version in ["candidate","normal"]:
  p.frames[key][slot]=texture if version=="candidate" else normal_texture
  game.grid_view.queue_redraw();await process_frame;await RenderingServer.frame_post_draw
  var submitted:Texture2D=game.grid_view._get_marsh_frame(game)
  check(submitted.get_image().get_data()==p.frames[key][slot].get_image().get_data(),"same-clock source held for native comparison")
  var native="%s-world-%03d.png"%[version,index];var source="%s-source-%03d.png"%[version,index]
  check(root.get_texture().get_image().save_png(OUTPUT+native)==OK,"full native station comparison saved")
  check(submitted.get_image().save_png(OUTPUT+source)==OK,"exact submitted source saved")
  record[version]={"file":native,"sourceFile":source}
 p.frames[key][slot]=texture
 captures.append(record)
func run():
 if DisplayServer.get_name()=="headless":quit(2);return
 DirAccess.make_dir_recursive_absolute(OUTPUT)
 preload("res://scripts/title_settings.gd").reduced_motion=true
 var store=preload("res://scripts/room_layout_store.gd");store.loaded=true;store.data={}
 game=load("res://scenes/main.tscn").instantiate()
 game.set_meta("authored_site_fixture",true)
 game.meta.save_path="user://east_walk.meta";game.run_save_path="user://east_walk.loop"
 game.meta.unlocked_architect_ids={"bill":true,"marsh":true};game.meta.selected_architect="marsh"
 root.add_child(game);current_scene=game
 var deadline:=Time.get_ticks_msec()+120000
 while not game.startup_complete and Time.get_ticks_msec()<deadline:await process_frame
 check(game.startup_complete,"observable main startup completes")
 if not game.startup_complete:quit(1);return
 game.set_process(false);game.tick_timer.stop();game.crew_comms.set_process(false);game.crew_comms.dismiss()
 var overlay=null
 for child in root.get_children():
  if child.get_script()==Loading:overlay=child;break
 if overlay!=null:
  deadline=Time.get_ticks_msec()+20000
  while overlay.continue_button.disabled and Time.get_ticks_msec()<deadline:await process_frame
  check(not overlay.continue_button.disabled,"loading transmission Continue enabled")
  overlay.continue_button.pressed.emit()
  while is_instance_valid(overlay) and Time.get_ticks_msec()<deadline:await process_frame
  check(not is_instance_valid(overlay),"actual loading overlay gone before visual evidence")
 game._confirm_doctrines();game.tick_timer.stop();game.set_process(false)
 check(game.running and not game.testing_free_build and not game.testing_disable_failures,"normal paid/failure flags retained")
 game.marsh_npc=CountedMarsh.new();var actor=game.marsh_npc
 actor.rebuild(game);actor.active=true;actor.battery=100
 game.paused=false;game.Architects.advance_core(game,10)
 var cell:=Vector2i(20,21)
 for y in range(20,28):
  for x in range(20,28):
   var candidate:=Vector2i(x,y)
   if not game.occupied.has(candidate) and not game.wrecks.has(candidate):cell=candidate;break
  if not game.occupied.has(cell) and not game.wrecks.has(cell):break
 check(not game.occupied.has(cell) and not game.wrecks.has(cell),"unoccupied room site")
 game._place_room("cold_store",cell,true);game.powered_room_cells[cell]=true;actor.signature="";actor.rebuild(game)
 for peer in [game.bill_npc,game.veld_npc,game.branforth_npc]:peer.active=false
 var start:=Vector2.INF
 for id in actor.room_nodes.get(cell,[]):
  var point: Vector2=actor.graph.get_point_position(id)
  if actor.can_stand(point) and actor.segment_clear(point,point+Vector2(112,0)) and actor.can_stand(point+Vector2(112,0)):start=point;break
 check(start.is_finite(),"actual furnished room clears East walk envelope")
 if not start.is_finite():quit(1);return
 game.selected_room_cell=cell;game.paused=true;game._refresh_all();game.hand_panel.hide()
 var camera: Vector2=(Vector2(cell)+Vector2.ONE*.5)/float(game.GRID_SIZE)
 check(await settle_camera(camera),"observable camera/layers settle")
 var player=game.grid_view.marsh_player
 var normal_rows:Dictionary={}
 for key in ["idle-east","walk-start-east","walk-east","walk-stop-east"]:normal_rows[key]=player.frames[key].duplicate()
 player.load_manifest("res://character/marsh-east-walk-bob-contact-v1/manifest.json",true)
 check(player.frames["walk-east"].size()==6,"staged six-phase override loaded into actual grid player")
 for length in [96.0,112.0]:
  actor=CountedMarsh.new();game.marsh_npc=actor;actor.rebuild(game);actor.active=true;actor.battery=100
  actor.foot=start;actor.direction="east";actor.state="idle";actor.goal="";actor.stage="";actor.timer=10
  actor.needs={"hunger":0.0,"fatigue":0.0,"curiosity":0.0,"maintenance":0.0}
  actor.path=PackedVector2Array([start+Vector2(length,0)])
  actor._arm_selected_route();game.paused=false;player.current_key=""
  var seen:Dictionary={};var last:="";var previous:=start
  for step in range(250):
   if step>0:actor.update(game,.02);game.visual_time_seconds+=.02
   check(actor.foot.x>=previous.x-.001 and actor.foot.x<=start.x+length+.001 and absf(actor.foot.y-start.y)<.001,"actual navigation progresses on prescribed East floor route")
   previous=actor.foot
   var key:String=actor.animation_state()+"-"+actor.direction
   check(normal_rows.has(key),"actual controller remains in idle/start/walk/stop family")
   if not normal_rows.has(key):break
   var texture:Texture2D=game.grid_view._get_marsh_frame(game)
   var slot:int=player.frames[key].find(texture);check(slot>=0,"actual grid selects declared slot")
   if slot<0:break
   var old:Texture2D=normal_rows[key][slot]
   var position:Vector2=actor.foot+Vector2(0,384.0*.038)
   var scale:float=65.28/float(texture.get_meta("crew_standing_height"))
   var candidate_contact:Vector2=position+(contact(texture)-Vector2(texture.get_meta("crew_pivot")))*scale
   var normal_contact:Vector2=position+(contact(old)-Vector2(old.get_meta("crew_pivot")))*scale
   check(absf(candidate_contact.y-normal_contact.y)<.001,"candidate preserves normal source sole depth at same actor root")
   seen[key+":"+str(slot)]=true
   var snap:Dictionary=actor.snapshot();var cursor:Dictionary=player.snapshot()
   game.paused=true;actor.update(game,.25)
   check(actor.snapshot()==snap and player.snapshot()==cursor,"real pause preserves actor and selected gait cursor")
   game.paused=false
   samples.append({"length":length,"step":step,"key":key,"slot":slot,"foot":[actor.foot.x,actor.foot.y],"candidateContact":[candidate_contact.x,candidate_contact.y],"normalContact":[normal_contact.x,normal_contact.y],"depthDifference":candidate_contact.y-normal_contact.y})
   var selector:=key+":"+str(slot)
   if selector!=last:await capture("length%.0f step%d"%[length,step],key,slot,old);last=selector
   if key=="walk-east" and slot in [0,2,5] and not restored_slots.has(slot):
    var saved:Dictionary=actor.snapshot();var pixels:PackedByteArray=texture.get_image().get_data()
    check(Normal.valid_marsh_snapshot(saved),"actual normal actor validates moving snapshot")
    var fresh=CountedMarsh.new();game.marsh_npc=fresh
    await fresh.restore_snapshot(game,bytes_to_var(var_to_bytes(saved)),true)
    fresh.arrivals=actor.arrivals;actor=fresh
    check(actor.snapshot()==saved,"actual topology rebuild restores moving actor fields")
    check(player.snapshot()==cursor and game.grid_view._get_marsh_frame(game).get_image().get_data()==pixels,"moving restore retains actual grid source and gait cursor")
    restored_slots[slot]=true
   if actor.path.is_empty() and not actor.stop_active() and key=="idle-east":break
  for slot in range(6):check(seen.has("walk-east:"+str(slot)),"all six walk holds observed through actual root movement")
  for key in ["walk-start-east","walk-stop-east"]:
   for slot in range(4):check(seen.has(key+":"+str(slot)),"all start/stop join holds observed")
  check(actor.foot.is_equal_approx(start+Vector2(length,0)) and actor.path.is_empty() and actor.arrivals==1,"normal approximate arrival contract fires once")
  samples.append({"arrivalLength":length,"endpointResidual":actor.foot.distance_to(start+Vector2(length,0)),"arrivals":actor.arrivals})
 var file=FileAccess.open(OUTPUT+"report.json",FileAccess.WRITE)
 file.store_string(JSON.stringify({"checks":checks,"failures":failures,"captures":captures,"samples":samples,"normalActorRestores":restored_slots.size(),"scope":"Actual normal actor/main/grid/equipment player, staged six-phase art override only in fixture instance; two prescribed96/112unit dry East routes,20ms actual updates/visual clock, all idle/start/walk/stop joins, paired same-root normal/candidate source sole depth and native full station/source captures, pause and three moving actor-only topology restores. Default furnished cold_store, fixture room/site, peers paused; paid/failure flags normal. No autonomous goals/paid building/disk fullRunSave/TitleContinue/continuous watched cadence/full-set acceptance."},"\t"));file.close()
 print("MARSH EAST WALK WORLD: ",checks,"checks,",failures,"failures,",captures.size(),"paired captures");quit(1 if failures else 0)
