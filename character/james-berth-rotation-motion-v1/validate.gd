extends "res://character/james-rest-material-continuity-v1/validate.gd"
const DEST="res://character/james-berth-rotation-motion-v1/"
var cases:Array=[]
var records:Array=[]
var current_case:String=""
var previous_pose:String=""
func record_pose(actor,force:=false) -> void:
 var source:Texture2D=game.grid_view._get_branforth_frame_source(game)
 var player=game.grid_view.branforth_player
 var key:String=actor.animation_state()+"-"+actor.direction
 var pool:Dictionary=player.equipment_frames["diving-helmet"] if actor.helmet_equipped else player.frames
 check(pool.has(key),"Selected rest source "+key)
 if not pool.has(key):return
 var index:int=pool[key].find(source)
 check(index>=0,"Exact selected source identity "+key)
 var signature:String=key+":"+str(index)
 if not force and signature==previous_pose:return
 previous_pose=signature
 game.selected_card_id="";game.selected_room_cell=Vector2i(-1,-1)
 game._set_grid_zoom(1.3,true,(Vector2(CELL)+Vector2.ONE*.5)/40.0)
 await process_frame
 game.grid_scroll.scroll_horizontal=roundi((CELL.x+.5)*game.get_cell_size()-game.grid_scroll.size.x/2)
 game.grid_scroll.scroll_vertical=roundi((CELL.y+.5)*game.get_cell_size()-game.grid_scroll.size.y/2)
 game.grid_view.queue_redraw();await process_frame;await RenderingServer.frame_post_draw
 var file:String=DEST+"native/"+current_case+"-"+str(records.size()).pad_zeros(4)+".png"
 check(root.get_texture().get_image().save_png(file)==OK,"Chronological native pose capture")
 var foot_screen:Vector2=root.get_stretch_transform()*game.grid_view.get_global_transform_with_canvas()*(actor.foot/384.0*game.get_cell_size())
 var hash:=HashingContext.new();hash.start(HashingContext.HASH_SHA256);hash.update(source.get_image().get_data())
 records.append({"case":current_case,"key":key,"index":index,"gear":actor.helmet_equipped,"stage":actor.stage,"timer":actor.timer,"clock":game.visual_time_seconds,"foot":[actor.foot.x,actor.foot.y],"footViewport":[foot_screen.x,foot_screen.y],"visualOffset":[actor.observation_visual_offset().x,actor.observation_visual_offset().y],"headAlignment":[preload("res://scripts/crew_life.gd").head_alignment(actor,player).x,preload("res://scripts/crew_life.gd").head_alignment(actor,player).y],"pivot":source.get_meta("crew_pivot"),"standingHeight":source.get_meta("crew_standing_height"),"sourceHash":hash.finish().hex_encode(),"capture":file})
func evidence(complete:bool) -> void:
 var f:=FileAccess.open(DEST+("evidence.json" if complete else "progress-evidence.json"),FileAccess.WRITE)
 f.store_string(JSON.stringify({"checks":checks,"failures":failures,"complete":complete,"cases":cases,"records":records,"scope":"Eight actual ordinary retained-berth chooser/approach/arrival/full normal actor rest sequences across four room rotations and both prescribed initial gears. Chronological source changes captured, including repeated breathing cycles; all20ms simulation samples check navigation/contact. Initial foot/need/gear/room fixture resets, isolated retained authored crew_hab view with no Studio overrides. No genuine gear acquisition, special East station-prop bunk, disk Continue, traffic/hazard/owner-layout or continuous native-video acceptance."},"  "))
func run() -> void:
 var expected:=OS.get_environment("APPDATA").path_join("Godot/app_userdata/BrineSpace").replace("\\","/")
 if DisplayServer.get_name()=="headless" or not "brine-james-native-" in OS.get_environment("APPDATA") or OS.get_user_data_dir().replace("\\","/").to_lower()!=expected.to_lower():quit(3);return
 root.size=Vector2i(1600,900);DirAccess.make_dir_recursive_absolute(DEST+"native")
 await fresh_scene();game.running=true;game.paused=false;game.Architects.advance_core(game,10)
 check(game.recovered_crew.any(func(member):return member.get("architect_id","")=="branforth"),"Actual James core release")
 for mode in ["bare","helmet"]:
  for quarter in range(4):
   current_case=mode+"-q"+str(quarter);previous_pose=""
   game.occupied.clear();game.placed_rooms.clear();game.powered_room_cells.clear();game.wrecks.clear();game.selected_rotation=quarter;game._place_room("crew_hab",CELL,true);game.powered_room_cells[CELL]=true
   for peer in [game.bill_npc,game.veld_npc,game.marsh_npc]:peer.active=false
   var actor=game.branforth_npc;actor.rebuild(game);actor.active=true;actor.dead=false;actor.helmet_equipped=mode=="helmet";actor.movement_medium="dry";actor.breath_oxygen=15;actor.tank_oxygen=60;actor.air_recovery=0;actor.bunk_motion.clear();actor.path.clear();actor.goal="";actor.stage="";actor.state="idle";actor.timer=0
   var center:Vector2=(Vector2(CELL)+Vector2.ONE*.5)*384;var node:int=actor.nearest_in_room(center,CELL,false)
   check(node>=0,"Valid initial room node "+current_case)
   if node<0:evidence(false);quit(2);return
   actor.foot=actor.graph.get_point_position(node);actor.direction="south"
   for need in actor.needs:actor.needs[need]=0.0
   actor.needs.fatigue=100;actor.service_preferences.fatigue=["crew_hab"];actor.decision_rng=RandomNumberGenerator.new();actor.decision_rng.seed=881
   actor.choose_goal(game);check(actor.goal=="fatigue" and actor.goal_cell==CELL and not actor.path.is_empty(),"Normal chooser selects a routed berth "+current_case)
   if actor.path.is_empty():evidence(false);quit(2);return
   var final_heading:String=actor.travel_heading(actor.path[-2] if actor.path.size()>1 else actor.foot,actor.path[-1],actor.direction)
   var travelled:=0.0;game.visual_time_seconds=100;game.grid_view.branforth_player.current_key="";game.grid_view.branforth_player.motion.clear()
   for step in range(4000):
    if actor.path.is_empty():break
    var old:Vector2=actor.foot;actor.move(.02);game.visual_time_seconds+=.02
    travelled+=old.distance_to(actor.foot);check(actor.segment_clear(old,actor.foot),"Actual approach stays clear")
   check(actor.path.is_empty() and actor.stage=="life_lie" and not actor.bunk_motion_active(),"Actual arrival starts ordinary lying "+current_case)
   if actor.stage!="life_lie":evidence(false);quit(2);return
   var arrival_facing:String=actor.direction;var foot:Vector2=actor.foot;var completed_before:int=actor.completed_activity.get("serial",0);var start:float=game.visual_time_seconds;var seen:Dictionary={};var samples:=0
   await record_pose(actor,true)
   for step in range(800):
    actor.update(game,.02);game.visual_time_seconds+=.02;samples+=1
    check(actor.foot==foot,"Rest navigation contact remains planted")
    check(actor.direction==arrival_facing and actor.helmet_equipped==(mode=="helmet"),"Rest facing/gear stable")
    var source:Texture2D=game.grid_view._get_branforth_frame_source(game);var key:String=actor.animation_state()+"-"+actor.direction;var pool:Dictionary=game.grid_view.branforth_player.equipment_frames["diving-helmet"] if mode=="helmet" else game.grid_view.branforth_player.frames
    if actor.stage in ["life_lie","life_sleep","life_get_up"]:seen[key+":"+str(pool[key].find(source))]=true
    await record_pose(actor)
    if actor.stage.is_empty():break
   check(actor.stage.is_empty() and int(actor.completed_activity.get("serial",0))==completed_before+1,"One ordinary rest completion "+current_case)
   check(actor.needs.fatigue<60 and actor.completed_activity.get("activity","")=="resting in the berth","Normal fatigue relief/event")
   for action in ["lie-down","sleep","get-up"]:
    for index in range(6):check(seen.has(action+"-"+arrival_facing+":"+str(index)),"Every actual selected rest slot "+action+str(index))
   cases.append({"id":current_case,"rotation":quarter,"gear":mode,"travelled":travelled,"finalRouteHeading":final_heading,"arrivalFacing":arrival_facing,"instantFacingChange":final_heading!=arrival_facing,"samples":samples,"sourceSlots":seen.size(),"duration":game.visual_time_seconds-start,"completed":actor.stage.is_empty(),"fatigueAfter":actor.needs.fatigue})
   print("JAMES BERTH ROTATION CASE ",current_case," complete=true facingJump=",final_heading!=arrival_facing);evidence(false)
   if failures:quit(2);return
 evidence(true)
 if not FileAccess.file_exists(get_script().resource_path+".uid"):
  var uid:=FileAccess.open(get_script().resource_path+".uid",FileAccess.WRITE);uid.store_line(ResourceUID.id_to_text(ResourceUID.create_id()))
 print("JAMES BERTH ROTATION: ",checks," checks; ",failures," failures; ",cases.size()," actual full rest journeys")
 quit(1 if failures else 0)
