extends "res://tests/test_marsh_battery.gd"
const DEST="res://character/james-east-bunk-lifecycle-v1/"
const HAB=Vector2i(20,22)
var checks:=0
var cases:Array=[]
var records:Array=[]
var checkpoints:Array=[]
var previous_pose:String=""
var current_case:String=""
func check(ok:bool,message:String):
 checks+=1
 if not ok:failures+=1;push_error(message)
func fresh_scene() -> void:
 if is_instance_valid(game):root.remove_child(game);game.queue_free();await process_frame
 var store=preload("res://scripts/room_layout_store.gd");store.loaded=true;store.data={}
 game=load("res://scenes/main.tscn").instantiate();game.set_meta("authored_site_fixture",true)
 game.meta.save_path="user://james-bunk-life.meta";game.run_save_path="user://james-bunk-life.loop"
 game.meta.unlocked_architect_ids={"bill":true,"branforth":true};game.meta.selected_architect="branforth"
 root.add_child(game);current_scene=game
 while not game.startup_complete:await process_frame
 game.set_process(false);game.tick_timer.stop();game.crew_comms.set_process(false);game.crew_comms.dismiss()
func settle() -> void:
 game.selected_card_id="";game.selected_room_cell=Vector2i(-1,-1)
 if not game.hand_collapsed:game._toggle_hand_collapsed()
 game._set_grid_zoom(1.6,true,(Vector2(HAB)+Vector2.ONE*.5)/40.0)
 var center:Vector2=(Vector2(HAB)+Vector2.ONE*.5)/40.0
 for step in range(120):
  await process_frame
  game.inspector_focus_button.set_meta("cell",HAB);game._focus_inspected_room()
  if step>=3 and game._grid_view_center_ratio().distance_to(center)<.002 and game.grid_view.pending_layers.is_empty() and not game.grid_view.zoom_preparing and not game.grid_view.zoom_settling:break
 check(game._grid_view_center_ratio().distance_to(center)<.002,"Actual bunk camera centered after deferred layout")
func capture_pose(actor,force:=false) -> void:
 var source:Texture2D=game.grid_view._get_branforth_frame_source(game)
 var key:String=actor.animation_state()+"-"+actor.direction
 var pool:Dictionary=game.grid_view.branforth_player.equipment_frames["diving-helmet"] if actor.helmet_equipped else game.grid_view.branforth_player.frames
 var index:int=pool[key].find(source);check(index>=0,"Exact selected bunk source "+key)
 var token:String=key+":"+str(index)
 if not force and token==previous_pose:return
 previous_pose=token
 game.grid_view.queue_redraw();await process_frame;await RenderingServer.frame_post_draw
 var file:String=DEST+"native/"+current_case+"-"+str(records.size()).pad_zeros(4)+".png"
 check(root.get_texture().get_image().save_png(file)==OK,"Actual bunk lifecycle capture")
 var pt:Vector2=root.get_stretch_transform()*game.grid_view.get_global_transform_with_canvas()*(actor.foot/384.0*game.get_cell_size())
 check(Rect2(Vector2(0,150),Vector2(1600,700)).has_point(pt),"Actual bunk actor visible in native capture")
 records.append({"case":current_case,"key":key,"index":index,"gear":actor.helmet_equipped,"stage":actor.stage,"timer":actor.timer,"clock":game.visual_time_seconds,"foot":[actor.foot.x,actor.foot.y],"footViewport":[pt.x,pt.y],"offset":[actor.observation_visual_offset().x,actor.observation_visual_offset().y],"capture":file})
func save_checkpoint(actor,phase:String) -> void:
 var was_paused:bool=game.paused;game.paused=true
 var item:Dictionary={"id":current_case+"-"+phase,"phase":phase,"actor":actor.snapshot().duplicate(true),"player":game.grid_view.branforth_player.snapshot().duplicate(true),"clock":game.visual_time_seconds,"resources":game.resources.duplicate(true),"pixels":game.grid_view._get_branforth_frame_source(game).get_image().get_data(),"offset":actor.observation_visual_offset()}
 item.path="user://"+item.id+".loop"
 check(Save.problem(Save.capture(game)).is_empty(),"Bunk disk checkpoint valid")
 check(Save.write(game,item.path)==OK and not Save.read(item.path).is_empty(),"Bunk checkpoint writes/reads scratch disk")
 checkpoints.append(item);game.paused=was_paused
func evidence(complete:bool) -> void:
 var f:=FileAccess.open(DEST+"evidence.json",FileAccess.WRITE)
 f.store_string(JSON.stringify({"complete":complete,"checks":checks,"failures":failures,"cases":cases,"records":records,"scope":"Default authored unmirrored East station-prop bunk q3, no Studio overrides. Two normal chooser/clear approach/full rest journeys with prescribed initial gears. Six actual mid-entry/sleep/exit disk checkpoints restored into fresh main scenes, exact actor/player/pixels/offset/pause/resources, followed by actual power loss and normal update return. Not all bunk layouts/rotations, gear acquisition, traffic/hazards or continuous native-video acceptance."},"  "))
func run() -> void:
 var expected:=OS.get_environment("APPDATA").path_join("Godot/app_userdata/BrineSpace").replace("\\","/")
 if DisplayServer.get_name()=="headless" or not "brine-james-native-" in OS.get_environment("APPDATA") or OS.get_user_data_dir().replace("\\","/").to_lower()!=expected.to_lower():quit(3);return
 root.size=Vector2i(1600,900);DirAccess.make_dir_recursive_absolute(DEST+"native")
 for gear in [false,true]:
  await fresh_scene();game.running=true;game.paused=false;game.Architects.advance_core(game,10)
  game.wrecks.erase(HAB);game._place_room("corridor",Vector2i(20,21),true);game._place_room("crew_hab",HAB,true);game.occupied[HAB].rotation=3;game.powered_room_cells[HAB]=true
  for peer in [game.bill_npc,game.veld_npc,game.marsh_npc]:peer.active=false
  var actor=game.branforth_npc;actor.rebuild(game);actor.active=true;actor.helmet_equipped=gear
  var stations:Array=actor.RoomActivity.stations(actor.geometry[HAB]).filter(func(s):return s.get("branforth_bunk",false))
  check(not stations.is_empty(),"Current actual authored East bunk available")
  if stations.is_empty():evidence(false);quit(2);return
  var center:Vector2=(Vector2(HAB)+Vector2.ONE*.5)*384
  var node:int=actor.nearest_in_room(center+Vector2(0,130),HAB)
  check(node>=0,"Clear actual approach start")
  if node<0:evidence(false);quit(2);return
  actor.foot=actor.graph.get_point_position(node);actor.path.clear();actor.goal="";actor.stage="";actor.timer=0;actor.state="idle"
  for need in actor.needs:actor.needs[need]=100.0 if need=="fatigue" else 0.0
  actor.decision_rng.seed=8923;actor.choose_goal(game)
  check(actor.goal=="fatigue" and actor.goal_cell==HAB and not actor.path.is_empty(),"Normal chooser routes to actual East bunk")
  game.visual_time_seconds=100
  for step in range(4000):
   if actor.path.is_empty():break
   var old:Vector2=actor.foot;actor.move(.02);game.visual_time_seconds+=.02;check(actor.segment_clear(old,actor.foot),"Genuine bunk approach clear")
  check(actor.path.is_empty() and actor.bunk_motion_active() and actor.stage=="life_lie" and actor.direction=="east","Automatic actual arrival selects specialized bunk")
  if not actor.bunk_motion_active():evidence(false);quit(2);return
  current_case=("helmet" if gear else "bare")+"-normal";previous_pose="";await settle();await capture_pose(actor,true)
  var foot:Vector2=actor.foot;var serial:int=actor.completed_activity.get("serial",0);var seen:Dictionary={};var saved:Dictionary={}
  for step in range(1000):
   actor.update(game,.02);game.visual_time_seconds+=.02
   check(actor.foot==foot and actor.direction=="east" and actor.helmet_equipped==gear,"Actual bunk navigation/gear/facing stable")
   await capture_pose(actor)
   if actor.bunk_motion_active():
    var key:String=actor.animation_state()+"-east";var pool:Dictionary=game.grid_view.branforth_player.equipment_frames["diving-helmet"] if gear else game.grid_view.branforth_player.frames
    seen[key+":"+str(pool[key].find(game.grid_view._get_branforth_frame_source(game)))]=true
   var phase:String="entry" if actor.stage=="life_lie" and actor.timer<1.28 else ("sleep" if actor.stage=="life_sleep" and actor.timer<6.6 else ("exit" if actor.stage=="life_get_up" and actor.timer<1.04 else ""))
   if not phase.is_empty() and not saved.has(phase):saved[phase]=true;await save_checkpoint(actor,phase)
   if actor.stage.is_empty():break
  check(actor.stage.is_empty() and actor.completed_activity.get("serial",0)==serial+1 and actor.needs.fatigue<60,"Actual full rest completion and fatigue relief")
  for action in ["bunk-enter","bunk-exit"]:
   for i in range(7):check(seen.has(action+"-east:"+str(i)),"Actual authored bunk slot "+action+str(i))
  check(seen.has("bunk-sleep-east:0") and saved.size()==3,"Sleep and all three disk phase checkpoints")
  cases.append({"id":current_case,"kind":"normal","sourceSlots":seen.size(),"fatigueAfter":actor.needs.fatigue,"completed":actor.stage.is_empty()});evidence(false)
  print("JAMES EAST BUNK NORMAL ",current_case," complete=",actor.stage.is_empty())
 for item in checkpoints:
  await fresh_scene();var disk:Dictionary=Save.read(item.path)
  check(await Save.restore_staged(game,disk),"Actual bunk disk restores fresh main")
  game.run_save_path=item.path;game.set_process(false);game.tick_timer.stop();game.crew_comms.set_process(false);game.crew_comms.dismiss()
  var actor=game.branforth_npc
  check(actor.snapshot()==item.actor and game.grid_view.branforth_player.snapshot()==item.player,"Fresh Continue exact actor and player")
  check(game.paused and game.visual_time_seconds==item.clock and game.resources==item.resources,"Fresh Continue pause/clock/all resources")
  check(game.grid_view._get_branforth_frame_source(game).get_image().get_data()==item.pixels and actor.observation_visual_offset()==item.offset,"Fresh Continue exact source and furniture offset")
  game._process(.5);check(actor.snapshot()==item.actor and game.visual_time_seconds==item.clock,"Paused fresh bunk Continue freezes")
  current_case=item.id+"-continue-power";previous_pose="";await settle();await capture_pose(actor,true);game.paused=false
  var old_stage:String=actor.stage;var old_serial:int=actor.completed_activity.get("serial",0);var foot:Vector2=actor.foot
  game.powered_room_cells.erase(HAB);actor.update(game,.02);game.visual_time_seconds+=.02
  var retained_exit:bool=actor.stage=="life_get_up" and actor.bunk_motion_active()
  check(retained_exit,"Power loss retains visible bunk return from "+old_stage)
  if old_stage=="life_get_up":check(absf(actor.timer-(float(item.actor.timer)-.02))<.0001,"Power loss preserves existing return clock")
  await capture_pose(actor,true)
  for step in range(200):
   if actor.stage.is_empty():break
   actor.update(game,.02);game.visual_time_seconds+=.02;check(actor.foot==foot,"Interrupted bunk foot remains planted");await capture_pose(actor)
  check(actor.stage.is_empty() and actor.completed_activity.get("serial",0)==old_serial,"Interrupted return ends without false rest event")
  cases.append({"id":current_case,"kind":"fresh-disk-continue-power","phase":item.phase,"retainedExit":retained_exit,"completed":actor.stage.is_empty()});evidence(false)
  print("JAMES EAST BUNK CONTINUE ",current_case," retainedExit=",retained_exit)
 evidence(true)
 if not FileAccess.file_exists(get_script().resource_path+".uid"):
  var uid:=FileAccess.open(get_script().resource_path+".uid",FileAccess.WRITE);uid.store_line(ResourceUID.id_to_text(ResourceUID.create_id()))
 print("JAMES EAST BUNK LIFECYCLE: ",checks," checks; ",failures," failures; ",records.size()," captures")
 quit(1 if failures else 0)
